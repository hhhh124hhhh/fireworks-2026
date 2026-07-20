#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 联网功能使用示例

展示如何使用在线搜索、模板更新等新功能
"""

import sys
from pathlib import Path

# 添加脚本路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))


def example_1_basic_prompt_generation():
    """示例 1: 基本提示词生成"""
    print("\n" + "=" * 80)
    print("示例 1: 基本提示词生成")
    print("=" * 80 + "\n")

    from prompt_generator import PromptGenerator

    generator = PromptGenerator()

    result = generator.generate_prompt(
        scene="一位年轻女性在花园里散步",
        style="梦幻",
        difficulty="INTERMEDIATE",
        video_type="photo-realistic"
    )

    print(f"提示词: {result['prompt']}")
    print(f"\n元素组成:")
    for key, value in result['elements'].items():
        if value and key != 'subject':
            print(f"  {key}: {value}")

    print(f"\n变体数量: {len(result['variants'])}")
    for i, variant in enumerate(result['variants'], 1):
        print(f"\n变体 {i}:")
        print(f"  {variant}")


def example_2_online_search():
    """示例 2: 在线搜索提示词"""
    print("\n" + "=" * 80)
    print("示例 2: 在线搜索提示词")
    print("=" * 80 + "\n")

    from search_online import search_prompts

    print("正在搜索在线提示词...")

    results = search_prompts(
        query="Seedance 2.0 提示词",
        max_results=3
    )

    if results:
        print(f"找到 {len(results)} 个结果:\n")

        for i, result in enumerate(results, 1):
            print(f"结果 {i}:")
            print(f"  标题: {result['title']}")
            print(f"  类型: {result['video_type']}")
            print(f"  难度: {result['difficulty']}")
            if result.get('prompt'):
                print(f"  提示词: {result['prompt'][:100]}...")
            print()
    else:
        print("未找到结果（可能是因为网络或搜索源配置）")


def example_3_prompt_with_online_search():
    """示例 3: 使用在线搜索生成提示词"""
    print("\n" + "=" * 80)
    print("示例 3: 使用在线搜索生成提示词")
    print("=" * 80 + "\n")

    from prompt_generator import PromptGenerator

    generator = PromptGenerator()

    result = generator.generate_prompt_with_search(
        scene="雨天城市街道",
        style="梦幻",
        difficulty="INTERMEDIATE",
        video_type="photo-realistic",
        online_search=True,
        max_online_results=3
    )

    print(f"生成的提示词: {result['prompt']}")
    print(f"\n在线搜索: {'已使用' if result.get('online_used') else '未使用'}")

    if result.get('online_used') and result.get('online_results'):
        print(f"\n找到 {len(result['online_results'])} 个在线提示词:")
        for i, online_prompt in enumerate(result['online_results'], 1):
            print(f"\n{i}. {online_prompt['title']}")
            print(f"   类型: {online_prompt['video_type']}")
            print(f"   难度: {online_prompt['difficulty']}")
            if online_prompt.get('prompt'):
                print(f"   提示词: {online_prompt['prompt'][:80]}...")


def example_4_update_templates():
    """示例 4: 更新模板库"""
    print("\n" + "=" * 80)
    print("示例 4: 更新模板库")
    print("=" * 80 + "\n")

    from update_templates import TemplateUpdater

    updater = TemplateUpdater()

    # 从搜索获取模板
    print("正在从搜索获取模板...")
    new_templates = updater.fetch_templates_from_search(
        query="Seedance 2.0 提示词",
        max_results=2
    )

    if new_templates:
        print(f"获取到 {len(new_templates)} 个模板\n")

        # 显示预览
        for i, template in enumerate(new_templates, 1):
            print(f"模板 {i}:")
            print(f"  名称: {template['name']}")
            print(f"  类型: {template['video_type']}")
            print(f"  难度: {template['difficulty']}")
            if template.get('prompt'):
                print(f"  提示词: {template['prompt'][:80]}...")
            print()

        # 询问是否更新
        print("注意: 此示例仅演示，实际更新时会提示确认")
        print("如需更新，请使用:")
        print("  python scripts/update_templates.py --search 'Seedance 2.0 提示词'")
    else:
        print("未获取到模板（可能是因为网络或搜索源配置）")


def example_5_batch_generation():
    """示例 5: 批量生成提示词"""
    print("\n" + "=" * 80)
    print("示例 5: 批量生成提示词")
    print("=" * 80 + "\n")

    from prompt_generator import PromptGenerator

    generator = PromptGenerator()

    scenes = [
        ("一位年轻女性在花园里散步", "梦幻"),
        ("雨天的城市街道", "写实"),
        ("科幻风格的太空场景", "科幻")
    ]

    for scene, style in scenes:
        print(f"\n场景: {scene} ({style})")

        result = generator.generate_prompt(
            scene=scene,
            style=style,
            difficulty="INTERMEDIATE",
            video_type="photo-realistic"
        )

        print(f"提示词: {result['prompt']}")
        print(f"推荐时长: {result['recommended_duration']}")


def example_6_interactive_generator():
    """示例 6: 交互式提示词生成器"""
    print("\n" + "=" * 80)
    print("示例 6: 交互式提示词生成器")
    print("=" * 80 + "\n")

    from prompt_generator import PromptGenerator

    generator = PromptGenerator()

    print("启动交互式生成器...")
    print("注意: 此示例展示代码，实际使用时可直接运行:")
    print("  python scripts/prompt_generator.py")
    print("\n代码示例:")
    print("""
    generator = PromptGenerator()
    generator.interactive_prompt_generator()
    """)


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("Seedance 2.0 联网功能使用示例")
    print("=" * 80)

    examples = [
        ("基本提示词生成", example_1_basic_prompt_generation),
        ("在线搜索提示词", example_2_online_search),
        ("使用在线搜索生成提示词", example_3_prompt_with_online_search),
        ("更新模板库", example_4_update_templates),
        ("批量生成提示词", example_5_batch_generation),
        ("交互式提示词生成器", example_6_interactive_generator)
    ]

    print("\n可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\n选择要运行的示例 (1-6, 或按 Enter 运行所有):")
    choice = input("> ").strip()

    if choice:
        try:
            index = int(choice) - 1
            if 0 <= index < len(examples):
                name, func = examples[index]
                func()
            else:
                print("无效的选择")
        except ValueError:
            print("无效的选择")
    else:
        # 运行所有示例
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\n示例 '{name}' 出错: {str(e)}")

    print("\n" + "=" * 80)
    print("示例运行完成")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
