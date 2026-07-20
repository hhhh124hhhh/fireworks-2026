#!/usr/bin/env python3
"""
EvoMap Complete Task - 完成悬赏任务并赚取积分
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import argparse
from evomap_client import EvoMapClient
import json


def complete_task(hub_url, task_id, asset_id, node_id):
    """完成悬赏任务"""
    url = f"{hub_url}/task/complete"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "task_id": task_id,
        "asset_id": asset_id,
        "node_id": node_id
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"响应: {e.response.text}")
            except:
                pass
        return None


def main():
    parser = argparse.ArgumentParser(description='完成悬赏任务并赚取积分')
    parser.add_argument('--node-id', type=str, required=True, help='你的节点ID')
    parser.add_argument('--hub-url', type=str, default='https://evomap.ai', help='EvoMap Hub URL（默认：https://evomap.ai）')
    parser.add_argument('--task-id', type=str, required=True, help='任务ID')
    parser.add_argument('--asset-id', type=str, required=True, help='资产ID（sha256:...）')
    
    args = parser.parse_args()
    
    print("🏆 完成悬赏任务并赚取积分")
    print("=" * 50)
    print(f"🆔 节点ID: {args.node_id}")
    print(f"🎯 任务ID: {args.task_id}")
    print(f"📦 资产ID: {args.asset_id}")
    
    # 发送 complete 请求
    print("\n📤 发送 task/complete 请求...")
    response = complete_task(
        hub_url=args.hub_url,
        task_id=args.task_id,
        asset_id=args.asset_id,
        node_id=args.node_id
    )
    
    if response:
        print("\n✅ 任务完成成功！")
        print(f"\n📝 响应:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
        print(f"\n💡 悬赏自动匹配中...")
        print(f"💡 当用户接受后，积分将进入你的账户")
        print(f"💡 检查收益: https://evomap.ai/billing/earnings/{args.node_id}")
    else:
        print("\n❌ 任务完成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
