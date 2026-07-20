#!/bin/bash

# Git 同步脚本 - 同步重要文件到 GitHub
# 频率: 每天凌晨 1:30 执行（通过 cron）
# 更新: 2026-02-10 - 创建 Git 同步脚本

set -e

# 配置
REPO_DIR="/root/clawd"
GIT_REPO=""  # 需要配置 GitHub 仓库地址
GIT_BRANCH="main"
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
LOG_DIR="/root/clawd/logs/git"
LOG_FILE="${LOG_DIR}/git-sync-${DATE}-${TIME}.log"

# 需要提交的文件
COMMIT_FILES=(
    "memory/"
    "docs/"
    "scripts/"
    "IDENTITY.md"
    "USER.md"
    "SOUL.md"
    "AGENTS.md"
    "HEARTBEAT.md"
    "TOOLS.md"
)

# 排除的文件
EXCLUDE_FILES=(
    ".env"
    "*.pyc"
    "__pycache__"
    "*.log"
    "node_modules/"
    ".git/"
)

# 创建目录
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "Git 同步任务"
log "=========================================="
log "开始时间: $(date)"
log "仓库目录: $REPO_DIR"
log ""

# 检查 Git 仓库
if [ ! -d "$REPO_DIR/.git" ]; then
    log "⚠️  Git 仓库未初始化"

    if [ -z "$GIT_REPO" ]; then
        log "❌ 未配置 GitHub 仓库地址"
        log "请设置 GIT_REPO 变量"
        exit 1
    fi

    log "初始化 Git 仓库..."
    cd "$REPO_DIR"
    git init
    git remote add origin "$GIT_REPO"
    log "✅ Git 仓库已初始化"
else
    log "✅ Git 仓库已存在"
    cd "$REPO_DIR"
fi

# 检查远程仓库
if [ -z "$GIT_REPO" ]; then
    log "⚠️  未配置 GitHub 仓库地址"
    log "跳过 Git 同步"
    exit 0
fi

# 创建 .gitignore（如果不存在）
if [ ! -f "$REPO_DIR/.gitignore" ]; then
    log "创建 .gitignore..."
    cat > "$REPO_DIR/.gitignore" << EOF
# 环境变量
.env
.env.*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log
yarn-error.log

# 日志
*.log
logs/

# 备份
backups/
*.bak
*.backup

# 临时文件
tmp/
temp/
*.tmp

# 操作系统
.DS_Store
Thumbs.db
EOF
    log "✅ .gitignore 已创建"
fi

# 添加文件
log ""
log "添加文件到 Git..."

for item in "${COMMIT_FILES[@]}"; do
    if [ -e "$REPO_DIR/$item" ]; then
        git add "$item" 2>/dev/null
        if [ $? -eq 0 ]; then
            log "  ✅ $item"
        else
            log "  ⚠️  $item (添加失败)"
        fi
    else
        log "  ⚠️  $item (不存在)"
    fi
done

# 检查是否有更改
CHANGES=$(git diff --cached --name-only)
if [ -z "$CHANGES" ]; then
    log ""
    log "✅ 没有需要提交的更改"
    exit 0
fi

# 提交更改
log ""
log "提交更改..."

COMMIT_MESSAGE="Daily backup - $DATE $TIME"

git commit -m "$COMMIT_MESSAGE"

if [ $? -eq 0 ]; then
    log "✅ 更改已提交"
else
    log "❌ 提交失败"
    exit 1
fi

# 推送到远程
log ""
log "推送到远程仓库..."

git push origin "$GIT_BRANCH"

if [ $? -eq 0 ]; then
    log "✅ 已推送到远程仓库"
else
    log "❌ 推送失败"
    exit 1
fi

# 完成报告
log ""
log "=========================================="
log "Git 同步完成"
log "=========================================="
log "提交信息: $COMMIT_MESSAGE"
log "日志文件: $LOG_FILE"
log ""

# 清理旧日志（保留 30 天）
find "$LOG_DIR" -name "git-sync-*.log" -mtime +30 -delete
log "旧日志已清理（保留最近 30 天）"
log "=========================================="
