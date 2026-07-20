#!/bin/bash

# 阶段 2: 生成 PPT
# 使用阶段 1 保存的 ID

set -e

# 配置
export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"

# 参数
IDS_FILE="$1"

if [ -z "$IDS_FILE" ]; then
    echo "❌ 请提供 ID 文件"
    echo "用法: bash ai-content-creator-stage2.sh <ids-file>"
    exit 1
fi

# 读取 ID
source "$IDS_FILE"

echo "========================================"
echo "阶段 2: 生成 PPT"
echo "========================================"
echo "query_id: $QUERY_ID"
echo "chat_id: $CHAT_ID"
echo "title: $TITLE"
echo "query: $QUERY"
echo "开始时间: $(date)"
echo ""

# 输出目录
OUTPUT_DIR="/root/clawd/memory/ai-content-creator"
mkdir -p "$OUTPUT_DIR"

# 生成 PPT
echo "正在生成 PPT，这可能需要 2-5 分钟..."

cd /root/clawd/skills/ai-ppt-generate/scripts

PPT_OUTPUT_FILE="${OUTPUT_DIR}/ppt-raw-${TIMESTAMP}.txt"
timeout 300 python3 ppt_generate.py \
  --query_id "$QUERY_ID" \
  --chat_id "$CHAT_ID" \
  --query "$QUERY" \
  --title "$TITLE" \
  --style_id 0 \
  --tpl_id 3 > "$PPT_OUTPUT_FILE" 2>&1

# 提取 PPT 下载链接
PPT_URL=$(grep '"pptx_url"' "$PPT_OUTPUT_FILE" | head -1 | sed 's/.*"pptx_url":"\([^"]*\)".*/\1/')

if [ -z "$PPT_URL" ]; then
    echo "❌ PPT 生成失败：无法提取 pptx_url"
    exit 1
fi

# 修复协议（https:// → http://）
PPT_URL_HTTP=$(echo "$PPT_URL" | sed 's|^https://|http://|')

echo "✅ PPT 生成完成"
echo "PPT 下载链接: $PPT_URL_HTTP"
echo ""

# 保存结果
RESULT_FILE="${OUTPUT_DIR}/workflow-${TIMESTAMP}.json"
cat > "$RESULT_FILE" << EOF
{
  "workflow": "$TIMESTAMP",
  "query": "$QUERY",
  "title": "$TITLE",
  "steps": [
    {
      "step": 1,
      "name": "生成 PPT 大纲",
      "status": "completed",
      "query_id": "$QUERY_ID",
      "chat_id": "$CHAT_ID"
    },
    {
      "step": 2,
      "name": "生成 PPT",
      "status": "completed",
      "ppt_url": "$PPT_URL_HTTP"
    }
  ],
  "result": {
    "ppt_download_url": "$PPT_URL_HTTP"
  }
}
EOF

echo ""
echo "========================================"
echo "工作流完成！"
echo "========================================"
echo ""
echo "结束时间: $(date)"
echo ""
echo "📥 PPT 下载链接:"
echo "$PPT_URL_HTTP"
echo ""
echo "结果文件: $RESULT_FILE"
