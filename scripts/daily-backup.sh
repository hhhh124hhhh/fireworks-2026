#!/bin/bash

# 每日备份脚本 - 备份记忆、配置、文档
# 频率: 每天凌晨 1:00 执行（通过 cron）
# 更新: 2026-02-10 - 创建每日备份脚本

set -e

# 配置
BACKUP_DIR="/root/clawd/backups/daily"
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
BACKUP_NAME="daily-backup-${DATE}-${TIME}"
BACKUP_FILE="${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
LOG_DIR="/root/clawd/logs/backup"
LOG_FILE="${LOG_DIR}/daily-backup-${DATE}-${TIME}.log"

# 需要备份的目录
BACKUP_TARGETS=(
    "/root/clawd/memory"
    "/root/clawd/docs"
    "/root/clawd/data"
)

# 需要备份的文件
BACKUP_FILES=(
    "/root/clawd/IDENTITY.md"
    "/root/clawd/USER.md"
    "/root/clawd/SOUL.md"
    "/root/clawd/AGENTS.md"
    "/root/clawd/HEARTBEAT.md"
    "/root/clawd/TOOLS.md"
)

# 创建目录
mkdir -p "$BACKUP_DIR"
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "每日备份任务"
log "=========================================="
log "开始时间: $(date)"
log "备份名称: $BACKUP_NAME"
log ""

# 创建临时目录
TEMP_DIR=$(mktemp -d)
log "创建临时目录: $TEMP_DIR"

# 复制文件
log ""
log "复制文件..."

for file in "${BACKUP_FILES[@]}"; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        cp "$file" "$TEMP_DIR/$filename"
        log "  ✅ $filename"
    else
        log "  ⚠️  文件不存在: $file"
    fi
done

# 复制目录
log ""
log "复制目录..."

for dir in "${BACKUP_TARGETS[@]}"; do
    if [ -d "$dir" ]; then
        dirname=$(basename "$dir")
        cp -r "$dir" "$TEMP_DIR/$dirname"
        log "  ✅ $dirname"
    else
        log "  ⚠️  目录不存在: $dir"
    fi
done

# 创建压缩包
log ""
log "创建压缩包..."

tar -czf "$BACKUP_FILE" -C "$TEMP_DIR" . 2>/dev/null

if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(stat -c%s "$BACKUP_FILE")
    BACKUP_SIZE_MB=$((BACKUP_SIZE / 1024 / 1024))
    log "✅ 压缩包创建成功"
    log "  文件: $BACKUP_FILE"
    log "  大小: ${BACKUP_SIZE_MB}MB"
else
    log "❌ 压缩包创建失败"
    exit 1
fi

# 清理临时目录
rm -rf "$TEMP_DIR"
log ""
log "✅ 临时目录已清理"

# 上传到百度云（可选）
log ""
log "尝试上传到百度云..."

if [ -f "$BACKUP_FILE" ]; then
    # 这里可以添加百度云上传逻辑
    # 目前只记录日志
    log "  ⚠️  百度云上传功能待配置"
    log "  备份文件: $BACKUP_FILE"
fi

# 清理旧备份（保留 7 天）
log ""
log "清理旧备份..."
find "$BACKUP_DIR" -name "daily-backup-*.tar.gz" -mtime +7 -delete
OLD_COUNT=$(find "$BACKUP_DIR" -name "daily-backup-*.tar.gz" | wc -l)
log "✅ 已清理 7 天前的备份"
log "  当前备份数: $OLD_COUNT"

# 完成报告
log ""
log "=========================================="
log "备份完成"
log "=========================================="
log "备份文件: $BACKUP_FILE"
log "备份大小: ${BACKUP_SIZE_MB}MB"
log "日志文件: $LOG_FILE"
log ""

# 清理旧日志（保留 30 天）
find "$LOG_DIR" -name "daily-backup-*.log" -mtime +30 -delete
log "旧日志已清理（保留最近 30 天）"
log "=========================================="

# 生成备份摘要
SUMMARY_FILE="${BACKUP_DIR}/daily-backup-summary.md"
cat > "$SUMMARY_FILE" << EOF
# 每日备份摘要

**最后更新**: $(date '+%Y-%m-%d %H:%M:%S')

---

## 最近的备份

| 日期 | 文件 | 大小 |
|------|------|------|
EOF

find "$BACKUP_DIR" -name "daily-backup-*.tar.gz" -mtime -7 -exec ls -lh {} \; | awk '{print " | " $6 " | " $9 " | " $5 " |"}' >> "$SUMMARY_FILE"

log "✅ 备份摘要已更新: $SUMMARY_FILE"
