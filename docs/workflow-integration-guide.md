# 工作流整合方案

## 概述

将 **x-prompt-hunter**（数据发现层）和 **prompt-to-skill-converter**（转换发布层）整合为一个统一的自动化工作流。

## 整合前 vs 整合后

### 整合前（两个独立工作流）

**Stage 1: 数据发现**
```bash
cd /root/clawd/skills/x-prompt-hunter
python3 main.py pipeline --query "AI prompts" --limit 100 --evaluate-limit 30
```

**Stage 2: 转换发布**
```bash
cd /root/clawd/skills/prompt-to-skill-converter
python3 scripts/convert-prompts-to-skills.py --quality-threshold 80
clawdhub publish <skill-name>.skill --registry https://www.clawhub.ai/api
```

**问题**：
- ❌ 需要手动切换目录和执行两个命令
- ❌ 缺乏统一的通知机制
- ❌ 没有整合的报告
- ❌ 无法一键完成整个流程
- ❌ 参数分散，难以管理

### 整合后（统一工作流）

```bash
# 一键执行
bash /root/clawd/scripts/integrated-prompt-workflow.sh

# 自定义参数
bash /root/clawd/scripts/integrated-prompt-workflow.sh \
  --query "creative writing" \
  --limit 50 \
  --evaluate-limit 20 \
  --quality-threshold 80

# 测试模式（不发布）
bash /root/clawd/scripts/integrated-prompt-workflow.sh \
  --test-mode
```

**优势**：
- ✅ 一键执行整个流程
- ✅ 统一的日志和报告
- ✅ 自动通知（Slack + Feishu）
- ✅ Git 自动提交
- ✅ 灵活的参数配置
- ✅ 测试模式支持

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│           Integrated Prompt Workflow                        │
│           /root/clawd/scripts/integrated-prompt-workflow.sh │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 1: 数据发现（x-prompt-hunter）                         │
│ ─────────────────────────────────────────────────────────── │
│  1.1 抓取（GitHub + HuggingFace）                           │
│      ↓                                                        │
│  1.2 语义去重（sentence-transformers）                       │
│      ↓                                                        │
│  1.3 LLM 评估（Claude API）                                  │
│         • 创新性（1-10）                                      │
│         • 实用性（1-10）                                      │
│         • 清晰度（1-10）                                      │
│         • 可复用性（1-10）                                    │
│      ↓                                                        │
│  1.4 Langfuse 追踪                                          │
│                                                              │
│  输出: data/evaluation_results.json                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 2: 转换发布（prompt-to-skill-converter）               │
│ ─────────────────────────────────────────────────────────── │
│  2.1 转换为 Skills（质量过滤）                               │
│      • 只转换评分 ≥ THRESHOLD 的提示词                       │
│      • 生成 SKILL.md                                         │
│      • 创建目录结构                                          │
│      ↓                                                        │
│  2.2 打包 Skills（skill-creator）                           │
│      • 验证结构                                              │
│      • 生成 .skill 文件                                      │
│      ↓                                                        │
│  2.3 发布到 ClawdHub                                        │
│      • --registry https://www.clawhub.ai/api                  │
│      • 记录发布状态                                          │
│                                                              │
│  输出: 发布的 Skills + 统计数据                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ Stage 3: 报告和通知                                         │
│ ─────────────────────────────────────────────────────────── │
│  3.1 生成整合报告（Markdown）                                │
│      • Stage 1 统计                                         │
│      • Stage 2 统计                                         │
│      • 质量指标                                              │
│      ↓                                                        │
│  3.2 Git 提交                                                │
│      • 添加相关文件                                         │
│      • 自动推送                                              │
│      ↓                                                        │
│  3.3 发送通知（Slack + Feishu）                              │
│      • 仅在有新数据时发送                                    │
│      • 包含关键统计                                          │
│                                                              │
│  输出: 报告文件 + Git commit + 通知                         │
└─────────────────────────────────────────────────────────────┘
```

## 数据流

```
数据源（GitHub, HuggingFace）
    ↓
原始提示词（prompts.json）
    ↓
去重后（prompts_deduplicated.json）
    ↓
评估结果（evaluation_results.json）←─── Stage 1 输出
    ↓
高质量提示词（过滤后）
    ↓
SKILL.md 文件（批量生成）
    ↓
.skill 包（批量打包）
    ↓
发布到 ClawdHub
    ↓
报告 + 通知
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--query` | "AI prompts" | 搜索查询 |
| `--limit` | 50 | 每个数据源的抓取限制 |
| `--evaluate-limit` | 30 | 评估限制（节省 API 调用） |
| `--quality-threshold` | 70 | 质量阈值（0-100） |
| `--test-mode` | false | 测试模式，不发布 |

## 使用示例

### 基本使用

```bash
# 使用默认参数
bash /root/clawd/scripts/integrated-prompt-workflow.sh
```

### 自定义查询

```bash
# 搜索创意写作提示词
bash /root/clawd/scripts/integrated-prompt-workflow.sh \
  --query "creative writing prompts" \
  --quality-threshold 80
```

### 快速测试

```bash
# 少量数据，测试模式
bash /root/clawd/scripts/integrated-prompt-workflow.sh \
  --limit 10 \
  --evaluate-limit 5 \
  --quality-threshold 60 \
  --test-mode
```

### 定时任务（Cron）

```bash
# 每天早上 9 点运行
0 9 * * * cd /root/clawd && bash scripts/integrated-prompt-workflow.sh >> logs/cron-integrated.log 2>&1

# 每周一早上 8 点运行，提高质量阈值
0 8 * * 1 cd /root/clawd && bash scripts/integrated-prompt-workflow.sh --quality-threshold 80 >> logs/cron-integrated.log 2>&1
```

## 输出文件

```
/root/clawd/
├── logs/
│   └── integrated-prompt-workflow.log           # 完整日志
├── reports/
│   └── integrated-workflow-report-YYYYMMDD-HHMM.md  # 整合报告
├── skills/
│   └── <new-skills>/                              # 新生成的 Skills
│       └── SKILL.md
└── skills/x-prompt-hunter/
    └── data/
        ├── prompts.json                          # 原始提示词
        ├── prompts_deduplicated.json            # 去重后
        ├── evaluation_results.json              # 评估结果
        └── langfuse_reports/                    # Langfuse 报告
```

## 报告示例

```markdown
# 整合的 AI 提示词自动化流程报告

**生成时间**: 2026-02-02 10:30:00

## 📊 流程统计

| 阶段 | 工具 | 状态 | 详情 |
|------|------|------|------|
| Stage 1 | x-prompt-hunter | ✅ 完成 | 30 个提示词已评估 |
| Stage 2.1 | prompt-to-skill-converter | ✅ 完成 | 15 个 Skill 已转换 |
| Stage 2.2 | skill-creator | ✅ 完成 | 打包完成 |
| Stage 2.3 | ClawdHub | ✅ 完成 | 12 成功, 3 失败 |

## 🔍 数据详情

**Stage 1: 数据发现（x-prompt-hunter）**
- 查询: AI prompts
- 数据源: GitHub, HuggingFace
- 评估限制: 30 个
- 已评估: 30 个

**Stage 2: 转换和发布**
- 质量阈值: 70
- 已转换: 15 个 Skill
- 已发布: 12 个
```

## 通知示例

```
📊 **整合工作流完成！**

**Stage 1: 数据发现（x-prompt-hunter）**
• 查询: AI prompts
• 评估提示词: 30 个
• 特性: 语义去重 + LLM 评估 + Langfuse 追踪

**Stage 2: 转换发布（prompt-to-skill-converter）**
• 质量阈值: 70
• 转换 Skills: 15 个
• ClawdHub 发布: 12 成功

**报告**: /root/clawd/reports/integrated-workflow-report-20260202-103000.md
**详情**: 查看日志: /root/clawd/logs/integrated-prompt-workflow.log
```

## 优势总结

### 1. 简化操作
- **整合前**: 需要 2 个独立命令 + 手动切换目录
- **整合后**: 1 个命令完成所有操作

### 2. 统一管理
- **整合前**: 日志分散，没有统一报告
- **整合后**: 集中式日志 + 整合报告

### 3. 质量保证
- **整合前**: 可能跳过去重和评估步骤
- **整合后**: 强制执行语义去重 + LLM 评估

### 4. 自动化
- **整合前**: 手动 Git 提交 + 通知
- **整合后**: 自动 Git 提交 + 智能通知

### 5. 灵活性
- **整合前**: 参数分散，难以测试
- **整合后**: 统一参数 + 测试模式

## 对比表

| 特性 | 整合前 | 整合后 |
|------|--------|--------|
| 命令数量 | 2+ | 1 |
| 目录切换 | 手动 | 自动 |
| 语义去重 | 可选 | 强制 |
| LLM 评估 | 可选 | 强制 |
| 质量过滤 | 手动 | 自动 |
| 日志管理 | 分散 | 集中 |
| 报告生成 | 无 | 自动 |
| Git 提交 | 手动 | 自动 |
| 通知机制 | 无 | 自动 |
| 测试模式 | 无 | 有 |
| Cron 集成 | 复杂 | 简单 |

## 迁移指南

### 从旧工作流迁移

**如果你正在使用 `full-prompt-workflow.sh`**：

```bash
# 旧方式
bash /root/clawd/scripts/full-prompt-workflow.sh

# 新方式（推荐）
bash /root/clawd/scripts/integrated-prompt-workflow.sh
```

**主要区别**：
- 旧方式：使用多数据源收集（Reddit, GitHub, HN, SearXNG, Firecrawl）
- 新方式：专注于高质量数据源（GitHub, HuggingFace）+ 深度评估

**建议**：
- 如果数据质量最重要 → 使用新的整合工作流
- 如果数据覆盖面最重要 → 继续使用 `full-prompt-workflow.sh`
- 可以同时使用两个工作流，覆盖不同需求

### 逐步迁移

1. **测试阶段**（1 周）
   ```bash
   # 在测试模式运行新工作流
   bash /root/clawd/scripts/integrated-prompt-workflow.sh --test-mode
   ```

2. **对比阶段**（1 周）
   ```bash
   # 同时运行两个工作流，对比结果
   bash /root/clawd/scripts/full-prompt-workflow.sh
   bash /root/clawd/scripts/integrated-prompt-workflow.sh --test-mode
   ```

3. **切换阶段**
   ```bash
   # 切换 Cron 任务
   0 9 * * * cd /root/clawd && bash scripts/integrated-prompt-workflow.sh >> logs/cron-integrated.log 2>&1
   ```

## 故障排查

### 问题：Stage 1 失败

**原因**: x-prompt-hunter 配置问题

**解决**:
```bash
# 检查配置
cd /root/clawd/skills/x-prompt-hunter
cat config.yaml

# 测试单独运行
python3 main.py pipeline --query "test" --limit 5 --evaluate-limit 3
```

### 问题：Stage 2 没有转换任何 Skill

**原因**: 质量阈值过高

**解决**:
```bash
# 降低质量阈值
bash /root/clawd/scripts/integrated-prompt-workflow.sh --quality-threshold 50
```

### 问题：没有发送通知

**原因**: 没有新数据或通知配置错误

**解决**:
```bash
# 检查日志
tail -100 /root/clawd/logs/integrated-prompt-workflow.log

# 测试通知
clawdbot message send --channel slack --target "<YOUR_DM_ID>" --message "测试"
```

## 下一步优化

### 短期（1-2 周）
- [ ] 添加更多数据源（Reddit, Twitter/X）
- [ ] 支持自定义评估维度
- [ ] 添加重试机制

### 中期（1-2 月）
- [ ] 集成 Langfuse 可视化报告
- [ ] 添加 A/B 测试功能
- [ ] 支持多语言提示词

### 长期（3-6 月）
- [ ] 自动调参系统
- [ ] 集成用户反馈循环
- [ ] 智能推荐系统

## 总结

整合后的工作流提供了：
1. ✅ **一体化体验** - 一个命令完成所有操作
2. ✅ **质量保证** - 强制执行去重和评估
3. ✅ **自动化** - 自动报告、提交、通知
4. ✅ **灵活性** - 可配置参数 + 测试模式
5. ✅ **可维护性** - 清晰的架构和日志

**推荐**: 使用整合工作流替代原有的两个独立工作流。
