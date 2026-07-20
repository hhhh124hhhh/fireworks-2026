"""
成就引擎模块

负责检测和解锁成就
"""

from typing import Dict, List, Optional, Set
from datetime import datetime
from data_store import DataStore
from achievements.definitions import create_achievement_definitions, Achievement, AchievementCategory


class AchievementEngine:
    """成就引擎"""

    def __init__(self, data_store: Optional[DataStore] = None):
        """
        初始化成就引擎

        Args:
            data_store: 数据存储实例
        """
        self.data_store = data_store or DataStore()
        self.achievements = create_achievement_definitions()
        self._init_achievements()

    def _init_achievements(self):
        """初始化成就数据存储"""
        stored_achievements = self.data_store.get_achievements()

        # 如果存储为空，初始化所有成就
        if not stored_achievements:
            for aid, achievement in self.achievements.items():
                self.data_store.save_achievement(aid, {
                    'name': achievement.name,
                    'description': achievement.description,
                    'category': achievement.category.value,
                    'icon': achievement.icon,
                    'unlocked': False,
                    'unlock_time': None,
                    'unlock_count': 0,
                    'rarity': achievement.rarity,
                    'hidden': achievement.hidden
                })
        else:
            # 更新成就定义（如果版本更新）
            for aid, achievement in self.achievements.items():
                if aid in stored_achievements:
                    # 更新可能变化的字段
                    stored = stored_achievements[aid]
                    if stored.get('name') != achievement.name or \
                       stored.get('description') != achievement.description:
                        stored['name'] = achievement.name
                        stored['description'] = achievement.description
                        stored['category'] = achievement.category.value
                        stored['icon'] = achievement.icon
                        stored['rarity'] = achievement.rarity
                        stored['hidden'] = achievement.hidden
                        self.data_store.save_achievement(aid, stored)
                else:
                    # 新增的成就
                    self.data_store.save_achievement(aid, {
                        'name': achievement.name,
                        'description': achievement.description,
                        'category': achievement.category.value,
                        'icon': achievement.icon,
                        'unlocked': False,
                        'unlock_time': None,
                        'unlock_count': 0,
                        'rarity': achievement.rarity,
                        'hidden': achievement.hidden
                    })

    def _build_context(self) -> Dict:
        """构建检查上下文"""
        from datetime import timedelta

        # 获取所有活动数据
        activities = self.data_store.get_activities()

        # 统计总数
        total_tools = 0
        total_skills = 0
        total_messages = 0
        successful_calls = 0
        total_tool_calls = 0

        tools_usage = {}
        skills_usage = {}
        platform_messages = {}
        night_owl_count = 0

        for date_data in activities.values():
            # 工具统计
            tools = date_data.get('tools', {})
            for tool_name, data in tools.items():
                count = data.get('count', 0)
                total_tools += count
                total_tool_calls += count
                successful_calls += data.get('success', 0)
                tools_usage[tool_name] = tools_usage.get(tool_name, 0) + count

            # 技能统计
            skills = date_data.get('skills', {})
            for skill_name, count in skills.items():
                total_skills += count
                skills_usage[skill_name] = skills_usage.get(skill_name, 0) + count

            # 消息统计
            messages = date_data.get('messages', {})
            for platform, count in messages.items():
                total_messages += count
                platform_messages[platform] = platform_messages.get(platform, 0) + count

            # 夜猫子统计
            night_owl_count += date_data.get('night_owl', 0)

        # 获取工作流数据
        workflows = self.data_store.get_workflows()
        total_workflows = sum(w.get('completion_count', 0) for w in workflows.values())
        total_cron_tasks = sum(w.get('cron_runs', 0) for w in workflows.values())

        # 获取效率指标
        metrics = self.data_store.get_metrics()

        # 获取连续使用天数
        streak_info = self.data_store.get_streak_info()

        return {
            'total_tools': total_tools,
            'total_skills': total_skills,
            'total_messages': total_messages,
            'total_tool_calls': total_tool_calls,
            'successful_tool_calls': successful_calls,
            'total_workflows': total_workflows,
            'total_cron_tasks': total_cron_tasks,
            'tools': tools_usage,
            'skills': skills_usage,
            'platform_messages': platform_messages,
            'night_owl_count': night_owl_count,
            'streak_current': streak_info.get('current', 0),
            'streak_longest': streak_info.get('longest', 0),
            'time_saved_minutes': metrics.get('time_saved_minutes', 0),
            'problems_solved': metrics.get('problems_solved', 0),
            'creative_uses': metrics.get('creative_uses', 0),
            'combo_coding_filesystem': metrics.get('combo_coding_filesystem', False)
        }

    def check_achievements(self) -> List[str]:
        """
        检查所有成就，返回新解锁的成就ID列表

        Returns:
            新解锁的成就ID列表
        """
        context = self._build_context()
        newly_unlocked = []

        for achievement_id, achievement in self.achievements.items():
            stored = self.data_store.get_achievements().get(achievement_id, {})

            # 如果已经解锁，跳过
            if stored.get('unlocked', False):
                continue

            # 检查是否满足条件
            if achievement.check(context):
                # 解锁成就
                self.data_store.unlock_achievement(achievement_id)
                newly_unlocked.append(achievement_id)

        return newly_unlocked

    def check_specific_achievement(self, achievement_id: str) -> bool:
        """
        检查特定成就是否解锁

        Args:
            achievement_id: 成就ID

        Returns:
            是否解锁（新解锁返回True，已解锁返回False）
        """
        stored = self.data_store.get_achievements().get(achievement_id, {})

        # 如果已经解锁
        if stored.get('unlocked', False):
            return False

        # 检查成就是否存在
        if achievement_id not in self.achievements:
            return False

        # 构建上下文并检查
        context = self._build_context()
        achievement = self.achievements[achievement_id]

        if achievement.check(context):
            self.data_store.unlock_achievement(achievement_id)
            return True

        return False

    def get_unlocked_achievements(self) -> List[Dict]:
        """
        获取已解锁的成就列表

        Returns:
            已解锁成就列表
        """
        stored = self.data_store.get_achievements()
        unlocked = []

        for aid, data in stored.items():
            if data.get('unlocked', False):
                achievement = self.achievements.get(aid)
                if achievement:
                    unlocked.append({
                        'id': aid,
                        'name': data.get('name'),
                        'description': data.get('description'),
                        'category': data.get('category'),
                        'icon': data.get('icon'),
                        'unlocked': True,
                        'unlock_time': data.get('unlock_time'),
                        'rarity': data.get('rarity')
                    })

        return sorted(unlocked, key=lambda x: x.get('unlock_time', ''), reverse=True)

    def get_locked_achievements(self) -> List[Dict]:
        """
        获取未解锁的成就列表

        Returns:
            未解锁成就列表（隐藏成就除外）
        """
        stored = self.data_store.get_achievements()
        locked = []

        for aid, data in stored.items():
            if not data.get('unlocked', False) and not data.get('hidden', False):
                achievement = self.achievements.get(aid)
                if achievement:
                    locked.append({
                        'id': aid,
                        'name': data.get('name'),
                        'description': data.get('description'),
                        'category': data.get('category'),
                        'icon': data.get('icon'),
                        'unlocked': False,
                        'rarity': data.get('rarity')
                    })

        # 按稀有度排序
        rarity_order = {'legendary': 0, 'epic': 1, 'rare': 2, 'common': 3}
        return sorted(locked, key=lambda x: rarity_order.get(x.get('rarity', 'common'), 4))

    def get_progress(self, achievement_id: str) -> Optional[Dict]:
        """
        获取成就进度

        Args:
            achievement_id: 成就ID

        Returns:
            进度信息，如果成就不存在返回None
        """
        if achievement_id not in self.achievements:
            return None

        context = self._build_context()
        achievement = self.achievements[achievement_id]

        # 这里可以添加更详细的进度计算逻辑
        # 简化版：只返回是否已解锁
        stored = self.data_store.get_achievements().get(achievement_id, {})

        return {
            'unlocked': stored.get('unlocked', False),
            'unlock_time': stored.get('unlock_time'),
            'unlock_count': stored.get('unlock_count', 0)
        }

    def get_achievements_by_category(self, category: AchievementCategory) -> List[Dict]:
        """
        按分类获取成就

        Args:
            category: 成就分类

        Returns:
            该分类下的所有成就
        """
        stored = self.data_store.get_achievements()
        result = []

        for aid, data in stored.items():
            if data.get('category') == category.value:
                achievement = self.achievements.get(aid)
                if achievement:
                    result.append({
                        'id': aid,
                        'name': data.get('name'),
                        'description': data.get('description'),
                        'icon': data.get('icon'),
                        'unlocked': data.get('unlocked', False),
                        'unlock_time': data.get('unlock_time'),
                        'rarity': data.get('rarity'),
                        'hidden': data.get('hidden', False)
                    })

        return result

    def get_achievement_stats(self) -> Dict:
        """
        获取成就统计信息

        Returns:
            统计信息字典
        """
        stored = self.data_store.get_achievements()

        total = len(stored)
        unlocked = sum(1 for data in stored.values() if data.get('unlocked', False))
        locked = total - unlocked

        # 按稀有度统计
        rarity_stats = {}
        for data in stored.values():
            rarity = data.get('rarity', 'common')
            if rarity not in rarity_stats:
                rarity_stats[rarity] = {'total': 0, 'unlocked': 0}
            rarity_stats[rarity]['total'] += 1
            if data.get('unlocked', False):
                rarity_stats[rarity]['unlocked'] += 1

        # 按分类统计
        category_stats = {}
        for data in stored.values():
            category = data.get('category', 'unknown')
            if category not in category_stats:
                category_stats[category] = {'total': 0, 'unlocked': 0}
            category_stats[category]['total'] += 1
            if data.get('unlocked', False):
                category_stats[category]['unlocked'] += 1

        return {
            'total': total,
            'unlocked': unlocked,
            'locked': locked,
            'completion_rate': round(unlocked / total * 100, 2) if total > 0 else 0,
            'rarity_stats': rarity_stats,
            'category_stats': category_stats
        }

    def manual_unlock(self, achievement_id: str) -> bool:
        """
        手动解锁成就（用于创造性使用案例等）

        Args:
            achievement_id: 成就ID

        Returns:
            是否成功
        """
        if achievement_id not in self.achievements:
            return False

        return self.data_store.unlock_achievement(achievement_id)
