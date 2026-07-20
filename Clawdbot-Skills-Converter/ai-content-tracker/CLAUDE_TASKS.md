# Claude Code 任务规划 - AI 媒体清单和抓取

## 阶段 1: brainstorming - 媒体来源讨论

**提示词：**
```
Claude，我需要创建一个 AI 媒体抓取系统。请使用 brainstorming 技能帮我讨论需求。

项目目标:
- 创建 AI 媒体清单（YouTube、博客、工具网站等）
- 根据清单逐一抓取内容
- 汇总为文档并上传到 GitHub

需要:
1. 媒体类型和来源清单
2. 每个来源的抓取方法
3. 数据结构设计
4. 实施计划

请帮我:
- 澄清媒体类型
- 设计清单结构
- 规划抓取方法
- 制定实施计划
```

## 阶段 2: writing-plans - 详细实施计划

**提示词：**
```
使用 writing-plans 技能为 AI 媒体清单和抓取系统创建详细的实施计划。

基于需求讨论，创建:
- 媒体清单结构和格式
- 抓取方法（YouTube、博客、工具网站）
- 数据存储方案
- 文档生成逻辑
- GitHub 同步方案

每个任务包括:
- 文件路径
- 实施步骤
- 验证方法
```

## 阶段 3: subagent-driven-development - 并行开发

**提示词：**
```
使用 subagent-driven-development 技能并行开发核心功能。

任务分配:
- Agent 1: 创建媒体清单（media-list.json）
- Agent 2: YouTube 抓取脚本
- Agent 3: 博客文章抓取脚本
- Agent 4: 工具网站信息抓取
- Agent 5: 文档汇总生成器

每个 Agent 需要:
- 完整的功能实现
- 数据结构定义
- 错误处理
- 测试验证
```

## 阶段 4: test-driven-development - TDD 开发

**提示词：**
```
使用 test-driven-development 技能开发抓取脚本。

为每个功能:
1. 先写测试（RED）
2. 实现最小功能（GREEN）
3. 重构优化（REFACTOR）

重点测试:
- JSON 数据格式验证
- 抓取成功/失败处理
- 数据完整性检查
```

## 阶段 5: requesting-code-review - 代码审查准备

**提示词：**
```
使用 requesting-code-review 技能准备代码审查。

生成:
- 完整的 PR 描述
- 功能清单
- 测试结果
- 已知问题
- 部署说明
```

## 阶段 6: crafting-effective-readmes - 文档编写

**提示词：**
```
使用 crafting-effective-readmes 技能编写项目文档。

生成:
- README.md - 使用指南
- TECHNICAL.md - 技术文档
- MEDIA_LIST.md - 媒体清单说明
```

---

## 执行记录

### 阶段 1 完成
- brainstorming 输出：[记录]
- 媒体类型确认：[记录]

### 阶段 2 完成
- writing-plans 输出：[记录]
- 任务分解：[记录]

### 阶段 3 完成
- subagent-driven-development 输出：[记录]
- 功能实现：[记录]

...

---

**当前阶段**: 准备开始
**开始时间**: 2026-01-27 23:20
**使用的技能包**: Ultimate Skills Bundle v1.0.0
