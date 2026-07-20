#!/usr/bin/env python3
"""
Clawdbot 终端成就系统 - 主入口

这是一个用于追踪和激励 Clawdbot 使用情况的成就系统工具。
"""

import argparse
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

# 修复导入问题：使用绝对导入
from achievement_system import AchievementSystem

def main():
    parser = argparse.ArgumentParser(
        description="Clawdbot 终端成就系统 - 追踪和激励使用情况",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s status                    # 查看当前状态
  %(prog)s list                      # 列出所有成就
  %(prog)s track --tool read         # 记录工具使用
  %(prog)s track --skill coding      # 记录技能使用
  %(prog)s export --format json      # 导出数据
  %(prog)s visualize                 # 显示可视化统计
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 状态命令
    status_parser = subparsers.add_parser("status", help="查看当前状态")
    status_parser.add_argument("--detailed", "-d", action="store_true", help="显示详细信息")

    # 成就列表命令
    list_parser = subparsers.add_parser("list", help="列出所有成就")
    list_parser.add_argument("--unlocked", "-u", action="store_true", help="只显示已解锁")
    list_parser.add_argument("--locked", "-l", action="store_true", help="只显示未解锁")

    # 追踪命令
    track_parser = subparsers.add_parser("track", help="记录活动")
    track_parser.add_argument("--tool", "-t", help="记录工具使用")
    track_parser.add_argument("--skill", "-s", help="记录技能使用")
    track_parser.add_argument("--workflow", "-w", help="记录工作流完成")
    track_parser.add_argument("--message", "-m", type=int, help="记录消息数量")
    track_parser.add_argument("--platform", "-p", help="平台名称 (slack/telegram/feishu)")
    track_parser.add_argument("--success", action="store_true", help="标记为成功")

    # 工作流命令
    workflow_parser = subparsers.add_parser("workflow", help="工作流相关操作")
    workflow_parser.add_argument("--start", "-s", help="启动工作流")
    workflow_parser.add_argument("--complete", "-c", help="完成工作流")
    workflow_parser.add_argument("--name", "-n", help="工作流名称")

    # 导出命令
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("--format", "-f", choices=["json", "csv"], default="json", help="导出格式")
    export_parser.add_argument("--output", "-o", help="输出文件路径")

    # 可视化命令
    viz_parser = subparsers.add_parser("visualize", help="显示可视化统计")
    viz_parser.add_argument("--type", "-t", choices=["all", "activity", "achievements", "metrics"],
                           default="all", help="可视化类型")
    viz_parser.add_argument("--days", "-d", type=int, default=7, help="显示最近N天的数据")

    # 重置命令
    reset_parser = subparsers.add_parser("reset", help="重置数据")
    reset_parser.add_argument("--all", action="store_true", help="重置所有数据")
    reset_parser.add_argument("--achievements", action="store_true", help="重置成就")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # 初始化成就系统
    system = AchievementSystem()

    try:
        if args.command == "status":
            system.show_status(detailed=args.detailed)

        elif args.command == "list":
            system.list_achievements(unlocked_only=args.unlocked, locked_only=args.locked)

        elif args.command == "track":
            if args.tool:
                system.track_tool_usage(args.tool, success=args.success)
            if args.skill:
                system.track_skill_usage(args.skill)
            if args.workflow:
                system.track_workflow_completion(args.workflow)
            if args.message:
                system.track_message_count(args.message, platform=args.platform)

        elif args.command == "workflow":
            if args.start:
                system.workflow_tracker.start_workflow(args.start, args.name)
            if args.complete:
                system.workflow_tracker.complete_workflow(args.complete)

        elif args.command == "export":
            system.export_data(format=args.format, output_path=args.output)

        elif args.command == "visualize":
            system.visualize(view_type=args.type, days=args.days)

        elif args.command == "reset":
            if args.all:
                confirm = input("确定要重置所有数据吗？(yes/no): ")
                if confirm.lower() == "yes":
                    system.reset_all()
                    print("✓ 所有数据已重置")
            elif args.achievements:
                system.reset_achievements()
                print("✓ 成就已重置")

        return 0

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
