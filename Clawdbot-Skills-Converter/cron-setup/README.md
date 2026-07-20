# X 和网上资源自动化抓取工作流 - 设置完成

## ✅ 已配置的定时任务

### 1. collect-prompts（已启用）
- **频率**: 每 6 小时 (21600000ms)
- **状态**: ✅ 启用
- **功能**: 使用 web_search 搜索 AI 提示词关键词
- **输出**: `/root/clawd/data/prompts/collected.jsonl`

### 2. x-twitter-prompts-scraper（待启用）
- **频率**: 每 8 小时
- **状态**: ⏸️ 禁用
- **功能**: 使用 twitter-search-skill 搜索 Twitter/X 提示词
- **关键词**: "AI prompt", "ChatGPT prompt", "Claude prompt", "prompt engineering"
- **输出**: `/root/clawd/data/x-scraping/prompts-YYYYMMDD.jsonl`

### 3. x-trends-monitor（待启用）
- **频率**: 每 4 小时
- **状态**: ⏸️ 禁用
- **功能**: 使用 x-trends 监控热门话题
- **过滤**: AI, prompt, ChatGPT, Claude 等关键词
- **输出**: `/root/clawd/data/trends/x-trends-YYYYMMDD.json`

### 4. web-prompts-collector（待启用）
- **频率**: 每 12 小时
- **状态**: ⏸️ 禁用
- **功能**: 搜索并抓取网上的 AI 提示词资源
- **输出**: `/root/clawd/data/web-resources/collected-YYYYMMDD.jsonl`

### 5. prompts-quality-evaluator（待启用）
- **频率**: 每 8 小时
- **状态**: ⏸️ 禁用
- **功能**: 5 维度质量评估系统
- **评分**: 实用性(30%) + 创新性(20%) + 完整性(20%) + 热度(25%) + 作者影响力(5%)
- **输出**: `/root/clawd/data/evaluation/scored-prompts-YYYYMMDD.jsonl`

### 6. high-quality-skill-generator（待启用）
- **频率**: 每 24 小时
- **状态**: ⏸️ 禁用
- **功能**: 将高分提示词(>=80分)自动转换为 Skill
- **输出**: `/root/clawd/data/generated-skills/`

## 📁 数据目录结构

```
/root/clawd/data/
├── x-scraping/           # Twitter/X 抓取数据
├── trends/              # 热门话题监控
├── web-resources/       # 网络资源收集
├── evaluation/          # 质量评估结果
└── generated-skills/    # 自动生成的 Skills
```

## 🚀 启用任务

要启用特定的定时任务，编辑 `/root/.clawdbot/cron/jobs.json`，将对应的 `"enabled": false` 改为 `"enabled": true"`，然后重启 Gateway：

```bash
clawdbot gateway restart
```

### 推荐启用顺序

1. **第一阶段**: 只启用数据收集
   - `x-twitter-prompts-scraper`
   - `x-trends-monitor`
   - `web-prompts-collector`

2. **第二阶段**: 启用评估系统
   - `prompts-quality-evaluator`

3. **第三阶段**: 启用自动化转换
   - `high-quality-skill-generator`

## 📊 工作流说明

### 完整自动化链

```
1. 数据收集 (每4-12小时)
   ├─ X/Twitter 搜索
   ├─ 热门话题监控
   └─ 网络资源抓取
        ↓
2. 质量评估 (每8小时)
   ├─ 5维度评分
   ├─ 等级划分 (A+ to D)
   └─ 过滤低质量内容
        ↓
3. 自动转换 (每24小时)
   ├─ 筛选高分提示词 (>=80)
   ├─ 生成 Skill 结构
   ├─ 打包为 .skill 文件
   └─ 提交到 Git
        ↓
4. 发布到 ClawdHub (手动)
   └─ 定价和上架
```

## 🎯 评分标准

| 等级 | 分数范围 | 建议价格 |
|------|----------|----------|
| A+   | 90-100   | $9.99    |
| A    | 85-89    | $4.99    |
| B+   | 80-84    | $2.99    |
| B    | 70-79    | $1.99    |
| C+   | 60-69    | $0.99    |
| C    | 50-59    | 免费     |
| D    | 0-49     | 不收录   |

## 📈 预期效果

- **数据收集**: 每天 600-1000 条 AI 提示词
- **高质量内容**: 每天 100-200 条评分 >= 60
- **可转换 Skill**: 每天 10-30 条评分 >= 80
- **月产出**: 约 300-900 个高质量 Skills

## 🔧 管理命令

### 查看所有任务
```bash
clawdbot cron list
```

### 手动运行任务
```bash
clawdbot cron run <job-id>
```

### 查看任务运行记录
```bash
clawdbot cron runs <job-id>
```

### 启用/禁用任务
编辑 `/root/.clawdbot/cron/jobs.json` 后重启 Gateway。

## 📝 注意事项

1. **Twitter API Key**: 需要先配置 `TWITTER_API_KEY` 环境变量
2. **磁盘空间**: 数据会持续增长，建议定期清理旧数据
3. **Git 仓库**: 所有生成的 Skills 会自动提交到私有仓库
4. **Slack 通知**: 重要结果会发送到 #clawdbot 频道

## 🎉 下一步

1. 配置 Twitter API Key（如果还没有）
2. 手动测试第一个任务
3. 启用第一阶段的数据收集任务
4. 监控几天数据质量
5. 启用后续的评估和转换任务

---

*配置完成时间: 2026-01-29 13:35 UTC*
*Gateway 已重启并应用新配置*
