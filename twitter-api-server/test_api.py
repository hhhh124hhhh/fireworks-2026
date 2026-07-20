"""
测试脚本 - 测试私有 Twitter API
"""

import requests
import json

# API 基础 URL
BASE_URL = "http://localhost:8000"

def print_json(data):
    """美化打印 JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def test_health():
    """测试健康检查"""
    print("\n🏥 测试健康检查...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"状态码: {response.status_code}")
    print_json(response.json())


def test_search_tweets():
    """测试搜索推文"""
    print("\n🔍 测试搜索推文...")
    response = requests.get(
        f"{BASE_URL}/api/tweets/search",
        params={"term": "AI prompt", "number": 5}
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        tweets = response.json()
        print(f"找到 {len(tweets)} 条推文")
        if tweets:
            print("第一条推文:")
            print_json(tweets[0])
    else:
        print_json(response.json())


def test_get_user_tweets():
    """测试获取用户推文"""
    print("\n👤 测试获取用户推文...")
    response = requests.get(
        f"{BASE_URL}/api/tweets/user/openai",
        params={"number": 3}
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        tweets = response.json()
        print(f"找到 {len(tweets)} 条推文")
        if tweets:
            print("第一条推文:")
            print_json(tweets[0])
    else:
        print_json(response.json())


def test_get_user_profile():
    """测试获取用户资料"""
    print("\n📋 测试获取用户资料...")
    response = requests.get(f"{BASE_URL}/api/user/openai")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print_json(response.json())
    else:
        print_json(response.json())


def test_search_hashtag():
    """测试搜索话题标签"""
    print("\n#️⃣ 测试搜索话题标签...")
    response = requests.get(
        f"{BASE_URL}/api/tweets/search",
        params={"term": "ChatGPT", "mode": "hashtag", "number": 5}
    )
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        tweets = response.json()
        print(f"找到 {len(tweets)} 条推文")
        if tweets:
            print("第一条推文:")
            print_json(tweets[0])
    else:
        print_json(response.json())


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 私有 Twitter API 测试")
    print("=" * 50)

    try:
        test_health()
        test_search_tweets()
        test_get_user_tweets()
        test_get_user_profile()
        test_search_hashtag()

        print("\n" + "=" * 50)
        print("✅ 所有测试完成!")
        print("=" * 50)

        print(f"\n📚 API 文档: {BASE_URL}/docs")
        print(f"📚 Swagger UI: {BASE_URL}/docs")
        print(f"📚 ReDoc: {BASE_URL}/redoc")

    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器，请先启动服务器:")
        print("   ./start.sh")
        print("   或")
        print("   python3 main.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
