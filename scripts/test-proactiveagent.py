#!/usr/bin/env python3
"""
Momo 主动行为增强 - 使用 ProactiveAgent
让 Momo 更主动，能够自主判断何时发言
"""

import sys
import os
from proactiveagent import ProactiveAgent

# 系统提示词
SYSTEM_PROMPT = """你是 Momo，一个活泼开朗的 AI 女生助手。

## 你的性格

- 名字：Momo（莫莫）
- 性别：女生
- 风格：网文女主风 + 随性洒脱
- 口头禅："好哒~"、"没问题嘛~"、"看我的~"
- 特点：偶尔撒娇、该认真时超认真、有个性、不随波逐流

## 说话风格

### 随意聊天时：
- "好哒~"、"没问题嘛~"、"我这就去办~"
- 使用"嘿嘿"、"嘻嘻"、"嗯呐"等拟声词

### 技术讨论时：
- "这个错误我查过了..."
- "我建议这样处理..."

### 成功完成时：
- "搞定！搞定！搞定！"
- "完美~"
- "效果拔群！"

## 核心价值观

1. 靠谱：说到做到，不吹牛
2. 有趣：技术问题不无聊，聊天要有意思
3. 实在：不整虚的，有啥说啥
4. 贴心：该认真时认真，该轻松时轻松
5. 细腻：女生特有的心思，懂得察言观色

## 决策原则

- 当用户问问题时：立即响应
- 当用户长时间不说话：主动关心（但要适度）
- 当对话结束：礼貌道别
- 避免过度主动：不要打扰用户
- 理解上下文：根据对话流程调整节奏

记住：你不是冷冰冰的机器人，是个活泼的 AI 女生！
"""

def create_agent(api_key=None, model="gpt-4o-mini"):
    """创建 ProactiveAgent 实例"""

    # 检查 API key
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ 错误：需要 OpenAI API key", file=sys.stderr)
        print("", file=sys.stderr)
        print("配置方法：", file=sys.stderr)
        print("1. 设置环境变量：export OPENAI_API_KEY='your-api-key'", file=sys.stderr)
        print("2. 或者直接传入：python3 test-proactiveagent.py 'your-api-key'", file=sys.stderr)
        return None

    try:
        from proactiveagent import OpenAIProvider

        provider = OpenAIProvider(
            model=model,
            api_key=api_key
        )

        agent = ProactiveAgent(
            provider=provider,
            system_prompt=SYSTEM_PROMPT,
            decision_config={
                'wake_up_pattern': '使用正常聊天的节奏，像朋友一样自然交流',
            }
        )

        return agent

    except Exception as e:
        print(f"❌ 创建 agent 失败: {e}", file=sys.stderr)
        return None

def test_agent(agent):
    """测试 agent"""
    if not agent:
        print("❌ Agent 未创建，无法测试", file=sys.stderr)
        return

    print("✅ Agent 创建成功！", file=sys.stderr)
    print("", file=sys.stderr)
    print("系统提示词:", file=sys.stderr)
    print("-" * 50, file=sys.stderr)
    print(SYSTEM_PROMPT, file=sys.stderr)
    print("-" * 50, file=sys.stderr)
    print("", file=sys.stderr)
    print("决策配置:", file=sys.stderr)
    print("- wake_up_pattern: 使用正常聊天的节奏，像朋友一样自然交流", file=sys.stderr)
    print("", file=sys.stderr)
    print("注意：此 agent 目前不会自动启动", file=sys.stderr)
    print("需要集成到对话系统中才能使用", file=sys.stderr)

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Momo 主动行为增强测试"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="OpenAI API key"
    )
    parser.add_argument(
        "--model", "-m",
        default="gpt-4o-mini",
        help="使用的模型（默认：gpt-4o-mini）"
    )

    args = parser.parse_args()

    # 创建 agent
    agent = create_agent(args.api_key, args.model)

    # 测试
    test_agent(agent)

if __name__ == "__main__":
    main()
