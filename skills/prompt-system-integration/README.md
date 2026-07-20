# AI 提示词系统整合说明

## 架构概览

根据 Jack 的建议，我们将 AI 提示词系统整合为两阶段架构：

```
┌─────────────────────┐
│ x-prompt-hunter     │ ← 数据发现层（去重+评估）
└─────────┬───────────┘
        │ 高质量提示词
        ▼
┌─────────────────────┐
│ prompt-to-skill-    │ ← 转换发布层（SKILL.md + ClawdHub）
│ converter          │
└─────────────────────┘
```

## 技能整合状态

### ✅ 保留的技能

#### 1. x-prompt-hunter（数据发现层）
- **角色**：数据发现、去重、评估
- **核心功能**：
  - 语义去重（使用 sentence-transformers）
  - 多源抓取（GitHub、HuggingFace）
  - LLM 评估（Claude API）
  - Langfuse 追踪
- **输出**：高质量提示词列表（JSON 格式）
- **位置**：`/root/clawd/skills/x-prompt-hunter/`

#### 2. prompt-to-skill-converter（转换发布层）
- **角色**：转换、打包、发布
- **核心功能**：
  - 将提示词转换为 Skills
  - 生成 SKILL.md 文件
  - 打包技能文件
  - 发布到 ClawdHub
- **输入**：高质量提示词（来自 x-prompt-hunter）
- **输出**：可发布的 Skills
- **位置**：`/root/clawd/skills/prompt-to-skill-converter/`

### ⚠️ 废弃的技能

#### 3. prompts-workflow（已废弃）
- **废弃时间**：2026-02-02
- **原因**：功能已整合到两阶段架构中
- **状态**：已标记为废弃，保留文档作为参考
- **位置**：`/root/clawd/skills/prompts-workflow/`

## 推荐工作流

### 完整工作流（两阶段）

```bash
# ========================================
# Stage 1: Data Discovery & Quality Control
# ========================================
cd /root/clawd/skills/x-prompt-hunter

# 完整流程：抓取 → 去重 → 评估 → 生成报告
python3 main.py pipeline \
  --query "AI prompts" \
  --limit 100 \
  --batch-size 10 \
  --evaluate-limit 30

# 输出文件：
# - data/prompts.json                    # 原始提示词
# - data/prompts_deduplicated.json       # 去重后的提示词
# - data/evaluation_results.json         # 评估结果（高质量）
# - data/langfuse_reports/               # Langfuse 报告

# ========================================
# Stage 2: Conversion & Publishing
# ========================================
cd /root/clawd/skills/prompt-to-skill-converter

# 转换高质量提示词为 Skills
python3 scripts/convert-prompts-to-skills.py \
  --input /root/clawd/skills/x-prompt-hunter/data/evaluation_results.json \
  --quality-threshold 80 \
  --output-dir /root/clawd/skills

# 打包技能（针对每个生成的 skill）
python3 /usr/lib/node_modules/clawdbot/skills/skill-creator/scripts/package_skill.py \
  /root/clawd/skills/<skill-name>

# 发布到 ClawdHub
clawdhub publish <skill-name>.skill --registry https://www.clawhub.ai/api
```

### 快速测试模式

```bash
# Stage 1: 测试数据发现（少量数据）
cd /root/clawd/skills/x-prompt-hunter
python3 main.py pipeline --query "test" --limit 10 --evaluate-limit 5

# Stage 2: 测试转换（不实际创建文件）
cd /root/clawd/skills/prompt-to-skill-converter
python3 scripts/convert-prompts-to-skills.py --dry-run
```

## 数据流

```
x-prompt-hunter
├── data/prompts.json                    # 原始提示词
├── data/prompts_deduplicated.json       # 去重后（0.85 相似度阈值）
├── data/evaluation_results.json         # 评估后（只保留高质量）
│
▼
prompt-to-skill-converter
├── /root/clawd/skills/<skill-name>/    # 生成的技能目录
│   └── SKILL.md                        # 技能文档
│
▼
ClawdHub
└── <skill-name>.skill                  # 发布的技能包
```

## 技能唯一性

### 无重复功能

| 功能 | 所属技能 | 说明 |
|------|---------|------|
| 语义去重 | x-prompt-hunter | 唯一的去重实现 |
| 多源抓取 | x-prompt-hunter | GitHub、HuggingFace |
| LLM 评估 | x-prompt-hunter | Claude API 评估 |
| Langfuse 追踪 | x-prompt-hunter | 质量追踪 |
| 转换为 Skill | prompt-to-skill-converter | 唯一的转换实现 |
| 打包 Skill | prompt-to-skill-converter | package_skill.py |
| 发布到 ClawdHub | prompt-to-skill-converter | clawdhub publish |

### 已废弃的功能

| 旧技能 | 功能 | 新归属 |
|--------|------|--------|
| prompts-workflow | 收集 | x-prompt-hunter |
| prompts-workflow | 转换 | prompt-to-skill-converter |
| prompts-workflow | 发布 | prompt-to-skill-converter |
| prompts-workflow | 编排 | cron / sessions_spawn |

## Cron 集成

### 方式 1: 使用 sessions_spawn（推荐）

```bash
# 添加到 crontab
crontab -e

# 每天早上 9 点运行
0 9 * * * cd /root/clawd && /usr/local/bin/clawdbot sessions_spawn \
  --task "运行 AI 提示词系统完整流程：1. x-prompt-hunter 数据发现（抓取 100 条，评估 30 条）2. prompt-to-skill-converter 转换发布（质量阈值 80）" \
  --cleanup delete
```

### 方式 2: 分离的 Cron 任务

```bash
# 添加到 crontab
crontab -e

# Stage 1: 每天早上 8 点数据发现
0 8 * * * cd /root/clawd/skills/x-prompt-hunter && python3 main.py pipeline --query "AI prompts" --limit 100 --evaluate-limit 30

# Stage 2: 每天早上 9 点转换发布（依赖 Stage 1）
0 9 * * * cd /root/clawd/skills/prompt-to-skill-converter && python3 scripts/convert-prompts-to-skills.py --quality-threshold 80
```

## 环境变量

### x-prompt-hunter

```bash
# GitHub API（可选）
export GITHUB_TOKEN="your_github_token"

# HuggingFace Token（可选）
export HUGGINGFACE_TOKEN="your_huggingface_token"

# Claude API（必需，用于评估）
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# Langfuse（可选，用于质量追踪）
export LANGFUSE_PUBLIC_KEY="your_public_key"
export LANGFUSE_SECRET_KEY="your_secret_key"
```

### prompt-to-skill-converter

```bash
# ClawdHub Token（必需，用于发布）
export CLAWDHUB_TOKEN="clh_Ki_M1Xiws5Qzi83gqdZhYG3jXSuZOnEfQOxhaRsjHcw"

# Twitter API Key（可选，用于直接收集）
export TWITTER_API_KEY="your_twitter_api_key"

# SearXNG URL（可选，用于直接收集）
export SEARXNG_URL="http://localhost:8080"
```

## 维护任务

### 定期检查

1. **每日**：
   - 检查数据收集质量（查看 langfuse_reports/）
   - 检查转换成功率（查看技能目录）
   - 检查发布状态（查看 ClawdHub）

2. **每周**：
   - 清理旧的临时文件（data/ 目录）
   - 更新搜索关键词（config.yaml）
   - 调整质量阈值（根据效果）

3. **每月**：
   - 审查生成的技能质量
   - 收集用户反馈
   - 更新评估标准

### 日志文件

- `x-prompt-hunter/logs/prompt_hunter.log` - 数据发现日志
- `x-prompt-hunter/data/langfuse_reports/` - 质量追踪报告
- `prompt-to-skill-converter/scripts/convert.log` - 转换日志（如果存在）

## 故障排查

### 问题：x-prompt-hunter 评估失败

**检查**：
1. ANTHROPIC_API_KEY 是否正确设置
2. API key 是否有足够余额
3. 查看日志 `logs/prompt_hunter.log`

### 问题：转换失败

**检查**：
1. 输入文件是否存在（`data/evaluation_results.json`）
2. 质量阈值是否合理
3. 输出目录是否有写入权限

### 问题：发布失败

**检查**：
1. ClawdHub token 是否有效（`clawdhub whoami`）
2. Registry URL 是否正确（`--registry https://www.clawhub.ai/api`）
3. 技能文件是否完整（`.skill` 文件）

## 未来改进

1. **自动化编排**：创建统一的编排脚本（整合两阶段）
2. **质量监控**：自动监控技能质量并报警
3. **智能去重**：改进语义去重算法
4. **多语言支持**：支持中英文提示词
5. **A/B 测试**：测试不同质量阈值的效果

## 整合时间线

- **2026-02-02**：完成架构整合
- **2026-02-01**：废弃 prompts-workflow
- **2026-01-31**：初始架构设计

## 联系方式

如有问题或建议，请联系 Jack。

---

**最后更新**：2026-02-02
**版本**：1.0.0
