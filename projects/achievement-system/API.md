# 成就系统 API 文档

## 核心类

### AchievementSystem

成就系统主类，提供统一的高层接口。

#### 初始化

```python
from achievement_system import AchievementSystem

system = AchievementSystem(base_dir=None)  # base_dir 可选，默认为 data 目录
```

#### 工具追踪

```python
# 记录工具使用
system.track_tool_usage(tool_name: str, success: bool = True)

# 示例
system.track_tool_usage('read', success=True)
system.track_tool_usage('coding-agent', success=False)
```

#### 技能追踪

```python
# 记录技能使用
system.track_skill_usage(skill_name: str)

# 示例
system.track_skill_usage('coding')
system.track_skill_usage('search')
```

#### 工作流追踪

```python
# 记录工作流完成
system.track_workflow_completion(workflow_name: str)

# 示例
system.track_workflow_completion('automation')
system.track_workflow_completion('backup')
```

#### 消息追踪

```python
# 记录消息数量
system.track_message_count(count: int, platform: str = "unknown")

# 示例
system.track_message_count(10, platform='slack')
system.track_message_count(5, platform='telegram')
```

#### 状态查询

```python
# 显示当前状态
system.show_status(detailed: bool = False)

# 示例
system.show_status()           # 简要信息
system.show_status(detailed=True)  # 详细信息
```

#### 成就列表

```python
# 列出成就
system.list_achievements(
    unlocked_only: bool = False,
    locked_only: bool = False
)

# 示例
system.list_achievements()              # 所有成就
system.list_achievements(unlocked_only=True)   # 只显示已解锁
system.list_achievements(locked_only=True)     # 只显示未解锁
```

#### 数据导出

```python
# 导出数据
system.export_data(
    format: str = "json",        # "json" 或 "csv"
    output_path: str = None      # 输出文件路径，可选
)

# 示例
system.export_data(format="json", output_path="achievements.json")
system.export_data(format="csv")
```

#### 可视化

```python
# 显示可视化统计
system.visualize(
    view_type: str = "all",      # "all", "activity", "achievements", "metrics"
    days: int = 7                # 显示最近多少天
)

# 示例
system.visualize()                           # 所有统计
system.visualize(view_type="activity")      # 只显示活动
system.visualize(view_type="achievements", days=30)  # 最近30天成就
```

#### 重置功能

```python
# 重置所有数据
system.reset_all()

# 重置成就
system.reset_achievements()
```

---

### ActivityTracker

活动追踪器，负责记录和统计用户活动。

#### 初始化

```python
from activity_tracker import ActivityTracker

tracker = ActivityTracker(data_store=None)
```

#### 记录活动

```python
# 工具使用
tracker.track_tool_usage(tool_name: str, success: bool = True) -> bool

# 技能使用
tracker.track_skill_usage(skill_name: str) -> bool

# 消息数量
tracker.track_message_count(count: int, platform: str = "unknown") -> bool

# 命令执行
tracker.track_command_execution(
    command: str,
    success: bool = True,
    duration_ms: int = None
) -> bool

# 会话开始
tracker.track_session_start(session_type: str = "general") -> bool

# 深夜时段使用
tracker.track_night_owl_usage(hour: int) -> bool
```

#### 统计查询

```python
# 工具使用统计
tool_stats = tracker.get_tool_usage_stats(days: int = 7)

# 技能使用统计
skill_stats = tracker.get_skill_usage_stats(days: int = 7)

# 消息统计
message_stats = tracker.get_message_stats(days: int = 7)

# 最常用工具
top_tools = tracker.get_top_tools(limit: int = 5, days: int = 7)

# 最常用技能
top_skills = tracker.get_top_skills(limit: int = 5, days: int = 7)
```

---

### AchievementEngine

成就引擎，负责检测和解锁成就。

#### 初始化

```python
from achievement_engine import AchievementEngine

engine = AchievementEngine(data_store=None)
```

#### 成就检测

```python
# 检查所有成就
newly_unlocked = engine.check_achievements()
# 返回新解锁的成就ID列表

# 检查特定成就
unlocked = engine.check_specific_achievement(achievement_id: str)
# 返回是否解锁（新解锁返回True）
```

#### 查询成就

```python
# 获取已解锁成就
unlocked = engine.get_unlocked_achievements()

# 获取未解锁成就
locked = engine.get_locked_achievements()

# 获取成就进度
progress = engine.get_progress(achievement_id: str)

# 按分类获取成就
achievements = engine.get_achievements_by_category(category)

# 获取成就统计
stats = engine.get_achievement_stats()
# 返回：{
#     'total': 总数,
#     'unlocked': 已解锁数,
#     'locked': 未解锁数,
#     'completion_rate': 完成率,
#     'rarity_stats': 按稀有度统计,
#     'category_stats': 按分类统计
# }
```

#### 手动解锁

```python
# 手动解锁成就（用于创造性使用案例等）
success = engine.manual_unlock(achievement_id: str)
```

---

### DataStore

数据存储类，提供 JSON 文件持久化功能。

#### 初始化

```python
from data_store import DataStore

store = DataStore(base_dir=None)  # 默认为 data 目录
```

#### 活动数据

```python
# 获取所有活动数据
activities = store.get_activities()

# 保存活动数据
store.save_activity(date: str, activity_data: dict) -> bool

# 获取指定日期的活动
activity = store.get_activity_by_date(date: str)

# 获取日期范围内的活动
activities = store.get_activities_in_range(start_date: str, end_date: str)
```

#### 成就数据

```python
# 获取所有成就数据
achievements = store.get_achievements()

# 保存成就数据
store.save_achievement(achievement_id: str, data: dict) -> bool

# 解锁成就
store.unlock_achievement(achievement_id: str, unlock_time: str = None) -> bool

# 重置所有成就
store.reset_achievements() -> bool
```

#### 工作流数据

```python
# 获取所有工作流数据
workflows = store.get_workflows()

# 保存工作流数据
store.save_workflow(workflow_id: str, data: dict) -> bool
```

#### 效率指标

```python
# 获取所有效率指标
metrics = store.get_metrics()

# 更新效率指标
store.update_metric(metric_name: str, value: Any) -> bool

# 递增效率指标
store.increment_metric(metric_name: str, amount: int = 1) -> bool
```

#### 用户配置

```python
# 获取用户配置
profile = store.get_user_profile()

# 更新用户配置
store.update_user_profile(data: dict) -> bool

# 获取连续使用天数信息
streak_info = store.get_streak_info()
# 返回：{
#     'current': 当前连续天数,
#     'longest': 最长连续天数,
#     'last_active_date': 最后活跃日期
# }

# 更新连续使用天数
streak_info = store.update_streak(date: str)
```

#### 数据导出

```python
# 导出所有数据
all_data = store.export_all_data()

# 导出 CSV 格式数据
csv_data = store.export_csv(data_type: str = "activities")
```

---

### WorkflowTracker

工作流追踪器，负责追踪和记录工作流相关信息。

#### 初始化

```python
from workflow_tracker import WorkflowTracker

tracker = WorkflowTracker(data_store=None)
```

#### 工作流操作

```python
# 启动工作流
workflow_id = tracker.start_workflow(
    workflow_type: str,
    name: str = None
) -> str

# 完成工作流
tracker.complete_workflow(workflow_id: str, success: bool = True) -> bool

# 记录 cron 任务执行
tracker.track_cron_execution(workflow_type: str) -> bool
```

#### 效率指标

```python
# 记录时间节省
tracker.record_time_saved(minutes: int) -> bool

# 记录问题解决
tracker.record_problem_solved() -> bool

# 记录子代理任务
tracker.track_subagent_task(created: bool = False, completed: bool = False) -> bool
```

#### 统计查询

```python
# 获取工作流统计
stats = tracker.get_workflow_stats()
# 返回：{
#     'total_completions': 总完成数,
#     'total_cron_runs': 总 cron 执行数,
#     'by_type': 按类型统计,
#     'top_workflows': 最常用工作流
# }

# 获取工作流历史
history = tracker.get_workflow_history(limit: int = 10)
```

---

### Visualizer

数据可视化器，提供 ASCII 风格的数据可视化。

#### 静态方法

```python
from visualization import Visualizer

# 打印标题
Visualizer.print_header(title: str, width: int = 60)

# 打印章节标题
Visualizer.print_section(title: str)

# 格式化数字
formatted = Visualizer.format_number(num: int)

# 创建条形图
bar_chart = Visualizer.create_bar_chart(
    data: Dict[str, int],
    width: int = 40,
    label_width: int = 15
) -> str

# 创建进度条
progress_bar = Visualizer.create_progress_bar(
    progress: float,      # 0-100
    width: int = 30,
    filled_char: str = "█",
    empty_char: str = "░"
) -> str

# 创建表格
table = Visualizer.create_table(
    headers: List[str],
    rows: List[List[str]],
    align: List[str] = None  # 'left', 'right', 'center'
) -> str
```

#### 可视化方法

```python
# 可视化成就
Visualizer.visualize_achievements(
    unlocked: List[Dict],
    locked: List[Dict],
    stats: Dict
)

# 可视化活动
Visualizer.visualize_activity(
    tool_stats: Dict,
    skill_stats: Dict,
    message_stats: Dict
)

# 可视化效率指标
Visualizer.visualize_metrics(metrics: Dict, streak_info: Dict)

# 可视化工作流
Visualizer.visualize_workflow(workflow_stats: Dict)

# 显示完整仪表板
Visualizer.show_dashboard(system: AchievementSystem)
```

---

### Achievement (成就定义)

成就类，定义单个成就的属性和行为。

#### 定义新成就

```python
from achievements.definitions import Achievement, AchievementCategory

achievement = Achievement(
    achievement_id: str,          # 成就唯一标识
    name: str,                    # 成就名称
    description: str,             # 成就描述
    category: AchievementCategory,# 成就分类
    check_fn: Callable,           # 检查函数
    icon: str = "🏆",             # 成就图标
    hidden: bool = False,         # 是否隐藏（直到解锁）
    rarity: str = "common"        # 稀有度：common, rare, epic, legendary
)

# 检查是否满足条件
context = {...}
result = achievement.check(context) -> bool
```

#### 成就分类

```python
AchievementCategory.FIRST_TIME   # 首次使用
AchievementCategory.STREAK       # 连续使用
AchievementCategory.MILESTONE    # 里程碑
AchievementCategory.SKILL        # 技能大师
AchievementCategory.WORKFLOW     # 工作流专家
AchievementCategory.EFFICIENCY   # 效率达人
AchievementCategory.PERSONAL     # 个性化
AchievementCategory.NIGHT_OWL    # 夜猫子
```

---

## 上下文格式

成就检查函数接收的上下文字典：

```python
context = {
    # 工具统计
    'total_tools': int,                    # 总工具使用次数
    'total_tool_calls': int,               # 总工具调用次数
    'successful_tool_calls': int,          # 成功的调用次数
    'tools': Dict[str, int],               # 各工具使用次数

    # 技能统计
    'total_skills': int,                   # 总技能使用次数
    'skills': Dict[str, int],              # 各技能使用次数

    # 消息统计
    'total_messages': int,                 # 总消息数
    'platform_messages': Dict[str, int],   # 各平台消息数

    # 工作流统计
    'total_workflows': int,                # 总工作流完成数
    'total_cron_tasks': int,               # 总 cron 任务数

    # 连续使用
    'streak_current': int,                # 当前连续天数
    'streak_longest': int,                 # 最长连续天数

    # 效率指标
    'time_saved_minutes': int,            # 节省的时间（分钟）
    'problems_solved': int,                # 解决的问题数

    # 其他指标
    'night_owl_count': int,                # 深夜时段使用次数
    'creative_uses': int,                  # 创造性使用次数
    'combo_coding_filesystem': bool,       # 组合使用标记
}
```

---

## 使用示例

### 集成到 Clawdbot 技能

```python
from achievement_system import AchievementSystem

# 初始化（建议在技能初始化时）
system = AchievementSystem()

# 在技能执行时记录
def my_skill():
    # 记录技能使用
    system.track_skill_usage('my_skill')

    # 执行业务逻辑
    result = do_something()

    # 记录工具使用
    system.track_tool_usage('tool_name', success=result)

    # 自动检查成就
    system.achievement_engine.check_achievements()

    return result
```

### Cron 任务集成

```python
from achievement_system import AchievementSystem

def cron_job():
    system = AchievementSystem()

    # 开始工作流
    workflow_id = system.workflow_tracker.start_workflow('daily_backup')

    # 执行任务
    try:
        do_backup()
        system.track_tool_usage('exec', success=True)
        system.workflow_tracker.track_cron_execution('daily_backup')
    except:
        system.track_tool_usage('exec', success=False)
        raise
    finally:
        # 完成工作流
        system.workflow_tracker.complete_workflow(workflow_id)
        system.workflow_tracker.record_time_saved(10)  # 节省10分钟
```

### 子代理集成

```python
def create_subagent():
    system = AchievementSystem()

    # 创建子代理
    system.workflow_tracker.track_subagent_task(created=True)

    # 子代理执行...
    result = subagent.run()

    # 子代理完成
    if result:
        system.workflow_tracker.track_subagent_task(completed=True)

    return result
```

---

## 最佳实践

1. **惰性检查**：不要频繁调用 `check_achievements()`，建议在关键事件后调用
2. **批量记录**：对于大量活动，使用批量记录以提高效率
3. **错误处理**：记录工具使用时，确保正确标记成功/失败
4. **数据导出**：定期导出数据进行备份和分析
5. **自定义成就**：根据具体需求扩展成就定义

---

## 注意事项

- 数据存储使用文件锁，支持并发访问
- 所有数据存储在本地 JSON 文件中，确保备份
- 成就ID必须唯一，否则会覆盖
- 时间格式统一使用 ISO 8601 字符串
