#!/bin/bash

# 配置备份 Cron 任务

echo "=========================================="
echo "配置备份 Cron 任务"
echo "=========================================="
echo ""

# 添加备份任务到 crontab
(crontab -l 2>/dev/null; cat << EOF

# =========== BACKUP & SYNC ===========

# Daily Backup (daily 1:00)
0 1 * * * bash /root/clawd/scripts/daily-backup.sh >> /root/clawd/logs/backup/daily-backup-cron.log 2>&1

# Git Sync (daily 1:30)
0 1 * * * bash /root/clawd/scripts/git-sync.sh >> /root/clawd/logs/git/git-sync-cron.log 2>&1

# Backup Status Check (hourly)
0 * * * * bash /root/clawd/scripts/backup-status.sh >> /root/clawd/logs/backup/backup-status-cron.log 2>&1
EOF
) | crontab -

echo "✅ 备份 Cron 任务已添加"
echo ""
echo "=========================================="
echo "备份任务列表"
echo "=========================================="
echo ""
echo "时间          | 任务"
echo "-------------|----------------------------------------"
echo "每天 1:00    | 每日备份（memory、docs、配置）"
echo "每天 1:30    | Git 同步到 GitHub"
echo "每小时       | 备份状态检查"
echo ""
echo "=========================================="
echo "查看完整 Cron:"
echo "=========================================="
crontab -l 2>/dev/null | tail -20
