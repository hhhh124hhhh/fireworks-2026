# Slack 卡顿问题 - 完整解决方案

## 问题现象
- Slack 脚本运行时看起来像"卡死"
- 没有进度反馈
- 等待时间过长

---

## 根本原因

### 1. SearXNG 搜索超时 (主要原因)
```
问题：
- 每次搜索需要启动 Python 子进程
- 搜索引擎（Google, Bing）没有 API key
- 没有超时机制，无限等待

现象：
- 单次搜索耗时 30-90 秒
- 经常超时失败
- 脚本看起来像卡死
```

### 2. Slack API 响应慢 (正常)
```
现实：
- 每次 Slack 发送需要约 10 秒
- 这是 Clawdbot → Slack WebSocket 的正常延迟
- 不算卡顿，是正常的 API 调用时间
```

---

## 解决方案对比

### ✅ 方案 1：快速统计报告（推荐）

**脚本**: `/root/clawd/scripts/quick-report.py`

**特点**:
- ⚡ 秒级响应（~12秒）
- 📊 只统计已有数据，不做搜索
- 🎯 稳定可靠，不会卡顿
- 📱 带进度反馈

**使用**:
```bash
python3 /root/clawd/scripts/quick-report.py
```

**报告内容**:
```
📊 AI 提示词数据报告 - 2026-01-30 08:40

📈 数据统计
• 总数据量: 51 条
• 高质量数据: 20 条
• 独特关键词: 5 个

🔍 热门关键词
• ChatGPT prompts: 15 条
• Claude prompts: 12 条
• AI prompt engineering: 10 条

⭐ 最新 3 条
1. 100 Best ChatGPT Prompts (0.9)
2. Claude Prompt Engineering (0.85)
3. AI Prompt Templates (0.8)

💾 数据文件: `/root/clawd/data/prompts/collected.jsonl`
```

---

### ⚠️ 方案 2：带搜索的完整报告（不推荐）

**问题**:
- SearXNG 搜索不稳定
- 耗时 30-90 秒
- 容易超时

**脚本**: `/root/clawd/scripts/collect-slack-fast.py`

**仅在需要实时搜索时使用**

---

## 定时任务配置

### 当前配置（已更新）
```bash
# 查看任务
clawdbot cron list | grep daily-slack-stats

# 手动触发
clawdbot cron run 10e898a6-481b-4fde-97ed-e9c9449fa9be
```

### 调整发送频率
```bash
# 删除旧任务
clawdbot cron remove 10e898a6-481b-4fde-97ed-e9c9449fa9be

# 创建新任务（例如每 6 小时）
clawdbot cron add \
  --name "slack-stats-6h" \
  --cron "0 */6 * * *" \
  --session main \
  --wake next-heartbeat \
  --system-event "运行 /root/clawd/scripts/quick-report.py"
```

---

## 手动发送（快速）

### 发送统计报告
```bash
python3 /root/clawd/scripts/quick-report.py
```

### 发送详细统计
```bash
python3 /root/clawd/scripts/send-stats.py
```

### 测试 Slack 连接
```bash
python3 /root/clawd/scripts/test-slack.py
```

---

## 性能对比

| 操作 | 耗时 | 推荐度 |
|------|------|--------|
| 快速统计报告 | ~12s | ⭐⭐⭐⭐⭐ |
| 详细统计 | ~12s | ⭐⭐⭐⭐ |
| Slack 测试 | ~10s | ⭐⭐⭐⭐⭐ |
| 带搜索报告 | ~60s+ | ⭐⭐ |
| 完整收集 | ~90s+ | ⭐ |

---

## 如何修复 SearXNG（可选）

如果想使用带搜索的版本，需要：

### 1. 配置搜索引擎 API Keys
编辑 SearXNG 配置文件，添加：
- Google Custom Search API Key
- Bing API Key
- DuckDuckGo（免费，但结果较少）

### 2. 优化引擎选择
只用快速引擎：
```python
params = {"engines": "duckduckgo,wikipedia"}  # 只用免费引擎
```

### 3. 使用本地 HTTP API
直接调用 HTTP 而非 subprocess（已在优化版中实现）

---

## 常见问题

### Q: 为什么需要 10 秒发送消息？
A: 这是 Clawdbot → Slack WebSocket 的正常延迟，不算卡顿。

### Q: 可以让它更快吗？
A: Slack API 限制无法绕过，但可以通过简化报告内容减少几秒。

### Q: 脚本卡住了怎么办？
A:
1. 按 Ctrl+C 终止
2. 使用快速版 `quick-report.py`
3. 检查 Slack 连接状态

### Q: 如何知道脚本在运行？
A: 快速版有进度输出：
```
📊 加载数据... ✓ 51 条
📤 生成报告... ✓
📤 发送 Slack (预计 ~10秒)...✅ 成功
```

---

## 总结

**推荐配置**:
- ✅ 使用 `quick-report.py` 发送统计
- ✅ 每天 9:00 自动运行
- ✅ 避免实时搜索，只统计已有数据

**不推荐**:
- ❌ 使用带搜索的版本（不稳定）
- ❌ 频繁发送 Slack 消息（浪费配额）

**核心原则**: **统计 > 搜索，稳定 > 完整**

---

*最后更新: 2026-01-30*
