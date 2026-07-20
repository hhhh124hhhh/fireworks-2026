#!/bin/bash

# Content Hotspot Collector v0.6
# 多平台热点收集脚本（调试版）
# 用于自媒体创作者的内容灵感发现

set -e

# 配置
PROJECT_DIR="/root/clawd/projects/info-search"
DATA_DIR="$PROJECT_DIR/data/hotspots"
MEMORY_DIR="$root/clawd/memory/hotspots"
DATE=$(date +"%Y-%m-%d")
DATETIME=$(date +"%Y%m%d_%H%M%S")

# API 配置
HN_API_URL="https://hacker-news.firebaseio.com/v0"

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
TEMP_FILE="/tmp/hotspots-$DATETIME.txt"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Content Hotspot Collector v0.6 ===${NC}"
echo "开始收集真实热点..."
echo ""

# 初始化临时文件
> "$TEMP_FILE"

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
    
    # 逐个检查故事（限制前 15 个）
    COUNT=0
    for STORY_ID in $HN_IDS; do
        if [ $COUNT -ge 15 ]; then
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
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
" 2>/dev/null || echo "")
            
            if [ -n "$STORY_INFO" ] && ! echo "$STORY_INFO" | grep -q "^Error:"; then
                # 正确解析字段
                TITLE=$(echo "$STORY_INFO" | cut -d'|' -f1)
                SCORE=$(echo "$STORY_INFO" | cut -d'|' -f2)
                URL=$(echo "$STORY_INFO" | cut -d'|' -f3)
                
                # 调试输出
                echo "  [DEBUG] STORY_INFO=$STORY_INFO" >&2
                echo "  [DEBUG] TITLE=$TITLE" >&2
                echo "  [DEBUG] SCORE=$SCORE" >&2
                echo "  [DEBUG] URL=$URL" >&2
                
                echo "  ${GREEN}+${NC} $TITLE (score: $SCORE)"
                echo "HN|$TITLE|$SCORE|$URL" >> "$TEMP_FILE"
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
        print(f'SearXNG:{title}|0|{url}')
except:
    pass
" >> "$TEMP_FILE" 2>/dev/null
    fi
done

echo -e "${GREEN}✓ SearXNG 搜索完成${NC}"

# ============================================
# 统计和排序
# ============================================
echo ""
echo -e "${GREEN}=== 统计和排序 ===${NC}"

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

---

## 🔥 热门热点

EOF

# 添加热点到报告（前 10 个）
INDEX=1
head -n 10 "$TEMP_FILE" | while read -r HOTSPOT; do
    # 调试输出
    echo "[DEBUG] HOTSPOT=$HOTSPOT" >&2
    
    SOURCE=$(echo "$HOTSPOT" | cut -d'|' -f1)
    TITLE=$(echo "$HOTSPOT" | cut -d'|' -f2)
    SCORE=$(echo "$HOTSPOT" | cut -d'|' -f3)
    URL=$(echo "$HOTSPOT" | cut -d'|' -f4)
    
    # 调试输出
    echo "[DEBUG] SOURCE=$SOURCE" >&2
    echo "[DEBUG] TITLE=$TITLE" >&2
    echo "[DEBUG] SCORE=$SCORE" >&2
    echo "[DEBUG] URL=$URL" >&2
    
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
    cat >> "$REPORT_FILE" << EOF
### $INDEX. $TITLE
- **热度**: $HEAT
- **来源**: $SOURCE
EOF
    
    if [ -n "$SCORE" ] && [ "$SCORE" != "0" ]; then
        echo "- **分数**: $SCORE" >> "$REPORT_FILE"
    fi
    
    if [ -n "$URL" ] && [ "$URL" != "null" ] && [ "$URL" != "" ]; then
        echo "- **链接**: [查看详情]($URL)" >> "$REPORT_FILE"
    fi
    
    echo "" >> "$REPORT_FILE"
    
    INDEX=$((INDEX + 1))
done

# 添加选题建议
cat >> "$REPORT_FILE" << EOF

---

## 💡 选题建议

EOF

# 基于 Hacker News 热点生成建议
HN_HOTSPOTS=$(grep "^HN:" "$TEMP_FILE" | head -n 3)
COUNT=1

if [ -n "$HN_HOTSPOTS" ]; then
    echo "$HN_HOTSPOTS" | while read -r HOTSPOT; do
        TITLE=$(echo "$HOTSPOT" | cut -d'|' -f2)
        
        # 生成建议
        SUGGESTION="$TITLE 深度解读"
        
        case "$TITLE" in
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
        
        cat >> "$REPORT_FILE" << EOF
### $COUNT. **$SUGGESTION**
   - 基于热点: $TITLE
   - 难度: ⭐⭐⭐
   
EOF
        
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

---

**下次更新**: 明天 08:00  
**收集工具**: Content Hotspot Collector v0.6
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
echo -e "${BLUE}提示:${NC} 使用真实数据源，带调试输出"
echo ""
