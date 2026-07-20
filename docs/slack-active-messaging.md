# Slack 主动消息发送方案

## 方案 1: 使用 Slack Webhook（推荐）

### 1. 创建 Slack Incoming Webhook

1. 访问 https://api.slack.com/apps
2. 创建新应用 → "Incoming Webhooks"
3. 激活 Incoming Webhooks
4. 添加新 Webhook，选择目标频道
5. 复制 Webhook URL

### 2. 配置环境变量

```bash
# 临时设置（当前会话）
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 使用增强版脚本

```bash
# 运行带 Slack 通知的收集脚本
python3 /root/clawd/scripts/collect-prompts-with-slack.py
```

### 4. 设置定时任务

```bash
# 编辑 crontab
crontab -e

# 每天早上 9 点运行
0 9 * * * export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL" && /usr/bin/python3 /root/clawd/scripts/collect-prompts-with-slack.py >> /root/clawd/logs/prompts-collect.log 2>&1
```

---

## 方案 2: 使用 Clawdbot Message Tool

如果你已经配置了 Slack channel，可以在收集后调用 Clawdbot 发送消息：

### 创建通知脚本

```bash
#!/bin/bash
# /root/clawd/scripts/collect-and-notify.sh

# 1. 运行收集脚本
python3 /root/clawd/scripts/collect-prompts-test.py

# 2. 发送 Slack 通知
# 需要先配置 Slack channel
clawdbot message send --channel slack --message "✅ AI 提示词收集完成！数据已保存到 /root/clawd/data/prompts/collected.jsonl"
```

---

## 方案 3: 使用 Cron Job（内置）

使用 Clawdbot 的 cron 系统设置定时提醒：

```bash
# 添加定时任务
clawdbot cron add \
  --schedule "0 9 * * *" \
  --text "运行 AI 提示词收集任务，查看结果: /root/clawd/data/prompts/collected.jsonl"
```

---

## 方案 4: 修改 Slack Skill（高级）

编辑 `/usr/lib/node_modules/clawdbot/skills/slack/SKILL.md`，添加主动推送逻辑。

---

## 消息示例

Slack 会收到如下格式的消息：

```
🤖 AI 提示词收集报告 - 2026-01-30 09:00

新收集: 25 条
平均分数: 0.82

━━━━━━━━━━━━━━━━━━

1. 100 Best ChatGPT Prompts for 2026
https://example.com/chatgpt-prompts

> Learn the most effective ChatGPT prompts for content
  creation, coding, and business automation. Updated for 2026.

━━━━━━━━━━━━━━━━━━

2. Claude Prompt Engineering Guide
https://example.com/claude-guide

> Master Claude's prompt system with these proven techniques
  and examples...

📁 数据保存到: /root/clawd/data/prompts/collected.jsonl
```

---

## 常见问题

### Q: Webhook URL 在哪里？
A: 在 Slack 应用设置 → Incoming Webhooks → Add New Webhook

### Q: 如何发送到特定频道？
A: 创建 Webhook 时选择目标频道即可

### Q: 消息格式可以自定义吗？
A: 可以！修改 `send_slack_message()` 函数中的 `blocks` 结构

### Q: 如何处理敏感数据？
A: Webhook URL 应该保密，不要提交到代码仓库

---

## 下一步

1. 创建 Slack Webhook
2. 配置环境变量
3. 测试脚本运行
4. 设置定时任务
5. 根据需求调整消息格式
