#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 在线提示词搜索模块
使用 info-search 项目的 search-wrapper.py 搜索最新的 Seedance 2.0 提示词
"""

import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# 配置日志（必须在导入之前）
LOG_DIR = Path("/root/clawd/skills/seedance-2-prompt/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'search_online.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# 添加 info-search 脚本路径到 Python 路径
INFO_SEARCH_SCRIPTS = Path("/root/clawd/projects/info-search/scripts")
sys.path.insert(0, str(INFO_SEARCH_SCRIPTS))

# 导入 search_wrapper
try:
    from search_wrapper import search
    SEARCH_AVAILABLE = True
    logger.info("✓ search_wrapper 模块已成功导入")
except ImportError as e:
    SEARCH_AVAILABLE = False
    logger.warning(f"✗ search_wrapper 导入失败: {e}")
    logger.warning("  在线搜索功能将被禁用")
    logger.warning(f"  搜索路径: {INFO_SEARCH_SCRIPTS}")

# 视频类型映射
VIDEO_TYPES = {
    "photo-realistic": "超逼真视频生成",
    "character-consistency": "角色与场景一致性",
    "camera-movement": "高级运镜动作",
    "creative-effects": "创意视觉特效",
    "storytelling": "剧情发展与延伸",
    "audio-sync": "音频与语音合成",
    "one-shot": "一镜到底",
    "emotion-performance": "情绪演绎"
}

# 难度级别映射
DIFFICULTY_LEVELS = {
    "BEGINNER": "初学者",
    "INTERMEDIATE": "中级",
    "ADVANCED": "高级",
    "EXPERT": "专家"
}


def search_prompts(
    query: str,
    video_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    max_results: int = 10
) -> List[Dict]:
    """
    搜索在线 Seedance 2.0 提示词

    Args:
        query: 搜索关键词
        video_type: 视频类型（可选）
        difficulty: 难度级别（可选）
        max_results: 最大结果数量

    Returns:
        统一格式的提示词结果列表

    示例:
        >>> results = search_prompts("雨天城市街道", video_type="photo-realistic", difficulty="INTERMEDIATE")
        >>> print(f"找到 {len(results)} 个提示词")
    """
    if not SEARCH_AVAILABLE:
        logger.error("在线搜索功能不可用，请检查 search-wrapper 配置")
        return []

    if not query or not query.strip():
        logger.warning("搜索查询为空")
        return []

    # 构建搜索查询
    search_query = build_search_query(query, video_type, difficulty)
    logger.info(f"开始搜索: '{search_query}'")

    try:
        # 使用 search-wrapper 搜索
        results = search(
            query=search_query,
            max_results=max_results,
            timeout=30
        )

        # 过滤和格式化结果
        formatted_results = []

        for result in results:
            # 跳过错误结果
            if result.get('source') == 'error':
                logger.warning(f"搜索结果包含错误: {result.get('content', '')}")
                continue

            # 尝试从搜索结果中提取提示词
            prompt_data = extract_prompt_from_result(result)

            if prompt_data:
                # 添加来源信息
                prompt_data['search_source'] = result.get('source', 'unknown')
                prompt_data['search_timestamp'] = result.get('timestamp', datetime.now().isoformat())

                formatted_results.append(prompt_data)

        logger.info(f"成功获取 {len(formatted_results)} 个提示词")
        return formatted_results

    except Exception as e:
        logger.error(f"搜索失败: {str(e)}")
        return []


def build_search_query(
    query: str,
    video_type: Optional[str] = None,
    difficulty: Optional[str] = None
) -> str:
    """
    构建优化后的搜索查询

    Args:
        query: 基础搜索关键词
        video_type: 视频类型（可选）
        difficulty: 难度级别（可选）

    Returns:
        优化后的搜索查询字符串
    """
    parts = [query]

    # 添加 Seedance 2.0 相关关键词
    parts.append("Seedance 2.0")

    # 添加提示词相关关键词
    parts.append("提示词")

    # 添加视频类型
    if video_type and video_type in VIDEO_TYPES:
        parts.append(VIDEO_TYPES[video_type])

    # 添加难度级别
    if difficulty and difficulty in DIFFICULTY_LEVELS:
        parts.append(DIFFICULTY_LEVELS[difficulty])

    return " ".join(parts)


def extract_prompt_from_result(result: Dict) -> Optional[Dict]:
    """
    从搜索结果中提取提示词信息

    Args:
        result: 搜索结果字典

    Returns:
        提示词数据字典，如果无法提取则返回 None
    """
    try:
        # 尝试解析搜索结果内容
        title = result.get('title', '')
        content = result.get('content', '')
        url = result.get('url', '')

        # 简单的提取逻辑：如果标题或内容包含提示词相关信息
        # 在实际应用中，这里可以更复杂地解析和提取

        # 创建提示词数据
        prompt_data = {
            'id': f"online-{hash(url + title) % 1000000}",
            'name': title[:100],  # 限制长度
            'title': title,
            'prompt': content[:500],  # 限制长度
            'url': url,
            'video_type': extract_video_type(title, content),
            'difficulty': extract_difficulty(title, content),
            'description': content[:300],
            'tags': extract_tags(title, content)
        }

        return prompt_data

    except Exception as e:
        logger.warning(f"提取提示词失败: {str(e)}")
        return None


def extract_video_type(title: str, content: str) -> str:
    """
    从标题和内容中提取视频类型

    Args:
        title: 标题
        content: 内容

    Returns:
        视频类型（默认为 photo-realistic）
    """
    text = f"{title} {content}".lower()

    for video_type in VIDEO_TYPES.keys():
        if video_type.lower() in text or VIDEO_TYPES[video_type].lower() in text:
            return video_type

    return "photo-realistic"


def extract_difficulty(title: str, content: str) -> str:
    """
    从标题和内容中提取难度级别

    Args:
        title: 标题
        content: 内容

    Returns:
        难度级别（默认为 INTERMEDIATE）
    """
    text = f"{title} {content}".lower()

    for difficulty in DIFFICULTY_LEVELS.keys():
        if difficulty.lower() in text or DIFFICULTY_LEVELS[difficulty].lower() in text:
            return difficulty

    # 检查中文难度级别
    if "初学者" in text or "简单" in text or "入门" in text:
        return "BEGINNER"
    elif "高级" in text or "专家" in text or "复杂" in text:
        return "ADVANCED"
    elif "专家" in text or "极致" in text:
        return "EXPERT"

    return "INTERMEDIATE"


def extract_tags(title: str, content: str) -> List[str]:
    """
    从标题和内容中提取标签

    Args:
        title: 标题
        content: 内容

    Returns:
        标签列表
    """
    text = f"{title} {content}"

    # 提取常见标签
    common_tags = [
        "Seedance 2.0", "AI", "视频生成", "提示词",
        "photo-realistic", "camera", "lighting", "style"
    ]

    tags = []
    for tag in common_tags:
        if tag.lower() in text.lower():
            tags.append(tag)

    # 如果没有标签，至少添加一个基础标签
    if not tags:
        tags = ["Seedance 2.0"]

    return tags


def search_and_display(
    query: str,
    video_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    max_results: int = 10
):
    """
    搜索并显示提示词

    Args:
        query: 搜索关键词
        video_type: 视频类型（可选）
        difficulty: 难度级别（可选）
        max_results: 最大结果数量
    """
    print("\n" + "=" * 80)
    print("🔍 Seedance 2.0 在线提示词搜索")
    print("=" * 80 + "\n")

    print(f"搜索查询: {query}")
    if video_type:
        print(f"视频类型: {VIDEO_TYPES.get(video_type, video_type)}")
    if difficulty:
        print(f"难度级别: {DIFFICULTY_LEVELS.get(difficulty, difficulty)}")
    print(f"最大结果数: {max_results}\n")

    print("-" * 80)
    print("🚀 正在搜索...")
    print("-" * 80 + "\n")

    # 执行搜索
    results = search_prompts(query, video_type, difficulty, max_results)

    # 显示结果
    if not results:
        print("❌ 未找到相关提示词")
        print("\n可能的原因:")
        print("  - 搜索关键词不匹配")
        print("  - 网络连接问题")
        print("  - 搜索源不可用")
        print("\n建议:")
        print("  - 尝试使用更通用的关键词")
        print("  - 检查网络连接")
        return

    print(f"\n✅ 找到 {len(results)} 个相关提示词:\n")

    for i, prompt in enumerate(results, 1):
        print("=" * 80)
        print(f"[{i}] {prompt.get('name', '未命名')}")
        print("=" * 80)

        print(f"ID: {prompt.get('id', 'N/A')}")
        print(f"标题: {prompt.get('title', 'N/A')}")
        print(f"视频类型: {VIDEO_TYPES.get(prompt.get('video_type'), prompt.get('video_type', 'N/A'))}")
        print(f"难度级别: {DIFFICULTY_LEVELS.get(prompt.get('difficulty'), prompt.get('difficulty', 'N/A'))}")

        if prompt.get('prompt'):
            print(f"\n提示词:\n{prompt.get('prompt')}")

        if prompt.get('tags'):
            print(f"\n标签: {', '.join(prompt.get('tags', []))}")

        if prompt.get('url'):
            print(f"\n来源: {prompt.get('url')}")

        print(f"\n搜索来源: {prompt.get('search_source', 'unknown')}")
        print("\n")


def main():
    """
    命令行入口

    用法:
        python3 search_online.py <query> [options]

    选项:
        -t, --type <video_type>: 指定视频类型
        -d, --difficulty <difficulty>: 指定难度级别
        -n, --num <max_results>: 指定最大结果数量

    示例:
        python3 search_online.py "雨天城市街道" -t photo-realistic -d INTERMEDIATE -n 10
    """
    if len(sys.argv) < 2:
        print("用法: python3 search_online.py <query> [options]")
        print("")
        print("选项:")
        print("  -t, --type <video_type>       指定视频类型 (photo-realistic, character-consistency, etc.)")
        print("  -d, --difficulty <difficulty>  指定难度级别 (BEGINNER, INTERMEDIATE, ADVANCED, EXPERT)")
        print("  -n, --num <max_results>        指定最大结果数量 (默认: 10)")
        print("")
        print("视频类型:")
        for key, name in VIDEO_TYPES.items():
            print(f"  - {key}: {name}")
        print("")
        print("难度级别:")
        for key, name in DIFFICULTY_LEVELS.items():
            print(f"  - {key}: {name}")
        print("")
        print("示例:")
        print("  python3 search_online.py '雨天城市街道' -t photo-realistic -d INTERMEDIATE -n 10")
        print("  python3 search_online.py '人物肖像' -d ADVANCED")
        sys.exit(1)

    # 解析参数
    query = sys.argv[1]
    video_type = None
    difficulty = None
    max_results = 10

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg in ['-t', '--type'] and i + 1 < len(sys.argv):
            video_type = sys.argv[i + 1]
            if video_type not in VIDEO_TYPES:
                print(f"错误: 无效的视频类型 '{video_type}'")
                print(f"有效的视频类型: {', '.join(VIDEO_TYPES.keys())}")
                sys.exit(1)
            i += 2
        elif arg in ['-d', '--difficulty'] and i + 1 < len(sys.argv):
            difficulty = sys.argv[i + 1]
            if difficulty not in DIFFICULTY_LEVELS:
                print(f"错误: 无效的难度级别 '{difficulty}'")
                print(f"有效的难度级别: {', '.join(DIFFICULTY_LEVELS.keys())}")
                sys.exit(1)
            i += 2
        elif arg in ['-n', '--num'] and i + 1 < len(sys.argv):
            try:
                max_results = int(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"错误: 无效的结果数量 '{sys.argv[i + 1]}'")
                sys.exit(1)
        else:
            i += 1

    # 执行搜索并显示结果
    search_and_display(query, video_type, difficulty, max_results)


if __name__ == "__main__":
    main()
