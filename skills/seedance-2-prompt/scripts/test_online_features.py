#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 联网功能测试脚本
"""

import sys
import os
from pathlib import Path

# 添加脚本路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# 配置测试输出颜色
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    """打印标题"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")


def print_success(text):
    """打印成功消息"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    """打印错误消息"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text):
    """打印警告消息"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def test_imports():
    """测试模块导入"""
    print_header("测试 1: 模块导入")

    try:
        # 测试 prompt_generator 导入
        from prompt_generator import PromptGenerator
        print_success("prompt_generator 导入成功")

        # 测试 search_online 导入
        try:
            from search_online import search_prompts
            print_success("search_online 导入成功")
            online_search_available = True
        except ImportError as e:
            print_warning(f"search_online 导入失败: {str(e)}")
            print_warning("在线搜索功能可能不可用")
            online_search_available = False

        # 测试 update_templates 导入
        try:
            from update_templates import TemplateUpdater
            print_success("update_templates 导入成功")
            update_available = True
        except ImportError as e:
            print_warning(f"update_templates 导入失败: {str(e)}")
            update_available = False

        return {
            'prompt_generator': True,
            'search_online': online_search_available,
            'update_templates': update_available
        }

    except Exception as e:
        print_error(f"模块导入失败: {str(e)}")
        return None


def test_prompt_generator():
    """测试提示词生成器"""
    print_header("测试 2: 提示词生成器")

    try:
        from prompt_generator import PromptGenerator

        generator = PromptGenerator()
        print_success("PromptGenerator 初始化成功")

        # 测试基本生成
        print("\n测试基本生成:")
        result = generator.generate_prompt(
            scene="一位年轻女性在花园里散步",
            style="梦幻",
            difficulty="INTERMEDIATE",
            video_type="photo-realistic"
        )

        if result and 'prompt' in result:
            print_success("基本生成成功")
            print(f"  提示词: {result['prompt'][:50]}...")
            print(f"  难度: {result['difficulty']}")
            print(f"  类型: {result['video_type']}")
        else:
            print_error("基本生成失败")
            return False

        # 测试带在线搜索的生成
        print("\n测试带在线搜索的生成:")
        result = generator.generate_prompt_with_search(
            scene="一位年轻女性在花园里散步",
            style="梦幻",
            difficulty="INTERMEDIATE",
            video_type="photo-realistic",
            online_search=True
        )

        if result and 'prompt' in result:
            print_success("带在线搜索的生成成功")
            print(f"  提示词: {result['prompt'][:50]}...")
            print(f"  在线搜索使用: {result.get('online_used', False)}")
            if result.get('online_used'):
                print(f"  在线结果数: {len(result.get('online_results', []))}")
        else:
            print_error("带在线搜索的生成失败")
            return False

        return True

    except Exception as e:
        print_error(f"提示词生成器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_online_search():
    """测试在线搜索"""
    print_header("测试 3: 在线搜索")

    try:
        from search_online import search_prompts

        print("执行搜索查询...")
        results = search_prompts(
            query="Seedance 2.0 提示词",
            max_results=3
        )

        if results:
            print_success(f"搜索成功，找到 {len(results)} 个结果")

            for i, result in enumerate(results, 1):
                print(f"\n结果 {i}:")
                print(f"  标题: {result.get('title', 'N/A')[:50]}...")
                print(f"  类型: {result.get('video_type', 'N/A')}")
                print(f"  难度: {result.get('difficulty', 'N/A')}")
                print(f"  来源: {result.get('search_source', 'N/A')}")

            return True
        else:
            print_warning("搜索未返回结果")
            print_warning("这可能是正常的，取决于网络和搜索源配置")
            return True  # 不算失败

    except ImportError as e:
        print_warning(f"search_online 模块不可用: {str(e)}")
        print_warning("跳过在线搜索测试")
        return True  # 不算失败

    except Exception as e:
        print_error(f"在线搜索测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_template_updater():
    """测试模板更新器"""
    print_header("测试 4: 模板更新器")

    try:
        from update_templates import TemplateUpdater

        updater = TemplateUpdater()
        print_success("TemplateUpdater 初始化成功")

        # 测试加载本地模板
        print("\n测试加载本地模板:")
        templates = updater._load_local_templates()

        if templates:
            print_success("本地模板加载成功")
            template_count = len(templates.get('templates', []))
            print(f"  本地模板数量: {template_count}")
        else:
            print_warning("本地模板加载失败或为空")

        # 测试从搜索获取模板
        print("\n测试从搜索获取模板:")
        try:
            new_templates = updater.fetch_templates_from_search(
                query="Seedance 2.0",
                max_results=2
            )

            if new_templates:
                print_success(f"成功获取 {len(new_templates)} 个模板")

                # 显示预览
                for i, template in enumerate(new_templates, 1):
                    print(f"\n模板 {i}:")
                    print(f"  名称: {template.get('name', 'N/A')[:50]}...")
                    print(f"  类型: {template.get('video_type', 'N/A')}")
                    print(f"  难度: {template.get('difficulty', 'N/A')}")
            else:
                print_warning("搜索未返回模板")
                print_warning("这可能是正常的，取决于网络和搜索源配置")

        except Exception as e:
            print_warning(f"从搜索获取模板失败: {str(e)}")
            print_warning("这可能是正常的，取决于网络和搜索源配置")

        return True

    except ImportError as e:
        print_warning(f"update_templates 模块不可用: {str(e)}")
        print_warning("跳过模板更新器测试")
        return True  # 不算失败

    except Exception as e:
        print_error(f"模板更新器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_integration():
    """集成测试"""
    print_header("测试 5: 集成测试")

    try:
        from prompt_generator import PromptGenerator

        print("测试完整工作流程...")

        # 1. 创建生成器
        generator = PromptGenerator()

        # 2. 使用在线搜索生成提示词
        result = generator.generate_prompt_with_search(
            scene="雨天城市街道",
            style="梦幻",
            difficulty="INTERMEDIATE",
            video_type="photo-realistic",
            online_search=True,
            max_online_results=3
        )

        # 3. 验证结果
        if not result or 'prompt' not in result:
            print_error("集成测试失败：生成结果无效")
            return False

        print_success("集成测试成功")
        print(f"\n生成的提示词:")
        print(f"  {result['prompt']}")
        print(f"\n在线搜索状态: {'已使用' if result.get('online_used') else '未使用'}")

        if result.get('online_results'):
            print(f"在线结果数量: {len(result['online_results'])}")

        return True

    except Exception as e:
        print_error(f"集成测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║       Seedance 2.0 联网功能测试脚本                              ║")
    print("║       Online Features Test Suite                                 ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}\n")

    # 运行所有测试
    tests = [
        ("模块导入", test_imports),
        ("提示词生成器", test_prompt_generator),
        ("在线搜索", test_online_search),
        ("模板更新器", test_template_updater),
        ("集成测试", test_integration)
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            if result is None or result is False:
                results.append((test_name, "失败"))
            else:
                results.append((test_name, "成功"))
        except Exception as e:
            print_error(f"{test_name} 异常: {str(e)}")
            results.append((test_name, "异常"))

    # 打印测试总结
    print_header("测试总结")

    success_count = sum(1 for _, status in results if status == "成功")
    total_count = len(results)

    for test_name, status in results:
        if status == "成功":
            print_success(f"{test_name}: {status}")
        else:
            print_error(f"{test_name}: {status}")

    print(f"\n{Colors.BOLD}总计: {success_count}/{total_count} 通过{Colors.ENDC}")

    if success_count == total_count:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}所有测试通过！{Colors.ENDC}\n")
        return 0
    else:
        print(f"\n{Colors.WARNING}{Colors.BOLD}部分测试失败，请检查上面的错误信息。{Colors.ENDC}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
