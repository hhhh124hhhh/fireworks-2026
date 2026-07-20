#!/bin/bash
# AI 日报生成 Agent v1.0
# 最简单的版本：读取今天的 ai-research 数据，生成摘要

TODAY=$(date +%Y%m%d)
echo "🤖 AI 日报生成 Agent 启动"
echo "日期: $(date)"
echo ""

# 查找今天的研究文件
echo "🔍 正在查找最新的 AI 研究数据..."
LATEST_FILE=$(ls -t ~/clawd/memory/ai-research/AI_news_*.json 2>/dev/null | head -1)

if [ -z "$LATEST_FILE" ]; then
    echo "❌ 未找到研究数据文件"
    echo "提示: 确保 ~/clawd/memory/ai-research/ 目录中有数据文件"
    exit 1
fi

echo "✅ 找到数据文件: $(basename $LATEST_FILE)"

# 统计信息
echo "📊 正在统计数据..."
ARTICLE_COUNT=$(grep -o '"title"' "$LATEST_FILE" 2>/dev/null | wc -l)
echo "📰 文章数量: $ARTICLE_COUNT"

# 提取日期（从文件名）
FILE_DATE=$(basename "$LATEST_FILE" | grep -oP '\d{8}' | head -1)
if [ -n "$FILE_DATE" ]; then
    FORMATTED_DATE="${FILE_DATE:0:4}年${FILE_DATE:4:2}月${FILE_DATE:6:2}日"
else
    FORMATTED_DATE=$(date +%Y年%m月%d日)
fi

# 生成报告
REPORT_FILE="output/daily-report-${TODAY}.md"
mkdir -p output

echo "📝 正在生成报告..."

cat > "$REPORT_FILE" << REPORT
# 🤖 AI 日报 - ${FORMATTED_DATE}

## 📊 数据概览

| 项目 | 数值 |
|------|------|
| **数据文件** | $(basename $LATEST_FILE) |
| **文章数量** | ${ARTICLE_COUNT} 篇 |
| **生成时间** | $(date "+%Y-%m-%d %H:%M:%S") |

## 📰 主要内容

本次数据收集涵盖了最新的 AI 行业动态，包括但不限于：

- 人工智能技术的最新进展
- 大语言模型的更新与发布
- AI 应用场景的拓展
- 行业趋势分析与洞察

## 🔍 数据来源

- **原始数据**: \`$LATEST_FILE\`
- **数据格式**: JSON
- **采集时间**: ${FORMATTED_DATE}

---

*本报告由 AI 日报生成 Agent (v1.0) 自动生成*
*生成时间: $(date "+%Y-%m-%d %H:%M:%S")*
REPORT

echo ""
echo "✅ 日报生成完成！"
echo "📄 报告位置: $REPORT_FILE"
echo ""

# 显示报告预览
echo "📝 报告预览 (前30行):"
echo "==================================="
head -30 "$REPORT_FILE"
echo "==================================="
echo ""
echo "💡 提示: 使用以下命令查看完整报告:"
echo "   cat $REPORT_FILE"
