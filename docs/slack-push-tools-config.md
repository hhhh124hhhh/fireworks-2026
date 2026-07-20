# Slack 推送工具配置

## 工具列表

### 1. md-to-slack.sh - MD 转 Slack 格式化文本

**位置**: `/root/clawd/scripts/md-to-slack.sh`

**功能**: 将 Markdown 文件转换为 Slack 友好的格式化文本

**模式**:
- `summary` - 推送摘要（前 100 行）
- `full` - 推送完整内容（分批）
- `tag` - 推送指定部分（使用标签）

**使用示例**:
```bash
# 查看今天的记忆（摘要）
bash /root/clawd/scripts/md-to-slack.sh /root/clawd/memory/2026-02-10.md summary

# 查看上下文溢出方案（摘要）
bash /root/clawd/scripts/md-to-slack.sh /root/clawd/memory/context-overflow-solution.md summary

# 查看最佳实践文档（摘要）
bash /root/clawd/scripts/md-to-slack.sh /root/clawd/docs/ai-content-creator-best-practices.md summary

# 查看完整内容（分批推送）
bash /root/clawd/scripts/md-to-slack.sh /root/clawd/memory/2026-02-10.md full

# 查看指定标签
bash /root/clawd/scripts/md-to-slack.sh /root/clawd/memory/2026-02-10.md tag 任务清单
```

---

### 2. summary-to-slack.sh - 自动摘要推送

**位置**: `/root/clawd/scripts/summary-to-slack.sh`

**功能**: 每天自动推送任务清单、进度总结、明日计划

**模式**:
- `morning` - 推送任务清单（早上 9:00）
- `evening` - 推送进度总结（晚上 18:00）
- `night` - 推送明日计划（晚上 22:00）
- `all` - 推送所有

**使用示例**:
```bash
# 早上 9:00 推送任务清单
bash /root/clawd/scripts/summary-to-slack.sh morning

# 晚上 18:00 推送进度总结
bash /root/clawd/scripts/summary-to-slack.sh evening

# 晚上 22:00 推送明日计划
bash /root/clawd/scripts/summary-to-slack.sh night

# 推送所有
bash /root/clawd/scripts/summary-to-slack.sh all
```

---

## Cron 配置（可选）

如果需要自动推送，可以添加以下 Crontab 任务：

```bash
# 编辑 crontab
crontab -e

# 添加以下内容
# 早上 9:00 推送任务清单
0 9 * * * bash /root/clawd/scripts/summary-to-slack.sh morning > /tmp/summary-morning.log 2>&1

# 晚上 18:00 推送进度总结
0 18 * * * bash /root/clawd/scripts/summary-to-slack.sh evening > /tmp/summary-evening.log 2>&1

# 晚上 22:00 推送明日计划
0 22 * * * bash /root/clawd/scripts/summary-to-slack.sh night > /tmp/summary-night.log 2>&1
```

---

## 重要文件路径

### 记忆文件
- 今日记忆: `/root/clawd/memory/2026-02-10.md`
- 上下文溢出方案: `/root/clawd/memory/context-overflow-solution.md`
- 长期记忆: `/root/clawd/MEMORY.md`

### 文档文件
- AI Content Creator 最佳实践: `/root/clawd/docs/ai-content-creator-best-practices.md`
- AI Content Creator 每日总结: `/root/clawd/docs/ai-content-creator-daily-summary-2026-02-09.md`

### 脚本文件
- MD 转 Slack: `/root/clawd/scripts/md-to-slack.sh`
- 摘要推送: `/root/clawd/scripts/summary-to-slack.sh`
- 上下文清理: `/root/clawd/scripts/backup-and-flush-memory.sh`

---

## Slack 配置

- **频道**: #clawdbot (C0ABSK92X4G)
- **Feishu**: 已配置（待确认 Webhook）

---

## 常见问题

### Q1: 如何查看服务器的 MD 文件？

A: 使用 `md-to-slack.sh` 工具：
```bash
bash /root/clawd/scripts/md-to-slack.sh /root/clawd/memory/2026-02-10.md summary
```

### Q2: 如何获取任务清单？

A: 使用 `summary-to-slack.sh` 工具：
```bash
bash /root/clawd/scripts/summary-to-slack.sh morning
```

### Q3: 如何查看今日进度？

A: 使用 `summary-to-slack.sh` 工具：
```bash
bash /root/clawd/scripts/summary-to-slack.sh evening
```

### Q4: 如何自动推送？

A: 配置 Cron 任务，见上方的 Cron 配置部分。

---

## 快速参考

| 命令 | 说明 |
|------|------|
| `md-to-slack.sh file.md summary` | 查看 MD 文件摘要 |
| `md-to-slack.sh file.md full` | 查看 MD 文件完整内容 |
| `md-to-slack.sh file.md tag 标签名` | 查看指定标签内容 |
| `summary-to-slack.sh morning` | 推送任务清单 |
| `summary-to-slack.sh evening` | 推送进度总结 |
| `summary-to-slack.sh night` | 推送明日计划 |
| `summary-to-slack.sh all` | 推送所有 |

---

## 注意事项

1. **长度限制**: Slack 消息长度限制约 4000 字符，长文件会自动分批推送
2. **格式转换**: MD 格式会转换为 Slack 友好格式，但某些复杂格式可能不完全保留
3. **标签格式**: 使用 `## 标签名` 格式的标签，`tag` 模式才能正确提取

---

## 更新记录

- 2026-02-10: 创建工具并测试成功
- 2026-02-10: 配置文档完成
