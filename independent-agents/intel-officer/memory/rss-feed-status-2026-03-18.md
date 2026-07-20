# RSS 订阅源状态报告 (2026-03-18 测试)

> 测试时间：2026-03-18 07:20-07:30  
> 测试工具：feedparser + requests  
> 测试地点：国内网络环境

---

## ✅ 已验证可用源 (5 个)

| 源 | URL | 状态 | 条数 | 内容类型 | 访问速度 |
|----|-----|------|------|----------|----------|
| **OpenAI** | `https://openai.com/news/rss.xml` | ✅ 200 | 888 条 | application/xml | 快 |
| **TechCrunch** | `https://techcrunch.com/feed/` | ✅ 200 | 20 条 | application/rss+xml | 快 |
| **MIT Tech Review** | `https://www.technologyreview.com/topic/artificial-intelligence/feed` | ✅ 200 | 10 条 | application/rss+xml | 中 |
| **Hacker News** | `https://hnrss.org/frontpage` | ✅ 200 | 20 条 | application/rss+xml | 快 |
| **量子位** | `https://www.qbitai.com/feed` | ✅ 200 | 10 条 | application/rss+xml | 快 |
| **少数派** | `https://sspai.com/feed` | ✅ 200 | - | application/xml | 快 |
| **雷锋网** | `https://www.leiphone.com/feed` | ✅ 200 | - | application/rss+xml | 快 |

**推荐配置:** 前 5 个已测试成功，可立即使用

---

## ❌ 失效/问题源 (4 个)

| 源 | URL | 问题 | 原因 | 替代方案 |
|----|-----|------|------|----------|
| **机器之心** | `https://www.jiqizhixin.com/rss` | ❌ 返回 HTML | RSS 已下线，转为微信公众号 | 使用 RSSHub 或替换为量子位 |
| **Google AI Blog** | `https://research.google/blog/rss/` | ⚠️ 超时 | 国内访问慢 (GFW) | 需要代理或降低优先级 |
| **Hugging Face** | `https://huggingface.co/blog/feed.xml` | ⚠️ 超时 | 国内访问慢 | 需要代理或降低优先级 |
| **36Kr** | `http://feeds.feedburner.com/36kr/motie` | ⚠️ 超时 | feedburner 被墙 | 替换为 IT 桔子或其他 |

---

## 🔧 修复建议

### 方案 1: 使用 RSSHub (推荐)

RSSHub 可以为不支持 RSS 的网站生成 RSS 订阅：

```python
# 机器之心 - 微信公众号
"https://rsshub.app/wechat/wasi/almosthuman2014"

# 36Kr - 直接订阅
"https://rsshub.app/36kr"

# 知乎热榜
"https://rsshub.app/zhihu/hotlist"

# 微博热搜
"https://rsshub.app/weibo/search/hot"
```

RSSHub 实例：
- 官方：`https://rsshub.app`
- 自建：Docker 部署

### 方案 2: 替换为可用源

| 原源 | 替换为 |
|------|--------|
| 机器之心 | 量子位 (已可用) |
| 36Kr | IT 桔子 / 雷锋网 |
| Google AI | 降低优先级 + 重试 |
| Hugging Face | 降低优先级 + 重试 |

### 方案 3: 添加重试 + 超时

```python
import socket
socket.setdefaulttimeout(30)  # 全局 30 秒超时

# 或使用 requests 的 timeout
requests.get(url, timeout=30)
```

---

## 📋 推荐配置 (立即使用)

### 核心订阅源 (5 个，100% 可用)

```python
CORE_FEEDS = {
    # 官方实验室 (1 个)
    "openai": "https://openai.com/news/rss.xml",
    
    # 科技媒体 (3 个)
    "techcrunch": "https://techcrunch.com/feed/",
    "mit_tech_review": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "hacker_news": "https://hnrss.org/frontpage",
    
    # 中文媒体 (1 个)
    "qbitai": "https://www.qbitai.com/feed",
}
```

### 扩展订阅源 (+3 个)

```python
EXTENDED_FEEDS = {
    # 中文媒体 (2 个)
    "sspai": "https://sspai.com/feed",
    "leiphone": "https://www.leiphone.com/feed",
    
    # 社交媒体 (1 个，通过 RSSHub)
    "zhihu_hot": "https://rsshub.app/zhihu/hotlist",
}
```

---

## 📊 抓取内容示例

### OpenAI (最新 3 条)
1. **Introducing GPT-5.4 mini and nano**
   - 发布时间：2026-03-17
   - 摘要：GPT-5.4 mini and nano are smaller, faster versions optimized for coding...

2. **Equipping workers with insights about compensation**
   - 发布时间：2026-03-17
   - 摘要：New research shows Americans send nearly 3 million daily messages to ChatGPT...

3. **Why Codex Security Doesn't Include a SAST Report**
   - 发布时间：2026-03-16
   - 摘要：A deep dive into why Codex Security doesn't rely on traditional SAST...

### 量子位 (最新 3 条)
1. **北京养虾 er！明晚 19 点，为你带来 9+ 场养虾干货 Talk**
   - 发布时间：2026-03-17 13:56
   - 摘要：从用法到应用场景，全流程干货分享

2. **黄仁勋：龙虾就是新操作系统！英伟达 7 种芯片拼出算力怪兽**
   - 发布时间：2026-03-17 13:08
   - 摘要：所有人都在等老黄掏出新芯片，但他没有掏...

3. **从"养虾热"到实体交互：元萝卜推动 OpenClaw 走向真实世界**
   - 发布时间：2026-03-17 12:12
   - 摘要：元萝卜让"桌面智能体"有了现实参照

### TechCrunch (最新 3 条)
1. **Kalshi's legal troubles pile up, as Arizona files first ever criminal charges**
   - 发布时间：2026-03-17 21:39
   - 摘要：It's the latest salvo in an escalating battle between state regulators...

2. **Mistral bets on 'build-your-own AI' as it takes on OpenAI, Anthropic**
   - 发布时间：2026-03-17 21:00
   - 摘要：Mistral Forge lets enterprises train custom AI models from scratch...

3. **Why Garry Tan's Claude Code setup has gotten so much love, and hate**
   - 发布时间：2026-03-17 20:50
   - 摘要：Thousands of people are trying Garry Tan's Claude Code setup...

---

## 🛠️ 下一步行动

### 立即执行
1. ✅ 使用 5 个核心源配置脚本
2. ⏳ 创建定时任务 (每天 06:00)
3. ⏳ 集成飞书写入

### 本周优化
1. 添加 RSSHub 支持 (机器之心，36Kr)
2. 添加重试逻辑 (Google AI, Hugging Face)
3. 扩展到 10 个源

### 监控告警
- 连续失败 3 次 → 飞书通知
- 源失效检测 → 每周检查

---

*报告生成时间：2026-03-18 07:30*  
*下次检查：2026-03-25*
