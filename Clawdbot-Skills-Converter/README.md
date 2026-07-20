# AI Prompt Marketplace → Clawdbot Skills Converter

自动化将 X (Twitter) 上的高质量 AI 提示词转换为 Clawdbot 技能，并通过 ClawdHub 平台变现的项目。

## 核心功能

### 1. 内容抓取与筛选
- 从 X 搜索热门 AI 提示词
- 使用关键词、趋势和影响力筛选内容
- 基于互动率（点赞、转发、评论）评估质量

### 2. 提示词质量评估
- 自动评估提示词的实用性、原创性、清晰度
- 识别重复或低质量内容
- 按领域分类（编程、设计、写作、商业等）

### 3. 技能转换系统
- 将提示词转换为符合 Clawdbot SKILL.md 规范的结构化技能
- 自动生成示例、参数、使用场景
- 优化技能描述以提高转化率

### 4. ClawdHub 集成
- 自动打包技能为 `.skill` 格式
- 批量发布到 ClawdHub 市场
- 自动生成技能截图和演示视频

## 项目结构

```
/root/clawd/
├── ai-content-aggregator/      # 内容抓取模块
├── ai-content-tracker/         # 质量追踪系统
├── skills/                     # 转换后的技能
├── experiments/                # 实验性功能
└── .clawdhub/                  # ClawdHub 发布配置
```

## 技术栈

- **X (Twitter) API**: 内容抓取
- **Clawdbot Skills**: 技能框架
- **ClawdHub CLI**: 发布工具
- **Node.js**: 自动化脚本
- **质量评估算法**: 自定义评分系统

## 商业模式

1. **免费技能**: 吸引用户，建立品牌
2. **付费技能**: 高质量、专业领域技能
3. **订阅套餐**: 批量访问技能库
4. **企业定制**: 为企业开发专属技能

## 开发阶段

- [x] 项目初始化
- [ ] X 搜索集成
- [ ] 质量评估算法
- [ ] 自动转换工具
- [ ] ClawdHub 自动发布
- [ ] 商业化验证

## 使用说明

```bash
# 安装依赖
npm install

# 运行内容抓取
./ai-content-aggregator/run.sh

# 评估和转换
./scripts/convert-prompts.js

# 发布到 ClawdHub
clawdhub publish
```

## 许可证

MIT License - 开源核心，商业变现
