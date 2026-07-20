#!/bin/bash

# AI Content Creator 自动化工作流 (简化版)
# 流程：AI 搜索 → PPT 生成

set -e

# 配置
export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"

# 参数
QUERY="${1:-AI技术发展趋势2026}"
PPT_PAGES="${2:-10}"

# 输出目录
OUTPUT_DIR="/root/clawd/memory/ai-content-creator"
mkdir -p "$OUTPUT_DIR"

# 时间戳
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
OUTPUT_FILE="${OUTPUT_DIR}/workflow-${TIMESTAMP}.json"
LOG_FILE="${OUTPUT_DIR}/workflow-${TIMESTAMP}.log"

echo "========================================" | tee -a "$LOG_FILE"
echo "AI Content Creator 自动化工作流" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "开始时间: $(date)" | tee -a "$LOG_FILE"
echo "搜索主题: $QUERY" | tee -a "$LOG_FILE"
echo "PPT 页数: $PPT_PAGES" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 步骤 1: AI 搜索
echo "========================================" | tee -a "$LOG_FILE"
echo "步骤 1: AI 搜索" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 1.1 百度学术检索
echo "1.1 百度学术检索..." | tee -a "$LOG_FILE"
SCHOLAR_RESULT=$(curl -s -X GET "https://qianfan.baidubce.com/v2/tools/baidu_scholar/search?wd=${QUERY}&pageNum=0&enable_abstract=true" \
  -H "Authorization: Bearer $BAIDU_API_KEY" \
  -H "X-Appbuilder-From: openclaw")

SCHOLAR_COUNT=$(echo "$SCHOLAR_RESULT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('data', [])))" 2>/dev/null || echo "0")
echo "   找到论文: $SCHOLAR_COUNT 篇" | tee -a "$LOG_FILE"

# 1.2 百度搜索
echo "1.2 百度搜索..." | tee -a "$LOG_FILE"
SEARCH_COUNT=0
SEARCH_RESULT=$(bash /root/clawd/scripts/baidu-search-wrapper.sh "$QUERY" 2>/dev/null | tail -1)
if [ -n "$SEARCH_RESULT" ]; then
    SEARCH_COUNT=$(echo "$SEARCH_RESULT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('result', [])))" 2>/dev/null || echo "0")
fi
echo "   找到文章: $SEARCH_COUNT 篇" | tee -a "$LOG_FILE"

echo "   ✅ AI 搜索完成" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 步骤 2: 生成 PPT 大纲
echo "========================================" | tee -a "$LOG_FILE"
echo "步骤 2: 生成 PPT 大纲" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

cd /root/clawd/skills/ai-ppt-generate/scripts

echo "   正在生成大纲..." | tee -a "$LOG_FILE"

# 生成大纲并保存输出
OUTLINE_OUTPUT_FILE="${OUTPUT_DIR}/outline-raw-${TIMESTAMP}.txt"
timeout 60 python3 ppt_outline_generate.py --query "$QUERY" > "$OUTLINE_OUTPUT_FILE" 2>&1

# 从输出中提取 query_id, chat_id, title
# 查找包含 query_id 且 query_id 不为空的行
QUERY_ID=$(grep '"query_id"' "$OUTLINE_OUTPUT_FILE" | grep -v '": ""' | grep -v '": ""' | tail -1 | sed 's/.*"query_id":"\([^"]*\)".*/\1/' | head -1)
CHAT_ID=$(grep '"chat_id"' "$OUTLINE_OUTPUT_FILE" | grep -v '": ""' | grep -v '": ""' | tail -1 | sed 's/.*"chat_id":"\([^"]*\)".*/\1/' | head -1)
TITLE=$(grep '"title"' "$OUTLINE_OUTPUT_FILE" | grep -v '": ""' | grep -v '": ""' | tail -1 | sed 's/.*"title":"\([^"]*\)".*/\1/' | head -1)

# 清理 title 中的 \n
TITLE=$(echo "$TITLE" | sed 's/\\n/ /g')

if [ -z "$QUERY_ID" ]; then
    echo "   ❌ 大纲生成失败：无法提取 query_id" | tee -a "$LOG_FILE"
    exit 1
fi

if [ -z "$CHAT_ID" ]; then
    echo "   ❌ 大纲生成失败：无法提取 chat_id" | tee -a "$LOG_FILE"
    exit 1
fi

echo "   query_id: $QUERY_ID" | tee -a "$LOG_FILE"
echo "   chat_id: $CHAT_ID" | tee -a "$LOG_FILE"
echo "   title: $TITLE" | tee -a "$LOG_FILE"
echo "   ✅ 大纲生成完成" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 步骤 3: 生成 PPT
echo "========================================" | tee -a "$LOG_FILE"
echo "步骤 3: 生成 PPT" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

echo "   正在生成 PPT，这可能需要 2-5 分钟..." | tee -a "$LOG_FILE"

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
    echo "   ❌ PPT 生成失败：无法提取 pptx_url" | tee -a "$LOG_FILE"
    exit 1
fi

# 修复协议（https:// → http://）
PPT_URL_HTTP=$(echo "$PPT_URL" | sed 's|^https://|http://|')

echo "   PPT 下载链接: $PPT_URL_HTTP" | tee -a "$LOG_FILE"
echo "   ✅ PPT 生成完成" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 保存结果
cat > "$OUTPUT_FILE" << EOF
{
  "workflow": "$TIMESTAMP",
  "query": "$QUERY",
  "ppt_pages": "$PPT_PAGES",
  "steps": [
    {
      "step": 1,
      "name": "AI 搜索",
      "status": "completed",
      "scholar_count": $SCHOLAR_COUNT,
      "search_count": $SEARCH_COUNT
    },
    {
      "step": 2,
      "name": "生成 PPT 大纲",
      "status": "completed",
      "query_id": "$QUERY_ID",
      "chat_id": "$CHAT_ID",
      "title": "$TITLE"
    },
    {
      "step": 3,
      "name": "生成 PPT",
      "status": "completed",
      "ppt_url": "$PPT_URL_HTTP"
    }
  ],
  "result": {
    "ppt_download_url": "$PPT_URL_HTTP",
    "scholar_count": $SCHOLAR_COUNT,
    "search_count": $SEARCH_COUNT
  }
}
EOF

# 完成
echo "========================================" | tee -a "$LOG_FILE"
echo "工作流完成！" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "结束时间: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "结果文件: $OUTPUT_FILE" | tee -a "$LOG_FILE"
echo "日志文件: $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "📥 PPT 下载链接" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "$PPT_URL_HTTP" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 输出结果
echo "========================================"
echo "✅ 工作流执行成功！"
echo "========================================"
echo ""
echo "搜索主题: $QUERY"
echo "找到论文: $SCHOLAR_COUNT 篇"
echo "找到文章: $SEARCH_COUNT 篇"
echo ""
echo "📥 PPT 下载链接:"
echo "$PPT_URL_HTTP"
echo ""
echo "结果文件: $OUTPUT_FILE"
echo "日志文件: $LOG_FILE"
