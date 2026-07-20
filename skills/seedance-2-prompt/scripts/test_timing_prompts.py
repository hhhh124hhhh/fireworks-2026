#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试时间分段提示词生成功能
"""

import sys
from pathlib import Path

# 添加脚本路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from prompt_generator import PromptGenerator

def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def print_test_case(name, result):
    """打印测试用例结果"""
    print_section(f"测试用例：{name}")
    print(f"\n风格：{result.get('style', '未指定')}")
    print(f"时长：{result.get('duration', '15s')}")
    print(f"难度：{result.get('difficulty', 'ADVANCED')}")
    print(f"视频类型：{result.get('video_type', 'photo-realistic')}")

    print("\n--- 时间分段 ---")
    segments = result.get('segments', {})
    for segment_name, segment_content in segments.items():
        print(f"\n[{segment_name}]")
        print(segment_content)

    print("\n--- 完整提示词 ---")
    full_prompt = result.get('prompt', '')
    print(full_prompt)

    print("\n--- 验证 ---")
    word_count = result.get('word_count', len(full_prompt))
    segment_count = len(segments)

    print(f"✅ 提示词长度：{word_count} 字 {'✓ 通过' if word_count > 100 else '✗ 未通过（需要 > 100 字）'}")
    print(f"✅ 时间分段数量：{segment_count} {'✓ 通过' if segment_count == 4 else '✗ 未通过（需要 4 个分段）'}")

    # 检查每个分段是否有明确的情感变化
    emotion_checks = []
    for segment_name in segments.keys():
        segment = segments[segment_name]
        has_emotion = any(keyword in segment for keyword in ["表情", "情感", "眼神", "微笑", "满足", "喜悦", "悲伤", "惊讶"])
        emotion_checks.append(has_emotion)

    has_emotion_changes = sum(emotion_checks) >= 2  # 至少2个分段有情感描述
    print(f"✅ 情感变化：{'✓ 通过' if has_emotion_changes else '✗ 未通过（需要明确的情感变化）'}")

    # 检查环境互动
    full_text = full_prompt
    env_keywords = ["雨", "光", "风", "霓虹", "雪", "火焰", "海", "树", "科技", "城市", "水花", "水珠", "光影", "树叶", "电子"]
    has_env_interaction = any(keyword in full_text for keyword in env_keywords)
    print(f"✅ 环境互动：{'✓ 通过' if has_env_interaction else '✗ 未通过（需要环境互动描述）'}")

    # 总体通过
    all_passed = (word_count > 100 and segment_count == 4 and has_emotion_changes and has_env_interaction)
    print(f"\n{'🎉 测试通过！' if all_passed else '❌ 测试未通过'}")

    return all_passed

def main():
    """主测试函数"""
    generator = PromptGenerator()

    print_section("Seedance 2.0 时间分段提示词生成测试")

    test_cases = [
        {
            "name": "赛博朋克雨夜",
            "scene": "赛博朋克雨夜，霓虹灯闪烁，未来城市",
            "style": "科幻"
        },
        {
            "name": "童话花园",
            "scene": "童话花园，色彩鲜艳，魔法氛围",
            "style": "童话"
        },
        {
            "name": "武术竹林",
            "scene": "武术竹林，飘逸动作，水墨风格",
            "style": "武侠"
        },
        {
            "name": "巴黎咖啡馆",
            "scene": "巴黎咖啡馆，浪漫氛围，阳光透过窗户",
            "style": "浪漫"
        }
    ]

    results = []
    for test_case in test_cases:
        result = generator.generate_prompt_with_timing(
            scene=test_case["scene"],
            style=test_case["style"],
            duration="15s",
            difficulty="ADVANCED",
            video_type="photo-realistic"
        )

        # 添加风格到结果中
        result["style"] = test_case["style"]

        passed = print_test_case(test_case["name"], result)
        results.append({
            "name": test_case["name"],
            "passed": passed
        })

    # 总结
    print_section("测试总结")
    total = len(results)
    passed = sum(1 for r in results if r["passed"])

    for r in results:
        status = "✅ 通过" if r["passed"] else "❌ 未通过"
        print(f"{r['name']}: {status}")

    print(f"\n总计：{passed}/{total} 通过")
    print(f"\n{'🎉 所有测试通过！' if passed == total else '❌ 部分测试未通过'}")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
