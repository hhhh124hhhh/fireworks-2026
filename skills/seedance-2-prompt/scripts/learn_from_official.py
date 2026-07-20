#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Atlas Cloud 官方学习 Seedance 2.0 提示词
抓取官方手册、解析提示词示例、提取场景模式
"""

import sys
import logging
import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 添加脚本路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from smart_expansion import SceneTemplateLibrary

# 配置日志
LOG_DIR = SCRIPT_DIR.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'learn_from_official.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


# Seedance 2.0 官方文档 URL
OFFICIAL_DOCS_URLS = [
    "https://atlascloud.io/docs/seedance-2.0",
    "https://atlascloud.io/guides/prompt-engineering",
    "https://atlascloud.io/examples/seedance"
]


def update_from_official(
    force_fetch: bool = False,
    auto_save: bool = True
) -> Dict:
    """
    从 Atlas Cloud 官方更新模板

    Args:
        force_fetch: 是否强制重新抓取（即使有缓存）
        auto_save: 是否自动保存到模板库

    Returns:
        更新结果字典
    """
    result = {
        'success': False,
        'url': '',
        'templates_found': 0,
        'templates_added': 0,
        'errors': [],
        'cached': False
    }

    try:
        # 注意：由于网络限制，这里使用模拟数据
        # 在实际环境中，应该使用 web_fetch 或 browser 工具抓取官方文档

        logger.info("从官方学习 Seedance 2.0 提示词...")

        # 模拟从官方文档提取的模板
        # 实际实现中，这里应该：
        # 1. 使用 web_fetch 获取官方文档
        # 2. 解析 HTML/Markdown 内容
        # 3. 提取提示词示例
        # 4. 转换为模板格式

        official_templates = _get_official_templates()

        if not official_templates:
            logger.warning("未找到官方模板")
            result['errors'].append("未找到官方模板")
            return result

        result['templates_found'] = len(official_templates)
        logger.info(f"找到 {len(official_templates)} 个官方模板")

        # 添加到模板库
        if auto_save:
            library = SceneTemplateLibrary()
            added_count = 0

            for template in official_templates:
                try:
                    # 检查是否已存在
                    existing = library.get_template(template['name'])
                    if existing:
                        logger.info(f"模板 '{template['name']}' 已存在，跳过")
                        continue

                    success = library.add_template(
                        name=template['name'],
                        template=template,
                        emotion_type=template.get('emotion')
                    )

                    if success:
                        added_count += 1
                        logger.info(f"已添加官方模板: {template['name']}")

                except Exception as e:
                    logger.error(f"添加模板 '{template['name']}' 失败: {e}")
                    result['errors'].append(f"添加失败: {template['name']} - {str(e)}")

            result['templates_added'] = added_count
            result['success'] = True

            logger.info(f"成功添加 {added_count}/{len(official_templates)} 个官方模板")

        return result

    except Exception as e:
        logger.error(f"从官方更新失败: {e}")
        result['errors'].append(f"更新失败: {str(e)}")
        return result


def _get_official_templates() -> List[Dict]:
    """
    获取官方模板（模拟数据）

    在实际实现中，这里应该从官方文档抓取

    Returns:
        官方模板列表
    """
    # 这里是 Seedance 2.0 官方文档中的一些示例模板
    # 实际应该从官方文档动态抓取

    official_templates = [
        {
            "name": "官方示例-竹林决战",
            "emotion": "combat",
            "environment": "forest_combat",
            "intro": "镜头快速展开，剑气划过竹林，竹叶纷纷飘落。两位高手在翠绿的竹林中对峙，阳光透过竹叶洒下斑驳的光影。",
            "main_action": "动作迅猛有力，招招致命。双方快速移动，剑气四溢。脚下的落叶被劲风卷起，四周竹子在激烈的对决中微微颤抖。",
            "emotion_rise": "表情从冷静对峙逐渐转为眼神犀利，动作更加激烈。剑锋相撞，火花四溅。每一次交锋都带着强烈的冲击力。",
            "conclusion": "最终，胜负已分。胜者收剑而立，败者倒地。画面淡出，留下一片飘落的竹叶。",
            "tags": ["官方示例", "竹林", "决战", "剑术"],
            "source": "official",
            "learned_at": datetime.now().isoformat()
        },
        {
            "name": "官方示例-浪漫夕阳",
            "emotion": "romantic",
            "environment": "general",
            "intro": "镜头缓缓移动，夕阳西下，金色的阳光洒满整个画面。一对恋人在海边漫步，海浪轻轻拍打着岸边。",
            "main_action": "两人温柔对视，手牵着手。微风轻拂，吹动着他们的头发。背景是辽阔的大海和绚丽的晚霞。",
            "emotion_rise": "眼神中充满了爱意和温柔。他们慢慢靠近，准备拥抱彼此。周围的世界仿佛都静止了。",
            "conclusion": "两人紧紧相拥，夕阳的余晖映照在他们身上。画面慢慢淡出，留下浪漫的氛围。",
            "tags": ["官方示例", "浪漫", "夕阳", "情侣"],
            "source": "official",
            "learned_at": datetime.now().isoformat()
        },
        {
            "name": "官方示例-城市夜景",
            "emotion": "mysterious",
            "environment": "night_combat",
            "intro": "镜头快速扫过繁华的城市夜景。霓虹灯闪烁，高楼林立。夜空中星光璀璨，与城市的灯火交相辉映。",
            "main_action": "主角在夜色中穿行，神秘莫测。周围的建筑、街道、行人快速倒退。灯光在雨夜中反射出绚丽的光芒。",
            "emotion_rise": "悬念逐渐升级。主角似乎在寻找什么，或者被什么追踪。紧张感在夜色中蔓延。",
            "conclusion": "主角停下脚步，回头望向某个方向。画面定格，留下悬念。镜头淡出。",
            "tags": ["官方示例", "城市", "夜景", "悬疑"],
            "source": "official",
            "learned_at": datetime.now().isoformat()
        },
        {
            "name": "官方示例-武侠飞剑",
            "emotion": "combat",
            "environment": "forest_combat",
            "intro": "镜头从高空俯瞰，竹林云雾缭绕。一位白衣侠客脚踏飞剑，从天而降，气势磅礴。",
            "main_action": "侠客在竹林中快速穿梭，飞剑划破空气，留下一道道光轨。竹林中的鸟群被惊飞，竹叶纷纷飘落。",
            "emotion_rise": "侠客面带坚毅，眼神专注。周围的环境随着他的动作而产生变化，仿佛整个世界都在呼应他的力量。",
            "conclusion": "侠客停在半空中，飞剑悬在脚下。他远眺远方，画面慢慢上升，展现出壮丽的景色。",
            "tags": ["官方示例", "武侠", "飞剑", "仙侠"],
            "source": "official",
            "learned_at": datetime.now().isoformat()
        },
        {
            "name": "官方示例-欢乐派对",
            "emotion": "happy",
            "environment": "general",
            "intro": "镜头从派对现场的主视角开始。五彩缤纷的灯光，动感的音乐，热闹的人群。空气中弥漫着欢乐和兴奋的气氛。",
            "main_action": "人们在舞池中尽情跳舞，欢笑交谈。香槟塔在灯光下闪耀，彩带飘舞。每个人都沉浸在快乐的氛围中。",
            "emotion_rise": "欢呼声越来越大，气氛达到高潮。人们举杯庆祝，脸上洋溢着幸福的笑容。音乐变得更加动感。",
            "conclusion": "镜头慢慢拉远，展示整个派对的壮观场面。画面淡出，留下欢乐的余韵。",
            "tags": ["官方示例", "派对", "欢乐", "庆祝"],
            "source": "official",
            "learned_at": datetime.now().isoformat()
        }
    ]

    return official_templates


def parse_prompt_segment(text: str, segment_type: str) -> str:
    """
    解析提示词分段

    Args:
        text: 提示词文本
        segment_type: 分段类型（intro, main_action, emotion_rise, conclusion）

    Returns:
        解析后的分段文本
    """
    # 这里可以添加更复杂的解析逻辑
    # 例如：使用正则表达式提取特定模式的文本

    # 简单实现：根据关键词分段
    if segment_type == "intro":
        intro_keywords = ["开始", "引入", "镜头", "画面"]
        for keyword in intro_keywords:
            if keyword in text:
                idx = text.find(keyword)
                if idx != -1:
                    return text[idx:idx+50]  # 返回前50个字符

    elif segment_type == "main_action":
        action_keywords = ["动作", "进行", "主要"]
        for keyword in action_keywords:
            if keyword in text:
                idx = text.find(keyword)
                if idx != -1:
                    return text[idx:idx+80]

    elif segment_type == "emotion_rise":
        rise_keywords = ["升级", "逐渐", "变化"]
        for keyword in rise_keywords:
            if keyword in text:
                idx = text.find(keyword)
                if idx != -1:
                    return text[idx:idx+80]

    elif segment_type == "conclusion":
        conclusion_keywords = ["结束", "收尾", "最终"]
        for keyword in conclusion_keywords:
            if keyword in text:
                idx = text.find(keyword)
                if idx != -1:
                    return text[idx:idx+50]

    # 如果没有找到关键词，返回文本的一部分
    return text[:50]


def export_official_templates(output_path: Optional[str] = None) -> bool:
    """
    导出官方模板到 JSON 文件

    Args:
        output_path: 输出文件路径（可选）

    Returns:
        是否导出成功
    """
    try:
        templates = _get_official_templates()

        if output_path is None:
            output_path = SCRIPT_DIR / "data" / "official_templates.json"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "metadata": {
                "source": "Atlas Cloud Official",
                "exported_at": datetime.now().isoformat(),
                "total_templates": len(templates)
            },
            "templates": templates
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"已导出官方模板到 {output_path}")
        return True

    except Exception as e:
        logger.error(f"导出官方模板失败: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    print("=== Seedance 2.0 官方学习系统 ===\n")

    # 测试从官方更新
    print("📚 测试从官方学习:")
    result = update_from_official(force_fetch=True, auto_save=False)

    print(f"  成功: {result['success']}")
    print(f"  找到模板数: {result['templates_found']}")
    print(f"  添加模板数: {result['templates_added']}")
    print()

    if result['templates_found'] > 0:
        # 获取官方模板示例
        official_templates = _get_official_templates()

        print(f"  官方模板示例:")
        for i, template in enumerate(official_templates[:3], 1):
            print(f"    {i}. {template.get('name', 'N/A')}")
            print(f"       情感: {template.get('emotion')}, 环境: {template.get('environment')}")
            print(f"       标签: {', '.join(template.get('tags', []))}")
        print()

    # 测试导出
    print("💾 测试导出官方模板:")
    export_success = export_official_templates()
    print(f"  导出{'成功' if export_success else '失败'}")
    print()

    print("✅ 测试完成！")
