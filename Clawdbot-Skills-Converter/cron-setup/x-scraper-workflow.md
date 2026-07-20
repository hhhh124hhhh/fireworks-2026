# X 和网上资源自动化抓取工作流

## 工作流设计

基于 AI 提示词转 Skill 商业计划，创建完整的自动化链：

### 任务 1: X/Twitter 提示词抓取
- **频率**: 每 8 小时
- **关键词**: "AI prompt", "ChatGPT prompt", "Claude prompt", "prompt engineering", "AI tips"
- **输出**: `/root/clawd/data/x-scraping/prompts-YYYYMMDD.jsonl`
- **内容**: 推文内容、作者、互动数据、时间戳

### 任务 2: 质量评估
- **频率**: 每 8 小时（抓取后）
- **评分维度**:
  - 🎯 实用性 (30%)
  - 🎨 创新性 (20%)
  - 📖 完整性 (20%)
  - 🔥 热度 (25%)
  - 👨‍💼 作者影响力 (5%)
- **输出**: `/root/clawd/data/evaluation/scored-prompts-YYYYMMDD.jsonl`
- **过滤**: 只保留评分 >= 60 的提示词

### 任务 3: 转换为 Skill
- **频率**: 每 24 小时
- **输入**: 评分 >= 80 的高质量提示词
- **输出**: `/root/clawd/data/generated-skills/`
- **格式**: 完整的 Skill 目录结构

### 任务 4: 热门话题监控
- **频率**: 每 4 小时
- **工具**: x-trends
- **输出**: `/root/clawd/data/trends/x-trends-YYYYMMDD.json`
- **目的**: 发现新的热门 AI 相关话题

### 任务 5: 网络资源补充
- **频率**: 每 12 小时
- **工具**: web_search
- **关键词**: AI 提示词相关
- **输出**: `/root/clawd/data/web-resources/collected-YYYYMMDD.jsonl`

## Cron 调度

所有任务通过 Clawdbot cron 系统统一管理，确保：
- 任务之间的依赖关系
- 错误处理和重试机制
- 结果通知到 Slack
- 自动备份到 Git
