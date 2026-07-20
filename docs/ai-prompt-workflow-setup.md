# AI Prompt Workflow - 配置指南

## 问题诊断

整合测试脚本现在可以正常运行，但由于缺少 API Token 配置，导致数据抓取失败。

## 解决步骤

### 1️⃣ 配置 API Tokens

#### 方式 A: 编辑环境变量文件（推荐）

```bash
# 编辑配置文件
nano /root/clawd/.env.d/ai-prompt-workflow.env
```

填入你的 API Keys：

```bash
# GitHub API Token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxx"

# HuggingFace Token
export HUGGINGFACE_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxx"

# Anthropic API Key（必需，用于评估）
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxx"

# Langfuse（可选）
export LANGFUSE_PUBLIC_KEY="pk-xxxxxxxxxxxxx"
export LANGFUSE_SECRET_KEY="sk-xxxxxxxxxxxxx"
```

保存后加载：

```bash
source /root/clawd/.env.d/ai-prompt-workflow.env
```

#### 方式 B: 直接写入 ~/.bashrc

```bash
nano ~/.bashrc
```

在文件末尾添加：

```bash
# AI Prompt Workflow
export GITHUB_TOKEN="your_token_here"
export HUGGINGFACE_TOKEN="your_token_here"
export ANTHROPIC_API_KEY="your_anthropic_key_here"
```

保存后重新加载：

```bash
source ~/.bashrc
```

### 2️⃣ 验证配置

```bash
# 检查环境变量
echo "GITHUB_TOKEN: ${GITHUB_TOKEN:+已设置}"
echo "HUGGINGFACE_TOKEN: ${HUGGINGFACE_TOKEN:+已设置}"
echo "ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:+已设置}"
```

### 3️⃣ 测试数据抓取

```bash
# 测试模式（不发布）
bash /root/clawd/scripts/integrated-prompt-workflow.sh --test-mode
```

### 4️⃣ 查看报告

```bash
# 查看最新报告
ls -lt /root/clawd/reports/integrated-workflow-report-*.md | head -1 | xargs cat
```

## API Key 获取指南

### GitHub Token
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制 token

### HuggingFace Token
1. 访问 https://huggingface.co/settings/tokens
2. 点击 "New token"
3. 选择权限（至少需要 read 权限）
4. 生成并复制 token

### Anthropic API Key (必需)
1. 访问 https://console.anthropic.com/
2. 注册/登录
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制 key（格式：`sk-ant-xxx`）

### Langfuse（可选）
1. 访问 https://cloud.langfuse.com/
2. 注册账户
3. 获取 Public Key 和 Secret Key
4. 填入环境变量

## 故障排查

### 问题：抓取了 0 个提示词

**原因：** API Token 未配置或无效

**解决：**
```bash
# 检查 token 是否设置
echo $GITHUB_TOKEN

# 重新加载环境变量
source /root/clawd/.env.d/ai-prompt-workflow.env
```

### 问题：HuggingFace 数据集加载失败

**已修复：** 已从配置中移除不存在的数据集 `prompts/prompts`

### 问题：评估失败

**原因：** ANTHROPIC_API_KEY 未设置

**解决：**
1. 确保 `ANTHROPIC_API_KEY` 已设置
2. 确保账户有足够余额
3. 检查 key 格式是否正确（`sk-ant-xxx`）

## 下一步

配置完成后，你可以：

1. **手动运行测试**
   ```bash
   bash /root/clawd/scripts/integrated-prompt-workflow.sh --test-mode
   ```

2. **设置定时任务（每天早上 9 点）**
   ```bash
   # 编辑 crontab
   crontab -e

   # 添加以下行
   0 9 * * * cd /root/clawd && bash scripts/integrated-prompt-workflow.sh >> logs/cron-integrated.log 2>&1
   ```

3. **查看日志**
   ```bash
   tail -f /root/clawd/logs/integrated-prompt-workflow.log
   ```

## 当前状态

✅ 代码语法错误已修复
✅ 配置文件已更新（移除无效数据集）
⚠️  需要配置 API Tokens 才能正常抓取数据

配置完成后再运行测试，就能看到实际的提示词抓取和评估结果了！🚀
