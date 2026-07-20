#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 智能扩展系统
提供模板库管理、自动扩展和联网学习功能
"""

import json
import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# 配置日志
SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'smart_expansion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class SceneTemplateLibrary:
    """场景模板库管理类"""

    def __init__(self, data_path: Optional[str] = None):
        """
        初始化场景模板库

        Args:
            data_path: 模板数据文件路径，默认为当前目录下的 data/template_library.json
        """
        if data_path is None:
            data_path = SCRIPT_DIR / "data" / "template_library.json"

        self.data_path = Path(data_path)
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """从文件加载模板数据"""
        if not self.data_path.exists():
            # 创建默认结构
            return {
                "metadata": {
                    "version": "2.0",
                    "created_at": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_templates": 0
                },
                "templates": {}
            }

        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 确保有 templates 键
                if 'templates' not in data:
                    data['templates'] = {}
                return data
        except Exception as e:
            logger.error(f"加载模板库失败: {e}")
            return {"templates": {}}

    def _save_templates(self) -> bool:
        """保存模板到文件"""
        try:
            # 确保目录存在
            self.data_path.parent.mkdir(parents=True, exist_ok=True)

            # 更新元数据
            self.templates['metadata']['last_updated'] = datetime.now().isoformat()
            self.templates['metadata']['total_templates'] = self._count_templates()

            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, ensure_ascii=False, indent=2)
            logger.info(f"模板库已保存到 {self.data_path}")
            return True
        except Exception as e:
            logger.error(f"保存模板库失败: {e}")
            return False

    def _count_templates(self) -> int:
        """统计模板总数"""
        count = 0
        for emotion_type in self.templates.get('templates', {}).values():
            count += len(emotion_type)
        return count

    def get_template(self, scene_key: str, emotion_type: Optional[str] = None) -> Optional[Dict]:
        """
        获取指定模板

        Args:
            scene_key: 场景键名（如 "竹林决战"）
            emotion_type: 情感类型（可选，用于加速查找）

        Returns:
            模板字典，如果不存在则返回 None
        """
        templates_dict = self.templates.get('templates', {})

        if emotion_type and emotion_type in templates_dict:
            if scene_key in templates_dict[emotion_type]:
                return templates_dict[emotion_type][scene_key]

        # 在所有情感类型中查找
        for emotion_dict in templates_dict.values():
            if scene_key in emotion_dict:
                return emotion_dict[scene_key]

        return None

    def add_template(self, name: str, template: Dict, emotion_type: Optional[str] = None) -> bool:
        """
        添加新模板

        Args:
            name: 模板名称（场景键名）
            template: 模板字典
            emotion_type: 情感类型（可选，如果未提供则从 template 中推断）

        Returns:
            是否添加成功
        """
        try:
            # 确定情感类型
            if emotion_type is None:
                emotion_type = template.get('emotion', 'other')

            # 确保 templates 字典和情感类型字典存在
            if 'templates' not in self.templates:
                self.templates['templates'] = {}

            if emotion_type not in self.templates['templates']:
                self.templates['templates'][emotion_type] = {}

            # 添加模板
            self.templates['templates'][emotion_type][name] = template
            self.templates['templates'][emotion_type][name]['created_at'] = datetime.now().isoformat()

            logger.info(f"已添加模板: {name} (情感类型: {emotion_type})")
            return self._save_templates()

        except Exception as e:
            logger.error(f"添加模板失败: {e}")
            return False

    def list_templates(self, emotion_type: Optional[str] = None) -> Dict:
        """
        列出模板

        Args:
            emotion_type: 情感类型（可选，为 None 时列出所有）

        Returns:
            模板字典
        """
        templates_dict = self.templates.get('templates', {})

        if emotion_type:
            return templates_dict.get(emotion_type, {})
        else:
            return templates_dict

    def search_templates(self, keyword: str) -> List[Tuple[str, str, Dict]]:
        """
        搜索模板

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的模板列表 [(emotion_type, scene_name, template)]
        """
        keyword = keyword.lower()
        results = []

        for emotion_type, emotion_dict in self.templates.get('templates', {}).items():
            for scene_name, template in emotion_dict.items():
                # 搜索名称、标签、描述
                search_text = ' '.join([
                    scene_name,
                    ' '.join(template.get('tags', [])),
                    template.get('intro', ''),
                    template.get('main_action', ''),
                    template.get('emotion_rise', ''),
                    template.get('conclusion', '')
                ])

                if keyword in search_text.lower():
                    results.append((emotion_type, scene_name, template))

        return results

    def get_stats(self) -> Dict:
        """获取模板库统计信息"""
        templates_dict = self.templates.get('templates', {})

        stats = {
            'total_templates': self._count_templates(),
            'emotion_types': list(templates_dict.keys()),
            'emotion_distribution': {},
            'last_updated': self.templates.get('metadata', {}).get('last_updated', 'N/A')
        }

        # 统计每个情感类型的模板数
        for emotion_type, emotion_dict in templates_dict.items():
            stats['emotion_distribution'][emotion_type] = len(emotion_dict)

        return stats

    def print_template(self, template: Dict):
        """打印模板信息"""
        print("\n" + "=" * 80)
        print(f"场景名称: {template.get('name', 'N/A')}")
        print(f"情感类型: {template.get('emotion', 'N/A')}")
        print(f"环境类型: {template.get('environment', 'N/A')}")
        print(f"标签:     {', '.join(template.get('tags', []))}")
        print("-" * 80)
        print(f"引入 (0-3s):\n{template.get('intro', 'N/A')}\n")
        print(f"主要动作 (3-7s):\n{template.get('main_action', 'N/A')}\n")
        print(f"情感升级 (7-12s):\n{template.get('emotion_rise', 'N/A')}\n")
        print(f"情感收尾 (12-15s):\n{template.get('conclusion', 'N/A')}")
        print("=" * 80 + "\n")


def detect_emotion(scene: str) -> str:
    """
    检测场景的情感类型

    Args:
        scene: 场景描述

    Returns:
        情感类型（combat, happy, sad, romantic, mysterious 等）
    """
    scene_lower = scene.lower()

    # 情感关键词映射
    emotion_keywords = {
        "combat": ["战斗", "打", "剑", "刀", "武术", "对峙", "决战", "格斗", "攻击", "防御", "招式"],
        "happy": ["开心", "快乐", "喜悦", "笑", "欢", "庆祝", "party", "celebration", "joy", "laugh"],
        "sad": ["悲伤", "难过", "哭泣", "眼泪", "哀", "悼", "loss", "cry", "tears"],
        "romantic": ["浪漫", "爱情", "吻", "拥抱", "love", "romantic", "kiss", "embrace"],
        "mysterious": ["神秘", "谜", "unknown", "mystery", "secret"],
        "action": ["跑", "跳", "飞", "追", "escape", "chase", "run", "jump"],
        "surprise": ["惊讶", "意外", "surprise", "shock", "unexpected"]
    }

    # 统计每个情感类型的关键词出现次数
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword in scene_lower)
        if score > 0:
            emotion_scores[emotion] = score

    # 返回得分最高的情感类型
    if emotion_scores:
        return max(emotion_scores.items(), key=lambda x: x[1])[0]

    return "other"


def detect_environment(scene: str) -> str:
    """
    检测场景的环境类型

    Args:
        scene: 场景描述

    Returns:
        环境类型
    """
    scene_lower = scene.lower()

    # 先检测是否是打戏场景
    combat_keywords = ["决战", "打戏", "对决", "激战", "交锋", "对峙", "战斗", "对打", "搏斗", "厮杀", "刀剑", "打斗", "街斗", "格斗", "夜战"]
    is_combat = any(keyword in scene_lower for keyword in combat_keywords)

    # 环境关键词映射（按优先级顺序，更具体的关键词放在前面）
    environment_keywords = {
        "snow": ["雪", "snow", "冰", "ice", "雪山", "冰雪"],
        "rain": ["雨", "rain", "雨天", "暴雨", "雨夜"],
        "night": ["夜", "night", "夜晚", "黑暗", "夜景", "霓虹"],
        "fire": ["火", "fire", "火焰", "burning"],
        "ocean": ["海", "sea", "ocean", "沙滩", "beach", "海边"],
        "cafe": ["咖啡", "cafe", "咖啡厅", "室内"],
        "forest": ["花园", "草地", "自然", "nature", "竹林", "竹", "森林", "树林", "山", "野外"],
        "urban": ["城市", "街头", "urban", "city", "街道", "建筑"]
    }

    # 检测环境类型
    for env_type, keywords in environment_keywords.items():
        if any(keyword in scene_lower for keyword in keywords):
            # 如果是打戏场景，返回对应的打戏环境类型
            if is_combat:
                if env_type in ["forest"]:
                    return "forest_combat"
                elif env_type == "rain":
                    return "rain_combat"
                elif env_type == "night":
                    return "night_combat"
                elif env_type == "snow":
                    return "snow"  # 雪地打戏还是 snow
                elif env_type == "urban":
                    return "urban_combat"
                else:
                    return env_type
            return env_type

    return "urban_combat" if is_combat else "general"


def add_custom_template(
    scene_name: str,
    intro: str,
    main_action: str,
    emotion_rise: str,
    conclusion: str,
    tags: Optional[List[str]] = None,
    emotion: Optional[str] = None,
    environment: Optional[str] = None
) -> bool:
    """
    用户添加自定义模板

    Args:
        scene_name: 场景名称
        intro: 引入部分 (0-3s)
        main_action: 主要动作 (3-7s)
        emotion_rise: 情感升级 (7-12s)
        conclusion: 情感收尾 (12-15s)
        tags: 标签列表（可选）
        emotion: 情感类型（可选，会自动检测）
        environment: 环境类型（可选，会自动检测）

    Returns:
        是否添加成功
    """
    try:
        library = SceneTemplateLibrary()

        # 自动检测情感和环境
        detected_emotion = emotion or detect_emotion(scene_name)
        detected_environment = environment or detect_environment(scene_name)

        template = {
            "emotion": detected_emotion,
            "environment": detected_environment,
            "intro": intro,
            "main_action": main_action,
            "emotion_rise": emotion_rise,
            "conclusion": conclusion,
            "tags": tags or []
        }

        return library.add_template(scene_name, template, detected_emotion)

    except Exception as e:
        logger.error(f"添加自定义模板失败: {e}")
        return False


def auto_expand_template(scene: str, generated_prompt: Dict) -> bool:
    """
    自动扩展模板（将生成的提示词保存到模板库）

    Args:
        scene: 场景描述
        generated_prompt: 生成的提示词字典（包含 segments）

    Returns:
        是否保存成功
    """
    try:
        library = SceneTemplateLibrary()

        # 检查是否已有该场景的模板
        existing = library.get_template(scene)
        if existing:
            logger.info(f"场景 '{scene}' 已存在模板，跳过自动扩展")
            return False

        # 从生成的提示词中提取分段
        segments = generated_prompt.get('segments', {})

        template = {
            "emotion": detect_emotion(scene),
            "environment": detect_environment(scene),
            "intro": segments.get('intro_0-3s', ''),
            "main_action": segments.get('main_action_3-7s', ''),
            "emotion_rise": segments.get('emotion_rise_7-12s', ''),
            "conclusion": segments.get('conclusion_12-15s', ''),
            "tags": ["自动生成", scene],
            "auto_generated": True
        }

        success = library.add_template(scene, template)
        if success:
            logger.info(f"已自动保存场景 '{scene}' 的模板")

        return success

    except Exception as e:
        logger.error(f"自动扩展模板失败: {e}")
        return False


# 便捷函数
def load_scene_library() -> SceneTemplateLibrary:
    """加载场景模板库的便捷函数"""
    return SceneTemplateLibrary()


def get_scene_template(scene_key: str, emotion_type: Optional[str] = None) -> Optional[Dict]:
    """获取场景模板的便捷函数"""
    library = SceneTemplateLibrary()
    return library.get_template(scene_key, emotion_type)


if __name__ == "__main__":
    # 测试代码
    print("=== Seedance 2.0 智能扩展系统 ===\n")

    # 加载模板库
    library = SceneTemplateLibrary()
    stats = library.get_stats()

    print("📊 模板库统计:")
    print(f"  总模板数: {stats['total_templates']}")
    print(f"  情感类型: {', '.join(stats['emotion_types'])}")
    print(f"  最后更新: {stats['last_updated']}\n")

    # 按情感类型显示
    print("📁 按情感类型分布:")
    for emotion_type, count in stats['emotion_distribution'].items():
        print(f"  {emotion_type}: {count} 个")
    print()

    # 测试情感检测
    print("🔍 情感检测测试:")
    test_scenes = ["竹林决战", "开心的派对", "浪漫的约会", "神秘的探险"]
    for scene in test_scenes:
        emotion = detect_emotion(scene)
        environment = detect_environment(scene)
        print(f"  '{scene}' -> 情感: {emotion}, 环境: {environment}")
    print()

    # 测试添加模板
    print("📝 测试添加模板:")
    success = add_custom_template(
        scene_name="测试场景",
        intro="镜头缓缓展开，画面清晰明亮。",
        main_action="角色开始进行动作，流畅自然。",
        emotion_rise="情感逐渐升级，表情变得丰富。",
        conclusion="最终收尾，画面淡出。",
        tags=["测试", "示例"]
    )
    print(f"  添加{'成功' if success else '失败'}")
    print()
