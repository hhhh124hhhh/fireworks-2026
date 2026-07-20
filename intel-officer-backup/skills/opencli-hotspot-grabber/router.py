"""
Router Module - 智能路由层
根据平台和配置选择最佳抓取源

更新 (2026-03-24): 
- 优先使用 NewsNow MCP
- 降级到 opencli
"""

from typing import List, Dict, Optional, Callable
import time
import sys
import subprocess
import json

# 导入缓存模块
from cache import get_cached, set_cache, clear_cache, get_cache_stats

# 导入抓取模块
from fetcher import fetch_zhihu, fetch_weibo, fetch_bilibili, fetch_from_newsnow_mcp

# 路由配置
# 优先级：1=NewsNow MCP(最快), 2=opencli(有登录态)
ROUTE_CONFIG = {
    'zhihu': {
        'priority': ['newsnow_mcp', 'opencli'],
        'cache_ttl': 1800,  # 30 分钟
    },
    'weibo': {
        'priority': ['newsnow_mcp', 'opencli'],
        'cache_ttl': 300,  # 5 分钟（微博更新快）
    },
    'bilibili': {
        'priority': ['newsnow_mcp', 'opencli'],
        'cache_ttl': 1800,
    },
    'douyin': {
        'priority': ['newsnow_mcp', 'opencli'],
        'cache_ttl': 300,
    },
    'toutiao': {
        'priority': ['newsnow_mcp', 'opencli'],
        'cache_ttl': 300,
    },
    'baidu': {
        'priority': ['newsnow_mcp', 'opencli'],
        'cache_ttl': 300,
    },
    'hackernews': {
        'priority': ['newsnow_mcp', 'opencli'],
        'cache_ttl': 1800,
    },
    'v2ex': {
        'priority': ['newsnow_mcp', 'opencli'],
        'cache_ttl': 1800,
    },
    'reddit': {
        'priority': ['opencli'],  # NewsNow MCP 不支持
        'cache_ttl': 1800,
    },
    'twitter': {
        'priority': ['opencli'],
        'cache_ttl': 300,
    },
    'youtube': {
        'priority': ['opencli'],
        'cache_ttl': 1800,
    },
    'xiaohongshu': {
        'priority': ['opencli'],
        'cache_ttl': 600,
    },
}

# 抓取函数映射
FETCHERS = {
    'zhihu': fetch_zhihu,
    'weibo': fetch_weibo,
    'bilibili': fetch_bilibili,
}


def fetch_platform(platform: str, limit: int = 50, use_cache: bool = True) -> Optional[List[Dict]]:
    """
    智能抓取平台热点
    
    Args:
        platform: 平台 ID
        limit: 返回数量限制
        use_cache: 是否使用缓存
    
    Returns:
        热点列表，失败返回 None
    """
    start_time = time.time()
    
    # 检查缓存
    if use_cache:
        cached = get_cached(platform)
        if cached:
            return cached
    
    # 获取路由配置
    config = ROUTE_CONFIG.get(platform, {'priority': ['opencli'], 'cache_ttl': 1800})
    priority_list = config['priority']
    
    # 按优先级尝试抓取
    for source in priority_list:
        try:
            items = None
            
            if source == 'newsnow_mcp':
                items = fetch_from_newsnow_mcp(platform, limit)
            elif source == 'opencli':
                fetcher = FETCHERS.get(platform)
                if fetcher:
                    items = fetcher(limit)
                else:
                    # 未知平台，尝试通用 opencli 命令
                    items = fetch_generic_opencli(platform, limit)
            
            # 成功获取
            if items:
                # 保存到缓存
                if use_cache:
                    set_cache(platform, items)
                
                elapsed = time.time() - start_time
                print(f"  {platform}: {elapsed:.2f}s")
                return items
            
            print(f"  {platform}: {source} empty, trying next")
            
        except Exception as e:
            print(f"  {platform}: {source} error - {e}")
            continue
    
    # 所有源都失败
    print(f"  {platform}: all sources failed")
    return None


def fetch_from_newsnow_mcp(platform: str, limit: int = 50) -> Optional[List[Dict]]:
    """
    通过 NewsNow API 抓取热点
    
    Args:
        platform: 平台 ID
        limit: 返回数量限制
    
    Returns:
        热点列表
    """
    try:
        # Windows 编码修复
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        code = f'''
import requests
import json
BASE_URL = "https://newsnow.busiyi.world/api/hotlist"
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
        
        print(f"  {platform}: NewsNow empty")
        return None
        
    except Exception as e:
        print(f"  {platform}: NewsNow error - {e}")
        return None


def fetch_generic_opencli(platform: str, limit: int = 50) -> Optional[List[Dict]]:
    """
    通用 opencli 抓取（用于没有专用 fetcher 的平台）
    
    Args:
        platform: 平台 ID
        limit: 返回数量限制
    
    Returns:
        热点列表
    """
    try:
        # Windows 编码修复
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # 构建 opencli 命令（Windows 需要 shell=True）
        cmd = f"opencli {platform} hot -f json --limit {limit}"
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=30,
            shell=True,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
        )
        
        # 解码输出（强制 UTF-8）
        stdout = result.stdout.decode('utf-8', errors='ignore')
        
        if result.returncode == 0 and stdout.strip():
            data = json.loads(stdout)
            if isinstance(data, list) and len(data) > 0:
                # 标准化格式
                items = []
                for item in data:
                    standardized = {
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'hot': str(item.get('hot', item.get('rank', 0))),
                        'platform': platform,
                        'source': 'opencli',
                    }
                    items.append(standardized)
                
                print(f"  {platform}: {len(items)} items (opencli)")
                return items
        
        print(f"  {platform}: opencli empty")
        return None
        
    except Exception as e:
        print(f"  {platform}: opencli error - {e}")
        return None


def fetch_all_platforms(platforms: list, limit: int = 50, use_cache: bool = True) -> Dict[str, List[Dict]]:
    """
    批量抓取多个平台
    
    Args:
        platforms: 平台 ID 列表
        limit: 每个平台返回数量限制
        use_cache: 是否使用缓存
    
    Returns:
        {platform: [items]}
    """
    results = {}
    
    for platform in platforms:
        items = fetch_platform(platform, limit, use_cache)
        results[platform] = items or []
    
    return results


def get_router_stats() -> Dict:
    """
    获取路由器统计信息
    
    Returns:
        统计信息字典
    """
    cache_stats = get_cache_stats()
    
    return {
        'cache': cache_stats,
        'platforms': list(ROUTE_CONFIG.keys()),
        'fetchers': list(FETCHERS.keys()),
        'note': '优先使用 NewsNow MCP，降级到 opencli',
    }


if __name__ == '__main__':
    # Windows 编码修复
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # 测试代码
    print("=== Router 测试 ===")
    print("Priority: NewsNow MCP > opencli")
    print()
    
    # 测试单个平台
    print("1. 测试知乎...")
    items = fetch_platform('zhihu', limit=5, use_cache=True)
    print(f"   获取 {len(items) if items else 0} 条")
    print()
    
    print("2. 测试微博...")
    items = fetch_platform('weibo', limit=5, use_cache=True)
    print(f"   获取 {len(items) if items else 0} 条")
    print()
    
    # 测试统计
    print("3. 统计信息...")
    stats = get_router_stats()
    print(f"   缓存：{stats['cache']['count']} 个文件，{stats['cache']['size_mb']} MB")
    print(f"   平台：{', '.join(stats['platforms'])}")
    print(f"   备注：{stats['note']}")
