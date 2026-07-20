#!/usr/bin/env python3
"""
Momo Preference Recorder
记录用户偏好和对话习惯
"""

import json
import os
from datetime import datetime

# 数据目录
DATA_DIR = "/root/clawd/skills/momo-personality/data"
RECORDS_DIR = "/root/clawd/skills/momo-personality/records"

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RECORDS_DIR, exist_ok=True)

# 偏好文件路径
PREFERENCES_FILE = os.path.join(DATA_DIR, "preferences.json")
CONVERSATION_LOG = os.path.join(RECORDS_DIR, "conversation_log.json")


def load_preferences():
    """加载用户偏好"""
    if os.path.exists(PREFERENCES_FILE):
        with open(PREFERENCES_FILE, 'r', encoding='utf-8') as fi:
            return json.load(fi)
    return {}


def save_preferences(preferences):
    """保存用户偏好"""
    with open(PREFERENCES_FILE, 'w', encoding='utf-8') as fo:
        json.dump(preferences, fo, ensure_ascii=False, indent=2)


def record_preference(category, preference):
    """记录用户偏好"""
    preferences = load_preferences()

    if category not in preferences:
        preferences[category] = []

    if preference not in preferences[category]:
        preferences[category].append(preference)

    # 添加时间戳
    preferences[f"{category}_updated"] = datetime.now().isoformat()

    save_preferences(preferences)
    print(f"已记录偏好: {category} = {preference}")


def get_preferences(category=None):
    """获取用户偏好"""
    preferences = load_preferences()

    if category:
        return preferences.get(category, [])
    return preferences


def record_conversation(topic, mood, style):
    """记录对话"""
    log = []

    if os.path.exists(CONVERSATION_LOG):
        with open(CONVERSATION_LOG, 'r', encoding='utf-8') as fi:
            log = json.load(fi)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "mood": mood,
        "style": style
    }

    log.append(entry)

    # 只保留最近 100 条记录
    if len(log) > 100:
        log = log[-100:]

    with open(CONVERSATION_LOG, 'w', encoding='utf-8') as fo:
        json.dump(log, fo, ensure_ascii=False, indent=2)

    print(f"已记录对话: {topic} ({mood}, {style})")


def get_conversation_stats():
    """获取对话统计"""
    if not os.path.exists(CONVERSATION_LOG):
        return {}

    with open(CONVERSATION_LOG, 'r', encoding='utf-8') as fi:
        log = json.load(fi)

    stats = {
        "total_conversations": len(log),
        "topics": {},
        "moods": {},
        "styles": {}
    }

    for entry in log:
        topic = entry.get("topic", "unknown")
        mood = entry.get("mood", "unknown")
        style = entry.get("style", "unknown")

        stats["topics"][topic] = stats["topics"].get(topic, 0) + 1
        stats["moods"][mood] = stats["moods"].get(mood, 0) + 1
        stats["styles"][style] = stats["styles"].get(style, 0) + 1

    return stats


def main():
    """主函数 - 命令行使用"""
    import sys

    if len(sys.argv) < 2:
        # 显示帮助
        print("=== Momo Preference Recorder ===")
        print("\n使用方法:")
        print("  记录偏好: python3 preference_record.py record <category> <preference>")
        print("  查看偏好: python3 preference_record.py show [category]")
        print("  记录对话: python3 preference_record.py log <topic> <mood> <style>")
        print("  查看统计: python3 preference_record.py stats")
        print("\n示例:")
        print("  python3 preference_record.py record style 简洁技术回答")
        print("  python3 preference_record.py show style")
        print("  python3 preference_record.py log 技术问题 认真 专业")
        print("  python3 preference_record.py stats")
        sys.exit(0)

    command = sys.argv[1]

    if command == "record":
        if len(sys.argv) < 4:
            print("用法: python3 preference_record.py record <category> <preference>", file=sys.stderr)
            sys.exit(1)

        category = sys.argv[2]
        preference = " ".join(sys.argv[3:])
        record_preference(category, preference)

    elif command == "show":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        preferences = get_preferences(category)

        if category:
            print(f"\n偏好类别: {category}")
            for pref in preferences:
                print(f"  - {pref}")
        else:
            print(f"\n所有偏好:")
            for key, value in preferences.items():
                if not key.endswith("_updated"):
                    print(f"  {key}: {value}")

    elif command == "log":
        if len(sys.argv) < 5:
            print("用法: python3 preference_record.py log <topic> <mood> <style>", file=sys.stderr)
            sys.exit(1)

        topic = sys.argv[2]
        mood = sys.argv[3]
        style = sys.argv[4]
        record_conversation(topic, mood, style)

    elif command == "stats":
        stats = get_conversation_stats()

        print("\n=== 对话统计 ===")
        print(f"总对话数: {stats['total_conversations']}")

        print("\n话题分布:")
        for topic, count in sorted(stats["topics"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {topic}: {count}")

        print("\n情绪分布:")
        for mood, count in sorted(stats["moods"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {mood}: {count}")

        print("\n风格分布:")
        for style, count in sorted(stats["styles"].items(), key=lambda x: x[1], reverse=True):
            print(f"  {style}: {count}")

    else:
        print(f"未知命令: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
