# Clawdbot 成就系统

一个用于追踪和激励 Clawdbot 使用情况的成就系统，采用终端优先的方式。

## ✨ 特性

- 🏆 **多维度成就追踪**：工具使用、技能调用、消息处理、工作流完成等
- 🔥 **连续使用统计**：记录每日使用习惯
- 📊 **详细的活动统计**：可视化展示使用情况
- 💾 **JSON 数据持久化**：所有数据本地存储
- 🎨 **ASCII 风格可视化**：终端友好的界面展示
- 🔄 **工作流追踪**：支持自动化任务统计
- ⚡ **实时成就检测**：自动检测并解锁成就

## 📦 安装

```bash
cd /root/clawd/projects/achievement-system
```

## 🚀 快速开始

### 查看当前状态

```bash
python clawd_achievement.py status
python clawd_achievement.py status --detailed
```

### 记录活动

```bash
# 记录工具使用
python clawd_achievement.py track --tool read --success
python clawd_achievement.py track --tool coding-agent --success

# 记录技能使用
python clawd_achievement.py track --skill coding

# 记录消息处理
python clawd_achievement.py track --message 10 --platform slack

# 记录工作流完成
python clawd_achievement.py track --workflow automation
```

### 查看成就列表

```bash
# 所有成就
python clawd_achievement.py list

# 只显示已解锁
python clawd_achievement.py list --unlocked

# 只显示未解锁
python clawd_achievement.py list --locked
```

### 可视化统计

```bash
# 显示所有统计
python clawd_achievement.py visualize

# 只显示活动统计
python clawd_achievement.py visualize --type activity

# 只显示成就统计
python clawd_achievement.py visualize --type achievements

# 显示最近30天的数据
python clawd_achievement.py visualize --days 30
```

### 数据导出

```bash
# 导出为 JSON
python clawd_achievement.py export --format json

# 导出到文件
python clawd_achievement.py export --format json --output achievements.json

# 导出为 CSV
python clawd_achievement.py export --format csv
```

### 工作流操作

```bash
# 启动工作流
python clawd_achievement.py workflow --start automation --name "自动备份"

# 完成工作流
python clawd_achievement.py workflow --complete automation_20250131_123456_789
```

## 🏆 成就分类

### 🎯 首次使用
- 初次接触 - 第一次使用任何工具
- 技能觉醒 - 第一次使用技能
- 破冰 - 发送或接收第一条消息
- 自动化初体验 - 完成第一个工作流
- Hello World - 第一次使用 coding-agent

### 🔥 连续使用
- 坚持3天 - 连续使用 3 天
- 一周习惯 - 连续使用 7 天
- 月度忠实 - 连续使用 30 天

### 📈 里程碑
- 工具达人/专家/大师 - 累计使用工具 100/500/1000 次
- 技能爱好者/专家 - 累计使用技能 50/200 次
- 话痨/社交达人 - 累计处理消息 100/500 条

### 💪 技能大师
- 编程大师 - 使用 coding-agent 超过 50 次
- 探索者 - 使用超过 10 种不同的工具
- 多面手 - 使用超过 10 种不同的技能

### 🔄 工作流专家
- 自动化新手 - 完成 5 个工作流
- 自动化狂热者 - 完成 25 个工作流
- 时间管理者 - 执行 10 个 cron 任务

### ⚡ 效率达人
- 高效助手 - 工具调用成功率超过 95%
- 时间节省者 - 累计节省时间超过 10 小时
- 问题解决者 - 成功解决超过 50 个问题

### 🎨 个性化
- 强力组合 - 同一次会话中使用 coding-agent 和 filesystem 工具
- Slack 达人 - 在 Slack 平台处理超过 200 条消息
- Telegram 粉丝 - 在 Telegram 平台处理超过 200 条消息

### 🦉 夜猫子
- 熬夜冠军 - 深夜时段（23:00-07:00）使用超过 10 次
- 夜行者 - 深夜时段使用超过 50 次
- 暗夜之神 - 深夜时段使用超过 100 次

## 📊 数据结构

### 活动数据 (activities.json)
```json
{
  "2025-01-31": {
    "tools": {
      "read": {"count": 10, "success": 9, "failure": 1}
    },
    "skills": {
      "coding": 5
    },
    "messages": {
      "slack": 20,
      "telegram": 15
    },
    "night_owl": 2
  }
}
```

### 成就数据 (achievements.json)
```json
{
  "first_tool": {
    "name": "初次接触",
    "description": "第一次使用任何工具",
    "category": "首次使用",
    "icon": "🎯",
    "unlocked": true,
    "unlock_time": "2025-01-31T12:00:00",
    "rarity": "common"
  }
}
```

### 用户配置 (user_profile.json)
```json
{
  "streak": {
    "current": 5,
    "longest": 7,
    "last_active_date": "2025-01-31"
  }
}
```

## 🔧 高级用法

### 作为 Python 模块使用

```python
from sys.path.insert(0, '/root/clawd/projects/achievement-system/src')
from achievement_system import AchievementSystem

# 初始化系统
system = AchievementSystem()

# 记录活动
system.track_tool_usage('read', success=True)
system.track_skill_usage('coding')

# 自动检测成就
system.achievement_engine.check_achievements()

# 获取统计
stats = system.achievement_engine.get_achievement_stats()
print(f"完成度: {stats['completion_rate']}%")
```

### 自定义成就

编辑 `src/achievements/definitions.py`，添加新成就：

```python
achievements['my_custom'] = Achievement(
    achievement_id='my_custom',
    name='自定义成就',
    description='我的自定义成就描述',
    category=AchievementCategory.PERSONAL,
    check_fn=lambda ctx: ctx.get('custom_metric', 0) >= 100,
    icon='🌟',
    rarity='epic'
)
```

## 📁 项目结构

```
achievement-system/
├── clawd_achievement.py          # 命令行入口
├── src/
│   ├── __init__.py
│   ├── achievement_system.py     # 主系统集成类
│   ├── achievement_engine.py      # 成就检测引擎
│   ├── activity_tracker.py       # 活动追踪器
│   ├── data_store.py             # 数据存储层
│   ├── workflow_tracker.py       # 工作流追踪器
│   ├── visualization.py          # 数据可视化
│   └── achievements/
│       ├── __init__.py
│       └── definitions.py        # 成就定义
├── data/                         # 数据存储目录（自动创建）
│   ├── activities.json
│   ├── achievements.json
│   ├── workflows.json
│   ├── metrics.json
│   └── user_profile.json
├── examples/                     # 示例文件
└── README.md
```

## 🎯 使用场景

### 日常使用追踪
每次使用 Clawdbot 时记录活动：
```bash
# 开发前
python clawd_achievement.py track --tool coding-agent --success

# 检查进度
python clawd_achievement.py visualize
```

### 技能集成
将成就系统集成到 Clawdbot 技能中，自动记录使用情况。

### 数据分析
导出数据进行长期趋势分析：
```bash
python clawd_achievement.py export --format json --output analysis.json
```

## 🛠️ 技术细节

- **数据持久化**：JSON 文件 + 文件锁（并发安全）
- **成就检测**：惰性检查 + 事件触发
- **可视化**：纯 Python ASCII 艺术
- **依赖**：仅使用 Python 标准库

## 📝 开发计划

- [ ] 前端界面展示
- [ ] 更多成就类型
- [ ] 成就分享功能
- [ ] 成就排行榜（多用户）
- [ ] 统计图表生成

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可

MIT License
