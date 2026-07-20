#!/bin/bash
# =========================================
# 云端选题收集脚本（只收集，不推送）
# 收集 → 写入本地文件夹 → 本地开机后拉取
# =========================================

set -e

REPO_DIR="/root/clawd/workspace-shared/topics"
cd "$REPO_DIR"

LOG="$REPO_DIR/collect.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Collect started ===" >> "$LOG"

# 运行收集（intel-officer 的 pipeline）
# 具体命令根据你的 pipeline 配置
if [ -f "package.json" ]; then
    node merge-topics.js >> "$LOG" 2>&1 || true
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Collect completed ===" >> "$LOG"
