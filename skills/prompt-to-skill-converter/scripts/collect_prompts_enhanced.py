#!/usr/bin/env python3
"""
增强版 AI 提示词收集系统 - Phase 1

功能特性：
- 扩展的搜索关键词库（50+ 查询）
- 智能关键词组合策略
- 高级搜索结果过滤
- 增强的提示词提取算法
- 支持中英文双语搜索
- 自动分类和质量评分
- 完整的错误处理和日志记录

Phase 1 改进：
1. 升级查询系统
2. 扩展关键词和搜索组合
3. 改进 URL 质量判断
4. 优化提示词提取模式
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
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
OUTPUT_FILE = OUTPUT_DIR / f"prompts-enhanced-{datetime.now().strftime('%Y%m%d-%H%M')}.jsonl"
LOGS_DIR = Path("/root/clawd/logs")

# 创建目录
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logger = logging.getLogger("collect_prompts_enhanced")
logger.setLevel(logging.INFO)

# 控制台日志（简化版）
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(console_handler)

# 文件日志（详细版）
file_handler = logging.FileHandler(
    LOGS_DIR / "collect-prompts-enhanced.log",
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
REQUEST_DELAY = 1.5  # 请求延迟（秒）

# ============================================================================
# 扩展的搜索关键词库 - Phase 1 核心改进
# ============================================================================

# 基础关键词（用于组合）
BASE_KEYWORDS = {
    "prompt": ["prompt", "提示词", "提示", "命令", "instruction", "template"],
    "ai": ["AI", "artificial intelligence", "人工智能", "LLM", "GPT", "Claude", "Gemini"],
    "type": ["image", "video", "text", "代码", "code", "艺术", "art", "creative"],
    "platform": ["Midjourney", "DALL-E", "Stable Diffusion", "Veo", "Kling", "Runway", "Pika"],
    "action": ["generate", "create", "write", "design", "生成", "创作", "设计"],
    "quality": ["best", "top", "high quality", "professional", "高质量", "专业", "最佳"],
}

# 专业提示词网站和资源
PROFESSIONAL_SOURCES = [
    # 综合性资源
    "awesome-chatgpt-prompts github repository",
    "LearnPrompting guide comprehensive tutorial",
    "PromptBase marketplace best prompts",
    "OpenAI prompt engineering guide",

    # 图像生成专项
    "Midjourney prompt tutorial examples",
    "Midjourney 参数详解 --ar --style --chaos",
    "DALL-E 3 prompt examples guide",
    "Stable Diffusion prompt engineering negative",
    "Stable Diffusion LoRA model prompts",

    # 视频生成专项（新增）
    "Veo 3 prompt examples video generation",
    "Kling AI prompt guide text to video",
    "Runway ML prompt tutorial motion",
    "Pika Labs prompt examples animation",
    "video generation prompt best practices",

    # 技术平台搜索
    "site:github.com \"prompt engineering\" tutorial",
    "site:github.com \"AI prompts\" repository",
    "site:medium.com \"prompt engineering\" guide",
    "site:dev.to \"AI prompts\" examples",
    "site:hashnode.com \"prompt guide\" tutorial",
    "site:towardsdatascience.com \"prompt\" techniques",

    # 行业应用（新增）
    "AI prompts for marketing content",
    "business AI prompt templates",
    "educational AI prompts teaching",
    "product photography AI prompts",
    "character design AI prompts",
    "game asset AI prompts",
    "fashion design AI prompts",
    "architecture AI prompts",

    # 高级技巧（新增）
    "negative prompt examples Midjourney",
    "prompt chaining techniques LLM",
    "few-shot prompting examples",
    "role-based prompts system instructions",
    "context-aware prompts examples",

    # 特定领域（新增）
    "legal AI prompts contract",
    "medical AI prompts diagnosis",
    "finance AI prompts analysis",
    "scientific AI prompts research",
    "creative writing AI prompts storytelling",
]

# 中文搜索查询（新增）
CHINESE_QUERIES = [
    "Midjourney 提示词 教程 示例",
    "DALL-E 3 提示词 指南",
    "Stable Diffusion 提示词 负面",
    "AI 提示词 工程 最佳实践",
    "ChatGPT 提示词 模板",
    "Claude 提示词 角色扮演",
    "AI 绘画 提示词 风格",
    "视频生成 提示词 Veo Kling",
    "AI 写作 提示词 文案",
    "商业 AI 提示词 模板",

    "site:github.com \"提示词\" AI",
    "site:zhihu.com \"提示词\" AI",
    "site:csdn.net AI 提示词 教程",
]

# 组合搜索策略（新增）
# 基础关键词 + 平台 + 质量词
COMBINATION_QUERIES = []

# 自动生成组合查询
platforms = ["Midjourney", "DALL-E", "Stable Diffusion", "Veo", "Kling", "Runway", "Pika"]
actions = ["best prompts", "tutorial", "guide", "examples", "templates"]
qualities = ["professional", "high quality", "advanced"]

for platform in platforms[:4]:  # 限制组合数量
    for action in actions[:2]:
        for quality in qualities[:2]:
            query = f"{platform} {action} {quality}"
            COMBINATION_QUERIES.append(query)

# 合并所有搜索查询
ALL_QUERIES = list(set(PROFESSIONAL_SOURCES + CHINESE_QUERIES + COMBINATION_QUERIES))

# ============================================================================
# 域名质量控制 - Phase 1 改进
# ============================================================================

# 高质量域名白名单（扩展）
HIGH_QUALITY_DOMAINS = {
    # 综合性资源
    'github.com', 'gitlab.com', 'bitbucket.org',

    # AI 和技术平台
    'openai.com', 'anthropic.com', 'google.com', 'deepmind.com',
    'midjourney.com', 'stability.ai', 'huggingface.co',

    # 提示词专业网站
    'promptbase.com', 'learnprompting.org', 'promptengineering.ai',

    # 技术博客和社区
    'medium.com', 'dev.to', 'hashnode.com', 'towardsdatascience.com',
    'analyticsvidhya.com', 'kdnuggets.com', 'machinelearningmastery.com',

    # 中文技术社区（新增）
    'zhihu.com', 'csdn.net', 'juejin.cn', 'segmentfault.com',

    # 教育资源
    'coursera.org', 'udacity.com', 'edx.org',

    # 文档和指南
    'readthedocs.io', 'docs.python.org',
}

# 低质量域名黑名单（扩展）
LOW_QUALITY_DOMAINS = {
    # 社交媒体（通常内容质量不稳定）
    'pinterest.com', 'instagram.com', 'tiktok.com', 'facebook.com',
    'twitter.com', 'x.com',  # 使用 twitter-search skill

    # 新闻聚合和低质量内容
    'buzzfeed.com', 'clickhole.com', 'clickbait',

    # 广告和推广网站
    'ad', 'ads', 'promotion', 'affiliate',

    # 下载和破解网站
    'crack', 'torrent', 'pirate', 'warez',
}

# ============================================================================
# 全局状态
# ============================================================================

# 用于优雅退出
shutdown_flag = False

def signal_handler(signum, frame):
    """信号处理"""
    global shutdown_flag
    logger.info("\n⏸️  收到中断信号，正在优雅退出...")
    shutdown_flag = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ============================================================================
# 核心功能函数
# ============================================================================

def is_high_quality_url(url: str) -> Tuple[bool, str]:
    """
    判断 URL 是否来自高质量来源 - Phase 1 改进版

    Args:
        url: 目标 URL

    Returns:
        (是否高质量, 原因)
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # 1. 检查黑名单（严格）
        for blacklisted in LOW_QUALITY_DOMAINS:
            if blacklisted in domain:
                return False, f"黑名单域名: {blacklisted}"

        # 2. 检查白名单（信任）
        for whitelisted in HIGH_QUALITY_DOMAINS:
            if whitelisted in domain:
                return True, f"白名单域名: {whitelisted}"

        # 3. 检查 URL 模式（启发式规则）
        # 有用的模式
        good_patterns = [
            r'/blog/',  # 博客文章
            r'/tutorial',  # 教程
            r'/guide',  # 指南
            r'/docs/',  # 文档
            r'/learn/',  # 学习资源
            r'/wiki/',  # Wiki
            r'github\.com/[^/]+/[^/]+',  # GitHub 仓库
            r'readthedocs\.io',  # ReadTheDocs
        ]

        for pattern in good_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True, f"匹配良好模式: {pattern}"

        # 4. 检查可疑模式
        bad_patterns = [
            r'/ad',  # 广告
            r'/ads',  # 广告
            r'/affiliate',  # 联盟营销
            r'/ref=',  # 推荐链接
            r'\.exe$',  # 可执行文件
            r'\.apk$',  # Android 应用
        ]

        for pattern in bad_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return False, f"匹配可疑模式: {pattern}"

        # 5. 默认允许，但标记为未验证
        return True, "默认允许（未验证）"

    except Exception as e:
        logger.warning(f"URL 解析失败 {url}: {e}")
        return True, "解析失败，默认允许"


def search_searxng(query: str, limit: int = MAX_RESULTS_PER_QUERY) -> List[Dict]:
    """
    使用 SearXNG 搜索 - Phase 1 改进版

    Args:
        query: 搜索查询
        limit: 返回结果数量

    Returns:
        搜索结果列表
    """
    if shutdown_flag:
        return []

    params = {
        "q": query,
        "format": "json",
        "categories": "general",
        "engines": "",  # 使用所有可用引擎
    }

    try:
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
    获取页面内容 - Phase 1 改进版

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

    except requests.exceptions.Timeout:
        logger.debug(f"获取页面超时: {url}")
        return None
    except requests.exceptions.RequestException as e:
        logger.debug(f"获取页面失败 {url}: {e}")
        return None
    except Exception as e:
        logger.warning(f"未知错误 {url}: {e}")
        return None


def detect_language(text: str) -> str:
    """
    检测文本语言（中文/英文/混合）

    Args:
        text: 输入文本

    Returns:
        'zh', 'en', 'mixed'
    """
    # 计算中文字符数
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    # 计算英文字符数
    english_chars = sum(1 for c in text if c.isalpha() and ord(c) < 128)
    # 计算总字符数
    total_chars = chinese_chars + english_chars

    if total_chars == 0:
        return 'unknown'

    # 计算比例
    chinese_ratio = chinese_chars / total_chars
    english_ratio = english_chars / total_chars

    # 判断
    if chinese_ratio > 0.7:
        return 'zh'
    elif english_ratio > 0.7:
        return 'en'
    else:
        return 'mixed'


def is_navigation_or_footer(text: str) -> bool:
    """
    检查文本是否来自导航栏或页脚

    Args:
        text: 文本内容

    Returns:
        True 如果是导航栏/页脚内容
    """
    text_lower = text.lower()

    # 导航关键词
    nav_keywords = [
        'menu', 'navigation', 'home', 'about', 'contact',
        'login', 'sign in', 'register', 'sign up',
        'pricing', 'pricing plans', 'subscribe', 'subscription',
        'search', 'search...', 'search bar',
        '导航', '菜单', '首页', '关于', '联系',
        '登录', '注册', '定价', '订阅', '搜索',
    ]

    # 页脚关键词
    footer_keywords = [
        'copyright', 'all rights reserved', 'privacy policy',
        'terms of service', 'cookie policy', 'contact us',
        'follow us', 'social media', 'newsletter',
        '版权所有', '隐私政策', '服务条款', 'cookie政策',
        '联系我们', '关注我们', '社交媒体',
    ]

    # 广告关键词
    ad_keywords = [
        'ad', 'advertisement', 'sponsored', 'affiliate',
        'promo', 'promotion', 'discount', 'sale', 'offer',
        'limited time', 'only $', 'free trial', 'click here',
        '广告', '推广', '优惠', '折扣', '促销',
    ]

    # 检查
    for keyword in nav_keywords + footer_keywords + ad_keywords:
        if keyword in text_lower:
            return True

    # 检查纯 URL 或短文本
    if len(text.split()) < 3:
        return True

    return False


def is_truncated(text: str) -> Tuple[bool, str]:
    """
    检查文本是否被截断

    Args:
        text: 文本内容

    Returns:
        (是否截断, 截断原因)
    """
    text_lower = text.lower()

    # 截断标记
    truncation_markers = [
        '...', '…', '...', '...',  # 省略号
        'read more', 'continue reading', 'click to continue',
        'view more', 'see more', 'show more', 'learn more',
        '继续阅读', '点击继续', '查看更多', '了解更多',
        '[...]', '(...)', '{...}', '<...>',
    ]

    for marker in truncation_markers:
        if marker in text_lower:
            return True, f"截断标记: {marker}"

    # 检查结尾 - 不完整的句子
    if text[-3:] in ['...', '...', '...', '…']:
        return True, "以省略号结尾"

    # 检查开头 - 缺少主语或动词
    if text[0].islower() and not text.startswith(('a ', 'an ', 'the ')):
        return True, "以小写字母开头（可能不完整）"

    # 检查标点 - 正常文本应该有标点符号结尾
    if not text[-1] in ['.', '!', '?', '。', '！', '？', '"', "'", '"', "'", '`']:
        # 但如果很短（< 200 字符），可能是关键词列表
        if len(text) > 200:
            return True, "缺少结尾标点"

    return False, ""


def extract_prompts_from_content(content: str, max_prompts: int = 20) -> List[str]:
    """
    从内容中提取提示词 - Phase 2 改进版

    改进点：
    - 更精确的上下文标记
    - 导航栏/页脚过滤
    - 完整性检查
    - 语言感知

    Args:
        content: 页面内容
        max_prompts: 最大提取数量

    Returns:
        提示词列表
    """
    prompts = []

    # 模式 1: 代码块中的提示词（最高优先级）
    code_block_patterns = [
        r'```(?:prompt|text|提示词)?\s*\n+([\s\S]{50,1000}?)\n+```',
    ]

    for pattern in code_block_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        prompts.extend(matches)

    # 模式 2: 明确标记后的内容
    explicit_patterns = [
        r'(?:prompt[:：]\s*)["\']([^"\']{50,1000})["\']',  # Prompt: "text"
        r'(?:提示词[:：]\s*)["\']([^"\']{50,1000})["\']',  # 提示词: "text"
        r'(?:example[:：]\s*)["\']([^"\']{50,1000})["\']',  # Example: "text"
        r'(?:例子[:：]\s*)["\']([^"\']{50,1000})["\']',  # 例子: "text"
    ]

    for pattern in explicit_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        prompts.extend(matches)

    # 模式 3: 角色扮演模式
    roleplay_patterns = [
        r'(?:act as|act as a|扮演|角色[:：]\s*)([^.\n]{50,1000})',
        r'(?:you are|you are a|你是)([\s]+[^.\n]{50,1000})',
    ]

    for pattern in roleplay_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        prompts.extend(matches)

    # 模式 4: 动作指令模式
    action_patterns = [
        r'(?:generate|create|design|write|生成|创作|设计)[\s,]+([^.\n]{50,1000})',
        r'(?:create|make|generate)([\s]+a[\s]+[^.\n]{50,1000})',
    ]

    for pattern in action_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        prompts.extend(matches)

    # 模式 5: 列表中的提示词（最后，因为可能包含噪音）
    list_patterns = [
        r'(?i)(?:^\d+[\.\)]|[-*•])\s+["\']([^"\']{50,1000})["\']',  # 带引号的列表项
        r'(?i)(?:^\d+[\.\)]|[-*•])\s+([^.\n]{80,500})',  # 较长的列表项
    ]

    for pattern in list_patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        prompts.extend(matches)

    # 去重（保留顺序）
    seen = set()
    unique_prompts = []
    for p in prompts:
        p_clean = p.strip()
        if p_clean and p_clean not in seen:
            seen.add(p_clean)
            unique_prompts.append(p_clean)

    # 质量过滤（改进版）
    filtered = []
    for p in unique_prompts:
        p_clean = p.strip()

        # 1. 长度过滤（调整范围）
        if not (50 <= len(p_clean) <= 1000):
            continue

        # 2. 导航栏/页脚检查（新增）
        if is_navigation_or_footer(p_clean):
            continue

        # 3. 完整性检查（新增）
        is_trunc, trunc_reason = is_truncated(p_clean)
        if is_trunc and len(p_clean) < 300:
            # 短文本且被截断，跳过
            continue

        # 4. 内容质量过滤
        # 检查字母数字/中文比例
        alpha_ratio = sum(
            c.isalnum() or c.isspace() or ord(c) > 127  # 支持中文
            for c in p_clean
        ) / len(p_clean)
        if alpha_ratio < 0.6:
            continue

        # 5. 检查是否有意义的内容（关键词检查）
        meaningful_keywords = [
            # 英文关键词
            'image', 'photo', 'picture', 'portrait', 'art', 'design', 'create',
            'generate', 'write', 'style', 'quality', 'detailed', 'realistic',
            'video', 'animation', 'text', 'story', 'code', 'function',
            # 中文关键词
            '图像', '照片', '艺术', '设计', '创建', '生成', '写作',
            '风格', '质量', '详细', '逼真', '视频', '动画', '文本',
            '故事', '代码', '函数',
        ]
        has_meaningful = any(
            kw in p_clean.lower()
            for kw in meaningful_keywords
        )
        if not has_meaningful:
            continue

        # 6. 检查垃圾内容
        junk_patterns = [
            r'^\s*https?://',  # 纯 URL
            r'^\s*[a-z]{10,}\s*$',  # 纯随机字符
            r'^\s*\d+\s*$',  # 纯数字
            r'^\s*[^\w\s]{10,}\s*$',  # 纯特殊字符
        ]
        for pattern in junk_patterns:
            if re.match(pattern, p_clean, re.IGNORECASE):
                break
        else:
            # 添加完整性信息到元数据
            filtered.append({
                'content': p_clean,
                'is_truncated': is_trunc,
                'truncation_reason': trunc_reason,
            })

    return filtered[:max_prompts]


def classify_prompt_type(prompt: str, language: str = 'unknown') -> str:
    """
    分类提示词类型 - Phase 2 改进版（语言感知）

    Args:
        prompt: 提示词文本
        language: 语言 ('zh', 'en', 'mixed', 'unknown')

    Returns:
        提示词类型
    """
    prompt_lower = prompt.lower()

    # 图像生成关键词（扩展）
    image_keywords = {
        'en': [
            'image', 'photo', 'picture', 'portrait', 'painting', 'drawing',
            'illustration', 'midjourney', 'dall-e', 'stable diffusion', 'diffusion',
            'render', 'visual', 'art', 'scene', 'landscape', 'portrait',
            'sketch', 'watercolor', 'oil painting', 'digital art',
        ],
        'zh': [
            '图片', '图像', '绘画', '插画', '照片', '渲染',
        ]
    }

    # 视频生成关键词（扩展）
    video_keywords = {
        'en': [
            'video', 'animation', 'motion', 'animate', 'runway', 'pika',
            'kling', 'veo', 'clip', 'footage', 'film', 'movie',
            'transition', 'camera movement', 'zoom', 'pan',
        ],
        'zh': [
            '视频', '动画', '影片', '转场',
        ]
    }

    # 文本生成关键词（扩展）
    text_keywords = {
        'en': [
            'write', 'essay', 'article', 'blog', 'content', 'story',
            'chatgpt', 'gpt', 'llm', 'text generation', 'summarize',
            'translate', 'analyze', 'explain', 'code', 'programming',
        ],
        'zh': [
            '写作', '文章', '博客', '故事', '代码', '编程',
        ]
    }

    # 代码生成关键词（新增）
    code_keywords = {
        'en': [
            'code', 'function', 'class', 'algorithm', 'debug', 'refactor',
        ],
        'zh': [
            '代码', '函数', '类', '算法', '调试', '重构',
        ]
    }

    # 角色扮演关键词（新增）
    roleplay_keywords = {
        'en': [
            'act as', 'you are', 'role', 'character', 'persona',
        ],
        'zh': [
            '扮演', '角色', '你是',
        ]
    }

    # 计算分数（语言感知）
    def calculate_score(keywords_dict: Dict, lang: str) -> int:
        """根据语言计算关键词得分"""
        score = 0
        # 优先使用匹配的语言关键词
        if lang in keywords_dict:
            score += sum(1 for kw in keywords_dict[lang] if kw in prompt_lower)
        # 也检查其他语言的关键词（混合语言的情况）
        for other_lang, kw_list in keywords_dict.items():
            if other_lang != lang:
                score += sum(1 for kw in kw_list if kw in prompt_lower) // 2  # 降低权重
        return score

    image_score = calculate_score(image_keywords, language)
    video_score = calculate_score(video_keywords, language)
    text_score = calculate_score(text_keywords, language)
    code_score = calculate_score(code_keywords, language)
    roleplay_score = calculate_score(roleplay_keywords, language)

    # 判断类型
    if code_score >= 2 and code_score > text_score:
        return 'code-generation'
    elif roleplay_score >= 2:
        return 'roleplay'
    elif video_score > image_score and video_score > text_score:
        return 'video-generation'
    elif image_score > text_score:
        return 'image-generation'
    elif text_score > 0:
        return 'text-generation'
    else:
        return 'general'


def calculate_quality_score(prompt: str, is_truncated: bool = False) -> int:
    """
    计算提示词质量分数 - Phase 2 改进版（考虑截断）

    Args:
        prompt: 提示词文本
        is_truncated: 是否被截断

    Returns:
        质量分数 (0-100)
    """
    score = 0
    prompt_lower = prompt.lower()

    # 1. 长度评分（改进 - 给更长提示词更高分）
    length = len(prompt)
    if 80 <= length <= 200:
        score += 20
    elif 201 <= length <= 400:
        score += 30
    elif 401 <= length <= 600:
        score += 35
    elif 601 <= length <= 800:
        score += 30
    elif 801 <= length <= 1000:
        score += 25
    else:
        score += 15

    # 2. 关键词评分（扩展）
    quality_keywords = [
        'detailed', 'realistic', 'high quality', 'professional', 'creative',
        'specific', 'precise', 'clear', 'comprehensive', 'well-structured',
        'vibrant', 'stunning', 'beautiful', 'elegant', 'sophisticated',
        '详细', '逼真', '高质量', '专业', '创意', '具体', '精确', '清晰',
        '生动', '惊艳', '美丽', '优雅', '精致',
    ]
    score += min(25, sum(3 for kw in quality_keywords if kw in prompt_lower))

    # 3. 动作动词评分（扩展）
    action_verbs = [
        'generate', 'create', 'write', 'design', 'build', 'make', 'develop',
        'analyze', 'explain', 'summarize', 'translate', 'optimize',
        'render', 'depict', 'illustrate', 'portray', 'capture',
        '生成', '创作', '编写', '设计', '构建', '制作', '开发',
        '分析', '解释', '总结', '翻译', '优化', '渲染', '描绘',
    ]
    score += min(20, sum(3 for verb in action_verbs if verb in prompt_lower))

    # 4. 结构评分（改进）
    if ',' in prompt:
        score += 6
    if ':' in prompt:
        score += 4
    if '\n' in prompt or '，' in prompt:
        score += 6
    if '--' in prompt:  # Midjourney 参数
        score += 5

    # 5. 描述性词汇（改进）
    descriptive_words = [
        'with', 'featuring', 'including', 'showing', 'displaying', 'depicting',
        'containing', 'using', 'inspired by', 'style of', 'in the style',
        '包含', '展示', '描绘', '使用', '灵感来自', '风格',
    ]
    score += min(15, sum(3 for word in descriptive_words if word in prompt_lower))

    # 6. 细节程度（改进）
    detail_markers = [
        'in the style of', 'similar to', 'resembling', 'like',
        'inspired by', 'based on', 'reminiscent of',
        '风格', '类似于', '像', '灵感来自', '基于',
    ]
    if any(marker in prompt_lower for marker in detail_markers):
        score += 8

    # 7. 风格参考（新增）
    style_keywords = [
        'photorealistic', 'hyperrealistic', 'cinematic', 'dramatic',
        'minimalist', 'vintage', 'modern', 'contemporary',
        '超写实', '电影感', '戏剧性', '极简', '复古', '现代', '当代',
    ]
    if any(kw in prompt_lower for kw in style_keywords):
        score += 5

    # 8. 截断惩罚（新增 - 如果截断，降低分数但不要完全拒绝）
    if is_truncated:
        score = max(score - 15, score * 0.7)  # 至少降低 15 分或 30%

    return min(100, int(score))


def process_search_result(result: Dict, seen_urls: Set[str]) -> List[Dict]:
    """
    处理单个搜索结果

    Args:
        result: 搜索结果字典
        seen_urls: 已处理的 URL 集合

    Returns:
        提取的提示词列表
    """
    url = result.get('url', '')
    title = result.get('title', '')
    snippet = result.get('content', '')

    # 检查 URL 质量
    is_high_quality, reason = is_high_quality_url(url)
    if not is_high_quality:
        logger.debug(f"  跳过低质量 URL: {reason}")
        return []

    # 检查是否已处理
    if url in seen_urls:
        logger.debug(f"  跳过已处理 URL")
        return []

    seen_urls.add(url)

    logger.info(f"  处理: {title[:60]}...")

    # 获取页面内容
    content = fetch_page_content(url)
    if not content:
        return []

    # 提取提示词（现在返回字典列表，包含元数据）
    prompt_data_list = extract_prompts_from_content(content, max_prompts=20)

    if not prompt_data_list:
        return []

    logger.info(f"    找到 {len(prompt_data_list)} 个提示词")

    # 处理每个提示词
    prompt_list = []
    for prompt_dict in prompt_data_list:
        prompt = prompt_dict['content']
        is_truncated = prompt_dict['is_truncated']

        # 检测语言
        language = detect_language(prompt)

        # 分类提示词类型（传入语言）
        prompt_type = classify_prompt_type(prompt, language)

        # 计算质量分数（传入截断信息）
        quality_score = calculate_quality_score(prompt, is_truncated)

        prompt_data = {
            'content': prompt,
            'title': title,
            'source': 'searxng-enhanced',
            'url': url,
            'type': prompt_type,
            'quality_score': quality_score,
            'language': language,  # 新增：语言字段
            'is_truncated': is_truncated,  # 新增：截断状态
            'truncation_reason': prompt_dict['truncation_reason'],  # 新增：截断原因
            'collected_at': datetime.now().isoformat(),
        }

        prompt_list.append(prompt_data)

    return prompt_list


def run_collection(queries: List[str], max_workers: int = MAX_WORKERS) -> List[Dict]:
    """
    执行收集任务 - Phase 1 并发版

    Args:
        queries: 搜索查询列表
        max_workers: 最大并发数

    Returns:
        所有收集的提示词
    """
    all_prompts = []
    seen_urls = set()

    logger.info(f"开始执行 {len(queries)} 个搜索查询...")

    # 使用线程池并发执行
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有搜索任务
        future_to_query = {
            executor.submit(search_searxng, query): query
            for query in queries
        }

        # 处理完成的搜索
        for future in as_completed(future_to_query):
            if shutdown_flag:
                break

            query = future_to_query[future]

            try:
                results = future.result()

                if not results:
                    continue

                logger.info(f"\n搜索: {query}")
                logger.info(f"  找到 {len(results)} 个结果")

                # 处理每个结果
                for result in results:
                    if shutdown_flag:
                        break

                    prompts = process_search_result(result, seen_urls)
                    all_prompts.extend(prompts)

                    # 延迟，避免过载
                    time.sleep(REQUEST_DELAY)

            except Exception as e:
                logger.error(f"处理查询 '{query}' 失败: {e}")

    return all_prompts


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 增强版 AI 提示词收集系统 - Phase 1")
    logger.info("=" * 80)
    logger.info(f"搜索查询总数: {len(ALL_QUERIES)}")
    logger.info(f"输出文件: {OUTPUT_FILE}")
    logger.info("=" * 80)

    # 执行收集
    all_prompts = run_collection(ALL_QUERIES)

    if shutdown_flag:
        logger.info("\n⏸️  收集中断，保存已收集的数据...")
    else:
        logger.info(f"\n{'=' * 80}")
        logger.info("📊 收集完成！")
        logger.info(f"{'=' * 80}")

    # 保存结果
    logger.info(f"总共收集: {len(all_prompts)} 个提示词")

    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for prompt in all_prompts:
            f.write(json.dumps(prompt, ensure_ascii=False) + '\n')

    logger.info(f"✅ 保存到: {OUTPUT_FILE}")

    # 统计信息
    if all_prompts:
        # 类型分布
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
        logger.info(f"  高质量 (≥70): {high_quality} ({high_quality*100//len(all_prompts) if all_prompts else 0}%)")
        logger.info(f"  中等 (50-69): {medium_quality} ({medium_quality*100//len(all_prompts) if all_prompts else 0}%)")
        logger.info(f"  低质量 (<50): {low_quality} ({low_quality*100//len(all_prompts) if all_prompts else 0}%)")

        # 平均质量分数
        avg_score = sum(p['quality_score'] for p in all_prompts) / len(all_prompts)
        logger.info(f"\n平均质量分数: {avg_score:.1f}/100")

        # 高质量提示词示例
        high_quality_prompts = sorted(
            [p for p in all_prompts if p['quality_score'] >= 80],
            key=lambda x: x['quality_score'],
            reverse=True
        )[:5]

        if high_quality_prompts:
            logger.info(f"\n🏆 前 5 个高质量提示词示例:")
            for i, p in enumerate(high_quality_prompts, 1):
                logger.info(f"\n  {i}. [{p['type']}] 质量分数: {p['quality_score']}")
                logger.info(f"     {p['content'][:100]}...")

    logger.info(f"\n{'=' * 80}")
    logger.info("✅ 完成！")
    logger.info(f"{'=' * 80}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⏸️  用户中断")
    except Exception as e:
        logger.error(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
