#!/bin/bash
# 设置 AI 研究搜索的 Cron 任务

set -e

SCRIPT_PATH="/root/clawd/projects/info-search/workflows/ai-research-extended.sh"
CRON_TIME="0 8 * * *"  # 每天 08:00 执行

echo "=========================================="
echo "设置 AI 研究搜索 Cron 任务"
echo "=========================================="
echo ""
echo "配置："
echo "  脚本路径: $SCRIPT_PATH"
echo "  执行时间: 每天 08:00 (GMT+8)"
echo "  Cron 表达式: $CRON_TIME"
echo ""

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 错误: 脚本不存在: $SCRIPT_PATH"
    exit 1
fi

echo "✅ 脚本存在"
echo ""

# 备份当前 crontab
echo "备份当前 crontab..."
crontab -l > /tmp/crontab-backup-$(date +%Y%m%d_%H%M%S) 2>&1 || true
echo "✅ 已备份"
echo ""

# 检查是否已存在相同的任务
echo "检查现有 Cron 任务..."
EXISTING=$(crontab -l 2>&1 | grep -c "ai-research" || true)
if [ "$EXISTING" -gt 0 ]; then
    echo "⚠️  发现 $EXISTING 个现有的 AI 研究 Cron 任务"
    echo "将删除旧任务..."
    crontab -l 2>&1 | grep -v "ai-research" | crontab - || true
    echo "✅ 已删除旧任务"
else
    echo "✅ 未发现现有任务"
fi
echo ""

# 添加新的 Cron 任务
echo "添加新的 Cron 任务..."
(crontab -l 2>&1; echo "$CRON_TIME $SCRIPT_PATH >> /root/clawd/logs/ai-research-cron.log 2>&1") | crontab - || true
echo "✅ Cron 任务已添加"
echo ""

# 验证
echo "验证 Cron 任务..."
crontab -l | grep "ai-research"
echo ""

echo "=========================================="
echo "✅ 设置完成！"
echo "=========================================="
echo ""
echo "Cron 任务详情："
echo "  执行时间: 每天 08:00 (GMT+8)"
echo "  脚本: $SCRIPT_PATH"
echo "  日志: /root/clawd/logs/ai-research-cron.log"
echo ""
echo "可以手动测试："
echo "  bash $SCRIPT_PATH"
echo ""
echo "查看日志："
echo "  tail -f /root/clawd/logs/ai-research-cron.log"
