"""
成就系统集成模块

整合所有子模块，提供统一的高层接口
"""

from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

from data_store import DataStore
from activity_tracker import ActivityTracker
from achievement_engine import AchievementEngine


class AchievementSystem:
    """成就系统主类"""

    def __init__(self, base_dir: Optional[Path] = None):
        """
        初始化成就系统

        Args:
            base_dir: 数据存储基础目录
        """
        # 初始化数据存储
        self.data_store = DataStore(base_dir=base_dir)

        # 初始化活动追踪器
        self.activity_tracker = ActivityTracker(data_store=self.data_store)

        # 初始化成就引擎
        self.achievement_engine = AchievementEngine(data_store=self.data_store)

        # 工作流追踪器
        self.workflow_tracker = WorkflowTracker(data_store=self.data_store)

    # ========== 工具追踪 ==========

    def track_tool_usage(self, tool_name: str, success: bool = True):
        """
        记录工具使用

        Args:
            tool_name: 工具名称
            success: 是否成功
        """
        self.activity_tracker.track_tool_usage(tool_name, success=success)

        # 检查成就
        self.achievement_engine.check_achievements()

    # ========== 技能追踪 ==========

    def track_skill_usage(self, skill_name: str):
        """
        记录技能使用

        Args:
            skill_name: 技能名称
        """
        self.activity_tracker.track_skill_usage(skill_name)

        # 检查成就
        self.achievement_engine.check_achievements()

    # ========== 工作流追踪 ==========

    def track_workflow_completion(self, workflow_name: str):
        """
        记录工作流完成

        Args:
            workflow_name: 工作流名称
        """
        self.workflow_tracker.complete_workflow(workflow_name)

        # 检查成就
        self.achievement_engine.check_achievements()

    # ========== 消息追踪 ==========

    def track_message_count(self, count: int, platform: str = "unknown"):
        """
        记录消息数量

        Args:
            count: 消息数量
            platform: 平台名称
        """
        self.activity_tracker.track_message_count(count, platform=platform)

        # 检查成就
        self.achievement_engine.check_achievements()

    # ========== 状态查询 ==========

    def show_status(self, detailed: bool = False):
        """
        显示当前状态

        Args:
            detailed: 是否显示详细信息
        """
        print("\n" + "="*60)
        print("🏆 Clawdbot 成就系统 - 状态概览")
        print("="*60)

        # 获取成就统计
        stats = self.achievement_engine.get_achievement_stats()

        print(f"\n📊 成就进度: {stats['unlocked']}/{stats['total']} ({stats['completion_rate']}%)")

        # 获取连续使用天数
        streak = self.data_store.get_streak_info()
        print(f"🔥 连续使用: {streak['current']} 天 (最长: {streak['longest']} 天)")

        # 获取今日活动
        today = datetime.now().strftime("%Y-%m-%d")
        today_activity = self.data_store.get_activity_by_date(today)

        if detailed:
            print("\n" + "-"*60)
            print("📈 今日活动详情:")
            print("-"*60)

            # 工具使用
            tools = today_activity.get('tools', {})
            if tools:
                print("\n🛠️ 工具使用:")
                for tool, data in tools.items():
                    print(f"  - {tool}: {data['count']} 次 (成功率: {data.get('success',0)}/{data.get('count',0)})")

            # 技能使用
            skills = today_activity.get('skills', {})
            if skills:
                print("\n⚡ 技能使用:")
                for skill, count in skills.items():
                    print(f"  - {skill}: {count} 次")

            # 消息处理
            messages = today_activity.get('messages', {})
            if messages:
                print("\n💬 消息处理:")
                for platform, count in messages.items():
                    print(f"  - {platform}: {count} 条")

            # 最近解锁的成就
            unlocked = self.achievement_engine.get_unlocked_achievements()
            if unlocked:
                print("\n✨ 最近解锁的成就:")
                for achievement in unlocked[:5]:
                    print(f"  - {achievement['icon']} {achievement['name']}: {achievement['description']}")
                    print(f"    解锁时间: {achievement['unlock_time'][:19]}")

        print("\n" + "="*60 + "\n")

    # ========== 成就列表 ==========

    def list_achievements(self, unlocked_only: bool = False, locked_only: bool = False):
        """
        列出成就

        Args:
            unlocked_only: 只显示已解锁
            locked_only: 只显示未解锁
        """
        if unlocked_only:
            achievements = self.achievement_engine.get_unlocked_achievements()
            title = "已解锁成就"
        elif locked_only:
            achievements = self.achievement_engine.get_locked_achievements()
            title = "未解锁成就"
        else:
            unlocked = self.achievement_engine.get_unlocked_achievements()
            locked = self.achievement_engine.get_locked_achievements()
            achievements = unlocked + locked
            title = "所有成就"

        print(f"\n{'='*60}")
        print(f"🏆 {title}")
        print(f"{'='*60}\n")

        if not achievements:
            print("暂无成就\n")
            return

        # 按分类分组
        from achievements.definitions import AchievementCategory

        by_category = {}
        for achievement in achievements:
            category = achievement.get('category', 'unknown')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(achievement)

        # 显示各分类
        category_names = {
            'first_time': '🎯 首次使用',
            'streak': '🔥 连续使用',
            'milestone': '📈 里程碑',
            'skill': '💪 技能大师',
            'workflow': '🔄 工作流专家',
            'efficiency': '⚡ 效率达人',
            'personal': '🎨 个性化',
            'night_owl': '🦉 夜猫子'
        }

        for category, achievements_list in by_category.items():
            cat_name = category_names.get(category, f'📁 {category}')
            print(f"\n{cat_name}")

            for achievement in achievements_list:
                unlocked = achievement.get('unlocked', False)
                status = "✅" if unlocked else "🔒"
                icon = achievement.get('icon', '🏆')
                rarity = achievement.get('rarity', 'common')
                name = achievement.get('name', 'Unknown')
                description = achievement.get('description', '')

                # 稀有度标记
                rarity_marks = {
                    'legendary': '⭐⭐⭐',
                    'epic': '⭐⭐',
                    'rare': '⭐',
                    'common': ''
                }
                rarity_mark = rarity_marks.get(rarity, '')

                print(f"\n  {status} {icon} {name} {rarity_mark}")
                print(f"      {description}")

                if unlocked and achievement.get('unlock_time'):
                    print(f"      解锁时间: {achievement['unlock_time'][:19]}")

        print("\n" + "="*60 + "\n")

    # ========== 数据导出 ==========

    def export_data(self, format: str = "json", output_path: Optional[str] = None):
        """
        导出数据

        Args:
            format: 导出格式 (json/csv)
            output_path: 输出文件路径
        """
        if format == "json":
            data = self.data_store.export_all_data()

            if output_path:
                import json
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"✓ 数据已导出到: {output_path}")
            else:
                import json
                print(json.dumps(data, indent=2, ensure_ascii=False))

        elif format == "csv":
            csv_data = self.data_store.export_csv("activities")

            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(csv_data)
                print(f"✓ 数据已导出到: {output_path}")
            else:
                print(csv_data)

    # ========== 可视化 ==========

    def visualize(self, view_type: str = "all", days: int = 7):
        """
        显示可视化统计

        Args:
            view_type: 可视化类型 (all/activity/achievements/metrics)
            days: 显示最近多少天
        """
        from datetime import timedelta

        if view_type in ["all", "activity"]:
            print("\n" + "="*60)
            print("📊 活动统计 (最近{}天)".format(days))
            print("="*60)

            # 工具使用统计
            tool_stats = self.activity_tracker.get_tool_usage_stats(days)
            if tool_stats:
                print("\n🛠️ 工具使用 TOP 5:")
                for i, (tool, stats) in enumerate(list(tool_stats.items())[:5], 1):
                    print(f"  {i}. {tool}: {stats['count']} 次")
            else:
                print("\n🛠️ 暂无工具使用记录")

            # 技能使用统计
            skill_stats = self.activity_tracker.get_skill_usage_stats(days)
            if skill_stats:
                print("\n⚡ 技能使用 TOP 5:")
                for i, (skill, count) in enumerate(list(skill_stats.items())[:5], 1):
                    print(f"  {i}. {skill}: {count} 次")
            else:
                print("\n⚡ 暂无技能使用记录")

            # 消息统计
            message_stats = self.activity_tracker.get_message_stats(days)
            if message_stats:
                print("\n💬 消息统计:")
                for platform, count in message_stats.items():
                    print(f"  - {platform}: {count} 条")
            else:
                print("\n💬 暂无消息记录")

        if view_type in ["all", "achievements"]:
            print("\n" + "="*60)
            print("🏆 成就统计")
            print("="*60)

            stats = self.achievement_engine.get_achievement_stats()
            print(f"\n总进度: {stats['unlocked']}/{stats['total']} ({stats['completion_rate']}%)")

            # 按稀有度统计
            rarity_stats = stats.get('rarity_stats', {})
            if rarity_stats:
                print("\n按稀有度:")
                rarity_names = {'legendary': '🌟 传说', 'epic': '💎 史诗',
                               'rare': '💠 稀有', 'common': '🏅 普通'}
                for rarity, data in rarity_stats.items():
                    name = rarity_names.get(rarity, rarity)
                    print(f"  - {name}: {data['unlocked']}/{data['total']}")

            # 按分类统计
            category_stats = stats.get('category_stats', {})
            if category_stats:
                print("\n按分类:")
                category_names = {
                    'first_time': '首次使用',
                    'streak': '连续使用',
                    'milestone': '里程碑',
                    'skill': '技能大师',
                    'workflow': '工作流专家',
                    'efficiency': '效率达人',
                    'personal': '个性化',
                    'night_owl': '夜猫子'
                }
                for category, data in category_stats.items():
                    name = category_names.get(category, category)
                    print(f"  - {name}: {data['unlocked']}/{data['total']}")

        print("\n" + "="*60 + "\n")

    # ========== 重置功能 ==========

    def reset_all(self):
        """重置所有数据"""
        self.data_store._init_files()

    def reset_achievements(self):
        """重置成就"""
        self.data_store.reset_achievements()


class WorkflowTracker:
    """工作流追踪器"""

    def __init__(self, data_store: DataStore):
        """
        初始化工作流追踪器

        Args:
            data_store: 数据存储实例
        """
        self.data_store = data_store

    def start_workflow(self, workflow_id: str, name: Optional[str] = None):
        """
        开始工作流

        Args:
            workflow_id: 工作流ID
            name: 工作流名称
        """
        workflows = self.data_store.get_workflows()

        if workflow_id not in workflows:
            workflows[workflow_id] = {
                'name': name or workflow_id,
                'start_time': None,
                'completion_count': 0,
                'cron_runs': 0,
                'last_run': None
            }

        workflows[workflow_id]['start_time'] = datetime.now().isoformat()
        self.data_store.save_workflow(workflow_id, workflows[workflow_id])

    def complete_workflow(self, workflow_id: str):
        """
        完成工作流

        Args:
            workflow_id: 工作流ID
        """
        workflows = self.data_store.get_workflows()

        if workflow_id not in workflows:
            workflows[workflow_id] = {
                'name': workflow_id,
                'start_time': None,
                'completion_count': 0,
                'cron_runs': 0,
                'last_run': None
            }

        workflows[workflow_id]['completion_count'] = \
            workflows[workflow_id].get('completion_count', 0) + 1
        workflows[workflow_id]['last_run'] = datetime.now().isoformat()
        self.data_store.save_workflow(workflow_id, workflows[workflow_id])
