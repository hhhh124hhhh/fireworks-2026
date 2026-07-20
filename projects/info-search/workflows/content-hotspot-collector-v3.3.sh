#!/bin/bash

# Content Hotspot Collector v3.3
# 多平台热点收集脚本（带内容摘要 - 优化版）
# 用于自媒体创作者的内容灵感发现

set -e

# 配置
PROJECT_DIR="/root/clawd/projects/info-search"
DATA_DIR="$PROJECT_DIR/data/hotspots"
MEMORY_DIR="/root/clawd/memory/hotspots"
DATE=$(date +"%Y-%m-%d")
DATETIME=$(date +"%Y%m%d_%H%M%S")

# API 配置
HN_API_URL="https://hacker-news.firebaseio.com/v0"

# 翻译配置
TRANSLATE_API="https://api.mymemory.translated.net/get"
TRANSLATE_ENABLED=true

# 内容摘要配置
SUMMARY_ENABLED=true
SUMMARY_LENGTH=300  # 摘要长度（字符）

# AI 摘要配置（可选）
AI_SUMMARY_ENABLED=false
# AI_SUMMARY_API_KEY=""  # OpenAI API Key
# AI_SUMMARY_MODEL="gpt-4-mini"

# 搜索关键词
SEARCH_TOPICS=(
    "AI news"
    "artificial intelligence"
    "GPT Claude"
    "machine learning"
)

# 创建目录
mkdir -p "$DATA_DIR"
mkdir -p "$MEMORY_DIR"

# 输出文件
REPORT_FILE="$DATA_DIR/hotspot-report-$DATETIME.md"
MEMORY_FILE="$MEMORY_DIR/hotspots-$DATE.md"
TEMP_FILE="/tmp/hotspots-v3-$DATETIME.txt"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Content Hotspot Collector v3.3 (优化版内容摘要）===${NC}"
echo "开始收集真实热点..."
echo ""

# 初始化临时文件
> "$TEMP_FILE"

# ============================================
# 翻译函数
# ============================================
translate_text() {
    local text="$1"
    local translated="$text"

    if [ "$TRANSLATE_ENABLED" = "true" ]; then
        # 使用 MyMemory Translation API
        local response=$(curl -s --max-time 3 "${TRANSLATE_API}?q=$(echo "$text" | sed 's/ /%20/g')&langpair=en|zh-CN" 2>/dev/null)

        if [ -n "$response" ]; then
            # 提取翻译结果
            translated=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    matches = data.get('responseData', {}).get('translatedText', '')
    print(matches)
except:
    pass
" 2>/dev/null || echo "$text")

            # 如果翻译失败，使用原文
            if [ -z "$translated" ] || [ "$translated" = "null" ]; then
                translated="$text"
            fi
        fi
    fi

    echo "$translated"
}

# ============================================
# 优化的 URL 内容摘要函数（使用 jina.ai）
# ============================================
get_url_summary() {
    local url="$1"
    local summary=""

    if [ ! "$SUMMARY_ENABLED" = "true" ]; then
        echo ""
        return
    fi

    if [ -z "$url" ] || [ "$url" = "null" ]; then
        echo ""
        return
    fi

    # 使用 jina.ai 的 URL 提取服务
    local content=$(curl -s --max-time 15 "https://r.jina.ai/http://$url" 2>/dev/null || echo "")

    if [ -z "$content" ]; then
        echo "无法获取内容，请访问链接查看详情"
        return
    fi

    # 检查是否有错误（如被阻止）
    if echo "$content" | grep -qiE "(error|blocked|forbidden|unauthorized)"; then
        echo "网站限制访问，请手动查看详情"
        return
    fi

    # 提取正文内容（移除元信息）
    # jina.ai 返回格式: Title: ...\nURL Source: ...\nMarkdown Content: ...\n[正文]
    local body_content=$(echo "$content" | sed -n '/Markdown Content:/,/^[^ ]/p' | tail -n +2)

    # 如果没有找到 Markdown Content，尝试其他方法
    if [ -z "$body_content" ]; then
        # 移除前几行（通常是元信息）
        body_content=$(echo "$content" | tail -n +5)
    fi

    # 清理内容
    if [ -n "$body_content" ]; then
        # 移除多余的空行和空格
        summary=$(echo "$body_content" | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//' | tr -s '\n' '\n')

        # 移除导航和菜单文本（常见模式）
        summary=$(echo "$summary" | sed '/^Navigation Menu$/d' | sed '/^Toggle navigation$/d' | sed '/^Skip to content$/d')
        sed -i '/^===*$/d' <<< "$summary" 2>/dev/null
        sed -i '/^---*$/d' <<< "$summary" 2>/dev/null

        # 限制长度
        summary=$(echo "$summary" | head -c $SUMMARY_LENGTH)

        # 如果截断了，添加省略号
        if [ ${#summary} -ge $SUMMARY_LENGTH ]; then
            summary="${summary}..."
        fi
    else
        summary="内容提取失败，请访问链接查看详情"
    fi

    echo "$summary"
}

# ============================================
# AI 摘要函数（需要配置 API Key）
# ============================================
get_ai_summary() {
    local content="$1"
    local summary=""

    if [ "$AI_SUMMARY_ENABLED" = "true" ] && [ -n "$AI_SUMMARY_API_KEY" ]; then
        # 使用 OpenAI API 生成摘要
        local response=$(curl -s --max-time 15 \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $AI_SUMMARY_API_KEY" \
            -d "{
                \"model\": \"$AI_SUMMARY_MODEL\",
                \"messages\": [
                    {\"role\": \"system\", \"content\": \"你是一个专业的摘要助手。请用 2-3 句话总结以下内容。\"},
                    {\"role\": \"user\", \"content\": \"请总结：$content\"}
                ],
                \"max_tokens\": 150
            }" \
            "https://api.openai.com/v1/chat/completions" 2>/dev/null || echo "")

        if [ -n "$response" ]; then
            summary=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data['choices'][0]['message']['content'])
except:
    pass
" 2>/dev/null || echo "")
        fi
    fi

    echo "$summary"
}

# ============================================
# 1. Hacker News 热点收集
# ============================================
echo -e "${YELLOW}[1/2] 收集 Hacker News 热点...${NC}"

# 获取前 50 个热门故事 ID
HN_IDS=$(curl -s --max-time 5 "$HN_API_URL/topstories.json" 2>/dev/null | sed 's/\[//' | sed 's/\]//' | tr ',' '\n' | head -n 50)

if [ -z "$HN_IDS" ]; then
    echo -e "${RED}✗ Hacker News 数据收集失败${NC}"
else
    echo -e "${GREEN}✓ 获取到故事 ID${NC}"

    # 逐个检查故事（限制前 10 个，因为要获取内容摘要）
    COUNT=0
    for STORY_ID in $HN_IDS; do
        if [ $COUNT -ge 10 ]; then
            break
        fi

        # 获取故事详情
        STORY_JSON=$(curl -s --max-time 3 "$HN_API_URL/item/$STORY_ID.json" 2>/dev/null || echo "")

        # 检查是否包含 AI 关键词
        if echo "$STORY_JSON" | grep -qiE "(AI|artificial intelligence|machine learning|GPT|Claude|OpenAI|ChatGPT|neural|deep learning|llm|large language model|coding agent)"; then
            # 使用 Python 正确解析 JSON
            STORY_INFO=$(echo "$STORY_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    title = data.get('title', 'N/A').replace('|', '')
    score = data.get('score', 0)
    url = data.get('url', '')
    print(f'{title}|{score}|{url}')
except:
    print('')
" 2>/dev/null || echo "")

            if [ -n "$STORY_INFO" ] && [ "$STORY_INFO" != "" ]; then
                # 正确解析字段
                TITLE=$(echo "$STORY_INFO" | cut -d'|' -f1)
                SCORE=$(echo "$STORY_INFO" | cut -d'|' -f2)
                URL=$(echo "$STORY_INFO" | cut -d'|' -f3)

                # 翻译标题
                TRANSLATED_TITLE=$(translate_text "$TITLE")

                # 获取 URL 内容摘要
                echo -n "  [${GREEN}+${NC}] 获取内容摘要: $TRANSLATED_TITLE... "
                SUMMARY=$(get_url_summary "$URL")
                echo -e "${GREEN}完成${NC}"

                # 如果启用了 AI 摘要，尝试生成
                AI_SUMMARY=""
                if [ "$AI_SUMMARY_ENABLED" = "true" ] && [ -n "$SUMMARY" ] && ! echo "$SUMMARY" | grep -qiE "(无法|失败|限制)"; then
                    echo -n "  [${GREEN}+${NC}] 生成 AI 摘要... "
                    AI_SUMMARY=$(get_ai_summary "$SUMMARY")
                    if [ -n "$AI_SUMMARY" ]; then
                        echo -e "${GREEN}完成${NC}"
                    else
                        echo -e "${YELLOW}失败（使用摘要）${NC}"
                    fi
                fi

                # 写入临时文件
                echo "HN|$TITLE|$SCORE|$URL|$TRANSLATED_TITLE|$SUMMARY|$AI_SUMMARY" >> "$TEMP_FILE"
                COUNT=$((COUNT + 1))
            fi
        fi
    done

    echo -e "${GREEN}✓ 找到 $COUNT 个 AI 相关热点${NC}"
fi

# ============================================
# 2. SearXNG 搜索热点
# ============================================
echo ""
echo -e "${YELLOW}[2/2] 使用 SearXNG 搜索热点...${NC}"

for TOPIC in "${SEARCH_TOPICS[@]}"; do
    echo "  搜索: $TOPIC"

    # 搜索并提取结果
    SEARCH_JSON=$(curl -s --noproxy '*' --max-time 5 \
        "http://localhost:8080/search?q=${TOPIC}&format=json&language=en&results=2&time_range=day" \
        2>/dev/null || echo "")

    if [ -n "$SEARCH_JSON" ]; then
        # 提取标题和 URL
        echo "$SEARCH_JSON" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for r in data.get('results', [])[:2]:
        title = r.get('title', '').replace('|', '')
        url = r.get('url', '')
        print(f'SearXNG:{title}|0|{url}|||')
except:
    pass
" >> "$TEMP_FILE" 2>/dev/null
    fi
done

echo -e "${GREEN}✓ SearXNG 搜索完成${NC}"

# ============================================
# 统计
# ============================================
echo ""
echo -e "${GREEN}=== 统计 ===${NC}"

TOTAL=$(wc -l < "$TEMP_FILE" 2>/dev/null || echo 0)
echo -e "${GREEN}总计收集到 $TOTAL 个热点${NC}"

# ============================================
# 生成报告
# ============================================
echo ""
echo -e "${GREEN}=== 生成热点报告 ===${NC}"

# 创建报告
cat > "$REPORT_FILE" << EOF
# 今日 AI 热点

**收集时间**: $(date +"%Y-%m-%d %H:%M")
**数据来源**: Hacker News, SearXNG
**总计热点**: $TOTAL 个
**内容摘要**: ${SUMMARY_ENABLED}（优化版 jina.ai）
**AI 摘要**: ${AI_SUMMARY_ENABLED}

---

## 🔥 热门热点

EOF

# 添加热点到报告（所有热点）
INDEX=1
while IFS='|' read -r SOURCE TITLE SCORE URL TRANSLATED_TITLE SUMMARY AI_SUMMARY; do
    if [ -z "$SOURCE" ]; then
        continue
    fi

    # 根据来源设置热度
    if echo "$SOURCE" | grep -q "HN"; then
        HEAT="🔥🔥🔥🔥"
    else
        HEAT="🔥🔥🔥"
    fi

    # 根据分数调整
    if [ -n "$SCORE" ] && [ "$SCORE" -gt 50 ]; then
        HEAT="🔥🔥🔥🔥🔥"
    elif [ -n "$SCORE" ] && [ "$SCORE" -gt 30 ]; then
        HEAT="🔥🔥🔥🔥"
    fi

    # 添加到报告
    echo "### $INDEX. $TRANSLATED_TITLE" >> "$REPORT_FILE"
    echo "- **热度**: $HEAT" >> "$REPORT_FILE"
    echo "- **来源**: $SOURCE" >> "$REPORT_FILE"

    if [ -n "$SCORE" ] && [ "$SCORE" != "0" ]; then
        echo "- **分数**: $SCORE" >> "$REPORT_FILE"
    fi

    # 如果有 AI 摘要，使用 AI 摘要；否则使用内容摘要
    if [ -n "$AI_SUMMARY" ] && [ "$AI_SUMMARY" != "" ]; then
        echo "- **AI 摘要**: $AI_SUMMARY" >> "$REPORT_FILE"
    elif [ -n "$SUMMARY" ] && [ "$SUMMARY" != "" ]; then
        echo "- **内容摘要**: $SUMMARY" >> "$REPORT_FILE"
    fi

    if [ -n "$URL" ] && [ "$URL" != "null" ] && [ "$URL" != "" ]; then
        echo "- **链接**: [查看详情]($URL)" >> "$REPORT_FILE"
    fi

    echo "" >> "$REPORT_FILE"

    INDEX=$((INDEX + 1))
done < "$TEMP_FILE"

# 添加选题建议
cat >> "$REPORT_FILE" << EOF

---

## 💡 选题建议

EOF

# 基于 Hacker News 热点生成建议
HN_HOTSPOTS=$(grep "^HN:" "$TEMP_FILE" 2>/dev/null | head -n 3)
COUNT=1

if [ -n "$HN_HOTSPOTS" ]; then
    echo "$HN_HOTSPOTS" | while IFS='|' read -r SOURCE TITLE SCORE URL TRANSLATED_TITLE SUMMARY AI_SUMMARY; do
        if [ -z "$SOURCE" ]; then
            continue
        fi

        # 生成建议
        SUGGESTION="$TRANSLATED_TITLE 深度解读"

        case "$TRANSLATED_TITLE" in
            *"GPT"*|*"OpenAI"*|*"ChatGPT"*)
                SUGGESTION="GPT/ChatGPT 最新功能深度分析"
                ;;
            *"Claude"*|*"Anthropic"*|*"coding agent"*)
                SUGGESTION="Claude AI 实战应用案例"
                ;;
            *"AI tool"*|*"AI tools"*|*"automation"*)
                SUGGESTION="AI 自动化工具合集与对比"
                ;;
            *"release"*|*"launch"*|*"update"*)
                SUGGESTION="新发布 AI 工具评测与试用"
                ;;
            *"shortage"*|*"economy"*)
                SUGGESTION="AI 浪潮下的经济影响分析"
                ;;
        esac

        echo "### $COUNT. **$SUGGESTION**" >> "$REPORT_FILE"
        echo "   - 基于热点: $TRANSLATED_TITLE" >> "$REPORT_FILE"
        echo "   - 难度: ⭐⭐⭐" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"

        COUNT=$((COUNT + 1))
    done
else
    echo "暂无基于 Hacker News 的建议" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# 添加数据统计
cat >> "$REPORT_FILE" << EOF
---

## 📊 数据统计

- **收集热点**: $TOTAL 个
- **数据源**: 2 个 (Hacker News, SearXNG)
- **搜索关键词**: ${#SEARCH_TOPICS[@]} 个
- **翻译状态**: ${TRANSLATE_ENABLED}（启用）
- **内容摘要**: ${SUMMARY_ENABLED}（优化版 jina.ai）
- **AI 摘要**: ${AI_SUMMARY_ENABLED}（未启用）

---

**下次更新**: 明天 08:00
**收集工具**: Content Hotspot Collector v3.3
EOF

echo -e "${GREEN}✓ 报告生成成功${NC}"
echo "  文件: $REPORT_FILE"

# ============================================
# 复制到 Memory
# ============================================
echo ""
echo -e "${GREEN}=== 存储到 Memory ===${NC}"

cp "$REPORT_FILE" "$MEMORY_FILE"
echo -e "${GREEN}✓ 已存储到 memory/hotspots/${NC}"

# ============================================
# 完成
# ============================================
echo ""
echo -e "${GREEN}=== 完成 ===${NC}"
echo "热点收集完成！"
echo ""
echo "报告文件: $REPORT_FILE"
echo "Memory 文件: $MEMORY_FILE"
echo ""
echo -e "${BLUE}提示:${NC}"
echo "  - 中文翻译: ${TRANSLATE_ENABLED}"
echo "  - 内容摘要: ${SUMMARY_ENABLED}（优化版 jina.ai）"
echo "  - AI 摘要: ${AI_SUMMARY_ENABLED}（需要配置 API Key）"
echo ""
