#!/usr/bin/env python3
"""
AI 提示词系统 - 主入口
集成语义去重、数据源抓取、LLM 评估和 Langfuse 追踪
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

import yaml

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from github_hf_fetcher import PromptFetcher
from llm_judge import LLMJudge
from langfuse_tracker import LangfuseTracker

# 延迟导入 SemanticDedup（仅在需要时导入）
SemanticDedup = None


def setup_logging(config: Dict):
    """设置日志"""
    log_config = config.get("logging", {})
    log_level = getattr(logging, log_config.get("level", "INFO"))
    log_format = log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    log_file = log_config.get("file", "logs/prompt_hunter.log")

    # 确保日志目录存在
    os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else ".", exist_ok=True)

    # 配置日志
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> Dict:
    """加载配置文件"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cmd_fetch(args, config: Dict):
    """抓取提示词命令"""
    logger = logging.getLogger(__name__)

    fetcher = PromptFetcher(config)

    logger.info("Fetching prompts from all sources...")

    results = fetcher.fetch_all(
        query=args.query,
        limit_per_source=args.limit
    )

    # 保存结果
    data_config = config.get("data", {})
    prompts_file = data_config.get("prompts_file", "data/prompts.json")

    fetcher.save_prompts(results.get("all", []), prompts_file)

    print(f"\n✓ Fetched {len(results.get('all', []))} prompts total")
    print(f"  - GitHub: {len(results.get('github', []))}")
    print(f"  - HuggingFace: {len(results.get('huggingface', []))}")
    print(f"  Saved to: {prompts_file}")


def cmd_deduplicate(args, config: Dict):
    """语义去重命令"""
    logger = logging.getLogger(__name__)

    # 加载提示词
    data_config = config.get("data", {})
    input_file = args.input or data_config.get("prompts_file", "data/prompts.json")

    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    logger.info(f"Loaded {len(prompts)} prompts from {input_file}")

    # 延迟导入 SemanticDedup
    global SemanticDedup
    if SemanticDedup is None:
        from semantic_dedup import SemanticDedup as SD
        SemanticDedup = SD

    # 初始化去重器
    dedup = SemanticDedup(config.get("semantic_dedup", {}))

    # 执行去重
    deduplicated, stats = dedup.deduplicate(prompts)

    # 保存结果
    output_file = args.output or input_file.replace(".json", "_deduplicated.json")

    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(deduplicated, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Deduplication completed")
    print(f"  Original: {stats['original_count']} prompts")
    print(f"  Kept: {stats['kept_count']} prompts")
    print(f"  Removed: {stats['removed_count']} prompts ({stats['removal_rate']:.2%})")
    print(f"  Saved to: {output_file}")


def cmd_evaluate(args, config: Dict):
    """评估提示词命令"""
    logger = logging.getLogger(__name__)

    # 加载提示词
    data_config = config.get("data", {})
    input_file = args.input or data_config.get("prompts_file", "data/prompts.json")

    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    logger.info(f"Loaded {len(prompts)} prompts from {input_file}")

    # 初始化评估器
    judge = LLMJudge(config.get("llm_judge", {}))

    # 初始化追踪器
    tracker = LangfuseTracker(config.get("langfuse", {}))

    # 评估
    results = judge.evaluate_batch(prompts, batch_size=args.batch_size)

    # 追踪结果
    if results:
        tracker.track_batch_evaluation(
            prompts[:len(results)],
            results,
            batch_metadata={"batch_size": len(results)}
        )
        tracker.flush()

    print(f"\n✓ Evaluation completed for {len(results)} prompts")

    # 显示统计
    stats = judge.get_statistics()
    if stats:
        print(f"  Average total score: {stats['average_total_score']:.2f}/10")
        print(f"  Highest score: {stats['highest_score']}/10")
        print(f"  Lowest score: {stats['lowest_score']}/10")


def cmd_report(args, config: Dict):
    """生成报告命令"""
    logger = logging.getLogger(__name__)

    tracker = LangfuseTracker(config.get("langfuse", {}))

    if args.type == "trend":
        report = tracker.generate_trend_report(days=args.days)
        print(f"\n✓ Trend report generated")
        print(f"  Period: last {args.days} days")
    elif args.type == "comparison":
        report = tracker.compare_periods(days1=args.days1, days2=args.days2)
        print(f"\n✓ Comparison report generated")
    elif args.type == "metrics":
        report = tracker.export_metrics()
        print(f"\n✓ Metrics exported")
    else:
        logger.error(f"Unknown report type: {args.type}")
        return

    # 打印报告路径
    if "error" not in report:
        print(f"  Saved to: {tracker.output_dir}")


def cmd_pipeline(args, config: Dict):
    """完整流程命令：抓取 -> 去重 -> 评估"""
    logger = logging.getLogger(__name__)

    print("\n" + "="*60)
    print("STARTING FULL PIPELINE")
    print("="*60 + "\n")

    # 1. 抓取
    print("Step 1: Fetching prompts...")
    fetcher = PromptFetcher(config)
    results = fetcher.fetch_all(query=args.query, limit_per_source=args.limit)

    data_config = config.get("data", {})
    prompts_file = data_config.get("prompts_file", "data/prompts.json")
    fetcher.save_prompts(results.get("all", []), prompts_file)
    print(f"✓ Fetched {len(results.get('all', []))} prompts\n")

    # 2. 去重（如果启用）
    dedup_config = config.get("semantic_dedup", {})
    if dedup_config.get("enabled", True):
        print("Step 2: Deduplicating...")
        with open(prompts_file, "r", encoding="utf-8") as f:
            prompts = json.load(f)

        # 延迟导入 SemanticDedup
        global SemanticDedup
        if SemanticDedup is None:
            from semantic_dedup import SemanticDedup as SD
            SemanticDedup = SD

        dedup = SemanticDedup(dedup_config)
        deduplicated, stats = dedup.deduplicate(prompts)

        dedup_file = prompts_file.replace(".json", "_deduplicated.json")
        with open(dedup_file, "w", encoding="utf-8") as f:
            json.dump(deduplicated, f, ensure_ascii=False, indent=2)

        print(f"✓ Deduplicated: {stats['kept_count']}/{stats['original_count']} kept\n")
        prompts_to_evaluate = deduplicated
    else:
        print("Step 2: Skipping deduplication (disabled in config)\n")
        with open(prompts_file, "r", encoding="utf-8") as f:
            prompts_to_evaluate = json.load(f)

    # 3. 评估
    print("Step 3: Evaluating...")
    judge = LLMJudge(config.get("llm_judge", {}))
    tracker = LangfuseTracker(config.get("langfuse", {}))

    # 限制评估数量以节省 API 调用
    evaluate_limit = min(args.evaluate_limit, len(prompts_to_evaluate))
    prompts_to_evaluate = prompts_to_evaluate[:evaluate_limit]

    results = judge.evaluate_batch(prompts_to_evaluate, batch_size=args.batch_size)

    if results:
        tracker.track_batch_evaluation(
            prompts_to_evaluate,
            results,
            batch_metadata={"pipeline_run": True}
        )
        tracker.flush()

    print(f"✓ Evaluated {len(results)} prompts\n")

    # 4. 生成报告
    print("Step 4: Generating report...")
    report = tracker.generate_trend_report(days=30)
    print("✓ Report generated\n")

    print("="*60)
    print("PIPELINE COMPLETED")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(description="AI 提示词系统")

    # 全局参数
    parser.add_argument("--config", "-c", default="config.yaml", help="配置文件路径")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # fetch 命令
    fetch_parser = subparsers.add_parser("fetch", help="抓取提示词")
    fetch_parser.add_argument("--query", "-q", help="搜索查询")
    fetch_parser.add_argument("--limit", "-l", type=int, default=50, help="每个数据源的抓取数量")

    # deduplicate 命令
    dedup_parser = subparsers.add_parser("deduplicate", help="语义去重")
    dedup_parser.add_argument("--input", "-i", help="输入文件")
    dedup_parser.add_argument("--output", "-o", help="输出文件")

    # evaluate 命令
    eval_parser = subparsers.add_parser("evaluate", help="评估提示词")
    eval_parser.add_argument("--input", "-i", help="输入文件")
    eval_parser.add_argument("--batch-size", "-b", type=int, default=10, help="批次大小")

    # report 命令
    report_parser = subparsers.add_parser("report", help="生成报告")
    report_parser.add_argument("--type", "-t", choices=["trend", "comparison", "metrics"], help="报告类型")
    report_parser.add_argument("--days", "-d", type=int, default=30, help="天数（用于趋势报告）")
    report_parser.add_argument("--days1", type=int, default=30, help="第一个时间段天数")
    report_parser.add_argument("--days2", type=int, default=30, help="第二个时间段天数")

    # pipeline 命令
    pipeline_parser = subparsers.add_parser("pipeline", help="运行完整流程")
    pipeline_parser.add_argument("--query", "-q", help="搜索查询")
    pipeline_parser.add_argument("--limit", "-l", type=int, default=50, help="抓取数量")
    pipeline_parser.add_argument("--batch-size", "-b", type=int, default=10, help="评估批次大小")
    pipeline_parser.add_argument("--evaluate-limit", type=int, default=20, help="评估数量限制")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 加载配置
    config = load_config(args.config)

    # 设置日志
    setup_logging(config)

    # 执行命令
    if args.command == "fetch":
        cmd_fetch(args, config)
    elif args.command == "deduplicate":
        cmd_deduplicate(args, config)
    elif args.command == "evaluate":
        cmd_evaluate(args, config)
    elif args.command == "report":
        cmd_report(args, config)
    elif args.command == "pipeline":
        cmd_pipeline(args, config)


if __name__ == "__main__":
    main()
