#!/usr/bin/env python3
"""
统一的搜索包装器 - 支持多搜索源的 Fallback 机制

支持搜索源：
1. Tavily (优先)
2. 百度搜索 (Fallback 1)
3. SearXNG (Fallback 2)
4. Brave Search API (Fallback 3)

使用方法：
    from search_wrapper import search

    results = search("Python 编程", max_results=5)
    for result in results:
        print(f"{result['title']} - {result['url']}")
"""

import os
import sys
import json
import time
import logging
import urllib.request
import urllib.error
import urllib.parse
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

# 配置日志
LOG_DIR = Path("/root/clawd/logs/search-wrapper")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'search-wrapper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# 加载配置
CONFIG_DIR = Path("/root/clawd/.config/data-sources")

def load_config() -> Dict:
    """加载配置文件"""
    config = {
        "tavily": {
            "api_key": "",
            "api_base": "https://api.tavily.com",
            "timeout": 30
        },
        "baidu": {
            "api_key": "",
            "api_base": "https://qianfan.baidubce.com/v2/ai_search/web_search",
            "timeout": 30
        },
        "searxng": {
            "url": "",
            "timeout": 30
        },
        "brave": {
            "api_base": "https://api.search.brave.com/res/v1/web/search",
            "api_key": "",  # 免费版无需 API Key
            "timeout": 30
        }
    }

    # 加载 Tavily 配置
    tavily_conf = CONFIG_DIR / "tavily.conf"
    if tavily_conf.exists():
        with open(tavily_conf) as f:
            for line in f:
                line = line.strip()
                if line.startswith("TAVILY_API_KEY="):
                    config["tavily"]["api_key"] = line.split("=", 1)[1].strip('"\'')
                elif line.startswith("API_BASE="):
                    config["tavily"]["api_base"] = line.split("=", 1)[1].strip('"\'')
                elif line.startswith("TIMEOUT="):
                    config["tavily"]["timeout"] = int(line.split("=", 1)[1].strip())

    # 加载 SearXNG 配置
    searxng_conf = CONFIG_DIR / "searxng.conf"
    if searxng_conf.exists():
        with open(searxng_conf) as f:
            for line in f:
                line = line.strip()
                if line.startswith("SEARXNG_URL="):
                    config["searxng"]["url"] = line.split("=", 1)[1].strip('"\'')
                elif line.startswith("TIMEOUT="):
                    config["searxng"]["timeout"] = int(line.split("=", 1)[1].strip())

    # 从环境变量加载（可选）
    config["tavily"]["api_key"] = os.environ.get("TAVILY_API_KEY", config["tavily"]["api_key"])
    config["baidu"]["api_key"] = os.environ.get("BAIDU_API_KEY", config["baidu"]["api_key"])
    config["searxng"]["url"] = os.environ.get("SEARXNG_URL", config["searxng"]["url"])
    config["brave"]["api_key"] = os.environ.get("BRAVE_API_KEY", config["brave"]["api_key"])

    # 检查百度 API Key 是否配置
    if config["baidu"]["api_key"]:
        logger.info("百度搜索 API Key 已配置")
    else:
        logger.warning("百度搜索 API Key 未配置，将跳过百度搜索")

    return config

# 加载全局配置
CONFIG = load_config()


def search_baidu(query: str, max_results: int = 5, timeout: int = 30) -> Tuple[List[Dict], Optional[str]]:
    """
    使用百度 AI 搜索 API 搜索

    Args:
        query: 搜索查询
        max_results: 最大结果数量
        timeout: 超时时间（秒）

    Returns:
        (结果列表, 错误信息)
    """
    if not CONFIG["baidu"]["api_key"]:
        return [], "百度 API Key 未配置"

    try:
        logger.info(f"[百度] 开始搜索: {query}")

        url = CONFIG["baidu"]["api_base"]
        headers = {
            "Authorization": f"Bearer {CONFIG['baidu']['api_key']}",
            "X-Appbuilder-From": "openclaw",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [
                {
                    "content": query,
                    "role": "user"
                }
            ],
            "edition": "standard",
            "search_source": "baidu_search_v2",
            "resource_type_filter": [
                {"type": "web", "top_k": max_results}
            ],
            "search_filter": {},
            "search_recency_filter": "year",
            "safe_search": False
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            response_data = json.loads(response.read().decode('utf-8'))

            results = []
            # 百度 API 返回的数据结构：references 数组
            if 'references' in response_data:
                for item in response_data['references'][:max_results]:
                    # 使用 snippet 或 content 作为内容摘要
                    content = item.get('snippet', '')
                    if not content:
                        content = item.get('content', '')
                    # 限制内容长度
                    content = content[:500] if content else ''

                    results.append({
                        "title": item.get('title', ''),
                        "url": item.get('url', ''),
                        "content": content,
                        "source": "baidu",
                        "timestamp": datetime.now().isoformat()
                    })
            elif 'data' in response_data and 'result' in response_data['data']:
                # 兼容其他可能的格式
                for item in response_data['data']['result'][:max_results]:
                    results.append({
                        "title": item.get('title', ''),
                        "url": item.get('url', ''),
                        "content": item.get('content', '')[:500],
                        "source": "baidu",
                        "timestamp": datetime.now().isoformat()
                    })

            logger.info(f"[百度] 成功返回 {len(results)} 个结果")
            return results, None

    except urllib.error.HTTPError as e:
        error_msg = f"百度 HTTP 错误: {e.code} - {e.reason}"
        logger.error(f"[百度] {error_msg}")
        return [], error_msg
    except urllib.error.URLError as e:
        error_msg = f"百度 URL 错误: {e.reason}"
        logger.error(f"[百度] {error_msg}")
        return [], error_msg
    except Exception as e:
        error_msg = f"百度 未知错误: {str(e)}"
        logger.error(f"[百度] {error_msg}")
        return [], error_msg


def search_tavily(query: str, max_results: int = 5, timeout: int = 30) -> Tuple[List[Dict], Optional[str]]:
    """
    使用 Tavily API 搜索

    Args:
        query: 搜索查询
        max_results: 最大结果数量
        timeout: 超时时间（秒）

    Returns:
        (结果列表, 错误信息)
    """
    if not CONFIG["tavily"]["api_key"]:
        return [], "Tavily API Key 未配置"

    try:
        logger.info(f"[Tavily] 开始搜索: {query}")

        url = f"{CONFIG['tavily']['api_base']}/search"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "api_key": CONFIG["tavily"]["api_key"],
            "query": query,
            "max_results": max_results,
            "search_depth": "basic",
            "include_answer": False,
            "include_raw_content": False
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=timeout) as response:
            response_data = json.loads(response.read().decode('utf-8'))

            results = []
            if 'results' in response_data:
                for item in response_data['results'][:max_results]:
                    results.append({
                        "title": item.get('title', ''),
                        "url": item.get('url', ''),
                        "content": item.get('content', '')[:500],  # 限制内容长度
                        "source": "tavily",
                        "timestamp": datetime.now().isoformat()
                    })

            logger.info(f"[Tavily] 成功返回 {len(results)} 个结果")
            return results, None

    except urllib.error.HTTPError as e:
        error_msg = f"Tavily HTTP 错误: {e.code} - {e.reason}"
        logger.error(f"[Tavily] {error_msg}")
        return [], error_msg
    except urllib.error.URLError as e:
        error_msg = f"Tavily URL 错误: {e.reason}"
        logger.error(f"[Tavily] {error_msg}")
        return [], error_msg
    except Exception as e:
        error_msg = f"Tavily 未知错误: {str(e)}"
        logger.error(f"[Tavily] {error_msg}")
        return [], error_msg


def search_searxng(query: str, max_results: int = 5, timeout: int = 30) -> Tuple[List[Dict], Optional[str]]:
    """
    使用 SearXNG 搜索

    Args:
        query: 搜索查询
        max_results: 最大结果数量
        timeout: 超时时间（秒）

    Returns:
        (结果列表, 错误信息)
    """
    if not CONFIG["searxng"]["url"]:
        return [], "SearXNG URL 未配置"

    try:
        logger.info(f"[SearXNG] 开始搜索: {query}")

        # 构建 SearXNG API 请求
        params = {
            'q': query,
            'format': 'json',
            'language': 'en',
            'engines': 'google,bing,duckduckgo'
        }

        url = f"{CONFIG['searxng']['url']}/search?{urllib.parse.urlencode(params)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=timeout) as response:
            response_data = json.loads(response.read().decode('utf-8'))

            results = []
            if 'results' in response_data:
                for item in response_data['results'][:max_results]:
                    # 提取内容摘要
                    content = ""
                    if 'content' in item:
                        content = item['content']
                    elif 'snippet' in item:
                        content = item['snippet']

                    results.append({
                        "title": item.get('title', ''),
                        "url": item.get('url', ''),
                        "content": content[:500] if content else '',
                        "source": "searxng",
                        "timestamp": datetime.now().isoformat()
                    })

            logger.info(f"[SearXNG] 成功返回 {len(results)} 个结果")
            return results, None

    except urllib.error.HTTPError as e:
        error_msg = f"SearXNG HTTP 错误: {e.code} - {e.reason}"
        logger.error(f"[SearXNG] {error_msg}")
        return [], error_msg
    except urllib.error.URLError as e:
        error_msg = f"SearXNG URL 错误: {e.reason}"
        logger.error(f"[SearXNG] {error_msg}")
        return [], error_msg
    except Exception as e:
        error_msg = f"SearXNG 未知错误: {str(e)}"
        logger.error(f"[SearXNG] {error_msg}")
        return [], error_msg


def search_brave(query: str, max_results: int = 5, timeout: int = 30) -> Tuple[List[Dict], Optional[str]]:
    """
    使用 Brave Search API 搜索

    Args:
        query: 搜索查询
        max_results: 最大结果数量
        timeout: 超时时间（秒）

    Returns:
        (结果列表, 错误信息)
    """
    try:
        logger.info(f"[Brave] 开始搜索: {query}")

        # 构建 Brave Search API 请求
        params = {
            'q': query,
            'count': max_results
        }

        url = f"{CONFIG['brave']['api_base']}?{urllib.parse.urlencode(params)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }

        # 如果配置了 API Key，添加到请求头
        if CONFIG["brave"]["api_key"]:
            headers['X-Subscription-Token'] = CONFIG["brave"]["api_key"]

        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=timeout) as response:
            response_data = json.loads(response.read().decode('utf-8'))

            results = []
            if 'web' in response_data and 'results' in response_data['web']:
                for item in response_data['web']['results'][:max_results]:
                    results.append({
                        "title": item.get('title', ''),
                        "url": item.get('url', ''),
                        "content": item.get('description', '')[:500],
                        "source": "brave",
                        "timestamp": datetime.now().isoformat()
                    })

            logger.info(f"[Brave] 成功返回 {len(results)} 个结果")
            return results, None

    except urllib.error.HTTPError as e:
        error_msg = f"Brave HTTP 错误: {e.code} - {e.reason}"
        logger.error(f"[Brave] {error_msg}")
        return [], error_msg
    except urllib.error.URLError as e:
        error_msg = f"Brave URL 错误: {e.reason}"
        logger.error(f"[Brave] {error_msg}")
        return [], error_msg
    except Exception as e:
        error_msg = f"Brave 未知错误: {str(e)}"
        logger.error(f"[Brave] {error_msg}")
        return [], error_msg


def search(
    query: str,
    max_results: int = 5,
    timeout: int = 30,
    sources: Optional[List[str]] = None
) -> List[Dict]:
    """
    统一的搜索接口 - 自动 Fallback 机制

    Args:
        query: 搜索查询
        max_results: 最大结果数量
        timeout: 超时时间（秒）
        sources: 指定使用的搜索源列表（可选），默认使用所有源

    Returns:
        统一格式的搜索结果列表

    示例:
        >>> results = search("Python 编程", max_results=5)
        >>> for r in results:
        ...     print(f"{r['title']} - {r['source']}")
    """
    if not query or not query.strip():
        logger.warning("搜索查询为空")
        return []

    logger.info(f"开始搜索: '{query}' (max_results={max_results}, timeout={timeout})")

    # 确定搜索源顺序
    if sources:
        # 使用指定的搜索源
        search_sources = sources
    else:
        # 默认顺序：Tavily → 百度 → SearXNG → Brave
        search_sources = ["tavily", "baidu", "searxng", "brave"]

    # 搜索源对应的函数
    search_functions = {
        "tavily": search_tavily,
        "baidu": search_baidu,
        "searxng": search_searxng,
        "brave": search_brave
    }

    # 记录所有错误
    errors = []

    # 尝试每个搜索源
    for source_name in search_sources:
        search_func = search_functions.get(source_name)
        if not search_func:
            logger.warning(f"未知搜索源: {source_name}")
            continue

        logger.info(f"尝试使用 {source_name} 搜索...")

        try:
            results, error = search_func(query, max_results, timeout)

            if results:
                logger.info(f"✓ {source_name} 搜索成功，返回 {len(results)} 个结果")
                return results
            else:
                logger.warning(f"✗ {source_name} 搜索失败: {error}")
                errors.append(f"{source_name}: {error}")

        except Exception as e:
            error_msg = f"{source_name} 搜索异常: {str(e)}"
            logger.error(f"✗ {error_msg}")
            errors.append(error_msg)
            continue

    # 所有搜索源都失败
    error_summary = "所有搜索源都失败:\n" + "\n".join(f"  - {e}" for e in errors)
    logger.error(error_summary)

    # 返回包含错误信息的空结果
    return [{
        "title": "搜索失败",
        "url": "",
        "content": error_summary,
        "source": "error",
        "timestamp": datetime.now().isoformat()
    }]


def search_all_sources(
    query: str,
    max_results: int = 5,
    timeout: int = 30
) -> Dict[str, List[Dict]]:
    """
    尝试所有搜索源，返回所有结果（用于比较和测试）

    Args:
        query: 搜索查询
        max_results: 最大结果数量
        timeout: 超时时间（秒）

    Returns:
        字典，键为搜索源名称，值为结果列表

    示例:
        >>> all_results = search_all_sources("Python 编程")
        >>> print(f"Tavily: {len(all_results['tavily'])} 个结果")
        >>> print(f"SearXNG: {len(all_results['searxng'])} 个结果")
    """
    logger.info(f"尝试所有搜索源: '{query}'")

    search_functions = {
        "tavily": search_tavily,
        "baidu": search_baidu,
        "searxng": search_searxng,
        "brave": search_brave
    }

    all_results = {}

    for source_name, search_func in search_functions.items():
        try:
            results, error = search_func(query, max_results, timeout)
            if results:
                all_results[source_name] = results
                logger.info(f"✓ {source_name}: {len(results)} 个结果")
            else:
                all_results[source_name] = []
                logger.warning(f"✗ {source_name}: {error}")
        except Exception as e:
            all_results[source_name] = []
            logger.error(f"✗ {source_name}: {str(e)}")

    return all_results


def print_results(results: List[Dict], show_content: bool = False):
    """
    打印搜索结果（便于调试）

    Args:
        results: 搜索结果列表
        show_content: 是否显示内容
    """
    if not results:
        print("无搜索结果")
        return

    print(f"\n找到 {len(results)} 个结果:\n")
    print("=" * 80)

    for i, result in enumerate(results, 1):
        print(f"\n[{i}] {result['title']}")
        print(f"    来源: {result['source']}")
        print(f"    URL: {result['url']}")
        if show_content and result['content']:
            print(f"    内容: {result['content'][:200]}...")
        print("=" * 80)


def main():
    """
    命令行入口

    用法:
        python3 search-wrapper.py <query> [max_results] [options]

    选项:
        --all: 尝试所有搜索源
        --verbose: 显示详细内容
    """
    if len(sys.argv) < 2:
        print("用法: python3 search-wrapper.py <query> [max_results] [options]")
        print("")
        print("选项:")
        print("  --all       尝试所有搜索源")
        print("  --verbose   显示详细内容")
        print("")
        print("示例:")
        print("  python3 search-wrapper.py 'Python 编程' 5")
        print("  python3 search-wrapper.py 'AI 技术' 10 --all")
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 5
    show_all = "--all" in sys.argv
    verbose = "--verbose" in sys.argv

    if show_all:
        print(f"尝试所有搜索源: '{query}'")
        all_results = search_all_sources(query, max_results)

        print("\n" + "=" * 80)
        for source_name, results in all_results.items():
            print(f"\n{source_name.upper()} ({len(results)} 个结果):")
            print("-" * 80)
            print_results(results, verbose)
    else:
        print(f"搜索: '{query}'")
        results = search(query, max_results)
        print_results(results, verbose)


if __name__ == "__main__":
    main()
