#!/bin/bash
# Video Prompt Generator - Test Examples
# 视频提示词生成器 - 测试示例

echo "============================================"
echo "Video Prompt Generator - Test Examples"
echo "视频提示词生成器 - 测试示例"
echo "============================================"
echo ""

# Example 1: List all styles
echo "Example 1: List all available styles"
echo "示例 1: 列出所有可用风格"
echo "----------------------------------------"
python3 main.py --list
echo ""
echo ""
echo "Press Enter to continue..."
read
echo ""

# Example 2: Generate prompts from topic
echo "Example 2: Generate prompts from topic"
echo "示例 2: 从主题生成提示词"
echo "----------------------------------------"
python3 main.py \
  --topic "一只可爱的猫咪在花园里玩耍" \
  --style "landscape" \
  --variants 3
echo ""
echo "Press Enter to continue..."
read
echo ""

# Example 3: Generate prompts from keywords
echo "Example 3: Generate prompts from keywords"
echo "示例 3: 从关键词生成提示词"
echo "----------------------------------------"
python3 main.py \
  --keywords "可爱,温暖,阳光" \
  --style "emotional" \
  --variants 2
echo ""
echo "Press Enter to continue..."
read
echo ""

# Example 4: Generate prompts in JSON format
echo "Example 4: Generate prompts in JSON format"
echo "示例 4: 生成 JSON 格式的提示词"
echo "----------------------------------------"
python3 main.py \
  --topic "产品展示" \
  --style "product" \
  --variants 3 \
  --output json \
  --file product_prompts.json
echo ""
echo "Press Enter to continue..."
read
echo ""

# Example 5: Generate prompts in Markdown format
echo "Example 5: Generate prompts in Markdown format"
echo "示例 5: 生成 Markdown 格式的提示词"
echo "----------------------------------------"
python3 main.py \
  --topic "美食烹饪" \
  --style "food" \
  --variants 2 \
  --output markdown \
  --file food_prompts.md
echo ""
echo "Press Enter to continue..."
read
echo ""

# Example 6: Generate prompts without enhancement
echo "Example 6: Generate prompts without enhancement"
echo "示例 6: 生成不增强的提示词"
echo "----------------------------------------"
python3 main.py \
  --topic "简单描述" \
  --style "landscape" \
  --no-enhance
echo ""
echo "Press Enter to continue..."
read
echo ""

# Example 7: Generate video (requires API key)
echo "Example 7: Generate video with Grok Imagine API"
echo "示例 7: 使用 Grok Imagine API 生成视频"
echo "----------------------------------------"
echo "Note: This requires XAI_API_KEY environment variable"
echo "注意：这需要设置 XAI_API_KEY 环境变量"
echo ""

if [ -z "$XAI_API_KEY" ]; then
    echo "XAI_API_KEY not set. Skipping video generation example."
    echo "未设置 XAI_API_KEY。跳过视频生成示例。"
    echo ""
    echo "To test video generation, set your API key:"
    echo "要测试视频生成，请设置您的 API 密钥："
    echo "  export XAI_API_KEY=\"your-api-key-here\""
    echo ""
else
    echo "XAI_API_KEY found. Generating video..."
    echo "找到 XAI_API_KEY。正在生成视频..."
    echo ""

    python3 main.py \
      --topic "简单的风景" \
      --style "landscape" \
      --generate-video \
      --duration 3 \
      --aspect-ratio 16:9
fi

echo ""
echo ""
echo "============================================"
echo "Test examples completed!"
echo "测试示例完成！"
echo "============================================"
echo ""
echo "Files generated / 生成的文件:"
echo "  - product_prompts.json (if not exists)"
echo "  - food_prompts.md (if not exists)"
echo ""
