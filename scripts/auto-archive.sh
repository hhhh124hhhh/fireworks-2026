#!/bin/bash

# 配置自动归档脚本
# 功能：将旧文件归档到压缩包
# 频率：每周日凌晨 2:00 执行（通过 cron）
# 更新：2026-02-10 - 创建自动归档脚本

set -e

# 配置
ARCHIVE_DIRS=(
    "/root/clawd/memory"
    "/root/clawd/logs"
)
ARCHIVE_DIR="/root/clawd/archives"
DAYS=30  # 归档 30 天前的文件
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
LOG_DIR="/root/clawd/logs/archive"
LOG_FILE="$LOG_DIR/archive-$DATE-$TIME.log"

# 创建目录
mkdir -p "$ARCHIVE_DIR"
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "自动归档任务"
log "=========================================="
log "开始时间: $(date)"
log "归档目录: ${ARCHIVE_DIRS[@]}"
log "归档天数: $DAYS 天"
log ""

# 统计变量
TOTAL_ARCHIVED=0
TOTAL_ARCHIVED_SIZE=0

# 遍历每个目录
for DIR in "${ARCHIVE_DIRS[@]}"; do
    if [ ! -d "$DIR" ]; then
        log "⚠️  目录不存在: $DIR"
        continue
    fi

    log "归档目录: $DIR"

    # 查找超过 30 天的文件
    OLD_FILES=$(find "$DIR" -type f -mtime +$DAYS 2>/dev/null)
    OLD_COUNT=$(echo "$OLD_FILES" | grep -v '^$' | wc -l)

    if [ "$OLD_COUNT" -eq 0 ]; then
        log "  ✅ 没有需要归档的文件"
        continue
    fi

    log "  找到 $OLD_COUNT 个旧文件"

    # 计算总大小
    TOTAL_SIZE=$(echo "$OLD_FILES" | xargs du -cb 2>/dev/null | tail -1 | cut -f1)

    if [ -z "$TOTAL_SIZE" ] || [ "$TOTAL_SIZE" = "0" ]; then
        log "  ⚠️  无法计算文件大小"
        continue
    fi

    TOTAL_SIZE_MB=$((TOTAL_SIZE / 1024 / 1024))

    log "  总大小: ${TOTAL_SIZE_MB}MB"

    # 创建归档文件名
    DIR_NAME=$(basename "$DIR")
    ARCHIVE_FILE="$ARCHIVE_DIR/${DIR_NAME}-archive-${DATE}.tar.gz"

    log "  归档文件: $ARCHIVE_FILE"

    # 创建归档
    ARCHIVED=0
    for file in $OLD_FILES; do
        # 将文件路径转换为相对路径
        REL_PATH="${file#$DIR/}"

        # 添加到归档
        tar -czf "$ARCHIVE_FILE" -C "$DIR" "$REL_PATH" 2>/dev/null

        if [ $? -eq 0 ]; then
            # 删除原始文件
            rm -f "$file"
            ARCHIVED=$((ARCHIVED + 1))
        fi
    done

    # 检查归档文件大小
    if [ -f "$ARCHIVE_FILE" ]; then
        ARCHIVE_SIZE=$(stat -c%s "$ARCHIVE_FILE")
        ARCHIVE_SIZE_MB=$((ARCHIVE_SIZE / 1024 / 1024))

        log "  ✅ 已归档 $ARCHIVED 个文件"
        log "  归档文件大小: ${ARCHIVE_SIZE_MB}MB"
    else
        log "  ⚠️  归档文件未创建"
        continue
    fi

    TOTAL_ARCHIVED=$((TOTAL_ARCHIVED + ARCHIVED))
    TOTAL_ARCHIVED_SIZE=$((TOTAL_ARCHIVED_SIZE + TOTAL_SIZE))
done

# 完成报告
TOTAL_ARCHIVED_SIZE_MB=$((TOTAL_ARCHIVED_SIZE / 1024 / 1024))
TOTAL_ARCHIVED_SIZE_GB=$((TOTAL_ARCHIVED_SIZE / 1024 / 1024 / 1024))

log ""
log "=========================================="
log "归档完成"
log "=========================================="
log "总归档文件数: $TOTAL_ARCHIVED"
log "总归档大小: ${TOTAL_ARCHIVED_SIZE_MB}MB (${TOTAL_ARCHIVED_SIZE_GB}GB)"
log "归档目录: $ARCHIVE_DIR"
log ""
log "日志文件: $LOG_FILE"
log ""

# 清理旧的归档文件（保留最近 6 个月）
find "$ARCHIVE_DIR" -name "*.tar.gz" -mtime +180 -delete
log "旧归档文件已清理（保留最近 6 个月）"

# 清理旧日志（保留最近 30 天）
find "$LOG_DIR" -name "archive-*.log" -mtime +30 -delete
log "旧日志已清理（保留最近 30 天）"
log "=========================================="
