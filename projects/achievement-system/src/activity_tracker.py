"""
活动追踪模块

记录和统计用户的各种活动
"""

from datetime import datetime
from typing import Dict, List, Optional
from data_store import DataStore


class ActivityTracker:
    """活动追踪器"""

    def __init__(self, data_store: Optional[DataStore] = None):
        """
        初始化活动追踪器

        Args:
            data_store: 数据存储实例，如果为None则创建新实例
        """
        self.data_store = data_store or DataStore()

    def _get_today(self) -> str:
        """获取今天的日期字符串"""
        return datetime.now().strftime("%Y-%m-%d")

    def track_tool_usage(self, tool_name: str, success: bool = True) -> bool:
        """
        记录工具使用

        Args:
            tool_name: 工具名称
            success: 是否成功

        Returns:
            是否保存成功
        """
        date = self._get_today()
        activities = self.data_store.get_activity_by_date(date)

        if 'tools' not in activities:
            activities['tools'] = {}

        if tool_name not in activities['tools']:
            activities['tools'][tool_name] = {
                'count': 0,
                'success': 0,
                'failure': 0
            }

        activities['tools'][tool_name]['count'] += 1
        if success:
            activities['tools'][tool_name]['success'] += 1
        else:
            activities['tools'][tool_name]['failure'] += 1

        return self.data_store.save_activity(date, activities)

    def track_skill_usage(self, skill_name: str) -> bool:
        """
        记录技能使用

        Args:
            skill_name: 技能名称

        Returns:
            是否保存成功
        """
        date = self._get_today()
        activities = self.data_store.get_activity_by_date(date)

        if 'skills' not in activities:
            activities['skills'] = {}

        activities['skills'][skill_name] = activities['skills'].get(skill_name, 0) + 1

        return self.data_store.save_activity(date, activities)

    def track_message_count(self, count: int, platform: str = "unknown") -> bool:
        """
        记录消息数量

        Args:
            count: 消息数量
            platform: 平台名称 (slack/telegram/feishu)

        Returns:
            是否保存成功
        """
        date = self._get_today()
        activities = self.data_store.get_activity_by_date(date)

        if 'messages' not in activities:
            activities['messages'] = {}

        activities['messages'][platform] = activities['messages'].get(platform, 0) + count

        return self.data_store.save_activity(date, activities)

    def track_command_execution(self, command: str, success: bool = True, duration_ms: Optional[int] = None) -> bool:
        """
        记录命令执行

        Args:
            command: 命令
            success: 是否成功
            duration_ms: 执行时长（毫秒）

        Returns:
            是否保存成功
        """
        date = self._get_today()
        activities = self.data_store.get_activity_by_date(date)

        if 'commands' not in activities:
            activities['commands'] = []

        activities['commands'].append({
            'command': command,
            'success': success,
            'duration_ms': duration_ms,
            'timestamp': datetime.now().isoformat()
        })

        return self.data_store.save_activity(date, activities)

    def track_session_start(self, session_type: str = "general") -> bool:
        """
        记录会话开始

        Args:
            session_type: 会话类型

        Returns:
            是否保存成功
        """
        date = self._get_today()
        activities = self.data_store.get_activity_by_date(date)

        if 'sessions' not in activities:
            activities['sessions'] = {}

        if session_type not in activities['sessions']:
            activities['sessions'][session_type] = 0

        activities['sessions'][session_type] += 1

        # 更新连续使用天数
        self.data_store.update_streak(date)

        return self.data_store.save_activity(date, activities)

    def track_night_owl_usage(self, hour: int) -> bool:
        """
        记录深夜时段使用（23:00-07:00）

        Args:
            hour: 当前小时（0-23）

        Returns:
            是否保存成功
        """
        if 23 <= hour or hour < 7:
            date = self._get_today()
            activities = self.data_store.get_activity_by_date(date)

            if 'night_owl' not in activities:
                activities['night_owl'] = 0

            activities['night_owl'] += 1

            return self.data_store.save_activity(date, activities)

        return True

    # ========== 统计查询 ==========

    def get_tool_usage_stats(self, days: int = 7) -> Dict[str, Dict]:
        """
        获取工具使用统计

        Args:
            days: 统计最近多少天

        Returns:
            工具使用统计数据
        """
        from datetime import timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        activities = self.data_store.get_activities_in_range(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        tool_stats = {}

        for date_data in activities.values():
            tools = date_data.get('tools', {})
            for tool_name, data in tools.items():
                if tool_name not in tool_stats:
                    tool_stats[tool_name] = {
                        'count': 0,
                        'success': 0,
                        'failure': 0,
                        'success_rate': 0.0
                    }

                tool_stats[tool_name]['count'] += data.get('count', 0)
                tool_stats[tool_name]['success'] += data.get('success', 0)
                tool_stats[tool_name]['failure'] += data.get('failure', 0)

        # 计算成功率
        for tool, stats in tool_stats.items():
            total = stats['success'] + stats['failure']
            if total > 0:
                stats['success_rate'] = round(stats['success'] / total * 100, 2)

        return tool_stats

    def get_skill_usage_stats(self, days: int = 7) -> Dict[str, int]:
        """
        获取技能使用统计

        Args:
            days: 统计最近多少天

        Returns:
            技能使用统计数据
        """
        from datetime import timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        activities = self.data_store.get_activities_in_range(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        skill_stats = {}

        for date_data in activities.values():
            skills = date_data.get('skills', {})
            for skill_name, count in skills.items():
                skill_stats[skill_name] = skill_stats.get(skill_name, 0) + count

        # 按使用次数排序
        return dict(sorted(skill_stats.items(), key=lambda x: x[1], reverse=True))

    def get_message_stats(self, days: int = 7) -> Dict[str, int]:
        """
        获取消息统计

        Args:
            days: 统计最近多少天

        Returns:
            消息统计数据
        """
        from datetime import timedelta

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        activities = self.data_store.get_activities_in_range(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        message_stats = {}

        for date_data in activities.values():
            messages = date_data.get('messages', {})
            for platform, count in messages.items():
                message_stats[platform] = message_stats.get(platform, 0) + count

        return message_stats

    def get_top_tools(self, limit: int = 5, days: int = 7) -> List[tuple]:
        """
        获取最常用的工具

        Args:
            limit: 返回数量
            days: 统计天数

        Returns:
            (工具名, 使用次数) 列表
        """
        tool_stats = self.get_tool_usage_stats(days)
        sorted_tools = sorted(
            tool_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        return [(name, stats['count']) for name, stats in sorted_tools[:limit]]

    def get_top_skills(self, limit: int = 5, days: int = 7) -> List[tuple]:
        """
        获取最常用的技能

        Args:
            limit: 返回数量
            days: 统计天数

        Returns:
            (技能名, 使用次数) 列表
        """
        skill_stats = self.get_skill_usage_stats(days)
        return list(skill_stats.items())[:limit]
