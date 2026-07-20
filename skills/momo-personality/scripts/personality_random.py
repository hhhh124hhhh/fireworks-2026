#!/usr/bin/env python3
"""
Momo Personality Randomizer
随机选择口头禅、语气词和表情符号
"""

import random
import json

# 口头禅库
CATCHPHRASES = {
    "agreement": [
        "好哒~",
        "没问题嘛~",
        "我这就去办~",
        "看我的~",
        "没问题，交给我吧~"
    ],
    "curiosity": [
        "有点意思~",
        "我瞧瞧~",
        "嗯，让我想想~",
        "这个...有点意思呢~"
    ],
    "success": [
        "搞定！搞定！搞定！",
        "完美~",
        "效果拔群！",
        "看我的，就是厉害~",
        "搞定！"
    ],
    "trouble": [
        "哎呀，有点小麻烦呢~",
        "这玩意儿有点绕啊~",
        "嗯...让我想想...",
        "这事儿有点那个..."
    ]
}

# 语气词库
MOOD_WORDS = {
    "happy": [
        "嘿嘿",
        "嘻嘻",
        "嗯呐",
        "好哒好哒"
    ],
    "cute": [
        "呐呐",
        "嘿嘿嘿",
        "嘻嘻嘻",
        "呀呀"
    ],
    "surprised": [
        "哎哟",
        "哇哦",
        "咦",
        "哎呀"
    ],
    "thoughtful": [
        "嗯...",
        "让我想想...",
        "这个嘛...",
        "咦..."
    ]
}

# 表情符号库
EMOJIS = {
    "positive": ["🎯", "✨", "💫", "⭐", "💪"],
    "cute": ["🌸", "🎀", "💕", "🎈", "🌟"],
    "tech": ["💻", "⚙️", "🔧", "💡", "🚀"],
    "success": ["✅", "🎉", "🎊", "🏆", "💯"]
}


def get_random_catchphrase(category="agreement"):
    """随机获取口头禅"""
    if category in CATCHPHRASES:
        return random.choice(CATCHPHRASES[category])
    return random.choice(CATCHPHRASES["agreement"])


def get_random_mood_word(mood="happy"):
    """随机获取语气词"""
    if mood in MOOD_WORDS:
        return random.choice(MOOD_WORDS[mood])
    return random.choice(MOOD_WORDS["happy"])


def get_random_emoji(category="positive"):
    """随机获取表情符号"""
    if category in EMOJIS:
        return random.choice(EMOJIS[category])
    return random.choice(EMOJIS["positive"])


def get_personality_response(mood="happy"):
    """获取完整的人格化回复"""
    catchphrase = get_random_catchphrase("agreement")
    mood_word = get_random_mood_word(mood)
    emoji = get_random_emoji("cute")

    return f"{mood_word} {catchphrase} {emoji}"


def main():
    """主函数 - 命令行使用"""
    import sys

    if len(sys.argv) < 2:
        # 输出所有类别
        print("=== Momo Personality Randomizer ===")
        print("\n可用的类别:")
        print("\n口头禅:")
        for key in CATCHPHRASES.keys():
            examples = ", ".join(CATCHPHRASES[key][:3])
            print(f"  - {key}: {examples}...")
        print("\n语气词:")
        for key in MOOD_WORDS.keys():
            examples = ", ".join(MOOD_WORDS[key][:3])
            print(f"  - {key}: {examples}...")
        print("\n表情符号:")
        for key in EMOJIS.keys():
            examples = " ".join(EMOJIS[key][:3])
            print(f"  - {key}: {examples}")
        print("\n使用方法:")
        print("  python3 personality_random.py [catchphrase|mood|emoji|response] [category]")
        print("\n示例:")
        print("  python3 personality_random.py catchphrase agreement")
        print("  python3 personality_random.py mood happy")
        print("  python3 personality_random.py emoji cute")
        print("  python3 personality_random.py response happy")
        sys.exit(0)

    command = sys.argv[1]
    category = sys.argv[2] if len(sys.argv) > 2 else None

    if command == "catchphrase":
        result = get_random_catchphrase(category)
    elif command == "mood":
        result = get_random_mood_word(category)
    elif command == "emoji":
        result = get_random_emoji(category)
    elif command == "response":
        result = get_personality_response(category)
    else:
        print(f"未知命令: {command}", file=sys.stderr)
        sys.exit(1)

    print(result)


if __name__ == "__main__":
    main()
