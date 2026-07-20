#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCLI Hotspot Grabber v3.0 - 混合架构版
支持：
- NewsNow MCP（30+ 平台，快速）
- opencli（有登录态）
- 缓存机制（30 分钟默认）
- 模块化架构
"""

import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Windows 编码修复
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

# 导入路由模块
from router import fetch_all_platforms, get_router_stats, clear_cache


class HotspotGrabberV3:
    """热点抓取器 v3.0（混合架构）"""
    
    def __init__(self, output_dir: str = "tmp", use_cache: bool = True):
        self.output_dir = Path(output_dir)
        self.use_cache = use_cache
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def grab(self, platforms: List[str], limit: int = 50) -> Dict[str, Any]:
        """
        抓取热点
        
        Args:
            platforms: 平台列表
            limit: 每个平台返回数量
        
        Returns:
            结果字典
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ts_file = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        print(f"\n{'='*60}")
        print(f"  OpenCLI Hotspot Grabber v3.0 (混合架构)")
        print(f"  时间：{timestamp}")
        print(f"  平台：{', '.join(platforms)}")
        print(f"  缓存：{'启用' if self.use_cache else '禁用'}")
        print(f"{'='*60}\n")
        
        # 抓取
        results = fetch_all_platforms(platforms, limit, self.use_cache)
        
        # 构建输出
        output = {
            'version': '3.0.0',
            'timestamp': timestamp,
            'platforms': {},
            'summary': {'total': 0},
            'errors': []
        }
        
        for platform, items in results.items():
            if items:
                output['platforms'][platform] = {
                    'count': len(items),
                    'items': items
                }
                output['summary'][platform] = len(items)
                output['summary']['total'] += len(items)
            else:
                output['errors'].append(f"{platform}: 抓取失败")
                output['platforms'][platform] = {'count': 0, 'items': []}
        
        # 保存结果
        json_path = self.output_dir / f"hotspots-{ts_file}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        print(f"\n{'='*60}")
        print(f"  总计：{output['summary']['total']} items")
        for platform, count in output['summary'].items():
            if platform != 'total':
                print(f"  {platform}: {count}")
        if output['errors']:
            print(f"  错误：{len(output['errors'])}")
        print(f"{'='*60}")
        print(f"\n  输出：{json_path}\n")
        
        return output
    
    def stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return get_router_stats()
    
    def clear_cache(self, platform: str = None) -> int:
        """清除缓存"""
        return clear_cache(platform)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='OpenCLI Hotspot Grabber v3.0')
    parser.add_argument('--output', '-o', default='tmp', help='输出目录')
    parser.add_argument('--platforms', '-p', nargs='+', help='指定平台列表')
    parser.add_argument('--limit', '-l', type=int, default=50, help='每个平台返回数量')
    parser.add_argument('--no-cache', action='store_true', help='禁用缓存')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--clear-cache', action='store_true', help='清除缓存')
    parser.add_argument('--quiet', '-q', action='store_true', help='安静模式')
    
    args = parser.parse_args()
    
    grabber = HotspotGrabberV3(output_dir=args.output, use_cache=not args.no_cache)
    
    # 显示统计
    if args.stats:
        stats = grabber.stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return 0
    
    # 清除缓存
    if args.clear_cache:
        count = grabber.clear_cache()
        print(f"已清除 {count} 个缓存文件")
        return 0
    
    # 默认平台
    platforms = args.platforms or ['zhihu', 'weibo', 'bilibili']
    
    # 抓取
    result = grabber.grab(platforms, limit=args.limit)
    
    # 输出 JSON
    if not args.quiet:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return 0 if not result['errors'] else 1


if __name__ == '__main__':
    sys.exit(main())
