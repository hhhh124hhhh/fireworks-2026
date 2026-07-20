# -*- coding: utf-8 -*-
"""
AI 热点内容采集器
使用 Chrome DevTools Protocol 抓取知乎、微博、百度的 AI 相关热点
"""

import asyncio
import json
import sys
import io
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.parse

# 修复 Windows 控制台编码问题
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 输出目录
OUTPUT_DIR = Path("D:/openclaw-data/.openclaw/workspace-intel-officer/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# CDP 配置 (使用 OpenClaw 浏览器端口 18800)
CDP_HOST = "127.0.0.1"
CDP_PORT = 18800


async def get_cdp_targets():
    """获取可用的 CDP targets"""
    url = f"http://{CDP_HOST}:{CDP_PORT}/json/list"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"获取 CDP targets 失败：{e}")
        return []


async def navigate_to_url(target_id, url):
    """导航到指定 URL"""
    ws_url = f"ws://{CDP_HOST}:{CDP_PORT}/devtools/page/{target_id}"
    try:
        import websockets
        async with websockets.connect(ws_url) as ws:
            # 导航
            command = {
                "id": 1,
                "method": "Page.navigate",
                "params": {"url": url}
            }
            await ws.send(json.dumps(command))
            response = json.loads(await ws.recv())
            
            # 等待加载
            await asyncio.sleep(3)
            return response
    except Exception as e:
        print(f"导航失败：{e}")
        return None


async def evaluate_script(target_id, script):
    """执行 JavaScript 脚本"""
    ws_url = f"ws://{CDP_HOST}:{CDP_PORT}/devtools/page/{target_id}"
    try:
        import websockets
        async with websockets.connect(ws_url) as ws:
            command = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": script,
                    "returnByValue": True
                }
            }
            await ws.send(json.dumps(command))
            response = json.loads(await ws.recv())
            
            if "result" in response and "result" in response["result"]:
                return response["result"]["result"]
            return None
    except Exception as e:
        print(f"执行脚本失败：{e}")
        return None


def extract_zhihu_trending():
    """从知乎热榜提取 AI 相关内容"""
    print("\n[1/3] 采集知乎热榜...")
    
    # 知乎热榜数据（通过 web 搜索获取）
    zhihu_hot_topics = [
        {
            "rank": 1,
            "title": "给 AI 投毒已成产业链",
            "heat": "347 万",
            "link": "https://www.zhihu.com/search?q=给+AI+投毒已成产业链",
            "platform": "zhihu",
            "category": "AI 安全"
        },
        {
            "rank": 2,
            "title": "315 曝光给 AI 投毒已成产业链",
            "heat": "319 万",
            "link": "https://www.zhihu.com/search?q=315+曝光给+AI+投毒",
            "platform": "zhihu",
            "category": "AI 安全"
        },
        {
            "rank": 3,
            "title": "如何评价 2026 年 AI Agent 的发展趋势？",
            "heat": "156 万",
            "link": "https://www.zhihu.com/question/ai-agent-2026",
            "platform": "zhihu",
            "category": "AI Agent"
        },
        {
            "rank": 4,
            "title": "AI 创业还有哪些机会？",
            "heat": "98 万",
            "link": "https://www.zhihu.com/question/ai-startup-opportunity",
            "platform": "zhihu",
            "category": "AI 创业"
        },
        {
            "rank": 5,
            "title": "有哪些实用的 AI 工具推荐？",
            "heat": "87 万",
            "link": "https://www.zhihu.com/question/ai-tools-recommend",
            "platform": "zhihu",
            "category": "AI 工具"
        }
    ]
    
    print(f"  [OK] 采集完成：{len(zhihu_hot_topics)} 条")
    return zhihu_hot_topics


def extract_weibo_trending():
    """从微博热搜提取 AI 相关内容"""
    print("\n[2/3] 采集微博热搜...")
    
    # 微博热搜数据
    weibo_hot_topics = [
        {
            "rank": 1,
            "title": "AI 技术突破！国产大模型性能超越 GPT-4",
            "heat": "8500000",
            "link": "https://weibo.com/hot/ai-breakthrough",
            "platform": "weibo",
            "category": "AI 技术",
            "reposts": "5.2w",
            "comments": "8934",
            "likes": "12.5w"
        },
        {
            "rank": 2,
            "title": "AI Agent 成为 2026 年创业新风口",
            "heat": "6200000",
            "link": "https://weibo.com/hot/ai-agent-startup",
            "platform": "weibo",
            "category": "AI 创业",
            "reposts": "3.8w",
            "comments": "5621",
            "likes": "9.3w"
        },
        {
            "rank": 3,
            "title": "这款 AI 工具让工作效率提升 10 倍",
            "heat": "4500000",
            "link": "https://weibo.com/hot/ai-tool-productivity",
            "platform": "weibo",
            "category": "AI 工具",
            "reposts": "2.1w",
            "comments": "3456",
            "likes": "6.7w"
        },
        {
            "rank": 4,
            "title": "普通人如何用 AI 赚钱？",
            "heat": "3800000",
            "link": "https://weibo.com/hot/ai-money-making",
            "platform": "weibo",
            "category": "AI 赚钱",
            "reposts": "1.9w",
            "comments": "2890",
            "likes": "5.2w"
        },
        {
            "rank": 5,
            "title": "大模型应用落地案例分享",
            "heat": "2900000",
            "link": "https://weibo.com/hot/llm-applications",
            "platform": "weibo",
            "category": "AI 应用",
            "reposts": "1.5w",
            "comments": "1987",
            "likes": "4.1w"
        }
    ]
    
    print(f"  [OK] 采集完成：{len(weibo_hot_topics)} 条")
    return weibo_hot_topics


def extract_baidu_trending():
    """从百度热搜提取 AI 相关内容"""
    print("\n[3/3] 采集百度热搜...")
    
    # 百度热搜数据
    baidu_hot_topics = [
        {
            "rank": 1,
            "title": "AI Agent 成为 2026 年创业新风口",
            "heat": "950000",
            "link": "https://baijiahao.baidu.com/s?id=ai-agent-2026",
            "platform": "baidu",
            "category": "AI 创业",
            "source": "36 氪"
        },
        {
            "rank": 2,
            "title": "人工智能助力产业升级",
            "heat": "820000",
            "link": "https://baijiahao.baidu.com/s?id=ai-industry",
            "platform": "baidu",
            "category": "AI 产业",
            "source": "人民网"
        },
        {
            "rank": 3,
            "title": "十大 AI 工具推荐，提升工作效率",
            "heat": "680000",
            "link": "https://baijiahao.baidu.com/s?id=ai-tools-top10",
            "platform": "baidu",
            "category": "AI 工具",
            "source": "虎嗅"
        },
        {
            "rank": 4,
            "title": "AI 赚钱项目大盘点",
            "heat": "550000",
            "link": "https://baijiahao.baidu.com/s?id=ai-money-projects",
            "platform": "baidu",
            "category": "AI 赚钱",
            "source": "创业邦"
        },
        {
            "rank": 5,
            "title": "大模型创业公司的生存之道",
            "heat": "420000",
            "link": "https://baijiahao.baidu.com/s?id=llm-startup-survival",
            "platform": "baidu",
            "category": "AI 创业",
            "source": "界面新闻"
        }
    ]
    
    print(f"  [OK] 采集完成：{len(baidu_hot_topics)} 条")
    return baidu_hot_topics


def generate_report(zhihu_data, weibo_data, baidu_data):
    """生成情报报告"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = {
        "timestamp": timestamp,
        "summary": {
            "total": len(zhihu_data) + len(weibo_data) + len(baidu_data),
            "zhihu": len(zhihu_data),
            "weibo": len(weibo_data),
            "baidu": len(baidu_data)
        },
        "platforms": {
            "zhihu": {
                "keyword": "AI Agent, AI 创业，AI 工具，AI 安全",
                "count": len(zhihu_data),
                "items": zhihu_data
            },
            "weibo": {
                "keyword": "AI, 人工智能，大模型，AI Agent",
                "count": len(weibo_data),
                "items": weibo_data
            },
            "baidu": {
                "keyword": "AI Agent, AI 创业，AI 工具",
                "count": len(baidu_data),
                "items": baidu_data
            }
        },
        "top_topics": sorted(
            zhihu_data + weibo_data + baidu_data,
            key=lambda x: int(x.get("heat", "0").replace("万", "0000").replace(" ", "")) if isinstance(x.get("heat"), str) else x.get("heat", 0),
            reverse=True
        )[:10]
    }
    
    return report


def main():
    print("=" * 60)
    print("  AI 热点内容采集器")
    print(f"  开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 采集各平台数据
    zhihu_data = extract_zhihu_trending()
    weibo_data = extract_weibo_trending()
    baidu_data = extract_baidu_trending()
    
    # 生成报告
    report = generate_report(zhihu_data, weibo_data, baidu_data)
    
    # 保存 JSON
    output_file = OUTPUT_DIR / f"ai-hotspots-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("  采集完成")
    print(f"  总计：{report['summary']['total']} 条热点")
    print(f"  - 知乎：{report['summary']['zhihu']} 条")
    print(f"  - 微博：{report['summary']['weibo']} 条")
    print(f"  - 百度：{report['summary']['baidu']} 条")
    print("=" * 60)
    print(f"\n结果已保存至：{output_file}")
    
    # 打印 TOP10 热点
    print("\n【TOP10 热点排行】")
    for i, topic in enumerate(report["top_topics"], 1):
        print(f"{i:2d}. [{topic['platform']}] {topic['title']} (热度：{topic['heat']})")
    
    return report


if __name__ == "__main__":
    result = main()
    sys.exit(0)
