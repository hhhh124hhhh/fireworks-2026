# 多源 AI 提示词收集系统

## 🎯 目标

解决 Twitter API 额度问题，集成多个数据源收集 AI 提示词。

---

## 📱 数据源列表

### 1. Reddit r/prompts
- **URL**: https://www.reddit.com/r/prompts
- **类型**: 社区分享的 prompt
- **频率**: 高频更新
- **优势**: 质量高，有评分系统
- **API**: Reddit API（免费）

### 2. GitHub Awesome Prompts
- **URL**: https://github.com/f/awesome-chatgpt-prompts
- **类型**: 精选 prompt 列表
- **频率**: 定期更新
- **优势**: 经过筛选，质量保证
- **API**: GitHub API（免费）

### 3. Hacker News
- **URL**: https://hn.algolia.com/api
- **类型**: AI 相关讨论
- **频率**: 持续更新
- **优势**: 技术社区，讨论质量高
- **API**: Algolia API（免费）

### 4. Product Hunt
- **URL**: https://www.producthunt.com
- **类型**: AI 产品和工具
- **频率**: 每日更新
- **优势**: 最新 AI 工具，含 prompt
- **API**: Product Hunt API

### 5. arXiv AI 论文
- **URL**: https://arxiv.org
- **类型**: 学术论文
- **频率**: 持续更新
- **优势**: 学术研究，理论支持
- **API**: arXiv API（免费）

### 6. Medium 文章
- **URL**: https://medium.com/tag/artificial-intelligence
- **类型**: AI 文章和教程
- **频率**: 高频更新
- **优势**: 实战经验，教程详细
- **API**: Medium API 或 RSS

### 7. Dev.to
- **URL**: https://dev.to/t/artificialintelligence
- **类型**: 开发者文章
- **频率**: 高频更新
- **优势**: 开发者社区，代码多
- **API**: Dev.to API（免费）

### 8. SearXNG（已配置）
- **URL**: http://149.13.91.232:8080
- **类型**: 元搜索引擎
- **频率**: 按需搜索
- **优势**: 隐私，无 API 限制
- **状态**: ✅ 已集成

---

## 🚀 实施计划

### 阶段 1：Reddit 集成（优先）

**优势**：
- 大量高质量 prompt
- 免费且稳定的 API
- 有评分和评论系统

**预计收集量**: 100-200 条/天

### 阶段 2：GitHub Awesome

**优势**：
- 精选列表
- 质量保证
- 可定期更新

**预计收集量**: 50-100 条/周

### 阶段 3：Hacker News

**优势**：
- AI 相关讨论
- 技术社区
- 实时更新

**预计收集量**: 20-50 条/天

### 阶段 4：其他源

根据前三阶段效果，决定是否集成其他源。

---

## 💡 数据源对比

| 数据源 | 免费 | API 频度 | 质量 | 更新频率 | 推荐度 |
|--------|------|----------|------|----------|--------|
| Reddit r/prompts | ✅ | 高 | ⭐⭐⭐⭐⭐ | 实时 | ⭐⭐⭐⭐⭐ |
| GitHub Awesome | ✅ | 高 | ⭐⭐⭐⭐⭐ | 每周 | ⭐⭐⭐⭐⭐ |
| Hacker News | ✅ | 高 | ⭐⭐⭐⭐ | 实时 | ⭐⭐⭐⭐ |
| Product Hunt | ❌ | 中 | ⭐⭐⭐ | 每日 | ⭐⭐⭐ |
| arXiv | ✅ | 高 | ⭐⭐⭐⭐ | 每周 | ⭐⭐⭐⭐ |
| Medium | ✅ | 中 | ⭐⭐⭐ | 每日 | ⭐⭐⭐ |
| Dev.to | ✅ | 高 | ⭐⭐⭐⭐ | 每日 | ⭐⭐⭐⭐ |
| SearXNG | ✅ | 无限制 | ⭐⭐⭐ | 按需 | ⭐⭐⭐⭐ |

---

## 🔧 技术实现

### 统一数据格式

```json
{
  "source": "reddit",
  "source_id": "post_id",
  "title": "Prompt Title",
  "content": "Full prompt content",
  "url": "https://reddit.com/...",
  "author": "username",
  "metrics": {
    "upvotes": 100,
    "comments": 50,
    "created_at": "2026-01-30T..."
  },
  "tags": ["prompt", "chatgpt", "coding"],
  "quality_score": 85,
  "collected_at": "2026-01-30T15:00:00Z"
}
```

### 去重策略

- 基于 URL 的唯一标识
- 跨源去重（同一内容不同源）
- 内容相似度检测（可选）

---

## 📊 预期效果

### 集成前（仅 Twitter）

| 指标 | 数值 |
|------|------|
| 数据源 | 1 个（API 受限） |
| 日收集量 | 0-50 条（当前 0） |
| 数据质量 | ⭐⭐⭐⭐（但停滞） |

### 集成后（Reddit + GitHub + HN）

| 指标 | 数值 |
|------|------|
| 数据源 | 3+ 个（无限制） |
| 日收集量 | 150-300 条 |
| 数据质量 | ⭐⭐⭐⭐⭐ |

**提升**：
- 数据源：**+200%**
- 日收集量：**+400%**
- 稳定性：**无 API 限制**

---

## 🎯 下一步

1. ✅ 确认数据源列表
2. 🔧 开始集成 Reddit（优先）
3. 🧪 测试收集和质量评估
4. 📊 对比各源质量
5. 🚀 集成其他源

---

*最后更新: 2026-01-30*
