"""
Zhihu Fetcher - 知乎热榜抓取
使用 opencli + 备用方案
"""

import subprocess
import json
import sys
from typing import List, Dict, Optional


def fetch_zhihu(limit: int = 30) -> Optional[List[Dict]]:
    """
    抓取知乎热榜
    
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
        cmd = f"opencli zhihu hot --limit {limit} -f json"
        
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
                print(f"  zhihu: {len(data)} items (opencli)")
                # 标准化格式
                for i, item in enumerate(data):
                    item['platform'] = 'zhihu'
                    item['category'] = 'discussion'
                    item['priority'] = 'P0' if i < 20 else 'P1'
                    item['source'] = 'opencli'
                return data
        
        print(f"  zhihu: opencli empty")
        return None
        
    except subprocess.TimeoutExpired:
        print(f"  zhihu: timeout (30s)")
        return None
    except json.JSONDecodeError as e:
        print(f"  zhihu: JSON error - {e}")
        return None
    except Exception as e:
        print(f"  zhihu: error - {e}")
        return None


if __name__ == '__main__':
    # 测试代码
    print("=== Zhihu Fetcher 测试 ===")
    print()
    
    items = fetch_zhihu(limit=5)
    if items:
        for i, item in enumerate(items, 1):
            title = item.get('title', 'N/A')
            hot = item.get('hot', 'N/A')
            print(f"  {i}. {title} (热度：{hot})")
    else:
        print("  无数据")
