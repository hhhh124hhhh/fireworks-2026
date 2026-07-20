"""
Cache Module - 缓存机制
30 分钟默认缓存，减少重复抓取
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

# 缓存配置
CACHE_DIR = Path("cache")
CACHE_TTL = 1800  # 30 分钟（秒）
CACHE_TTL_SHORT = 300  # 5 分钟（快速更新平台）
CACHE_TTL_LONG = 3600  # 1 小时（慢速更新平台）

# 平台缓存间隔配置
PLATFORM_CACHE_TTL = {
    'zhihu': CACHE_TTL,        # 30 分钟
    'weibo': CACHE_TTL_SHORT,  # 5 分钟（微博更新快）
    'bilibili': CACHE_TTL,     # 30 分钟
    'douyin': CACHE_TTL_SHORT, # 5 分钟
    'hackernews': CACHE_TTL,   # 30 分钟
    'github': CACHE_TTL,       # 30 分钟
    'v2ex': CACHE_TTL_SHORT,   # 5 分钟
    'baidu': CACHE_TTL_SHORT,  # 5 分钟
    'toutiao': CACHE_TTL_SHORT,# 5 分钟
    'thepaper': CACHE_TTL,     # 30 分钟
    'cls': CACHE_TTL_LONG,     # 1 小时（财联社更新慢）
    'wallstreetcn': CACHE_TTL_LONG, # 1 小时
}


def get_cache_key(platform: str, params: Dict[str, Any] = None) -> str:
    """
    生成缓存键
    
    Args:
        platform: 平台 ID
        params: 额外参数（如 limit）
    
    Returns:
        缓存文件路径
    """
    key_str = f"{platform}_{json.dumps(params or {}, sort_keys=True)}"
    key_hash = hashlib.md5(key_str.encode('utf-8')).hexdigest()
    return CACHE_DIR / f"{platform}_{key_hash}.json"


def get_cached(platform: str, params: Dict[str, Any] = None) -> Optional[List[Dict]]:
    """
    获取缓存数据
    
    Args:
        platform: 平台 ID
        params: 额外参数
    
    Returns:
        缓存的热点列表，如果过期或不存在返回 None
    """
    # 确保缓存目录存在
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    cache_file = get_cache_key(platform, params)
    
    if not cache_file.exists():
        return None
    
    try:
        data = json.loads(cache_file.read_text(encoding='utf-8'))
        timestamp = data.get('timestamp', 0)
        ttl = PLATFORM_CACHE_TTL.get(platform, CACHE_TTL)
        
        # 检查是否过期
        if time.time() - timestamp > ttl:
            print(f"  [EXPIRED] {platform}: cache expired, deleting")
            cache_file.unlink(missing_ok=True)
            return None
        
        # 返回缓存数据
        age = time.time() - timestamp
        print(f"  [CACHE] {platform}: loaded from cache ({age:.0f}s ago)")
        return data.get('items', [])
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  [ERROR] {platform}: cache read failed - {e}")
        cache_file.unlink(missing_ok=True)
        return None


def set_cache(platform: str, items: List[Dict], params: Dict[str, Any] = None) -> bool:
    """
    设置缓存
    
    Args:
        platform: 平台 ID
        items: 热点列表
        params: 额外参数
    
    Returns:
        是否成功
    """
    try:
        # 确保缓存目录存在
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        cache_file = get_cache_key(platform, params)
        
        data = {
            'timestamp': time.time(),
            'platform': platform,
            'count': len(items),
            'items': items
        }
        
        cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"  [SAVE] {platform}: cache saved ({len(items)} items)")
        return True
        
    except Exception as e:
        print(f"  [ERROR] {platform}: cache save failed - {e}")
        return False


def clear_cache(platform: str = None) -> int:
    """
    清除缓存
    
    Args:
        platform: 平台 ID，如果为 None 则清除所有缓存
    
    Returns:
        清除的文件数
    """
    if not CACHE_DIR.exists():
        return 0
    
    count = 0
    if platform:
        # 清除指定平台缓存
        for cache_file in CACHE_DIR.glob(f"{platform}_*.json"):
            cache_file.unlink()
            count += 1
    else:
        # 清除所有缓存
        for cache_file in CACHE_DIR.glob("*.json"):
            cache_file.unlink()
            count += 1
    
    print(f"[CLEAR] Cleared {count} cache files")
    return count


def get_cache_stats() -> Dict[str, Any]:
    """
    获取缓存统计信息
    
    Returns:
        统计信息字典
    """
    if not CACHE_DIR.exists():
        return {'count': 0, 'size': 0, 'platforms': {}}
    
    cache_files = list(CACHE_DIR.glob("*.json"))
    total_size = sum(f.stat().st_size for f in cache_files)
    
    # 按平台统计
    platform_stats = {}
    for cache_file in cache_files:
        try:
            data = json.loads(cache_file.read_text(encoding='utf-8'))
            platform = data.get('platform', 'unknown')
            if platform not in platform_stats:
                platform_stats[platform] = {'count': 0, 'size': 0}
            platform_stats[platform]['count'] += 1
            platform_stats[platform]['size'] += cache_file.stat().st_size
        except:
            continue
    
    return {
        'count': len(cache_files),
        'size': total_size,
        'size_mb': round(total_size / 1024 / 1024, 2),
        'platforms': platform_stats
    }


if __name__ == '__main__':
    # 测试代码
    print("=== Cache Module Test ===")
    print()
    
    # 测试缓存统计
    stats = get_cache_stats()
    print(f"Cache stats: {stats['count']} files, {stats['size_mb']} MB")
