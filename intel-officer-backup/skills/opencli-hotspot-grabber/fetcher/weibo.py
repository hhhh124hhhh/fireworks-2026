"""
Weibo Fetcher - 微博热搜抓取
使用 opencli
"""

import subprocess
import json
import sys
from typing import List, Dict, Optional


def fetch_weibo(limit: int = 50) -> Optional[List[Dict]]:
    """
    抓取微博热搜
    
    Args:
        limit: 返回数量限制
    
    Returns:
        热点列表，失败返回 None
    """
    try:
        # Windows 编码修复
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # 使用 opencli 命令（Windows 需要 shell=True）
        cmd = f"opencli weibo hot --limit {limit} -f json"
        
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
            if isinstance(data, list) and data:
                print(f"  weibo: {len(data)} items (opencli)")
                # 标准化格式
                for i, item in enumerate(data):
                    item['platform'] = 'weibo'
                    item['category'] = 'social'
                    item['priority'] = 'P0' if i < 30 else 'P2'
                    item['source'] = 'opencli'
                return data
        
        print(f"  weibo: opencli 返回空或失败")
        return None
        
    except subprocess.TimeoutExpired:
        print(f"  weibo: 超时 (30s)")
        return None
    except json.JSONDecodeError as e:
        print(f"  weibo: JSON 解析失败 - {e}")
        return None
    except Exception as e:
        print(f"  weibo: {e}")
        return None


if __name__ == '__main__':
    print("=== Weibo Fetcher 测试 ===")
    print()
    
    items = fetch_weibo(limit=5)
    if items:
        for i, item in enumerate(items, 1):
            title = item.get('title', 'N/A')
            hot = item.get('hot', 'N/A')
            print(f"  {i}. {title} (热度：{hot})")
    else:
        print("  无数据")
