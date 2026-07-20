#!/bin/bash
# Search Wrapper 测试脚本

echo "=========================================="
echo "Search Wrapper 功能测试"
echo "=========================================="
echo ""

SCRIPT_DIR="/root/clawd/projects/info-search/scripts"
cd "$SCRIPT_DIR"

# 测试 1: 基本搜索
echo "测试 1: 基本搜索"
echo "----------------------------------------"
python3 search-wrapper.py "Python 编程" 2 2>&1 | grep -A 5 "找到"
echo ""

# 测试 2: Tavily 搜索（优先）
echo "测试 2: Tavily 搜索"
echo "----------------------------------------"
python3 search-wrapper.py "机器学习" 2 2>&1 | grep "tavily"
echo ""

# 测试 3: 错误处理（空查询）
echo "测试 3: 错误处理"
echo "----------------------------------------"
python3 search-wrapper.py "" 2 2>&1 | grep "搜索查询为空"
echo ""

echo "=========================================="
echo "测试完成！"
echo "=========================================="
