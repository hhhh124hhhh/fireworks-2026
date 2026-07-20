#!/usr/bin/env python3
"""
自动检查循环 - 定期检查 Twitter API Bridge 的健康状态
"""

import requests
import time
import logging
from datetime import datetime

# 配置
API_URL = "http://localhost:5000"
CHECK_INTERVAL = 300  # 5分钟检查一次
HEALTH_ENDPOINT = f"{API_URL}/health"
SELF_CHECK_ENDPOINT = f"{API_URL}/api/self-check"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_health():
    """检查服务健康状态"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=10)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✓ 服务健康 - 成功率: {data['statistics']['success_rate']}")
            return True
        else:
            logger.error(f"✗ 健康检查失败 - HTTP {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"✗ 无法连接到服务: {e}")
        return False


def run_self_check():
    """运行自我检查"""
    try:
        logger.info("执行自我检查...")
        response = requests.post(SELF_CHECK_ENDPOINT, timeout=60)

        if response.status_code == 200:
            data = response.json()
            summary = data['summary']
            logger.info(f"自我检查完成: {summary['passed']}/{summary['total']} 通过")
            logger.info(f"状态: {data['status']}")

            # 显示失败的测试
            if summary['failed'] > 0:
                logger.warning("失败的测试:")
                for test in data['tests']:
                    if test['status'] == 'failed':
                        logger.warning(f"  - {test['name']}: {test['error']}")

            return data['status'] == 'healthy'
        else:
            logger.error(f"✗ 自我检查失败 - HTTP {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"✗ 自我检查异常: {e}")
        return False


def main():
    """主循环"""
    logger.info("="*60)
    logger.info("Twitter API Bridge - 自动检查守护进程")
    logger.info(f"检查间隔: {CHECK_INTERVAL} 秒 ({CHECK_INTERVAL/60:.1f} 分钟)")
    logger.info("="*60)

    while True:
        try:
            # 检查健康状态
            if not check_health():
                logger.warning("服务不健康，尝试自我检查...")
                run_self_check()
            else:
                # 定期运行自我检查
                run_self_check()

            logger.info(f"下次检查: {CHECK_INTERVAL} 秒后...")
            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            logger.info("\n收到中断信号，退出...")
            break
        except Exception as e:
            logger.error(f"主循环异常: {e}")
            time.sleep(30)  # 出错后等待30秒再重试


if __name__ == "__main__":
    main()
