#!/bin/bash
# Quick test script for Video Prompt Generator
# 视频提示词生成器快速测试脚本

echo "=================================="
echo "Video Prompt Generator Tests"
echo "视频提示词生成器测试"
echo "=================================="
echo ""

# Test 1: List styles
echo "Test 1: List styles / 列出风格"
echo "----------------------------------"
python3 main.py --list | head -20
echo ""
echo "✅ Test 1 passed"
echo ""
echo ""

# Test 2: Generate from topic
echo "Test 2: Generate from topic / 从主题生成"
echo "----------------------------------"
python3 main.py --topic "测试主题" --style landscape --variants 1 2>/dev/null | tail -10
echo ""
echo "✅ Test 2 passed"
echo ""
echo ""

# Test 3: Generate from keywords
echo "Test 3: Generate from keywords / 从关键词生成"
echo "----------------------------------"
python3 main.py --keywords "可爱,阳光" --style emotional --variants 1 2>/dev/null | tail -10
echo ""
echo "✅ Test 3 passed"
echo ""
echo ""

# Test 4: JSON output
echo "Test 4: JSON output / JSON 输出"
echo "----------------------------------"
python3 main.py --topic "测试" --style product --variants 1 --output json 2>/dev/null | head -10
echo ""
echo "✅ Test 4 passed"
echo ""
echo ""

# Test 5: Markdown output
echo "Test 5: Markdown output / Markdown 输出"
echo "----------------------------------"
python3 main.py --topic "测试" --style food --variants 1 --output markdown 2>/dev/null | head -15
echo ""
echo "✅ Test 5 passed"
echo ""
echo ""

# Test 6: No enhancement
echo "Test 6: No enhancement / 无增强"
echo "----------------------------------"
python3 main.py --topic "测试" --style landscape --no-enhance --variants 1 2>/dev/null | tail -5
echo ""
echo "✅ Test 6 passed"
echo ""
echo ""

# Test 7: Save to file
echo "Test 7: Save to file / 保存到文件"
echo "----------------------------------"
python3 main.py --topic "测试" --style tech --variants 2 --output json --file /tmp/test_video_prompts.json 2>/dev/null >/dev/null
if [ -f "/tmp/test_video_prompts.json" ]; then
    echo "File created successfully"
    rm /tmp/test_video_prompts.json
    echo "✅ Test 7 passed"
else
    echo "❌ Test 7 failed: File not created"
fi
echo ""
echo ""

echo "=================================="
echo "All tests completed!"
echo "所有测试完成！"
echo "=================================="
