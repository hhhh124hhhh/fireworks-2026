# Slack 主动消息发送 - 完整指南

## ✅ 已完成的配置

### 1. Slack 频道连接
- ✅ 已连接到频道 `C0ABSK92X4G`
- ✅ 测试消息发送成功

### 2. 定时任务
- ✅ 创建每日报告任务（每天 9:00）
- ✅ 任务 ID: `a99a3a90-af13-4ad1-ba01-2770e3cdd51f`
- ✅ 脚本: `/root/clawd/scripts/collect-and-slack.py`

---

## 🚀 使用方法

### 方法 1: 自动定时（已配置）
每天早上 9 点自动运行并发送报告，无需任何操作。

### 方法 2: 手动运行
```bash
# 立即运行收集并发送报告
python3 /root/clawd/scripts/collect-and-slack.py
```

### 方法 3: 发送自定义消息
```bash
# 发送自定义消息到 Slack
clawdbot message send --channel slack --target C0ABSK92X4G --message "你的消息内容"
```

---

## 📊 报告内容示例

Slack 会收到以下格式的报告：

```
🤖 AI 提示词收集报告 - 2026-01-30 09:00

📊 统计信息
• 新收集: 25 条
• 平均分数: 0.82
• 有完整内容: 20 条

1. 100 Best ChatGPT Prompts for 2026
🔗 https://example.com/chatgpt-prompts
_Learn the most effective ChatGPT prompts for content creation..._

2. Claude Prompt Engineering Guide
🔗 https://example.com/claude-guide
_Master Claude's prompt system with these proven techniques..._

3. Best AI Prompts for Coding
🔗 https://example.com/coding-prompts
_Boost your productivity with these coding-focused AI prompts..._

💾 数据文件: /root/clawd/data/prompts/collected.jsonl
```

---

## ⚙️ 定制配置

### 修改发送时间
```bash
# 删除旧任务
clawdbot cron remove a99a3a90-af13-4ad1-ba01-2770e3cdd51f

# 创建新任务（例如改为每天 10:30）
clawdbot cron add \
  --name "daily-slack-report" \
  --cron "30 10 * * *" \
  --session main \
  --wake next-heartbeat \
  --system-event "运行 /root/clawd/scripts/collect-and-slack.py 发送 AI 提示词收集报告到 Slack"
```

### Cron 表达式示例
- `0 9 * * *` - 每天 9:00
- `0 */6 * * *` - 每 6 小时
- `0 9 * * 1` - 每周一 9:00
- `0 9,15,21 * * *` - 每天 9:00, 15:00, 21:00

### 修改频道
编辑 `/root/clawd/scripts/collect-and-slack.py` 中的频道 ID：
```python
SLACK_CHANNEL_ID = "C0ABSK92X4G"  # 改成你的频道 ID
```

---

## 📈 查看和管理任务

```bash
# 查看所有定时任务
clawdbot cron list

# 查看任务详情
clawdbot cron list | grep daily-slack-report

# 禁用任务
clawdbot cron remove <job-id>

# 手动触发（立即运行一次）
clawdbot cron run a99a3a90-af13-4ad1-ba01-2770e3cdd51f
```

---

## 🔧 故障排查

### 问题：没有收到消息
```bash
# 检查任务是否启用
clawdbot cron list | grep daily-slack-report

# 手动运行脚本测试
python3 /root/clawd/scripts/collect-and-slack.py

# 查看 Clawdbot 日志
clawdbot logs | grep -i slack
```

### 问题：消息格式不对
编辑脚本中的 `format_slack_message()` 函数自定义格式

### 问题：频道 ID 找不到
```bash
# 获取频道列表（需要 bot 权限）
# 查看 clawdbot.json 中的 channels.slack.channels 配置
cat ~/.clawdbot/clawdbot.json | grep -A 10 "slack"
```

---

## 📁 相关文件

- 脚本: `/root/clawd/scripts/collect-and-slack.py`
- 数据: `/root/clawd/data/prompts/collected.jsonl`
- 配置: `~/.clawdbot/clawdbot.json`
- 日志: `~/.clawdbot/cron/jobs.json`

---

## 🎯 下一步

1. ✅ 定时任务已创建，明天 9:00 自动运行
2. 可选：立即测试运行一次
3. 可选：调整报告格式或发送时间
4. 可选：添加更多收集关键词

---

*最后更新: 2026-01-30*
