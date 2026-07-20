#!/usr/bin/env python3
"""
语义去重系统测试脚本
"""

import json
import os
import tempfile
from semantic_deduplication import SemanticDeduplicator


def create_test_data():
    """创建测试数据"""
    test_prompts = [
        {"prompt": "You are a helpful assistant.", "source": "test"},
        {"prompt": "You are an AI assistant that helps users.", "source": "test"},  # 相似
        {"prompt": "Write a Python function to sort a list.", "source": "test"},
        {"prompt": "Create a Python function that sorts a list.", "source": "test"},  # 相似
        {"prompt": "What is the capital of France?", "source": "test"},  # 不相似
        {"prompt": "Explain quantum computing in simple terms.", "source": "test"},
    ]

    return test_prompts


def run_test():
    """运行测试"""
    print("=" * 80)
    print("🧪 语义去重系统测试")
    print("=" * 80)

    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False, encoding='utf-8') as f:
        input_file = f.name
        test_prompts = create_test_data()
        for prompt in test_prompts:
            f.write(json.dumps(prompt, ensure_ascii=False) + '\n')

    output_file = tempfile.mktemp(suffix='.jsonl')
    report_dir = tempfile.mkdtemp()

    try:
        # 创建去重器
        print("\n📦 创建去重器...")
        deduplicator = SemanticDeduplicator(
            model_name="all-MiniLM-L6-v2",
            similarity_threshold=0.85
        )

        # 加载测试数据
        print(f"📖 加载测试数据: {input_file}")
        prompts = deduplicator.load_prompts(input_file)
        print(f"   加载了 {len(prompts)} 个提示词")

        # 执行去重
        print("\n🔄 执行去重...")
        unique_prompts, stats = deduplicator.deduplicate(prompts)

        # 保存结果
        print(f"💾 保存结果到: {output_file}")
        deduplicator.save_results(unique_prompts, output_file)

        # 保存报告
        deduplicator.save_report(stats, [], report_dir)

        # 显示结果
        print("\n" + "=" * 80)
        print("📊 测试结果")
        print("=" * 80)
        print(f"原始提示词: {stats['total_original']}")
        print(f"去重后: {stats['total_unique']}")
        print(f"移除: {stats['total_duplicates_removed']} 个")
        print(f"去重率: {stats['dedup_rate']:.2f}%")
        print(f"平均相似度: {stats['average_similarity']:.3f}")
        print("=" * 80)

        # 显示去重后的提示词
        print("\n✨ 去重后的提示词:")
        for i, prompt in enumerate(unique_prompts, 1):
            print(f"  {i}. {prompt['text'][:60]}...")

        # 检查输出文件
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                output_count = sum(1 for line in f if line.strip())
            print(f"\n✅ 输出文件验证: {output_count} 条记录")

        print("\n✅ 测试完成！")

    finally:
        # 清理临时文件
        if os.path.exists(input_file):
            os.unlink(input_file)
        if os.path.exists(output_file):
            os.unlink(output_file)
        import shutil
        if os.path.exists(report_dir):
            shutil.rmtree(report_dir)


if __name__ == "__main__":
    try:
        run_test()
    except KeyboardInterrupt:
        print("\n⏸️  测试中断")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
