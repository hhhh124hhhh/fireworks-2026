# Claude Code 交互式演示项目 - 开发提示

## 阶段 1: 需求讨论（使用 brainstorming 技能）

**提示词:**
```
Claude, 请使用 brainstorming 技能帮我规划一个交互式演示网页。

项目目标:
- 展示 Ultimate Skills Bundle 的 70+ 技能
- 交互式浏览技能
- 展示技能效果对比
- 包含实际的代码示例
- 现代化 UI 设计

请帮我:
1. 澄清需求
2. 设计页面结构
3. 规划功能模块
4. 选择技术栈
5. 制定实施计划
```

## 阶段 2: 制定计划（使用 writing-plans 技能）

**提示词:**
```
使用 writing-plans 技能，为交互式演示网页创建详细的实施计划。

基于之前的需求讨论，创建:
- 详细的任务分解
- 每个任务的时间估算
- 技术实施细节
- 测试计划
- 部署方案
```

## 阶段 3: 项目初始化（使用 using-git-worktrees 技能）

**提示词:**
```
使用 using-git-worktrees 技能创建独立的开发环境。

创建一个新的 Git worktree 用于这个项目:
- 项目名: interactive-demo
- 基于 ultimate-skills-bundle 主分支
- 创建新分支: feature/interactive-demo
```

## 阶段 4: 核心开发（使用 subagent-driven-development 技能）

**提示词:**
```
使用 subagent-driven-development 技能并行开发核心功能。

任务分配:
- Agent 1: 主页面布局和导航
- Agent 2: 技能展示组件
- Agent 3: 交互式代码编辑器
- Agent 4: 效果对比图表
- Agent 5: 响应式设计

每个 Agent 需要:
- 完整的组件实现
- 单元测试
- TypeScript 类型定义
- 样式（Tailwind CSS）
```

## 阶段 5: 代码审查（使用 requesting-code-review 技能）

**提示词:**
```
使用 requesting-code-review 技能准备代码审查。

请生成:
- 完整的 PR 描述
- 功能清单
- 测试结果
- 已知问题
- 部署说明
```

## 阶段 6: 文档生成（使用 crafting-effective-readmes 技能）

**提示词:**
```
使用 crafting-effective-readmes 技能编写项目文档。

生成:
- 完整的 README.md
- 技术文档
- 用户指南
- 开发者文档
- 部署指南
```

## 阶段 7: 图表生成（使用 mermaid-diagrams 技能）

**提示词:**
```
使用 mermaid-diagrams 技能生成架构图。

创建:
- 系统架构图
- 组件层次图
- 数据流图
- 部署架构图
```

---

## 执行顺序

1. 阶段 1: brainstorming
2. 阶段 2: writing-plans
3. 阶段 3: using-git-worktrees
4. 阶段 4: subagent-driven-development
5. 阶段 5: requesting-code-review
6. 阶段 6: crafting-effective-readmes
7. 阶段 7: mermaid-diagrams
8. 部署到 Vercel

每个阶段完成后，记录输出和结果。
