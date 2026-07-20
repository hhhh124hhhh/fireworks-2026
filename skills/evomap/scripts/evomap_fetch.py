#!/usr/bin/env python3
"""
EvoMap Fetch - 获取推广资产和悬赏任务
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evomap_client import EvoMapClient
import argparse


def main():
    parser = argparse.ArgumentParser(description='获取推广资产和悬赏任务')
    parser.add_argument('--node-id', type=str, required=True, help='你的节点ID')
    parser.add_argument('--hub-url', type=str, default='https://evomap.ai', help='EvoMap Hub URL（默认：https://evomap.ai）')
    parser.add_argument('--asset-type', type=str, default='Capsule', help='资产类型（默认：Capsule）')
    parser.add_argument('--include-tasks', action='store_true', help='包含悬赏任务')
    
    args = parser.parse_args()
    
    print("📥 获取推广资产和悬赏任务")
    print("=" * 50)
    print(f"🆔 节点ID: {args.node_id}")
    print(f"📦 资产类型: {args.asset_type}")
    print(f"🎯 包含任务: {args.include_tasks}")
    
    client = EvoMapClient(node_id=args.node_id, hub_url=args.hub_url)
    
    # 发送 fetch 请求
    print("\n📥 发送 fetch 请求...")
    response = client.fetch(
        asset_type=args.asset_type,
        include_tasks=args.include_tasks
    )
    
    if response:
        print("\n✅ 获取成功！")
        
        # 显示资产
        if 'assets' in response and response['assets']:
            print(f"\n📦 推广资产（{len(response['assets'])}）:")
            for i, asset in enumerate(response['assets'][:10], 1):  # 只显示前 10 个
                print(f"\n   {i}. {asset.get('type', 'Unknown')}")
                print(f"      摘要: {asset.get('summary', 'N/A')}")
                if 'outcome' in asset:
                    outcome = asset['outcome']
                    print(f"      结果: {outcome.get('status', 'N/A')}, score: {outcome.get('score', 'N/A')}")
                if 'trigger' in asset:
                    print(f"      触发: {', '.join(asset['trigger'])}")
        else:
            print("\n📦 没有推广资产")
        
        # 显示任务
        if args.include_tasks and 'tasks' in response and response['tasks']:
            print(f"\n🎯 悬赏任务（{len(response['tasks'])}）:")
            for i, task in enumerate(response['tasks'][:10], 1):  # 只显示前 10 个
                print(f"\n   {i}. {task.get('title', 'Untitled')}")
                print(f"      任务ID: {task.get('task_id', 'N/A')}")
                print(f"      信号: {task.get('signals', 'N/A')}")
                if 'bounty_id' in task:
                    print(f"      悬赏ID: {task['bounty_id']}")
                if 'min_reputation' in task:
                    print(f"      最小声誉: {task['min_reputation']}")
                if 'expires_at' in task:
                    print(f"      过期时间: {task['expires_at']}")
                print(f"      状态: {task.get('status', 'N/A')}")
        elif args.include_tasks:
            print("\n🎯 没有悬赏任务")
        
        print(f"\n📝 完整响应:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
        print("\n❌ 获取失败")
        sys.exit(1)


if __name__ == "__main__":
    import json
    main()
