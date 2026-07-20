# 极客风格个人主页开发任务

## 项目概述
重新设计 jack 个人主页，采用 Cyberpunk/极客风格，包含动态效果和交互体验。

---

## 设计要求

### 主题：Cyberpunk / 极客风格

**关键词**：
- 终端美学
- 霓虹灯效
- 代码艺术
- 动态交互
- 游戏化元素

---

## 实现清单

### Phase 1：基础框架 ✅
- [ ] 创建新的 HTML 结构 (`index-cyberpunk.html`)
- [ ] 实现深色主题（黑色背景 + 霓虹色）
- [ ] 更新项目列表为 25 个
- [ ] 创建 Hero 区域（终端风格）
- [ ] 创建技能矩阵（星级评分）
- [ ] 创建项目矩阵（分类展示）

### Phase 2：视觉效果 ⚡
- [ ] 实现代码雨效果（Matrix 风格）
- [ ] 实现 CRT 扫描线叠加
- [ ] 实现终端窗口样式
- [ ] 创建霓虹灯卡片边框效果

### Phase 3：动画效果 ✨
- [ ] 实现打字机效果（Hero 标语）
- [ ] 实现数字滚动动画（统计数据）
- [ ] 实现卡片悬浮效果（发光阴影）
- [ ] 实现数字计数器（从 0 滚动到目标）

### Phase 4：交互效果 🎯
- [ ] 实现鼠标跟随光标（圆形 + 混合模式）
- [ ] 实现点击涟漪效果（霓虹绿渐变）
- [ ] 优化性能（减少重绘）

---

## 配色方案

```css
--bg-primary: #0a0e0a;      /* 深黑 */
--bg-secondary: #111111;    /* 次深黑 */
--accent-primary: #00ff88;   /* 霓虹绿 */
--accent-secondary: #ff00ff;  /* 霓虹紫 */
--accent-tertiary: #00ffff;  /* 霓虹青 */
--text-primary: #00ff88;     /* 主文本（霓虹绿）*/
--text-secondary: #88ff88;   /* 次文本 */
--text-muted: #444444;      /* 暗淡文本 */
```

---

## 项目列表（25 个）

### 旗舰项目（1 个）
1. **Ultimate AI Workspace** ⭐
   - Ultimate Skills Bundle (70+ 技能）
   - Interactive Demo
   - AI Content Tracker
   - AI Media Tracker

### 工具类（8 个）
2. **Achievement System** ✅ 已完成
3. **AI Prompt Marketplace** 🏗️ 前后端
4. **AI Prompt to Skill** 🔄 运行中
5. **Moltbot Research** 🔍 持续
6. **SearXNG Self-Hosted** ✅ 已部署
7. **Automation Workflows** 🔄 持续优化
8. **Twitter API Bridge** 🌉 API 服务器
9. **Subtasks** 📝 任务管理

### 技能类（5 个）
10. **Career Planner Skill** 📋 职业规划
11. **Resume Builder Skill** 📄 简历构建
12. **Job Interviewer Skill** 🎤 求职面试
13. **Content Writer Skill** ✍️ 内容撰写
14. **ChatGPT Prompts Skill** 💬 提示词

### 其他（11 个）
15. **Tasks** - 通用任务管理
16. **Tutorials** - 教程集合
17. **Config** - 配置管理
18. **Plans** - 计划管理
19. **Research** - 研究项目
20. **Coding Reddit** - Reddit 编程
21. **AI Content Aggregator** - 内容聚合
22. **AI Content Hub** - 内容中心
23. **AI Content Tracker** - 内容追踪
24. **Cron Setup** - 定时任务
25. **Ultimate AI Workspace** - 工作空间

---

## 核心功能

### 1. Hero 区域（终端风格）
```html
<div class="hero">
  <div class="terminal-window">
    <div class="terminal-header">
      <span class="terminal-button red"></span>
      <span class="terminal-button yellow"></span>
      <span class="terminal-button green"></span>
      <span class="terminal-title">jack@clawd.bot:~$</span>
    </div>
    <div class="terminal-body">
      <div class="terminal-line">
        <span class="terminal-prompt">$</span>
        <span class="terminal-command">cat bio.md</span>
      </div>
      <div class="terminal-line">
        <span class="terminal-output">
          <div class="hero-title" id="typewriter"></div>
          <div class="hero-subtitle">
            AI 技能开发者 · 自动化工程师 · 开源爱好者
          </div>
        </span>
      </div>
    </div>
  </div>
</div>
```

### 2. 统计卡片（数字滚动）
```html
<div class="hero-stats">
  <div class="stat-card">
    <div class="stat-number" data-target="70">0</div>
    <div class="stat-label">AI 技能</div>
  </div>
  <div class="stat-card">
    <div class="stat-number" data-target="25">0</div>
    <div class="stat-label">项目</div>
  </div>
  <div class="stat-card">
    <div class="stat-number" data-target="5000">0</div>
    <div class="stat-label">代码行</div>
  </div>
</div>
```

### 3. 技能矩阵（星级评分）
- 开发工作流 ⭐⭐⭐⭐
- 技术栈 ⭐⭐⭐⭐⭐
- AI/ML ⭐⭐⭐⭐⭐⭐

### 4. 项目矩阵（分类展示）
- 旗舰项目（1 个）
- 工具类（8 个）
- 技能类（5 个）
- 其他（11 个）

---

## 动画效果实现

### 1. 打字机效果
- 逐字显示标语："构建智能技能生态 · 重新定义人机协作"
- 闪烁光标："█"
- Glitch 故障效果

### 2. 代码雨效果
- 类似 Matrix 的绿色字符雨
- 字符掉落动画
- 拖尾效果

### 3. 数字滚动
- 从 0 滚动到目标数字
- 缓动函数（easeOutQuart）
- 2 秒动画时长

### 4. 霓虹灯卡片
- 悬浮时发光边框
- 渐变光晕
- 模糊动画

---

## 交互效果实现

### 1. 鼠标跟随光标
- 圆形光标（20px）
- 混合模式（difference）
- 悬停时放大（2x）

### 2. 点击涟漪
- 点击产生涟漪
- 霓虹绿渐变
- 动画消失（600ms）

---

## 技术栈

- HTML5
- CSS3（Flexbox, Grid, Animations）
- JavaScript（ES6+）
- Canvas API（代码雨）

---

## 输出要求

### 文件结构
```
jack-portfolio/
├── index-cyberpunk.html    # 新的极客风格主页
├── css/
│   └── cyberpunk.css       # 深色主题样式
└── js/
    └── cyberpunk.js        # 动画和交互效果
```

### 功能清单
- ✅ 深色主题（Cyberpunk 风格）
- ✅ 代码雨背景效果
- ✅ CRT 扫描线叠加
- ✅ 终端窗口样式
- ✅ 打字机效果
- ✅ 数字滚动动画
- ✅ 霓虹灯卡片边框
- ✅ 鼠标跟随光标
- ✅ 点击涟漪效果
- ✅ 25 个项目展示
- ✅ 响应式设计
- ✅ 性能优化

---

## 开发顺序

1. **第一步**：创建基础 HTML 结构和深色主题
2. **第二步**：实现代码雨和 CRT 扫描线效果
3. **第三步**：实现打字机效果和数字滚动
4. **第四步**：实现交互效果（光标、涟漪）
5. **第五步**：测试和优化性能

---

## 参考资源

- 设计方案：`/root/clawd/memory/portfolio-cyberpunk-redesign.md`
- 原始文件：`/root/clawd/jack-portfolio/index-optimized.html`
- 项目数据：`/root/clawd/memory/2026-02-06-project-summaries.md`

---

**任务开始时间**：2026-02-07 17:10
**预计完成时间**：2-3 小时
**优先级**：高

开始开发！🚀
