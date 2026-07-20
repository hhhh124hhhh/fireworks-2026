#!/usr/bin/env python3
"""
Twitter API Bridge - Playwright 版本
使用浏览器模拟抓取 Twitter/X 数据
不需要 API Key，但需要 Twitter 账号登录
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import logging
import time
import json
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

# 健康状态
health_status = {
    "start_time": datetime.now().isoformat(),
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "is_logged_in": False,
    "browser_status": "stopped"
}

class TwitterPlaywrightScraper:
    """使用 Playwright 的 Twitter 抓取器"""

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.is_logged_in = False

    def start_browser(self):
        """启动浏览器"""
        if self.browser is None:
            logger.info("启动浏览器...")
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=False,  # 首次登录时设为 False 以便手动登录
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self.context = self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            self.page = self.context.new_page()
            health_status["browser_status"] = "running"
            logger.info("浏览器已启动")
            return True
        return True

    def check_login(self) -> bool:
        """检查是否已登录"""
        try:
            self.page.goto('https://twitter.com/home', timeout=10000)
            # 检查是否已登录（查看页面是否有登录按钮）
            login_button = self.page.query_selector('a[href="/login"]')
            if login_button:
                logger.warning("未登录，需要手动登录")
                self.is_logged_in = False
                health_status["is_logged_in"] = False
                return False

            self.is_logged_in = True
            health_status["is_logged_in"] = True
            logger.info("已登录 Twitter")
            return True
        except Exception as e:
            logger.error(f"检查登录状态失败: {e}")
            return False

    def manual_login(self):
        """手动登录（会打开浏览器窗口）"""
        logger.info("打开浏览器进行手动登录...")
        self.start_browser()
        self.page.goto('https://twitter.com/i/flow/login', timeout=30000)
        logger.info("请在浏览器中完成登录...")
        logger.info("登录完成后，API 将自动检测登录状态")

    def get_user_tweets(self, username: str, num: int = 20) -> Dict:
        """获取用户推文"""
        logger.info(f"抓取 @{username} 的推文...")

        if not self.is_logged_in:
            return {"success": False, "error": "未登录 Twitter"}

        try:
            # 访问用户主页
            url = f'https://twitter.com/{username}'
            self.page.goto(url, timeout=30000)
            time.sleep(3)  # 等待页面加载

            # 等待推文加载
            self.page.wait_for_selector('[data-testid="tweet"]', timeout=10000)

            # 滚动加载更多推文
            tweets = []
            last_height = 0
            scroll_attempts = 0
            max_scrolls = 10  # 限制滚动次数

            while len(tweets) < num and scroll_attempts < max_scrolls:
                # 获取当前可见的推文
                tweet_elements = self.page.query_all('[data-testid="tweet"]')

                for element in tweet_elements:
                    try:
                        tweet_text = element.query_selector('[data-testid="tweetText"]')
                        if tweet_text:
                            text = tweet_text.inner_text().strip()

                            # 避免重复
                            if text not in [t['text'] for t in tweets]:
                                tweets.append({
                                    "text": text,
                                    "user": {
                                        "username": username,
                                        "name": username
                                    },
                                    "stats": {
                                        "comments": 0,
                                        "retweets": 0,
                                        "likes": 0
                                    },
                                    "date": datetime.now().strftime('%Y-%m-%d')
                                })

                                if len(tweets) >= num:
                                    break
                    except Exception as e:
                        logger.warning(f"解析推文失败: {e}")
                        continue

                if len(tweets) >= num:
                    break

                # 滚动到底部
                scroll_height = self.page.evaluate('document.body.scrollHeight')
                self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(2)

                if scroll_height == last_height:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0
                    last_height = scroll_height

            logger.info(f"成功获取 {len(tweets)} 条推文")
            return {
                "success": True,
                "data": {
                    "tweets": tweets
                },
                "count": len(tweets)
            }

        except PlaywrightTimeoutError:
            return {"success": False, "error": "加载超时"}
        except Exception as e:
            logger.error(f"抓取失败: {e}")
            return {"success": False, "error": str(e)}

    def search_tweets(self, term: str, num: int = 20) -> Dict:
        """搜索推文"""
        logger.info(f"搜索推文: {term}")

        if not self.is_logged_in:
            return {"success": False, "error": "未登录 Twitter"}

        try:
            # 访问搜索页面
            url = f'https://twitter.com/search?q={term}'
            self.page.goto(url, timeout=30000)
            time.sleep(3)

            # 等待推文加载
            self.page.wait_for_selector('[data-testid="tweet"]', timeout=10000)

            # 获取推文
            tweets = []
            tweet_elements = self.page.query_all('[data-testid="tweet"]')

            for element in tweet_elements[:num]:
                try:
                    tweet_text = element.query_selector('[data-testid="tweetText"]')
                    user_element = element.query_selector('[data-testid="User-Name"] a')

                    if tweet_text:
                        text = tweet_text.inner_text().strip()
                        username = user_element.inner_text().strip() if user_element else "unknown"

                        tweets.append({
                            "text": text,
                            "user": {
                                "username": username,
                                "name": username
                            },
                            "stats": {
                                "comments": 0,
                                "retweets": 0,
                                "likes": 0
                            },
                            "date": datetime.now().strftime('%Y-%m-%d')
                        })
                except Exception as e:
                    logger.warning(f"解析推文失败: {e}")
                    continue

            logger.info(f"成功获取 {len(tweets)} 条搜索结果")
            return {
                "success": True,
                "data": {
                    "tweets": tweets
                },
                "count": len(tweets)
            }

        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return {"success": False, "error": str(e)}

    def stop_browser(self):
        """关闭浏览器"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
            self.playwright.stop()
        self.browser = None
        health_status["browser_status"] = "stopped"
        logger.info("浏览器已关闭")


# 初始化抓取器
scraper = TwitterPlaywrightScraper()


@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "uptime": str(datetime.now() - datetime.fromisoformat(health_status["start_time"])),
        "statistics": {
            "total_requests": health_status["total_requests"],
            "successful_requests": health_status["successful_requests"],
            "failed_requests": health_status["failed_requests"],
            "success_rate": f"{(health_status['successful_requests'] / max(health_status['total_requests'], 1) * 100):.2f}%"
        },
        "twitter": {
            "is_logged_in": health_status["is_logged_in"],
            "browser_status": health_status["browser_status"]
        }
    })


@app.route('/api/login', methods=['POST'])
def manual_login():
    """启动手动登录"""
    try:
        scraper.manual_login()
        return jsonify({
            "success": True,
            "message": "浏览器已打开，请在浏览器中完成登录。登录完成后，访问 /api/check-login 检查状态。"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/check-login', methods=['GET'])
def check_login():
    """检查登录状态"""
    try:
        is_logged_in = scraper.check_login()
        return jsonify({
            "success": True,
            "is_logged_in": is_logged_in,
            "message": "已登录" if is_logged_in else "未登录，请调用 /api/login 进行登录"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/user/<username>', methods=['GET'])
def get_user_tweets(username):
    """获取用户推文"""
    health_status["total_requests"] += 1

    num = int(request.args.get('num', 20))
    result = scraper.get_user_tweets(username, num)

    if result["success"]:
        health_status["successful_requests"] += 1
        return jsonify({
            "success": True,
            "username": username,
            "count": result["count"],
            "data": result["data"]
        })
    else:
        health_status["failed_requests"] += 1
        return jsonify(result), 500


@app.route('/api/search', methods=['GET'])
def search_tweets():
    """搜索推文"""
    health_status["total_requests"] += 1

    term = request.args.get('q')
    if not term:
        return jsonify({"success": False, "error": "Missing query parameter 'q'"}), 400

    num = int(request.args.get('num', 20))
    result = scraper.search_tweets(term, num)

    if result["success"]:
        health_status["successful_requests"] += 1
        return jsonify({
            "success": True,
            "query": term,
            "count": result["count"],
            "data": result["data"]
        })
    else:
        health_status["failed_requests"] += 1
        return jsonify(result), 500


@app.route('/', methods=['GET'])
def index():
    """主页"""
    return jsonify({
        "name": "Twitter API Bridge (Playwright)",
        "version": "2.0.0",
        "description": "使用 Playwright 的 Twitter/X 抓取 API",
        "note": "需要 Twitter 账号登录才能使用",
        "endpoints": {
            "GET /health": "健康检查",
            "POST /api/login": "启动浏览器进行手动登录",
            "GET /api/check-login": "检查登录状态",
            "GET /api/user/<username>": "获取用户推文",
            "GET /api/search?q=关键词": "搜索推文"
        },
        "usage": [
            "1. 首次使用: POST /api/login 打开浏览器",
            "2. 在浏览器中完成 Twitter 登录",
            "3. GET /api/check-login 确认登录状态",
            "4. 开始使用 API 抓取数据"
        ]
    })


if __name__ == '__main__':
    logger.info("="*60)
    logger.info("Twitter API Bridge (Playwright) 启动中...")
    logger.info(f"监听地址: http://0.0.0.0:5000")
    logger.info("="*60)

    # 启动浏览器（但保持 headless=True）
    scraper.start_browser()

    app.run(host='0.0.0.0', port=5000, debug=False)
