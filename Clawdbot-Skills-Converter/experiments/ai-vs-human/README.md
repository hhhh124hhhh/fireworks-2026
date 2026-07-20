# Claude Code vs 24-Hour AI: Intensity Experiment 🧪

> 测试 Claude Code（使用 70+ 技能）与 24 小时 AI 在完整软件开发任务中的综合能力

---

## 🎯 实验目标

### 核心问题
**在相同的软件开发任务中，谁更强？**
- 🧪 Claude Code 使用 70+ 专业技能
- 🤖 24-Hour AI 使用一次性提示

### 测试维度
1. **代码质量** (25%) - TypeScript 类型安全、ESLint 检查、代码结构
2. **功能完整度** (20%) - 需求覆盖率、边缘情况处理
3. **测试覆盖率** (15%) - 单元测试、集成测试、覆盖率
4. **Bug 数量** (15%) - 已发现 bug 数（越少越好）
5. **完成时间** (15%) - 总用时（越短越好）
6. **用户体验** (10%) - UI/UX 评分、响应式设计、可访问性

**总分**: 100 分

---

## 📋 测试任务

### 项目：Ultimate Todo App

**完整的功能需求**（10 个）：
1. ✅ 添加新任务
2. ✅ 标记完成/未完成
3. ✅ 删除任务
4. ✅ 任务统计（已完成/总数/进度条）
5. ✅ 本地存储持久化（localStorage）
6. ✅ 响应式设计（移动端 + 桌面端）
7. ✅ 深色模式支持
8. ✅ 优雅的动画效果
9. ✅ 空状态提示
10. ✅ 可访问性（WCAG AA）

**技术栈**：
- **前端**: React 18.3.1 + TypeScript 5.6.3
- **构建工具**: Vite 6.0.5
- **样式**: Tailwind CSS 3.4.17 + shadcn/ui
- **测试**: Vitest 2.1.8 + React Testing Library 16.0.1
- **代码质量**: ESLint 9.14.0 + Prettier 3.3.3
- **状态管理**: React hooks (useState, useEffect, useContext, useReducer, useCallback, useMemo, useRef)
- **图标**: Lucide React 0.445.0

---

## 🔬 实验设计

### Claude Code 方案（使用技能）

#### 工作流
```
阶段 1: 需求讨论 (30 分钟)
├── brainstorming - 需求讨论和设计验证
└── writing-plans - 制定详细实施计划

阶段 2: 项目初始化 (10 分钟)
├── using-git-worktrees - 创建独立开发分支
└── design-system-starter - 设计系统初始化

阶段 3: 功能开发 (TDD) (90 分钟)
├── test-driven-development - RED-GREEN-REFACTOR 循环
│   ├── TodoItem 组件
│   ├── TodoList 组件
│   └── AddTodo 组件
└── subagent-driven-development - 多代理并行开发

阶段 4: 代码审查 (20 分钟)
├── requesting-code-review - 准备代码审查
└── receiving-code-review - 处理审查反馈

阶段 5: 文档生成 (15 分钟)
├── crafting-effective-readmes - 编写 README
└── mermaid-diagrams - 生成架构图
```

**预期结果**: 2.5 小时，100% 测试覆盖率，1 个 bug，代码质量 9/10

---

### 24-Hour AI 方案

#### 一次性提示
```
Create a complete todo app with React 18, TypeScript 5.6.3, Vite 6.0.5, Tailwind CSS 3.4.17, shadcn/ui, Vitest 2.1.8, React Testing Library 16.0.1, ESLint 9.14.0, Prettier 3.3.3, Lucide React 0.445.0.

Including ALL of these features:
- Add/delete/complete tasks
- Task statistics (completed/total/progress bar)
- Local storage persistence (localStorage)
- Responsive design (mobile + desktop)
- Dark mode support
- Smooth animations
- Empty state prompts
- Accessibility (WCAG AA)
- TypeScript type safety
- ESLint + Prettier code quality
- 100% test coverage with Vitest + React Testing Library

All components must follow best practices, be fully typed, include error handling, and be production-ready.
```

**预期结果**: 4 小时，60% 测试覆盖率，8 个 bug，代码质量 6/10

---

## 📊 预期结果对比

### 详细评分

| 维度 | 权重 | Claude Code | 24-Hour AI | 差距 |
|------|------|-------------|-------------|------|
| **代码质量** | 25% | 90/100 | 60/100 | +30 |
| **功能完整度** | 20% | 100/100 | 40/100 | +60 |
| **测试覆盖率** | 15% | 100/100 | 60/100 | +40 |
| **Bug 数量** | 15% | 95/100 | 50/100 | +45 |
| **完成时间** | 15% | 90/100 | 60/100 | +30 |
| **用户体验** | 10% | 90/100 | 65/100 | +25 |
| **总分** | 100% | **93/100** | **56/100** | **+37** |

### 时间对比

| 方案 | 预期时间 | 每分钟得分 |
|------|---------|-------------|
| Claude Code | 150 分钟 | 0.60 |
| 24-Hour AI | 240 分钟 | 0.38 |

**时间效率**: Claude Code 节省 37.5% (90 分钟)

---

## 🚀 快速开始

### 方式 1: 手动运行（推荐）

```bash
# 进入实验目录
cd /root/clawd/experiments/ai-vs-human

# 运行完整实验
bash ./run-experiment.sh

# 查看结果
cat report/comparison-report.md
```

### 方式 2: 查看详细计划

```bash
# 查看实验计划
cat EXPERIMENT_PLAN.md

# 查看 Claude Code 技能使用
cat claude-code-result/phase-*.md
```

### 方式 3: 运行单独脚本

```bash
# 只运行 Claude Code
bash ./run-claude.sh

# 只运行 24-Hour AI
bash ./run-24hour-ai.sh

# 只生成评估报告
bash ./evaluate-and-report.sh
```

---

## 📂 项目结构

```
ai-vs-human/
├── EXPERIMENT_PLAN.md      # 实验计划和评估标准
├── claude-code-result/      # Claude Code 完整工作流结果
│   ├── phase-1-brainstorming.md
│   ├── phase-2-writing-plans.md
│   ├── phase-3-git-worktrees.md
│   ├── phase-4-tdd.md
│   ├── phase-5-code-review.md
│   └── phase-6-documentation.md
├── 24hour-ai-result/        # 24-Hour AI 结果
│   └── result-summary.md
├── report/                  # 评估和报告
│   ├── comparison-report.md     # 详细对比报告
│   ├── generate-charts.js       # 图表数据脚本
│   └── evaluation.log          # 评估日志
├── results/                 # 实验结果
│   ├── claude-run.log         # Claude Code 运行日志
│   ├── 24hour-ai-run.log      # 24-Hour AI 运行日志
│   └── evaluation.log        # 评估日志
├── run-claude.sh            # 运行 Claude Code
├── run-24hour-ai.sh        # 运行 24-Hour AI
├── evaluate-and-report.sh   # 评估和报告生成
└── run-experiment.sh        # 主实验脚本
```

---

## 🎯 关键指标

### 成功标准

- ✅ **代码质量 > 85%**
- ✅ **功能完整度 > 90%**
- ✅ **测试覆盖率 > 90%**
- ✅ **Bug 数量 < 5**
- ✅ **完成时间 < 3 小时**
- ✅ **用户体验 > 80%**

### Claude Code 优势

如果 Claude Code 获胜，说明：
- 系统化的开发流程更有效
- 技能组合提升了效率
- TDD 流程保证代码质量
- 代码审查减少 bug 数量

### 24-Hour AI 优势

如果 24-Hour AI 获胜，说明：
- 一次性大 prompt 可能更适合某些场景
- AI 具备了更强的模式识别能力
- 不需要技能组合就能完成任务

---

## 🔬 评估方法

### 自动化评估

```bash
# 运行评估脚本
cd /root/clawd/experiments/ai-vs-human
bash ./evaluate-and-report.sh
```

**评估内容**:
- 自动化 ESLint 检查
- 自动化测试覆盖率统计
- 自动化性能指标收集
- 生成对比报告和图表

### 手动审查

1. **代码质量审查**
   - 代码结构清晰度
   - 命名规范
   - 错误处理完善度
   - 组件设计模式

2. **功能完整性审查**
   - 需求覆盖率
   - 边缘情况处理
   - 用户流程完整性

3. **用户体验审查**
   - 响应式设计质量
   - 动画流畅度
   - 交互反馈清晰度
   - 可访问性标准

---

## 📈 预期影响

### 如果 Claude Code 获胜

1. **验证技能价值**
   - 证明系统化工作流的有效性
   - 展示技能组合的威力
   - 推动 Claude Code 和 Skills Bundle 的采用

2. **指导 AI 使用**
   - 展示如何有效使用 AI 辅助开发
   - 确定最佳的 AI 编程实践
   - 促进 AI 和人类的协作模式

3. **推动技能发展**
   - 识别最有效的技能
   - 发现技能组合的最佳实践
   - 指导新技能的开发方向

### 如果 24-Hour AI 获胜

1. **发现 AI 优势**
   - 识别 AI 擅长的场景
   - 了解何时使用一次性 prompt 更有效
   - 探索 AI 与技能的结合点

2. **改进技能设计**
   - 基于发现调整技能策略
   - 优化技能组合和触发条件
   - 开发新的技能类别

---

## 🎓 实验意义

这个实验不仅仅是一次比赛，而是：

1. **验证假设**: 测试"系统化技能 vs 一次性 AI"哪个更有效
2. **收集数据**: 获得量化的性能和代码质量数据
3. **发现最佳实践**: 找出最有效的开发方式
4. **指导未来**: 为 AI 辅助开发的未来方向提供数据支持

---

## 🔗 相关资源

- **Ultimate Skills Bundle**: https://github.com/hhhh124hhhh/ultimate-skills-bundle
- **技能使用指南**: [技能文档](https://github.com/hhhh124hhhh/ultimate-skills-bundle/tree/main/skills-bundle)
- **Claude Code 文档**: https://claude.ai/code

---

## 📞 支持和反馈

如有问题或建议：

1. **查看实验计划**: `EXPERIMENT_PLAN.md`
2. **检查运行日志**: `results/*.log`
3. **查看对比报告**: `report/comparison-report.md`

---

**实验开始时间**: 2026-01-28
**实验设计者**: jack happy + Clawdbot
**参与 AI**: Claude Code vs 24-Hour AI
**评估标准**: 6 个维度，总分 100 分

---

*Let the experiment begin!* 🧪
