# AI 提示词收割器

自动化从 X (Twitter) 搜索高质量 AI 提示词，评估并转换为 Clawdbot Skills，发布到 ClawdHub 进行售卖。

## 📋 系统要求

- Python 3.7+
- Node.js 和 npm
- Twitter API Key（从 https://twitterapi.io 获取）
- ClawdHub CLI

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装 ClawdHub CLI
npm i -g clawdhub

# 登录 ClawdHub
clawdhub login

# 安装 Python 依赖
pip3 install requests python-dotenv
```

### 2. 配置 Twitter API Key

```bash
# 设置环境变量（推荐）
export TWITTER_API_KEY='your_api_key_here'

# 或者添加到 ~/.bashrc
echo 'export TWITTER_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 测试运行

```bash
# 进入项目目录
cd /root/clawd/automation/x-prompts-harvester

# 测试模式（不发布，只创建技能）
python3 harvest.py --test

# 完整运行（包括发布到 ClawdHub）
python3 harvest.py --auto-publish
```

## 📁 文件结构

```
x-prompts-harvester/
├── harvest.py           # 主协调脚本
├── search_x.py          # X 搜索模块
├── evaluate.py          # 质量评估模块
├── convert_to_skill.py  # 转换为 Skill 模块
├── publish.py           # 发布到 ClawdHub 模块
├── state/               # 状态跟踪
│   ├── processed_prompts.json
│   ├── published_skills.json
│   └── metrics.json
├── skills-generated/    # 生成的技能临时存储
└── logs/                # 运行日志
```

## 🔄 工作流程

1. **搜索 X**：使用关键词搜索 AI 提示词
2. **质量评估**：基于清晰度、具体性、结构等维度评分
3. **转换 Skill**：将高分提示词转换为 Clawdbot Skills
4. **发布到 ClawdHub**：自动发布到技能市场

## 📊 质量评分标准

| 维度 | 说明 |
|------|------|
| 清晰度 | 是否明确易懂 |
| 具体性 | 是否有明确的约束和输出要求 |
| 结构化 | 是否有清晰的步骤或格式 |
| 完整性 | 是否包含必要的上下文 |
| 实用性 | 是否有实际应用场景 |

**评分阈值：**
- 高质量：>= 7.0/10
- 中等：5.0-7.0/10
- 低质量：< 5.0/10

只有高质量提示词会被转换为技能。

## ⏰ 定时任务配置

设置 Cron 任务每 6 小时运行一次：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（根据实际情况调整路径）
0 */6 * * * cd /root/clawd/automation/x-prompts-harvester && /usr/bin/python3 harvest.py --auto-publish >> logs/$(date +\%Y\%m\%d).log 2>&1
```

## 📈 监控和日志

### 查看运行日志

```bash
# 查看今天的日志
tail -f logs/$(date +%Y%m%d).log

# 查看最近的运行记录
ls -lt state/run_*.json | head -5
```

### 检查统计指标

```bash
# 查看总体指标
cat state/metrics.json

# 查看已发布的技能
cat state/published_skills.json
```

## 🛠️ 常用命令

```bash
# 测试模式（不发布）
python3 harvest.py --test

# 运行并自动发布
python3 harvest.py --auto-publish

# 只运行搜索（用于调试）
python3 search_x.py

# 测试质量评估
python3 evaluate.py

# 测试转换
python3 convert_to_skill.py

# 检查 ClawdHub 安装
python3 publish.py
```

## ⚠️ 故障排除

### API Key 错误

```
Error: TWITTER_API_KEY environment variable not set
```

**解决方法：**
```bash
export TWITTER_API_KEY='your_key_here'
```

### ClawdHub 未安装

```
Error: clawdhub CLI is not installed
```

**解决方法：**
```bash
npm i -g clawdhub
clawdhub login
```

### 发布失败

如果发布失败，可以手动发布：

```bash
# 查看生成的技能
ls -la skills-generated/

# 手动发布单个技能
clawdhub publish ./skills-generated/skill-name \
  --slug skill-name \
  --name "Display Name" \
  --version 1.0.20260128 \
  --changelog "Initial release"
```

## 📝 自定义配置

### 修改搜索关键词

编辑 `search_x.py` 中的 `build_prompt_queries()` 方法：

```python
def build_prompt_queries(self) -> List[str]:
    queries = [
        # 添加你的自定义查询
        '("your keyword" OR "another keyword") min_retweets:20 lang:en -is:retweet',
        # ...
    ]
    return queries
```

### 调整质量阈值

编辑 `harvest.py` 中的初始化：

```python
self.evaluator = PromptEvaluator()
# 修改阈值
self.evaluator.quality_threshold = 8.0  # 更严格
self.evaluator.min_score = 6.0  # 更宽松
```

### 修改搜索频率

编辑 Cron 任务：

```bash
# 每 4 小时
0 */4 * * * ...

# 每 8 小时
0 */8 * * * ...

# 每天早上 9 点
0 9 * * * ...
```

## 🎯 成功指标

系统会自动追踪以下指标：

- 发现的提示词数量
- 转换的技能数量
- 发布的技能数量
- 平均质量评分
- 运行时间

查看详细指标：
```bash
python3 -c "import json; print(json.dumps(json.load(open('state/metrics.json')), indent=2))"
```

## 📧 支持

如有问题，请查看日志文件或联系管理员。

---

*创建时间：2026-01-28*
