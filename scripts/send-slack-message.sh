#!/bin/bash

# Slack Message Sender
# 发送消息到 Slack

set -e

# Slack 配置
SLACK_CHANNEL="${SLACK_CHANNEL:-C0ABSK92X4G}"  # 默认 #clawdbot
SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL}"

# 检查输入
if [ -z "$1" ] && [ -t 0 ]; then
    echo "使用方法:"
    echo "  echo '消息内容' | $0"
    echo "  $0 '消息内容'"
    exit 1
fi

# 获取消息内容
if [ -t 0 ]; then
    MESSAGE="$1"
else
    MESSAGE=$(cat)
fi

# 发送消息
if [ -n "$SLACK_WEBHOOK_URL" ]; then
    # 使用 Webhook
    curl -s -X POST "$SLACK_WEBHOOK_URL" \
        -H 'Content-Type: application/json' \
        -d "{\"channel\": \"$SLACK_CHANNEL\", \"text\": \"$MESSAGE\"}" \
        > /dev/null 2>&1
    echo "✓ 消息已发送到 Slack"
else
    # 使用 OpenClaw message 工具
    # 这里假设可以通过调用 OpenClaw API 发送
    echo "⚠ Slack Webhook 未配置"
    echo "消息内容:"
    echo "$MESSAGE"
fi
