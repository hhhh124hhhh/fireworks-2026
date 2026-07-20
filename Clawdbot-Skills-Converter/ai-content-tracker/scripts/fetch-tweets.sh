#!/bin/bash

# AI 内容抓取脚本
# 使用 bird CLI 抓取 X (Twitter) 上 AI 玩法相关内容

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.json"
DATA_DIR="$SCRIPT_DIR/../data"
TODAY=$(date +%Y-%m-%d)
OUTPUT_FILE="$DATA_DIR/tweets_$TODAY.json"

# 创建数据目录
mkdir -p "$DATA_DIR"

echo "🐦 开始抓取 AI 玩法相关内容..."
echo "📅 日期: $TODAY"
echo ""

# 读取配置
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在: $CONFIG_FILE"
    exit 1
fi

# 解析搜索查询
QUERIES=$(node -e "
    const config = require('$CONFIG_FILE');
    config.twitter.searchQueries.forEach(q => console.log(q));
")

echo "🔍 搜索查询数: $(echo "$QUERIES" | wc -l)"
echo ""

# 检查 bird 是否可用
if ! command -v bird &> /dev/null; then
    echo "❌ bird CLI 未安装"
    echo "   安装: npm install -g @steipete/bird"
    exit 1
fi

# 检查 cookies
echo "🔍 检查 bird cookies..."
if ! bird check &> /dev/null; then
    echo "⚠️  bird 未找到有效的 cookies"
    echo ""
    echo "💡 解决方法:"
    echo "   1. 访问 https://x.com 并登录"
    echo "   2. 确保浏览器 cookies 可访问"
    echo "   3. 或使用 --auth-token 手动设置"
    echo ""
    echo "   跳过抓取，创建空数据文件..."
    echo "[]" > "$OUTPUT_FILE"
    echo "✅ 空数据文件已创建"
    exit 0
fi

echo "✅ bird cookies 有效"
echo ""

# 创建输出文件
echo "[]" > "$OUTPUT_FILE"

# 抓取每个查询
echo "📊 开始抓取..."
echo ""

ALL_RESULTS=""
QUERY_INDEX=0

while IFS= read -r query; do
    QUERY_INDEX=$((QUERY_INDEX + 1))
    echo "[$QUERY_INDEX] 搜索: $query"

    # 使用 bird 搜索（JSON 格式）
    SEARCH_OUTPUT=$(bird search "$query" -n 10 --json 2>&1)

    # 检查是否是有效 JSON
    if ! echo "$SEARCH_OUTPUT" | jq . >/dev/null 2>&1; then
        echo "    ⚠️  无效的 JSON，跳过"
        continue
    fi

    # 保存到临时文件
    TEMP_FILE="$DATA_DIR/temp_$QUERY_INDEX.json"
    echo "$SEARCH_OUTPUT" > "$TEMP_FILE"

    COUNT=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$TEMP_FILE')).length)")
    echo "    ✓ 抓取完成 ($COUNT 条)"

done <<< "$QUERIES"

# 合并所有结果
echo ""
echo "📝 合并所有结果..."

COMBINED="["
FIRST=true

for file in $DATA_DIR/temp_*.json; do
    if [ -f "$file" ]; then
        if [ "$FIRST" = true ]; then
            FIRST=false
        else
            COMBINED="$COMBINED,"
        fi
        # 读取并追加（去掉外层 []）
        CONTENT=$(cat "$file")
        # 移除开头的 [ 和结尾的 ]
        CONTENT=$(echo "$CONTENT" | sed 's/^\[//' | sed 's/\]$//')
        COMBINED="$COMBINED$CONTENT"
    fi
done

COMBINED="$COMBINED]"

# 保存到最终文件
echo "$COMBINED" > "$OUTPUT_FILE"

# 清理临时文件
rm -f $DATA_DIR/temp_*.json

COUNT=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$OUTPUT_FILE')).length)")

echo ""
echo "✅ 抓取完成！"
echo "📊 总推文数: $COUNT"
echo "📂 输出文件: $OUTPUT_FILE"
echo ""
