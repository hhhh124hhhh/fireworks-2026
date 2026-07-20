---
name: ai-insights-generator
version: 3.0.0
description: 黄金选题 Skill - 多源搜索 + 洞察分析，基于上下文工程思想的智能选题工具
author: Clawdbot Team
category: ai-research
tags: [insights,选题,golden-topic,tavily,searxng,twitter,baidu,slack,feishu,workflow,context-engineering]
---

# 黄金选题 Skill - AI 洞察生成器

基于"上下文 > 模型"思想的多源搜索和洞察生成工具，自动化"持续的搜索加洞察才能出结果"流程，打造黄金选题能力。

## 核心理念

**"上下文 > 模型"**：
- 90% 的知识工作是重复、结构化、可预测的
- 不需要最强模型，需要的是：上下文 + 工作流 + 记忆 + 良好模型
- Skill 的价值来自设计，不是模型能力

**多源搜索 + 洞察分析 = 黄金选题**：
- Tavily: AI 优化的深度搜索
- SearXNG: 隐私保护的本地搜索
- Twitter/X: 社交媒体趋势和实时信息
- 百度搜索: 中文搜索和本地化内容
- 综合分析，生成选题建议

## 集成的搜索源

### 1. Tavily Search
- **特点**: AI 优化的深度搜索，返回高质量、相关性强结果
- **适用**: AI 技术、学术研究、深度分析
- **API**: Tavily API

### 2. SearXNG
- **特点**: 隐私保护的本地元搜索引擎
- **适用**: 通用搜索、网络趋势、广泛主题
- **API**: 本地 SearXNG 实例

### 3. Twitter/X API
- **特点**: 实时社交媒体趋势和用户讨论
- **适用**: 热点话题、社交媒体趋势、实时信息
- **API**: Twitter API

### 4. 百度搜索
- **特点**: 中文搜索和本地化内容，覆盖中文互联网
- **适用**: 中文选题、本地化趋势、中文用户讨论
- **API**: 百度千帆 AI 搜索 API

## 功能模块

### 1. 多源搜索模块（Multi-Source Search Module）
- 支持多个搜索源并行搜索
- 可选择特定搜索源或全部使用
- 每个搜索源获取指定数量结果
- 统一结果格式

### 2. 分布分析模块（Distribution Analysis Module）
- 分析搜索源结果分布
- 识别各搜索源的优势
- 综合评估选题热度

### 3. 选题建议模块（Topic Recommendation Module）
- 基于搜索结果生成选题建议
- 评估选题热度、可行性
- 提供多维度评分

### 4. 洞察模块（Insight Module）
- 聚合多个搜索主题的结果
- 生成可行动的洞察
- 识别关键发现

### 5. 推送模块（Push Module）
- 推送到 Slack/Feishu
- 支持 Markdown 格式
- PPT 友好的结构

### 6. 记忆模块（Memory Module）
- 保存历史洞察
- 识别长期趋势
- 跨会话传递

## 使用方法

### 基础使用（手动触发）

```bash
# 使用所有搜索源生成洞察
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py

# 自定义搜索主题
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --topics "AI agents 2026,knowledge worker automation"

# 选择特定搜索源
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --sources "tavily,searxng"

# 仅使用 Twitter
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --sources "twitter"

# 推送到 Slack
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --push-slack

# 推送到 Feishu
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --push-feishu

# 保存到文件
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --output /root/clawd/memory/ai-insights/insights-$(date +%Y%m%d).md
```

### 定时任务（可选）

```bash
# 每天早上 9 点执行，使用所有搜索源，推送到 Slack
0 9 * * * bash -c "python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py --push-slack"

# 每天早上 9 点执行，仅使用 Tavily 和 SearXNG
0 9 * * * bash -c "python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py --sources 'tavily,searxng' --push-slack"

# 每天早上 9 点执行，仅使用 Twitter（监控热点）
0 9 * * * bash -c "python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py --sources 'twitter' --push-slack"
```

## 默认搜索主题

1. AI agent best practices 2026
2. knowledge worker automation tools
3. workflow design patterns AI
4. context engineering examples
5. AI agent case studies enterprise
6. AI productivity software reviews
7. enterprise AI adoption trends
8. AI skill development training
9. AI automation use cases
10. AI implementation strategies

## 输出格式

### Markdown 格式（PPT 友好）
- 核心洞察
- 量化数据
- 搜索源分布
- 关键发现
- 选题建议
- 立即行动

### 选题建议评分

**高热度选题**（>50 条结果）：
- ✅ 高热度：该主题搜索结果丰富，适合作为黄金选题

**中热度选题**（20-50 条结果）：
- ⚠️ 中热度：该主题有一定关注度，可作为备选选题

**低热度选题**（<20 条结果）：
- ❌ 低热度：该主题关注度较低，建议重新评估

**社交媒体热度**：
- 📱 社交热度高：Twitter 上讨论热烈，适合热点选题

**AI 相关度**：
- 🤖 AI 相关度高：Tavily 结果丰富，适合 AI 技术选题

**通用搜索度**：
- 🔍 通用搜索高：SearXNG 结果丰富，适合通用选题

**中文热度**：
- 🇨🇳 中文热度高：百度结果丰富，适合中文选题

## 配置

### 环境变量

```bash
# Tavily API Key（必需）
export TAVILY_API_KEY="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"

# SearXNG URL（可选，默认 http://localhost:8080）
export SEARXNG_URL="http://localhost:8080"

# Twitter API Key（可选）
export TWITTER_API_KEY="your-twitter-api-key"

# Slack Webhook URL（可选）
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX"

# Feishu Webhook URL（可选）
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/XXX"
```

### 配置文件

```json
{
  "tavily_api_key": "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",
  "searxng_url": "http://localhost:8080",
  "twitter_api_key": "your-twitter-api-key",
  "search_topics": [
    "AI agent best practices",
    "knowledge worker automation"
  ],
  "default_sources": ["tavily", "searxng", "twitter"],
  "max_results_per_source": 5,
  "search_depth": "advanced",
  "output_format": "markdown",
  "push_to": ["slack", "file"],
  "output_directory": "/root/clawd/memory/ai-insights"
}
```

## 黄金选题策略

### 策略 1: 综合热度分析
- 使用所有搜索源
- 综合评估各搜索源的热度
- 识别全面受关注的主题

### 策略 2: AI 技术导向
- 主要使用 Tavily
- 关注 AI 技术和实现
- 适合技术深度选题

### 策略 3: 社交热点追踪
- 主要使用 Twitter
- 实时监控社交媒体热点
- 适合热点话题选题

### 策略 4: 通用趋势分析
- 主要使用 SearXNG
- 关注广泛网络趋势
- 适合通用选题

## 技能特点（基于"上下文 > 模型"）

### 上下文（Context）
- 多源搜索：Tavily、SearXNG、Twitter
- AI 趋势和新闻
- Agent 最佳实践
- 工作流设计案例
- 社交媒体热点
- 企业级 AI 应用

### 工作流（Workflow）
- 搜索 → 分析 → 洞察 → 推送
- 多源并行搜索
- 自动化流程
- 可扩展的模块化设计

### 记忆（Memory）
- 保存历史洞察
- 识别长期趋势
- 跨会话传递
- 版本化存储（最近 100 条）

## 版本信息

- **版本**: 3.0.0
- **发布日期**: 2026-02-21
- **兼容性**: Tavily API, SearXNG, Twitter API, 百度搜索 API, Slack Webhook, Feishu Webhook
- **Python 版本**: 3.7+
- **依赖**: tavily-python, requests, python-dotenv

## 更新日志

### v3.0.0 (2026-02-21)
- ✅ 集成百度搜索
- ✅ 添加中文选题建议（🇨🇳 中文热度高）
- ✅ 更新为 4 个搜索源
- ✅ 更新文档和示例

### v2.0.0 (2026-02-21)
- ✅ 集成多源搜索：Tavily、SearXNG、Twitter
- ✅ 添加选题建议模块
- ✅ 添加搜索源分布分析
- ✅ 添加黄金选题策略

### v1.0.0 (2026-02-21)
- ✅ 初始版本
- ✅ Tavily 搜索
- ✅ 洞察生成
- ✅ 推送到 Slack/Feishu
