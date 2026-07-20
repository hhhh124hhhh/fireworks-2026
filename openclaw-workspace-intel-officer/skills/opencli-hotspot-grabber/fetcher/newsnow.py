"""
NewsNow MCP Fetcher - 从 NewsNow API 获取热点
支持 30+ 平台，作为第一优先级抓取源

更新 (2026-03-24): 直接调用 NewsNow API，不经过 MCP Server
"""

import json
import subprocess
import sys
from typing import List, Dict, Optional
from datetime import datetime

# NewsNow 支持的平台
NEWSNOW_PLATFORMS = [
    'zhihu', 'weibo', 'bilibili', 'douyin', 'toutiao',
    'baidu', 'thepaper', 'cls', 'wallstreetcn', 'tieba',
    'hackernews', 'github', 'v2ex', 'arxiv',
    'producthunt', 'qqvideo'
]

# NewsNow API 基础 URL
BASE_URL = "https://newsnow.busiyi.world/api/hotlist"


def fetch_from_newsnow_mcp(platform: str, limit: int = 50) -> Optional[List[Dict]]:
    """
    从 NewsNow API 获取热点
    
    Args:
        platform: 平台 ID
        limit: 返回数量限制
    
    Returns:
        热点列表，失败返回 None
    """
    if platform not in NEWSNOW_PLATFORMS:
        print(f"  {platform}: NewsNow 不支持")
        return None
    
    try:
        # Windows 编码修复
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # 直接调用 NewsNow API
        code = f'''
import requests
import json
BASE_URL = "{BASE_URL}"
try:
    resp = requests.get(BASE_URL, params={{"platform": "{platform}", "limit": {limit}}}, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, dict) and data.get("code") == 0:
            items = data.get("data", [])
            if items:
                print(json.dumps(items, ensure_ascii=False))
            else:
                print("[]")
        else:
            print("[]")
    else:
        print("[]")
except Exception as e:
    print("[]")
'''
        result = subprocess.run(
            [sys.executable, '-c', code],
            capture_output=True,
            text=True,
            timeout=15,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
        )
        
        # 解码输出
        stdout = result.stdout.decode('utf-8', errors='ignore') if isinstance(result.stdout, bytes) else result.stdout
        
        if result.returncode == 0 and stdout.strip():
            items = json.loads(stdout)
            if isinstance(items, list) and len(items) > 0:
                print(f"  {platform}: {len(items)} items (NewsNow)")
                # 标准化格式
                for item in items:
                    item['platform'] = platform
                    item['source'] = 'NewsNow'
                return items
        
        print(f"  {platform}: NewsNow 返回空")
        return None
        
    except Exception as e:
        print(f"  {platform}: NewsNow 调用失败 - {e}")
        return None


def get_newsnow_available_platforms() -> List[str]:
    """
    获取 NewsNow 支持的平台列表
    
    Returns:
        平台 ID 列表
    """
    return NEWSNOW_PLATFORMS


if __name__ == '__main__':
    # 测试代码
    print("=== NewsNow Fetcher 测试 ===")
    print()
    
    # 测试知乎
    print("1. 测试知乎...")
    items = fetch_from_newsnow_mcp('zhihu', limit=5)
    if items:
        for i, item in enumerate(items, 1):
            title = item.get('title', 'N/A')
            print(f"  {i}. {title}")
    else:
        print("  无数据")
    print()
    
    # 测试微博
    print("2. 测试微博...")
    items = fetch_from_newsnow_mcp('weibo', limit=5)
    if items:
        for i, item in enumerate(items, 1):
            title = item.get('title', 'N/A')
            print(f"  {i}. {title}")
    else:
        print("  无数据")
