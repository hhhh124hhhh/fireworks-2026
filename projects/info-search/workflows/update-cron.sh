#!/bin/bash
# 更新 AI 研究搜索的 Cron 任务（添加推送功能）

set -e

SCRIPT_PATH="/root/clawd/projects/info-search/workflows/ai-research-extended.sh"
CRON_TIME="0 8 * * *"  # 每天 08:00 执行

echo "=========================================="
echo "更新 AI 研究搜索 Cron 任务（添加推送功能）"
echo "=========================================="
echo ""
echo "配置："
echo "  脚本路径: $SCRIPT_PATH"
echo "  执行时间: 每天 08:00 (GMT+8)"
echo "  推送功能: 启用（推送到 Slack/Feishu）"
echo ""

# 备份当前 crontab
echo "备份当前 crontab..."
crontab -l > /tmp/crontab-backup-$(date +%Y%m%d_%H%M%S) 2>&1 || true
echo "✅ 已备份"
echo ""

# 删除旧的 AI 研究任务
echo "删除旧的 AI 研究任务..."
crontab -l 2>&1 | grep -v "ai-research" | crontab - || true
echo "✅ 已删除"
echo ""

# 添加新的 Cron 任务（带推送功能）
echo "添加新的 Cron 任务..."
(crontab -l 2>&1; echo "$CRON_TIME PUSH_SUMMARY=true $SCRIPT_PATH >> /root/clawd/logs/ai-research-cron.log 2>&1") | crontab - || true
echo "✅ Cron 任务已添加"
echo ""

# 验证
echo "验证 Cron 任务..."
crontab -l | grep "ai-research"
echo ""

echo "=========================================="
echo "✅ 更新完成！"
echo "=========================================="
echo ""
echo "Cron 任务详情："
echo "  执行时间: 每天 08:00 (GMT+8)"
echo "  脚本: $SCRIPT_PATH"
echo "  推送功能: 启用（自动推送到 Slack/Feishu）"
echo "  日志: /root/clawd/logs/ai-research-cron.log"
echo ""
echo "手动测试（不推送）："
echo "  bash $SCRIPT_PATH"
echo ""
echo "手动测试（带推送）："
echo "  PUSH_SUMMARY=true bash $SCRIPT_PATH"
echo ""
echo "查看日志："
echo "  tail -f /root/clawd/logs/ai-research-cron.log"
