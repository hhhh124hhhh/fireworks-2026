#!/bin/bash
# AI 研究摘要报告推送脚本

set -e

# 配置
OUTPUT_DIR="/root/clawd/memory/ai-research"
SLACK_USER="U0ABB7VDJBT"
SLACK_CHANNEL="#clawdbot"
LATEST_SUMMARY="$OUTPUT_DIR/latest-summary.txt"

# 检查是否有新的摘要
if [ ! -f "$LATEST_SUMMARY" ]; then
    echo "❌ 错误: 没有找到最新的摘要文件"
    exit 1
fi

SUMMARY_FILE=$(cat "$LATEST_SUMMARY")

if [ ! -f "$SUMMARY_FILE" ]; then
    echo "❌ 错误: 摘要文件不存在: $SUMMARY_FILE"
    exit 1
fi

echo "=========================================="
echo "AI 研究摘要报告推送"
echo "=========================================="
echo ""
echo "摘要文件: $SUMMARY_FILE"
echo ""

# 提取统计信息
TOTAL_TOPICS=$(grep "总搜索主题" "$SUMMARY_FILE" | awk '{print $NF}' | tr -d ' ')
TOTAL_RESULTS=$(grep "总结果数量" "$SUMMARY_FILE" | awk '{print $NF}' | tr -d ' ')
AVG_RESULTS=$(grep "平均结果数量" "$SUMMARY_FILE" | awk '{print $NF}' | tr -d ' ')
DATE=$(grep "日期" "$SUMMARY_FILE | head -1" | awk '{print $NF}')

# 提取搜索主题列表
echo "提取搜索主题..."
TOPICS=$(grep -A 100 "## 搜索主题列表" "$SUMMARY_FILE" | grep "^\- \*\*" | head -5)
echo "✅ 提取完成"
echo ""

# 生成 Slack 消息
SLACK_MESSAGE="# 🔍 AI 研究搜索摘要

**日期**: $DATE
**统计**: $TOTAL_TOPICS 个搜索主题，$TOTAL_RESULTS 条结果

## 搜索主题示例

$TOPICS

---

## 统计摘要

- **总搜索主题**: $TOTAL_TOPICS
- **总结果数量**: $TOTAL_RESULTS
- **平均结果数量**: $AVG_RESULTS

---

详细日志已保存到 \`$OUTPUT_DIR/\`

---

*AI 研究搜索 - 每天 08:00 自动执行*"

echo "=========================================="
echo "Slack 消息"
echo "=========================================="
echo ""
echo "$SLACK_MESSAGE"
echo ""

# 推送到 Slack
echo "推送消息到 Slack..."
openclaw message send \
  --to "$SLACK_CHANNEL" \
  --message "$SLACK_MESSAGE" \
  2>&1 | grep -v "ok\|result" || echo "✅ 消息已推送"
echo ""

echo "=========================================="
echo "✅ 推送完成！"
echo "=========================================="
