#!/bin/bash
# 合并现有的数据源进行验证测试

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)

echo "=========================================="
echo "🔄 合并现有数据（测试模式）"
echo "=========================================="
echo ""

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
MERGED_FILE="/root/clawd/data/prompts/collected/merged-$TIMESTAMP.jsonl"
MERGED_COUNT=0

# 创建合并文件
> "$MERGED_FILE"

# 合并 Reddit
if [ -f /root/clawd/data/prompts/reddit-prompts.jsonl ] && [ -s /root/clawd/data/prompts/reddit-prompts.jsonl ]; then
    cat /root/clawd/data/prompts/reddit-prompts.jsonl >> "$MERGED_FILE"
    ADDED=$(wc -l < /root/clawd/data/prompts/reddit-prompts.jsonl)
    echo "✅ 合并 Reddit: $ADDED 条"
    MERGED_COUNT=$((MERGED_COUNT + ADDED))
fi

# 合并 GitHub
if [ -f /root/clawd/data/prompts/github-awesome-prompts.jsonl ] && [ -s /root/clawd/data/prompts/github-awesome-prompts.jsonl ]; then
    cat /root/clawd/data/prompts/github-awesome-prompts.jsonl >> "$MERGED_FILE"
    ADDED=$(wc -l < /root/clawd/data/prompts/github-awesome-prompts.jsonl)
    echo "✅ 合并 GitHub: $ADDED 条"
    MERGED_COUNT=$((MERGED_COUNT + ADDED))
fi

# 合并 SearXNG
if [ -f /root/clawd/data/prompts/collected.jsonl ] && [ -s /root/clawd/data/prompts/collected.jsonl ]; then
    cat /root/clawd/data/prompts/collected.jsonl >> "$MERGED_FILE"
    ADDED=$(wc -l < /root/clawd/data/prompts/collected.jsonl)
    echo "✅ 合并 SearXNG: $ADDED 条"
    MERGED_COUNT=$((MERGED_COUNT + ADDED))
fi

# 合并 Firecrawl
if [ -f /root/clawd/data/prompts/firecrawl-prompts.jsonl ] && [ -s /root/clawd/data/prompts/firecrawl-prompts.jsonl ]; then
    cat /root/clawd/data/prompts/firecrawl-prompts.jsonl >> "$MERGED_FILE"
    ADDED=$(wc -l < /root/clawd/data/prompts/firecrawl-prompts.jsonl)
    echo "✅ 合并 Firecrawl: $ADDED 条"
    MERGED_COUNT=$((MERGED_COUNT + ADDED))
fi

echo ""
echo "✅ 合并完成: $MERGED_COUNT 条 → $MERGED_FILE"

# 更新 latest 链接
ln -sf "$(basename "$MERGED_FILE")" /root/clawd/data/prompts/collected/latest.jsonl
echo "✅ Updated latest.jsonl symlink"

exit 0
