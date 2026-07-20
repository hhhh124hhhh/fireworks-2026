#!/bin/bash

# AI Content Creator 自动化工作流 (最终版)
# 两阶段：1. 生成大纲 + 2. 生成 PPT

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

exec > "$LOG_FILE" 2>&1

echo "========================================" | tee -a "$LOG_FILE"
echo "AI Content Creator 自动化工作流" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "搜索主题: $QUERY" | tee -a "$LOG_FILE"
echo "开始时间: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ========== 阶段 1: 生成 PPT 大纲 ==========
echo "========================================" | tee -a "$LOG_FILE"
echo "阶段 1: 生成 PPT 大纲" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

cd /root/clawd/skills/ai-ppt-generate/scripts

echo "正在生成大纲..." | tee -a "$LOG_FILE"
OUTLINE_OUTPUT_FILE="${OUTPUT_DIR}/outline-output-${TIMESTAMP}.txt"
timeout 60 python3 ppt_outline_generate.py --query "$QUERY" > "$OUTLINE_OUTPUT_FILE" 2>&1

# 提取所有相关信息（使用 Python）
PYTHON_CODE='
import re
import sys
import json

# 读取文件
with open(sys.argv[1], "r") as f:
    content = f.read()

# 查找最后一个完整的 JSON 对象（is_end: true）
json_pattern = re.compile(r"\{[^{}]*(?:query_id|chat_id|title|outline)[^{}]*\}")
matches = json_pattern.findall(content)

query_id = None
chat_id = None
title = None
outline_parts = []

for match in reversed(matches):
    try:
        data = json.loads(match)
        if "is_end" in data and data["is_end"] == True:
            # 找到了最终响应
            query_id = data.get("query_id")
            chat_id = data.get("chat_id")
            title = data.get("title")
            outline_parts.append(data.get("outline", ""))
            break
        else:
            outline_parts.append(data.get("outline", ""))
    except:
        continue

# 合并所有 outline
full_outline = "".join(outline_parts)

if query_id and chat_id and full_outline.strip():
    print(f"QUERY_ID={query_id.strip()}")
    print(f"CHAT_ID={chat_id.strip()}")
    title_clean = title.strip().replace("\\n", " ").strip()
    print(f"TITLE={title_clean}")
    # 保存 outline 到临时文件
    with open(sys.argv[1] + ".outline", "w") as f:
        f.write(full_outline)
    sys.exit(0)
else:
    print("ERROR")
    sys.exit(1)
'

EXTRACT_RESULT=$(python3 -c "$PYTHON_CODE" "$OUTLINE_OUTPUT_FILE" 2>&1)

if [ "$EXTRACT_RESULT" = "ERROR" ]; then
    echo "❌ 大纲生成失败：无法提取完整信息" | tee -a "$LOG_FILE"
    exit 1
fi

# 解析提取的 ID
QUERY_ID=$(echo "$EXTRACT_RESULT" | grep "^QUERY_ID=" | cut -d'=' -f2)
CHAT_ID=$(echo "$EXTRACT_RESULT" | grep "^CHAT_ID=" | cut -d'=' -f2)
TITLE=$(echo "$EXTRACT_RESULT" | grep "^TITLE=" | cut -d'=' -f2)

# 读取 outline 文件
OUTLINE_FILE="${OUTLINE_OUTPUT_FILE}.outline"
if [ ! -f "$OUTLINE_FILE" ]; then
    echo "❌ outline 文件不存在" | tee -a "$LOG_FILE"
    exit 1
fi

OUTLINE=$(cat "$OUTLINE_FILE")

if [ -z "$OUTLINE" ] || [ "$OUTLINE" = "" ]; then
    echo "❌ outline 为空" | tee -a "$LOG_FILE"
    exit 1
fi

echo "✅ 大纲生成完成" | tee -a "$LOG_FILE"
echo "query_id: $QUERY_ID" | tee -a "$LOG_FILE"
echo "chat_id: $CHAT_ID" | tee -a "$LOG_FILE"
echo "title: $TITLE" | tee -a "$LOG_FILE"
echo "outline 长度: $(echo "$OUTLINE" | wc -c) 字符" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# ========== 阶段 2: 生成 PPT ==========
echo "========================================" | tee -a "$LOG_FILE"
echo "阶段 2: 生成 PPT" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

echo "正在生成 PPT，这可能需要 2-5 分钟..." | tee -a "$LOG_FILE"

PPT_OUTPUT_FILE="${OUTPUT_DIR}/ppt-output-${TIMESTAMP}.txt"
timeout 300 python3 ppt_generate.py \
  --query_id "$QUERY_ID" \
  --chat_id "$CHAT_ID" \
  --query "$QUERY" \
  --title "$TITLE" \
  --outline "$OUTLINE" \
  --style_id 0 \
  --tpl_id 3 > "$PPT_OUTPUT_FILE" 2>&1

# 提取 PPT 下载链接
PPT_URL=$(grep '"pptx_url"' "$PPT_OUTPUT_FILE" | head -1 | sed 's/.*"pptx_url":"\([^"]*\)".*/\1/')

if [ -z "$PPT_URL" ]; then
    echo "❌ PPT 生成失败：无法提取 pptx_url" | tee -a "$LOG_FILE"
    exit 1
fi

# 修复协议（https:// → http://）
PPT_URL_HTTP=$(echo "$PPT_URL" | sed 's|^https://|http://|')

echo "✅ PPT 生成完成" | tee -a "$LOG_FILE"
echo "PPT 下载链接: $PPT_URL_HTTP" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 保存结果
cat > "$OUTPUT_FILE" << EOF
{
  "workflow": "$TIMESTAMP",
  "query": "$QUERY",
  "ppt_pages": "$PPT_PAGES",
  "result": {
    "ppt_download_url": "$PPT_URL_HTTP",
    "query_id": "$QUERY_ID",
    "chat_id": "$CHAT_ID"
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
echo "📥 PPT 下载链接:" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "$PPT_URL_HTTP" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 输出结果
echo "========================================"
echo "✅ 工作流执行成功！"
echo "========================================"
echo ""
echo "搜索主题: $QUERY"
echo ""
echo "📥 PPT 下载链接:"
echo "$PPT_URL_HTTP"
echo ""
echo "结果文件: $OUTPUT_FILE"
echo "日志文件: $LOG_FILE"
