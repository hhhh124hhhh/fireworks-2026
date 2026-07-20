#!/bin/bash
# 测试 Fallback 功能

echo "=========================================="
echo "Fallback 功能测试"
echo "=========================================="
echo ""

SCRIPT_DIR="/root/clawd/projects/info-search/scripts"
cd "$SCRIPT_DIR"

# 保存原始配置
TAVILY_KEY=$TAVILY_API_KEY
SEARXNG_URL=$SEARXNG_URL

echo "测试 1: 正常搜索（使用 Tavily）"
echo "----------------------------------------"
python3 search-wrapper.py "测试关键词" 1 2>&1 | grep "tavily 搜索成功"
echo ""

echo "测试 2: 指定使用 SearXNG"
echo "----------------------------------------"
timeout 10 python3 search-wrapper.py "测试关键词" 1 2>&1 | grep -E "(SearXNG|searxng)" | head -2
echo ""

echo "测试 3: 指定使用 Brave"
echo "----------------------------------------"
python3 search-wrapper.py "测试关键词" 1 2>&1 | grep -E "(Brave|brave)" | head -2
echo ""

echo "=========================================="
echo "Fallback 功能测试完成！"
echo "=========================================="
