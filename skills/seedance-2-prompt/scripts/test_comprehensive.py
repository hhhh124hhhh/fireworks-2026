#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面测试 mild_mode 功能
"""

import sys
from pathlib import Path

# 添加脚本路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from prompt_generator import PromptGenerator


def test_combat_scenes():
    """测试各种打戏场景"""
    print("=" * 80)
    print("全面测试 Seedance 2.0 提示词生成器 - 打戏场景")
    print("=" * 80)
    print()

    generator = PromptGenerator()

    test_cases = [
        {
            "name": "竹林剑战",
            "scene": "两位剑客在竹林中决战",
            "style": "武侠",
            "mild_mode": True
        },
        {
            "name": "雨夜决斗",
            "scene": "两位武术大师在雨夜中切磋",
            "style": "写实",
            "mild_mode": True
        },
        {
            "name": "街头拳战",
            "scene": "两位拳手在街头激烈对决",
            "style": "写实",
            "mild_mode": False
        },
        {
            "name": "霓虹夜战",
            "scene": "武术大师在霓虹灯下展示剑术",
            "style": "赛博朋克",
            "mild_mode": True
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-' * 80}")
        print(f"测试 {i}: {test_case['name']} (mild_mode={test_case['mild_mode']})")
        print(f"场景: {test_case['scene']}")
        print(f"风格: {test_case['style']}")
        print(f"{'-' * 80}")

        result = generator.generate_prompt_with_timing(
            scene=test_case['scene'],
            style=test_case['style'],
            duration="15s",
            difficulty="ADVANCED",
            video_type="camera-movement",
            mild_mode=test_case['mild_mode'],
            use_template=False
        )

        prompt_text = result['prompt']

        # 检查关键词
        intense_keywords = ["招招致命", "胜负已分", "停止攻击", "击杀", "杀戮", "致死"]
        mild_keywords = ["切磋", "竞技", "表演", "艺术", "展示", "行礼"]

        has_intense = any(keyword in prompt_text for keyword in intense_keywords)
        has_mild = any(keyword in prompt_text for keyword in mild_keywords)

        print(f"\n生成的提示词:")
        print(prompt_text[:200] + "...")

        if test_case['mild_mode']:
            print(f"\n✅ 温和模式验证:")
            print(f"  - 是否包含激烈词汇: {has_intense} (应为 False)")
            print(f"  - 是否包含温和词汇: {has_mild} (应为 True)")
            if not has_intense and has_mild:
                print(f"  ✓ 验证通过")
            else:
                print(f"  ✗ 验证失败")
        else:
            print(f"\n✅ 激烈模式验证:")
            print(f"  - 是否包含激烈词汇: {has_intense} (应为 True)")
            print(f"  - 是否包含温和词汇: {has_mild} (可能)")
            if has_intense:
                print(f"  ✓ 验证通过")
            else:
                print(f"  ✗ 验证失败")

        # 显示分段
        print(f"\n分段预览:")
        for segment, content in result['segments'].items():
            print(f"  {segment}: {content[:50]}...")

    print("\n" + "=" * 80)
    print("✅ 全面测试完成！")
    print("=" * 80)


def test_non_combat_scenes():
    """测试非打戏场景不受影响"""
    print("\n" + "=" * 80)
    print("测试非打戏场景（不受 mild_mode 影响）")
    print("=" * 80)
    print()

    generator = PromptGenerator()

    test_cases = [
        {
            "scene": "一位年轻女性在花园里散步",
            "style": "浪漫"
        },
        {
            "scene": "主角在咖啡馆里喝咖啡",
            "style": "写实"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'-' * 80}")
        print(f"测试 {i}: {test_case['scene']}")
        print(f"{'-' * 80}")

        # 测试两种模式，确保结果一致
        result1 = generator.generate_prompt_with_timing(
            scene=test_case['scene'],
            style=test_case['style'],
            duration="15s",
            difficulty="ADVANCED",
            video_type="camera-movement",
            mild_mode=True,
            use_template=False
        )

        result2 = generator.generate_prompt_with_timing(
            scene=test_case['scene'],
            style=test_case['style'],
            duration="15s",
            difficulty="ADVANCED",
            video_type="camera-movement",
            mild_mode=False,
            use_template=False
        )

        # 非打戏场景两种模式应该生成相同的结果
        if result1['prompt'] == result2['prompt']:
            print(f"✅ 两种模式生成结果一致 (正确)")
        else:
            print(f"✗ 两种模式生成结果不一致 (可能有问题)")
            print(f"  模式1: {result1['prompt'][:100]}...")
            print(f"  模式2: {result2['prompt'][:100]}...")

    print("\n" + "=" * 80)
    print("✅ 非打戏场景测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    test_combat_scenes()
    test_non_combat_scenes()
