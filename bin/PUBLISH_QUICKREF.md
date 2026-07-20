# 📋 Smart Publisher - 快速参考

## 常用命令

### 手动发布（推荐）
```bash
/root/clawd/bin/smart-publish-v2.sh ./my-skill --slug my-skill --name "My Skill" --version 1.0.0
```
- ✅ 自动质量检测
- 👀 显示审查结果
- ✋ 确认后发布

### 自动发布（CI/CD）
```bash
/root/clawd/bin/smart-publish-v2.sh ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --auto
```
- ✅ 检测通过直接发布
- 无需人工确认

### 强制发布（跳过检测）
```bash
/root/clawd/bin/smart-publish-v2.sh ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --force
```
- ⏭️ 跳过质量检测
- 适合紧急发布

## 参数速查

| 参数 | 必需 | 示例 |
|------|------|------|
| 路径 | ✅ | `./my-skill` |
| `--slug` | ✅ | `my-awesome-skill` |
| `--name` | ❌ | `"My Awesome Skill"` |
| `--version` | ❌ | `1.0.0` |
| `--changelog` | ❌ | `"Fixed bug #123"` |
| `--auto` | ❌ | 自动发布 |
| `--force` | ❌ | 跳过检测 |

## 质量检测标准

### 必须通过（Critical）
- ✅ SKILL.md 存在且完整
- ✅ 无硬编码密钥
- ✅ 无安全漏洞
- ✅ 依赖项已记录

### 建议修复（Warning）
- ⚠️ 添加错误处理示例
- ⚠️ 补充更多使用场景
- ⚠️ 改进代码注释

### 可选优化（Suggestion）
- 💡 添加更多示例
- 💡 优化文档结构
- 💡 添加测试用例

## 完整工作流

```bash
# 1. 创建技能
mkdir my-skill && cd my-skill

# 2. 编写 SKILL.md
cat > SKILL.md << 'EOF'
---
name: my-skill
description: My awesome skill
metadata: {}
---

# My Skill

## Usage
...
EOF

# 3. 添加代码文件
# ... write code ...

# 4. 返回上级目录
cd ..

# 5. 发布（自动检测 + 确认）
/root/clawd/bin/smart-publish-v2.sh \
  ./my-skill \
  --slug my-skill \
  --name "My Skill" \
  --version 1.0.0

# 6. 查看审查结果，确认发布
```

## 批量发布脚本

```bash
#!/bin/bash
# publish-all.sh

SKILLS=(
  "skill-a:slug-a:Skill A:1.0.0"
  "skill-b:slug-b:Skill B:1.2.0"
)

for s in "${SKILLS[@]}"; do
  IFS=':' read -r dir slug name ver <<< "$s"
  echo "Publishing: $name"
  /root/clawd/bin/smart-publish-v2.sh \
    "./skills/$dir" \
    --slug "$slug" \
    --name "$name" \
    --version "$ver" \
    --auto
done
```

## 前置要求

```bash
# 1. 安装 ClawdHub CLI
npm install -g clawdhub

# 2. 登录
clawdhub login

# 3. 安装 Claude Code（推荐）
npm install -g @anthropic-ai/claude-code

# 或安装 jq（用于解析 JSON）
apt-get install jq  # Ubuntu/Debian
# brew install jq   # macOS
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| Claude 未找到 | `npm install -g @anthropic-ai/claude-code` |
| 登录失败 | `clawdhub whoami` 检查状态 |
| 解析失败 | 安装 `jq` 工具 |
| 超时 | 增加 `REVIEW_TIMEOUT` 环境变量 |

## 完整文档

详细文档：`/root/clawd/docs/smart-publish-guide.md`

---

**提示**：第一次使用建议手动模式，熟悉后用 `--auto` 自动化！
