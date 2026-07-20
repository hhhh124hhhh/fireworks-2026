# AI 提示词系统快速参考

## 架构概览

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

## 快速开始

### 完整流程（一键执行）

```bash
# Stage 1: 数据发现
cd /root/clawd/skills/x-prompt-hunter
python3 main.py pipeline --query "AI prompts" --limit 100 --evaluate-limit 30

# Stage 2: 转换发布
cd /root/clawd/skills/prompt-to-skill-converter
python3 scripts/convert-prompts-to-skills.py --quality-threshold 80
clawdhub publish <skill-name>.skill --registry https://www.clawhub.ai/api
```

## 常用命令

### x-prompt-hunter（数据发现）

```bash
# 完整流程
python3 main.py pipeline --query "AI prompts" --limit 100 --evaluate-limit 30

# 单独抓取
python3 main.py fetch --query "creative writing" --limit 100

# 单独去重
python3 main.py deduplicate --input data/prompts.json --output data/prompts_clean.json

# 单独评估
python3 main.py evaluate --input data/prompts.json --batch-size 10

# 生成报告
python3 main.py report --type trend --days 30
```

### prompt-to-skill-converter（转换发布）

```bash
# 转换提示词为 Skills
python3 scripts/convert-prompts-to-skills.py \
  --input /root/clawd/skills/x-prompt-hunter/data/evaluation_results.json \
  --quality-threshold 80

# 打包技能
python3 /usr/lib/node_modules/clawdbot/skills/skill-creator/scripts/package_skill.py \
  /root/clawd/skills/<skill-name>

# 发布到 ClawdHub
clawdhub publish <skill-name>.skill --registry https://www.clawhub.ai/api
```

## 输出文件

### x-prompt-hunter

```
data/
├── prompts.json                    # 原始提示词
├── prompts_deduplicated.json       # 去重后
├── evaluation_results.json         # 评估结果（重要！）
└── langfuse_reports/               # 质量报告
```

### prompt-to-skill-converter

```
/root/clawd/skills/
├── example-prompt-skill/
│   └── SKILL.md
└── another-prompt-skill/
    └── SKILL.md
```

## 环境变量

```bash
# 必需
export ANTHROPIC_API_KEY="your_anthropic_api_key"
export CLAWDHUB_TOKEN="clh_Ki_M1Xiws5Qzi83gqdZhYG3jXSuZOnEfQOxhaRsjHcw"

# 可选
export GITHUB_TOKEN="your_github_token"
export HUGGINGFACE_TOKEN="your_huggingface_token"
export LANGFUSE_PUBLIC_KEY="your_public_key"
export LANGFUSE_SECRET_KEY="your_secret_key"
```

## Cron 配置

```bash
# 每天早上 9 点运行
0 9 * * * cd /root/clawd && /usr/local/bin/clawdbot sessions_spawn \
  --task "运行 AI 提示词系统完整流程" \
  --cleanup delete
```

## 故障排查

### 问题：评估失败
- 检查 ANTHROPIC_API_KEY
- 查看日志 `logs/prompt_hunter.log`

### 问题：转换失败
- 检查输入文件是否存在
- 调整质量阈值

### 问题：发布失败
- 检查 ClawdHub token（`clawdhub whoami`）
- 确保使用正确的 registry URL

## 技能状态

- ✅ **x-prompt-hunter**: 活跃（数据发现层）
- ✅ **prompt-to-skill-converter**: 活跃（转换发布层）
- ⚠️ **prompts-workflow**: 已废弃（保留参考）

## 文档

- 完整合档：`/root/clawd/skills/prompt-system-integration/README.md`
- 整合摘要：`/root/clawd/skills/prompt-system-integration/INTEGRATION-SUMMARY.md`

---

**最后更新**：2026-02-02
