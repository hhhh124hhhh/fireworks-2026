#!/bin/bash

# 配置 rclone 多云备份脚本
# 功能：使用 rclone 备份到多个云盘
# 频率：每天凌晨 4:00 执行（通过 cron）
# 更新：2026-02-10 - 创建 rclone 备份脚本

set -e

# 配置
RCLONE_CONFIG="/root/.config/rclone/rclone.conf"
LOCAL_DIR="/root/clawd/downloads"
REMOTE_NAME="baidu"
REMOTE_PATH="/ai-content-creator/downloads"
BACKUP_DIR="/root/clawd/backups/rclone"
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
LOG_DIR="/root/clawd/logs/rclone"
LOG_FILE="$LOG_DIR/backup-$DATE-$TIME.log"

# 创建目录
mkdir -p "$BACKUP_DIR"
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "Rclone 多云备份"
log "=========================================="
log "开始时间: $(date)"
log "本地目录: $LOCAL_DIR"
log "远程路径: $REMOTE_NAME:$REMOTE_PATH"
log ""

# 检查 rclone 是否安装
if ! command -v rclone &> /dev/null; then
    log "❌ rclone 未安装"

    # 安装 rclone
    log "正在安装 rclone..."
    curl https://rclone.org/install.sh | bash

    if [ $? -eq 0 ]; then
        log "✅ rclone 安装成功"
    else
        log "❌ rclone 安装失败"
        exit 1
    fi
fi

# 检查 rclone 配置
if [ ! -f "$RCLONE_CONFIG" ]; then
    log "⚠️  rclone 配置文件不存在"
    log "需要先配置 rclone"
    log ""
    log "配置步骤："
    log "1. 运行: rclone config"
    log "2. 添加远程存储（百度云、阿里云盘等）"
    log "3. 保存配置"
    log ""
    log "配置完成后，备份脚本将自动运行"
    exit 0
fi

# 检查本地目录
if [ ! -d "$LOCAL_DIR" ]; then
    log "⚠️  本地目录不存在: $LOCAL_DIR"
    exit 0
fi

# 检查本地文件
LOCAL_FILES=$(find "$LOCAL_DIR" -type f 2>/dev/null)
LOCAL_COUNT=$(echo "$LOCAL_FILES" | grep -v '^$' | wc -l)

if [ "$LOCAL_COUNT" -eq 0 ]; then
    log "✅ 没有需要备份的文件"
    exit 0
fi

log "找到 $LOCAL_COUNT 个本地文件"

# 开始备份
log ""
log "开始备份到云端..."

# 使用 rclone sync
log "执行: rclone sync $LOCAL_DIR $REMOTE_NAME:$REMOTE_PATH"

rclone sync "$LOCAL_DIR" "$REMOTE_NAME:$REMOTE_PATH" \
    --progress \
    --log-file "$LOG_FILE" \
    --log-level INFO \
    --create-empty-src-dirs

BACKUP_STATUS=$?

if [ $BACKUP_STATUS -eq 0 ]; then
    log "✅ 备份成功"
else
    log "❌ 备份失败 (状态码: $BACKUP_STATUS)"
    exit 1
fi

# 完成报告
log ""
log "=========================================="
log "备份完成"
log "=========================================="
log "日志文件: $LOG_FILE"
log ""

# 清理旧日志（保留最近 30 天）
find "$LOG_DIR" -name "backup-*.log" -mtime +30 -delete
log "旧日志已清理（保留最近 30 天）"
log "=========================================="
