#!/usr/bin/env python3
"""
EvoMap Publish - 发布 Gene + Capsule + EvolutionEvent 包
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evomap_client import EvoMapClient
import argparse


def create_gene(category, signals_match, summary, validation=None):
    """创建 Gene"""
    return {
        "type": "Gene",
        "schema_version": "1.5.0",
        "category": category,  # repair, optimize, innovate
        "signals_match": signals_match,  # array of trigger signals
        "summary": summary,  # min 10 chars
        "validation": validation or []
    }


def create_capsule(trigger, gene_id, summary, confidence, blast_radius, outcome, env_fingerprint, success_streak=None):
    """创建 Capsule"""
    capsule = {
        "type": "Capsule",
        "schema_version": "1.5.0",
        "trigger": trigger,  # array of trigger signals
        "gene": gene_id,  # reference to Gene's asset_id
        "summary": summary,  # min 20 chars
        "confidence": confidence,  # 0-1
        "blast_radius": blast_radius,  # { "files": N, "lines": N }
        "outcome": outcome,  # { "status": "success"/"failure", "score": 0-1 }
        "env_fingerprint": env_fingerprint  # { "platform": "linux", "arch": "x64" }
    }
    
    if success_streak is not None:
        capsule["success_streak"] = success_streak
    
    return capsule


def create_evolution_event(intent, capsule_id, genes_used, outcome, mutations_tried=None, total_cycles=None):
    """创建 EvolutionEvent"""
    event = {
        "type": "EvolutionEvent",
        "intent": intent,  # repair, optimize, innovate
        "capsule_id": capsule_id,  # Capsule's asset_id
        "genes_used": genes_used,  # array of Gene asset_ids
        "outcome": outcome  # { "status": "success"/"failure", "score": 0-1 }
    }
    
    if mutations_tried is not None:
        event["mutations_tried"] = mutations_tried
    
    if total_cycles is not None:
        event["total_cycles"] = total_cycles
    
    return event


def main():
    parser = argparse.ArgumentParser(description='发布 Gene + Capsule + EvolutionEvent 包')
    parser.add_argument('--node-id', type=str, required=True, help='你的节点ID')
    parser.add_argument('--hub-url', type=str, default='https://evomap.ai', help='EvoMap Hub URL（默认：https://evomap.ai）')
    
    # Gene 参数
    parser.add_argument('--gene-category', type=str, default='repair', choices=['repair', 'optimize', 'innovate'], help='Gene 类别（默认：repair）')
    parser.add_argument('--signals', type=str, required=True, help='触发信号，逗号分隔（例如：TimeoutError,ECONNREFUSED）')
    parser.add_argument('--gene-summary', type=str, required=True, help='Gene 摘要（最少 10 个字符）')
    
    # Capsule 参数
    parser.add_argument('--capsule-summary', type=str, required=True, help='Capsule 摘要（最少 20 个字符）')
    parser.add_argument('--confidence', type=float, required=True, help='信心分数（0-1）')
    parser.add_argument('--blast-radius-files', type=int, required=True, help='影响范围 - 文件数')
    parser.add_argument('--blast-radius-lines', type=int, required=True, help='影响范围 - 行数')
    parser.add_argument('--outcome-status', type=str, default='success', choices=['success', 'failure'], help='结果状态（默认：success）')
    parser.add_argument('--outcome-score', type=float, required=True, help='结果分数（0-1）')
    parser.add_argument('--platform', type=str, default='linux', help='平台（默认：linux）')
    parser.add_argument('--arch', type=str, default='x64', help='架构（默认：x64）')
    parser.add_argument('--success-streak', type=int, help='成功连续次数（可选）')
    
    # EvolutionEvent 参数
    parser.add_argument('--intent', type=str, default='repair', choices=['repair', 'optimize', 'innovate'], help='意图（默认：repair）')
    parser.add_argument('--mutations-tried', type=int, help='尝试的突变次数（可选）')
    parser.add_argument('--total-cycles', type=int, help='总循环次数（可选）')
    
    args = parser.parse_args()
    
    print("📤 发布 Gene + Capsule + EvolutionEvent 包")
    print("=" * 50)
    
    client = EvoMapClient(node_id=args.node_id, hub_url=args.hub_url)
    
    # 解析信号
    signals = [s.strip() for s in args.signals.split(',')]
    
    # 创建 Gene
    gene = create_gene(
        category=args.gene_category,
        signals_match=signals,
        summary=args.gene_summary
    )
    
    # 创建 Capsule
    outcome = {
        "status": args.outcome_status,
        "score": args.outcome_score
    }
    
    env_fingerprint = {
        "platform": args.platform,
        "arch": args.arch
    }
    
    blast_radius = {
        "files": args.blast_radius_files,
        "lines": args.blast_radius_lines
    }
    
    capsule = create_capsule(
        trigger=signals,
        gene_id=None,  # 将在 compute_asset_id 后更新
        summary=args.capsule_summary,
        confidence=args.confidence,
        blast_radius=blast_radius,
        outcome=outcome,
        env_fingerprint=env_fingerprint,
        success_streak=args.success_streak
    )
    
    # 创建 EvolutionEvent
    evolution_event = create_evolution_event(
        intent=args.intent,
        capsule_id=None,  # 将在 compute_asset_id 后更新
        genes_used=[None],  # 将在 compute_asset_id 后更新
        outcome=outcome,
        mutations_tried=args.mutations_tried,
        total_cycles=args.total_cycles
    )
    
    # 准备资产包
    assets = [gene, capsule, evolution_event]
    
    # 显示摘要
    print(f"\n📋 Gene:")
    print(f"   类别: {gene['category']}")
    print(f"   信号: {', '.join(gene['signals_match'])}")
    print(f"   摘要: {gene['summary']}")
    
    print(f"\n📋 Capsule:")
    print(f"   触发: {', '.join(capsule['trigger'])}")
    print(f"   摘要: {capsule['summary']}")
    print(f"   信心: {capsule['confidence']}")
    print(f"   影响范围: {capsule['blast_radius']['files']} files, {capsule['blast_radius']['lines']} lines")
    print(f"   结果: {outcome['status']}, score: {outcome['score']}")
    print(f"   环境: {capsule['env_fingerprint']}")
    
    print(f"\n📋 EvolutionEvent:")
    print(f"   意图: {evolution_event['intent']}")
    print(f"   结果: {outcome['status']}, score: {outcome['score']}")
    
    # 发送 publish 请求
    print("\n📤 发送 publish 请求...")
    response = client.publish(assets)
    
    if response:
        print("\n✅ 资产发布成功！")
        print(f"\n📝 响应:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
        print("\n❌ 资产发布失败")
        sys.exit(1)


if __name__ == "__main__":
    import json
    main()
