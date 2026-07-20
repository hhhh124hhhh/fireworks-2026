#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 人物特征生成器
防止人物撞脸，生成独特的人物描述
"""

import random
import json
from typing import Dict, List, Optional
from pathlib import Path

# ========== 人物特征库 ==========

class CharacterTraits:
    """人物特征库"""

    # 脸型
    FACE_TYPES = [
        '鹅蛋脸', '瓜子脸', '圆脸', '长脸', '方脸',
        '菱形脸', '椭圆脸', '心形脸', '三角形脸'
    ]

    # 眼睛
    EYE_TYPES = [
        '丹凤眼', '杏仁眼', '圆眼', '桃花眼', '凤眼',
        '单眼皮', '双眼皮', '内双', '欧式大双'
    ]

    # 眉毛
    EYEBROW_TYPES = [
        '剑眉', '平眉', '柳叶眉', '弯眉', '剑眉',
        '粗眉', '细眉', '自然眉形'
    ]

    # 鼻子
    NOSE_TYPES = [
        '高鼻梁', '小巧鼻', '直鼻梁', '鹰钩鼻', '塌鼻梁',
        '蒜头鼻', '直鼻', '鼻头微翘'
    ]

    # 嘴唇
    LIP_TYPES = [
        '樱桃小嘴', '厚唇', '薄唇', 'M字唇', '花瓣唇',
        '自然唇形', '微笑唇'
    ]

    # 发型
    HAIR_STYLES = [
        '长发', '短发', '中长发', '波波头', '卷发', '直发',
        '马尾', '丸子头', '披肩发', '刘海', '无刘海'
    ]

    # 发色
    HAIR_COLORS = [
        '黑色', '深棕色', '浅棕色', '金色', '银灰色',
        '红色', '蓝色', '紫色', '白色', '灰白色'
    ]

    # 肤色
    SKIN_TONES = [
        '白皙皮肤', '小麦色皮肤', '橄榄色皮肤', '深褐色皮肤', '古铜色皮肤',
        '自然肤色', '健康肤色'
    ]

    # 年龄
    AGE_RANGES = [
        '18-20岁少女', '20-25岁青年', '25-30岁青年',
        '30-35岁青年', '35-40岁青年', '40-45岁中年'
    ]

    # 气质
    TEMPERAMENTS = [
        '清纯可爱', '成熟优雅', '知性气质', '温柔甜美',
        '干练职业', '文艺气质', '阳光活力', '高冷气质'
    ]

    # 身高
    HEIGHT_RANGES = [
        '155cm娇小', '160cm纤细', '165cm标准', '170cm高挑', '175cm修长'
    ]

    # 体型
    BODY_TYPES = [
        '纤细苗条', '匀称健康', '丰满曲线', '清瘦骨感', '标准体型'
    ]

    # 服饰风格
    OUTFIT_STYLES = [
        '简约时尚', '休闲舒适', '职业装', '复古优雅', '运动休闲',
        '甜美可爱', '成熟气质', '潮流时尚'
    ]


class CharacterGenerator:
    """人物生成器"""

    def __init__(self):
        self.traits = CharacterTraits()
        self.generated_characters = []  # 记录已生成的角色

    def generate_unique_character(self, exclude: Optional[List[str]] = None) -> Dict:
        """
        生成独特的人物特征

        Args:
            exclude: 排除的人物 ID 列表

        Returns:
            人物特征字典
        """
        max_attempts = 100
        for attempt in range(max_attempts):
            char = self._generate_character()
            char_id = self._generate_character_id(char)

            # 检查是否已生成过
            if char_id not in self.generated_characters:
                if exclude and char_id in exclude:
                    continue
                self.generated_characters.append(char_id)
                return char

        # 如果无法生成新的，返回最后一个
        return self._generate_character()

    def generate_character_for_scene(self, scene: str, style: str = 'default') -> Dict:
        """
        为特定场景生成人物

        Args:
            scene: 场景描述
            style: 风格（default, realistic, anime, etc.）

        Returns:
            人物特征字典
        """
        # 根据场景选择特征
        char = self.generate_unique_character()

        # 根据风格调整
        if style == 'anime':
            # 动漫风格特征
            char['眼睛'] = random.choice(['杏眼', '圆润大眼', '水汪汪的眼睛'])
            char['肤色'] = random.choice(['白皙皮肤', '健康肤色'])
        elif style == 'realistic':
            # 写实风格
            char['五官'] = '立体精致'
        elif style == 'fantasy':
            # 奇幻风格
            char['眼睛'] = random.choice(['神秘紫眼', '银色眼睛', '金色眼睛'])
            char['发色'] = random.choice(['银白色', '浅紫色', '淡金色'])

        return char

    def generate_multiple_characters(self, count: int, exclude: Optional[List[str]] = None) -> List[Dict]:
        """
        生成多个独特人物

        Args:
            count: 人物数量
            exclude: 排除的人物 ID 列表

        Returns:
            人物特征字典列表
        """
        characters = []
        for i in range(count):
            char = self.generate_unique_character(exclude)
            characters.append(char)

        return characters

    def _generate_character(self) -> Dict:
        """生成单个人物特征"""
        return {
            '脸型': random.choice(self.traits.FACE_TYPES),
            '眼睛': random.choice(self.traits.EYE_TYPES),
            '眉毛': random.choice(self.traits.EYEBROW_TYPES),
            '鼻子': random.choice(self.traits.NOSE_TYPES),
            '嘴唇': random.choice(self.traits.LIP_TYPES),
            '发型': random.choice(self.traits.HAIR_STYLES),
            '发色': random.choice(self.traits.HAIR_COLORS),
            '肤色': random.choice(self.traits.SKIN_TONES),
            '年龄': random.choice(self.traits.AGE_RANGES),
            '气质': random.choice(self.traits.TEMPERAMENTS),
            '身高': random.choice(self.traits.HEIGHT_RANGES),
            '体型': random.choice(self.traits.BODY_TYPES),
            '服饰风格': random.choice(self.traits.OUTFIT_STYLES)
        }

    def _generate_character_id(self, char: Dict) -> str:
        """生成人物唯一 ID"""
        return f"{char['脸型']}_{char['眼睛']}_{char['发型']}_{char['发色']}_{char['年龄']}"

    def format_character_description(self, char: Dict, detailed: bool = False) -> str:
        """
        格式化人物描述

        Args:
            char: 人物特征字典
            detailed: 是否详细描述

        Returns:
            格式化的人物描述
        """
        if detailed:
            return (
                f"{char['年龄']}女性，{char['气质']}，"
                f"{char['脸型']}，{char['肤色']}，"
                f"{char['发型']}，{char['发色']}，"
                f"{char['眼睛']}，{char['眉毛']}，"
                f"{char['鼻子']}，{char['嘴唇']}，"
                f"{char['身高']}，{char['体型']}，"
                f"穿着{char['服饰风格']}的服装"
            )
        else:
            return (
                f"{char['年龄']}女性，{char['气质']}，"
                f"{char['脸型']}，{char['发型']}，{char['发色']}，"
                f"{char['肤色']}，{char['眼睛']}"
            )

    def format_character_for_prompt(self, char: Dict) -> str:
        """
        格式化为 Seedance 2.0 提示词用的人物描述

        Args:
            char: 人物特征字典

        Returns:
            提示词格式的人物描述
        """
        return (
            f"一位{char['年龄']}，{char['气质']}的女性，"
            f"{char['脸型']}，{char['肤色']}，"
            f"{char['发型']}，{char['发色']}，"
            f"{char['眼睛']}，{char['眉毛']}，"
            f"{char['鼻子']}，{char['嘴唇']}，"
            f"{char['身高']}，{char['体型']}"
        )


def main():
    """主函数 - 命令行接口"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Seedance 2.0 人物特征生成器')
    parser.add_argument('-n', '--number', type=int, default=1,
                        help='生成的人物数量')
    parser.add_argument('--detailed', action='store_true',
                        help='生成详细描述')
    parser.add_argument('--prompt-format', action='store_true',
                        help='输出 Seedance 2.0 提示词格式')
    parser.add_argument('--scene', type=str, default=None,
                        help='为特定场景生成人物')
    parser.add_argument('--style', type=str, default='default',
                        choices=['default', 'realistic', 'anime', 'fantasy'],
                        help='人物风格')
    parser.add_argument('--stats', action='store_true',
                        help='显示统计信息')

    args = parser.parse_args()

    generator = CharacterGenerator()

    # 显示统计信息
    if args.stats:
        print('📊 人物特征库统计')
        print('=' * 60)
        print(f'脸型：{len(CharacterTraits.FACE_TYPES)} 种')
        print(f'眼睛：{len(CharacterTraits.EYE_TYPES)} 种')
        print(f'眉毛：{len(CharacterTraits.EYEBROW_TYPES)} 种')
        print(f'鼻子：{len(CharacterTraits.NOSE_TYPES)} 种')
        print(f'嘴唇：{len(CharacterTraits.LIP_TYPES)} 种')
        print(f'发型：{len(CharacterTraits.HAIR_STYLES)} 种')
        print(f'发色：{len(CharacterTraits.HAIR_COLORS)} 种')
        print(f'肤色：{len(CharacterTraits.SKIN_TONES)} 种')
        print(f'年龄：{len(CharacterTraits.AGE_RANGES)} 种')
        print(f'气质：{len(CharacterTraits.TEMPERAMENTS)} 种')
        print(f'身高：{len(CharacterTraits.HEIGHT_RANGES)} 种')
        print(f'体型：{len(CharacterTraits.BODY_TYPES)} 种')
        print(f'服饰风格：{len(CharacterTraits.OUTFIT_STYLES)} 种')

        total = (len(CharacterTraits.FACE_TYPES) *
                 len(CharacterTraits.EYE_TYPES) *
                 len(CharacterTraits.EYEBROW_TYPES) *
                 len(CharacterTraits.NOSE_TYPES) *
                 len(CharacterTraits.LIP_TYPES) *
                 len(CharacterTraits.HAIR_STYLES) *
                 len(CharacterTraits.HAIR_COLORS) *
                 len(CharacterTraits.SKIN_TONES) *
                 len(CharacterTraits.AGE_RANGES) *
                 len(CharacterTraits.TEMPERAMENTS) *
                 len(CharacterTraits.HEIGHT_RANGES) *
                 len(CharacterTraits.BODY_TYPES) *
                 len(CharacterTraits.OUTFIT_STYLES))
        print(f'\n组合数量：{total:,}')
        return

    # 为特定场景生成
    if args.scene:
        char = generator.generate_character_for_scene(args.scene, args.style)
        if args.prompt_format:
            desc = generator.format_character_for_prompt(char)
        elif args.detailed:
            desc = generator.format_character_description(char, detailed=True)
        else:
            desc = generator.format_character_description(char, detailed=False)

        print(f'🎭 场景人物：{args.scene}')
        print('=' * 60)
        print(desc)
        return

    # 生成多个人物
    characters = generator.generate_multiple_characters(args.number)

    print(f'🎭 独特人物特征（防止撞脸）')
    print('=' * 60)

    for i, char in enumerate(characters, 1):
        print(f'\n{i}. 人物特征')
        print(f'   脸型：{char["脸型"]}')
        print(f'   眼睛：{char["眼睛"]}，眉毛：{char["眉毛"]}')
        print(f'   鼻子：{char["鼻子"]}，嘴唇：{char["嘴唇"]}')
        print(f'   发型：{char["发型"]}，发色：{char["发色"]}')
        print(f'   肤色：{char["肤色"]}，年龄：{char["年龄"]}')
        print(f'   气质：{char["气质"]}，身高：{char["身高"]}')
        print(f'   体型：{char["体型"]}，服饰：{char["服饰风格"]}')


if __name__ == '__main__':
    main()
