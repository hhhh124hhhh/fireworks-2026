# rss-grabber - RSS 订阅源抓取技能 (支持中英翻译)

> 版本：v2.0  
> 作者：Intel Officer  
> 日期：2026-03-18

---

## 📖 描述

自动抓取 AI/科技领域 RSS 订阅源，支持**中英文自动翻译**、重试逻辑、飞书多维表格自动写入、失败告警。

**核心功能:**
- ✅ RSS 自动抓取 (5-8 个源)
- ✅ **智能中英翻译** (自动检测语言)
- ✅ **双语显示** (中文 + 英文对照)
- ✅ 智能重试 (3 次 + 指数退避)
- ✅ 飞书多维表格自动写入
- ✅ 失败告警系统
- ✅ 数据去重

---

## 🌟 新增功能 (v2.0)

### 中英文自动翻译

**自动检测:**
- 英文内容 → 自动翻译为中文
- 中文内容 → 保持原文
- 混合内容 → 智能判断

**显示方式:**
```
标题：Introducing GPT-5.4 mini and nano
标题 (英文): Introducing GPT-5.4 mini and nano

原文内容：GPT-5.4 mini and nano are smaller...
原文内容 (英文): GPT-5.4 mini and nano are smaller...

是否翻译：是
```

**飞书字段:**
- `标题` - 中文翻译 (或原文)
- `标题 (英文)` - 英文原标题
- `原文内容` - 中文翻译 (或原文)
- `原文内容 (英文)` - 英文原内容
- `是否翻译` - 是/否

---

## 🚀 快速开始

### 方式 1: 命令行

```bash
# 核心模式 (5 个源)
python skills/rss-grabber/grabber.py --mode core --limit 10

# 扩展模式 (8 个源)
python skills/rss-grabber/grabber.py --mode extended --limit 5

# 带飞书写入
python skills/rss-grabber/grabber.py --mode core --limit 10 --feishu
```

### 方式 2: Python 调用

```python
from skills.rss_grabber.grabber import RSSGrabber

grabber = RSSGrabber()
entries, results = grabber.fetch_all(mode="core", limit=10)
grabber.save_to_feishu(entries, table_id="raw")
```

### 方式 3: MCP 工具

```python
# 使用 mcp_rss_grab 工具
mcp_rss_grab(mode="core", limit=10, feishu=True)
```

---

## 📋 配置

### 订阅源配置

**核心源 (5 个，100% 可用):**
```python
CORE_FEEDS = {
    "openai": "https://openai.com/news/rss.xml",
    "techcrunch": "https://techcrunch.com/feed/",
    "mit_tech_review": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "hacker_news": "https://hnrss.org/frontpage",
    "qbitai": "https://www.qbitai.com/feed",
}
```

**扩展源 (3 个):**
```python
EXTENDED_FEEDS = {
    "sspai": "https://sspai.com/feed",
    "leiphone": "https://www.leiphone.com/feed",
    "zhihu_hot": "https://rsshub.app/zhihu/hotlist",
}
```

### 飞书配置

```python
FEISHU_CONFIG = {
    "app_token": "DTt9bx9gka7UW6s52ndcdnLCnDe",
    "table_id_raw": "tbl97RKEz1h5uHJX",      # 原始情报表
    "table_id_clean": "tblnpKvIOTZ6sZNt",   # 清洗情报表
}
```

### 重试配置

```python
RETRY_CONFIG = {
    "max_attempts": 3,    # 最多重试 3 次
    "backoff": 2,         # 指数退避倍数
    "timeout": 30,        # 超时时间 (秒)
}
```

### 告警配置

```python
ALERT_CONFIG = {
    "max_failures": 3,     # 连续失败 3 次告警
    "feishu_user": "ou_c1f49efdd595b46e212560e66abc7205",
}
```

---

## 🔧 使用方法

### 1. 基础抓取

```python
from skills.rss_grabber.grabber import RSSGrabber

grabber = RSSGrabber()

# 抓取核心源
entries, results = grabber.fetch_all(mode="core", limit=10)

# 查看结果
print(f"成功：{sum(1 for r in results if r.success)}/{len(results)}")
print(f"总条目：{len(entries)}")
```

### 2. 飞书写入

```python
# 写入原始情报表
success = grabber.save_to_feishu(entries, table_id="raw")

# 写入清洗情报表
success = grabber.save_to_feishu(entries, table_id="clean")
```

### 3. 完整流程

```python
from skills.rss_grabber.grabber import RSSGrabber

grabber = RSSGrabber()

# 1. 抓取
entries, results = grabber.fetch_all(mode="core", limit=10)

# 2. 保存本地文件
json_path = grabber.save_to_json(entries)
md_path = grabber.save_to_markdown(entries)

# 3. 写入飞书
feishu_path = grabber.save_to_feishu(entries, table_id="raw")

# 4. 检查告警
alert = grabber.check_failures(results)
if alert:
    grabber.send_alert(alert)

# 5. 返回报告
return {
    "success": True,
    "entries": len(entries),
    "failed": len([r for r in results if not r.success]),
    "files": [json_path, md_path, feishu_path]
}
```

---

## 📊 输出格式

### 飞书多维表格字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 采集轮次 | 文本 | 唯一记录 ID (用于去重) |
| 采集时间 | 文本 | ISO 8601 格式时间戳 |
| 搜索关键词 | 文本 | RSS:源名称 |
| 信息源 | 文本 | 来源标识 (openai/techcrunch 等) |
| 标题 | 文本 | 文章标题 (最多 200 字) |
| 原文内容 | 长文本 | 文章摘要/内容 (最多 2000 字) |
| 原文链接 | 超链接 | 文章 URL |
| 发布时间 | 文本 | ISO 8601 格式 |
| 作者 | 文本 | 作者姓名 |

### 本地文件

**JSON 文件:** `skills/rss-grabber/output/rss-feed-YYYYMMDD-HHMMSS.json`

**Markdown 文件:** `skills/rss-grabber/output/rss-feed-YYYYMMDD-HHMMSS.md`

**告警文件:** `skills/rss-grabber/output/rss-alert-YYYYMMDD-HHMMSS.json`

---

## 🛠️ 故障排除

### 1. 飞书写入失败

**错误:** `Permission denied`

**解决:**
- 检查飞书 OAuth 权限
- 确认多维表格共享权限
- 验证 app_token 和 table_id

### 2. RSS 源超时

**错误:** `Connection timeout`

**解决:**
- 检查网络连接
- 增加超时时间：`RETRY_CONFIG["timeout"] = 60`
- 使用代理或降低优先级

### 3. 解析错误

**错误:** `RSS parse error`

**解决:**
- 检查 RSS URL 是否正确
- 验证 RSS 格式 (使用在线验证工具)
- 替换为可用源

---

## 📈 监控指标

### 关键指标

| 指标 | 目标 | 告警 |
|------|------|------|
| 成功率 | ≥ 95% | < 80% |
| 平均耗时 | < 500ms/源 | > 2000ms/源 |
| 数据量 | 50 条/次 | < 30 条/次 |
| 告警频率 | < 1 次/周 | > 3 次/周 |

### 日志查看

```bash
# 查看最新抓取结果
ls -lt skills/rss-grabber/output/rss-feed-*.json | head -5

# 查看告警
cat skills/rss-grabber/output/rss-alert-*.json | jq .

# 查看飞书写入状态
cat skills/rss-grabber/output/rss-feishu-*.json | jq '. | length'
```

---

## 🔗 相关文档

- [RSS 订阅源状态报告](../../memory/rss-feed-status-2026-03-18.md)
- [RSS 飞书集成指南](../../memory/rss-feishu-integration.md)
- [RSS 订阅源推荐清单](../../memory/rss-feeds-recommendations.md)

---

## 📝 更新日志

### v1.0 (2026-03-18)
- ✅ 初始版本
- ✅ 支持 5 个核心源 + 3 个扩展源
- ✅ 智能重试逻辑
- ✅ 飞书多维表格自动写入
- ✅ 失败告警系统
- ✅ 本地文件保存 (JSON + MD)

---

*Skill 版本：v1.0*  
*最后更新：2026-03-18*
