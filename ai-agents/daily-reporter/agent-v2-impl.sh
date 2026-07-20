#!/bin/bash
# AI 日报生成 Agent v2.0 - 真正的 AI Agent
# 使用 OpenClaw Cron 系统

set -e

TODAY=$(date +%Y%m%d)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
JOB_NAME="daily-reporter-v2"
LOG_FILE="${HOME}/clawd/ai-agents/daily-reporter/logs/${JOB_NAME}-${TODAY}.log"

mkdir -p "$(dirname $LOG_FILE)"

echo "🤖 AI 日报生成 Agent v2.0 启动"
echo "================================"
echo "日期: $(date)"
echo "Agent: ${JOB_NAME}"
echo ""

# 记录日志
exec > >(tee -a "$LOG_FILE")

# 步骤 1: 准备数据
echo "📂 步骤 1: 准备数据..."
echo ""

# 查找最新的 AI 研究数据
LATEST_FILE=$(ls -t ~/clawd/memory/ai-research/AI_news_*.json 2>/dev/null | head -1)

if [ -z "$LATEST_FILE" ]; then
    echo "❌ 错误: 未找到 AI 研究数据文件"
    echo "提示: 确保 ~/clawd/memory/ai-research/ 目录中有数据文件"
    exit 1
fi

echo "✅ 找到数据文件: $(basename $LATEST_FILE)"

# 统计数据
ARTICLE_COUNT=$(grep -o '"title"' "$LATEST_FILE" 2>/dev/null | wc -l)
echo "✅ 文章数量: $ARTICLE_COUNT"

# 复制数据到工作目录
WORK_DIR="${HOME}/clawd/ai-agents/daily-reporter/work/${TODAY}"
mkdir -p "$WORK_DIR"

cp "$LATEST_FILE" "$WORK_DIR/input-data.json"
echo "✅ 数据已复制到工作目录: $WORK_DIR"
echo ""

# 步骤 2: 生成 Agent 任务描述
echo "📝 步骤 2: 生成 Agent 任务描述..."
echo ""

cat > "$WORK_DIR/agent-task.md" << 'TASK'
# AI 日报分析任务

## 任务目标
分析今天收集的 AI 新闻数据，生成一份有洞察力的日报。

## 输入数据
- 文件: ~/clawd/ai-agents/daily-reporter/work/{{DATE}}/input-data.json
- 格式: JSON
- 文章数量: {{ARTICLE_COUNT}}

## 分析要求

### 1. 热点识别 (Top 3-5)
找出今天最热门的 3-5 个 AI 话题，包括：
- 话题名称
- 关键词/标签
- 文章数量
- 简要说明

### 2. 趋势分析 (2-3 个洞察)
识别重要的技术趋势和行业动向，包括：
- 趋势名称
- 重要性说明
- 可能的影响

### 3. 公司动态 (3-5 个)
关注主要 AI 公司的重大发布和新闻：
- 公司名称
- 事件描述
- 重要性评级

### 4. 技术突破 (2-3 个)
识别重要的技术进展：
- 技术名称
- 突破点
- 应用场景

## 输出格式

请按以下格式生成分析报告：

### 📊 数据概览
（统计信息）

### 🔥 今日热点 (Top 3-5)
（热点列表）

### 📈 趋势洞察 (2-3 个)
（趋势分析）

### 🏢 公司动态 (3-5 个)
（公司新闻）

### 🔬 技术突破 (2-3 个)
（技术进展）

## 输出文件
请将分析报告保存到:
~/clawd/ai-agents/daily-reporter/work/{{DATE}}/ai-analysis-report.md

请使用中文撰写报告。
TASK

# 替换占位符
sed -i "s/{{DATE}}/${TODAY}/g" "$WORK_DIR/agent-task.md"
sed -i "s/{{ARTICLE_COUNT}}/${ARTICLE_COUNT}/g" "$WORK_DIR/agent-task.md"

echo "✅ Agent 任务描述已创建: $WORK_DIR/agent-task.md"
echo ""

# 步骤 3: 配置 OpenClaw Cron 任务
echo "⏰ 步骤 3: 配置 OpenClaw Cron 任务..."
echo ""

# 检查是否已存在同名 cron 任务
EXISTING_CRON=$(openclaw cron list --json 2>/dev/null | grep -o "\"id\":\"[^\"]*\"" | grep -o "[^:]*$" | grep "$JOB_NAME" || echo "")

if [ -n "$EXISTING_CRON" ]; then
    echo "⚠️  Cron 任务 '$JOB_NAME' 已存在，将更新任务"
    # 删除旧任务
    openclaw cron rm "$EXISTING_CRON" 2>&1 | grep -E "(removed|deleted|✅)" || echo "   已删除旧任务"
else
    echo "✅  Cron 任务 '$JOB_NAME' 不存在，将创建新任务"
fi
echo ""

# 创建新的 cron 任务
CRON_SCHEDULE="0 9 * * *"  # 每天早上 9 点运行
AGENT_MESSAGE="请阅读 $WORK_DIR/agent-task.md 中的任务描述，然后完成 AI 新闻分析。数据文件在 $WORK_DIR/input-data.json"

echo "🚀 正在创建 Cron 任务..."
echo "   调度: $CRON_SCHEDULE"
echo "   任务: AI 日报分析"
echo ""

# 使用 openclaw cron add 创建任务
CRON_OUTPUT=$(openclaw cron add \
    --name "$JOB_NAME" \
    --schedule "$CRON_SCHEDULE" \
    --message "$AGENT_MESSAGE" 2>&1)

if echo "$CRON_OUTPUT" | grep -qE "(added|created|✅|success)"; then
    echo "✅ Cron 任务创建成功！"
else
    echo "❌ Cron 任务创建失败"
    echo "   输出: $CRON_OUTPUT"
    exit 1
fi
echo ""

# 步骤 4: 立即运行一次（测试）
echo "🧪 步骤 4: 立即运行一次（测试）..."
echo ""

echo "🚀 正在运行任务 '$JOB_NAME'..."
RUN_OUTPUT=$(openclaw cron run "$JOB_NAME" 2>&1)
echo "$RUN_OUTPUT"
echo ""

if echo "$RUN_OUTPUT" | grep -qE "(error|failed|❌)"; then
    echo "⚠️  任务运行可能有问题，请检查日志"
else
    echo "✅  任务运行完成！"
fi
echo ""

# 步骤 5: 查看结果
echo "📊 步骤 5: 查看分析结果..."
echo ""

# 查找 AI 分析报告
ANALYSIS_FILE="$WORK_DIR/ai-analysis-report.md"
if [ -f "$ANALYSIS_FILE" ]; then
    echo "✅ 找到 AI 分析报告"
    HAS_AI_ANALYSIS=true
    echo "   文件: $ANALYSIS_FILE"
    echo "   大小: $(du -h "$ANALYSIS_FILE" | cut -f1)"
else
    echo "⚠️  未找到 AI 分析报告"
    echo "   预期位置: $ANALYSIS_FILE"
    HAS_AI_ANALYSIS=false
fi
echo ""

# 步骤 6: 生成最终日报
echo "📝 步骤 6: 生成最终日报..."
echo ""

REPORT_FILE="${HOME}/clawd/ai-agents/daily-reporter/output/daily-report-${TODAY}-${TIMESTAMP}.md"
mkdir -p "$(dirname $REPORT_FILE)"

# 提取日期
FILE_DATE=$(basename "$LATEST_FILE" | grep -oP '\d{8}' | head -1)
if [ -n "$FILE_DATE" ]; then
    FORMATTED_DATE="${FILE_DATE:0:4}年${FILE_DATE:4:2}月${FILE_DATE:6:2}日"
else
    FORMATTED_DATE=$(date +%Y年%m月%d日)
fi

# 生成最终报告
cat > "$REPORT_FILE" << REPORT
# 🤖 AI 日报 - ${FORMATTED_DATE}

> **生成时间**: $(date "+%Y-%m-%d %H:%M:%S")  
> **Agent 版本**: v2.0 (OpenClaw AI Agent)  
> **数据来源**: $(basename $LATEST_FILE)

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| **文章总数** | ${ARTICLE_COUNT} 篇 |
| **数据日期** | ${FORMATTED_DATE} |
| **数据文件** | \`$(basename $LATEST_FILE)\` |
| **分析状态** | $([ "$HAS_AI_ANALYSIS" = true ] && echo "✅ AI 分析完成" || echo "⚠️  AI 分析未完成") |

---

REPORT

# 如果有 AI 分析，添加分析内容
if [ "$HAS_AI_ANALYSIS" = true ]; then
    echo "📝 正在整合 AI 分析内容..."
    echo "" >> "$REPORT_FILE"
    echo "## 🧠 AI 智能分析" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    cat "$ANALYSIS_FILE" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "---" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# 添加页脚
cat >> "$REPORT_FILE" << FOOTER
## 📁 相关文件

- **原始数据**: \`${LATEST_FILE}\`
- **工作目录**: \`${WORK_DIR}\`
- **任务描述**: \`${WORK_DIR}/agent-task.md\`
- **AI 分析**: \`${ANALYSIS_FILE}\` $([ "$HAS_AI_ANALYSIS" = true ] && echo "✅" || echo "❌")
- **日志文件**: \`${LOG_FILE}\`

## ⏰ Cron 任务

- **任务名称**: \`${JOB_NAME}\`
- **调度时间**: \`每天 09:00\`
- **状态**: 运行中

---

*本报告由 AI 日报生成 Agent v2.0 自动生成*  
*使用 OpenClaw AI Agent 技术栈*

**查看更多 Cron 任务**: \`openclaw cron list\`
**查看 Agent 运行历史**: \`openclaw cron runs --name ${JOB_NAME}\`

FOOTER

echo "✅ 日报生成完成！"
echo "📄 报告位置: $REPORT_FILE"
echo ""

# 步骤 7: 显示摘要
echo "================================"
echo "📊 执行摘要"
echo "================================"
echo "Agent 名称: AI 日报生成 Agent v2.0"
echo "运行时间: $(date)"
echo "数据文件: $(basename $LATEST_FILE)"
echo "文章数量: $ARTICLE_COUNT"
echo "AI 分析: $([ "$HAS_AI_ANALYSIS" = true ] && echo "已完成 ✅" || echo "未完成 ⚠️")"
echo "报告文件: $REPORT_FILE"
echo "Cron 任务: $JOB_NAME (每天 09:00)"
echo "================================"
echo ""

# 显示报告预览
echo "📝 报告预览 (前60行):"
echo "==================================="
head -60 "$REPORT_FILE"
echo "==================================="
echo ""
echo "💡 提示:"
echo "   查看完整报告: cat $REPORT_FILE"
echo "   查看 Cron 任务: openclaw cron list"
echo "   查看 Cron 运行历史: openclaw cron runs --name ${JOB_NAME}"
echo "   手动运行: openclaw cron run ${JOB_NAME}"
echo ""
