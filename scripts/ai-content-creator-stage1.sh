#!/bin/bash

# 阶段 1: 生成 PPT 大纲
# 只生成大纲，保存 ID

set -e

# 配置
export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"

# 参数
QUERY="${1:-AI技术发展趋势2026}"

# 输出目录
OUTPUT_DIR="/root/clawd/memory/ai-content-creator"
mkdir -p "$OUTPUT_DIR"

# 时间戳
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
IDS_FILE="${OUTPUT_DIR}/ppt-ids-${TIMESTAMP}.txt"

echo "========================================"
echo "阶段 1: 生成 PPT 大纲"
echo "========================================"
echo "搜索主题: $QUERY"
echo "开始时间: $(date)"
echo ""

cd /root/clawd/skills/ai-ppt-generate/scripts

# 生成大纲，只保存到文件，不打印到 stdout
echo "正在生成大纲..."
timeout 60 python3 ppt_outline_generate.py --query "$QUERY" > "${OUTPUT_DIR}/outline-raw-${TIMESTAMP}.txt" 2>&1

# 提取 ID（使用简单的方法）
# 查找最后包含非空 query_id 和 chat_id 的 JSON 对象
QUERY_ID=$(grep '"query_id"' "${OUTPUT_DIR}/outline-raw-${TIMESTAMP}.txt" | grep -v '": ""' | grep -v '": ""' | tail -1 | sed 's/.*"query_id":"\([^"]*\)".*/\1/' | head -1)
CHAT_ID=$(grep '"chat_id"' "${OUTPUT_DIR}/outline-raw-${TIMESTAMP}.txt" | grep -v '": ""' | grep -v '": ""' | tail -1 | sed 's/.*"chat_id":"\([^"]*\)".*/\1/' | head -1)
TITLE=$(grep '"title"' "${OUTPUT_DIR}/outline-raw-${TIMESTAMP}.txt" | grep -v '": ""' | grep -v '": ""' | tail -1 | sed 's/.*"title":"\([^"]*\)".*/\1/' | head -1 | sed 's/\\n/ /g')

if [ -z "$QUERY_ID" ] || [ "$QUERY_ID" = "" ]; then
    echo "❌ 无法提取 query_id"
    exit 1
fi

if [ -z "$CHAT_ID" ] || [ "$CHAT_ID" = "" ]; then
    echo "❌ 无法提取 chat_id"
    exit 1
fi

echo "✅ 大纲生成完成"
echo "query_id: $QUERY_ID"
echo "chat_id: $CHAT_ID"
echo "title: $TITLE"
echo ""

# 保存 ID 到文件
cat > "$IDS_FILE" << EOF
QUERY_ID=$QUERY_ID
CHAT_ID=$CHAT_ID
TITLE=$TITLE
QUERY=$QUERY
TIMESTAMP=$TIMESTAMP
EOF

echo "ID 已保存到: $IDS_FILE"
echo ""
echo "运行阶段 2: bash /root/clawd/scripts/ai-content-creator-stage2.sh $IDS_FILE"
