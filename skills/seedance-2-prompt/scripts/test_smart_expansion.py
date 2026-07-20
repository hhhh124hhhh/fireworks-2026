#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能扩展系统综合测试
验证所有功能是否正常工作
"""

import sys
import json
from pathlib import Path

# 添加脚本路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from prompt_generator import PromptGenerator
from smart_expansion import (
    SceneTemplateLibrary,
    add_custom_template,
    auto_expand_template,
    detect_emotion,
    detect_environment
)


def test_template_library():
    """测试模板库管理"""
    print("\n" + "=" * 80)
    print("测试 1: 模板库管理")
    print("=" * 80)

    try:
        # 加载模板库
        library = SceneTemplateLibrary()
        stats = library.get_stats()

        print(f"✓ 模板库加载成功")
        print(f"  总模板数: {stats['total_templates']}")
        print(f"  情感类型: {', '.join(stats['emotion_types'])}")
        print(f"  按情感分布: {stats['emotion_distribution']}")

        # 列出所有模板
        all_templates = library.list_templates()
        print(f"✓ 成功列出所有模板")
        for emotion_type, templates in all_templates.items():
            print(f"  {emotion_type}: {len(templates)} 个")

        # 搜索模板
        search_results = library.search_templates("竹")
        print(f"✓ 搜索 '竹' 找到 {len(search_results)} 个结果")

        return True

    except Exception as e:
        print(f"✗ 模板库管理测试失败: {e}")
        return False


def test_add_custom_template():
    """测试添加自定义模板"""
    print("\n" + "=" * 80)
    print("测试 2: 添加自定义模板")
    print("=" * 80)

    try:
        # 添加自定义模板
        success = add_custom_template(
            scene_name="测试场景-雪山对决",
            intro="镜头从雪山之巅开始，寒风呼啸，雪花纷飞。两位高手在白雪皑皑的山顶对峙。",
            main_action="动作迅猛有力，剑气激起的雪尘在空中飞舞。每一次交锋都带着破冰的气势，周围的雪松被劲风摇动。",
            emotion_rise="表情从冷静对峙转为激烈对抗，眼神中燃烧着战斗的火焰。风雪似乎也随着战斗的激烈程度而增大。",
            conclusion="最终，胜负已分。胜者站在雪山之巅，雪花落在他的剑上。镜头慢慢上升，展示壮丽的雪山景色，然后淡出。",
            tags=["测试", "雪山", "对决"],
            emotion="combat",
            environment="snow"
        )

        if success:
            print("✓ 自定义模板添加成功")

            # 验证模板已添加
            library = SceneTemplateLibrary()
            template = library.get_template("测试场景-雪山对决")

            if template:
                print("✓ 模板验证成功")
                print(f"  情感: {template.get('emotion')}")
                print(f"  环境: {template.get('environment')}")
                print(f"  标签: {', '.join(template.get('tags', []))}")
                return True
            else:
                print("✗ 模板验证失败：未找到刚添加的模板")
                return False
        else:
            print("✗ 自定义模板添加失败")
            return False

    except Exception as e:
        print(f"✗ 添加自定义模板测试失败: {e}")
        return False


def test_auto_expand():
    """测试自动扩展机制"""
    print("\n" + "=" * 80)
    print("测试 3: 自动扩展机制")
    print("=" * 80)

    try:
        generator = PromptGenerator()

        # 生成新场景提示词（应该自动保存）
        scene_name = "沙漠追逐"
        print(f"生成场景: {scene_name}")

        result = generator.generate_prompt_with_timing(
            scene=scene_name,
            style="写实",
            duration="15s",
            difficulty="ADVANCED",
            use_template=False,  # 不使用模板
            auto_save=True       # 自动保存
        )

        print(f"✓ 提示词生成成功")
        print(f"  使用模板: {result.get('used_template', False)}")
        print(f"  自动保存: {result.get('auto_saved', False)}")
        print(f"  字数: {result.get('word_count', 0)}")

        # 验证自动保存是否成功
        library = SceneTemplateLibrary()
        template = library.get_template(scene_name)

        if template:
            print("✓ 自动扩展验证成功：模板已保存")
            print(f"  情感: {template.get('emotion')}")
            print(f"  环境: {template.get('environment')}")
            print(f"  自动生成标记: {template.get('auto_generated', False)}")

            # 再次生成同一场景，应该使用模板
            result2 = generator.generate_prompt_with_timing(
                scene=scene_name,
                style="写实",
                use_template=True
            )

            if result2.get('used_template'):
                print("✓ 模板使用验证成功：第二次生成使用了模板")
                return True
            else:
                print("✗ 模板使用验证失败：第二次生成未使用模板")
                return False
        else:
            print("✗ 自动扩展验证失败：模板未保存")
            return False

    except Exception as e:
        print(f"✗ 自动扩展机制测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_emotion_detection():
    """测试情感检测"""
    print("\n" + "=" * 80)
    print("测试 4: 情感检测")
    print("=" * 80)

    try:
        test_cases = [
            ("竹林决战", "combat"),
            ("开心的派对", "happy"),
            ("悲伤的故事", "sad"),
            ("浪漫的约会", "romantic"),
            ("神秘的探险", "mysterious")
        ]

        all_passed = True
        for scene, expected_emotion in test_cases:
            detected = detect_emotion(scene)
            passed = detected == expected_emotion
            status = "✓" if passed else "✗"

            print(f"{status} '{scene}' -> {detected} (期望: {expected_emotion})")

            if not passed:
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"✗ 情感检测测试失败: {e}")
        return False


def test_environment_detection():
    """测试环境检测"""
    print("\n" + "=" * 80)
    print("测试 5: 环境检测")
    print("=" * 80)

    try:
        test_cases = [
            ("竹林打斗", "forest_combat"),
            ("雨夜街斗", "rain_combat"),
            ("城市夜战", "night_combat"),
            ("雪山对决", "snow"),
            ("海边漫步", "ocean"),
            ("花园约会", "forest")
        ]

        all_passed = True
        for scene, expected_env in test_cases:
            detected = detect_environment(scene)
            passed = detected == expected_env
            status = "✓" if passed else "✗"

            print(f"{status} '{scene}' -> {detected} (期望: {expected_env})")

            if not passed:
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"✗ 环境检测测试失败: {e}")
        return False


def test_template_retrieval():
    """测试模板检索"""
    print("\n" + "=" * 80)
    print("测试 6: 模板检索和使用")
    print("=" * 80)

    try:
        generator = PromptGenerator()

        # 测试检索现有模板
        existing_scenes = ["竹林决战", "雨夜街斗", "夕阳海边", "欢乐派对"]

        print("测试检索现有模板:")
        for scene in existing_scenes:
            result = generator.generate_prompt_with_timing(
                scene=scene,
                style="写实",
                use_template=True
            )

            used = result.get('used_template', False)
            status = "✓" if used else "✗"
            print(f"{status} '{scene}' -> {'使用模板' if used else '未使用模板'}")

            if not used:
                return False

        return True

    except Exception as e:
        print(f"✗ 模板检索测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 80)
    print("智能扩展系统 - 综合测试")
    print("=" * 80)

    results = {
        "模板库管理": test_template_library(),
        "添加自定义模板": test_add_custom_template(),
        "自动扩展机制": test_auto_expand(),
        "情感检测": test_emotion_detection(),
        "环境检测": test_environment_detection(),
        "模板检索": test_template_retrieval()
    }

    # 打印测试结果总结
    print("\n" + "=" * 80)
    print("测试结果总结")
    print("=" * 80)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")

    print("\n" + "-" * 80)
    print(f"总计: {passed}/{total} 测试通过")

    if passed == total:
        print("✅ 所有测试通过！")
        return True
    else:
        print(f"❌ {total - passed} 个测试失败")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
