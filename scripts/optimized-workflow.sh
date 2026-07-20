#!/bin/bash
# 集成工作流优化版 - 只评估 20 个提示词

set -e

echo "========================================="
echo "🚀 优化的 AI 提示词工作流"
echo "========================================="
echo ""
echo "优化策略："
echo "  • 搜索查询：15 个（vs 67 个）"
echo "  • 评估限制：20 个（vs 全部）"
echo "  • 启发式过滤：启用"
echo "  • 预期 API 调用：20 次（vs 500+ 次）"
echo ""

# Stage 1: 使用优化的收集脚本
echo ""
echo "========================================="
echo "Stage 1: 数据收集（优化版）"
echo "========================================="

python3 /root/clawd/scripts/collect_prompts_optimized.py

if [ $? -ne 0 ]; then
    echo "❌ 数据收集失败"
    exit 1
fi

# 找到最新的收集文件
LATEST_FILE=$(ls -t /root/clawd/data/prompts/collected/prompts-optimized-*.jsonl | head -1)

if [ ! -f "$LATEST_FILE" ]; then
    echo "❌ 未找到收集文件"
    exit 1
fi

echo ""
echo "✅ 收集文件: $LATEST_FILE"

# 统计提示词数量
PROMPT_COUNT=$(wc -l < "$LATEST_FILE")
echo "✅ 收集提示词数: $PROMPT_COUNT"

if [ "$PROMPT_COUNT" -eq 0 ]; then
    echo "❌ 没有收集到提示词"
    exit 1
fi

# Stage 2: LLM 评估（只评估前 20 个）
echo ""
echo "========================================="
echo "Stage 2: LLM 评估（只评估前 20 个）"
echo "========================================="

# 提取前 20 个提示词用于评估
TOP_20_FILE="/tmp/prompts-eval-$(date +%Y%m%d-%H%M%S).jsonl"

head -20 "$LATEST_FILE" > "$TOP_20_FILE"

echo "✅ 选择前 20 个提示词进行评估"
echo "✅ 临时文件: $TOP_20_FILE"

# 创建评估输出文件
EVAL_OUTPUT="/root/clawd/skills/x-prompt-hunter/data/evaluation_results.json"
mkdir -p /root/clawd/skills/x-prompt-hunter/data

# TODO: 这里应该调用 x-prompt-hunter 的评估功能
# 但由于需要 API 密钥配置，我们暂时跳过
echo ""
echo "⚠️  LLM 评估需要 API 密钥配置"
echo "   请确保 ANTHROPIC_API_KEY 已设置"
echo ""
echo "评估文件: $TOP_20_FILE"
echo "输出文件: $EVAL_OUTPUT"

# Stage 3: 转换为 Skills
echo ""
echo "========================================="
echo "Stage 3: 转换为 Skills（质量过滤）"
echo "========================================="

# 暂时跳过转换
echo "⚠️  转换功能需要进一步开发"
echo ""

# 生成报告
REPORT_FILE="/root/clawd/reports/optimized-workflow-report-$(date +%Y%m%d-%H%M%S).md"

cat > "$REPORT_FILE" << EOF
# 优化的 AI 提示词工作流报告

**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 📊 流程统计

| 阶段 | 状态 | 详情 |
|------|------|------|
| Stage 1 | ✅ 完成 | 收集 $PROMPT_COUNT 个提示词 |
| Stage 2 | ⏸️ 待配置 | 需要设置 ANTHROPIC_API_KEY |
| Stage 3 | ⏸️ 待配置 | 需要开发转换功能 |

## 🎯 优化效果

| 指标 | 优化前 | 优化后 | 改进 |
|------|--------|--------|------|
| 搜索查询数 | 67 个 | 15 个 | ↓ 78% |
| LLM 评估数 | 500+ 次 | 20 次 | ↓ 96% |
| API 成本 | 高 | 低 | ↓ 95% |

## 📂 文件位置

- **收集文件**: $LATEST_FILE
- **评估文件**: $TOP_20_FILE
- **报告文件**: $REPORT_FILE

## 💡 下一步

1. 配置 ANTHROPIC_API_KEY
2. 运行 LLM 评估
3. 开发转换功能
4. 发布到 ClawdHub

---

*优化版工作流*
EOF

echo ""
echo "========================================="
echo "✅ 报告已生成: $REPORT_FILE"
echo "========================================="
echo ""
echo "📊 查看报告:"
echo "  cat $REPORT_FILE"
echo ""
echo "🚀 下一步：配置 API 密钥并运行评估"
