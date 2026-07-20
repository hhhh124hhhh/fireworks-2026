#!/bin/bash

# AI Content Creator 自动化工作流
# 流程：AI 搜索 → PPT 生成

set -e

# 配置
export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"

# 参数
QUERY="${1:-AI技术发展趋势2026}"
PPT_PAGES="${2:-10}"
PPT_STYLE_ID="0"
PPT_TPL_ID="3"

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

# JSON 对象初始化
JSON_CONTENT='{"workflow":"'${TIMESTAMP}'","query":"'${QUERY}'","ppt_pages":"'${PPT_PAGES}'","steps":[]}'

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
SEARCH_RESULT=$(bash /root/clawd/scripts/baidu-search-wrapper.sh "$QUERY" 2>/dev/null | tail -1)
SEARCH_COUNT=$(echo "$SEARCH_RESULT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('result', [])))" 2>/dev/null || echo "0")
echo "   找到文章: $SEARCH_COUNT 篇" | tee -a "$LOG_FILE"

echo "   ✅ AI 搜索完成" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 添加步骤 1 到 JSON
STEP1='{"step":1,"name":"AI 搜索","status":"completed","scholar_count":'${SCHOLAR_COUNT}',"search_count":'${SEARCH_COUNT}'}'
JSON_CONTENT=$(echo "$JSON_CONTENT" | python3 -c "import sys, json; data=json.load(sys.stdin); data['steps'].append($STEP1); print(json.dumps(data, ensure_ascii=False))")

# 步骤 2: 生成 PPT 大纲
echo "========================================" | tee -a "$LOG_FILE"
echo "步骤 2: 生成 PPT 大纲" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

cd /root/clawd/skills/ai-ppt-generate/scripts
OUTLINE_RESULT=$(python3 ppt_outline_generate.py --query "$QUERY" 2>&1)

echo "$OUTLINE_RESULT" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 提取 query_id 和 chat_id
QUERY_ID=$(echo "$OUTLINE_RESULT" | grep -o '"query_id":"[^"]*"' | cut -d'"' -f4)
CHAT_ID=$(echo "$OUTLINE_RESULT" | grep -o '"chat_id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$QUERY_ID" ] || [ -z "$CHAT_ID" ]; then
    echo "   ❌ 大纲生成失败" | tee -a "$LOG_FILE"
    echo "$JSON_CONTENT" | python3 -m json.tool > "$OUTPUT_FILE"
    exit 1
fi

echo "   query_id: $QUERY_ID" | tee -a "$LOG_FILE"
echo "   chat_id: $CHAT_ID" | tee -a "$LOG_FILE"
echo "   ✅ 大纲生成完成" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 添加步骤 2 到 JSON
STEP2='{"step":2,"name":"生成 PPT 大纲","status":"completed","query_id":"'${QUERY_ID}'","chat_id":"'${CHAT_ID}'"}'
JSON_CONTENT=$(echo "$JSON_CONTENT" | python3 -c "import sys, json; data=json.load(sys.stdin); data['steps'].append($STEP2); print(json.dumps(data, ensure_ascii=False))")

# 步骤 3: 生成 PPT
echo "========================================" | tee -a "$LOG_FILE"
echo "步骤 3: 生成 PPT" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

echo "   正在生成 PPT，这可能需要 2-5 分钟..." | tee -a "$LOG_FILE"

PPT_RESULT=$(timeout 300 python3 ppt_generate.py \
  --query_id "$QUERY_ID" \
  --chat_id "$CHAT_ID" \
  --query "$QUERY" \
  --title "$QUERY" \
  --style_id "$PPT_STYLE_ID" \
  --tpl_id "$PPT_TPL_ID" 2>&1)

echo "$PPT_RESULT" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 提取 PPT 下载链接
PPT_URL=$(echo "$PPT_RESULT" | grep -o '"pptx_url":"[^"]*"' | cut -d'"' -f4)

if [ -z "$PPT_URL" ]; then
    echo "   ❌ PPT 生成失败" | tee -a "$LOG_FILE"
    echo "$JSON_CONTENT" | python3 -m json.tool > "$OUTPUT_FILE"
    exit 1
fi

# 修复协议（https:// → http://）
PPT_URL_HTTP=$(echo "$PPT_URL" | sed 's|^https://|http://|')

echo "   PPT 下载链接: $PPT_URL_HTTP" | tee -a "$LOG_FILE"
echo "   ✅ PPT 生成完成" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 添加步骤 3 到 JSON
STEP3='{"step":3,"name":"生成 PPT","status":"completed","ppt_url":"'${PPT_URL_HTTP}'"}'
JSON_CONTENT=$(echo "$JSON_CONTENT" | python3 -c "import sys, json; data=json.load(sys.stdin); data['steps'].append($STEP3); print(json.dumps(data, ensure_ascii=False))")

# 保存结果
echo "$JSON_CONTENT" | python3 -m json.tool > "$OUTPUT_FILE"

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
