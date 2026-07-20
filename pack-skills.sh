#!/bin/bash

# 测试并打包技能的脚本

SKILLS_DIR="skills"
OUTPUT_DIR="dist"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 需要打包的技能列表
SKILLS=(
    "creative-illustration"
    "game-character-gen"
    "style-transfer"
    "sql-assistant"
    "interview-coach"
    "openai-image-gen"
    "prompt-craft"
    "ai-music-prompts"
    "ad-creative-generator"
)

echo "开始测试并打包技能..."
echo "====================="

for skill in "${SKILLS[@]}"; do
    skill_dir="$SKILLS_DIR/$skill"
    skill_file="$OUTPUT_DIR/$skill.skill"

    echo ""
    echo "处理技能: $skill"

    # 检查技能目录是否存在
    if [ ! -d "$skill_dir" ]; then
        echo "❌ 错误: 技能目录不存在 $skill_dir"
        continue
    fi

    # 检查 SKILL.md 是否存在
    if [ ! -f "$skill_dir/SKILL.md" ]; then
        echo "❌ 错误: SKILL.md 不存在"
        continue
    fi

    # 验证 frontmatter (检查是否包含 name 和 description)
    if ! grep -q "^name:" "$skill_dir/SKILL.md"; then
        echo "❌ 错误: SKILL.md 缺少 name 字段"
        continue
    fi

    if ! grep -q "^description:" "$skill_dir/SKILL.md"; then
        echo "❌ 错误: SKILL.md 缺少 description 字段"
        continue
    fi

    # 提取 name 和 description
    name=$(grep "^name:" "$skill_dir/SKILL.md" | head -1 | sed 's/^name: //' | tr -d '"')
    description=$(grep "^description:" "$skill_dir/SKILL.md" | head -1 | sed 's/^description: //' | cut -c1-80)

    echo "  ✓ 验证通过"
    echo "  Name: $name"
    echo "  Description: $description..."

    # 打包成 .skill 文件
    cd "$skill_dir"
    zip -r "../../$skill_file" . -q
    cd ../..

    # 检查打包是否成功
    if [ -f "$skill_file" ]; then
        size=$(du -h "$skill_file" | cut -f1)
        echo "  ✓ 打包成功: $skill_file ($size)"
    else
        echo "❌ 打包失败"
    fi
done

echo ""
echo "====================="
echo "打包完成！"
echo "输出目录: $OUTPUT_DIR"
ls -lh "$OUTPUT_DIR"
