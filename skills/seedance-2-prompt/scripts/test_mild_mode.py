#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 mild_mode 功能
"""

import sys
from pathlib import Path

# 添加脚本路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from prompt_generator import PromptGenerator


def test_mild_mode():
    """测试温和模式功能"""
    print("=" * 80)
    print("测试 Seedance 2.0 提示词生成器 - 温和模式")
    print("=" * 80)
    print()

    generator = PromptGenerator()

    # 测试1：温和模式
    print("-" * 80)
    print("测试1：温和模式 (mild_mode=True)")
    print("-" * 80)
    result_mild = generator.generate_prompt_with_timing(
        scene="两位武术大师在竹林中精彩切磋",
        style="武侠",
        duration="15s",
        difficulty="ADVANCED",
        video_type="camera-movement",
        mild_mode=True,
        use_template=False  # 禁用模板库，使用自动生成
    )
    print("\n生成的提示词:")
    print(result_mild['prompt'])
    print()
    print("分段:")
    for segment, content in result_mild['segments'].items():
        print(f"  {segment}: {content}")
    print()

    # 验证温和模式
    prompt_text = result_mild['prompt']
    assert "招招致命" not in prompt_text, "❌ 温和模式不应包含'招招致命'"
    assert "胜负已分" not in prompt_text, "❌ 温和模式不应包含'胜负已分'"
    assert "停止攻击" not in prompt_text, "❌ 温和模式不应包含'停止攻击'"
    assert "切磋" in prompt_text or "竞技" in prompt_text or "表演" in prompt_text, "❌ 温和模式应包含'切磋'、'竞技'或'表演'"
    print("✅ 温和模式测试通过")

    # 测试2：激烈模式（默认）
    print("\n" + "-" * 80)
    print("测试2：激烈模式 (mild_mode=False，默认)")
    print("-" * 80)
    result_intense = generator.generate_prompt_with_timing(
        scene="两位侠客在竹林中决战",
        style="武侠",
        duration="15s",
        difficulty="ADVANCED",
        video_type="camera-movement",
        mild_mode=False,
        use_template=False  # 禁用模板库，使用自动生成
    )
    print("\n生成的提示词:")
    print(result_intense['prompt'])
    print()
    print("分段:")
    for segment, content in result_intense['segments'].items():
        print(f"  {segment}: {content}")
    print()

    # 验证激烈模式
    prompt_text_intense = result_intense['prompt']
    assert "招招致命" in prompt_text_intense or "胜负已分" in prompt_text_intense or "停止攻击" in prompt_text_intense, "❌ 激烈模式应包含'招招致命'、'胜负已分'或'停止攻击'"
    print("✅ 激烈模式测试通过")

    # 测试3：非打戏场景（不受影响）
    print("\n" + "-" * 80)
    print("测试3：非打戏场景（不受 mild_mode 影响）")
    print("-" * 80)
    result_romantic = generator.generate_prompt_with_timing(
        scene="一位年轻女性在花园里散步",
        style="浪漫",
        duration="15s",
        difficulty="ADVANCED",
        video_type="camera-movement",
        mild_mode=True
    )
    print("\n生成的提示词:")
    print(result_romantic['prompt'])
    print()
    print("分段:")
    for segment, content in result_romantic['segments'].items():
        print(f"  {segment}: {content}")
    print()
    print("✅ 非打戏场景测试通过")

    print("\n" + "=" * 80)
    print("✅ 所有测试通过！")
    print("=" * 80)


if __name__ == "__main__":
    test_mild_mode()
