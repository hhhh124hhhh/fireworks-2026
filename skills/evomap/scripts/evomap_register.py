#!/usr/bin/env python3
"""
EvoMap Register - 注册新节点到 EvoMap 网络
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evomap_client import EvoMapClient
import argparse


def main():
    parser = argparse.ArgumentParser(description='注册新节点到 EvoMap 网络')
    parser.add_argument('--node-id', type=str, help='现有节点ID（可选）')
    parser.add_argument('--hub-url', type=str, default='https://evomap.ai', help='EvoMap Hub URL（默认：https://evomap.ai）')
    parser.add_argument('--webhook-url', type=str, help='Webhook URL 用于推送通知（可选）')
    
    args = parser.parse_args()
    
    print("🚀 注册新节点到 EvoMap 网络")
    print("=" * 50)
    
    if args.node_id:
        print(f"📋 使用现有节点ID: {args.node_id}")
    else:
        print(f"📋 将生成新的节点ID")
    
    client = EvoMapClient(node_id=args.node_id, hub_url=args.hub_url)
    
    # 准备 payload
    capabilities = {}
    
    payload = {
        "capabilities": capabilities,
        "gene_count": 0,
        "capsule_count": 0
    }
    
    if args.webhook_url:
        payload["webhook_url"] = args.webhook_url
        print(f"🔗 Webhook URL: {args.webhook_url}")
    
    # 发送 hello 请求
    print("\n📤 发送 hello 请求...")
    response = client.hello(
        capabilities=capabilities,
        gene_count=0,
        capsule_count=0
    )
    
    if response:
        print("\n✅ 节点注册成功！")
        print(f"\n📝 响应:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
        if 'claim_code' in response:
            print(f"\n🎫 Claim Code: {response['claim_code']}")
            print(f"🔗 Claim URL: {response.get('claim_url', 'N/A')}")
            print(f"\n💡 请访问 Claim URL 将此节点绑定到你的 EvoMap 账户以追踪收益")
            print(f"⏰ Claim Code 有效期为 24 小时")
        
        print(f"\n🆔 你的节点ID: {client.node_id}")
        print(f"💾 请保存此 node_id，后续请求需要使用它")
        print(f"📄 建议保存到环境变量: export EVOMAP_NODE_ID={client.node_id}")
    else:
        print("\n❌ 节点注册失败")
        sys.exit(1)


if __name__ == "__main__":
    import json
    main()
