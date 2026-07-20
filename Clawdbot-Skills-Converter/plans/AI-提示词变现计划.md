# AI 提示词变现计划

## 🎯 目标

自动化流程：
1. 每 6 小时从 X 搜索高质量 AI 提示词
2. 评估提示词质量（使用 prompt-optimizer）
3. 转换为 Clawdbot Skills（使用 skill-creator）
4. 发布到 ClawdHub 进行售卖

## 📊 系统架构

```
X 搜索 → 质量评估 → 转换为 Skill → 发布到 ClawdHub → 监控销售
   ↓          ↓            ↓              ↓              ↓
twitter-search  prompt-optimizer  skill-creator  clawdhub  销售追踪
```

## 🔄 自动化流程

### 第一步：X 搜索（每 6 小时）

**搜索策略：**
- 关键词组合：
  - "ChatGPT prompt" OR "GPT prompt" OR "AI prompt"
  - "Claude prompt" OR "Claude AI prompt"
  - "best prompt" OR "effective prompt"
  - "prompt engineering" OR "prompt template"
  - "prompt for" + 常见任务（写作、编程、分析等）

**过滤条件：**
- 最小互动：min_retweets:20 或 min_faves:100
- 语言：lang:en（主要市场）和 lang:zh
- 时间范围：最近 24 小时
- 排除：转推，只看原创内容

**输出数据：**
- 提示词内容
- 作者信息
- 互动数据（点赞、转发、回复数）
- 原始链接

### 第二步：质量评估

**评估维度（使用 prompt-optimizer）：**
1. **清晰度** - 是否明确易懂
2. **具体性** - 是否有明确的约束和输出要求
3. **结构化** - 是否有清晰的步骤或格式
4. **完整性** - 是否包含必要的上下文
5. **实用性** - 是否有实际应用场景

**质量评分机制：**
- 评分 > 7/10：高质量，优先转换
- 评分 5-7/10：中等质量，手动审核
- 评分 < 5/10：低质量，直接丢弃

**重复检测：**
- 基于内容相似度检测重复提示词
- 维护已处理提示词数据库
- 避免重复发布相似技能

### 第三步：转换为 Skill

**Skill 创建流程：**
1. 提示词优化（使用 prompt-optimizer）
2. 确定技能类型和用途
3. 生成 SKILL.md（包含优化的提示词）
4. 添加示例和使用说明
5. 打包为 .skill 文件

**Skill 命名规范：**
- 格式：`{用途}-{关键词}.skill`
- 示例：`email-writer-persuasive.skill`, `code-review-ai.skill`
- 小写字母，使用连字符

**Skill 内容结构：**
```markdown
---
name: skill-name
description: 简洁描述技能用途和触发场景
---

# 技能名称

## 快速开始

### 使用场景
- 场景 1
- 场景 2

## 提示词优化

### 原始提示词
[来自 X 的原始提示词]

### 优化后的提示词
[使用 prompt-optimizer 优化后的版本]

### 优化说明
[说明应用了哪些技术]
```

### 第四步：发布到 ClawdHub

**发布前检查：**
1. 验证 Skill 格式（使用 package_skill.py）
2. 生成版本号（基于日期：v1.0.20260128）
3. 编写更新日志

**定价策略：**
- 高质量技能（评分 > 8）：$5-10
- 中等质量技能（评分 7-8）：$3-5
- 基础技能：$1-3

**发布命令：**
```bash
clawdhub publish ./skill-name \
  --slug skill-name \
  --name "Skill Display Name" \
  --version 1.0.20260128 \
  --changelog "Initial release based on popular X prompt"
```

## 📁 项目结构

```
/root/clawd/
├── plans/
│   └── AI-提示词变现计划.md          # 本计划文档
├── automation/
│   ├── x-prompts-harvester/         # 主自动化脚本
│   │   ├── harvest.py              # 主协调脚本
│   │   ├── search_x.py             # X 搜索模块
│   │   ├── evaluate.py             # 质量评估模块
│   │   ├── convert_to_skill.py      # 转换模块
│   │   └── publish.py              # 发布模块
│   ├── state/                      # 状态跟踪
│   │   ├── processed_prompts.json   # 已处理提示词数据库
│   │   ├── published_skills.json    # 已发布技能列表
│   │   └── metrics.json            # 性能指标
│   ├── skills-generated/           # 生成的技能临时存储
│   └── logs/                       # 运行日志
└── memory/
    └── x-harvesting-YYYY-MM-DD.md   # 每日操作记录
```

## ⏰ 定时任务配置

### Cron 任务（每 6 小时）

```bash
# 每 6 小时运行一次（0:00, 6:00, 12:00, 18:00 UTC）
0 */6 * * * cd /root/clawd/automation/x-prompts-harvester && /usr/bin/python3 harvest.py >> logs/$(date +\%Y\%m\%d).log 2>&1
```

### 心跳检查（每 30 分钟）

在 HEARTBEAT.md 中添加：
```markdown
## AI 提示词变现项目

- [ ] 检查最后运行时间（state/last_run.txt）
- [ ] 查看最近的日志文件
- [ ] 检查错误和失败
- [ ] 查看新技能发布数量
- [ ] 查看销售数据（如果可用）
```

## 📈 监控指标

### 追踪数据：
- **输入指标**：
  - 每次搜索获取的提示词数量
  - 通过质量筛选的提示词数量
  - 实际转换为技能的数量

- **输出指标**：
  - 发布的技能数量
  - 技能安装/下载数
  - 收入/销售额
  - 用户评价和反馈

- **质量指标**：
  - 平均提示词质量评分
  - 高质量提示词转化率
  - 重复提示词检测率

### 报告生成：
每周生成一次总结报告，包括：
- 本周新发现提示词统计
- 发布技能列表
- 销售数据
- 质量趋势分析

## 🚀 实施阶段

### 阶段 1：基础设施搭建（现在）
- [x] 创建计划文档
- [ ] 创建项目目录结构
- [ ] 编写主协调脚本 `harvest.py`
- [ ] 实现 X 搜索模块 `search_x.py`
- [ ] 实现质量评估模块 `evaluate.py`
- [ ] 实现转换模块 `convert_to_skill.py`
- [ ] 实现发布模块 `publish.py`
- [ ] 配置 cron 定时任务

### 阶段 2：测试与优化（1-2 周）
- [ ] 手动运行完整流程
- [ ] 调整搜索关键词和过滤条件
- [ ] 优化质量评估标准
- [ ] 测试技能生成质量
- [ ] 监控和修复 bug
- [ ] 优化错误处理

### 阶段 3：自动化运行（持续）
- [ ] 启动 cron 定时任务
- [ ] 设置监控和报警
- [ ] 定期检查日志和指标
- [ ] 收集用户反馈
- [ ] 持续优化提示词质量

### 阶段 4：扩展与改进（长期）
- [ ] 添加更多社交媒体源（Reddit, LinkedIn）
- [ ] 实现智能定价策略
- [ ] 开发用户推荐系统
- [ ] 创建技能分类和标签系统
- [ ] 建立 A/B 测试框架

## 🔧 技术依赖

**已安装：**
- Clawdbot (v22.22.0)
- Python 3

**需要安装：**
- Twitter API key（从 https://twitterapi.io 获取）
- ClawdHub CLI：`npm i -g clawdhub`

**Python 依赖：**
```bash
pip3 install requests python-dotenv
```

## ⚠️ 注意事项

1. **API 限制**：
   - Twitter API 有速率限制，需要合理控制请求频率
   - 考虑使用缓存避免重复请求

2. **质量控制**：
   - 不自动发布，需要人工审核高质量技能
   - 建立质量评分阈值，低于阈值不发布

3. **版权问题**：
   - 提示词本身通常不受版权保护，但需要谨慎
   - 如果提示词包含特定内容，需要进行改编和优化
   - 明确技能来源基于社区提示词

4. **避免垃圾内容**：
   - 控制发布频率，避免 flooding
   - 确保每个技能都有独特价值
   - 建立分类和标签系统

## 📝 待办事项

**立即执行：**
1. 获取 Twitter API key
2. 创建项目目录结构
3. 编写第一个版本的自动化脚本

**本周完成：**
1. 完成所有模块的开发
2. 配置 cron 任务
3. 运行第一次完整测试

**下周开始：**
1. 启动自动化运行
2. 监控和优化
3. 分析第一批数据

## 🎯 成功指标

**短期目标（1 个月）：**
- 发布 20+ 高质量技能
- 实现自动发现和处理提示词
- 建立稳定的自动化流程

**中期目标（3 个月）：**
- 发布 100+ 技能
- 实现稳定收入
- 优化提示词质量评估准确性 > 80%

**长期目标（6 个月）：**
- 发布 300+ 技能
- 建立品牌和用户群
- 实现月收入 > $1000

---

*创建时间：2026-01-28*
*最后更新：2026-01-28*
