#!/bin/bash

# Content Hotspot Collector v5.1
# 多平台热点收集脚本（带 AI 摘要 - 优化版）
# 用于自媒体创作者的内容灵感发现

set -e

# 加载共享配置
CONFIG_DIR="/root/clawd/.config/data-sources"
SEARXNG_CONF="$CONFIG_DIR/searxng.conf"

# 检查配置文件
if [ ! -f "$SEARXNG_CONF" ]; then
    echo "❌ SearXNG 配置文件不存在: $SEARXNG_CONF"
    exit 1
fi

source "$SEARXNG_CONF"

# 配置
PROJECT_DIR="/root/clawd/projects/info-search"
DATA_DIR="$PROJECT_DIR/data/hotspots"
MEMORY_DIR="/root/clawd/memory/hotspots"
DATE=$(date +"%Y-%m-%d")
DATETIME=$(date +"%Y%m%d_%H%M%S")

# API 配置
HN_API_URL="https://hacker-news.firebaseio.com/v0"
SEARXNG_SEARCH_URL="$SEARXNG_URL/search"

# 翻译配置
TRANSLATE_API="https://api.mymemory.translated.net/get"
TRANSLATE_ENABLED=true

# AI 摘要配置
AI_ASSISTANT_SCRIPT="$PROJECT_DIR/scripts/hotspot-ai-assistant.py"
AI_SUMMARY_ENABLED=true

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
TEMP_FILE="/tmp/hotspots-v5-$DATETIME.txt"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Content Hotspot Collector v5.1 (AI 摘要 - 优化版）===${NC}"
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
# 1. Hacker News 热点收集
# ============================================
echo -e "${YELLOW}[1/2] 收集 Hacker News 热点...${NC}"

# 获取前 50 个热门故事 ID
HN_IDS=$(curl -s --max-time 5 "$HN_API_URL/topstories.json" 2>/dev/null | sed 's/\[//' | sed 's/\]//' | tr ',' '\n' | head -n 50)

if [ -z "$HN_IDS" ]; then
    echo -e "${RED}✗ Hacker News 数据收集失败${NC}"
else
    echo -e "${GREEN}✓ 获取到故事 ID${NC}"

    # 逐个检查故事（限制前 10 个）
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

                # 生成 AI 摘要和创作建议（传递中文标题）
                echo -n "  [${GREEN}+${NC}] 生成 AI 摘要: $TRANSLATED_TITLE... "
                AI_RESULT=$(python3 "$AI_ASSISTANT_SCRIPT" "$TITLE" "$URL" "$SCORE" "$TRANSLATED_TITLE" 2>/dev/null || echo '{"summary":"生成失败","content_direction":"N/A","suggestions":[],"target_audience":"N/A","difficulty":"N/A"}')
                echo -e "${GREEN}完成${NC}"

                # 写入临时文件（使用特殊分隔符避免问题）
                # 格式: HN|TITLE|SCORE|URL|TRANSLATED_TITLE|<JSON_START>$AI_RESULT<JSON_END>
                echo "HN|$TITLE|$SCORE|$URL|$TRANSLATED_TITLE|<JSON_START>$AI_RESULT<JSON_END>" >> "$TEMP_FILE"
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
    SEARCH_JSON=$(curl -s --noproxy '*' --max-time "$TIMEOUT" \
        "$SEARXNG_SEARCH_URL?q=${TOPIC}&format=json&language=en&results=2&time_range=day" \
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
        ai_result = '{\"summary\":\"建议访问链接查看详情\",\"content_direction\":\"N/A\",\"suggestions\":[],\"target_audience\":\"N/A\",\"difficulty\":\"N/A\"}'
        print(f'SearXNG:{title}|0|{url}||<JSON_START>\${ai_result}<JSON_END>')
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
**AI 摘要**: ${AI_SUMMARY_ENABLED}（优化版）

---

## 🔥 热门热点

EOF

# 添加热点到报告（所有热点）
INDEX=1
# 使用特殊分隔符读取 JSON
while IFS='|' read -r SOURCE TITLE SCORE URL TRANSLATED_TITLE JSON_PART; do
    # 提取 JSON 部分（去除标记）
    AI_RESULT=$(echo "$JSON_PART" | sed 's/<JSON_START>//' | sed 's/<JSON_END>//' | tr -d '\n')
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
    if [ -n "$SCORE" ] && [ "$SCORE" -gt 200 ]; then
        HEAT="🔥🔥🔥🔥🔥"
    elif [ -n "$SCORE" ] && [ "$SCORE" -gt 100 ]; then
        HEAT="🔥🔥🔥🔥"
    elif [ -n "$SCORE" ] && [ "$SCORE" -gt 50 ]; then
        HEAT="🔥🔥🔥🔥"
    fi

    # 添加到报告
    echo "### $INDEX. $TRANSLATED_TITLE" >> "$REPORT_FILE"
    echo "- **热度**: $HEAT" >> "$REPORT_FILE"
    echo "- **来源**: $SOURCE" >> "$REPORT_FILE"

    if [ -n "$SCORE" ] && [ "$SCORE" != "0" ]; then
        echo "- **分数**: $SCORE" >> "$REPORT_FILE"
    fi

    # 解析 AI 结果并添加到报告
    if [ -n "$AI_RESULT" ] && [ "$AI_RESULT" != "" ]; then
        # 使用临时文件传递 JSON
        echo "$AI_RESULT" > /tmp/hotspot-ai-result-temp.json
        
        # 使用 Python 解析 JSON
        python3 -c "
import sys, json
try:
    with open('/tmp/hotspot-ai-result-temp.json', 'r') as f:
        data = json.load(f)
    if 'summary' in data:
        print(f'- **AI 摘要**: {data[\"summary\"]}')
    if 'content_direction' in data and data['content_direction'] != 'N/A':
        print(f'- **内容方向**: {data[\"content_direction\"]}')
    if 'target_audience' in data and data['target_audience'] != 'N/A':
        print(f'- **目标受众**: {data[\"target_audience\"]}')
    if 'difficulty' in data and data['difficulty'] != 'N/A':
        print(f'- **创作难度**: {data[\"difficulty\"]}')
    if 'suggestions' in data and data['suggestions']:
        print(f'- **创作建议**:')
        for i, sugg in enumerate(data['suggestions'], 1):
            print(f'  {i}. {sugg}')
except Exception as e:
    print(f'- **AI 摘要**: JSON 解析失败')
" >> "$REPORT_FILE" 2>/dev/null
    fi

    if [ -n "$URL" ] && [ "$URL" != "null" ] && [ "$URL" != "" ]; then
        echo "- **链接**: [查看详情]($URL)" >> "$REPORT_FILE"
    fi

    echo "" >> "$REPORT_FILE"

    INDEX=$((INDEX + 1))
done < "$TEMP_FILE"

# 添加数据统计
cat >> "$REPORT_FILE" << EOF
---

## 📊 数据统计

- **收集热点**: $TOTAL 个
- **数据源**: 2 个 (Hacker News, SearXNG)
- **搜索关键词**: ${#SEARCH_TOPICS[@]} 个
- **翻译状态**: ${TRANSLATE_ENABLED}（启用）
- **AI 摘要**: ${AI_SUMMARY_ENABLED}（优化版：摘要 + 智能内容方向 + 中文创作建议）

---

**下次更新**: 明天 08:00
**收集工具**: Content Hotspot Collector v5.1
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
# 发送到 Slack
# ============================================
echo ""
echo -e "${GREEN}=== 发送到 Slack ===${NC}"

# 提取热点摘要（前 3 个热点）
SLACK_MESSAGE="# 🔥 今日 AI 热点报告

**收集时间**: $(date '+%Y-%m-%d %H:%M:%S')
**收集热点**: $TOTAL 个
**数据源**: Hacker News, SearXNG

"

# 添加前 3 个热点到消息
INDEX=1
while IFS= read -r LINE; do
    if [ $INDEX -gt 3 ]; then
        break
    fi
    
    # 提取标题、热度、内容方向
    TITLE=$(echo "$LINE" | grep "^###" | sed 's/### //' | cut -d'-' -f1 | sed 's/^ *//;s/ *$//')
    HEAT=$(echo "$LINE" | grep "热度:" | sed 's/.*热度: //' | sed 's/-$//' | sed 's/^ *//;s/ *$//')
    DIRECTION=$(echo "$LINE" | grep "内容方向:" | sed 's/.*内容方向: //' | sed 's/^ *//;s/ *$//')
    
    if [ -n "$TITLE" ] && [ -n "$HEAT" ]; then
        SLACK_MESSAGE="${SLACK_MESSAGE}
**${INDEX}. ${TITLE}**
- 热度: ${HEAT}
- 方向: ${DIRECTION}

"
        INDEX=$((INDEX + 1))
    fi
done < "$REPORT_FILE"

SLACK_MESSAGE="${SLACK_MESSAGE}
📄 完整报告: \`/root/clawd/projects/info-search/data/hotspots/${REPORT_NAME}\`

下次更新: 明天 08:00"

# 发送到 Slack
/usr/bin/openclaw message send --channel slack --target C0ABSK92X4G --message "$SLACK_MESSAGE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 已发送到 Slack #clawdbot${NC}"
else
    echo -e "${YELLOW}⚠ Slack 发送失败（可能需要配置）${NC}"
fi

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
echo "  - AI 摘要: ${AI_SUMMARY_ENABLED}（优化版）"
echo "  - 改进 HTML 清理、智能内容方向判断、中文创作建议"
echo "  - 自动发送到 Slack: 启用"
echo ""
