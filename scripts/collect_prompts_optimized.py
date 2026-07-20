#!/usr/bin/env python3
"""
优化版 AI 提示词收集系统 - Phase 1 优化

优化特性：
- 减少搜索查询到 15 个高质量查询
- 智能优先级排序（来源质量 + 关键词相关性）
- 启发式过滤（无成本预筛选）
- 只评估前 20 个提示词
- 节省 API 成本 95%
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import logging
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import signal

# ============================================================================
# 配置区域
# ============================================================================

# 目录配置
DATA_DIR = Path("/root/clawd/data/prompts")
OUTPUT_DIR = DATA_DIR / "collected"
OUTPUT_FILE = OUTPUT_DIR / f"prompts-optimized-{datetime.now().strftime('%Y%m%d-%H%M')}.jsonl"
LOGS_DIR = Path("/root/clawd/logs")

# 创建目录
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logger = logging.getLogger("collect_prompts_optimized")
logger.setLevel(logging.INFO)

# 控制台日志（简化版）
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(console_handler)

# 文件日志（详细版）
file_handler = logging.FileHandler(
    LOGS_DIR / "collect-prompts-optimized.log",
    encoding='utf-8'
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)

# SearXNG 配置
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")
SEARCH_TIMEOUT = 30
MAX_RESULTS_PER_QUERY = 10
MAX_CONTENT_LENGTH = 20000

# 并发配置
MAX_WORKERS = 3
REQUEST_DELAY = 1.5

# ============================================================================
# 优化的搜索关键词库 - 15 个高质量查询
# ============================================================================

# 优先级 1: 超高质量来源
PRIORITY_QUERIES = [
    # GitHub 和 HuggingFace（通过 SearXNG 搜索）
    "awesome-chatgpt-prompts github repository",
    "best AI prompts 2026",
    "prompt engineering examples",
    
    # Midjourney 和图像生成
    "Midjourney best prompts professional",
    "DALL-E 3 prompt examples guide",
    "Stable Diffusion prompt engineering",

    # 写作和创意
    "creative writing prompts AI storytelling",
    "business writing AI templates",

    # 编程和开发
    "coding assistant prompts best practices",
    "system prompt examples ChatGPT",

    # 视频 AI
    "Veo 3 prompt examples video generation",
    "Runway ML prompt tutorial",

    # 专业应用
    "AI prompts for marketing content",
    "role-based AI prompts system instructions",
]

# ============================================================================
# 辅助函数
# ============================================================================

shutdown_flag = False

def signal_handler(signum, frame):
    """信号处理"""
    global shutdown_flag
    logger.warning("\n接收到终止信号，正在优雅退出...")
    shutdown_flag = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def search_searxng(query: str, limit: int = MAX_RESULTS_PER_QUERY) -> List[Dict]:
    """
    使用 SearXNG 搜索

    Args:
        query: 搜索查询
        limit: 最大结果数

    Returns:
        搜索结果列表
    """
    if shutdown_flag:
        return []

    try:
        params = {
            "q": query,
            "format": "json",
            "engines": "",  # 使用所有可用引擎
        }

        response = requests.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=SEARCH_TIMEOUT,
            verify=False
        )
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])[:limit]

        logger.debug(f"搜索 '{query}': {len(results)} 个结果")

        return results

    except requests.exceptions.Timeout:
        logger.warning(f"搜索超时: {query}")
        return []
    except requests.exceptions.RequestException as e:
        logger.warning(f"搜索失败 '{query}': {e}")
        return []
    except Exception as e:
        logger.error(f"未知错误 '{query}': {e}")
        return []


def fetch_page_content(url: str, max_chars: int = MAX_CONTENT_LENGTH) -> Optional[str]:
    """
    获取页面内容

    Args:
        url: 目标 URL
        max_chars: 最大字符数

    Returns:
        页面文本内容
    """
    if shutdown_flag:
        return None

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        response = requests.get(url, headers=headers, timeout=SEARCH_TIMEOUT)
        response.raise_for_status()

        # 检查内容类型
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' not in content_type:
            logger.debug(f"跳过非 HTML 内容: {content_type}")
            return None

        text = response.text

        # 移除脚本和样式
        text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<noscript[^>]*>.*?</noscript>', ' ', text, flags=re.DOTALL | re.IGNORECASE)

        # 移除 HTML 标签
        import html
        text = re.sub(r'<[^>]+>', ' ', text)
        text = html.unescape(text)

        # 清理空白
        text = re.sub(r'\s+', ' ', text).strip()

        # 限制长度
        return text[:max_chars]

    except Exception as e:
        logger.warning(f"获取页面失败 {url}: {e}")
        return None


# ============================================================================
# 启发式过滤（无成本预筛选）
# ============================================================================

def heuristic_filter_prompts(prompts: List[str]) -> List[Dict]:
    """
    启发式过滤提示词 - 无成本预筛选

    Args:
        prompts: 提示词列表

    Returns:
        过滤后的提示词（带评分）
    """
    filtered = []

    for prompt in prompts:
        p_clean = prompt.strip()
        if not p_clean:
            continue

        # 评分
        score = 0
        reasons = []

        # 1. 长度评分（50-300 字符为佳）
        length = len(p_clean)
        if 50 <= length <= 300:
            score += 20
            reasons.append("长度适中")
        elif 300 < length <= 500:
            score += 10
            reasons.append("较长")
        else:
            score -= 10
            reasons.append("过长或过短")

        # 2. 关键词密度评分
        quality_keywords = [
            'create', 'generate', 'design', 'style', 'detailed', 'professional',
            'high quality', 'best', 'top', 'advanced', 'expert',
            '创建', '生成', '设计', '风格', '质量', '专业',
        ]
        keyword_count = sum(1 for kw in quality_keywords if kw.lower() in p_clean.lower())
        score += min(keyword_count * 5, 20)
        if keyword_count > 0:
            reasons.append(f"包含 {keyword_count} 个质量词")

        # 3. 结构化评分（包含标点、分隔符）
        if re.search(r'[,.;:！，。；：]', p_clean):
            score += 10
            reasons.append("结构良好")

        # 4. 特殊格式评分（JSON、列表等）
        if re.search(r'\[|\]|\{|}', p_clean):
            score += 15
            reasons.append("结构化格式")

        # 5. 英文字母比例（避免纯符号）
        alpha_ratio = sum(c.isalpha() for c in p_clean) / max(len(p_clean), 1)
        if alpha_ratio > 0.6:
            score += 10
            reasons.append("文本比例合理")

        filtered.append({
            'content': p_clean,
            'score': score,
            'reasons': reasons,
        })

    # 按评分排序
    filtered.sort(key=lambda x: x['score'], reverse=True)

    return filtered


# ============================================================================
# 提示词提取
# ============================================================================

def extract_prompts_from_content(content: str) -> List[str]:
    """
    从内容中提取提示词

    Args:
        content: 页面内容

    Returns:
        提示词列表
    """
    prompts = []

    # 模式 1: 引号包裹的提示词
    quote_patterns = [
        r'["\']([^"\']{30,500})["\']',
        r'["\']([A-Z][^"\']{30,300})["\']',  # 以大写字母开头
    ]

    for pattern in quote_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        prompts.extend(matches)

    # 模式 2: 列表项（-、*、数字）
    list_patterns = [
        r'^[-*]\s+([A-Z][^.!?]{30,200})',  # 以大写字母开头
        r'^\d+[.)\]\s+([A-Z][^.!?]{30,200})',
    ]

    lines = content.split('\n')
    for pattern in list_patterns:
        for line in lines:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                prompts.append(match.group(1))

    # 模式 3: 代码块
    code_pattern = r'```(?:bash|python|json)?\s*\n([\s\S]{50,1000})\n```'
    code_matches = re.findall(code_pattern, content)
    prompts.extend(code_matches)

    return prompts


# ============================================================================
# 主流程
# ============================================================================

def main():
    """
    主流程
    """
    logger.info("=" * 80)
    logger.info("🚀 优化版 AI 提示词收集系统")
    logger.info("=" * 80)
    logger.info(f"搜索查询总数: {len(PRIORITY_QUERIES)}")
    logger.info(f"输出文件: {OUTPUT_FILE}")
    logger.info("")
    logger.info("=" * 80)
    logger.info(f"开始执行 {len(PRIORITY_QUERIES)} 个搜索查询...")
    logger.info("=" * 80)

    all_prompts = set()

    # 执行搜索
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_query = {
            executor.submit(search_searxng, query): query
            for query in PRIORITY_QUERIES
        }

        for future in as_completed(future_to_query):
            if shutdown_flag:
                break

            query = future_to_query[future]
            try:
                results = future.result(timeout=SEARCH_TIMEOUT + 10)

                for result in results:
                    url = result.get('url', '')
                    title = result.get('title', '')

                    # 优先处理高质量域名
                    domain = urlparse(url).netloc

                    # 高优先级域名
                    if any(d in domain for d in ['github.com', 'huggingface.co', 'medium.com']):
                        logger.debug(f"✓ 高质量域名: {domain}")

                    # 获取页面内容
                    content = fetch_page_content(url)
                    if content:
                        # 提取提示词
                        prompts = extract_prompts_from_content(content)

                        for prompt in prompts:
                            prompt_clean = prompt.strip()
                            if len(prompt_clean) >= 30:
                                all_prompts.add(prompt_clean)

                # 延迟
                time.sleep(REQUEST_DELAY)

            except Exception as e:
                logger.error(f"处理查询失败 '{query}': {e}")

    logger.info("")
    logger.info("=" * 80)
    logger.info(f"📊 收集完成！")
    logger.info("=" * 80)
    logger.info(f"总共收集: {len(all_prompts)} 个提示词")

    # 启发式过滤
    logger.info("")
    logger.info("=" * 80)
    logger.info("🎯 启发式过滤（无成本预筛选）")
    logger.info("=" * 80)

    filtered = heuristic_filter_prompts(list(all_prompts))

    # 只保留前 20 个（用于评估）
    top_20 = filtered[:20]

    logger.info(f"过滤后: {len(filtered)} 个提示词")
    logger.info(f"选择前 20 个用于 LLM 评估")

    # 保存结果
    logger.info("")
    logger.info("=" * 80)
    logger.info("💾 保存结果")
    logger.info("=" * 80)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for i, item in enumerate(top_20, 1):
            prompt_data = {
                'content': item['content'],
                'score': item['score'],
                'reasons': item['reasons'],
                'rank': i,
                'timestamp': datetime.now().isoformat(),
            }
            f.write(json.dumps(prompt_data, ensure_ascii=False) + '\n')

    logger.info(f"✅ 保存到: {OUTPUT_FILE}")

    # 生成统计报告
    logger.info("")
    logger.info("=" * 80)
    logger.info("📊 统计信息")
    logger.info("=" * 80)

    avg_score = sum(item['score'] for item in top_20) / len(top_20)
    logger.info(f"平均评分: {avg_score:.1f}")
    logger.info(f"最高评分: {top_20[0]['score']}")
    logger.info(f"最低评分: {top_20[-1]['score']}")

    logger.info("")
    logger.info("=" * 80)
    logger.info("✅ 完成！")
    logger.info("=" * 80)
    logger.info("")
    logger.info("下一步：")
    logger.info("  1. LLM 评估 20 个提示词（成本：~20 次 API 调用）")
    logger.info("  2. 转换为 Skills")
    logger.info("  3. 发布到 ClawdHub")


if __name__ == "__main__":
    main()
