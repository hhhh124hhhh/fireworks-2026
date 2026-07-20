#!/bin/bash
# 更新 AI 研究搜索 Cron 任务（优化版）

set -e

SCRIPT_PATH="/root/clawd/projects/info-search/workflows/ai-research-extended.sh"
CRON_TIME="0 8 * * *"  # 每天 08:00 执行

echo "=========================================="
echo "更新 AI 研究搜索 Cron 任务（优化版）"
echo "=========================================="
echo ""
echo "配置："
echo "  脚本路径: $SCRIPT_PATH"
echo "  执行时间: 每天 08:00 (GMT+8)"
echo "  搜索主题: 5 个核心主题"
echo "  每天调用: 25 次（5 × 5）"
echo "  可用天数: 40 天"
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

# 添加新的 Cron 任务（优化版）
echo "添加新的 Cron 任务..."
(crontab -l 2>&1; echo "$CRON_TIME /root/clawd/projects/info-search/workflows/ai-research-extended.sh >> /root/clawd/logs/ai-research-cron.log 2>&1") | crontab - || true
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
echo "  搜索主题: 5 个核心主题"
echo "  每天调用: 25 次（5 × 5）"
echo "  可用天数: 40 天"
echo "  日志: /root/clawd/logs/ai-research-cron.log"
echo ""
echo "混合模式（启用备选主题）："
echo "  编辑 crontab: crontab -e"
echo "  添加: ENABLE_WEEKLY_TOPICS=true"
echo ""
echo "手动测试："
echo "  bash $SCRIPT_PATH"
echo ""
echo "查看日志："
echo "  tail -f /root/clawd/logs/ai-research-cron.log"
