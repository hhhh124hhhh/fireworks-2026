# 黄金选题 Skill - 使用说明

## 概述

黄金选题 Skill 是基于"上下文 > 模型"思想的多源搜索和洞察生成工具，集成四大搜索源：
- **Tavily**: AI 优化的深度搜索
- **SearXNG**: 隐私保护的本地搜索
- **Twitter/X**: 社交媒体趋势和实时信息
- **百度搜索**: 中文搜索和本地化内容

核心价值：**多源搜索 + 洞察分析 = 黄金选题**

## 快速开始

### 1. 设置环境变量

```bash
# Tavily API Key（必需）
export TAVILY_API_KEY="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"

# SearXNG URL（可选，默认 http://localhost:8080）
export SEARXNG_URL="http://localhost:8080"

# Twitter API Key（可选）
export TWITTER_API_KEY="your-twitter-api-key"

# 百度 API Key（可选）
export BAIDU_API_KEY="your-baidu-api-key"

# Slack Webhook URL（可选）
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX"

# Feishu Webhook URL（可选）
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/XXX"
```

### 2. 基础使用

```bash
# 使用所有搜索源生成洞察
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py

# 自定义搜索主题
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --topics "AI agents 2026,knowledge worker automation"

# 选择特定搜索源
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --sources "tavily,searxng"

# 仅使用百度（中文选题）
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --sources "baidu"

# 仅使用 Twitter（监控热点）
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
  --output /root/clawd/memory/ai-insights/my-insights.md
```

### 3. 定时任务

```bash
# 每天早上 9 点执行，使用所有搜索源，推送到 Slack
0 9 * * * bash -c "python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py --push-slack"

# 每天早上 9 点执行，仅使用 Tavily 和 SearXNG
0 9 * * * bash -c "python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py --sources 'tavily,searxng' --push-slack"

# 每天早上 9 点执行，仅使用 Twitter（监控热点）
0 9 * * * bash -c "python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py --sources 'twitter' --push-slack"

# 每天早上 9 点执行，保存到文件
0 9 * * * bash -c "python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py --output /root/clawd/memory/ai-insights/insights-$(date +\%Y\%m\%d).md"
```

## 搜索源说明

### Tavily Search
- **特点**: AI 优化的深度搜索，返回高质量、相关性强结果
- **适用**: AI 技术、学术研究、深度分析
- **API**: Tavily API
- **结果格式**: JSON

### SearXNG
- **特点**: 隐私保护的本地元搜索引擎
- **适用**: 通用搜索、网络趋势、广泛主题
- **API**: 本地 SearXNG 实例
- **结果格式**: JSON

### Twitter/X API
- **特点**: 实时社交媒体趋势和用户讨论
- **适用**: 热点话题、社交媒体趋势、实时信息
- **API**: Twitter API
- **结果格式**: JSON

### 百度搜索
- **特点**: 中文搜索和本地化内容，覆盖中文互联网
- **适用**: 中文选题、本地化趋势、中文用户讨论
- **API**: 百度千帆 AI 搜索 API
- **结果格式**: JSON

## 输出示例

### Markdown 格式（PPT 友好）

```markdown
# AI 洞察报告 - 黄金选题分析

**日期**: 2026-02-21
**时间**: 10:35:00
**搜索主题**: 10
**搜索源**: tavily, searxng, twitter
**总结果数**: 150
**平均每个主题**: 15.0

---

## 核心洞察

多源搜索 + 洞察分析 = 黄金选题

---

## 量化数据

- ✅ 搜索主题: 10
- ✅ 总结果数: 150
- ✅ 平均结果: 15.0
- ✅ 搜索源: tavily, searxng, twitter

---

## 搜索源分布

- Tavily: 50 条
- SearXNG: 50 条
- Twitter: 50 条

---

## 关键发现

1. 搜索了 10 个主题
2. 总共获取了 150 条结果
3. 平均每个主题 15 条结果
4. 搜索源: tavily, searxng, twitter
5. Tavily: 50 条
6. SearXNG: 50 条
7. Twitter: 50 条

---

## 选题建议

1. ✅ 高热度：该主题搜索结果丰富，适合作为黄金选题
2. 📱 社交热度高：Twitter 上讨论热烈，适合热点选题
3. 🤖 AI 相关度高：Tavily 结果丰富，适合 AI 技术选题
4. 🔍 通用搜索高：SearXNG 结果丰富，适合通用选题

---

## 立即行动

1. 评估选题的上下文现状
2. 分析不同来源的趋势
3. 识别最佳选题方向
4. 验证选题可行性

---

## 搜索主题列表

1. AI agent best practices 2026
2. knowledge worker automation tools
3. workflow design patterns AI
...
```

## 黄金选题策略

### 策略 1: 综合热度分析
- 使用所有搜索源
- 综合评估各搜索源的热度
- 识别全面受关注的主题

```bash
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --sources "tavily,searxng,twitter"
```

### 策略 2: AI 技术导向
- 主要使用 Tavily
- 关注 AI 技术和实现
- 适合技术深度选题

```bash
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --sources "tavily"
```

### 策略 3: 社交热点追踪
- 主要使用 Twitter
- 实时监控社交媒体热点
- 适合热点话题选题

```bash
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --sources "twitter"
```

### 策略 4: 通用趋势分析
- 主要使用 SearXNG
- 关注广泛网络趋势
- 适合通用选题

### 策略 5: 中文选题导向
- 主要使用百度
- 关注中文互联网趋势
- 适合中文选题

```bash
python3 /root/clawd/skills/ai-insights-generator/scripts/ai_insights_generator.py \
  --sources "searxng"
```

## 设计原则（基于"上下文 > 模型"）

### 1. 上下文优先
- 特定场景的数据源（多源搜索）
- 清晰的检索策略（并行搜索）
- 相关性和可靠性保证（多源验证）

### 2. 工作流清晰
- 任务分解（搜索、分析、洞察、推送）
- 工具调用（多源搜索器、分析器、推送器）
- 错误处理（各搜索源独立失败）

### 3. 记忆持久
- 知识库（历史洞察）
- 历史记录（最近 100 条）
- 跨会话传递（JSON 存储）

### 4. 不追求最强模型
- 好模型就够了
- 设计比模型重要
- 上下文 + 工作流 + 记忆 > 模型

## 选题建议评分

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

## 故障排除

### 问题：TAVILY_API_KEY 未设置
**解决方案**：
```bash
export TAVILY_API_KEY="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"
```

### 问题：SearXNG 连接失败
**解决方案**：
```bash
# 检查 SearXNG 是否运行
curl http://localhost:8080/search?q=test

# 如果没有运行，启动 SearXNG
docker run -p 8080:8080 searxng/searxng
```

### 问题：Twitter API Key 未设置
**解决方案**：
```bash
export TWITTER_API_KEY="your-twitter-api-key"
```

注意：Twitter API Key 是可选的，如果没有设置，将跳过 Twitter 搜索。

### 问题：百度 API Key 未设置
**解决方案**：
```bash
export BAIDU_API_KEY="your-baidu-api-key"
```

注意：百度 API Key 是可选的，如果没有设置，将跳过百度搜索。

### 问题：推送到 Slack 失败
**解决方案**：
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX"
```

### 问题：Python 依赖缺失
**解决方案**：
```bash
pip3 install tavily-python requests python-dotenv
```

## 扩展和定制

### 添加新的搜索源
在 `MultiSourceSearcher` 类中添加新的搜索方法：

```python
def search_new_source(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """使用新的搜索源"""
    # 实现你的搜索逻辑
    pass
```

### 自定义搜索主题
编辑脚本中的 `default_topics` 列表，或使用 `--topics` 参数。

### 修改输出格式
编辑 `format_markdown` 方法，自定义 Markdown 格式。

### 添加新的推送目标
添加新的推送方法，如邮件、Telegram 等。

```python
def push_to_email(self, message: str, email: str) -> bool:
    """推送到邮件"""
    # 实现邮件推送逻辑
    pass
```

## 版本信息

- **版本**: 3.0.0
- **发布日期**: 2026-02-21
- **作者**: Clawdbot Team
- **许可证**: MIT

## 更新日志

### v3.0.0 (2026-02-21)
- ✅ 集成百度搜索
- ✅ 添加中文选题建议（🇨🇳 中文热度高）
- ✅ 更新为 4 个搜索源
- ✅ 添加中文选题导向策略
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
