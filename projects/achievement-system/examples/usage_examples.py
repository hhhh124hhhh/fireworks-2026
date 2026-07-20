"""
成就系统使用示例

展示如何在不同的场景中使用成就系统
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from achievement_system import AchievementSystem


def example_1_basic_usage():
    """示例 1：基础使用"""
    print("=" * 60)
    print("示例 1：基础使用")
    print("=" * 60)

    # 初始化成就系统
    system = AchievementSystem()

    # 记录工具使用
    system.track_tool_usage('read', success=True)
    system.track_tool_usage('write', success=True)
    system.track_tool_usage('exec', success=False)  # 失败的调用

    # 记录技能使用
    system.track_skill_usage('coding')
    system.track_skill_usage('search')

    # 记录消息处理
    system.track_message_count(10, platform='slack')

    # 显示状态
    system.show_status(detailed=True)


def example_2_workflow_tracking():
    """示例 2：工作流追踪"""
    print("=" * 60)
    print("示例 2：工作流追踪")
    print("=" * 60)

    system = AchievementSystem()

    # 启动工作流
    workflow_id = system.workflow_tracker.start_workflow('automation', '自动备份')

    # 记录时间节省
    system.workflow_tracker.record_time_saved(30)  # 节省 30 分钟

    # 记录问题解决
    system.workflow_tracker.record_problem_solved()

    # 完成工作流
    system.workflow_tracker.complete_workflow(workflow_id)

    print(f"✓ 工作流 {workflow_id} 已完成")
    print(f"✓ 累计节省时间: {system.data_store.get_metrics().get('time_saved_minutes', 0)} 分钟")
    print(f"✓ 解决问题数: {system.data_store.get_metrics().get('problems_solved', 0)}")


def example_3_cron_task():
    """示例 3：Cron 任务追踪"""
    print("=" * 60)
    print("示例 3：Cron 任务追踪")
    print("=" * 60)

    system = AchievementSystem()

    # 模拟 cron 任务执行
    cron_task = 'daily_backup'
    system.workflow_tracker.track_cron_execution(cron_task)

    # 记录工具使用（cron 内部）
    system.track_tool_usage('exec', success=True)

    print(f"✓ Cron 任务 {cron_task} 已记录")


def example_4_custom_metrics():
    """示例 4：自定义指标"""
    print("=" * 60)
    print("示例 4：自定义指标")
    print("=" * 60)

    system = AchievementSystem()

    # 更新自定义指标
    system.data_store.update_metric('custom_metric', 100)
    system.data_store.increment_metric('counter_metric', 5)

    # 读取指标
    metrics = system.data_store.get_metrics()
    print(f"自定义指标: {metrics.get('custom_metric')}")
    print(f"计数指标: {metrics.get('counter_metric')}")


def example_5_achievement_check():
    """示例 5：手动检查成就"""
    print("=" * 60)
    print("示例 5：手动检查成就")
    print("=" * 60)

    system = AchievementSystem()

    # 记录一些活动
    for i in range(5):
        system.track_tool_usage('read', success=True)

    # 检查成就
    newly_unlocked = system.achievement_engine.check_achievements()

    if newly_unlocked:
        print(f"🎉 新解锁的成就: {newly_unlocked}")
        for aid in newly_unlocked:
            achievement = system.achievement_engine.data_store.get_achievements()[aid]
            print(f"  - {achievement['icon']} {achievement['name']}: {achievement['description']}")
    else:
        print("没有新成就解锁")


def example_6_visualization():
    """示例 6：可视化统计"""
    print("=" * 60)
    print("示例 6：可视化统计")
    print("=" * 60)

    system = AchievementSystem()

    # 显示可视化
    system.visualize(view_type="all", days=7)


def example_7_export_data():
    """示例 7：数据导出"""
    print("=" * 60)
    print("示例 7：数据导出")
    print("=" * 60)

    system = AchievementSystem()

    # 导出 JSON 数据到文件
    output_file = system.base_dir / "export_example.json"
    system.export_data(format="json", output_path=str(output_file))

    print(f"✓ 数据已导出到: {output_file}")

    # 导出 CSV 数据
    csv_data = system.data_store.export_csv("activities")
    print("\n前 10 行 CSV 数据:")
    print('\n'.join(csv_data.split('\n')[:10]))


def example_8_batch_recording():
    """示例 8：批量记录"""
    print("=" * 60)
    print("示例 8：批量记录")
    print("=" * 60)

    system = AchievementSystem()

    # 模拟一天的活动
    tools = ['read', 'write', 'exec', 'coding-agent', 'search']
    skills = ['coding', 'search', 'deploy']

    # 批量记录工具使用
    for tool in tools:
        for _ in range(3):
            system.track_tool_usage(tool, success=True)

    # 批量记录技能使用
    for skill in skills:
        for _ in range(5):
            system.track_skill_usage(skill)

    print("✓ 已批量记录活动")

    # 查看统计
    system.show_status(detailed=True)


def example_9_session_tracking():
    """示例 9：会话追踪"""
    print("=" * 60)
    print("示例 9：会话追踪")
    print("=" * 60)

    system = AchievementSystem()

    # 开始会话
    system.activity_tracker.track_session_start('coding_session')

    # 会话中的活动
    system.track_tool_usage('read', success=True)
    system.track_tool_usage('coding-agent', success=True)
    system.track_skill_usage('coding')

    # 结束会话（检查成就）
    newly_unlocked = system.achievement_engine.check_achievements()

    print(f"✓ 会话已记录")
    if newly_unlocked:
        print(f"🎉 解锁新成就: {len(newly_unlocked)} 个")


def example_10_subagent_tracking():
    """示例 10：子代理追踪"""
    print("=" * 60)
    print("示例 10：子代理追踪")
    print("=" * 60)

    system = AchievementSystem()

    # 创建子代理
    system.workflow_tracker.track_subagent_task(created=True)

    # 子代理完成任务
    system.workflow_tracker.track_subagent_task(completed=True)

    # 查看指标
    metrics = system.data_store.get_metrics()
    print(f"✓ 子代理创建数: {metrics.get('subagent_created', 0)}")
    print(f"✓ 子代理完成数: {metrics.get('subagent_completed', 0)}")


def main():
    """运行所有示例"""
    examples = [
        ("基础使用", example_1_basic_usage),
        ("工作流追踪", example_2_workflow_tracking),
        ("Cron 任务追踪", example_3_cron_task),
        ("自定义指标", example_4_custom_metrics),
        ("手动检查成就", example_5_achievement_check),
        ("可视化统计", example_6_visualization),
        ("数据导出", example_7_export_data),
        ("批量记录", example_8_batch_recording),
        ("会话追踪", example_9_session_tracking),
        ("子代理追踪", example_10_subagent_tracking),
    ]

    print("\n" + "=" * 60)
    print("成就系统使用示例")
    print("=" * 60 + "\n")

    for name, func in examples:
        try:
            func()
            print()
            input("按 Enter 继续...")
            print()
        except KeyboardInterrupt:
            print("\n\n示例已中断")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
