# AI 提示词系统整合摘要

## 整合完成时间
2026-02-02 09:30

## 架构变化

### 整合前（三技能架构）
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ x-prompt-hunter │    │ prompts-        │    │ prompt-to-skill-│
│                 │    │ workflow        │    │ converter       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
     去重+评估              收集+转换+发布          转换+发布
```

### 整合后（两技能架构）
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

## 已完成的工作

### 1. 更新 SKILL.md 文档

#### ✅ x-prompt-hunter
- 添加架构定位说明（数据发现层）
- 明确与 prompt-to-skill-converter 的关系
- 添加推荐工作流说明

#### ✅ prompt-to-skill-converter
- 添加架构定位说明（转换发布层）
- 添加对 x-prompt-hunter 的依赖说明
- 更新推荐工作流（两阶段）
- 标记遗留功能

#### ⚠️ prompts-workflow
- 标记为废弃（DEPRECATED）
- 添加废弃说明和替代方案
- 提供迁移指南
- 保留原始文档作为参考

### 2. 创建整合文档

#### ✅ /root/clawd/skills/prompt-system-integration/README.md
- 完整的架构说明
- 推荐工作流（完整版 + 快速测试版）
- 数据流图
- 技能唯一性检查
- Cron 集成方案
- 环境变量配置
- 维护任务清单
- 故障排查指南
- 未来改进方向

### 3. 技能唯一性验证

| 功能 | 所属技能 | 唯一性 |
|------|---------|--------|
| 语义去重 | x-prompt-hunter | ✅ 唯一 |
| 多源抓取（GitHub/HF） | x-prompt-hunter | ✅ 唯一 |
| LLM 评估 | x-prompt-hunter | ✅ 唯一 |
| Langfuse 追踪 | x-prompt-hunter | ✅ 唯一 |
| 转换为 Skill | prompt-to-skill-converter | ✅ 唯一 |
| 打包 Skill | prompt-to-skill-converter | ✅ 唯一 |
| 发布到 ClawdHub | prompt-to-skill-converter | ✅ 唯一 |

### 4. 废弃技能处理

- **prompts-workflow**: 已标记为废弃，保留文档
- **状态**: 不会删除，仅作为参考
- **原因**: 功能已整合到两阶段架构中

## 需要清理的脚本（待处理）

以下脚本存在重复功能，建议清理：

### 收集相关（重复）
- `scripts/collect-all-sources-prompts.sh` - 多源收集（旧）
- `scripts/collect-all-sources-prompts-v2.sh` - 多源收集 v2（新）
- `scripts/collect-github-prompts.py` - GitHub 收集
- `scripts/collect-google-sora2-prompts.py` - 特定收集
- `scripts/collect-image-video-prompts.py` - 特定收集
- `scripts/run-collect-prompts.sh` - 运行收集

**建议**：统一使用 `x-prompt-hunter` 的收集功能

### 搜索相关（重复）
- `scripts/search-x-prompts.py` - X 搜索
- `scripts/twitter_prompt_search.py` - Twitter 搜索
- `scripts/twitter_prompt_search_simple.py` - Twitter 搜索简化版

**建议**：整合到 `x-prompt-hunter` 或使用 searXNG

### 评估相关（重复）
- `scripts/analyze-prompts-quality.py` - 质量分析
- `scripts/prompt-evaluator.py` - 提示词评估

**建议**：统一使用 `x-prompt-hunter` 的 LLM 评估

### 转换相关（重复）
- `scripts/generate-google-sora2-skills.py` - 特定转换
- `scripts/tweet-to-skill-converter.js` - Tweet 转 Skill
- `scripts/convert-prompts-to-skills.py` - 批量转换（已移至 skill 内）

**建议**：统一使用 `prompt-to-skill-converter` 的转换功能

### 打包发布相关（重复）
- `scripts/package-all-skills.sh` - 批量打包
- `scripts/package-single-skill.sh` - 单个打包
- `scripts/package-skills.sh` - 打包
- `scripts/batch-upload-skills-v3.sh` - 批量上传
- `scripts/batch-upload-new-skills.sh` - 批量上传新技能
- `scripts/batch-publish-skills-from-source.sh` - 批量发布
- `scripts/auto-publish-skills.sh` - 自动发布
- `scripts/publish-skills-with-retry.sh` - 带重试发布
- `scripts/batch-process-all-skills.sh` - 批量处理
- `scripts/analyze-skills-for-publish.sh` - 分析可发布技能

**建议**：统一使用 `prompt-to-skill-converter` 的打包发布流程

### 其他相关脚本（保留）
- `scripts/init_skill.py` - 技能初始化（保留）
- `scripts/refactor-skills.py` - 技能重构（保留）
- `scripts/refactor-single-skill.py` - 单个技能重构（保留）
- `scripts/refactor-nonstandard-skills.py` - 非标准技能重构（保留）
- `scripts/cleanup-duplicate-skills.py` - 清理重复技能（保留）
- `scripts/track-clawdhub-skills.sh` - 追踪 ClawdHub 技能（保留）
- `scripts/update-skill-descriptions.py` - 更新技能描述（保留）
- `scripts/ai-prompt-hunter.sh` - AI 提示词猎手（保留）
- `scripts/full-prompt-workflow.sh` - 完整工作流（保留，但标记为遗留）

## 推荐工作流

### 完整流程（每日自动执行）

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

# ========================================
# Stage 2: Conversion & Publishing
# ========================================
cd /root/clawd/skills/prompt-to-skill-converter

# 转换高质量提示词为 Skills
python3 scripts/convert-prompts-to-skills.py \
  --input /root/clawd/skills/x-prompt-hunter/data/evaluation_results.json \
  --quality-threshold 80

# 打包并发布（需要针对每个 skill）
for skill_dir in /root/clawd/skills/*/; do
  if [ -f "$skill_dir/SKILL.md" ]; then
    skill_name=$(basename "$skill_dir")
    python3 /usr/lib/node_modules/clawdbot/skills/skill-creator/scripts/package_skill.py "$skill_dir"
    clawdhub publish "${skill_name}.skill" --registry https://www.clawhub.ai/api
  fi
done
```

### Cron 配置

```bash
# 添加到 crontab
crontab -e

# 每天早上 9 点运行完整流程
0 9 * * * cd /root/clawd && /usr/local/bin/clawdbot sessions_spawn \
  --task "运行 AI 提示词系统完整流程：1. x-prompt-hunter 数据发现（抓取 100 条，评估 30 条）2. prompt-to-skill-converter 转换发布（质量阈值 80）" \
  --cleanup delete
```

## 环境变量配置

### 必需的环境变量

```bash
# Claude API（x-prompt-hunter 评估用）
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# ClawdHub Token（prompt-to-skill-converter 发布用）
export CLAWDHUB_TOKEN="clh_Ki_M1Xiws5Qzi83gqdZhYG3jXSuZOnEfQOxhaRsjHcw"
```

### 可选的环境变量

```bash
# GitHub API（x-prompt-hunter 抓取用）
export GITHUB_TOKEN="your_github_token"

# HuggingFace Token（x-prompt-hunter 抓取用）
export HUGGINGFACE_TOKEN="your_huggingface_token"

# Langfuse（x-prompt-hunter 追踪用）
export LANGFUSE_PUBLIC_KEY="your_public_key"
export LANGFUSE_SECRET_KEY="your_secret_key"

# Twitter API（直接收集用）
export TWITTER_API_KEY="your_twitter_api_key"

# SearXNG URL（直接收集用）
export SEARXNG_URL="http://localhost:8080"
```

## 验证清单

### ✅ 已完成的验证

- [x] x-prompt-hunter SKILL.md 已更新
- [x] prompt-to-skill-converter SKILL.md 已更新
- [x] prompts-workflow 已标记为废弃
- [x] 整合文档已创建
- [x] 技能唯一性已验证
- [x] 推荐工作流已定义

### ⏳ 待完成的任务

- [ ] 清理重复脚本（建议使用 `scripts/` 子目录归档）
- [ ] 测试完整工作流（收集 → 转换 → 发布）
- [ ] 配置 cron 自动执行
- [ ] 创建监控脚本（检查执行状态）
- [ ] 更新用户文档（如果有外部文档）

## 关键决策

### 1. 不上传到 ClawdHub

**原因**：此技能为内部集成工具，不适合公开发布

**操作**：确保不使用 `clawdhub publish` 发布此技能

### 2. 保留 prompts-workflow

**原因**：
- 作为旧架构的参考
- 可能用于回滚或兼容性需求
- 已明确标记为废弃

**操作**：仅标记为废弃，不删除

### 3. 分离两阶段架构

**原因**：
- 职责清晰：数据发现 vs 转换发布
- 灵活性：可以独立使用任一阶段
- 可维护性：易于调试和优化

**操作**：明确两阶段的输入输出关系

## 后续计划

### 短期（本周）

1. **测试完整工作流**
   - 运行 x-prompt-hunter pipeline
   - 运行 prompt-to-skill-converter
   - 验证输出质量

2. **清理重复脚本**
   - 创建 `scripts/deprecated/` 子目录
   - 移动旧脚本到 deprecated
   - 更新相关文档

3. **配置 cron**
   - 添加每日自动执行
   - 配置日志记录
   - 配置错误通知

### 中期（本月）

1. **优化性能**
   - 优化去重算法
   - 调整评估阈值
   - 优化批量处理

2. **增强监控**
   - 创建状态监控脚本
   - 配置告警规则
   - 生成质量报告

3. **文档完善**
   - 添加常见问题解答
   - 添加故障排查指南
   - 添加性能优化建议

### 长期（下季度）

1. **扩展功能**
   - 支持多语言提示词
   - 添加 A/B 测试
   - 支持自定义评估标准

2. **质量提升**
   - 收集用户反馈
   - 迭代优化算法
   - 提升自动化程度

## 联系方式

如有问题或建议，请联系 Jack。

---

**整合完成时间**：2026-02-02 09:30
**最后更新**：2026-02-02 09:30
**版本**：1.0.0
**状态**：✅ 完成（等待测试和清理）
