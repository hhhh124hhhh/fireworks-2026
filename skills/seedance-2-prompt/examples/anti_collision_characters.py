#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 防撞脸人物提示词生成示例
展示如何使用人物特征生成器防止撞脸
"""

import sys
import random
from pathlib import Path

# 添加脚本路径
script_dir = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(script_dir))

from character_generator import CharacterGenerator


def example_1_single_character():
    """示例 1：单个人物场景"""
    print("示例 1：单个人物场景")
    print("-" * 50)

    generator = CharacterGenerator()
    char = generator.generate_unique_character()

    # 格式化为 Seedance 2.0 提示词
    prompt = (
        f"{generator.format_character_for_prompt(char)}，"
        "在海边看日落，唯美风格，超高清电影级画质，"
        "黄金时刻光线，浪漫氛围，电影感"
    )

    print(f"提示词：\n{prompt}\n")


def example_2_multiple_characters():
    """示例 2：多个人物场景"""
    print("示例 2：多个人物场景")
    print("-" * 50)

    generator = CharacterGenerator()
    characters = generator.generate_multiple_characters(3)

    # 生成多人物提示词
    char_descs = [generator.format_character_for_prompt(c) for c in characters]
    prompt = (
        f"{char_descs[0]}和{char_descs[1]}在咖啡馆聊天，"
        f"{char_descs[2]}在旁边看书，"
        "都市风格，超高清电影级画质，室内柔光，温馨氛围"
    )

    print(f"提示词：\n{prompt}\n")


def example_3_character_series():
    """示例 3：人物系列（连续剧）"""
    print("示例 3：人物系列（防止连续剧撞脸）")
    print("-" * 50)

    generator = CharacterGenerator()

    # 为连续剧生成 5 个不同场景的同一人物
    print("同一人物，5 个不同场景：\n")

    char = generator.generate_unique_character()
    scenes = [
        ("在清晨的公园里慢跑", "清新的晨光"),
        ("在办公室里工作", "明亮的办公室灯光"),
        ("在咖啡馆里休息", "温馨的咖啡厅氛围"),
        ("在夜市里逛街", "霓虹灯点缀的夜市"),
        ("在海边看日落", "黄金时刻的暖光")
    ]

    for i, (action, lighting) in enumerate(scenes, 1):
        prompt = (
            f"{generator.format_character_for_prompt(char)}，{action}，"
            "都市风格，超高清电影级画质，"
            f"{lighting}，自然表情"
        )
        print(f"场景 {i}：")
        print(f"{prompt}\n")


def example_4_different_ages():
    """示例 4：不同年龄的人物"""
    print("示例 4：不同年龄的人物（增加多样性）")
    print("-" * 50)

    generator = CharacterGenerator()
    characters = generator.generate_multiple_characters(5)

    print("5 个不同年龄段的人物：\n")

    ages = set()
    for i, char in enumerate(characters, 1):
        ages.add(char['年龄'])
        prompt = (
            f"{generator.format_character_for_prompt(char)}，"
            "在花园里赏花，唯美风格，"
            "超高清电影级画质，自然光线"
        )
        print(f"人物 {i}（{char['年龄']}）：")
        print(f"{prompt}\n")

    print(f"✅ 覆盖 {len(ages)} 个不同年龄段")


def example_5_consistent_character():
    """示例 5：一致性人物（角色设定）"""
    print("示例 5：一致性人物（固定角色设定）")
    print("-" * 50)

    generator = CharacterGenerator()

    # 固定角色设定
    fixed_character = {
        '脸型': '瓜子脸',
        '眼睛': '杏仁眼',
        '眉毛': '柳叶眉',
        '鼻子': '高鼻梁',
        '嘴唇': '樱桃小嘴',
        '发型': '中长发',
        '发色': '黑色',
        '肤色': '白皙皮肤',
        '年龄': '20-25岁青年',
        '气质': '知性气质',
        '身高': '165cm标准',
        '体型': '匀称健康',
        '服饰风格': '简约时尚'
    }

    scenes = [
        "在图书馆里看书",
        "在咖啡馆里写东西",
        "在公园里散步",
        "在海边思考",
        "在教室里上课"
    ]

    print("固定角色（主角），5 个场景：\n")

    for i, scene in enumerate(scenes, 1):
        # 格式化固定角色
        char_desc = (
            f"一位{fixed_character['年龄']}，{fixed_character['气质']}的女性，"
            f"{fixed_character['脸型']}，{fixed_character['肤色']}，"
            f"{fixed_character['发型']}，{fixed_character['发色']}，"
            f"{fixed_character['眼睛']}，{fixed_character['眉毛']}，"
            f"{fixed_character['鼻子']}，{fixed_character['嘴唇']}，"
            f"{fixed_character['身高']}，{fixed_character['体型']}"
        )

        prompt = (
            f"{char_desc}，{scene}，"
            "文艺风格，超高清电影级画质，自然光线"
        )

        print(f"场景 {i}：")
        print(f"{prompt}\n")

    print("✅ 同一角色，5 个场景，角色特征完全一致")


def main():
    """运行所有示例"""
    print("🎭 Seedance 2.0 防撞脸 - 人物特征生成器示例")
    print("=" * 70)
    print()

    examples = [
        ("1. 单个人物场景", example_1_single_character),
        ("2. 多个人物场景", example_2_multiple_characters),
        ("3. 人物系列（连续剧）", example_3_character_series),
        ("4. 不同年龄的人物", example_4_different_ages),
        ("5. 一致性人物（角色设定）", example_5_consistent_character)
    ]

    for title, example_func in examples:
        print(f"\n{title}")
        print("=" * 70)
        example_func()
        print()


if __name__ == '__main__':
    main()
