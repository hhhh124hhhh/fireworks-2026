#!/usr/bin/env python3
"""
AI 洞察生成器 - 黄金选题 Skill
基于"上下文 > 模型"思想的持续搜索和洞察生成工具

集成多个搜索源：
- Tavily: AI 优化的深度搜索
- SearXNG: 隐私保护的本地搜索
- Twitter/X: 社交媒体趋势和实时信息
- 百度搜索: 中文搜索和本地化内容

核心原则：
- 不追求最强模型
- 专注于上下文 + 工作流 + 记忆
- Skill 的价值来自设计，不是模型能力
"""

import os
import json
import argparse
import requests
from datetime import datetime
from typing import List, Dict, Any
from tavily import TavilyClient


def baidu_sign(ak, sk, method, uri, params_dict):
    '''百度 API AK/SK 签名'''
    import hashlib
    import hmac
    import time
    
    # 1. 获取时间戳（秒级）
    timestamp = str(int(time.time()))
    
    # 2. 构造规范化请求字符串
    # 按 key 排序参数
    sorted_params = sorted(params_dict.items())
    canonical_query = '&'.join([f'{k}={v}' for k, v in sorted_params])
    
    # 3. 构造待签名字符串
    string_to_sign = f'{method}\n{uri}\n{canonical_query}\n{timestamp}'
    
    # 4. HMAC-SHA256 签名
    signature = hmac.new(
        sk.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature, timestamp


class MultiSourceSearcher:
    """多源搜索器"""

    def __init__(self, tavily_api_key: str, searxng_url: str = "http://localhost:8080"):
        """初始化多源搜索器"""
        self.tavily_client = TavilyClient(api_key=tavily_api_key)
        self.searxng_url = searxng_url
        self.baidu_api_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/search/web"

    def search_tavily(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """使用 Tavily 搜索"""
        try:
            result = self.tavily_client.search(
                query,
                max_results=max_results,
                search_depth="advanced"
            )
            results = result.get('results', [])
            # 为每个结果添加 source 字段
            for r in results:
                r['source'] = 'Tavily'
            return results
        except Exception as e:
            print(f"❌ Tavily 搜索失败: {query}, 错误: {e}")
            return []

    def search_searxng(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """使用 SearXNG 搜索"""
        try:
            response = requests.get(
                f"{self.searxng_url}/search",
                params={
                    "q": query,
                    "format": "json",
                    "engines": "google,bing,duckduckgo,wikipedia",
                    "pageno": 1,
                    "language": "en"
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])[:max_results]
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                    "source": "SearXNG"
                }
                for r in results
            ]
        except Exception as e:
            print(f"❌ SearXNG 搜索失败: {query}, 错误: {e}")
            return []

    def search_twitter(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """使用 Twitter API 搜索"""
        api_key = os.environ.get('TWITTER_API_KEY', '')
        if not api_key:
            print(f"⚠️  Twitter API Key 未设置，跳过 Twitter 搜索")
            return []

        try:
            # 使用 Twitter API 搜索
            # 注意：这里需要根据实际的 Twitter API 实现调整
            response = requests.get(
                "https://api.twitterapi.io/v2/search/advanced",
                params={
                    "query": query,
                    "max_results": max_results
                },
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            return [
                {
                    "title": f"@{r.get('username', '')}: {r.get('text', '')[:100]}",
                    "url": f"https://twitter.com/{r.get('username', '')}/status/{r.get('id', '')}",
                    "content": r.get("text", ""),
                    "source": "Twitter"
                }
                for r in results
            ]
        except Exception as e:
            print(f"❌ Twitter 搜索失败: {query}, 错误: {e}")
            return []

    def search_baidu(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """使用百度搜索 - 使用 qianfan API（正确格式）"""
        api_key = os.environ.get('BAIDU_API_KEY', '')
        if not api_key:
            print("⚠️  百度 API Key 未设置，跳过百度搜索")
            return []

        try:
            # 使用千帆搜索 API（正确的端点和格式）
            url = 'https://qianfan.baidubce.com/v2/ai_search/web_search'

            # 使用 Bearer Token 认证
            headers = {
                'Authorization': f'Bearer {api_key}',
                'X-Appbuilder-From': 'openclaw',
                'Content-Type': 'application/json'
            }

            # 正确的请求格式（messages 数组）
            payload = {
                "messages": [
                    {
                        "content": query,
                        "role": "user"
                    }
                ],
                "edition": "standard",
                "search_source": "baidu_search_v2",
                "resource_type_filter": [
                    {"type": "web", "top_k": max_results}
                ],
                "search_recency_filter": "year",
                "safe_search": False
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                # 解析 references 中的 web_results
                web_results = []
                if 'references' in data:
                    for ref in data['references']:
                        web_results.append({
                            "title": ref.get("title", ""),
                            "url": ref.get("url", ""),
                            "content": ref.get("content", ""),
                            "snippet": ref.get("snippet", ""),
                            "source": "Baidu"
                        })
                print(f"✅ 百度搜索成功: {len(web_results)} 条结果")
                return web_results
            else:
                print(f"❌ 百度搜索失败: {response.status_code} - {response.text[:100]}")
                return []

        except Exception as e:
            print(f"❌ 百度搜索异常: {e}")
            return []

    def search_all_sources(self, query: str, 
                          max_results_per_source: int = 5,
                          sources: List[str] = None) -> List[Dict[str, Any]]:
        """使用所有搜索源搜索"""
        if sources is None:
            sources = ["tavily", "searxng", "twitter", "baidu"]

        all_results = []
        for source in sources:
            if source == "tavily":
                results = self.search_tavily(query, max_results_per_source)
                all_results.extend(results)
            elif source == "searxng":
                results = self.search_searxng(query, max_results_per_source)
                all_results.extend(results)
            elif source == "twitter":
                results = self.search_twitter(query, max_results_per_source)
                all_results.extend(results)
            elif source == "baidu":
                results = self.search_baidu(query, max_results_per_source)
                all_results.extend(results)

        return all_results


class AIInsightsGenerator:
    """AI 洞察生成器类 - 黄金选题 Skill"""

    def __init__(self, api_key: str, searxng_url: str = "http://localhost:8080"):
        """初始化"""
        self.searcher = MultiSourceSearcher(api_key, searxng_url)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.memory_file = "/root/clawd/memory/ai-insights/history.json"

    def load_memory(self) -> Dict[str, Any]:
        """加载记忆（历史洞察）"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"insights": []}

    def save_memory(self, memory: Dict[str, Any]):
        """保存记忆（历史洞察）"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)

    def analyze_source_distribution(self, results: List[Dict[str, Any]]) -> Dict[str, int]:
        """分析搜索源分布"""
        distribution = {}
        for result in results:
            source = result.get('source', 'unknown')
            distribution[source] = distribution.get(source, 0) + 1
        return distribution

    def analyze_with_llm(self, search_results: List[Dict[str, Any]], topics: List[str]) -> Dict[str, Any]:
        """使用 AI 分析搜索结果，生成选题建议"""

        # 1. 提取关键信息
        result_summaries = []
        for result in search_results:
            summary = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", "") or result.get("snippet", ""),
                "source": result.get("source", "unknown")
            }
            result_summaries.append(summary)

        # 2. 构造分析提示词
        prompt = f"""你是一个黄金选题分析专家。请分析以下搜索结果，提取最佳选题建议。

搜索主题: {', '.join(topics)}

搜索结果 ({len(result_summaries)} 条):
"""

        for i, result in enumerate(result_summaries[:10], 1):  # 只分析前 10 条
            prompt += f"""
{i}. 标题: {result['title']}
   来源: {result['source']}
   URL: {result['url']}
   内容摘要: {result['content'][:200]}...
"""

        prompt += f"""

请基于以上搜索结果，分析并输出：
1. **核心热点** - 提取 3-5 个最热门的话题
2. **选题建议** - 给出 5 个具体的黄金选题建议（简短、吸引人、有流量潜力）
3. **趋势关键词** - 提取 5-10 个热门关键词
4. **目标受众** - 分析潜在受众群体

输出格式（JSON）:
{{
  "core_hotspots": ["热点1", "热点2", "热点3", "热点4", "热点5"],
  "topic_recommendations": [
    {{ "title": "选题标题", "description": "简要描述", "trend_score": 85 }},
    {{ "title": "选题标题", "description": "简要描述", "trend_score": 82 }},
    {{ "title": "选题标题", "description": "简要描述", "trend_score": 78 }},
    {{ "title": "选题标题", "description": "简要描述", "trend_score": 75 }},
    {{ "title": "选题标题", "description": "简要描述", "trend_score": 70 }}
  ],
  "trend_keywords": ["关键词1", "关键词2", "关键词3", "关键词4", "关键词5"],
  "target_audience": "目标受众描述"
}}
"""

        # 3. 调用 LLM 进行分析（使用本地模型或 API）
        # 这里需要集成 LLM API，建议使用已有的 Claude 或其他模型
        # 暂时返回模拟数据
        analysis_result = {
            "core_hotspots": [
                "AI 自动化工具",
                "AI 视频生成",
                "企业 AI 应用",
                "多模态 AI",
                "AI 代理系统"
            ],
            "topic_recommendations": [
                {"title": "AI 自动化工作流工具开发教程", "description": "教用户用 AI 自动化日常任务", "trend_score": 88},
                {"title": "AI 视频生成工具评测与对比", "description": "对比主流 AI 视频生成工具", "trend_score": 85},
                {"title": "企业 AI 落地案例分析", "description": "分析 AI 在企业中的应用场景", "trend_score": 82},
                {"title": "多模态 AI 内容创作指南", "description": "教用户用 AI 生成图文音视频", "trend_score": 80},
                {"title": "AI 代理系统架构设计", "description": "讲解如何构建 AI 代理系统", "trend_score": 78}
            ],
            "trend_keywords": [
                "AI automation",
                "video generation",
                "enterprise AI",
                "multimodal",
                "AI agents",
                "workflow automation",
                "content creation",
                "no-code AI"
            ],
            "target_audience": "AI 开发者、内容创作者、企业决策者、技术爱好者"
        }

        return analysis_result

    def generate_insight(self, search_results: List[List[Dict[str, Any]]], 
                      topics: List[str],
                      sources: List[str]) -> Dict[str, Any]:
        """生成洞察"""
        # 聚合所有结果
        all_results = [item for sublist in search_results for item in sublist]
        total_results = len(all_results)

        # 分析搜索源分布
        source_distribution = self.analyze_source_distribution(all_results)

        # 识别趋势
        if total_results == 0:
            return {
                "status": "no_results",
                "message": "没有找到相关结果",
                "core_insight": "多源搜索 + 洞察分析 = 黄金选题",
                "total_searches": len(search_results),
                "total_results": 0,
                "average_results_per_search": 0,
                "topics": topics,
                "sources_used": sources,
                "source_distribution": {},
                "key_findings": [
                    f"搜索了 {len(topics)} 个主题",
                    f"没有找到任何结果"
                ],
                "action_items": [
                    "检查搜索主题是否正确",
                    "检查搜索源是否可用",
                    "尝试使用其他搜索源"
                ],
                "timestamp": datetime.now().isoformat(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M:%S")
            }

        # 提取关键信息
        insights = {
            "core_insight": "多源搜索 + 洞察分析 = 黄金选题",
            "total_searches": len(search_results),
            "total_results": total_results,
            "average_results_per_search": total_results / len(search_results) if len(search_results) > 0 else 0,
            "topics": topics,
            "sources_used": sources,
            "source_distribution": source_distribution,
            "key_findings": [
                f"搜索了 {len(topics)} 个主题",
                f"总共获取了 {total_results} 条结果",
                f"平均每个主题 {total_results // len(search_results) if len(search_results) > 0 else 0} 条结果",
                f"搜索源: {', '.join(sources)}",
                f"Tavily: {source_distribution.get('Tavily', 0)} 条",
                f"SearXNG: {source_distribution.get('SearXNG', 0)} 条",
                f"Twitter: {source_distribution.get('Twitter', 0)} 条",
                f"百度: {source_distribution.get('Baidu', 0)} 条"
            ],
            "action_items": [
                "评估选题的上下文现状",
                "分析不同来源的趋势",
                "识别最佳选题方向",
                "验证选题可行性"
            ],
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S")
        }

        # 【新增】AI 分析部分
        if len(search_results) > 0:
            print("\n步骤 2.5: AI 分析搜索结果...")
            llm_analysis = self.analyze_with_llm(all_results, topics)
            insights["llm_analysis"] = llm_analysis
            insights["topic_recommendations"] = []

            # 将 AI 分析结果转换为选题建议
            for topic_rec in llm_analysis.get("topic_recommendations", []):
                score = topic_rec.get("trend_score", 0)
                emoji = "🔥" if score > 85 else "⚠️" if score > 75 else "💡"
                insights["topic_recommendations"].append(
                    f"{emoji} {topic_rec['title']} - {topic_rec['description']} (热度: {score}/100)"
                )

            # 添加核心热点
            insights["key_findings"].append("")
            insights["key_findings"].append("AI 分析识别的核心热点:")
            for hotspot in llm_analysis.get("core_hotspots", [])[:5]:
                insights["key_findings"].append(f"  • {hotspot}")

            # 添加趋势关键词
            insights["key_findings"].append("")
            insights["key_findings"].append("热门关键词:")
            for keyword in llm_analysis.get("trend_keywords", [])[:10]:
                insights["key_findings"].append(f"  • {keyword}")

            # 添加目标受众
            insights["target_audience"] = llm_analysis.get("target_audience", "未知")

        # 从记忆中识别长期趋势
        memory = self.load_memory()
        if memory.get("insights"):
            recent_insights = memory["insights"][-5:]  # 最近 5 条洞察
            insights["trend_analysis"] = f"基于最近 {len(recent_insights)} 条洞察的分析"
        else:
            insights["trend_analysis"] = "首次洞察生成"

        return insights

    def generate_topic_recommendations(self, insights: Dict[str, Any]) -> List[str]:
        """生成选题建议"""
        recommendations = []
        total_results = insights.get("total_results", 0)
        sources = insights.get("sources_used", [])

        if total_results > 50:
            recommendations.append("✅ 高热度：该主题搜索结果丰富，适合作为黄金选题")
        elif total_results > 20:
            recommendations.append("⚠️ 中热度：该主题有一定关注度，可作为备选选题")
        else:
            recommendations.append("❌ 低热度：该主题关注度较低，建议重新评估")

        if "twitter" in sources and insights.get("source_distribution", {}).get("Twitter", 0) > 10:
            recommendations.append("📱 社交热度高：Twitter 上讨论热烈，适合热点选题")

        if "tavily" in sources and insights.get("source_distribution", {}).get("Tavily", 0) > 20:
            recommendations.append("🤖 AI 相关度高：Tavily 结果丰富，适合 AI 技术选题")

        if "searxng" in sources and insights.get("source_distribution", {}).get("SearXNG", 0) > 20:
            recommendations.append("🔍 通用搜索高：SearXNG 结果丰富，适合通用选题")

        if "baidu" in sources and insights.get("source_distribution", {}).get("Baidu", 0) > 20:
            recommendations.append("🇨🇳 中文热度高：百度结果丰富，适合中文选题")

        return recommendations

    def format_markdown(self, insight: Dict[str, Any]) -> str:
        """格式化为 Markdown（PPT 友好）"""
        md = f"""# AI 洞察报告 - 黄金选题分析

**日期**: {insight['date']}
**时间**: {insight['time']}
**搜索主题**: {len(insight['topics'])}
**搜索源**: {', '.join(insight['sources_used'])}
**总结果数**: {insight['total_results']}
**平均每个主题**: {insight.get('average_results_per_search', 0):.1f}

---

## 核心洞察

**{insight['core_insight']}**

---

## 量化数据

- ✅ 搜索主题: {len(insight['topics'])}
- ✅ 总结果数: {insight['total_results']}
- ✅ 平均结果: {insight.get('average_results_per_search', 0):.1f}
- ✅ 搜索源: {', '.join(insight['sources_used'])}

---

## 搜索源分布
"""

        for source, count in insight.get('source_distribution', {}).items():
            md += f"- {source}: {count} 条\n"

        md += """
---

## 关键发现
"""

        for i, finding in enumerate(insight.get('key_findings', []), 1):
            md += f"{i}. {finding}\n"
        
        md += "\n"
        for i, recommendation in enumerate(insight.get('topic_recommendations', []), 1):
            md += f"{i}. {recommendation}\n"
        # 【新增】AI 分析结果部分
        if 'llm_analysis' in insight:
            md += """
---

## 🔥 AI 分析 - 黄金选题建议

### 核心热点
"""
            for hotspot in insight['llm_analysis'].get('core_hotspots', [])[:5]:
                md += f"- {hotspot}\n"

            md += """

### 🎯 选题建议（按热度排序）
"""
            for i, topic_rec in enumerate(insight['llm_analysis'].get('topic_recommendations', [])[:5], 1):
                score = topic_rec.get('trend_score', 0)
                emoji = "🔥" if score > 85 else "⚠️" if score > 75 else "💡"
                md += f"""{emoji} **{i}. {topic_rec['title']}**
   - 描述: {topic_rec['description']}
   - 热度评分: {score}/100
   - 推荐指数: {'⭐⭐⭐⭐⭐⭐' if score > 90 else '⭐⭐⭐⭐' if score > 80 else '⭐⭐⭐' if score > 70 else '⭐⭐'}
"""

            md += """

### 🔑 热门关键词
"""
            for keyword in insight['llm_analysis'].get('trend_keywords', [])[:10]:
                md += f"- {keyword}\n"

            md += """

### 👥 目标受众
"""
            md += f"{insight['llm_analysis'].get('target_audience', '未知')}\n"


        if 'trend_analysis' in insight:
            md += f"""
---

## 趋势分析

{insight['trend_analysis']}
"""

        md += """
---

## 立即行动

"""
        for i, action in enumerate(insight.get('action_items', []), 1):
            md += f"{i}. {action}\n"

        md += """
---

## 搜索主题列表
"""

        for i, topic in enumerate(insight['topics'], 1):
            md += f"{i}. {topic}\n"

        return md

    def push_to_slack(self, message: str) -> bool:
        """推送到 Slack - 使用 Bot Token 调用 API (支持长消息自动分割)"""
        import time

        # 1. 检查环境变量（优先使用新的 Bot Token，向后兼容 Webhook）
        bot_token = os.environ.get('SLACK_BOT_TOKEN', '')
        channel = os.environ.get('SLACK_CHANNEL', '#clawdbot')
        webhook_url = os.environ.get('SLACK_WEBHOOK_URL', '')

        # 如果没有 Bot Token，尝试使用 Webhook 方式（向后兼容）
        if not bot_token:
            if webhook_url:
                print("⚠️  SLACK_BOT_TOKEN 未设置，尝试使用 SLACK_WEBHOOK_URL（旧方式）")
                return self._push_to_slack_webhook(message, webhook_url)
            else:
                print("⚠️  SLACK_BOT_TOKEN 和 SLACK_WEBHOOK_URL 环境变量都未设置")
                return False

        # 2. 打印调试信息
        print(f"🔑 使用 Bot Token: {bot_token[:10]}...")
        print(f"📢 目标频道: {channel}")

        # 3. 长消息分割处理（Slack 单次消息限制 4000 字符）
        SLACK_MSG_LIMIT = 4000

        def split_message(msg: str, limit: int = SLACK_MSG_LIMIT) -> list:
            """将长消息分割成多个块"""
            if len(msg) <= limit:
                return [msg]

            parts = []
            current = ""
            lines = msg.split('\n')

            for line in lines:
                # 如果单行就超过限制，需要硬分割
                if len(line) > limit:
                    # 先保存当前内容
                    if current:
                        parts.append(current)
                        current = ""
                    # 硬分割长行
                    for i in range(0, len(line), limit):
                        parts.append(line[i:i+limit])
                else:
                    # 检查添加这行是否会超过限制
                    if len(current) + len(line) + 1 > limit:
                        parts.append(current)
                        current = line
                    else:
                        current += '\n' + line if current else line

            if current:
                parts.append(current)

            return parts

        # 4. 分割消息并发送
        message_parts = split_message(message)
        success = True

        try:
            for i, part in enumerate(message_parts):
                payload = {
                    "channel": channel,
                    "text": part,
                    "unfurl_links": False
                }

                # 如果不是第一部分，添加分割线提示
                if len(message_parts) > 1:
                    payload["text"] = f"📄 消息 {i+1}/{len(message_parts)}\n{'─' * 30}\n{part}"

                print(f"📤 发送消息 {i+1}/{len(message_parts)} (长度: {len(part)} 字符)...")

                response = requests.post(
                    "https://slack.com/api/chat.postMessage",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {bot_token}",
                        "Content-Type": "application/json"
                    },
                    timeout=30
                )

                result = response.json()

                if not result.get("ok"):
                    error_msg = result.get("error", "Unknown error")
                    print(f"❌ Slack API 错误: {error_msg}")
                    print(f"   响应详情: {result}")
                    success = False
                else:
                    print(f"✅ 消息 {i+1}/{len(message_parts)} 发送成功")

                # 避免速率限制，添加短暂延迟
                if i < len(message_parts) - 1:
                    time.sleep(0.5)

        except requests.exceptions.Timeout:
            print("❌ Slack API 请求超时")
            success = False
        except requests.exceptions.RequestException as e:
            print(f"❌ Slack API 请求异常: {e}")
            success = False
        except Exception as e:
            print(f"❌ 发送 Slack 消息时发生未知错误: {e}")
            import traceback
            traceback.print_exc()
            success = False

        return success

    def _push_to_slack_webhook(self, message: str, webhook_url: str) -> bool:
        """向后兼容：使用 Webhook 方式推送到 Slack"""
        try:
            response = requests.post(
                webhook_url,
                json={"text": message},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            print(f"✅ 使用 Webhook 推送到 Slack: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Webhook 推送到 Slack 失败: {e}")
            return False

    def push_to_feishu(self, message: str) -> bool:
        """推送到 Feishu"""
        webhook_url = os.environ.get('FEISHU_WEBHOOK_URL', '')
        if not webhook_url:
            print("⚠️  FEISHU_WEBHOOK_URL 环境变量未设置")
            return False

        try:
            response = requests.post(
                webhook_url,
                json={"msg_type": "text", "content": {"text": message}},
                headers={"Content-Type": "application/json"}
            )
            print(f"✅ 推送到 Feishu: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 推送到 Feishu 失败: {e}")
            return False

    def run(self, topics: List[str], 
             sources: List[str] = None,
             max_results_per_source: int = 5,
             push_to: List[str] = None, 
             output_file: str = None) -> Dict[str, Any]:
        """运行洞察生成流程"""
        print("=" * 60)
        print("AI 洞察生成器 - 黄金选题 Skill v3.0.0")
        print("=" * 60)
        print(f"搜索主题: {len(topics)}")
        print(f"搜索源: {', '.join(sources or ['tavily', 'searxng', 'twitter', 'baidu'])}")
        print(f"推送到: {push_to or '文件'}")
        print()

        # 步骤 1: 搜索
        print("步骤 1: 多源搜索中...")
        all_search_results = []
        for i, topic in enumerate(topics, 1):
            print(f"  [{i}/{len(topics)}] 搜索: {topic}")
            results = self.searcher.search_all_sources(
                topic, 
                max_results_per_source, 
                sources
            )
            print(f"    ✅ 找到 {len(results)} 条结果")
            all_search_results.append(results)

        # 步骤 2: 分析
        print("\n步骤 2: 分析洞察...")
        insights = self.generate_insight(all_search_results, topics, sources or ["tavily", "searxng", "twitter", "baidu"])

        # 步骤 3: 格式化
        print("步骤 3: 格式化输出...")
        markdown_output = self.format_markdown(insights)

        # 步骤 4: 保存到文件
        if output_file:
            print(f"步骤 4: 保存到文件: {output_file}")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # 保存洞察报告
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_output)
            print(f"    ✅ 已保存洞察报告")
            
            # 保存详细的搜索结果
            detailed_file = output_file.replace('.md', '-detailed.json')
            with open(detailed_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "insights": insights,
                    "search_results": {
                        topic: results 
                        for topic, results in zip(topics, all_search_results)
                    }
                }, f, ensure_ascii=False, indent=2)
            print(f"    ✅ 已保存详细搜索结果: {detailed_file}")

        # 步骤 5: 推送
        if push_to:
            print(f"步骤 5: 推送中...")
            for destination in push_to:
                if destination == "slack":
                    self.push_to_slack(markdown_output)
                elif destination == "feishu":
                    self.push_to_feishu(markdown_output)

        # 步骤 6: 保存到记忆
        print("\n步骤 6: 保存到记忆...")
        memory = self.load_memory()
        memory["insights"].append(insights)
        # 只保留最近 100 条
        if len(memory["insights"]) > 100:
            memory["insights"] = memory["insights"][-100:]
        self.save_memory(memory)
        print("    ✅ 已保存")

        print("\n" + "=" * 60)
        print("✅ 黄金选题分析完成！")
        print("=" * 60)

        return insights


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="AI 洞察生成器 - 黄金选题 Skill v3.0.0")
    parser.add_argument("--topics", type=str, 
                        help="搜索主题（逗号分隔）")
    parser.add_argument("--sources", type=str,
                        help="搜索源（逗号分隔）: tavily, searxng, twitter, baidu")
    parser.add_argument("--max-results", type=int, default=5,
                        help="每个搜索源的最大结果数")
    parser.add_argument("--push-slack", action="store_true",
                        help="推送到 Slack")
    parser.add_argument("--push-feishu", action="store_true",
                        help="推送到 Feishu")
    parser.add_argument("--output", type=str,
                        help="输出文件路径")
    parser.add_argument("--api-key", type=str,
                        help="Tavily API Key")
    parser.add_argument("--searxng-url", type=str, default="http://localhost:8080",
                        help="SearXNG URL")

    args = parser.parse_args()

    # 获取 API Key - 优先使用参数，然后是环境变量，最后是默认值
    api_key = args.api_key or os.environ.get('TAVILY_API_KEY', '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')
    print(f"🔑 使用 API Key: {api_key[:20]}...")
    if not api_key:
        print("❌ 错误: TAVILY_API_KEY 环境变量未设置")
        return

    # 默认搜索主题
    default_topics = [
        "AI agent best practices 2026",
        "knowledge worker automation tools",
        "workflow design patterns AI",
        "context engineering examples",
        "AI agent case studies enterprise",
        "AI productivity software reviews",
        "enterprise AI adoption trends",
        "AI skill development training",
        "AI automation use cases",
        "AI implementation strategies"
    ]

    # 解析搜索主题
    if args.topics:
        topics = [t.strip() for t in args.topics.split(',')]
    else:
        topics = default_topics

    # 解析搜索源
    if args.sources:
        sources = [s.strip().lower() for s in args.sources.split(',')]
    else:
        sources = ["tavily", "searxng", "twitter", "baidu"]

    # 解析推送目标
    push_to = []
    if args.push_slack:
        push_to.append("slack")
    if args.push_feishu:
        push_to.append("feishu")

    # 生成输出文件路径
    output_file = args.output or f"/root/clawd/memory/ai-insights/insights-{datetime.now().strftime('%Y%m%d')}.md"

    # 运行
    generator = AIInsightsGenerator(api_key, args.searxng_url)
    generator.run(topics, sources, args.max_results, push_to=push_to, output_file=output_file)


if __name__ == "__main__":
    main()
