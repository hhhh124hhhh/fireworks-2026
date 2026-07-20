# 📘 演示案例使用指南

本指南说明如何使用 Ultimate Skills Bundle 的实战案例。

---

## 📁 案例文件结构

```
demo-project/
├── README.md                    # 案例概述
├── CASE_STUDY.md                # 完整实战案例（核心）
├── SKILLS_COMPARISON.md         # 技能效果对比
├── code-examples/               # 代码示例
│   ├── TodoItem.tsx            # 实际组件代码
│   └── TodoItem.test.tsx       # TDD 测试代码
└── screenshots/                  # 截图占位符
    ├── light.png
    ├── dark.png
    └── mobile.png
```

---

## 🚀 快速开始

### 1. 阅读完整案例

```bash
# 在你的编辑器中打开
cd /root/clawd/demo-project

# 阅读核心案例文档
cat CASE_STUDY.md
```

### 2. 了解技能对比

```bash
# 查看技能效果对比
cat SKILLS_COMPARISON.md
```

### 3. 查看代码示例

```bash
# 查看使用 TDD 开发的组件
cat code-examples/TodoItem.tsx

# 查看测试代码
cat code-examples/TodoItem.test.tsx
```

---

## 📖 案例内容详解

### CASE_STUDY.md - 完整实战案例

这是核心文档，包含：

#### 📋 6 个开发阶段

1. **阶段 1: 需求讨论与规划**
   - 使用 `brainstorming` 技能
   - 使用 `writing-plans` 技能

2. **阶段 2: 项目初始化**
   - 使用 `using-git-worktrees` 技能

3. **阶段 3: TDD 开发**
   - 使用 `test-driven-development` 技能
   - 展示 RED-GREEN-REFACTOR 流程

4. **阶段 4: 多代理并行开发**
   - 使用 `subagent-driven-development` 技能

5. **阶段 5: 代码审查**
   - 使用 `requesting-code-review` 技能

6. **阶段 6: 文档与图表**
   - 使用 `crafting-effective-readmes` 技能
   - 使用 `mermaid-diagrams` 技能

#### 🎯 每个阶段包含

- 使用的技能名称
- 触发命令示例
- Claude 的实际输出
- 生成的代码/文档
- 预期结果

---

### SKILLS_COMPARISON.md - 技能效果对比

这个文档对比使用技能前后的差异：

#### ⏱️ 时间效率对比

| 任务 | 传统方式 | 使用技能 | 节省时间 |
|------|---------|---------|---------|
| 需求讨论 | 2 小时 | 30 分钟 | 75% |
| 制定计划 | 1.5 小时 | 20 分钟 | 78% |
| ... | ... | ... | ... |

#### 🎯 质量对比

| 指标 | 传统方式 | 使用技能 | 改进 |
|------|---------|---------|------|
| 测试覆盖率 | 60% | 100% | +67% |
| Bug 数量 | 8 个 | 1 个 | -87.5% |
| ... | ... | ... | ... |

#### 🚀 具体技能效果展示

每个技能都有：
- ❌ 传统方式的实现（缺点）
- ✅ 使用技能后的实现（优点）
- 💡 优势总结

---

### code-examples/ - 代码示例目录

包含实际使用技能开发的代码：

#### TodoItem.tsx

使用 `test-driven-development` + `frontend-design` 技能开发的 React 组件。

**特点:**
- ✅ TypeScript 类型安全
- ✅ 完整的 Props 接口
- ✅ 响应式设计
- ✅ 深色模式支持
- ✅ 可访问性（ARIA）
- ✅ 优雅的动画效果

#### TodoItem.test.tsx

展示 TDD 的 RED-GREEN-REFACTOR 完整流程：

1. **RED** - 编写失败测试
2. **GREEN** - 编写最小实现
3. **REFACTOR** - 优化代码

**包含 6 个测试用例:**
- 基础渲染测试
- 完成状态测试
- 交互测试
- 可访问性测试
- 删除动画测试
- 样式状态测试

---

## 💡 如何使用这个案例

### 对于开发者

1. **学习技能使用方法**
   - 阅读 `CASE_STUDY.md`
   - 了解每个技能的具体用法
   - 复制触发命令到 Claude Code

2. **理解 TDD 流程**
   - 查看 `code-examples/TodoItem.test.tsx`
   - 理解 RED-GREEN-REFACTOR 循环
   - 应用到自己的项目

3. **对比效果**
   - 阅读 `SKILLS_COMPARISON.md`
   - 看到使用技能的优势
   - 说服团队采用

### 对于团队管理者

1. **评估技能价值**
   - 查看时间和质量对比数据
   - 计算投资回报率（ROI）
   - 决定是否采用

2. **制定培训计划**
   - 根据案例制定培训流程
   - 安排团队成员学习
   - 组织技能分享会

3. **推广最佳实践**
   - 将案例分享给团队
   - 鼓励使用技能
   - 收集反馈改进

### 对于项目决策者

1. **评估技术选型**
   - 了解技能的实际效果
   - 评估投入产出比
   - 做出采购决策

2. **制定实施计划**
   - 根据案例制定试点计划
   - 选择合适的团队试用
   - 制定推广时间表

---

## 🎯 关键要点

### 1. 技能自动触发

所有技能会根据上下文自动触发，无需手动指定：

```
# 你只需要说
"Let's use TDD to build a user authentication system"

# Claude 会自动触发
- brainstorming（如果需要）
- writing-plans
- test-driven-development
- requesting-code-review
```

### 2. 渐进式学习

不要一次性使用所有技能，建议按顺序学习：

**阶段 1: 基础技能**
- test-driven-development
- writing-plans

**阶段 2: 进阶技能**
- brainstorming
- systematic-debugging

**阶段 3: 高级技能**
- subagent-driven-development
- requesting-code-review

**阶段 4: 专业技能**
- crafting-effective-readmes
- mermaid-diagrams

### 3. 定制化使用

根据项目需求选择合适的技能组合：

**小项目:**
- test-driven-development
- writing-plans

**中等项目:**
- brainstorming
- writing-plans
- test-driven-development
- requesting-code-review

**大型项目:**
- 全套工作流
- 使用 git-worktrees
- 多代理并行开发

---

## 📞 获取帮助

### 问题反馈

如果在学习过程中遇到问题：

1. **查看文档**
   - Ultimate Skills Bundle README
   - 各技能的 SKILL.md

2. **搜索解决方案**
   - GitHub Issues
   - Discussions

3. **提问交流**
   - 在仓库提 Issue
   - 在 Discussions 讨论

### 贡献改进

如果你有改进建议：

1. Fork 仓库
2. 创建改进分支
3. 提交 Pull Request

---

## 🚀 下一步

1. ✅ 阅读完整案例（CASE_STUDY.md）
2. ✅ 理解技能对比（SKILLS_COMPARISON.md）
3. ✅ 查看代码示例（code-examples/）
4. 🎯 在实际项目中尝试使用技能
5. 📊 记录效果并分享
6. 🔄 持续改进和优化

---

**开始时间:** 今天
**预计学习时间:** 2-3 小时
**实际应用时间:** 立即开始

**祝你学习愉快！** 🎉
