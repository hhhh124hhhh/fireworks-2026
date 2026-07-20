#!/usr/bin/env python3
"""
测试脚本 - 测试 Twitter API Bridge 的所有功能
"""

import requests
import json
import sys
from datetime import datetime

API_URL = "http://localhost:5000"


def print_section(title):
    """打印分隔线"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_health():
    """测试健康检查"""
    print_section("1. 健康检查")

    try:
        response = requests.get(f"{API_URL}/health")
        data = response.json()

        print(f"✓ 状态: {data['status']}")
        print(f"  运行时间: {data['uptime']}")
        print(f"  总请求数: {data['statistics']['total_requests']}")
        print(f"  成功数: {data['statistics']['successful_requests']}")
        print(f"  失败数: {data['statistics']['failed_requests']}")
        print(f"  成功率: {data['statistics']['success_rate']}")
        print(f"  工作实例: {len(data['instances']['working'])} 个")
        print(f"  失败实例: {len(data['instances']['failed'])} 个")

        return response.status_code == 200

    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


def test_user_tweets():
    """测试获取用户推文"""
    print_section("2. 获取用户推文 (@OpenAI)")

    try:
        response = requests.get(f"{API_URL}/api/user/OpenAI?num=5")
        data = response.json()

        if data['success']:
            print(f"✓ 成功获取 {data['count']} 条推文")
            print(f"  使用的实例: {data['instance']}")

            if data['count'] > 0:
                tweet = data['data']['tweets'][0]
                print(f"\n  示例推文:")
                print(f"  - 日期: {tweet['date']}")
                print(f"  - 内容: {tweet['text'][:100]}...")
                print(f"  - 统计: 💬 {tweet['stats']['comments']} | 🔄 {tweet['stats']['retweets']} | ❤️ {tweet['stats']['likes']}")

            return True
        else:
            print(f"✗ 失败: {data['error']}")
            return False

    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


def test_search():
    """测试搜索推文"""
    print_section("3. 搜索推文 (关键词: AI)")

    try:
        response = requests.get(f"{API_URL}/api/search?q=AI&num=5")
        data = response.json()

        if data['success']:
            print(f"✓ 成功获取 {data['count']} 条推文")
            print(f"  使用的实例: {data['instance']}")

            if data['count'] > 0:
                tweet = data['data']['tweets'][0]
                print(f"\n  示例推文:")
                print(f"  - 用户: {tweet['user']['name']} (@{tweet['user']['username']})")
                print(f"  - 内容: {tweet['text'][:100]}...")

            return True
        else:
            print(f"✗ 失败: {data['error']}")
            return False

    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


def test_self_check():
    """测试自我检查"""
    print_section("4. 自我检查")

    try:
        response = requests.post(f"{API_URL}/api/self-check")
        data = response.json()

        print(f"✓ 检查时间: {data['check_time']}")
        print(f"  整体状态: {data['status']}")
        print(f"  测试结果: {data['summary']['passed']}/{data['summary']['total']} 通过")

        if data['summary']['failed'] > 0:
            print(f"\n  失败的测试:")
            for test in data['tests']:
                if test['status'] == 'failed':
                    print(f"    ✗ {test['name']}: {test['error']}")

        return data['status'] == 'healthy'

    except Exception as e:
        print(f"✗ 错误: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("  Twitter API Bridge - 功能测试")
    print("="*60)
    print(f"  测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  API 地址: {API_URL}")
    print("="*60)

    results = []

    # 运行所有测试
    results.append(("健康检查", test_health()))
    results.append(("获取用户推文", test_user_tweets()))
    results.append(("搜索推文", test_search()))
    results.append(("自我检查", test_self_check()))

    # 总结
    print_section("测试总结")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {name}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常。")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查日志。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
