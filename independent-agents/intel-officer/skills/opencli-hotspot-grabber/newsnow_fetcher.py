#!/usr/bin/env python
# encoding: utf-8
"""
NewsNow API 热点抓取模块 - ⚠️ 已废弃

⚠️ 废弃日期：2026-03-24
⚠️ 原因：API 服务返回 HTML 页面而非 JSON 数据
✅ 替代方案：使用 opencli CLI

原 API 来源：https://newsnow.busiyi.world/
"""

import requests
import json
import sys
import os
import subprocess
from typing import List, Dict, Optional
from datetime import datetime

# ⚠️ 废弃标记
DEPRECATED = True
DEPRECATED_DATE = "2026-03-24"
DEPRECATED_REASON = "API 服务返回 HTML 页面而非 JSON 数据"

# NewsNow API 基础 URL（已废弃）
BASE_URL = "https://newsnow.busiyi.world/api/hotlist"

# 平台映射
PLATFORM_MAP = {
    'zhihu': 'zhihu',
    'weibo': 'weibo',
    'bilibili': 'bilibili',
    'douyin': 'douyin',
    'toutiao': 'toutiao',
    'baidu': 'baidu',
    'thepaper': 'thepaper',
    'cls': 'cls',
    'wallstreetcn': 'wallstreetcn',
    'tieba': 'tieba',
}

# 请求头
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
}

TIMEOUT = 10
MAX_RETRIES = 3


def fetch_platform_hotlist(platform: str, limit: int = 50) -> List[Dict]:
    """
    ⚠️ 已废弃：NewsNow API 不再可用
    
    ✅ 替代方案：使用 opencli CLI
    
    Args:
        platform: 平台 ID
        limit: 返回数量限制
    
    Returns:
        热点列表（现在调用 opencli）
    """
    print(f"⚠️ NewsNow API 已废弃 ({DEPRECATED_DATE}): {DEPRECATED_REASON}")
    print(f"✅ 降级使用 opencli: {platform}")
    
    # 降级到 opencli
    return fetch_via_opencli(platform, limit)


def fetch_via_opencli(platform: str, limit: int = 50) -> List[Dict]:
    """
    通过 opencli CLI 抓取热点（替代方案）
    
    Args:
        platform: 平台 ID
        limit: 返回数量限制
    
    Returns:
        热点列表
    """
    try:
        # 构建 opencli 命令
        cmd = ['opencli', platform, 'hot', '-f', 'json', '--limit', str(limit)]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, list):
                # 标准化格式
                items = []
                for item in data:
                    standardized = {
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'hot': str(item.get('hot', item.get('rank', 0))),
                        'platform': platform,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'opencli',  # 标记来源
                    }
                    items.append(standardized)
                
                print(f"✅ opencli 抓取成功：{platform} ({len(items)} 条)")
                return items
        
        print(f"⚠️ opencli 返回空：{platform}")
        return []
        
    except FileNotFoundError:
        print(f"❌ opencli 命令未找到，请确保已安装")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ opencli 响应解析失败：{e}")
        return []
    except subprocess.TimeoutExpired:
        print(f"❌ opencli 请求超时：{platform}")
        return []
    except Exception as e:
        print(f"❌ opencli 调用失败：{platform} - {e}")
        return []


def fetch_all_platforms(platforms: List[str], limit: int = 50) -> Dict[str, List[Dict]]:
    """
    批量抓取多个平台
    
    Args:
        platforms: 平台 ID 列表
        limit: 每个平台返回数量限制
    
    Returns:
        dict: {platform: [items]}
    """
    results = {}
    
    for platform in platforms:
        items = fetch_platform_hotlist(platform, limit)
        results[platform] = items
    
    return results


def get_available_platforms() -> List[str]:
    """
    获取支持的平台列表
    
    Returns:
        平台 ID 列表
    """
    return list(PLATFORM_MAP.keys())


def test_api_health() -> bool:
    """
    测试 API 是否可用
    
    Returns:
        bool: API 是否可用（总是返回 False，因为已废弃）
    """
    print(f"⚠️ NewsNow API 已废弃，请使用 opencli")
    return False


def get_deprecation_info() -> Dict:
    """
    获取废弃信息
    
    Returns:
        废弃信息字典
    """
    return {
        'deprecated': DEPRECATED,
        'date': DEPRECATED_DATE,
        'reason': DEPRECATED_REASON,
        'alternative': 'opencli',
        'migration': '所有抓取函数已自动降级到 opencli',
    }


if __name__ == '__main__':
    # Windows 编码修复
    if sys.platform == 'win32':
        os.system('chcp 65001 > nul')
        sys.stdout.reconfigure(encoding='utf-8')
    
    # 测试代码
    print("=== NewsNow API 测试 (已废弃) ===\n")
    print(f"⚠️ 废弃日期：{DEPRECATED_DATE}")
    print(f"⚠️ 原因：{DEPRECATED_REASON}")
    print(f"✅ 替代方案：opencli\n")
    
    # 显示废弃信息
    info = get_deprecation_info()
    print(f"废弃信息：{json.dumps(info, ensure_ascii=False, indent=2)}\n")
    
    # 测试 opencli 降级
    print("测试 opencli 降级抓取...\n")
    
    print("1. 测试知乎热榜...")
    items = fetch_platform_hotlist('zhihu', limit=5)
    for i, item in enumerate(items, 1):
        print(f"   {i}. {item['title']} (热度：{item['hot']})")
    print()
    
    # 测试多平台
    print("2. 测试多平台...")
    platforms = ['zhihu', 'weibo', 'bilibili']
    results = fetch_all_platforms(platforms, limit=3)
    
    for platform, items in results.items():
        print(f"   {platform}: {len(items)} items")
    print()
    
    # 输出 JSON
    print("3. 输出 JSON 格式...")
    output = {
        'timestamp': datetime.now().isoformat(),
        'source': 'opencli (NewsNow 已废弃)',
        'deprecation': info,
        'platforms': results,
        'summary': {p: len(items) for p, items in results.items()}
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
