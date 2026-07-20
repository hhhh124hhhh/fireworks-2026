#!/bin/bash

# 自动清理旧文件脚本
# 功能：清理指定目录中超过 7 天的文件
# 频率：每天凌晨 3:00 执行（通过 cron）
# 更新：2026-02-10 - 创建自动清理脚本

set -e

# 配置
CLEAN_DIRS=(
    "/root/clawd/downloads"
    "/root/clawd/memory/ai-content-creator"
    "/root/clawd/ai-prompt-marketplace/reports"
)
DAYS=7
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
LOG_DIR="/root/clawd/logs/cleanup"
LOG_FILE="$LOG_DIR/cleanup-$DATE-$TIME.log"

# 创建目录
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "自动清理旧文件"
log "=========================================="
log "开始时间: $(date)"
log "保留天数: $DAYS 天"
log ""

# 统计变量
TOTAL_DELETED=0
TOTAL_SPACE_FREED=0

# 遍历每个目录
for DIR in "${CLEAN_DIRS[@]}"; do
    if [ ! -d "$DIR" ]; then
        log "⚠️  目录不存在: $DIR"
        continue
    fi

    log "清理目录: $DIR"

    # 查找超过 7 天的文件
    OLD_FILES=$(find "$DIR" -type f -mtime +$DAYS 2>/dev/null)
    OLD_COUNT=$(echo "$OLD_FILES" | grep -v '^$' | wc -l)

    if [ "$OLD_COUNT" -eq 0 ]; then
        log "  ✅ 没有需要清理的文件"
        continue
    fi

    log "  找到 $OLD_COUNT 个旧文件"

    # 计算总大小
    TOTAL_SIZE=$(echo "$OLD_FILES" | xargs du -cb 2>/dev/null | tail -1 | cut -f1)
    TOTAL_SIZE_MB=$((TOTAL_SIZE / 1024 / 1024))

    log "  总大小: ${TOTAL_SIZE_MB}MB"

    # 删除文件
    DELETED=0
    for file in $OLD_FILES; do
        if rm -f "$file" 2>/dev/null; then
            DELETED=$((DELETED + 1))
        fi
    done

    log "  ✅ 已删除 $DELETED 个文件"

    TOTAL_DELETED=$((TOTAL_DELETED + DELETED))
    TOTAL_SPACE_FREED=$((TOTAL_SPACE_FREED + TOTAL_SIZE))
done

# 完成报告
TOTAL_SPACE_FREED_MB=$((TOTAL_SPACE_FREED / 1024 / 1024))
TOTAL_SPACE_FREED_GB=$((TOTAL_SPACE_FREED / 1024 / 1024 / 1024))

log ""
log "=========================================="
log "清理完成"
log "=========================================="
log "总删除文件数: $TOTAL_DELETED"
log "释放空间: ${TOTAL_SPACE_FREED_MB}MB (${TOTAL_SPACE_FREED_GB}GB)"
log ""
log "日志文件: $LOG_FILE"
log ""

# 清理旧日志（保留最近 30 天）
find "$LOG_DIR" -name "cleanup-*.log" -mtime +30 -delete
log "旧日志已清理（保留最近 30 天）"
log "=========================================="
