#!/usr/bin/env python3
"""
成就系统测试脚本
验证核心功能是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from achievement_system import AchievementSystem


def test_basic_tracking():
    """测试基础追踪功能"""
    print("测试 1: 基础追踪功能... ", end="")

    system = AchievementSystem()

    # 记录工具使用
    system.track_tool_usage('read', success=True)
    system.track_tool_usage('write', success=True)

    # 记录技能使用
    system.track_skill_usage('coding')

    # 记录消息
    system.track_message_count(5, platform='slack')

    print("✓ 通过")
    return True


def test_workflow_tracking():
    """测试工作流追踪"""
    print("测试 2: 工作流追踪... ", end="")

    system = AchievementSystem()

    workflow_id = system.workflow_tracker.start_workflow('test', '测试工作流')
    system.workflow_tracker.complete_workflow(workflow_id)

    print("✓ 通过")
    return True


def test_achievement_detection():
    """测试成就检测"""
    print("测试 3: 成就检测... ", end="")

    system = AchievementSystem()

    # 重置成就以便测试
    system.reset_achievements()

    # 记录一些活动以触发成就
    for i in range(5):
        system.track_tool_usage('test_tool', success=True)

    # 检查成就
    newly_unlocked = system.achievement_engine.check_achievements()

    # 预期至少解锁 "初次接触" 成就
    stats = system.achievement_engine.get_achievement_stats()
    assert stats['unlocked'] >= 1, "应该至少解锁一个成就"

    print("✓ 通过")
    return True


def test_data_persistence():
    """测试数据持久化"""
    print("测试 4: 数据持久化... ", end="")

    system = AchievementSystem()

    # 记录数据
    system.track_tool_usage('persistent_test', success=True)
    system.track_skill_usage('persistent_skill')

    # 创建新实例，验证数据是否持久化
    system2 = AchievementSystem()
    activities = system2.data_store.get_activities()

    # 验证数据存在
    today = Path(system.data_store.activities_file).read_text()
    assert 'persistent_test' in today, "工具数据未持久化"

    print("✓ 通过")
    return True


def test_export_data():
    """测试数据导出"""
    print("测试 5: 数据导出... ", end="")

    system = AchievementSystem()

    # 导出 JSON
    json_data = system.data_store.export_all_data()
    assert 'activities' in json_data, "导出数据缺少 activities"
    assert 'achievements' in json_data, "导出数据缺少 achievements"

    # 导出 CSV
    csv_data = system.data_store.export_csv("activities")
    assert 'Date' in csv_data, "CSV 数据格式错误"

    print("✓ 通过")
    return True


def test_statistics():
    """测试统计功能"""
    print("测试 6: 统计功能... ", end="")

    system = AchievementSystem()

    # 添加一些数据
    for tool in ['read', 'write', 'exec']:
        for i in range(3):
            system.track_tool_usage(tool, success=True)

    # 获取统计
    tool_stats = system.activity_tracker.get_tool_usage_stats(7)
    assert 'read' in tool_stats, "缺少工具统计"

    skill_stats = system.activity_tracker.get_skill_usage_stats(7)
    # 可能为空，不需要断言

    message_stats = system.activity_tracker.get_message_stats(7)
    # 可能为空，不需要断言

    print("✓ 通过")
    return True


def test_achievement_categories():
    """测试成就分类"""
    print("测试 7: 成就分类... ", end="")

    system = AchievementSystem()

    # 检查各分类成就是否存在
    categories = ['first_time', 'streak', 'milestone', 'skill', 'workflow',
                  'efficiency', 'personal', 'night_owl']

    for category in categories:
        achievements = system.achievement_engine.get_achievements_by_category(
            eval(f"AchievementCategory.{category.upper()}")
            if category != 'first_time' else AchievementCategory.FIRST_TIME
        )
        # 某些分类可能为空，这是正常的

    print("✓ 通过")
    return True


def test_visualization():
    """测试可视化"""
    print("测试 8: 可视化功能... ", end="")

    system = AchievementSystem()

    # 测试可视化不会抛出异常
    try:
        system.visualize(view_type="all", days=7)
        system.show_status(detailed=True)
    except Exception as e:
        print(f"\n错误: {e}")
        return False

    print("✓ 通过")
    return True


def test_reset_functionality():
    """测试重置功能"""
    print("测试 9: 重置功能... ", end="")

    system = AchievementSystem()

    # 记录一些数据
    system.track_tool_usage('reset_test', success=True)

    # 重置成就
    system.reset_achievements()

    # 验证成就已重置
    achievements = system.achievement_engine.get_achievements()
    for aid, data in achievements.items():
        assert not data.get('unlocked', False), f"成就 {aid} 未被重置"

    print("✓ 通过")
    return True


def test_error_handling():
    """测试错误处理"""
    print("测试 10: 错误处理... ", end="")

    system = AchievementSystem()

    # 测试无效操作不会崩溃
    try:
        # 检查不存在的成就
        result = system.achievement_engine.check_specific_achievement('non_existent')
        assert result == False, "应该返回 False"

        # 记空消息
        system.track_message_count(0, platform='test')

        # 不存在的 workflow
        system.workflow_tracker.complete_workflow('non_existent')

    except Exception as e:
        print(f"\n错误: {e}")
        return False

    print("✓ 通过")
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("成就系统功能测试")
    print("=" * 60 + "\n")

    from achievements.definitions import AchievementCategory

    tests = [
        test_basic_tracking,
        test_workflow_tracking,
        test_achievement_detection,
        test_data_persistence,
        test_export_data,
        test_statistics,
        test_achievement_categories,
        test_visualization,
        test_reset_functionality,
        test_error_handling,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"✗ 失败")
        except Exception as e:
            failed += 1
            print(f"✗ 异常: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60 + "\n")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
