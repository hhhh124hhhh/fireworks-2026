#!/bin/bash
# 简化的 AI 搜索脚本 - 避免卡住

MEMORY_DIR="/root/clawd/memory/ai-research"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%H%M%S)

mkdir -p "$MEMORY_DIR"

echo "开始 AI 研究搜索: $(date)"

# 只搜索一个主题
TOPIC="AI news 2026"
QUERY="AI news 2026 artificial intelligence latest"
OUTPUT_JSON="$MEMORY_DIR/AI_news_${DATE}-${TIMESTAMP}.json"
OUTPUT_MD="$MEMORY_DIR/AI_news_${DATE}-${TIMESTAMP}.md"

echo "搜索主题: $TOPIC"

# 使用 curl 调用 SearXNG API，设置超时
timeout 30 curl -s "http://localhost:8080/search?format=json&q=$(echo "$QUERY" | sed 's/ /%20/g')" -o "$OUTPUT_JSON"

if [ $? -eq 0 ]; then
    echo "搜索成功，结果保存到: $OUTPUT_JSON"

    # 提取结果到 MD 文件
    echo "# AI News - $DATE" > "$OUTPUT_MD"
    echo "" >> "$OUTPUT_MD"
    echo "搜索时间: $(date)" >> "$OUTPUT_MD"
    echo "" >> "$OUTPUT_MD"

    # 检查 jq 是否可用
    if command -v jq &> /dev/null; then
        COUNT=$(jq -r '.results | length' "$OUTPUT_JSON" 2>/dev/null || echo "0")
        echo "**找到 $COUNT 个结果**" >> "$OUTPUT_MD"
        echo "" >> "$OUTPUT_MD"

        jq -r '.results[] | "- \(.title)\\n  URL: \(.url)\\n  摘要: \(.content)"' "$OUTPUT_JSON" 2>/dev/null >> "$OUTPUT_MD"
    else
        echo "jq 不可用，无法解析 JSON" >> "$OUTPUT_MD"
    fi

    echo "结果摘要保存到: $OUTPUT_MD"
else
    echo "搜索失败或超时"
    echo "# AI News - $DATE (失败)" > "$OUTPUT_MD"
    echo "" >> "$OUTPUT_MD"
    echo "搜索失败: $(date)" >> "$OUTPUT_MD"
fi

echo "完成: $(date)"
