# Ultimate Skills Bundle - 交互式演示项目

## 项目目标

创建一个现代化的交互式网页，展示 Ultimate Skills Bundle 的 70+ 技能，让用户能够：

1. **交互式浏览技能**
   - 按类别筛选
   - 搜索技能
   - 查看技能详情

2. **查看技能效果对比**
   - 传统方式 vs 使用技能
   - 可视化数据图表
   - 量化指标展示

3. **实际代码示例**
   - 在线代码编辑器
   - 实时预览
   - 一键复制

4. **实战案例展示**
   - 完整的开发流程
   - 每个阶段的输出
   - 使用技能的命令

## 技术需求

### 前端技术栈
- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **UI 组件**: shadcn/ui
- **图表**: Recharts
- **代码高亮**: Prism.js
- **动画**: Framer Motion

### 功能需求

#### 1. 首页
- Hero 区域：项目介绍
- 技能统计：70+ 技能概览
- 快速导航：跳转到各个模块

#### 2. 技能浏览页面
- 侧边栏：技能分类
  - Superpowers (14)
  - Anthropic Skills (16)
  - Agent Toolkit (40+)
- 主内容区：技能卡片
  - 技能名称
  - 技能描述
  - 使用场景
  - 相关技能
- 搜索功能：实时搜索

#### 3. 技能详情页
- 完整的技能说明
- 使用示例
- 命令示例
- 代码示例（可编辑）
- 相关技能链接

#### 4. 对比页面
- 时间效率对比
- 代码质量对比
- 交互式图表（Recharts）
- 具体技能效果对比

#### 5. 实战案例页
- 完整的开发流程时间线
- 6 个阶段的详细说明
- 每个阶段使用的技能
- 实际输出示例

#### 6. 代码示例页
- 集成代码编辑器（Monaco Editor）
- 实时预览
- 语法高亮
- 复制按钮

### 设计要求

#### 响应式设计
- 桌面端：> 1024px
- 平板端：768px - 1024px
- 移动端：< 768px

#### 主题
- 支持浅色/深色模式切换
- 优雅的配色方案
- 一致的设计语言

#### 动画
- 页面过渡动画
- 卡片悬停效果
- 按钮点击反馈
- 平滑滚动

## 页面结构

```
/ (首页)
├── Hero Section
├── Skills Overview
├── Quick Start Guide
└── Call to Action

/skills (技能浏览)
├── Sidebar (分类)
├── Search Bar
└── Skills Grid

/skills/[id] (技能详情)
├── Skill Header
├── Description
├── Usage Examples
├── Code Examples (可编辑)
└── Related Skills

/comparison (对比页面)
├── Overview Cards
├── Charts Section
└── Detailed Comparison

/case-study (实战案例)
├── Timeline
├── Phase Details
└── Outputs

/code-examples (代码示例)
├── Editor
├── Preview
└── Copy Button
```

## 数据结构

### Skill 数据

```typescript
interface Skill {
  id: string
  name: string
  collection: 'superpowers' | 'anthropics' | 'agent-toolkit'
  description: string
  category: string
  useCases: string[]
  examples: CodeExample[]
  commands: string[]
  relatedSkills: string[]
}
```

### Comparison 数据

```typescript
interface ComparisonMetric {
  category: string
  metric: string
  traditional: number
  withSkills: number
  unit: string
  improvement: string
}
```

## 性能要求

- **首次加载**: < 2s
- **页面切换**: < 500ms
- **搜索响应**: < 100ms
- **Lighthouse 分数**: > 90

## SEO 要求

- Meta tags 优化
- 结构化数据（Schema.org）
- Sitemap.xml
- Robots.txt

## 部署要求

- **平台**: Vercel
- **域名**: skills-demo.vercel.app
- **CI/CD**: 自动部署
- **监控**: Vercel Analytics

## 开发时间线

| 阶段 | 任务 | 预计时间 | 使用的技能 |
|------|------|---------|-----------|
| 1 | 需求讨论与规划 | 30 min | brainstorming, writing-plans |
| 2 | 项目初始化 | 15 min | using-git-worktrees, design-system-starter |
| 3 | 首页开发 | 60 min | test-driven-development, frontend-design |
| 4 | 技能浏览页 | 90 min | subagent-driven-development |
| 5 | 对比页面 | 45 min | frontend-design |
| 6 | 实战案例页 | 60 min | subagent-driven-development |
| 7 | 代码示例页 | 60 min | frontend-design |
| 8 | 代码审查 | 30 min | requesting-code-review |
| 9 | 文档编写 | 20 min | crafting-effective-readmes |
| 10 | 部署 | 15 min | - |

**总计**: ~7 小时

## 成功标准

- ✅ 所有页面正常渲染
- ✅ 响应式设计完美适配
- ✅ 所有功能可正常使用
- ✅ 性能指标达标
- ✅ 代码测试覆盖率 > 80%
- ✅ 无控制台错误
- ✅ 部署成功并可访问

---

**创建时间**: 2026-01-27
**技术选型**: Next.js 14 + TypeScript + Tailwind CSS
**使用的技能包**: Ultimate Skills Bundle v1.0.0
