"""
成就定义模块

定义所有可解锁的成就
"""

from typing import Dict, List, Callable, Any
from enum import Enum


class AchievementCategory(Enum):
    """成就分类"""
    FIRST_TIME = "首次使用"
    STREAK = "连续使用"
    MILESTONE = "里程碑"
    SKILL = "技能大师"
    WORKFLOW = "工作流专家"
    EFFICIENCY = "效率达人"
    PERSONAL = "个性化"
    NIGHT_OWL = "夜猫子"


class Achievement:
    """成就类"""

    def __init__(
        self,
        achievement_id: str,
        name: str,
        description: str,
        category: AchievementCategory,
        check_fn: Callable[[], bool],
        icon: str = "🏆",
        hidden: bool = False,
        rarity: str = "common"  # common, rare, epic, legendary
    ):
        """
        初始化成就

        Args:
            achievement_id: 成就唯一标识
            name: 成就名称
            description: 成就描述
            category: 成就分类
            check_fn: 检查函数，返回是否解锁
            icon: 成就图标
            hidden: 是否隐藏（直到解锁）
            rarity: 稀有度
        """
        self.achievement_id = achievement_id
        self.name = name
        self.description = description
        self.category = category
        self.check_fn = check_fn
        self.icon = icon
        self.hidden = hidden
        self.rarity = rarity

    def check(self, context: Dict[str, Any]) -> bool:
        """检查是否满足解锁条件"""
        return self.check_fn(context)


def create_achievement_definitions() -> Dict[str, Achievement]:
    """
    创建所有成就定义

    Returns:
        成就ID到成就对象的映射
    """
    achievements = {}

    # ========== 首次使用成就 ==========

    achievements['first_tool'] = Achievement(
        achievement_id='first_tool',
        name='初次接触',
        description='第一次使用任何工具',
        category=AchievementCategory.FIRST_TIME,
        check_fn=lambda ctx: ctx.get('total_tools', 0) >= 1,
        icon='🎯'
    )

    achievements['first_skill'] = Achievement(
        achievement_id='first_skill',
        name='技能觉醒',
        description='第一次使用技能',
        category=AchievementCategory.FIRST_TIME,
        check_fn=lambda ctx: ctx.get('total_skills', 0) >= 1,
        icon='⚡'
    )

    achievements['first_message'] = Achievement(
        achievement_id='first_message',
        name='破冰',
        description='发送或接收第一条消息',
        category=AchievementCategory.FIRST_TIME,
        check_fn=lambda ctx: ctx.get('total_messages', 0) >= 1,
        icon='💬'
    )

    achievements['first_workflow'] = Achievement(
        achievement_id='first_workflow',
        name='自动化初体验',
        description='完成第一个工作流',
        category=AchievementCategory.FIRST_TIME,
        check_fn=lambda ctx: ctx.get('total_workflows', 0) >= 1,
        icon='🔄'
    )

    achievements['first_coding'] = Achievement(
        achievement_id='first_coding',
        name='Hello World',
        description='第一次使用 coding-agent',
        category=AchievementCategory.FIRST_TIME,
        check_fn=lambda ctx: ctx.get('tools', {}).get('coding-agent', 0) >= 1,
        icon='💻'
    )

    # ========== 连续使用成就 ==========

    achievements['streak_3'] = Achievement(
        achievement_id='streak_3',
        name='坚持3天',
        description='连续使用 Clawdbot 3天',
        category=AchievementCategory.STREAK,
        check_fn=lambda ctx: ctx.get('streak_current', 0) >= 3,
        icon='🔥'
    )

    achievements['streak_7'] = Achievement(
        achievement_id='streak_7',
        name='一周习惯',
        description='连续使用 Clawdbot 7天',
        category=AchievementCategory.STREAK,
        check_fn=lambda ctx: ctx.get('streak_current', 0) >= 7,
        icon='🔥🔥'
    )

    achievements['streak_30'] = Achievement(
        achievement_id='streak_30',
        name='月度忠实',
        description='连续使用 Clawdbot 30天',
        category=AchievementCategory.STREAK,
        check_fn=lambda ctx: ctx.get('streak_current', 0) >= 30,
        icon='🔥🔥🔥'
    )

    # ========== 里程碑成就 ==========

    achievements['tools_100'] = Achievement(
        achievement_id='tools_100',
        name='工具达人',
        description='累计使用工具 100次',
        category=AchievementCategory.MILESTONE,
        check_fn=lambda ctx: ctx.get('total_tool_calls', 0) >= 100,
        icon='🛠️'
    )

    achievements['tools_500'] = Achievement(
        achievement_id='tools_500',
        name='工具专家',
        description='累计使用工具 500次',
        category=AchievementCategory.MILESTONE,
        check_fn=lambda ctx: ctx.get('total_tool_calls', 0) >= 500,
        icon='🛠️🛠️',
        rarity='rare'
    )

    achievements['tools_1000'] = Achievement(
        achievement_id='tools_1000',
        name='工具大师',
        description='累计使用工具 1000次',
        category=AchievementCategory.MILESTONE,
        check_fn=lambda ctx: ctx.get('total_tool_calls', 0) >= 1000,
        icon='🛠️🛠️🛠️',
        rarity='epic'
    )

    achievements['skills_50'] = Achievement(
        achievement_id='skills_50',
        name='技能爱好者',
        description='累计使用技能 50次',
        category=AchievementCategory.MILESTONE,
        check_fn=lambda ctx: ctx.get('total_skill_calls', 0) >= 50,
        icon='⚡'
    )

    achievements['skills_200'] = Achievement(
        achievement_id='skills_200',
        name='技能专家',
        description='累计使用技能 200次',
        category=AchievementCategory.MILESTONE,
        check_fn=lambda ctx: ctx.get('total_skill_calls', 0) >= 200,
        icon='⚡⚡',
        rarity='rare'
    )

    achievements['messages_100'] = Achievement(
        achievement_id='messages_100',
        name='话痨',
        description='累计处理消息 100条',
        category=AchievementCategory.MILESTONE,
        check_fn=lambda ctx: ctx.get('total_messages', 0) >= 100,
        icon='💬'
    )

    achievements['messages_500'] = Achievement(
        achievement_id='messages_500',
        name='社交达人',
        description='累计处理消息 500条',
        category=AchievementCategory.MILESTONE,
        check_fn=lambda ctx: ctx.get('total_messages', 0) >= 500,
        icon='💬💬'
    )

    # ========== 技能大师成就 ==========

    achievements['coding_master'] = Achievement(
        achievement_id='coding_master',
        name='编程大师',
        description='使用 coding-agent 超过 50次',
        category=AchievementCategory.SKILL,
        check_fn=lambda ctx: ctx.get('tools', {}).get('coding-agent', 0) >= 50,
        icon='💻'
    )

    achievements['explorer'] = Achievement(
        achievement_id='explorer',
        name='探索者',
        description='使用超过 10种不同的工具',
        category=AchievementCategory.SKILL,
        check_fn=lambda ctx: len(ctx.get('tools', {})) >= 10,
        icon='🧭'
    )

    achievements['polyglot'] = Achievement(
        achievement_id='polyglot',
        name='多面手',
        description='使用超过 10种不同的技能',
        category=AchievementCategory.SKILL,
        check_fn=lambda ctx: len(ctx.get('skills', {})) >= 10,
        icon='🎭'
    )

    # ========== 工作流专家成就 ==========

    achievements['workflow_starter'] = Achievement(
        achievement_id='workflow_starter',
        name='自动化新手',
        description='完成 5个工作流',
        category=AchievementCategory.WORKFLOW,
        check_fn=lambda ctx: ctx.get('total_workflows', 0) >= 5,
        icon='🔄'
    )

    achievements['automation_enthusiast'] = Achievement(
        achievement_id='automation_enthusiast',
        name='自动化狂热者',
        description='完成 25个工作流',
        category=AchievementCategory.WORKFLOW,
        check_fn=lambda ctx: ctx.get('total_workflows', 0) >= 25,
        icon='🔄🔄',
        rarity='rare'
    )

    achievements['cron_master'] = Achievement(
        achievement_id='cron_master',
        name='时间管理者',
        description='执行 10个 cron 任务',
        category=AchievementCategory.WORKFLOW,
        check_fn=lambda ctx: ctx.get('total_cron_tasks', 0) >= 10,
        icon='⏰'
    )

    # ========== 效率达人成就 ==========

    achievements['efficient'] = Achievement(
        achievement_id='efficient',
        name='高效助手',
        description='工具调用成功率超过 95%',
        category=AchievementCategory.EFFICIENCY,
        check_fn=lambda ctx: _calculate_success_rate(ctx) >= 95,
        icon='📊'
    )

    achievements['time_saver'] = Achievement(
        achievement_id='time_saver',
        name='时间节省者',
        description='通过自动化累计节省时间超过 10小时',
        category=AchievementCategory.EFFICIENCY,
        check_fn=lambda ctx: ctx.get('time_saved_minutes', 0) >= 600,
        icon='⏱️'
    )

    achievements['problem_solver'] = Achievement(
        achievement_id='problem_solver',
        name='问题解决者',
        description='成功解决超过 50个问题',
        category=AchievementCategory.EFFICIENCY,
        check_fn=lambda ctx: ctx.get('problems_solved', 0) >= 50,
        icon='✅'
    )

    # ========== 个性化成就 ==========

    achievements['power_combo'] = Achievement(
        achievement_id='power_combo',
        name='强力组合',
        description='在同一次会话中使用 coding-agent 和 filesystem 工具',
        category=AchievementCategory.PERSONAL,
        check_fn=lambda ctx: ctx.get('combo_coding_filesystem', False),
        icon='🔗'
    )

    achievements['slack_active'] = Achievement(
        achievement_id='slack_active',
        name='Slack 达人',
        description='在 Slack 平台处理超过 200条消息',
        category=AchievementCategory.PERSONAL,
        check_fn=lambda ctx: ctx.get('platform_messages', {}).get('slack', 0) >= 200,
        icon='#️⃣'
    )

    achievements['telegram_active'] = Achievement(
        achievement_id='telegram_active',
        name='Telegram 粉丝',
        description='在 Telegram 平台处理超过 200条消息',
        category=AchievementCategory.PERSONAL,
        check_fn=lambda ctx: ctx.get('platform_messages', {}).get('telegram', 0) >= 200,
        icon='✈️'
    )

    achievements['creative_user'] = Achievement(
        achievement_id='creative_user',
        name='创意用户',
        description='手动标记为创造性使用案例',
        category=AchievementCategory.PERSONAL,
        check_fn=lambda ctx: ctx.get('creative_uses', 0) >= 1,
        icon='🎨',
        hidden=True
    )

    # ========== 夜猫子成就 ==========

    achievements['night_owl_1'] = Achievement(
        achievement_id='night_owl_1',
        name='熬夜冠军',
        description='深夜时段（23:00-07:00）使用超过 10次',
        category=AchievementCategory.NIGHT_OWL,
        check_fn=lambda ctx: ctx.get('night_owl_count', 0) >= 10,
        icon='🦉'
    )

    achievements['night_owl_2'] = Achievement(
        achievement_id='night_owl_2',
        name='夜行者',
        description='深夜时段（23:00-07:00）使用超过 50次',
        category=AchievementCategory.NIGHT_OWL,
        check_fn=lambda ctx: ctx.get('night_owl_count', 0) >= 50,
        icon='🦉🦉',
        rarity='rare'
    )

    achievements['night_owl_3'] = Achievement(
        achievement_id='night_owl_3',
        name='暗夜之神',
        description='深夜时段（23:00-07:00）使用超过 100次',
        category=AchievementCategory.NIGHT_OWL,
        check_fn=lambda ctx: ctx.get('night_owl_count', 0) >= 100,
        icon='🦉🦉🦉',
        rarity='epic'
    )

    return achievements


def _calculate_success_rate(ctx: Dict[str, Any]) -> float:
    """计算成功率"""
    total_calls = ctx.get('total_tool_calls', 0)
    successful_calls = ctx.get('successful_tool_calls', 0)

    if total_calls == 0:
        return 0.0

    return (successful_calls / total_calls) * 100
