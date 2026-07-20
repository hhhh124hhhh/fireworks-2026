#!/bin/bash

# 阶段 2: 生成 PPT (改进版)
# 使用阶段 1 保存的 ID

set -e

# 配置
export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"

# 参数
IDS_FILE="$1"

if [ -z "$IDS_FILE" ]; then
    echo "Usage: bash ai-content-creator-stage2.sh <ids-file>"
    exit 1
fi

# 读取 ID
eval $(grep -v "^#" "$IDS_FILE" | xargs)

echo "========================================"
echo "阶段 2: 生成 PPT"
echo "========================================"
echo "query_id: $QUERY_ID"
echo "chat_id: $CHAT_ID"
echo "开始时间: $(date)"
echo ""

# 输出目录
OUTPUT_DIR="/root/clawd/memory/ai-content-creator"
mkdir -p "$OUTPUT_DIR"

# 生成 PPT
echo "正在生成 PPT，这可能需要 2-5 分钟..."

cd /root/clawd/skills/ai-ppt-generate/scripts

PPT_OUTPUT_FILE="${OUTPUT_DIR}/ppt-output-${TIMESTAMP}.txt"
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
    echo "❌ PPT 生成失败"
    cat "$PPT_OUTPUT_FILE"
    exit 1
fi

# 修复协议（https:// → http://）
PPT_URL_HTTP=$(echo "$PPT_URL" | sed 's|^https://|http://|')

echo "✅ PPT 生成完成"
echo "PPT 下载链接: $PPT_URL_HTTP"
echo ""
echo "========================================"
echo "工作流完成！"
echo "========================================"
echo ""
echo "📥 PPT 下载链接:"
echo "$PPT_URL_HTTP"
echo ""
echo "结束时间: $(date)"
