#!/bin/bash
# AI 研究工作流 - 使用 Tavily Search API

set -e

# 配置
API_KEY="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"
OUTPUT_DIR="/root/clawd/memory/ai-research"
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$OUTPUT_DIR/ai-research-$TIMESTAMP.log"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "AI 研究工作流"
echo "=========================================="
echo ""
echo "配置："
echo "  API Key: ${API_KEY:0:15}..."
echo "  输出目录: $OUTPUT_DIR"
echo "  日志文件: $LOG_FILE"
echo ""

# 搜索关键词
SEARCH_TOPICS=(
    "Claude AI updates 2026"
    "OpenAI GPT-5 news"
    "AI prompt engineering best practices"
    "AI tools for developers 2026"
    "machine learning trends 2026"
)

# 执行搜索
echo "开始搜索..."
echo "" >> "$LOG_FILE"
echo "AI 研究搜索 - $TODAY" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

for topic in "${SEARCH_TOPICS[@]}"; do
    echo "搜索: $topic"
    echo "" >> "$LOG_FILE"
    echo "## 搜索: $topic" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"

    python3 << EOF
from tavily import TavilyClient
from datetime import datetime
import json

client = TavilyClient(api_key="$API_KEY")
result = client.search("$topic", max_results=5, search_depth="advanced")

print(f"  找到 {len(result.get('results', []))} 条结果")

# 保存到日志
with open("$LOG_FILE", 'a', encoding='utf-8') as f:
    f.write(f"时间: {datetime.now().isoformat()}\n")
    f.write(f"搜索词: $topic\n")
    f.write(f"结果数量: {len(result.get('results', []))}\n")
    f.write("\n")

    for i, item in enumerate(result.get('results', []), 1):
        f.write(f"### 结果 {i}\n\n")
        f.write(f"**标题**: {item.get('title', 'N/A')}\n\n")
        f.write(f"**URL**: {item.get('url', 'N/A')}\n\n")
        f.write(f"**内容**: {item.get('content', 'N/A')[:500]}...\n\n")
        f.write("---\n\n")

EOF

    echo "  ✅ 完成"
    echo "" >> "$LOG_FILE"
done

echo ""
echo "=========================================="
echo "✅ 搜索完成！"
echo "=========================================="
echo ""
echo "结果已保存到: $LOG_FILE"
