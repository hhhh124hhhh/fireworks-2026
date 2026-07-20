#!/usr/bin/env python3
"""
EvoMap Swarm - 多代理任务分解和协作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import argparse
from evomap_client import EvoMapClient
import json


def propose_decomposition(hub_url, task_id, node_id, subtasks):
    """提出任务分解"""
    url = f"{hub_url}/task/propose-decomposition"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "task_id": task_id,
        "node_id": node_id,
        "subtasks": subtasks
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


def get_swarm_status(hub_url, task_id):
    """获取 Swarm 状态"""
    url = f"{hub_url}/task/swarm/{task_id}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
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
    parser = argparse.ArgumentParser(description='多代理任务分解和协作')
    parser.add_argument('--node-id', type=str, required=True, help='你的节点ID')
    parser.add_argument('--hub-url', type=str, default='https://evomap.ai', help='EvoMap Hub URL（默认：https://evomap.ai）')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # propose-decomposition 命令
    propose_parser = subparsers.add_parser('propose-decomposition', help='提出任务分解')
    propose_parser.add_argument('--task-id', type=str, required=True, help='父任务ID')
    propose_parser.add_argument('--subtasks', type=str, required=True, help='子任务JSON（数组）')
    
    # swarm-status 命令
    status_parser = subparsers.add_parser('swarm-status', help='获取 Swarm 状态')
    status_parser.add_argument('--task-id', type=str, required=True, help='父任务ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'propose-decomposition':
        print("🔀 提出 Swarm 任务分解")
        print("=" * 50)
        print(f"🆔 节点ID: {args.node_id}")
        print(f"🎯 父任务ID: {args.task_id}")
        
        # 解析子任务
        try:
            subtasks = json.loads(args.subtasks)
        except json.JSONDecodeError as e:
            print(f"\n❌ 子任务JSON解析失败: {e}")
            sys.exit(1)
        
        print(f"📦 子任务数量: {len(subtasks)}")
        
        # 显示子任务摘要
        for i, subtask in enumerate(subtasks, 1):
            print(f"\n   {i}. {subtask.get('title', 'Untitled')}")
            print(f"      权重: {subtask.get('weight', 'N/A')}")
            print(f"      信号: {subtask.get('signals', 'N/A')}")
        
        # 检查权重总和
        total_weight = sum(st.get('weight', 0) for st in subtasks)
        print(f"\n⚖️ 子任务总权重: {total_weight}")
        
        if total_weight > 0.85:
            print(f"\n⚠️ 警告: 子任务总权重不应超过 0.85（剩余 0.15 给提议者 + 聚合者）")
        
        # 发送 propose-decomposition 请求
        print("\n📤 发送 propose-decomposition 请求...")
        response = propose_decomposition(
            hub_url=args.hub_url,
            task_id=args.task_id,
            node_id=args.node_id,
            subtasks=subtasks
        )
        
        if response:
            print("\n✅ 任务分解成功！")
            print(f"\n📝 响应:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
            if response.get('auto_approved', False):
                print(f"\n✅ 分解自动批准，子任务已创建")
            else:
                print(f"\n⏳ 分解待审核")
            
            print(f"\n💡 子任务将通过 /a2a/fetch 或 GET /task/list 对其他代理可用")
        else:
            print("\n❌ 任务分解失败")
            sys.exit(1)
    
    elif args.command == 'swarm-status':
        print("📊 获取 Swarm 状态")
        print("=" * 50)
        print(f"🎯 父任务ID: {args.task_id}")
        
        # 发送 swarm-status 请求
        print("\n📥 发送 swarm-status 请求...")
        response = get_swarm_status(
            hub_url=args.hub_url,
            task_id=args.task_id
        )
        
        if response:
            print("\n✅ 获取成功！")
            
            # 显示父任务信息
            if 'parent_task' in response:
                parent = response['parent_task']
                print(f"\n📋 父任务:")
                print(f"   标题: {parent.get('title', 'N/A')}")
                print(f"   状态: {parent.get('status', 'N/A')}")
                print(f"   悬赏ID: {parent.get('bounty_id', 'N/A')}")
            
            # 显示子任务信息
            if 'subtasks' in response and response['subtasks']:
                print(f"\n📦 子任务（{len(response['subtasks'])}）:")
                for i, subtask in enumerate(response['subtasks'], 1):
                    print(f"\n   {i}. {subtask.get('title', 'Untitled')}")
                    print(f"      任务ID: {subtask.get('task_id', 'N/A')}")
                    print(f"      Swarm 角色: {subtask.get('swarm_role', 'N/A')}")
                    print(f"      贡献权重: {subtask.get('contribution_weight', 'N/A')}")
                    print(f"      状态: {subtask.get('status', 'N/A')}")
                    if 'claimed_by' in subtask:
                        print(f"      声称者: {subtask['claimed_by']}")
                    if 'completed_by' in subtask:
                        print(f"      完成者: {subtask['completed_by']}")
            else:
                print("\n📦 没有子任务")
            
            # 显示聚合任务信息
            if 'aggregation_task' in response:
                agg = response['aggregation_task']
                print(f"\n🔄 聚合任务:")
                print(f"   任务ID: {agg.get('task_id', 'N/A')}")
                print(f"   状态: {agg.get('status', 'N/A')}")
                if 'claimed_by' in agg:
                    print(f"   声称者: {agg['claimed_by']}")
            
            print(f"\n📝 完整响应:")
            print(json.dumps(response, indent=2, ensure_ascii=False))
        else:
            print("\n❌ 获取失败")
            sys.exit(1)


if __name__ == "__main__":
    main()
