#!/bin/bash

# 备份状态检查脚本
# 功能: 检查备份状态，生成报告
# 频率: 每小时检查一次（通过 cron）
# 更新: 2026-02-10 - 创建备份状态检查脚本

set -e

# 配置
BACKUP_DIR="/root/clawd/backups/daily"
GIT_DIR="/root/clawd"
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
LOG_DIR="/root/clawd/logs/backup"
REPORT_FILE="${LOG_DIR}/backup-status-${DATE}-${TIME}.md"

# 创建目录
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "检查备份状态..."

# 生成报告
cat > "$REPORT_FILE" << EOF
# 备份状态报告

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

---

## 📦 每日备份状态

### 最近的备份

| 日期 | 文件 | 大小 |
|------|------|------|
EOF

if [ -d "$BACKUP_DIR" ]; then
    find "$BACKUP_DIR" -name "daily-backup-*.tar.gz" -mtime -7 -exec ls -lh {} \; | awk '{print " | " $6 " | " $9 " | " $5 " |"}' >> "$REPORT_FILE"
else
    echo " | 无备份 | - | - |" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

### 统计

EOF

if [ -d "$BACKUP_DIR" ]; then
    BACKUP_COUNT=$(find "$BACKUP_DIR" -name "daily-backup-*.tar.gz" | wc -l)
    BACKUP_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
    echo "- 备份文件数: $BACKUP_COUNT" >> "$REPORT_FILE"
    echo "- 备份总大小: $BACKUP_SIZE" >> "$REPORT_FILE"
else
    echo "- 备份目录不存在" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

## 🔧 Git 同步状态

### 仓库信息

EOF

if [ -d "$GIT_DIR/.git" ]; then
    cd "$GIT_DIR"

    # 获取最新提交
    LATEST_COMMIT=$(git log -1 --format="%h - %s (%cd)" --date=short 2>/dev/null)
    echo "- 最新提交: $LATEST_COMMIT" >> "$REPORT_FILE"

    # 获取分支
    BRANCH=$(git branch --show-current 2>/dev/null)
    echo "- 当前分支: $BRANCH" >> "$REPORT_FILE"

    # 获取远程仓库
    REMOTE=$(git remote get-url origin 2>/dev/null)
    if [ -n "$REMOTE" ]; then
        echo "- 远程仓库: $REMOTE" >> "$REPORT_FILE"
    else
        echo "- 远程仓库: 未配置" >> "$REPORT_FILE"
    fi

    # 检查未提交的更改
    CHANGES=$(git status --porcelain 2>/dev/null | wc -l)
    echo "- 未提交更改: $CHANGES" >> "$REPORT_FILE"
else
    echo "- Git 仓库未初始化" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

## 📊 记忆文件状态

### 关键文件

EOF

MEMORY_FILES=(
    "/root/clawd/memory/MEMORY.md"
    "/root/clawd/memory/2026-02-10.md"
    "/root/clawd/IDENTITY.md"
    "/root/clawd/USER.md"
    "/root/clawd/SOUL.md"
)

for file in "${MEMORY_FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(ls -lh "$file" | awk '{print $5}')
        MODIFIED=$(stat -c %y "$file" | cut -d'.' -f1)
        echo "- $(basename $file): $SIZE (${MODIFIED})" >> "$REPORT_FILE"
    else
        echo "- $(basename $file): 不存在" >> "$REPORT_FILE"
    fi
done

cat >> "$REPORT_FILE" << EOF

---

## ✅ 建议操作

EOF

# 检查是否需要备份
if [ -d "$BACKUP_DIR" ]; then
    LATEST_BACKUP=$(find "$BACKUP_DIR" -name "daily-backup-*.tar.gz" -mtime -1 | wc -l)
    if [ "$LATEST_BACKUP" -eq 0 ]; then
        echo "- ⚠️  最近 24 小时没有备份，建议手动执行备份" >> "$REPORT_FILE"
    else
        echo "- ✅ 最近 24 小时有备份" >> "$REPORT_FILE"
    fi
else
    echo "- ⚠️  备份目录不存在" >> "$REPORT_FILE"
fi

# 检查 Git 同步
if [ -d "$GIT_DIR/.git" ]; then
    REMOTE=$(git -C "$GIT_DIR" remote get-url origin 2>/dev/null)
    if [ -z "$REMOTE" ]; then
        echo "- ⚠️  Git 远程仓库未配置，建议配置 GitHub 仓库" >> "$REPORT_FILE"
    else
        echo "- ✅ Git 远程仓库已配置" >> "$REPORT_FILE"
    fi
else
    echo "- ⚠️  Git 仓库未初始化" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

---

**报告文件**: $REPORT_FILE
EOF

log "✅ 备份状态报告已生成: $REPORT_FILE"

# 清理旧报告（保留 7 天）
find "$LOG_DIR" -name "backup-status-*.md" -mtime +7 -delete
log "✅ 旧报告已清理（保留最近 7 天）"

# 输出报告内容
log ""
log "=========================================="
log "备份状态报告"
log "=========================================="
cat "$REPORT_FILE"
