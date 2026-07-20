"""
数据可视化模块

提供 ASCII 风格的数据可视化
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta


class Visualizer:
    """数据可视化器"""

    @staticmethod
    def print_header(title: str, width: int = 60):
        """打印标题"""
        padding = (width - len(title) - 2) // 2
        print("=" * width)
        print(" " * padding + title + " " * padding)
        print("=" * width)
        print()

    @staticmethod
    def print_section(title: str):
        """打印章节标题"""
        print(f"\n{'─' * 60}")
        print(f"  {title}")
        print(f"{'─' * 60}\n")

    @staticmethod
    def format_number(num: int) -> str:
        """格式化数字"""
        if num >= 1000:
            return f"{num / 1000:.1f}k"
        return str(num)

    @staticmethod
    def create_bar_chart(data: Dict[str, int], width: int = 40, label_width: int = 15) -> str:
        """
        创建 ASCII 条形图

        Args:
            data: 数据字典 {标签: 值}
            width: 条形最大宽度
            label_width: 标签宽度

        Returns:
            条形图字符串
        """
        if not data:
            return "  暂无数据"

        max_value = max(data.values())
        output = []

        for label, value in sorted(data.items(), key=lambda x: x[1], reverse=True):
            bar_length = int((value / max_value) * width) if max_value > 0 else 0
            bar = "█" * bar_length
            output.append(f"  {label.ljust(label_width)} │ {bar} {value}")

        return "\n".join(output)

    @staticmethod
    def create_progress_bar(progress: float, width: int = 30, filled_char: str = "█", empty_char: str = "░") -> str:
        """
        创建进度条

        Args:
            progress: 进度（0-100）
            width: 进度条宽度
            filled_char: 已填充字符
            empty_char: 空字符

        Returns:
            进度条字符串
        """
        filled = int((progress / 100) * width)
        empty = width - filled
        return f"[{filled_char * filled}{empty_char * empty}] {progress:.1f}%"

    @staticmethod
    def create_table(headers: List[str], rows: List[List[str]], align: List[str] = None) -> str:
        """
        创建 ASCII 表格

        Args:
            headers: 表头列表
            rows: 行数据列表
            align: 对齐方式列表 ('left', 'right', 'center')

        Returns:
            表格字符串
        """
        if not rows:
            return "  暂无数据"

        # 计算每列宽度
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        # 设置默认对齐
        if align is None:
            align = ['left'] * len(headers)

        # 创建分隔线
        separator = "┼".join("─" * (w + 2) for w in col_widths)

        # 创建表头
        header_row = "│"
        for i, (header, width, al) in enumerate(zip(headers, col_widths, align)):
            if al == 'center':
                header_row += f" {header.center(width)} │"
            elif al == 'right':
                header_row += f" {header.rjust(width)} │"
            else:
                header_row += f" {header.ljust(width)} │"

        # 创建数据行
        data_rows = []
        for row in rows:
            data_row = "│"
            for i, (cell, width, al) in enumerate(zip(row, col_widths, align)):
                if al == 'center':
                    data_row += f" {str(cell).center(width)} │"
                elif al == 'right':
                    data_row += f" {str(cell).rjust(width)} │"
                else:
                    data_row += f" {str(cell).ljust(width)} │"
            data_rows.append(data_row)

        return f"┌{'─' * (len(separator) - 1)}┐\n{header_row}\n├{separator}┤\n" + \
               f"\n├{separator}┤\n".join(data_rows) + f"\n└{'─' * (len(separator) - 1)}┘"

    @staticmethod
    def visualize_achievements(unlocked: List[Dict], locked: List[Dict], stats: Dict):
        """可视化成就"""
        Visualizer.print_section("🏆 成就总览")

        # 统计
        print(f"  总成就: {stats['total']}  |  "
              f"已解锁: {stats['unlocked']}  |  "
              f"未解锁: {stats['locked']}")
        print(f"  完成度: {Visualizer.create_progress_bar(stats['completion_rate'])}\n")

        # 按分类统计
        print("  📊 分类统计:")
        for category, cat_stats in stats['category_stats'].items():
            completion = cat_stats['unlocked'] / cat_stats['total'] * 100 if cat_stats['total'] > 0 else 0
            print(f"    {category}: {cat_stats['unlocked']}/{cat_stats['total']} "
                  f"{Visualizer.create_progress_bar(completion, 20)}")

        # 最近解锁
        if unlocked:
            Visualizer.print_section("🎉 最近解锁")
            for achievement in unlocked[:5]:
                rarity_color = {
                    'common': '⚪',
                    'rare': '🔵',
                    'epic': '🟣',
                    'legendary': '🟡'
                }.get(achievement['rarity'], '⚪')

                unlock_time = achievement.get('unlock_time', '')
                if unlock_time:
                    time_str = datetime.fromisoformat(unlock_time).strftime("%Y-%m-%d %H:%M")
                else:
                    time_str = "未知"

                print(f"  {achievement['icon']} {achievement['name']}")
                print(f"    {achievement['description']}")
                print(f"    {rarity_color} {achievement['rarity'].upper()} • 解锁于 {time_str}\n")

        # 未解锁（最近5个）
        if locked:
            Visualizer.print_section("🔒 待解锁成就 (Top 5)")
            for achievement in locked[:5]:
                print(f"  {achievement['icon']} {achievement['name']}")
                print(f"    {achievement['description']}\n")

    @staticmethod
    def visualize_activity(tool_stats: Dict, skill_stats: Dict, message_stats: Dict):
        """可视化活动统计"""
        Visualizer.print_section("📊 活动统计")

        # 工具使用
        if tool_stats:
            print("  🛠️  工具使用 (Top 10)")
            top_tools = dict(sorted(tool_stats.items(),
                                   key=lambda x: x[1]['count'],
                                   reverse=True)[:10])

            for tool, stats in top_tools.items():
                success_rate = stats['success_rate']
                print(f"    {tool}: {stats['count']} 次 "
                      f"(成功率: {success_rate}%)")

        # 技能使用
        if skill_stats:
            print("\n  ⚡ 技能使用 (Top 10)")
            for i, (skill, count) in enumerate(list(skill_stats.items())[:10], 1):
                print(f"    {i:2d}. {skill}: {count} 次")

        # 消息统计
        if message_stats:
            print("\n  💬 消息统计 (按平台)")
            for platform, count in message_stats.items():
                print(f"    {platform}: {count} 条")

    @staticmethod
    def visualize_metrics(metrics: Dict, streak_info: Dict):
        """可视化效率指标"""
        Visualizer.print_section("📈 效率指标")

        # 连续使用天数
        current = streak_info.get('current', 0)
        longest = streak_info.get('longest', 0)

        print(f"  🔥 连续使用天数: {current} 天")
        print(f"     最长记录: {longest} 天\n")

        # 时间节省
        time_saved = metrics.get('time_saved_minutes', 0)
        if time_saved >= 60:
            print(f"  ⏱️  累计节省时间: {time_saved // 60} 小时 {time_saved % 60} 分钟")
        else:
            print(f"  ⏱️  累计节省时间: {time_saved} 分钟")

        # 问题解决
        problems_solved = metrics.get('problems_solved', 0)
        print(f"  ✅ 解决问题数: {problems_solved}")

        # 子代理统计
        subagent_created = metrics.get('subagent_created', 0)
        subagent_completed = metrics.get('subagent_completed', 0)
        print(f"  🤖 子代理创建: {subagent_created} | 完成: {subagent_completed}")

    @staticmethod
    def visualize_workflow(workflow_stats: Dict):
        """可视化工作流统计"""
        Visualizer.print_section("🔄 工作流统计")

        print(f"  总完成数: {workflow_stats['total_completions']}")
        print(f"  Cron 执行: {workflow_stats['total_cron_runs']}\n")

        # 最常用工作流
        if workflow_stats['top_workflows']:
            print("  📋 最常用工作流:")
            headers = ["工作流", "完成次数", "Cron", "最后使用"]
            rows = []
            for wf_id, stats in workflow_stats['top_workflows'][:5]:
                last_used = stats['last_used']
                if last_used:
                    last_used_str = datetime.fromisoformat(last_used).strftime("%Y-%m-%d")
                else:
                    last_used_str = "从未"
                rows.append([
                    stats['name'],
                    stats['completions'],
                    stats['cron_runs'],
                    last_used_str
                ])

            print(Visualizer.create_table(headers, rows))

    @staticmethod
    def show_dashboard(system):
        """显示完整仪表板"""
        print("\n" * 2)
        Visualizer.print_header("🏆 Clawdbot 成就系统仪表板", 60)

        # 获取数据
        streak_info = system.data_store.get_streak_info()
        tool_stats = system.activity_tracker.get_tool_usage_stats()
        skill_stats = system.activity_tracker.get_skill_usage_stats()
        message_stats = system.activity_tracker.get_message_stats()
        metrics = system.data_store.get_metrics()
        workflow_stats = system.workflow_tracker.get_workflow_stats()
        achievement_stats = system.achievement_engine.get_achievement_stats()
        unlocked = system.achievement_engine.get_unlocked_achievements()
        locked = system.achievement_engine.get_locked_achievements()

        # 显示各部分
        Visualizer.visualize_achievements(unlocked, locked, achievement_stats)
        Visualizer.visualize_activity(tool_stats, skill_stats, message_stats)
        Visualizer.visualize_metrics(metrics, streak_info)
        Visualizer.visualize_workflow(workflow_stats)

        print(f"\n{'=' * 60}")
        print("  数据更新时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(f"{'=' * 60}\n")
