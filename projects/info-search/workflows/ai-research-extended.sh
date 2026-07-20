#!/bin/bash
# AI 研究工作流 - 扩展版（支持自定义搜索主题）

set -e

# 加载共享配置
CONFIG_DIR="/root/clawd/.config/data-sources"
TAVILY_CONF="$CONFIG_DIR/tavily.conf"

# 检查配置文件
if [ ! -f "$TAVILY_CONF" ]; then
    echo "❌ Tavily 配置文件不存在: $TAVILY_CONF"
    exit 1
fi

source "$TAVILY_CONF"

# 配置
OUTPUT_DIR="/root/clawd/memory/ai-research"
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$OUTPUT_DIR/ai-research-$TIMESTAMP.log"
SUMMARY_FILE="$OUTPUT_DIR/ai-research-summary-$TIMESTAMP.md"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 默认搜索主题（扩大版 - 15 个核心主题）
# 免费额度：1,000 次/月
# 每天调用：15 个主题 × 5 条结果 = 75 次
# 可用天数：1,000 ÷ 75 = 13 天
# ⚠️ 如果超过免费额度，建议减少主题数量
DEFAULT_SEARCH_TOPICS=(
    # AI 模型和平台更新
    "Claude AI updates 2026"
    "OpenAI GPT-5 news"
    "Google Gemini AI news 2026"
    "Anthropic Claude Sonnet 2026"
    "Meta Llama AI news 2026"

    # AI 技术和应用
    "AI agents 2026"
    "multimodal AI 2026"
    "AI coding tools 2026"
    "AI automation workflow 2026"
    "AI skill development 2026"

    # AI 商业化和产品
    "AI startup trends 2026"
    "AI business ideas 2026"
    "AI monetization 2026"
    "AI product development 2026"
    "AI market opportunities 2026"
)

# 备选主题（每周轮换，可选）
WEEKLY_TOPICS=(
    # 技术专题
    "AI prompt engineering best practices"
    "AI model fine-tuning 2026"
    "AI RAG implementation 2026"
    "AI function calling 2026"
    "AI memory systems 2026"
    "AI context management 2026"

    # 应用专题
    "AI for content creation"
    "AI for data analysis"
    "AI for customer service"
    "AI for marketing automation"
    "AI for productivity tools"

    # 商业专题
    "AI pricing models 2026"
    "AI user acquisition 2026"
    "AI SaaS growth strategies"
    "AI product launches 2026"
    "AI case studies 2026"
)

# 支持自定义搜索主题
if [ -n "$SEARCH_TOPICS" ]; then
    IFS=',' read -ra TOPICS <<< "$SEARCH_TOPICS"
    SEARCH_TOPICS=("${TOPICS[@]}")
elif [ "$ENABLE_WEEKLY_TOPICS" = "true" ]; then
    # 根据星期几选择备选主题
    DAY_OF_WEEK=$(date +%u)  # 1-7 (Mon-Sun)
    WEEKLY_INDEX=$(( (DAY_OF_WEEK - 1) % ${#WEEKLY_TOPICS[@]} ))
    SEARCH_TOPICS=("${DEFAULT_SEARCH_TOPICS[@]}" "${WEEKLY_TOPICS[$WEEKLY_INDEX]}")
    echo "📅 本周备选主题: ${WEEKLY_TOPICS[$WEEKLY_INDEX]}"
else
    SEARCH_TOPICS=("${DEFAULT_SEARCH_TOPICS[@]}")
fi

echo "=========================================="
echo "AI 研究工作流 - 扩展版"
echo "=========================================="
echo ""
echo "配置："
echo "  API Key: ${TAVILY_API_KEY:0:15}..."
echo "  输出目录: $OUTPUT_DIR"
echo "  日志文件: $LOG_FILE"
echo "  摘要文件: $SUMMARY_FILE"
echo "  搜索主题数量: ${#SEARCH_TOPICS[@]}"
echo ""

# 初始化摘要文件
cat > "$SUMMARY_FILE" << EOF
# AI 研究搜索摘要

**日期**: $TODAY
**时间**: $(date +%H:%M:%S)
**搜索主题数量**: ${#SEARCH_TOPICS[@]}

---

EOF

# 统计信息
TOTAL_RESULTS=0
declare -A TOPIC_RESULTS

# 执行搜索
echo "开始搜索..."
echo "" >> "$LOG_FILE"
echo "AI 研究搜索 - $TODAY" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

for i in "${!SEARCH_TOPICS[@]}"; do
    topic="${SEARCH_TOPICS[$i]}"
    topic_num=$((i + 1))

    echo "[$topic_num/${#SEARCH_TOPICS[@]}] 搜索: $topic"
    echo "" >> "$LOG_FILE"
    echo "## 搜索 $topic_num: $topic" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"

    # 执行搜索
    RESULT_COUNT=$(python3 << EOF
from tavily import TavilyClient
from datetime import datetime
import json

client = TavilyClient(api_key="$TAVILY_API_KEY")
result = client.search("$topic", max_results=5, search_depth="advanced")

results = result.get('results', [])
print(f"{len(results)}")

# 保存到日志
with open("$LOG_FILE", 'a', encoding='utf-8') as f:
    f.write(f"时间: {datetime.now().isoformat()}\n")
    f.write(f"搜索词: $topic\n")
    f.write(f"结果数量: {len(results)}\n")
    f.write("\n")

    for i, item in enumerate(results, 1):
        f.write(f"### 结果 {i}\n\n")
        f.write(f"**标题**: {item.get('title', 'N/A')}\n\n")
        f.write(f"**URL**: {item.get('url', 'N/A')}\n\n")
        f.write(f"**内容**: {item.get('content', 'N/A')[:500]}...\n\n")
        f.write("---\n\n")

EOF
)

    echo "  ✅ 找到 $RESULT_COUNT 条结果"

    # 更新统计
    TOTAL_RESULTS=$((TOTAL_RESULTS + RESULT_COUNT))
    TOPIC_RESULTS["$topic"]="$RESULT_COUNT"

    # 添加到摘要
    cat >> "$SUMMARY_FILE" << EOF
## 搜索 $topic_num: $topic

- **结果数量**: $RESULT_COUNT
- **关键词**: $topic

EOF

    echo "" >> "$LOG_FILE"
done

# 生成统计摘要
cat >> "$SUMMARY_FILE" << EOF

---

## 统计摘要

- **总搜索主题**: ${#SEARCH_TOPICS[@]}
- **总结果数量**: $TOTAL_RESULTS
- **平均结果数量**: $((TOTAL_RESULTS / ${#SEARCH_TOPICS[@]}))

## 搜索主题列表

EOF

for i in "${!SEARCH_TOPICS[@]}"; do
    topic="${SEARCH_TOPICS[$i]}"
    count="${TOPIC_RESULTS[$topic]}"
    echo "- **$topic**: $count 条结果" >> "$SUMMARY_FILE"
done

echo ""
echo "=========================================="
echo "✅ 搜索完成！"
echo "=========================================="
echo ""
echo "统计信息："
echo "  总搜索主题: ${#SEARCH_TOPICS[@]}"
echo "  总结果数量: $TOTAL_RESULTS"
echo "  平均结果数量: $((TOTAL_RESULTS / ${#SEARCH_TOPICS[@]}))"
echo ""
echo "结果已保存到:"
echo "  - 日志文件: $LOG_FILE"
echo "  - 摘要文件: $SUMMARY_FILE"
echo ""

# 输出最新日志文件路径（供其他脚本使用）
echo "$SUMMARY_FILE" > "$OUTPUT_DIR/latest-summary.txt"
echo "$LOG_FILE" > "$OUTPUT_DIR/latest-log.txt"

# 推送摘要报告（可选）
if [ "$PUSH_SUMMARY" = "true" ]; then
    echo ""
    echo "推送摘要报告到 Slack/Feishu..."
    bash /root/clawd/projects/info-search/workflows/push-ai-research-summary.sh || echo "⚠️  推送失败（继续执行）"
fi
