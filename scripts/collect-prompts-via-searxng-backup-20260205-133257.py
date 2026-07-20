#!/usr/bin/env python3
"""
使用 SearXNG 搜索高质量 AI 提示词

功能特性：
- 使用本地 SearXNG 实例搜索 AI 提示词
- 从多个来源收集提示词（GitHub、博客、专业网站）
- 高质量提取和验证
- 支持多种搜索策略
"""

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging
import requests

# 配置
DATA_DIR = Path("/root/clawd/data/prompts")
OUTPUT_DIR = DATA_DIR / "collected"
OUTPUT_FILE = OUTPUT_DIR / f"prompts-from-searxng-{datetime.now().strftime('%Y%m%d')}.jsonl"
LOGS_DIR = Path("/root/clawd/logs")

# 创建目录
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logger = logging.getLogger("collect_prompts_searxng")
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(LOGS_DIR / "collect-prompts-searxng.log", encoding='utf-8')
log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(log_handler)
logger.addHandler(logging.StreamHandler())

# SearXNG 配置
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")

# 搜索关键词 - 针对高质量来源
SEARCH_QUERIES = [
    # 专业提示词网站
    "PromptBase best prompts",
    "awesome-chatgpt-prompts github",
    "LearnPrompting engineering guide",

    # 技术博客和教程
    "Midjourney prompt tutorial examples",
    "DALL-E 3 prompt examples guide",
    "Stable Diffusion prompt engineering",
    "AI art prompt best practices",

    # GitHub 资源
    "site:github.com \"prompt engineering\"",
    "site:github.com \"AI prompts\"",
    "site:github.com \"ChatGPT prompts\"",

    # 技术平台
    "site:medium.com \"prompt engineering\"",
    "site:dev.to \"AI prompts\"",
    "site:hashnode.com \"prompt guide\"",

    # 视频生成
    "Runway ML prompt examples",
    "Pika Labs prompt guide",
    "Kling AI prompt examples",
    "Veo video prompts",

    # 特定用途
    "professional ChatGPT prompts",
    "business AI prompt templates",
    "educational AI prompts",
]

# 高质量域名白名单
HIGH_QUALITY_DOMAINS = {
    'github.com',
    'promptbase.com',
    'learnprompting.org',
    'midjourney.com',
    'openai.com',
    'stability.ai',
    'huggingface.co',
    'medium.com',
    'dev.to',
    'hashnode.com',
    'towardsdatascience.com',
    'analyticsvidhya.com',
}

# 低质量域名黑名单
LOW_QUALITY_DOMAINS = {
    'pinterest.com',  # 太多低质量图片
    'instagram.com',  # 社交媒体
    'tiktok.com',  # 社交媒体
    'facebook.com',  # 社交媒体
    'twitter.com',  # 社交媒体（使用 twitter-search skill）
}


def search_searxng(query: str, limit: int = 10) -> List[Dict]:
    """
    使用 SearXNG 搜索

    Args:
        query: 搜索查询
        limit: 返回结果数量

    Returns:
        搜索结果列表
    """
    params = {
        "q": query,
        "format": "json",
        "categories": "general",
    }

    try:
        response = requests.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=30,
            verify=False
        )
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])[:limit]

        logger.info(f"搜索 '{query}': 找到 {len(results)} 个结果")

        return results

    except Exception as e:
        logger.error(f"搜索失败 '{query}': {e}")
        return []


def is_high_quality_url(url: str) -> bool:
    """
    判断 URL 是否来自高质量来源

    Args:
        url: 目标 URL

    Returns:
        是否为高质量来源
    """
    from urllib.parse import urlparse

    try:
        domain = urlparse(url).netloc.lower()

        # 检查黑名单
        if any(blacklisted in domain for blacklisted in LOW_QUALITY_DOMAINS):
            return False

        # 检查白名单
        if any(whitelisted in domain for whitelisted in HIGH_QUALITY_DOMAINS):
            return True

        # 默认允许
        return True

    except Exception:
        return True


def fetch_page_content(url: str, max_chars: int = 15000) -> Optional[str]:
    """
    获取页面内容

    Args:
        url: 目标 URL
        max_chars: 最大字符数

    Returns:
        页面文本内容
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        text = response.text

        # 移除 HTML 标签
        import html
        text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = html.unescape(text)

        # 清理空白
        text = re.sub(r'\s+', ' ', text).strip()

        return text[:max_chars]

    except Exception as e:
        logger.warning(f"获取页面失败 {url}: {e}")
        return None


def extract_prompts_from_content(content: str, max_prompts: int = 15) -> List[str]:
    """
    从内容中提取提示词

    Args:
        content: 页面内容
        max_prompts: 最大提取数量

    Returns:
        提示词列表
    """
    prompts = []

    # 模式 1: 引号中的内容（更严格的匹配）
    quote_patterns = [
        r'"([^"]{40,800})"',  # 双引号，较长
        r"'([^']{40,800})",   # 单引号
        r'`([^`]{40,800})`',  # 反引号
    ]

    for pattern in quote_patterns:
        matches = re.findall(pattern, content)
        prompts.extend(matches)

    # 模式 2: 冒号后面的描述性文本
    colon_patterns = [
        r'(?:prompt|Prompt|PROMPT|example|Example)[\s:]+([^.!?]{40,800})',
        r'(?:prompt|Prompt|PROMPT)\s*[:=]\s*([^\n]{40,800})',
    ]

    for pattern in colon_patterns:
        matches = re.findall(pattern, content)
        prompts.extend(matches)

    # 模式 3: 编号列表（适合教程类内容）
    list_patterns = [
        r'\d+\.\s+([^.!?]{40,800})',
        r'[-*]\s+([^.!?]{40,800})',
    ]

    for pattern in list_patterns:
        matches = re.findall(pattern, content)
        prompts.extend(matches)

    # 去重
    unique_prompts = list(dict.fromkeys(prompts))

    # 过滤质量
    filtered = []
    for p in unique_prompts:
        p_clean = p.strip()

        # 长度过滤
        if not (40 <= len(p_clean) <= 800):
            continue

        # 内容质量过滤
        # 检查是否包含足够的字母数字
        alpha_ratio = sum(c.isalnum() or c.isspace() for c in p_clean) / len(p_clean)
        if alpha_ratio < 0.7:
            continue

        # 检查是否包含动作动词
        action_verbs = ['generate', 'write', 'create', 'design', 'build', 'make', 'act as', 'role', 'task']
        has_action = any(verb.lower() in p_clean.lower() for verb in action_verbs)
        if not has_action:
            continue

        # 检查是否包含截断标记
        truncation_markers = ['...', '# 1', 'Read more', 'continue reading', 'click to continue']
        if any(marker.lower() in p_clean.lower() for marker in truncation_markers):
            continue

        filtered.append(p_clean)

    return filtered[:max_prompts]


def classify_prompt_type(prompt: str) -> str:
    """
    分类提示词类型

    Args:
        prompt: 提示词文本

    Returns:
        提示词类型
    """
    prompt_lower = prompt.lower()

    image_keywords = [
        'image', 'photo', 'picture', 'portrait', 'painting', 'drawing',
        'illustration', 'midjourney', 'dall-e', 'stable diffusion',
        'render', 'visual', 'art', 'scene', 'landscape'
    ]

    video_keywords = [
        'video', 'animation', 'motion', 'animate', 'runway', 'pika',
        'kling', 'veo', 'clip', 'footage', 'film'
    ]

    text_keywords = [
        'write', 'essay', 'article', 'blog', 'content', 'story',
        'chatgpt', 'gpt', 'llm', 'text generation'
    ]

    image_score = sum(1 for kw in image_keywords if kw in prompt_lower)
    video_score = sum(1 for kw in video_keywords if kw in prompt_lower)
    text_score = sum(1 for kw in text_keywords if kw in prompt_lower)

    if video_score > image_score and video_score > text_score:
        return 'video-generation'
    elif image_score > text_score:
        return 'image-generation'
    elif text_score > 0:
        return 'text-generation'
    else:
        return 'general'


def calculate_quality_score(prompt: str) -> int:
    """
    计算提示词质量分数

    Args:
        prompt: 提示词文本

    Returns:
        质量分数 (0-100)
    """
    score = 0

    # 长度评分
    length = len(prompt)
    if 50 <= length <= 300:
        score += 30
    elif 301 <= length <= 500:
        score += 25
    elif 501 <= length <= 800:
        score += 15
    else:
        score += 5

    # 关键词评分
    quality_keywords = [
        'detailed', 'realistic', 'high quality', 'professional', 'creative',
        'specific', 'precise', 'clear', 'comprehensive', 'well-structured'
    ]
    score += min(20, sum(5 for kw in quality_keywords if kw in prompt.lower()))

    # 动作动词评分
    action_verbs = ['generate', 'create', 'write', 'design', 'build', 'make', 'develop']
    score += min(15, sum(5 for verb in action_verbs if verb in prompt.lower()))

    # 结构评分
    if ',' in prompt:
        score += 10
    if ':' in prompt:
        score += 5
    if '\n' in prompt:
        score += 10

    # 描述性词汇
    descriptive_words = [
        'with', 'featuring', 'including', 'showing', 'displaying', 'depicting'
    ]
    score += min(10, sum(2 for word in descriptive_words if word in prompt.lower()))

    return min(100, score)


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🔍 开始使用 SearXNG 搜索高质量 AI 提示词")
    logger.info("=" * 80)

    # 存储所有收集的提示词
    all_prompts = []
    seen_urls = set()

    # 遍历搜索查询
    for i, query in enumerate(SEARCH_QUERIES, 1):
        logger.info(f"\n[{i}/{len(SEARCH_QUERIES)}] 搜索: {query}")

        # 搜索
        results = search_searxng(query, limit=10)

        if not results:
            logger.warning(f"  没有找到结果")
            continue

        # 遍历结果
        for j, result in enumerate(results, 1):
            url = result.get('url', '')
            title = result.get('title', '')
            snippet = result.get('content', '')

            # 检查 URL 质量
            if not is_high_quality_url(url):
                logger.debug(f"  [{j}] 跳过低质量来源: {url}")
                continue

            # 检查是否已处理
            if url in seen_urls:
                logger.debug(f"  [{j}] 跳过已处理 URL: {url}")
                continue

            seen_urls.add(url)

            logger.info(f"  [{j}] 处理: {title}")
            logger.debug(f"      URL: {url}")

            # 获取页面内容
            page_content = fetch_page_content(url)

            if not page_content:
                logger.warning(f"      获取内容失败")
                continue

            # 保存页面内容本身作为提示词
            # 优先保存完整正文，如果正文太长则截取
            content_to_save = page_content[:15000] if len(page_content) > 15000 else page_content
            prompt_type = classify_prompt_type(content_to_save)
            quality_score = calculate_quality_score(content_to_save)

            prompt_data = {
                'content': content_to_save,
                'title': title,
                'source': 'searxng',
                'url': url,
                'type': prompt_type,
                'quality_score': quality_score,
                'collected_at': datetime.now().isoformat(),
                'search_query': query
            }

            all_prompts.append(prompt_data)
            logger.info(f"      保存页面内容 ({len(content_to_save)} 字符)")

            # 提取提示词（额外提取，作为补充）
            prompts = extract_prompts_from_content(page_content, max_prompts=15)

            if prompts:
                logger.info(f"      额外提取 {len(prompts)} 个提示词")

                # 处理每个额外提示词
                for prompt in prompts[:3]:  # 只保存前 3 个
                    # 避免与主内容重复
                    if prompt not in page_content:
                        prompt_type = classify_prompt_type(prompt)
                        quality_score = calculate_quality_score(prompt)

                        prompt_data = {
                            'content': prompt,
                            'title': f"{title} (extracted)",
                            'source': 'searxng',
                            'url': url,
                            'type': prompt_type,
                            'quality_score': quality_score,
                            'collected_at': datetime.now().isoformat(),
                            'search_query': query
                        }

                        all_prompts.append(prompt_data)

        # 搜索间隔，避免过于频繁
        time.sleep(2)

    # 保存结果
    logger.info(f"\n{'=' * 80}")
    logger.info(f"📊 收集完成！")
    logger.info(f"{'=' * 80}")
    logger.info(f"总共收集: {len(all_prompts)} 个提示词")

    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for prompt in all_prompts:
            f.write(json.dumps(prompt, ensure_ascii=False) + '\n')

    logger.info(f"保存到: {OUTPUT_FILE}")

    # 统计信息
    type_counts = {}
    for prompt in all_prompts:
        ptype = prompt['type']
        type_counts[ptype] = type_counts.get(ptype, 0) + 1

    logger.info(f"\n类型分布:")
    for ptype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  {ptype}: {count}")

    # 质量分布
    high_quality = sum(1 for p in all_prompts if p['quality_score'] >= 70)
    medium_quality = sum(1 for p in all_prompts if 50 <= p['quality_score'] < 70)
    low_quality = sum(1 for p in all_prompts if p['quality_score'] < 50)

    logger.info(f"\n质量分布:")
    logger.info(f"  高质量 (≥70): {high_quality}")
    logger.info(f"  中等 (50-69): {medium_quality}")
    logger.info(f"  低质量 (<50): {low_quality}")

    logger.info(f"\n✅ 完成！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⏸️  用户中断")
    except Exception as e:
        logger.error(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
