#!/bin/bash

# MD 转 Slack 格式化文本工具
# 将 Markdown 文件转换为 Slack 友好的格式化文本

set -e

# 参数
MD_FILE="$1"
MODE="${2:-summary}"  # summary, full, tag
TAG="${3:-}"

# 检查参数
if [ -z "$MD_FILE" ]; then
    echo "用法: bash md-to-slack.sh <md-file> [mode] [tag]"
    echo ""
    echo "参数:"
    echo "  md-file    - Markdown 文件路径"
    echo "  mode       - 模式: summary (摘要), full (完整), tag (标签)"
    echo "  tag        - 标签名（mode=tag 时使用）"
    echo ""
    echo "示例:"
    echo "  bash md-to-slack.sh /root/clawd/memory/2026-02-10.md summary"
    echo "  bash md-to-slack.sh /root/clawd/memory/2026-02-10.md full"
    echo "  bash md-to-slack.sh /root/clawd/memory/2026-02-10.md tag 任务清单"
    exit 1
fi

# 检查文件是否存在
if [ ! -f "$MD_FILE" ]; then
    echo "❌ 文件不存在: $MD_FILE"
    exit 1
fi

# 文件名
FILENAME=$(basename "$MD_FILE")
FILE_SIZE=$(wc -c < "$MD_FILE")
FILE_LINES=$(wc -l < "$MD_FILE")

# 转换函数
md_to_slack() {
    local content="$1"
    
    # 转换标题
    content=$(echo "$content" | sed 's/^## /**/g')
    content=$(echo "$content" | sed 's/^### /**/g')
    content=$(echo "$content" | sed 's/^#### /**/g')
    content=$(echo "$content" | sed 's/^##### /**/g')
    content=$(echo "$content" | sed 's/^###### /**/g')
    content=$(echo "$content" | sed 's/^# //g')
    
    # 转换列表
    content=$(echo "$content" | sed 's/^- /• /g')
    content=$(echo "$content" | sed 's/^  - /  • /g')
    content=$(echo "$content" | sed 's/^    - /    • /g')
    
    # 转换代码块（简化处理）
    content=$(echo "$content" | sed 's/^```/---/g')
    
    # 转换粗体
    content=$(echo "$content" | sed 's/\*\*\([^*]*\)\*\*/_\1_/g')
    
    # 转换斜体
    content=$(echo "$content" | sed 's/\*\([^*]*\)\*/_\1_/g')
    
    echo "$content"
}

# 分批推送函数
send_to_slack() {
    local content="$1"
    local header="$2"
    local part_num="$3"
    local total_parts="$4"
    
    # 限制每条消息长度（Slack 限制约 4000 字符）
    local max_length=3500
    
    # 如果内容太长，分割
    if [ ${#content} -gt $max_length ]; then
        # 分割内容
        echo "⚠️ 内容过长，将分 $((${#content} / max_length + 1)) 部分推送..."
        
        local offset=0
        local part=1
        while [ $offset -lt ${#content} ]; do
            local chunk="${content:$offset:$max_length}"
            
            # 添加头部
            if [ "$part" -gt 1 ]; then
                chunk="($part/$((${#content} / max_length + 1)))\n\n$chunk"
            fi
            
            # 推送（这里只是打印，实际推送需要调用 message 工具）
            echo "========================================"
            if [ -n "$header" ]; then
                echo "$header (Part $part/$((${#content} / max_length + 1)))"
            else
                echo "Part $part/$((${#content} / max_length + 1))"
            fi
            echo "========================================"
            echo ""
            echo "$chunk"
            echo ""
            
            offset=$((offset + max_length))
            part=$((part + 1))
        done
    else
        # 直接推送
        echo "========================================"
        if [ -n "$header" ]; then
            echo "$header"
        fi
        echo "========================================"
        echo ""
        echo "$content"
        echo ""
    fi
}

# 主逻辑
case "$MODE" in
    summary)
        # 摘要模式（前 100 行）
        echo "📄 文件信息"
        echo "文件名: $FILENAME"
        echo "大小: $FILE_SIZE bytes"
        echo "行数: $FILE_LINES"
        echo ""
        echo "========================================"
        echo "📋 内容摘要 (前 100 行)"
        echo "========================================"
        echo ""
        
        content=$(head -100 "$MD_FILE")
        slack_content=$(md_to_slack "$content")
        echo "$slack_content"
        
        if [ $FILE_LINES -gt 100 ]; then
            echo ""
            echo "..."
            echo ""
            echo "(还有 $((FILE_LINES - 100)) 行未显示)"
            echo "使用 'full' 模式查看完整内容："
            echo "bash md-to-slack.sh $MD_FILE full"
        fi
        ;;
    
    full)
        # 完整模式
        echo "📄 文件信息"
        echo "文件名: $FILENAME"
        echo "大小: $FILE_SIZE bytes"
        echo "行数: $FILE_LINES"
        echo ""
        echo "========================================"
        echo "📋 完整内容"
        echo "========================================"
        echo ""
        
        content=$(cat "$MD_FILE")
        slack_content=$(md_to_slack "$content")
        
        # 分批推送
        send_to_slack "$slack_content" "完整内容" 1 1
        ;;
    
    tag)
        # 标签模式
        if [ -z "$TAG" ]; then
            echo "❌ 请指定标签名"
            echo "用法: bash md-to-slack.sh $MD_FILE tag <tag-name>"
            exit 1
        fi
        
        echo "📄 文件信息"
        echo "文件名: $FILENAME"
        echo "标签: $TAG"
        echo ""
        echo "========================================"
        echo "📋 标签内容: $TAG"
        echo "========================================"
        echo ""
        
        # 查找标签部分（假设格式为 "## 标签名"）
        tag_content=$(awk "/## $TAG/,/^## / {print}" "$MD_FILE" | head -n -1)
        
        if [ -z "$tag_content" ]; then
            echo "❌ 未找到标签: $TAG"
            echo ""
            echo "可用的标签:"
            grep "^## " "$MD_FILE" | sed 's/^## /  - /'
            exit 1
        fi
        
        slack_content=$(md_to_slack "$tag_content")
        echo "$slack_content"
        ;;
    
    *)
        echo "❌ 未知的模式: $MODE"
        echo "可用模式: summary, full, tag"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "✅ 完成"
echo "========================================"
