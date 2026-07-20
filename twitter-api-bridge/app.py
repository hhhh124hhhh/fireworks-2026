#!/usr/bin/env python3
"""
Twitter API Bridge - 使用 Nitter 镜像站替代官方 Twitter API
无需 API Key，完全免费的替代方案
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from ntscraper import Nitter
import logging
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 健康状态和统计信息
health_status = {
    "start_time": datetime.now().isoformat(),
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "last_check": None,
    "last_successful_scrape": None,
    "working_instances": [],
    "failed_instances": []
}

# Nitter 实例列表（更新的、更可靠的实例）
NITTER_INSTANCES = [
    # 主要实例
    "https://xcancel.com",
    "https://lightbrd.com",

    # 备用实例（可能不稳定）
    "https://nitter.poast.org",
    "https://nitter.privacyredirect.com",
    "https://nitter.space",

    # 更多备用实例
    "https://nitter.fdn.fr",
    "https://nitter.1d4.us",
    "https://nitter.mint.lgbt",
    "https://nitter.namazso.eu",
    "https://nitter.kavin.rocks",
]


class TwitterScraper:
    """Twitter/X 抓取器 - 使用 Nitter 镜像站"""

    def __init__(self):
        # 跳过实例检查，手动管理实例
        self.scraper = Nitter(skip_instance_check=True)
        self.available_instances = NITTER_INSTANCES.copy()
        self.working_instances = []
        self.failed_instances = {}

    def _try_scrape(self, func_name: str, *args, **kwargs) -> Dict:
        """尝试抓取，自动重试不同的 Nitter 实例"""
        last_error = None
        attempted_instances = []

        for instance in self.available_instances:
            try:
                attempted_instances.append(instance)
                logger.info(f"尝试使用实例: {instance}")

                # 执行抓取
                result = getattr(self.scraper, func_name)(*args, **kwargs, instance=instance)

                # 检查结果
                if result and 'tweets' in result and len(result['tweets']) > 0:
                    # 成功！更新工作实例列表
                    if instance not in self.working_instances:
                        self.working_instances.insert(0, instance)
                        health_status["working_instances"] = self.working_instances[:5]
                    if instance in self.failed_instances:
                        del self.failed_instances[instance]
                        health_status["failed_instances"] = list(self.failed_instances.keys())

                    logger.info(f"✓ 成功！使用实例: {instance}")
                    return {"success": True, "data": result, "instance": instance}
                else:
                    # 返回了空结果
                    last_error = f"空结果（从 {instance}）"
                    logger.warning(f"实例 {instance} 返回空结果")

            except Exception as e:
                last_error = str(e)
                logger.warning(f"实例 {instance} 失败: {e}")

                # 记录失败的实例
                if instance not in self.failed_instances:
                    self.failed_instances[instance] = {
                        "error": last_error,
                        "timestamp": datetime.now().isoformat()
                    }
                    health_status["failed_instances"] = list(self.failed_instances.keys())

            # 如果该实例在工作列表中，移到末尾或移除
            if instance in self.working_instances:
                self.working_instances.remove(instance)

        # 所有实例都失败了，返回部分结果（如果有的话）
        # 尝试最后一次，不指定实例，让 ntscraper 自己选择
        try:
            logger.info("所有指定实例失败，尝试让 ntscraper 自动选择...")
            result = getattr(self.scraper, func_name)(*args, **kwargs)
            if result and 'tweets' in result and len(result['tweets']) > 0:
                return {"success": True, "data": result, "instance": "auto"}
        except Exception as e:
            logger.error(f"自动选择失败: {e}")

        # 彻底失败
        return {
            "success": False,
            "error": last_error or "无法从任何实例获取数据",
            "attempted_instances": attempted_instances,
            "working_instances": self.working_instances
        }

    def get_tweets(self, username: str, mode: str = "user", num: int = 20) -> Dict:
        """获取用户的推文

        Args:
            username: 用户名（不带 @）
            mode: 模式 - 'user' (用户推文), 'faves' (点赞), 'media' (媒体), 'replies' (回复)
            num: 获取推文数量

        Returns:
            Dict: 包含成功状态、数据和使用的实例
        """
        logger.info(f"抓取 @{username} 的推文 (模式: {mode}, 数量: {num})")
        return self._try_scrape("get_tweets", username, mode, num)

    def search_tweets(self, term: str, mode: str = "term", num: int = 20) -> Dict:
        """搜索推文

        Args:
            term: 搜索关键词
            mode: 模式 - 'term' (关键词), 'hashtag' (标签), 'user' (用户)
            num: 获取推文数量

        Returns:
            Dict: 包含成功状态、数据和使用的实例
        """
        logger.info(f"搜索推文: {term} (模式: {mode}, 数量: {num})")
        return self._try_scrape("get_tweets", term, mode, num)

    def get_profile_info(self, username: str) -> Dict:
        """获取用户资料信息"""
        logger.info(f"获取用户资料: @{username}")
        try:
            result = self.scraper.get_profile_info(username)
            if result:
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "无法获取用户资料"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# 初始化抓取器
twitter_scraper = TwitterScraper()


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "uptime": str(datetime.now() - datetime.fromisoformat(health_status["start_time"])),
        "statistics": {
            "total_requests": health_status["total_requests"],
            "successful_requests": health_status["successful_requests"],
            "failed_requests": health_status["failed_requests"],
            "success_rate": f"{(health_status['successful_requests'] / max(health_status['total_requests'], 1) * 100):.2f}%"
        },
        "instances": {
            "working": health_status["working_instances"],
            "failed": health_status["failed_instances"]
        },
        "last_check": health_status["last_check"],
        "last_successful_scrape": health_status["last_successful_scrape"]
    })


@app.route('/api/user/<username>', methods=['GET'])
def get_user_tweets(username):
    """获取用户推文"""
    health_status["total_requests"] += 1

    # 获取参数
    mode = request.args.get('mode', 'user')  # user, faves, media, replies
    num = int(request.args.get('num', 20))

    # 执行抓取
    result = twitter_scraper.get_tweets(username, mode, num)

    if result["success"]:
        health_status["successful_requests"] += 1
        health_status["last_successful_scrape"] = datetime.now().isoformat()
        return jsonify({
            "success": True,
            "username": username,
            "mode": mode,
            "count": len(result["data"]["tweets"]) if "tweets" in result["data"] else 0,
            "data": result["data"],
            "instance": result["instance"]
        })
    else:
        health_status["failed_requests"] += 1
        return jsonify({
            "success": False,
            "error": result.get("error", "Unknown error"),
            "working_instances": result.get("working_instances", []),
            "attempted_instances": result.get("attempted_instances", [])
        }), 500


@app.route('/api/profile/<username>', methods=['GET'])
def get_user_profile(username):
    """获取用户资料"""
    health_status["total_requests"] += 1

    # 执行抓取
    result = twitter_scraper.get_profile_info(username)

    if result["success"]:
        health_status["successful_requests"] += 1
        health_status["last_successful_scrape"] = datetime.now().isoformat()
        return jsonify(result)
    else:
        health_status["failed_requests"] += 1
        return jsonify(result), 500


@app.route('/api/search', methods=['GET'])
def search_tweets():
    """搜索推文"""
    health_status["total_requests"] += 1

    # 获取参数
    term = request.args.get('q')
    if not term:
        return jsonify({"success": False, "error": "Missing query parameter 'q'"}), 400

    mode = request.args.get('mode', 'term')  # term, hashtag, user
    num = int(request.args.get('num', 20))

    # 执行搜索
    result = twitter_scraper.search_tweets(term, mode, num)

    if result["success"]:
        health_status["successful_requests"] += 1
        health_status["last_successful_scrape"] = datetime.now().isoformat()
        return jsonify({
            "success": True,
            "query": term,
            "mode": mode,
            "count": len(result["data"]["tweets"]) if "tweets" in result["data"] else 0,
            "data": result["data"],
            "instance": result["instance"]
        })
    else:
        health_status["failed_requests"] += 1
        return jsonify({
            "success": False,
            "error": result.get("error", "Unknown error"),
            "working_instances": result.get("working_instances", []),
            "attempted_instances": result.get("attempted_instances", [])
        }), 500


@app.route('/api/self-check', methods=['POST'])
def run_self_check():
    """执行自我检查 - 测试抓取功能是否正常"""
    logger.info("开始自我检查...")

    # 测试用例
    test_cases = [
        {"type": "user", "username": "OpenAI", "mode": "user", "num": 5},
        {"type": "search", "term": "AI", "mode": "term", "num": 5}
    ]

    results = {
        "check_time": datetime.now().isoformat(),
        "status": "running",
        "tests": [],
        "summary": {"total": 0, "passed": 0, "failed": 0}
    }

    health_status["last_check"] = datetime.now().isoformat()

    # 运行测试
    for test in test_cases:
        test_name = test.get('username', test.get('term', 'unknown'))
        test_result = {
            "name": f"Test: {test_name}",
            "status": "pending",
            "error": None,
            "instance": None
        }
        results["summary"]["total"] += 1

        try:
            if test["type"] == "user":
                result = twitter_scraper.get_tweets(test["username"], test["mode"], test["num"])
            else:
                result = twitter_scraper.search_tweets(test["term"], test["mode"], test["num"])

            if result["success"]:
                test_result["status"] = "passed"
                test_result["instance"] = result["instance"]
                results["summary"]["passed"] += 1
                logger.info(f"✓ {test_result['name']} - 通过 (实例: {result['instance']})")
            else:
                test_result["status"] = "failed"
                test_result["error"] = result.get("error", "Unknown error")
                results["summary"]["failed"] += 1
                logger.error(f"✗ {test_result['name']} - 失败: {test_result['error']}")

        except Exception as e:
            test_result["status"] = "failed"
            test_result["error"] = str(e)
            results["summary"]["failed"] += 1
            logger.error(f"✗ {test_result['name']} - 异常: {e}")

        results["tests"].append(test_result)

    # 判断整体状态
    results["status"] = "healthy" if results["summary"]["passed"] > 0 else "unhealthy"

    logger.info(f"自我检查完成: {results['summary']['passed']}/{results['summary']['total']} 通过")

    return jsonify(results)


@app.route('/', methods=['GET'])
def index():
    """主页 - API 文档"""
    return jsonify({
        "name": "Twitter API Bridge",
        "version": "1.0.0",
        "description": "使用 Nitter 镜像站的免费 Twitter/X API 替代方案",
        "warning": "Nitter 实例可能不稳定，如果所有实例都失效，需要更新实例列表",
        "endpoints": {
            "GET /health": "健康检查和统计信息",
            "GET /api/user/<username>": "获取用户推文 (参数: mode=user|faves|media|replies, num=数量)",
            "GET /api/profile/<username>": "获取用户资料",
            "GET /api/search?q=关键词": "搜索推文 (参数: mode=term|hashtag|user, num=数量)",
            "POST /api/self-check": "执行自我检查"
        },
        "features": [
            "无需官方 Twitter API Key",
            "使用 Nitter 公开镜像站",
            "自动重试和实例切换",
            "自我健康检查",
            "完整的错误处理"
        ],
        "note": "如果抓取失败，可能是 Nitter 实例失效。请检查 /health 端点查看可用实例。"
    })


if __name__ == '__main__':
    logger.info("="*60)
    logger.info("Twitter API Bridge 启动中...")
    logger.info(f"监听地址: http://0.0.0.0:5000")
    logger.info(f"配置的 Nitter 实例: {len(NITTER_INSTANCES)} 个")
    logger.info("="*60)

    # 启动时不执行自我检查（因为可能需要时间）
    logger.info("服务已启动，访问 /api/self-check 运行自我检查")

    app.run(host='0.0.0.0', port=5000, debug=False)
