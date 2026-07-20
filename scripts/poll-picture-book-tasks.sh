#!/bin/bash

# AI 绘本生成状态轮询脚本

export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"

# 任务 ID
STATIC_TASK_ID="ba3636c0-0bbe-4489-b7ef-13089c7682d5"
DYNAMIC_TASK_ID="c05df768-80e6-4b4a-94e5-8d15f342077e"

echo "开始轮询 AI 绘本生成状态..."
echo "静态绘本任务 ID: $STATIC_TASK_ID"
echo "动态绘本任务 ID: $DYNAMIC_TASK_ID"
echo ""

MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    echo "第 $((ATTEMPT + 1)) 次查询..."
    
    # 查询任务状态
    RESULT=$(python3 /root/clawd/skills/ai-picture-book/scripts/ai_picture_book_task_query.py "${STATIC_TASK_ID},${DYNAMIC_TASK_ID}")
    
    echo "$RESULT" | python3 -m json.tool
    
    # 检查状态
    STATIC_STATUS=$(echo "$RESULT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data[0]['status'])")
    DYNAMIC_STATUS=$(echo "$RESULT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data[1]['status'])")
    
    if [ "$STATIC_STATUS" = "2" ] && [ "$DYNAMIC_STATUS" = "2" ]; then
        echo ""
        echo "✅ 两个任务都已完成！"
        echo "$RESULT" | python3 -m json.tool > /root/clawd/memory/picture-book-result.json
        break
    fi
    
    ATTEMPT=$((ATTEMPT + 1))
    echo ""
    echo "等待 10 秒..."
    sleep 10
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo "⚠️ 达到最大查询次数，任务可能还在处理中"
fi

echo ""
echo "最终结果："
cat /root/clawd/memory/picture-book-result.json 2>/dev/null || echo "结果文件不存在"
