#!/bin/bash
# AI 日报生成 Agent v2.0 - 真正的 AI Agent
# 使用 OpenClaw sub-agents 进行智能分析

set -e

TODAY=$(date +%Y%m%d)
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
AGENT_NAME="ai-daily-reporter-${TODAY}"

echo "🤖 AI 日报生成 Agent v2.0 启动"
echo "================================"
echo "日期: $(date)"
echo "Agent ID: ${AGENT_NAME}"
echo ""

# 步骤 1: 准备数据
echo "📂 步骤 1: 准备数据..."

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
echo "📊 文章数量: $ARTICLE_COUNT"

# 复制数据到工作目录
WORK_DIR="${HOME}/clawd/ai-agents/daily-reporter/work/${TODAY}"
mkdir -p "$WORK_DIR"

cp "$LATEST_FILE" "$WORK_DIR/input-data.json"
echo "✅ 数据已复制到工作目录: $WORK_DIR"
echo ""

# 步骤 2: 使用 OpenClaw sub-agent 进行 AI 分析
echo "🧠 步骤 2: 启动 AI 分析 sub-agent..."

cat > "$WORK_DIR/analysis-task.md" << 'TASK'
## 任务：分析今天的 AI 新闻数据

### 输入数据
- 文件: ~/clawd/ai-agents/daily-reporter/work/{{DATE}}/input-data.json
- 格式: JSON
- 内容: AI 新闻文章集合

### 分析要求
1. **热点识别**: 找出今天最热门的 3-5 个 AI 话题
2. **趋势分析**: 识别重要的技术趋势和行业动向
3. **公司动态**: 关注主要 AI 公司的重大发布
4. **技术突破**: 识别重要的技术进展

### 输出格式
请生成一份结构化的分析报告，包含：
1. **今日热点** (Top 3-5)
2. **趋势洞察** (2-3 个关键趋势)
3. **值得关注** (2-3 个重点)
4. **详细分析** (展开说明)

### 输出文件
请将分析报告保存到:
~/clawd/ai-agents/daily-reporter/work/{{DATE}}/ai-analysis-report.md

请使用中文撰写报告。
TASK

# 替换日期占位符
sed -i "s/{{DATE}}/${TODAY}/g" "$WORK_DIR/analysis-task.md"

echo "📝 任务描述已创建: $WORK_DIR/analysis-task.md"
echo ""

# 启动 sub-agent 进行分析
echo "🚀 正在启动 OpenClaw sub-agent 进行 AI 分析..."
echo "   (这可能需要 30-60 秒)"
echo ""

# 使用 sessions_spawn 创建 sub-agent
openclaw sessions_spawn \
    --task "请阅读 $WORK_DIR/analysis-task.md 中的任务描述，然后完成 AI 新闻分析任务。输入数据在 $WORK_DIR/input-data.json" \
    --mode run \
    --label "ai-analyst-${TODAY}" \
    --timeout-seconds 120

SUBAGENT_EXIT_CODE=$?

echo ""
echo "📊 Sub-agent 分析完成 (退出码: $SUBAGENT_EXIT_CODE)"
echo ""

# 步骤 3: 生成最终日报
echo "📝 步骤 3: 生成最终日报..."

REPORT_FILE="${HOME}/clawd/ai-agents/daily-reporter/output/daily-report-${TODAY}-${TIMESTAMP}.md"
mkdir -p "$(dirname $REPORT_FILE)"

# 检查是否有 AI 分析报告
ANALYSIS_FILE="$WORK_DIR/ai-analysis-report.md"
if [ -f "$ANALYSIS_FILE" ]; then
    echo "✅ 找到 AI 分析报告"
    HAS_AI_ANALYSIS=true
else
    echo "⚠️  未找到 AI 分析报告，将使用基础统计"
    HAS_AI_ANALYSIS=false
fi

# 生成最终报告
cat > "$REPORT_FILE" << REPORT
# 🤖 AI 日报 - $(date +%Y年%m月%d日)

> **生成时间**: $(date "+%Y-%m-%d %H:%M:%S")  
> **Agent 版本**: v2.0 (OpenClaw AI Agent)  
> **数据来源**: $(basename $LATEST_FILE)

---

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| **文章总数** | ${ARTICLE_COUNT} 篇 |
| **数据日期** | ${FORMATTED_DATE} |
| **分析方式** | $([ "$HAS_AI_ANALYSIS" = true ] && echo "AI 智能分析" || echo "统计分析") |

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
- **AI 分析**: \`${ANALYSIS_FILE}\` $([ "$HAS_AI_ANALYSIS" = true ] && echo "✅" || echo "❌")

---

*本报告由 AI 日报生成 Agent v2.0 自动生成*  
*使用 OpenClaw AI Agent 技术栈*
FOOTER

echo "✅ 日报生成完成！"
echo "📄 报告位置: $REPORT_FILE"
echo ""

# 步骤 4: 显示摘要
echo "================================"
echo "📊 执行摘要"
echo "================================"
echo "Agent 名称: AI 日报生成 Agent v2.0"
echo "运行时间: $(date)"
echo "数据文件: $(basename $LATEST_FILE)"
echo "文章数量: $ARTICLE_COUNT"
echo "AI 分析: $([ "$HAS_AI_ANALYSIS" = true ] && echo "已完成 ✅" || echo "未完成 ⚠️")"
echo "报告文件: $REPORT_FILE"
echo "================================"
echo ""

# 显示报告预览
echo "📝 报告预览 (前50行):"
echo "=================================="
head -50 "$REPORT_FILE"
echo "=================================="
echo ""
echo "💡 查看完整报告:"
echo "   cat $REPORT_FILE"
