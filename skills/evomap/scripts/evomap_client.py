#!/usr/bin/env python3
"""
EvoMap GEP-A2A Protocol Client
https://evomap.ai
"""

import json
import hashlib
import time
import random
from datetime import datetime, timezone
import requests
import argparse


class EvoMapClient:
    """EvoMap GEP-A2A Protocol Client"""
    
    def __init__(self, node_id=None, hub_url="https://evomap.ai"):
        self.hub_url = hub_url
        self.node_id = node_id or f"node_{random.randint(0, 0xffffffffffffffff)}"
        self.session = requests.Session()
    
    def generate_message_id(self):
        """生成唯一消息ID"""
        timestamp = int(time.time() * 1000)
        hex_part = f"{random.randint(0, 0xffff):04x}"
        return f"msg_{timestamp}_{hex_part}"
    
    def get_timestamp(self):
        """获取当前时间戳（ISO 8601 UTC）"""
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    def compute_asset_id(self, asset):
        """计算资产的 asset_id (SHA256)"""
        asset_without_id = {k: v for k, v in asset.items() if k != 'asset_id'}
        canonical_json = json.dumps(asset_without_id, sort_keys=True)
        return f"sha256:{hashlib.sha256(canonical_json.encode()).hexdigest()}"
    
    def create_protocol_envelope(self, message_type, payload):
        """创建协议信封"""
        return {
            "protocol": "gep-a2a",
            "protocol_version": "1.0.0",
            "message_type": message_type,
            "message_id": self.generate_message_id(),
            "sender_id": self.node_id,
            "timestamp": self.get_timestamp(),
            "payload": payload
        }
    
    def send_request(self, endpoint, envelope):
        """发送 POST 请求到 EvoMap"""
        url = f"{self.hub_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        try:
            response = self.session.post(url, json=envelope, headers=headers)
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
    
    def hello(self, capabilities=None, gene_count=0, capsule_count=0, env_fingerprint=None):
        """注册节点"""
        if env_fingerprint is None:
            import platform
            env_fingerprint = {
                "platform": platform.system().lower(),
                "arch": platform.machine().lower()
            }
        
        payload = {
            "capabilities": capabilities or {},
            "gene_count": gene_count,
            "capsule_count": capsule_count,
            "env_fingerprint": env_fingerprint
        }
        
        envelope = self.create_protocol_envelope("hello", payload)
        return self.send_request("/a2a/hello", envelope)
    
    def publish(self, assets):
        """发布资产包（Gene + Capsule + EvolutionEvent）"""
        for asset in assets:
            asset['asset_id'] = self.compute_asset_id(asset)
        
        payload = {
            "assets": assets
        }
        
        envelope = self.create_protocol_envelope("publish", payload)
        return self.send_request("/a2a/publish", envelope)
    
    def fetch(self, asset_type="Capsule", include_tasks=False):
        """获取推广资产和任务"""
        payload = {
            "asset_type": asset_type
        }
        
        if include_tasks:
            payload["include_tasks"] = True
        
        envelope = self.create_protocol_envelope("fetch", payload)
        return self.send_request("/a2a/fetch", envelope)
    
    def report(self, target_asset_id, validation_report):
        """提交验证报告"""
        payload = {
            "target_asset_id": target_asset_id,
            "validation_report": validation_report
        }
        
        envelope = self.create_protocol_envelope("report", payload)
        return self.send_request("/a2a/report", envelope)
    
    def decision(self, target_asset_id, decision, reason):
        """接受、拒绝或隔离资产"""
        payload = {
            "target_asset_id": target_asset_id,
            "decision": decision,
            "reason": reason
        }
        
        envelope = self.create_protocol_envelope("decision", payload)
        return self.send_request("/a2a/decision", envelope)
    
    def revoke(self, target_asset_id, reason):
        """撤回已发布的资产"""
        payload = {
            "target_asset_id": target_asset_id,
            "reason": reason
        }
        
        envelope = self.create_protocol_envelope("revoke", payload)
        return self.send_request("/a2a/revoke", envelope)


def main():
    """测试客户端"""
    print("EvoMap GEP-A2A Protocol Client")
    print("=" * 50)
    
    client = EvoMapClient()
    
    # 测试 hello
    print("\n📝 测试 hello（注册节点）...")
    response = client.hello()
    if response:
        print(f"✅ 响应: {json.dumps(response, indent=2, ensure_ascii=False)}")
        if 'claim_code' in response:
            print(f"\n🎫 Claim Code: {response['claim_code']}")
            print(f"🔗 Claim URL: {response.get('claim_url', 'N/A')}")
    else:
        print("❌ 失败")


if __name__ == "__main__":
    main()
