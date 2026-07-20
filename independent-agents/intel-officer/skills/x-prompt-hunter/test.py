#!/usr/bin/env python3
"""
AI 提示词系统 - 测试脚本
测试各模块的基本功能
"""

import json
import os
import sys

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import yaml


def load_config():
    """加载配置文件"""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def test_config_loading():
    """测试配置加载"""
    print("测试 1: 配置文件加载...")
    try:
        config = load_config()
        print(f"✓ 配置加载成功")
        print(f"  - 语义去重: {config.get('semantic_dedup', {}).get('enabled')}")
        print(f"  - GitHub: {config.get('github', {}).get('enabled')}")
        print(f"  - HuggingFace: {config.get('huggingface', {}).get('enabled')}")
        print(f"  - LLM Judge: {config.get('llm_judge', {}).get('enabled')}")
        print(f"  - Langfuse: {config.get('langfuse', {}).get('enabled')}")
        return True
    except Exception as e:
        print(f"✗ 配置加载失败: {e}")
        return False


def test_semantic_dedup():
    """测试语义去重"""
    print("\n测试 2: 语义去重模块...")
    try:
        from semantic_dedup import SemanticDedup

        config = {
            "enabled": True,
            "model_name": "all-MiniLM-L6-v2",
            "similarity_threshold": 0.85,
            "batch_size": 32,
            "log_file": "data/deduplication_log.json"
        }

        dedup = SemanticDedup(config)

        # 测试数据
        test_prompts = [
            {"text": "Write a story about a cat"},
            {"text": "Write a story about a feline"},  # 相似
            {"text": "Create a python function to sort a list"},
        ]

        deduplicated, stats = dedup.deduplicate(test_prompts)

        print(f"✓ 去重成功")
        print(f"  - 原始数量: {stats['original_count']}")
        print(f"  - 保留数量: {stats['kept_count']}")
        print(f"  - 移除数量: {stats['removed_prompts']}")
        print(f"  - 移除率: {stats['removal_rate']:.2%}")

        return True
    except Exception as e:
        print(f"✗ 去重测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fetcher():
    """测试数据抓取模块"""
    print("\n测试 3: 数据源抓取模块...")
    try:
        from github_hf_fetcher import PromptFetcher

        config = {
            "github": {"enabled": False},  # 禁用以避免 API 调用
            "huggingface": {"enabled": False}
        }

        fetcher = PromptFetcher(config)
        print("✓ 抓取模块初始化成功")

        # 测试文本提取
        test_text = '''
        Here is a prompt: "Write a creative story about space exploration"

        Another prompt: "Generate a summary of the following text"
        '''

        extracted = fetcher._extract_prompts_from_text(
            test_text,
            source="test",
            file_path="test.txt"
        )

        print(f"✓ 文本提取成功")
        print(f"  - 提取数量: {len(extracted)}")
        for i, prompt in enumerate(extracted[:2]):
            print(f"  - 提示词 {i+1}: {prompt['text'][:50]}...")

        return True
    except Exception as e:
        print(f"✗ 抓取模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_judge():
    """测试 LLM 评估模块（不实际调用 API）"""
    print("\n测试 4: LLM 评估模块...")
    try:
        from llm_judge import LLMJudge

        config = {
            "enabled": True,
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20241022",
            "api_key": "",  # 空 key，不会实际调用 API
            "evaluation_criteria": ["innovation", "practicality", "clarity", "reusability"],
            "output_file": "data/evaluation_results.json",
            "batch_size": 10
        }

        judge = LLMJudge(config)
        print("✓ LLM Judge 初始化成功")

        # 测试评估提示词生成
        test_prompt_text = "Write a short story about a robot learning to love"
        eval_prompt = judge._create_evaluation_prompt(test_prompt_text)

        print(f"✓ 评估提示词生成成功")
        print(f"  - 提示词长度: {len(eval_prompt)} 字符")

        # 测试统计功能
        test_evaluations = [
            {
                "innovation": 8,
                "practicality": 9,
                "clarity": 7,
                "reusability": 8,
                "total_score": 8.0
            },
            {
                "innovation": 6,
                "practicality": 7,
                "clarity": 9,
                "reusability": 6,
                "total_score": 7.0
            }
        ]

        judge.evaluation_history = test_evaluations
        stats = judge.get_statistics()

        print(f"✓ 统计功能正常")
        print(f"  - 总评估数: {stats['total_evaluations']}")
        print(f"  - 平均总分: {stats['average_total_score']:.2f}")
        print(f"  - 最高分: {stats['highest_score']}")
        print(f"  - 最低分: {stats['lowest_score']}")

        return True
    except Exception as e:
        print(f"✗ LLM Judge 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_langfuse_tracker():
    """测试 Langfuse 追踪模块"""
    print("\n测试 5: Langfuse 追踪模块...")
    try:
        from langfuse_tracker import LangfuseTracker

        config = {
            "enabled": True,
            "public_key": "",
            "secret_key": "",
            "host": "https://cloud.langfuse.com",
            "project_name": "prompt-hunter-test",
            "output_dir": "data/langfuse_reports"
        }

        tracker = LangfuseTracker(config)
        print("✓ Langfuse Tracker 初始化成功")

        # 测试报告生成（不实际发送数据）
        report = tracker.generate_trend_report(days=30)

        print(f"✓ 趋势报告生成成功")
        print(f"  - 报告天数: {report['period']['days']}")
        print(f"  - 项目名称: {report['project']}")

        return True
    except Exception as e:
        print(f"✗ Langfuse Tracker 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sample_workflow():
    """测试完整工作流程（使用模拟数据）"""
    print("\n测试 6: 完整工作流程...")
    try:
        from semantic_dedup import SemanticDedup

        # 创建测试数据
        test_prompts = [
            {"text": f"Prompt number {i} about topic {i % 5}"}
            for i in range(20)
        ]

        # 添加一些重复
        test_prompts.append({"text": "Prompt number 0 about topic 0"})
        test_prompts.append({"text": "Prompt number 1 about topic 1"})

        print(f"✓ 创建测试数据: {len(test_prompts)} 个提示词")

        # 去重
        dedup_config = {
            "enabled": True,
            "model_name": "all-MiniLM-L6-v2",
            "similarity_threshold": 0.85,
            "batch_size": 32,
            "log_file": "data/deduplication_log.json"
        }

        dedup = SemanticDedup(dedup_config)
        deduplicated, stats = dedup.deduplicate(test_prompts)

        print(f"✓ 去重完成")
        print(f"  - 保留: {stats['kept_count']}/{stats['original_count']}")

        # 保存结果
        output_file = "data/test_prompts.json"
        os.makedirs("data", exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(deduplicated, f, ensure_ascii=False, indent=2)

        print(f"✓ 结果保存到: {output_file}")

        return True
    except Exception as e:
        print(f"✗ 工作流程测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("="*60)
    print("AI 提示词系统 - 功能测试")
    print("="*60)

    results = []

    # 运行测试
    results.append(("配置加载", test_config_loading()))
    results.append(("语义去重", test_semantic_dedup()))
    results.append(("数据抓取", test_fetcher()))
    results.append(("LLM 评估", test_llm_judge()))
    results.append(("Langfuse 追踪", test_langfuse_tracker()))
    results.append(("完整工作流程", test_sample_workflow()))

    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:.<30} {status}")

    print("-"*60)
    print(f"总计: {passed}/{total} 通过 ({passed/total*100:.1f}%)")
    print("="*60)

    # 检查是否所有测试都通过
    if passed == total:
        print("\n🎉 所有测试通过！系统已准备就绪。")
        print("\n下一步:")
        print("1. 配置环境变量（复制 .env.example 为 .env 并填入 API 密钥）")
        print("2. 运行完整流程: python3 main.py pipeline --help")
        print("3. 查看文档: cat README.md")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
