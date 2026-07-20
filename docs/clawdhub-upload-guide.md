# ClawdHub Skill 上传指南

## 📦 打包 Skill

ClawdHub 需要 `.skill` 格式的文件。让我帮你打包：

```bash
# 方式 1: 手动打包
cd /root/clawd/generated-skills

# 为每个 skill 创建目录并打包
for skill_md in *.md; do
    skill_name=$(basename "$skill_md" .md)
    mkdir -p "$skill_name"
    cp "$skill_md" "$skill_name/SKILL.md"
    cd "$skill_name"
    zip -r "../${skill_name}.skill" *
    cd ..
    rm -rf "$skill_name"
done

# 方式 2: 使用脚本打包
cat > /root/clawd/scripts/package-skills.sh << 'SCRIPT'
#!/bin/bash
# 打包所有生成的 Skills 为 .skill 文件

set -e

SOURCE_DIR="/root/clawd/generated-skills"
OUTPUT_DIR="/root/clawd/dist"

mkdir -p "$OUTPUT_DIR"

for skill_md in "$SOURCE_DIR"/*.md; do
    if [[ "$skill_md" == *"version-report.md"* ]]; then
        continue
    fi

    skill_name=$(basename "$skill_md" .md)
    echo "📦 打包: $skill_name"

    # 创建临时目录
    TEMP_DIR="/tmp/skill-package-$$"
    mkdir -p "$TEMP_DIR/$skill_name"
    cp "$skill_md" "$TEMP_DIR/$skill_name/SKILL.md"

    # 打包
    cd "$TEMP_DIR"
    zip -q -r "$OUTPUT_DIR/${skill_name}.skill" "$skill_name"

    # 清理
    rm -rf "$TEMP_DIR"
    echo "✅ 已生成: $OUTPUT_DIR/${skill_name}.skill"
done

echo "📊 打包完成！"
echo "📁 位置: $OUTPUT_DIR"
ls -lh "$OUTPUT_DIR"/*.skill
SCRIPT

chmod +x /root/clawd/scripts/package-skills.sh
```

---

## 🚀 上传到 ClawdHub

### 方式 1: 使用新 Token（推荐）

**步骤**：

1. **获取新 Token**
   - 访问: https://clawdhub.com/settings/tokens
   - 创建 Access Token
   - 权限: `write:packages`
   - 复制 token（格式：`clh_xxxxxxxxx`）

2. **打包 Skills**
   ```bash
   bash /root/clawd/scripts/package-skills.sh
   ```

3. **发布 Skills**
   ```bash
   clawdhub login --token <YOUR_TOKEN> --no-browser

   cd /root/clawd/dist

   for skill in *.skill; do
       clawdhub publish "$skill"
   done
   ```

---

### 方式 2: 使用在线编辑器

1. 访问 https://clawdhub.com/new
2. 选择 "From Scratch"
3. 粘贴 SKILL.md 内容
4. 填写名称和描述
5. 发布

---

## 📋 生成的 Skills

| Skill 文件 | 来源 | 质量 |
|-----------|------|------|
| `ai-from-trueslazac.md` | Twitter | ⭐⭐⭐ |
| `prompt-from-lexx-aura.md` | Twitter | ⭐⭐⭐⭐ |

---

## 💡 建议

1. **先打包**: 使用 `package-skills.sh` 打包成 .skill 文件
2. **测试 Token**: 创建新 token 并测试登录
3. **逐个上传**: 先上传一个测试，确保流程正常
4. **查看结果**: 在 ClawdHub 查看发布的 Skills

---

**需要我帮你打包并上传吗？** 只要你提供新的 token！
