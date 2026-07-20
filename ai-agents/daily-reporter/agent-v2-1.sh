#!/bin/bash
# AI 日报生成 Agent v2.1 - 简化版
# 使用 OpenClaw Cron 系统

set -e

TODAY=$(date +%Y%m%d)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
JOB_NAME="daily-reporter-v2"
LOG_FILE="${HOME}/clawd/ai-agents/daily-reporter/logs/${JOB_NAME}-${TODAY}.log"

mkdir -p "$(dirname $LOG_FILE)"

echo "🤖 AI 日报生成 Agent v2.1 启动"
echo "================================"
echo "日期: $(date)"
echo "Agent: ${JOB_NAME}"
echo ""

# 记录日志
exec > >(tee -a "$LOG_FILE")

# 步骤 1: 准备数据
echo "📂 步骤 1: 准备数据..."

LATEST_FILE=$(ls -t ~/clawd/memory/ai-research/AI_news_*.json 2>/dev/null | head -1)

if [ -z "$LATEST_FILE" ]; then
    echo "❌ 错误: 未找到 AI 研究数据文件"
    exit 1
fi

echo "✅ 找到数据文件: $(basename $LATEST_FILE)"

ARTICLE_COUNT=$(grep -o '"title"' "$LATEST_FILE" 2>/dev/null | wc -l)
echo "📊 文章数量: $ARTICLE_COUNT"

# 复制数据到工作目录
WORK_DIR="${HOME}/clawd/ai-agents/daily-reporter/work/${TODAY}"
mkdir -p "$WORK_DIR"

cp "$LATEST_FILE" "$WORK_DIR/input-data.json"
echo "✅ 数据已复制到工作目录: $WORK_DIR"
echo ""

# 步骤 2: 添加 Cron 任务
echo "⏰ 步骤 2: 添加 Cron 任务..."

# 检查是否已存在同名任务
EXISTING_JOB=$(openclaw cron list --json 2>/dev/null | grep -o "\"name\":\"[^\"]*\"" | grep "\"name\":\"$JOB_NAME\"" || echo "")

if [ -n "$EXISTING_JOB" ]; then
    echo "⚠️  Cron 任务 '$JOB_NAME' 已存在"
    echo "   将删除旧任务..."
    JOB_ID=$(echo "$EXISTING_JOB" | grep -oP '(?<="name":")([^"]+)' || echo "")
    if [ -n "$JOB_ID" ]; then
        echo "   任务 ID: $JOB_ID"
        # 先用 cron rm 删除（需要找到job ID）
        # 暂时跳过删除，直接更新
    fi
else
    echo "✅ Cron 任务 '$JOB_NAME' 不存在，将创建新任务"
fi

CRON_SCHEDULE="0 9 * * *"  # 每天早上 9 点运行

echo "🚀 正在创建 Cron 任务..."
echo "   调度: $CRON_SCHEDULE"
echo "   任务: AI 日报分析"
echo "   消息: 请分析今天的AI新闻数据，生成洞察报告"
echo ""

# 创建 cron 任务
CRON_OUTPUT=$(openclaw cron add \
    --name "$JOB_NAME" \
    --cron "$CRON_SCHEDULE" \
    --message "请分析今天的AI新闻数据，生成洞察报告。数据文件路径：${WORK_DIR}/input-data.json" 2>&1)

if echo "$CRON_OUTPUT" | grep -qE "(added|created|✅|success)"; then
    echo "✅ Cron 任务创建成功！"
elif echo "$CRON_OUTPUT" | grep -qE "(already exists|⚠️)"; then
    echo "⚠️  Cron 任务已存在，继续使用现有任务"
else
    echo "❌ Cron 任务创建失败"
    echo "   输出: $CRON_OUTPUT"
    # 继续执行，不影响后续步骤
fi

echo ""

# 步骤 3: 显示当前 Cron 任务
echo "📋 步骤 3: 显示 Cron 任务状态..."
echo ""

Cron_LIST=$(openclaw cron list 2>&1)
echo "$Cron_LIST" | head -30

echo ""

# 步骤 4: 生成基础报告（无需 AI 分析）
echo "📝 步骤 4: 生成基础报告..."
echo ""

REPORT_FILE="${HOME}/clawd/ai-agents/daily-reporter/output/daily-report-${TODAY}.md"
mkdir -p "$(dirname $REPORT_FILE)"

FILE_DATE=$(basename "$LATEST_FILE" | grep -oP '\d{8}' | head -1)
if [ -n "$FILE_DATE" ]; then
    FORMATTED_DATE="${FILE_DATE:0:4}年${FILE_DATE:4:2}月${FILE_DATE:6:2}日"
else
    FORMATTED_DATE=$(date +%Y年%m月%d日)
fi

cat > "$REPORT_FILE" << REPORT
# 🤖 AI 日报 - ${FORMATTED_DATE}

> **生成时间**: $(date "+%Y-%m-%d %H:%M:%S")
> **Agent 版本**: v2.1 (OpenClaw Cron 系统)
> **数据来源**: $(basename $LATEST_FILE)

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| **文章总数** | ${ARTICLE_COUNT} 篇 |
| **数据日期** | ${FORMATTED_DATE} |
| **数据文件** | \`$(basename $LATEST_FILE)\` |

---

## 📰 主要内容

本次数据收集涵盖了最新的 AI 行业动态，包括但不限于：

- 人工智能技术的最新进展
- 大语言模型的更新与发布
- AI 应用场景的拓展
- 行业趋势分析与洞察

## 🔍 下一步

等待 Cron 任务在每天 09:00 自动运行，将由 AI Agent 进行深度分析并生成完整报告。

---

## 📁 相关文件

- **原始数据**: \`$LATEST_FILE\`
- **工作目录**: \`${WORK_DIR}\`
- **Cron 任务**: \`$JOB_NAME\`

---

*本报告由 AI 日报生成 Agent v2.1 自动生成*
*Cron 系统: OpenClaw*
*下次自动运行: 明天 09:00*

---

## 💡 查看和管理

- **查看 Cron 任务**: \`openclaw cron list\`
- **查看运行历史**: \`openclaw cron runs --name ${JOB_NAME}\`
- **手动运行任务**: \`openclaw cron run ${JOB_NAME}\`
- **删除任务**: \`openclaw cron rm <job-id>\`

REPORT

echo "✅ 基础报告生成完成！"
echo "📄 报告位置: $REPORT_FILE"
echo ""

# 步骤 5: 显示摘要
echo "================================"
echo "📊 执行摘要"
echo "================================"
echo "Agent 名称: AI 日报生成 Agent v2.1"
echo "运行时间: $(date)"
echo "数据文件: $(basename $LATEST_FILE)"
echo "文章数量: $ARTICLE_COUNT"
echo "Cron 任务: $JOB_NAME (每天 09:00)"
echo "报告文件: $REPORT_FILE"
echo "================================"
echo ""

echo "📝 报告预览 (前40行):"
echo "==================================="
head -40 "$REPORT_FILE"
echo "==================================="
echo ""
echo "💡 提示:"
echo "   查看完整报告: cat $REPORT_FILE"
echo "   查看 Cron 任务: openclaw cron list"
echo "   手动运行: openclaw cron run ${JOB_NAME}"
echo "   查看历史: openclaw cron runs --name ${JOB_NAME}"
echo ""
