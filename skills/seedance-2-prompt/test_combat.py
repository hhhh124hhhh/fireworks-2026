#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试打戏场景支持
验证 Seedance 2.0 提示词生成器是否正确识别和处理打戏场景
"""

import sys
from pathlib import Path

# 添加脚本路径
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

from prompt_generator import PromptGenerator


def test_bamboo_forest_combat():
    """测试用例 1：竹林决战"""
    print("\n" + "=" * 80)
    print("测试用例 1：竹林决战")
    print("=" * 80)

    generator = PromptGenerator()

    scene = "两位侠客在竹林中决战"

    result = generator.generate_prompt_with_timing(
        scene=scene,
        style="武侠",
        duration="15s",
        difficulty="ADVANCED",
        video_type="photo-realistic"
    )

    print(f"\n场景: {scene}")
    print(f"\n生成的提示词:\n{result['prompt']}\n")

    print("\n时间分段:")
    for segment_name, segment_text in result['segments'].items():
        print(f"\n{segment_name}:")
        print(segment_text)

    # 验证
    emotion = generator._detect_emotion(scene)
    env = generator._detect_environment(scene)

    print("\n" + "-" * 80)
    print("验证结果:")
    print("-" * 80)
    print(f"✅ 情感类型: {emotion} (期望: combat)")
    print(f"✅ 环境类型: {env} (期望: forest_combat)")

    emotion_words = generator.EMOTION_KEYWORDS.get(emotion, {})
    if emotion_words:
        print(f"✅ 情感路径: {emotion_words['base']} → {emotion_words['rising']} → {emotion_words['peak']} → {emotion_words['soothing']}")
        print(f"   (期望: 冷静对峙 → 眼神犀利 → 激烈对战 → 胜负已分)")

    # 检查环境互动
    env_desc = generator.ENVIRONMENT_INTERACTION.get(env, "")
    if "竹叶" in env_desc or "落叶" in env_desc:
        print(f"✅ 环境互动包含竹林相关描述")

    # 检查动作描述
    main_action = result['segments']['main_action_3-7s']
    action_keywords = ["剑", "劈砍", "格挡", "剑气", "交锋"]
    if any(keyword in main_action for keyword in action_keywords):
        print(f"✅ 动作描述包含招式和力度")

    success = emotion == "combat" and env == "forest_combat"
    print(f"\n{'✅ 测试通过' if success else '❌ 测试失败'}")

    return success


def test_street_fight():
    """测试用例 2：街头对战"""
    print("\n" + "=" * 80)
    print("测试用例 2：街头对战")
    print("=" * 80)

    generator = PromptGenerator()

    scene = "两位拳手在街头激烈对决"

    result = generator.generate_prompt_with_timing(
        scene=scene,
        style="写实",
        duration="15s",
        difficulty="ADVANCED",
        video_type="photo-realistic"
    )

    print(f"\n场景: {scene}")
    print(f"\n生成的提示词:\n{result['prompt']}\n")

    print("\n时间分段:")
    for segment_name, segment_text in result['segments'].items():
        print(f"\n{segment_name}:")
        print(segment_text)

    # 验证
    emotion = generator._detect_emotion(scene)
    env = generator._detect_environment(scene)

    print("\n" + "-" * 80)
    print("验证结果:")
    print("-" * 80)
    print(f"✅ 情感类型: {emotion} (期望: combat)")
    print(f"✅ 环境类型: {env} (期望: urban_combat)")

    # 检查动作描述
    main_action = result['segments']['main_action_3-7s']
    action_keywords = ["拳", "格挡", "反攻", "拳风", "冲击"]
    found_keywords = [kw for kw in action_keywords if kw in main_action]
    if found_keywords:
        print(f"✅ 动作描述包含: {', '.join(found_keywords)}")

    # 检查环境互动
    env_desc = generator.ENVIRONMENT_INTERACTION.get(env, "")
    if "混凝土" in env_desc or "劲波" in env_desc or "烟尘" in env_desc:
        print(f"✅ 环境互动包含街头打斗效果")

    success = emotion == "combat" and env == "urban_combat"
    print(f"\n{'✅ 测试通过' if success else '❌ 测试失败'}")

    return success


def test_rain_combat():
    """测试用例 3：雨中激战"""
    print("\n" + "=" * 80)
    print("测试用例 3：雨中激战")
    print("=" * 80)

    generator = PromptGenerator()

    scene = "两位剑客在雨中激烈交锋"

    result = generator.generate_prompt_with_timing(
        scene=scene,
        style="武侠",
        duration="15s",
        difficulty="ADVANCED",
        video_type="photo-realistic"
    )

    print(f"\n场景: {scene}")
    print(f"\n生成的提示词:\n{result['prompt']}\n")

    print("\n时间分段:")
    for segment_name, segment_text in result['segments'].items():
        print(f"\n{segment_name}:")
        print(segment_text)

    # 验证
    emotion = generator._detect_emotion(scene)
    env = generator._detect_environment(scene)

    print("\n" + "-" * 80)
    print("验证结果:")
    print("-" * 80)
    print(f"✅ 情感类型: {emotion} (期望: combat)")
    print(f"✅ 环境类型: {env} (期望: rain_combat)")

    # 检查环境互动
    env_desc = generator.ENVIRONMENT_INTERACTION.get(env, "")
    env_keywords = ["雨水", "飞溅", "水珠", "剑气"]
    found_keywords = [kw for kw in env_keywords if kw in env_desc]
    if found_keywords:
        print(f"✅ 环境互动包含: {', '.join(found_keywords)}")

    # 检查动作描述
    main_action = result['segments']['main_action_3-7s']
    action_keywords = ["剑", "劈砍", "剑气", "交锋", "移动"]
    found_action_keywords = [kw for kw in action_keywords if kw in main_action]
    if found_action_keywords:
        print(f"✅ 动作描述包含: {', '.join(found_action_keywords)}")

    success = emotion == "combat" and env == "rain_combat"
    print(f"\n{'✅ 测试通过' if success else '❌ 测试失败'}")

    return success


def run_all_tests():
    """运行所有测试用例"""
    print("\n" + "=" * 80)
    print("🧪 Seedance 2.0 打戏场景测试")
    print("=" * 80)

    results = {
        "竹林决战": test_bamboo_forest_combat(),
        "街头对战": test_street_fight(),
        "雨中激战": test_rain_combat()
    }

    print("\n" + "=" * 80)
    print("📊 测试总结")
    print("=" * 80)

    total = len(results)
    passed = sum(1 for success in results.values() if success)

    for test_name, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")

    print(f"\n总计: {passed}/{total} 个测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！打戏场景支持已成功优化。")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，需要进一步调试。")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
