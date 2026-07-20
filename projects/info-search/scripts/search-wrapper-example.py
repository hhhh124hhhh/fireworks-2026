#!/usr/bin/env python3
"""
search-wrapper 使用示例

演示如何使用统一的搜索包装器
"""

import sys
import json
from pathlib import Path
import importlib.util

# 动态加载 search_wrapper 模块
script_dir = Path(__file__).parent
spec = importlib.util.spec_from_file_location("search_wrapper", script_dir / "search-wrapper.py")
search_wrapper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_wrapper)

# 导入需要的函数
search = search_wrapper.search
search_all_sources = search_wrapper.search_all_sources
print_results = search_wrapper.print_results

def example_basic_search():
    """示例 1: 基本搜索"""
    print("=" * 80)
    print("示例 1: 基本搜索")
    print("=" * 80)

    results = search("Python 编程", max_results=3)

    print(f"\n找到 {len(results)} 个结果:\n")
    for i, result in enumerate(results, 1):
        print(f"[{i}] {result['title']}")
        print(f"    来源: {result['source']}")
        print(f"    URL: {result['url']}")
        print()


def example_fallback_behavior():
    """示例 2: Fallback 行为演示"""
    print("\n" + "=" * 80)
    print("示例 2: Fallback 行为演示")
    print("=" * 80)

    print("\n搜索源顺序: Tavily → SearXNG → Brave")
    print("当第一个搜索源失败时，自动切换到下一个\n")

    results = search("人工智能技术", max_results=2)

    # 查看哪个搜索源提供了结果
    if results and results[0]['source'] != 'error':
        print(f"✓ 成功从 {results[0]['source'].upper()} 获取结果\n")
    else:
        print("✗ 所有搜索源都失败\n")


def example_specific_source():
    """示例 3: 使用特定搜索源"""
    print("\n" + "=" * 80)
    print("示例 3: 使用特定搜索源")
    print("=" * 80)

    # 只使用 SearXNG
    print("\n只使用 SearXNG 搜索:")
    results = search("深度学习", max_results=2, sources=["searxng"])

    print(f"找到 {len(results)} 个结果\n")
    for result in results[:2]:
        print(f"  - {result['title']} ({result['source']})")


def example_all_sources():
    """示例 4: 尝试所有搜索源"""
    print("\n" + "=" * 80)
    print("示例 4: 尝试所有搜索源")
    print("=" * 80)

    print("\n同时尝试所有搜索源:\n")
    all_results = search_all_sources("自然语言处理", max_results=2)

    for source, results in all_results.items():
        if results:
            print(f"✓ {source.upper()}: {len(results)} 个结果")
            for r in results[:1]:
                print(f"    - {r['title'][:50]}...")
        else:
            print(f"✗ {source.upper()}: 失败")
    print()


def example_error_handling():
    """示例 5: 错误处理"""
    print("\n" + "=" * 80)
    print("示例 5: 错误处理")
    print("=" * 80)

    print("\n尝试无效的搜索（空查询）:\n")
    results = search("", max_results=5)

    if results and results[0]['source'] == 'error':
        print("捕获到错误:")
        print(f"  {results[0]['content'][:100]}...")
    else:
        print("未捕获到错误")


def example_result_format():
    """示例 6: 结果格式说明"""
    print("\n" + "=" * 80)
    print("示例 6: 结果格式说明")
    print("=" * 80)

    results = search("大数据", max_results=1)

    if results and results[0]['source'] != 'error':
        result = results[0]
        print("\n搜索结果格式:")
        print(f"  title:     {result['title']}")
        print(f"  url:       {result['url']}")
        print(f"  content:   {result['content'][:100]}...")
        print(f"  source:    {result['source']}")
        print(f"  timestamp: {result['timestamp']}")


def example_api_usage():
    """示例 7: 在代码中使用 API"""
    print("\n" + "=" * 80)
    print("示例 7: 在代码中使用 API")
    print("=" * 80)

    print("""
from search_wrapper import search

# 基本使用
results = search("关键词", max_results=10)

# 处理结果
for result in results:
    print(f"{result['title']}: {result['url']}")

# 指定搜索源
results = search("关键词", sources=["tavily"])

# 尝试所有搜索源
from search_wrapper import search_all_sources
all_results = search_all_sources("关键词")

for source, results in all_results.items():
    print(f"{source}: {len(results)} 个结果")
""")


def main():
    """运行所有示例"""
    print("\n" + "=" * 80)
    print("Search Wrapper 使用示例")
    print("=" * 80)

    try:
        example_basic_search()
        example_fallback_behavior()
        example_specific_source()
        example_all_sources()
        example_error_handling()
        example_result_format()
        example_api_usage()

        print("\n" + "=" * 80)
        print("所有示例运行完成！")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ 运行示例时出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
