#!/bin/bash

# AI Content Creator 自动化工作流 (改进版 v4)
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

# 运行大纲生成并捕获所有输出
echo "   正在生成大纲..." | tee -a "$LOG_FILE"
OUTLINE_OUTPUT=$(timeout 60 python3 ppt_outline_generate.py --query "$QUERY" 2>&1)

# 保存完整输出
echo "$OUTLINE_OUTPUT" > "${OUTPUT_DIR}/outline-${TIMESTAMP}.txt"

# 使用 Python 提取最后一个完整的 JSON 对象
# 找到 "is_end": true 的响应，提取其中的 query_id 和 chat_id

PYTHON_SCRIPT=$(cat << 'PYTHON_CODE'
import sys
import re
import json

# 读取输入
content = sys.stdin.read()

# 查找所有 JSON 对象
# pattern: { ... "is_end": true ... }
json_pattern = re.compile(r'\{[^{}]*(?:"is_end"\s*:\s*true)[^{}]*\}')

# 找到所有匹配的 JSON
matches = json_pattern.findall(content)

if matches:
    # 取最后一个（最新的）
    last_match = matches[-1]
    
    try:
        data = json.loads(last_match)
        query_id = data.get('query_id', '')
        chat_id = data.get('chat_id', '')
        title = data.get('title', '')
        
        if query_id and chat_id:
            print(f"QUERY_ID={query_id}")
            print(f"CHAT_ID={chat_id}")
            print(f"TITLE={title}")
            sys.exit(0)
    except:
        pass

print("ERROR: Could not extract IDs")
sys.exit(1)
PYTHON_CODE
)

# 使用 Python 提取
EXTRACTED_IDS=$(echo "$OUTLINE_OUTPUT" | python3 -c "$PYTHON_SCRIPT" 2>&1)

if [ $? -ne 0 ]; then
    echo "   ❌ 大纲生成失败：无法提取 query_id 和 chat_id" | tee -a "$LOG_FILE"
    echo "   错误: $EXTRACTED_IDS" | tee -a "$LOG_FILE"
    echo "   请检查: ${OUTPUT_DIR}/outline-${TIMESTAMP}.txt" | tee -a "$LOG_FILE"
    exit 1
fi

# 解析提取的 ID
QUERY_ID=$(echo "$EXTRACTED_IDS" | grep "^QUERY_ID=" | cut -d'=' -f2)
CHAT_ID=$(echo "$EXTRACTED_IDS" | grep "^CHAT_ID=" | cut -d'=' -f2)
TITLE=$(echo "$EXTRACTED_IDS" | grep "^TITLE=" | cut -d'=' -f2)

if [ -z "$QUERY_ID" ]; then
    echo "   ❌ 大纲生成失败：query_id 为空" | tee -a "$LOG_FILE"
    exit 1
fi

if [ -z "$CHAT_ID" ]; then
    echo "   ❌ 大纲生成失败：chat_id 为空" | tee -a "$LOG_FILE"
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

PPT_RESULT=$(timeout 300 python3 ppt_generate.py \
  --query_id "$QUERY_ID" \
  --chat_id "$CHAT_ID" \
  --query "$QUERY" \
  --title "$TITLE" \
  --style_id "$PPT_STYLE_ID" \
  --tpl_id "$PPT_TPL_ID" 2>&1)

# 保存 PPT 输出
echo "$PPT_RESULT" > "${OUTPUT_DIR}/ppt-${TIMESTAMP}.txt"

# 提取 PPT 下载链接
PPT_URL=$(echo "$PPT_RESULT" | grep -o '"pptx_url":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$PPT_URL" ]; then
    echo "   ❌ PPT 生成失败：无法提取 pptx_url" | tee -a "$LOG_FILE"
    echo "   完整输出已保存到: ${OUTPUT_DIR}/ppt-${TIMESTAMP}.txt" | tee -a "$LOG_FILE"
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
echo "大纲输出: ${OUTPUT_DIR}/outline-${TIMESTAMP}.txt" | tee -a "$LOG_FILE"
echo "PPT 输出: ${OUTPUT_DIR}/ppt-${TIMESTAMP}.txt" | tee -a "$LOG_FILE"
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
