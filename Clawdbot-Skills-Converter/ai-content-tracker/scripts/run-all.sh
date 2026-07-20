#!/bin/bash

# AI 内容自动抓取和汇总主脚本
# 整合所有步骤：按清单抓取 -> 生成文档 -> 推送到 GitHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "╔═══════════════════════════════════════╗"
echo "║  📺 AI 媒体自动抓取和汇总系统         ║"
echo "╚═══════════════════════════════════════╝"
echo ""

START_TIME=$(date +%s)

# 1. 根据媒体清单抓取内容
echo "📅 阶段 1: 根据 media-list.json 抓取媒体内容"
echo "─────────────────────────────────────────"
node "$SCRIPT_DIR/fetch-media.js"

if [ $? -ne 0 ]; then
    echo "❌ 抓取失败"
    exit 1
fi

echo ""
echo "✅ 阶段 1 完成"
echo ""

# 2. 推送到 GitHub
echo "📅 阶段 2: 推送到 GitHub"
echo "─────────────────────────────────────────"
bash "$SCRIPT_DIR/push-to-github.sh"

if [ $? -ne 0 ]; then
    echo "❌ 推送失败"
    exit 1
fi

echo ""
echo "✅ 阶段 2 完成"
echo ""

# 完成
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "╔═══════════════════════════════════════╗"
echo "║  ✅ 所有任务完成！                      ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "⏱️  总耗时: ${DURATION} 秒"
echo ""
echo "📋 完成的任务:"
echo "   ✅ 根据媒体清单抓取内容"
echo "   ✅ 生成 Markdown 文档"
echo "   ✅ 推送到 GitHub"
echo ""
echo "🔗 GitHub 仓库:"
echo "   https://github.com/hhhh124hhhh/ultimate-skills-bundle/tree/main/ai-content-tracker/docs"
echo ""
echo "📺 媒体清单:"
echo "   https://github.com/hhhh124hhhh/ultimate-skills-bundle/blob/main/ai-content-tracker/media-list.json"
echo ""
echo "🎉 下次自动运行: $(crontab -l 2>/dev/null | grep ai-content-tracker | head -1 || echo '未设置定时任务')"
echo ""
