#!/bin/bash
# =========================================
# Topics Sync Skill - 选题池同步脚本
# 全自动：pull → write → commit → push
# 冲突解决：优先本地（云端新建内容）
# 防并发锁机制
# =========================================

set -e

REPO_DIR="/root/clawd/workspace-shared/topics"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCK_FILE="/tmp/topics-sync.lock"
LOG_FILE="$REPO_DIR/sync-topics-cloud.log"

# 配置
REMOTE_URL="https://github.com/hhhh124hhhh/openclaw-topics-sync.git"

# 防并发锁
acquire_lock() {
    local MAX_WAIT=30
    local waited=0
    while [ -f "$LOCK_FILE" ]; do
        # 如果锁存在超过 5 分钟，认为是残留，删除后继续
        LOCK_AGE=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0)))
        if [ "$LOCK_AGE" -gt 300 ]; then
            rm -f "$LOCK_FILE"
            break
        fi
        if [ $waited -ge $MAX_WAIT ]; then
            echo "[$(date)] Lock timeout, skipping..."
            return 1
        fi
        sleep 1
        ((waited++))
    done
    echo $$ > "$LOCK_FILE"
    return 0
}

release_lock() {
    rm -f "$LOCK_FILE"
}

# 确保 Git 配置正确
setup_git() {
    cd "$REPO_DIR"
    git config user.email "intel-officer@openclaw.ai" 2>/dev/null || true
    git config user.name "intel-officer" 2>/dev/null || true
    git remote set-url origin "$REMOTE_URL" 2>/dev/null || true
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ============================================
# 主流程：同步 → 写入 → 推送
# ============================================

main() {
    local TOPIC_CONTENT="$1"
    local MODE="${2:-sync}"  # sync | read | sync-read
    
    # 获取锁
    acquire_lock || return 1
    
    trap release_lock EXIT
    
    log "=== Topics Sync Started ==="
    
    # Step 1: 确保仓库存在
    if [ ! -d "$REPO_DIR/.git" ]; then
        log "Cloning repo..."
        git clone "$REMOTE_URL" "$REPO_DIR"
        setup_git
    fi
    
    setup_git
    
    # Step 2: Pull 最新代码
    log "Pulling latest from GitHub..."
    GIT_TERMINAL_PROMPT=0 git pull origin main --allow-unrelated-histories -X ours 2>> "$LOG_FILE" || true
    
    # Step 3: 如果有内容要写入
    if [ -n "$TOPIC_CONTENT" ]; then
        local TIMESTAMP=$(date '+%Y%m%d-%H%M')
        local OUTPUT_FILE="$REPO_DIR/topics-pool-cloud-$TIMESTAMP.md"
        
        log "Writing topics to: $OUTPUT_FILE"
        echo "$TOPIC_CONTENT" > "$OUTPUT_FILE"
        
        # Stage 并检查
        git add -A
        if git diff --cached --quiet; then
            log "No changes to commit"
        else
            # Step 4: 提交
            log "Committing..."
            git commit -m "sync: $TIMESTAMP" 2>> "$LOG_FILE" || true
            
            # Step 5: 推送
            log "Pushing to GitHub..."
            GIT_TERMINAL_PROMPT=0 git push origin main 2>> "$LOG_FILE"
            log "✅ Pushed: $OUTPUT_FILE"
        fi
    fi
    
    # Step 6: 如果是 read 模式，读取今日选题
    if [ "$MODE" = "read" ] || [ "$MODE" = "sync-read" ]; then
        local TODAY_FILE=$(ls -t "$REPO_DIR"/topics-pool-cloud-$(date '+%Y%m%d')*.md 2>/dev/null | head -1)
        if [ -n "$TODAY_FILE" ]; then
            log "Reading: $TODAY_FILE"
            cat "$TODAY_FILE"
        else
            log "No today's topics found"
        fi
    fi
    
    log "=== Topics Sync Completed ==="
}

# ============================================
# 纯读取模式：只读取今日选题
# ============================================

read_today() {
    local TODAY_FILE=$(ls -t "$REPO_DIR"/topics-pool-cloud-$(date '+%Y%m%d')*.md 2>/dev/null | head -1)
    if [ -n "$TODAY_FILE" ]; then
        cat "$TODAY_FILE"
    else
        echo "No today's topics found"
    fi
}

# 执行
case "$1" in
    read)
        read_today
        ;;
    *)
        main "$1" "$2"
        ;;
esac
