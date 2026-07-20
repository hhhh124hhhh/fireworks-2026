#!/bin/bash

# 阶段 1: 生成 PPT 大纲 (改进版)
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

# 生成大纲，只保存到文件
echo "正在生成大纲..."
timeout 60 python3 ppt_outline_generate.py --query "$QUERY" > "${OUTPUT_DIR}/outline-raw-${TIMESTAMP}.txt" 2>&1

# 使用 Python 提取 ID
PYTHON_CODE='
import re
import sys
import json

# 读取文件
with open(sys.argv[1], "r") as f:
    content = f.read()

# 查找所有 JSON 对象
json_pattern = re.compile(r"\{[^{}]*(?:query_id|chat_id|title)[^{}]*\}")
matches = json_pattern.findall(content)

# 查找最后包含非空 query_id 和 chat_id 的对象
query_id = None
chat_id = None
title = None

for match in reversed(matches):
    try:
        data = json.loads(match)
        qid = data.get("query_id")
        cid = data.get("chat_id")
        t = data.get("title")
        
        if qid and qid.strip() and cid and cid.strip():
            query_id = qid.strip()
            chat_id = cid.strip()
            if t:
                title = t.strip().replace("\\n", " ")
            break
    except:
        continue

if query_id and chat_id:
    print(f"QUERY_ID={query_id}")
    print(f"CHAT_ID={chat_id}")
    if title:
        print(f"TITLE={title}")
    sys.exit(0)
else:
    print("ERROR: Could not extract IDs")
    sys.exit(1)
'

# 运行 Python 提取
EXTRACT_RESULT=$(python3 -c "$PYTHON_CODE" "${OUTPUT_DIR}/outline-raw-${TIMESTAMP}.txt" 2>&1)

if [ $? -ne 0 ]; then
    echo "❌ ID 提取失败: $EXTRACT_RESULT"
    exit 1
fi

# 解析提取的 ID
QUERY_ID=$(echo "$EXTRACT_RESULT" | grep "^QUERY_ID=" | cut -d'=' -f2)
CHAT_ID=$(echo "$EXTRACT_RESULT" | grep "^CHAT_ID=" | cut -d'=' -f2)
TITLE=$(echo "$EXTRACT_RESULT" | grep "^TITLE=" | cut -d'=' -f2)

echo "✅ 大纲生成完成"
echo "query_id: $QUERY_ID"
echo "chat_id: $CHAT_ID"
echo "title: $TITLE"
echo ""

# 保存 ID 到文件
cat > "$IDS_FILE" << EOF
QUERY_ID="$QUERY_ID"
CHAT_ID="$CHAT_ID"
TITLE="$TITLE"
QUERY="$QUERY"
TIMESTAMP="$TIMESTAMP"
EOF

echo "ID 已保存到: $IDS_FILE"
echo ""
echo "运行阶段 2: bash /root/clawd/scripts/ai-content-creator-stage2.sh $IDS_FILE"
