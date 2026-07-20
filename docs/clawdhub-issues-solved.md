# Clawdbot 问题记录 - 根本原因和解决方案

**日期**: 2026-01-30 17:35
**状态**: 已找到根本原因

---

## 🔍 问题诊断总结

### 1. ✅ ClawdHub Token 问题 - 根本原因

**问题原因**:
- ClawdHub CLI **默认使用错误的 registry URL**
- 必须 **明确指定** `--registry https://www.clawhub.ai/api` 参数
- 必须 **明确指定** `--workdir /root/clawd/generated-skills` 参数

**关键发现**:
```
clawdhub publish <path>

默认行为：
  - registry: 使用默认值（错误的！）
  - workdir: 使用默认值（可能是错的！）

正确行为：
  - registry: https://www.clawhub.ai/api ✅
  - workdir: /root/clawd/generated-skills ✅
```

---

### 2. ⚠️ 之前尝试的失败原因

| 尝试方法 | 失败原因 |
|----------|---------|
| `clawdhub login --token <token> --no-browser` | ❌ 可能没有使用正确的 registry |
| `export CLAWDHUB_TOKEN=<token>` | ❌ 环境变量可能不够 |
| `echo "token=..." > ~/.clawdhubrc` | ❌ 配置文件可能不支持 |
| `clawdhub publish /tmp/skill-folder` | ❌ 默认 registry 错误 |

---

### 3. ✅ 正确的解决方案

**正确命令**:
```bash
clawdhub \
  --registry https://www.clawhub.ai/api \
  --workdir /root/clawd/generated-skills \
  publish \
  --version 1.0.0 \
  <技能文件夹名>
```

**示例**:
```bash
# 上传第一个 Skill
clawdhub \
  --registry https://www.clawhub.ai/api \
  --workdir /root/clawd/generated-skills \
  publish \
  --version 1.0.0 \
  ai-from-trueslazac

# 上传第二个 Skill
clawdhub \
  --registry https://www.clawhub.ai/api \
  --workdir /root/clawd/generated-skills \
  publish \
  --version 1.0.0 \
  prompt-from-lexx-aura
```

---

### 4. ✅ 创建新的上传脚本

**脚本位置**: `/root/clawd/scripts/upload-to-clawhub.sh`

**功能**:
- 使用正确的 registry URL
- 使用正确的 workdir
- 自动上传所有 Skills
- 显示上传结果

---

### 5. 🔍 搜索已上传的 Skills

**搜索地址**: https://www.clawhub.ai/

**需要上传的 Skills**:
1. `ai-from-trueslazac` - AI 游戏视频 Prompt
2. `prompt-from-lexx-aura` - 超写实人像 Prompt

---

## 🔧 实施计划

### 阶段 1: 创建新的上传脚本

**目标**: 使用正确的参数

**步骤**:
1. 创建 `/root/clawd/scripts/upload-to-clawhub.sh`
2. 使用 `--registry https://www.clawhub.ai/api`
3. 使用 `--workdir /root/clawd/generated-skills`
4. 自动上传所有 Skills

---

### 阶段 2: 测试上传

**目标**: 验证命令是否正常工作

**步骤**:
1. 运行上传脚本
2. 检查输出
3. 在 ClawdHub 搜索确认

---

### 阶段 3: 集成到自动化流程

**目标**: 将上传集成到全源收集流程

**步骤**:
1. 修改 `/root/clawd/scripts/full-prompt-workflow.sh`
2. 在转换阶段后添加上传阶段
3. 使用正确的 registry 和 workdir 参数

---

## 📊 关键发现

| 发现 | 重要性 | 说明 |
|------|--------|------|
| **Registry URL** | ⭐⭐⭐⭐⭐ | 必须明确指定 |
| **Workdir** | ⭐⭐⭐⭐⭐ | 必须明确指定 |
| **Token 验证** | ⭐⭐⭐⭐ | 可能需要登录（但主要问题是 registry） |
| **文件位置** | ⭐⭐⭐ | 技能文件必须在 workdir 内 |

---

## 🎯 解决方案总结

### 根本原因
ClawdHub CLI 默认使用错误的 registry URL，必须明确指定。

### 正确命令格式
```bash
clawdhub \
  --registry https://www.clawhub.ai/api \
  --workdir /root/clawd/generated-skills \
  publish \
  --version 1.0.0 \
  <技能文件夹名>
```

### 下一步
1. ✅ 创建新的上传脚本（使用正确的参数）
2. ✅ 测试上传
3. ✅ 在 ClawdHub 搜索确认
4. ✅ 集成到自动化流程

---

*记录更新时间: 2026-01-30 17:35*
