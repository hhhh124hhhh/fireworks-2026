# RSS 订阅源推荐清单 (2026)

> 为 Intel Officer 情报收集任务精选的 RSS 订阅源
> 更新时间：2026-03-18
> 分类：国际 AI/科技 + 中文 AI/科技 + 开发者工具

---

## 🌏 国际 AI/科技 RSS (英文)

### 官方实验室 (一手消息)

| 名称 | RSS URL | 更新频率 | 特点 |
|------|---------|----------|------|
| **OpenAI News** | `https://openai.com/news/rss.xml` | 高频 | 官方模型和产品发布 |
| **Google AI Blog** | `https://research.google/blog/rss/` | 高频 | Google AI 研究进展 |
| **Google DeepMind** | `https://deepmind.google/discover/blog/feed/` | 中频 | 深度学习突破 |
| **Hugging Face Blog** | `https://huggingface.co/blog/feed.xml` | 高频 | 模型、工具、生态 |
| **BAIR Blog (Berkeley)** | `https://bair.berkeley.edu/blog/feed.xml` | 中频 | 伯克利 AI 研究 |

### 科技媒体 (深度分析)

| 名称 | RSS URL | 更新频率 | 特点 |
|------|---------|----------|------|
| **The Verge** | `https://www.theverge.com/rss/index.xml` | 30-50 篇/天 | 科技+文化视角 (摘要) |
| **Ars Technica** | `https://feeds.arstechnica.com/arstechnica/index` | 15-25 篇/天 | 深度技术分析 (摘要) |
| **TechCrunch** | `https://techcrunch.com/feed/` | 20-40 篇/天 | 创业融资、产品发布 (全文) |
| **MIT Technology Review AI** | `https://www.technologyreview.com/topic/artificial-intelligence/feed` | 每日 | 编辑分析+政策 |
| **Wired AI** | `https://www.wired.com/feed/tag-ai/rss` | 每日 | AI 社会影响 |

### 研究论文 (学术前沿)

| 名称 | RSS URL | 更新频率 | 特点 |
|------|---------|----------|------|
| **arXiv cs.AI** | `http://arxiv.org/rss/cs.AI` | 极高频 | 原始研究论文 |
| **arXiv cs.LG** | `http://arxiv.org/rss/cs.LG` | 极高频 | 机器学习论文 |
| **arXiv cs.CL** | `http://arxiv.org/rss/cs.CL` | 高频 | 计算语言学 |
| **Google Research** | `https://research.google/blog/rss/` | 高频 | 应用研究 |

### 开发者社区

| 名称 | RSS URL | 更新频率 | 特点 |
|------|---------|----------|------|
| **Hacker News (Front Page)** | `https://hnrss.org/frontpage` | 实时 | 社区精选 |
| **GitHub Blog** | `https://github.blog/feed/` | 每周 | GitHub 产品更新 |
| **Stack Overflow Blog** | `https://stackoverflow.blog/feed/` | 每周 | 开发者趋势 |
| **InfoQ AI** | `https://www.infoq.com/ai/feed/` | 每日 | 企业 AI 应用 |

---

## 🇨🇳 中文 AI/科技 RSS

### 头部 AI 媒体

| 名称 | RSS URL | 更新频率 | 特点 |
|------|---------|----------|------|
| **机器之心** | `https://www.jiqizhixin.com/rss` | 每日 | 专业 AI 自媒体 |
| **量子位** | `https://www.qbitai.com/feed` | 每日 | AI 产业动态 |
| **新智元** | `https://www.jingzhuan.cn/rss` | 每日 | AI 技术+产业 |
| **AI 科技大本营** | `https://blog.csdn.net/github_36364033/rss/list` | 每周 | 技术实战 |

### 科技媒体

| 名称 | RSS URL | 更新频率 | 特点 |
|------|---------|----------|------|
| **36Kr** | `http://feeds.feedburner.com/36kr/motie` | 每日 | 科技创投 |
| **少数派** | `https://sspai.com/feed` | 每日 | 效率工具 |
| **IT 之家** | `https://www.ithome.com/rss/` | 每日 | 科技快讯 |
| **雷锋网** | `https://www.leiphone.com/feed` | 每日 | AI+ 硬件 |

### 开发者技术

| 名称 | RSS URL | 更新频率 | 特点 |
|------|---------|----------|------|
| **美团技术团队** | `https://tech.meituan.com/feed/` | 每周 | 工程实践 |
| **阿里云开发者** | `https://developer.aliyun.com/feed` | 每周 | 云原生+AI |
| **腾讯云开发者** | `https://cloud.tencent.com/developer/column` | 每周 | 技术专栏 |
| **稀土掘金** | `https://juejin.cn/feed` | 每日 | 前端+AI |

---

## 🛠️ 实施建议

### 阶段 1: 核心订阅 (立即实施)

优先订阅 **10 个高价值源**:

```python
CORE_FEEDS = [
    # 官方实验室 (3 个)
    "https://openai.com/news/rss.xml",
    "https://research.google/blog/rss/",
    "https://huggingface.co/blog/feed.xml",
    
    # 科技媒体 (3 个)
    "https://techcrunch.com/feed/",
    "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "https://hnrss.org/frontpage",
    
    # 中文媒体 (4 个)
    "https://www.jiqizhixin.com/rss",
    "https://www.qbitai.com/feed",
    "http://feeds.feedburner.com/36kr/motie",
    "https://sspai.com/feed",
]
```

### 阶段 2: 扩展订阅 (本周)

扩展到 **20-30 个源**,覆盖:
- 更多研究方向 (arXiv 子类别)
- 更多中文媒体 (量子位、新智元、IT 之家)
- 更多开发者社区 (InfoQ、Stack Overflow)

### 阶段 3: 完整订阅 (本月)

完整清单 **50+ 源**,包括:
- 所有官方实验室
- 所有主流科技媒体
- 所有学术 RSS
- 所有开发者社区

---

## 📋 Python 抓取脚本模板

```python
import feedparser
from datetime import datetime
import json

FEEDS = {
    "openai": "https://openai.com/news/rss.xml",
    "google_ai": "https://research.google/blog/rss/",
    "huggingface": "https://huggingface.co/blog/feed.xml",
    "techcrunch": "https://techcrunch.com/feed/",
    "jiqizhixin": "https://www.jiqizhixin.com/rss",
    "qbitai": "https://www.qbitai.com/feed",
    "36kr": "http://feeds.feedburner.com/36kr/motie",
}

def fetch_feeds():
    all_entries = []
    
    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:  # 每个源取 Top10
                all_entries.append({
                    "source": source,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", ""),
                    "summary": entry.get("summary", "")[:500],
                    "fetched_at": datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
    return all_entries

# 执行抓取
entries = fetch_feeds()
print(f"共抓取 {len(entries)} 条内容")

# 保存到 JSON
with open("rss-feed-data.json", "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)
```

---

## 🔧 RSSHub 补充 (社交媒体)

对于不支持 RSS 的平台，使用 RSSHub:

| 平台 | RSSHub URL 示例 |
|------|----------------|
| **知乎热榜** | `https://rsshub.app/zhihu/hotlist` |
| **微博热搜** | `https://rsshub.app/weibo/search/hot` |
| **微信公众号** | `https://rsshub.app/wechat/wasi/[id]` |
| **B 站热门** | `https://rsshub.app/bilibili/ranking/0/1/3` |
| **抖音** | `https://rsshub.app/douyin/hot` |

RSSHub 实例：
- 官方：`https://rsshub.app`
- 自建：部署 Docker 容器

---

## ✅ 下一步行动

1. **创建 RSS 抓取脚本** (`rss-grabber.py`)
2. **添加定时任务** (每天 06:00 执行)
3. **写入飞书多维表格** (原始情报表)
4. **配置去重规则** (避免重复内容)
5. **设置失败告警** (连续失败 3 次通知)

---

## 📊 订阅源选择标准

- ✅ **更新频率**: 至少每周更新
- ✅ **内容质量**: 原创/深度分析优先
- ✅ **RSS 完整性**: 优先全文 RSS
- ✅ **稳定性**: 长期运营，非临时项目
- ✅ **相关性**: AI/科技/开发者相关
- ✅ **可访问性**: 国内可访问 (或可通过代理)

---

*清单持续更新中... 发现优质订阅源欢迎补充*
