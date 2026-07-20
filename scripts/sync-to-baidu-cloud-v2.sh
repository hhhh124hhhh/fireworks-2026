#!/bin/bash

# 百度云自动同步脚本 (改进版）
# 功能：管理 PPT 和绘本的下载链接，保持本地整洁
# 频率：每天凌晨 2:00 执行（通过 cron）
# 更新：2026-02-10 - 创建自动同步脚本

set -e

# 配置
DOWNLOAD_DIR="/root/clawd/downloads"
LINKS_DIR="/root/clawd/data/links"
DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H%M')
LOG_FILE="/root/clawd/logs/baidu-sync-$DATE-$TIME.log"
MANIFEST_FILE="$LINKS_DIR/manifest.json"

# 创建目录
mkdir -p "$LINKS_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "百度云同步任务"
log "=========================================="
log "开始时间: $(date)"
log ""

# 步骤 1: 清理本地下载的文件（可选，根据配置）
log "步骤 1: 检查本地文件..."

if [ -d "$DOWNLOAD_DIR" ]; then
    LOCAL_FILES=$(find "$DOWNLOAD_DIR" -type f 2>/dev/null)
    LOCAL_COUNT=$(echo "$LOCAL_FILES" | grep -v '^$' | wc -l)

    if [ "$LOCAL_COUNT" -gt 0 ]; then
        log "找到 $LOCAL_COUNT 个本地文件"

        for file in $LOCAL_FILES; do
            filename=$(basename "$file")
            filesize=$(du -h "$file" | cut -f1)
            log "  - $filename ($filesize)"
        done

        # 记录到 manifest
        log ""
        log "记录文件到 manifest..."

        if [ ! -f "$MANIFEST_FILE" ]; then
            echo "{}" > "$MANIFEST_FILE"
        fi

        for file in $LOCAL_FILES; do
            filename=$(basename "$file")
            filepath=$(realpath "$file")
            filesize=$(stat -c%s "$file")
            filesize_human=$(du -h "$file" | cut -f1)

            # 添加到 manifest（使用 jq 或 python）
            python3 << PYTHON_SCRIPT
import json
import os
from datetime import datetime

manifest_file = "$MANIFEST_FILE"
filepath = "$filepath"
filename = "$filename"
filesize = $filesize
filesize_human = "$filesize_human"

# 读取 manifest
if os.path.exists(manifest_file):
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
else:
    manifest = {}

# 添加文件记录
if "files" not in manifest:
    manifest["files"] = {}

manifest["files"][filename] = {
    "path": filepath,
    "size": filesize,
    "size_human": filesize_human,
    "uploaded_at": datetime.now().isoformat(),
    "location": "local"
}

# 保存 manifest
with open(manifest_file, 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"  ✅ {filename} 已记录")
PYTHON_SCRIPT

        done
    else
        log "✅ 本地目录为空"
    fi
else
    log "⚠️  本地目录不存在: $DOWNLOAD_DIR"
fi

# 步骤 2: 生成链接摘要报告
log ""
log "步骤 2: 生成链接摘要..."

LINKS_SUMMARY="$LINKS_DIR/links-summary-$DATE.md"

cat > "$LINKS_SUMMARY" << EOF
# 百度云下载链接摘要

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

---

## PPT 下载链接

EOF

# 添加 PPT 链接（如果有的话）
if [ -f "$MANIFEST_FILE" ]; then
    python3 << PYTHON_SCRIPT
import json
import os

manifest_file = "$MANIFEST_FILE"
links_file = "$LINKS_SUMMARY"

# 读取 manifest
if os.path.exists(manifest_file):
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
else:
    manifest = {}

# 添加到 summary
with open(links_file, 'a') as f:
    if "files" in manifest and len(manifest["files"]) > 0:
        for filename, info in manifest["files"].items():
            f.write(f"\n### {filename}\n\n")
            f.write(f"- **大小**: {info['size_human']}\n")
            f.write(f"- **路径**: \`{info['path']}\`\n")
            f.write(f"- **位置**: {info['location']}\n")
            f.write(f"- **上传时间**: {info['uploaded_at']}\n\n")
    else:
        f.write("\n暂无文件记录\n")
PYTHON_SCRIPT
fi

log "✅ 链接摘要已生成: $LINKS_SUMMARY"

# 步骤 3: 清理旧文件（可选）
log ""
log "步骤 3: 检查是否需要清理旧文件..."

# 可以在这里添加清理逻辑
# 例如：删除 7 天前下载的文件
# find "$DOWNLOAD_DIR" -type f -mtime +7 -delete

log "✅ 旧文件检查完成"

# 步骤 4: 生成统计报告
log ""
log "步骤 4: 生成统计报告..."

if [ -f "$MANIFEST_FILE" ]; then
    python3 << PYTHON_SCRIPT
import json
import os

manifest_file = "$MANIFEST_FILE"

# 读取 manifest
if os.path.exists(manifest_file):
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
else:
    manifest = {}

# 统计信息
if "files" in manifest:
    total_files = len(manifest["files"])
    total_size = sum(f['size'] for f in manifest["files"].values())
    total_size_mb = total_size / (1024 * 1024)

    print(f"  文件总数: {total_files}")
    print(f"  总大小: {total_size_mb:.2f} MB")
else:
    print("  文件总数: 0")
    print("  总大小: 0 MB")
PYTHON_SCRIPT
fi

# 完成
log ""
log "=========================================="
log "同步任务完成"
log "=========================================="
log ""
log "日志文件: $LOG_FILE"
log "链接摘要: $LINKS_SUMMARY"
log "Manifest: $MANIFEST_FILE"
log ""

# 清理旧日志
find "$(dirname "$LOG_FILE")" -name "baidu-sync-*.log" -mtime +7 -delete
log "旧日志已清理（保留最近 7 天）"
log ""
log "=========================================="
