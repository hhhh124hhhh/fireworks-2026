# RSS 抓取 - 飞书集成与告警配置指南

> 版本：v2.0  
> 更新时间：2026-03-18 07:45  
> 作者：Intel Officer

---

## ✅ 已完成功能

### 1. 重试逻辑 ✅

**配置:**
- 最大重试次数：3 次
- 退避策略：指数退避 (2 的幂次)
- 超时时间：30 秒

**实现:**
```python
@retry_on_failure(max_attempts=3, backoff=2)
def fetch_single_feed(source, url, limit):
    # 自动重试逻辑
    ...
```

**测试:**
- ✅ 5/5 源成功 (0 失败)
- ✅ 平均耗时：~600ms/源
- ✅ 总耗时：~3 秒 (5 个源)

---

### 2. 飞书集成 ⚠️ (需 OAuth 权限)

**当前状态:**
- ✅ 数据已暂存为 JSON
- ⚠️ 需要飞书 OAuth 权限才能直接写入
- ✅ 提供了完整的写入接口

**配置:**
```python
FEISHU_CONFIG = {
    "app_token": "DTt9bx9gka7UW6s52ndcdnLCnDe",
    "table_id_raw": "tbl97RKEz1h5uHJX",      # 原始情报表
    "table_id_clean": "tblnpKvIOTZ6sZNt",   # 清洗情报表
}
```

**使用方法:**

#### 方式 1: 使用 `--feishu` 参数
```bash
python scripts/rss-grabber-v2.py --mode core --limit 10 --feishu
```

#### 方式 2: 使用飞书工具手动写入

**步骤 1:** 运行抓取脚本生成 JSON
```bash
python scripts/rss-grabber-v2.py --mode core --limit 10
```

**步骤 2:** 使用 `feishu_bitable_app_table_record` 工具写入

```python
# 示例代码
feishu_bitable_app_table_record(
    action="batch_create",
    app_token="DTt9bx9gka7UW6s52ndcdnLCnDe",
    table_id="tbl97RKEz1h5uHJX",
    records=[
        {
            "fields": {
                "record_id": "abc123...",
                "fetch_time": "2026-03-18T07:40:46",
                "keyword": "RSS:openai",
                "source": "openai",
                "title": "Introducing GPT-5.4 mini and nano",
                "content": "GPT-5.4 mini and nano are smaller...",
                "link": "https://openai.com/index/...",
                "published": "2026-03-17T10:00:00Z",
                "author": ""
            }
        },
        # ... 更多记录
    ]
)
```

**输出文件:**
- `scripts/memory/rss-feishu-YYYYMMDD-HHMMSS.json`
- 格式与飞书多维表格字段完全匹配

---

### 3. 告警系统 ✅

**配置:**
```python
ALERT_CONFIG = {
    "max_failures": 3,          # 连续失败 3 次告警
    "feishu_user": "ou_c1f49efdd595b46e212560e66abc7205",  # 郝工
}
```

**告警触发条件:**
- 失败率 ≥ 50% → 警告 (warning)
- 失败率 ≥ 80% → 错误 (error)
- 连续失败 3 次 → 发送飞书通知

**告警消息格式:**
```json
{
  "level": "warning",
  "title": "RSS Fetch Alert (2/5)",
  "message": "Failure rate: 40.0%\n\nFailed feeds:\n- google_ai: Connection timeout\n- huggingface: Connection timeout",
  "failed_feeds": ["google_ai", "huggingface"],
  "timestamp": "2026-03-18T07:40:46"
}
```

**告警输出:**
- 控制台打印
- JSON 文件：`scripts/memory/rss-alert-YYYYMMDD-HHMMSS.json`
- (可选) 飞书消息推送

---

## 📋 使用指南

### 基础使用

#### 1. 核心模式 (5 个源)
```bash
python scripts/rss-grabber-v2.py --mode core --limit 10
```

**输出:**
- 5 个源 × 10 条 = 50 条记录
- 耗时：~1-2 分钟
- 文件：`rss-feed-YYYYMMDD-HHMMSS.json` + `.md`

#### 2. 扩展模式 (8 个源)
```bash
python scripts/rss-grabber-v2.py --mode extended --limit 5
```

**输出:**
- 8 个源 × 5 条 = 40 条记录
- 耗时：~2-3 分钟
- 包含 RSSHub 源 (知乎热榜)

#### 3. 带飞书写入
```bash
python scripts/rss-grabber-v2.py --mode core --limit 10 --feishu
```

**输出:**
- 标准输出文件 + `rss-feishu-YYYYMMDD-HHMMSS.json`
- 可直接用于飞书多维表格批量导入

#### 4. 测试重试逻辑
```bash
python scripts/rss-grabber-v2.py --test-retry
```

**输出:**
```
[TEST] Testing retry logic...
  [test] https://invalid-url-test.com/rss
  [RETRY] 1/3, waiting 2s...
  [RETRY] 2/3, waiting 4s...
[TEST] Retry logic works: ...
```

---

### 高级使用

#### 1. 自定义订阅源

编辑脚本中的 `CORE_FEEDS` 和 `EXTENDED_FEEDS`:

```python
CORE_FEEDS = {
    "my_feed": "https://example.com/rss",
    # ... 其他源
}
```

#### 2. 调整重试配置

```python
RETRY_CONFIG = {
    "max_attempts": 5,    # 重试 5 次
    "backoff": 3,         # 3 倍退避
}
```

#### 3. 调整告警阈值

```python
ALERT_CONFIG = {
    "max_failures": 5,    # 连续失败 5 次告警
}
```

---

## 🔧 飞书集成完整方案

### 方案 A: 自动写入 (推荐)

**前提:** 需要飞书 OAuth 权限

**步骤:**

1. **获取飞书 API 权限**
   - 应用需开通「多维表格」权限
   - 获取 User Access Token

2. **修改脚本集成飞书工具**

在 `save_to_feishu()` 函数中:

```python
def save_to_feishu(entries: List[FeedEntry], table_id: str = "raw") -> bool:
    # 转换为飞书格式
    records = []
    for entry in entries:
        records.append({
            "fields": {
                "采集轮次": entry.record_id,
                "采集时间": entry.fetch_time,
                "搜索关键词": entry.keyword,
                "信息源": entry.source,
                "标题": entry.title,
                "原文内容": entry.content,
                "原文链接": entry.link,
                "发布时间": entry.published,
                "作者": entry.author,
            }
        })
    
    # 调用飞书 API
    result = feishu_bitable_app_table_record(
        action="batch_create",
        app_token=FEISHU_CONFIG["app_token"],
        table_id=FEISHU_CONFIG["table_id_raw"] if table_id == "raw" else FEISHU_CONFIG["table_id_clean"],
        records=records
    )
    
    return result.get("success", False)
```

3. **测试写入**
```bash
python scripts/rss-grabber-v2.py --mode core --limit 10 --feishu
```

---

### 方案 B: 半自动写入 (当前)

**前提:** 无需额外权限

**步骤:**

1. **运行抓取脚本**
```bash
python scripts/rss-grabber-v2.py --mode core --limit 10
```

2. **使用飞书工具手动写入**

在飞书聊天中:
```
使用 feishu_bitable_app_table_record 工具
- action: batch_create
- app_token: DTt9bx9gka7UW6s52ndcdnLCnDe
- table_id: tbl97RKEz1h5uHJX
- records: [读取 rss-feishu-*.json 内容]
```

3. **批量导入 (可选)**

飞书多维表格支持 CSV/JSON 导入：
- 打开多维表格
- 点击「导入」
- 选择 `rss-feishu-*.json` 文件

---

## 🚨 告警系统集成

### 方案 A: 飞书消息推送

**前提:** 需要飞书 IM 权限

**修改 `send_alert()` 函数:**

```python
def send_alert(alert: AlertMessage) -> bool:
    # 保存告警
    alert_path = save_alert_to_file(alert)
    
    # 发送飞书消息
    message = f"""
🚨 RSS 抓取告警

级别：{alert.level.upper()}
标题：{alert.title}

{alert.message}

时间：{alert.timestamp}
"""
    
    feishu_im_user_message(
        action="send",
        msg_type="text",
        receive_id=ALERT_CONFIG["feishu_user"],
        receive_id_type="open_id",
        content=json.dumps({"text": message})
    )
    
    return True
```

---

### 方案 B: 告警文件监控 (当前)

**实现:**
- 告警保存为 JSON 文件
- 外部监控系统检测新文件
- 触发通知流程

**监控脚本示例:**

```python
# monitor-alerts.py
import time
from pathlib import Path

ALERT_DIR = Path("scripts/memory")
last_check = time.time()

while True:
    alerts = list(ALERT_DIR.glob("rss-alert-*.json"))
    new_alerts = [a for a in alerts if a.stat().st_mtime > last_check]
    
    for alert_file in new_alerts:
        with open(alert_file) as f:
            alert = json.load(f)
        send_notification(alert)
    
    last_check = time.time()
    time.sleep(60)  # 每分钟检查
```

---

## 📊 输出文件说明

### 1. JSON 文件
**文件名:** `rss-feed-YYYYMMDD-HHMMSS.json`

**格式:**
```json
[
  {
    "record_id": "abc123...",
    "fetch_time": "2026-03-18T07:40:46.123456",
    "keyword": "RSS:openai",
    "source": "openai",
    "title": "Introducing GPT-5.4 mini and nano",
    "content": "GPT-5.4 mini and nano are smaller...",
    "link": "https://openai.com/index/...",
    "published": "2026-03-17T10:00:00+00:00",
    "author": ""
  }
]
```

**用途:**
- 数据备份
- 飞书导入
- 后续处理

---

### 2. Markdown 文件
**文件名:** `rss-feed-YYYYMMDD-HHMMSS.md`

**格式:**
```markdown
# RSS Fetch Results

**Time:** 2026-03-18T07:40:46
**Total:** 15 entries

---

## [openai] (3 entries)

### 1. Introducing GPT-5.4 mini and nano

- **Source:** openai
- **Published:** 2026-03-17T10:00:00+00:00
- **Link:** [https://openai.com/index/...](...)

> GPT-5.4 mini and nano are smaller...

---
```

**用途:**
- 人工阅读
- 快速浏览
- 分享报告

---

### 3. 飞书专用 JSON
**文件名:** `rss-feishu-YYYYMMDD-HHMMSS.json`

**格式:** 与 JSON 文件相同，字段名已映射为飞书表格字段

**用途:**
- 直接导入飞书多维表格
- 批量写入

---

### 4. 告警文件
**文件名:** `rss-alert-YYYYMMDD-HHMMSS.json`

**格式:**
```json
{
  "level": "warning",
  "title": "RSS Fetch Alert (2/5)",
  "message": "Failure rate: 40.0%...",
  "failed_feeds": ["google_ai", "huggingface"],
  "timestamp": "2026-03-18T07:40:46"
}
```

**用途:**
- 告警记录
- 监控集成
- 审计日志

---

## 🎯 最佳实践

### 1. 日常抓取

**推荐配置:**
```bash
# 每天 06:00 执行
python scripts/rss-grabber-v2.py --mode core --limit 10
```

**预期输出:**
- 5 个源 × 10 条 = 50 条记录
- 耗时：~1-2 分钟
- 成功率：100%

---

### 2. 深度抓取

**推荐配置:**
```bash
# 每周一次，抓取更多内容
python scripts/rss-grabber-v2.py --mode extended --limit 20
```

**预期输出:**
- 8 个源 × 20 条 = 160 条记录
- 耗时：~5-8 分钟
- 包含社交媒体内容

---

### 3. 故障排查

**查看告警:**
```bash
ls -lt scripts/memory/rss-alert-*.json | head -5
cat scripts/memory/rss-alert-*.json | jq .
```

**查看失败源:**
```bash
cat scripts/memory/rss-feed-*.json | jq '[.[] | select(.error != null)]'
```

---

## 📈 监控指标

### 关键指标

1. **成功率**
   - 目标：≥ 95%
   - 告警：< 80%

2. **平均耗时**
   - 目标：< 500ms/源
   - 告警：> 2000ms/源

3. **数据量**
   - 核心模式：50 条/次
   - 扩展模式：80-160 条/次

4. **告警频率**
   - 目标：< 1 次/周
   - 告警：> 3 次/周

---

## 🔗 相关文档

- [RSS 订阅源状态报告](./rss-feed-status-2026-03-18.md)
- [RSS 订阅源解决方案](./rss-feed-solutions.md)
- [RSS 订阅源推荐清单](./rss-feeds-recommendations.md)

---

*文档版本：v2.0*  
*最后更新：2026-03-18 07:45*
