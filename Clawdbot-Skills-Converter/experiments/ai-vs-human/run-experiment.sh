#!/bin/bash

# 主实验运行脚本
# 执行 Claude Code vs 24-Hour AI 完整实验

set -e

PROJECT_DIR="/root/clawd/experiments/ai-vs-human"
START_TIME=$(date +%s)
TODAY=$(date +%Y-%m-%d)

echo "╔════════════════════════════════════╗"
echo "║  🧪 Claude Code vs 24-Hour AI 实验║"
echo "╚═════════════════════════════════════╝"
echo ""
echo "📅 实验日期: $TODAY"
echo "🎯 测试项目: Ultimate Todo App"
echo "⏱️ 开始时间: $(date '+%H:%M:%S')"
echo ""

# 创建结果目录
mkdir -p "$PROJECT_DIR/results"

# 阶段 1: 运行 Claude Code 完整流程
echo "╔════════════════════════════════════╗"
echo "║  📋 阶段 1: Claude Code 完整工作流    ║"
echo "╚═════════════════════════════════════╝"
echo ""

cd "$PROJECT_DIR"
bash ./run-claude.sh 2>&1 | tee results/claude-run.log

CLAUDE_DURATION=$((SECONDS))
echo ""
echo "✅ Claude Code 完整流程完成"
echo "⏱️  耗时: ${CLAUDE_DURATION} 秒 (${CLAUDE_DURATION} 分钟)"
echo ""

sleep 2

# 阶段 2: 运行 24-Hour AI 任务
echo "╔════════════════════════════════════╗"
echo "║  🤖 阶段 2: 24-Hour AI 完整任务     ║"
echo "╚═══════════════════════════════════════╝"
echo ""

bash ./run-24hour-ai.sh 2>&1 | tee results/24hour-ai-run.log

AI24_DURATION=$((SECONDS - CLAUDE_DURATION))
echo ""
echo "✅ 24-Hour AI 完整任务完成"
echo "⏱️  耗时: ${AI24_DURATION} 秒 (${AI24_DURATION} 分钟)"
echo ""

sleep 2

# 阶段 3: 评估和报告
echo "╔════════════════════════════════════╗"
echo "║  📊 阶段 3: 评估和报告生成       ║"
echo "╚═══════════════════════════════════════╝"
echo ""

bash ./evaluate-and-report.sh 2>&1 | tee results/evaluation.log

EVALUATION_DURATION=$((SECONDS - CLAUDE_DURATION - AI24_DURATION))
echo ""
echo "✅ 评估和报告生成完成"
echo "⏱️  耗时: ${EVALUATION_DURATION} 秒 (${EVALUATION_DURATION} 分钟)"
echo ""

# 总时间
TOTAL_DURATION=$(date +%s | head -1 | awk '{print $1 - '$START_TIME'}')

echo "╔════════════════════════════════════╗"
echo "║  ✅ 实验完成！                       ║"
echo "╚═════════════════════════════════════╝"
echo ""
echo "⏱️  总耗时: ${TOTAL_DURATION} 秒 ($(date -u -d @$TOTAL_DURATION +%H:%M:%S))"
echo ""
echo "📋 阶段总结:"
echo "   1. Claude Code 完整工作流: ${CLAUDE_DURATION} 秒"
echo "   2. 24-Hour AI 完整任务: ${AI24_DURATION} 秒"
echo "   3. 评估和报告生成: ${EVALUATION_DURATION} 秒"
echo ""
echo "📁 生成的文件:"
echo "   - results/claude-run.log"
echo "   - results/24hour-ai-run.log"
echo "   - results/evaluation.log"
echo "   - claude-code-result/*.md (详细结果）"
echo "   - 24hour-ai-result/*.md (详细结果）"
echo "   - report/comparison-report.md (对比报告）"
echo ""
echo "📊 总体结果:"
echo "   - Claude Code 得分: $(grep '总分' report/comparison-report.md | head -1 | awk '{print $NF}')"
echo "   - 24-Hour AI 得分: $(grep '总分' report/comparison-report.md | tail -1 | awk '{print $NF}')"
echo "   - Claude Code 领先: $(grep '差距' report/comparison-report.md | head -1 | awk '{print $NF}')"
echo ""
echo "🎉 实验数据收集完成！"
echo ""
echo "📊 查看详细报告:"
echo "   cat report/comparison-report.md"
echo ""
echo "🚀 下一步:"
echo "   1. 审查实验结果"
echo "   2. 根据发现优化技能"
echo "   3. 创建新的实验"
echo "   4. 分享发现到社区"
echo ""
