#!/bin/bash

# 配置百度云自动同步到 Cron

# 添加 cron 任务
# 每天凌晨 2:00 执行同步

CRON_JOB="0 2 * * * bash /root/clawd/scripts/sync-to-baidu-cloud-v2.sh > /tmp/baidu-sync.log 2>&1"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "sync-to-baidu-cloud"; then
    echo "⚠️  百度云同步任务已存在"
    echo ""
    echo "当前任务："
    crontab -l 2>/dev/null | grep "sync-to-baidu-cloud"
else
    echo "➕ 添加百度云同步任务..."
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "✅ 百度云同步任务已添加"
    echo ""
    echo "执行时间: 每天凌晨 2:00"
    echo "脚本: /root/clawd/scripts/sync-to-baidu-cloud-v2.sh"
fi

echo ""
echo "=========================================="
echo "查看当前 crontab:"
echo "=========================================="
crontab -l 2>/dev/null | tail -10
