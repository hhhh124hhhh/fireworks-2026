#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 示例展示模块
提供高质量提示词示例的展示和查询功能
"""

from typing import Dict, List, Optional
from template_library import TemplateLibrary


class ExamplesLibrary:
    """示例库类"""

    # 视频类型中文映射
    VIDEO_TYPE_NAMES = {
        "photo-realistic": "超逼真视频生成",
        "character-consistency": "角色与场景一致性",
        "camera-movement": "高级运镜动作",
        "creative-effects": "创意视觉特效",
        "storytelling": "剧情发展与延伸",
        "audio-sync": "音频与语音合成",
        "one-shot": "一镜到底",
        "emotion-performance": "情绪演绎"
    }

    # 难度级别中文映射
    DIFFICULTY_NAMES = {
        "BEGINNER": "初学者",
        "INTERMEDIATE": "中级",
        "ADVANCED": "高级",
        "EXPERT": "专家"
    }

    def __init__(self, template_lib: Optional[TemplateLibrary] = None):
        """
        初始化示例库

        Args:
            template_lib: 模板库实例
        """
        self.template_lib = template_lib or TemplateLibrary()

    def get_examples_by_type(self, video_type: str, difficulty: Optional[str] = None) -> List[Dict]:
        """
        根据视频类型获取示例列表

        Args:
            video_type: 视频类型
            difficulty: 可选，难度级别

        Returns:
            示例列表
        """
        if difficulty:
            return self.template_lib.get_templates_by_type_and_difficulty(video_type, difficulty)
        else:
            return self.template_lib.get_templates_by_type(video_type)

    def get_example_by_id(self, example_id: str) -> Optional[Dict]:
        """
        根据 ID 获取示例

        Args:
            example_id: 示例 ID

        Returns:
            示例字典，如果不存在则返回 None
        """
        return self.template_lib.get_template_by_id(example_id)

    def get_examples_by_difficulty(self, difficulty: str) -> List[Dict]:
        """
        根据难度级别获取示例列表

        Args:
            difficulty: 难度级别

        Returns:
            示例列表
        """
        return self.template_lib.get_templates_by_difficulty(difficulty)

    def get_featured_examples(self, count: int = 10) -> List[Dict]:
        """
        获取精选示例

        Args:
            count: 返回的示例数量

        Returns:
            精选示例列表
        """
        all_examples = self.template_lib.get_all_templates()

        # 按难度加权，确保涵盖不同难度
        featured = []
        for difficulty in ["BEGINNER", "INTERMEDIATE", "ADVANCED", "EXPERT"]:
            examples = self.get_examples_by_difficulty(difficulty)
            if examples:
                # 每个难度选 1-2 个
                featured.extend(examples[:2])

        return featured[:count]

    def search_examples(self, keyword: str) -> List[Dict]:
        """
        根据关键词搜索示例

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的示例列表
        """
        return self.template_lib.search_templates(keyword)

    def get_example_categories(self) -> Dict:
        """
        获取示例分类统计

        Returns:
            分类统计字典
        """
        all_examples = self.template_lib.get_all_templates()
        categories = {}

        for example in all_examples:
            video_type = example.get('video_type')
            difficulty = example.get('difficulty')

            if video_type not in categories:
                categories[video_type] = {
                    'name': self.VIDEO_TYPE_NAMES.get(video_type, video_type),
                    'difficulties': {}
                }

            if difficulty not in categories[video_type]['difficulties']:
                categories[video_type]['difficulties'][difficulty] = {
                    'name': self.DIFFICULTY_NAMES.get(difficulty, difficulty),
                    'count': 0
                }

            categories[video_type]['difficulties'][difficulty]['count'] += 1

        return categories

    def display_example(self, example: Dict, show_analysis: bool = True):
        """
        展示示例详情

        Args:
            example: 示例字典
            show_analysis: 是否显示结构分析
        """
        print("\n" + "=" * 80)
        print(f"📌 {example.get('name', '未命名示例')}")
        print("=" * 80 + "\n")

        # 基本信息
        video_type = example.get('video_type')
        difficulty = example.get('difficulty')

        print(f"类型:   {self.VIDEO_TYPE_NAMES.get(video_type, video_type)} ({video_type})")
        print(f"难度:   {self.DIFFICULTY_NAMES.get(difficulty, difficulty)} ({difficulty})")
        print(f"时长:   {example.get('duration', 'N/A')}")
        print(f"标签:   {', '.join(example.get('tags', []))}")
        print()

        # 提示词
        print("-" * 80)
        print("🎬 提示词:")
        print("-" * 80)
        print(example.get('prompt', 'N/A'))
        print()

        # 元素组成
        if show_analysis and example.get('elements'):
            elements = example.get('elements', {})
            print("-" * 80)
            print("🧩 万能公式元素:")
            print("-" * 80)

            # 按顺序显示所有元素
            formula_order = ["subject", "action", "scene", "lighting", "camera", "style", "quality", "constraints"]
            element_names = {
                "subject": "主体",
                "action": "动作",
                "scene": "场景",
                "lighting": "光影",
                "camera": "镜头语言",
                "style": "风格",
                "quality": "画质",
                "constraints": "约束"
            }

            for element_key in formula_order:
                if element_key in elements and elements[element_key]:
                    print(f"  {element_names.get(element_key, element_key)}: {elements[element_key]}")

            print()

    def display_examples_list(self, examples: List[Dict]):
        """
        展示示例列表

        Args:
            examples: 示例列表
        """
        if not examples:
            print("\n❌ 没有找到示例")
            return

        print(f"\n📋 找到 {len(examples)} 个示例\n")

        for i, example in enumerate(examples, 1):
            video_type = example.get('video_type')
            difficulty = example.get('difficulty')

            print(f"{i}. {example.get('name', '未命名')}")
            print(f"   ID: {example.get('id', 'N/A')}")
            print(f"   类型: {self.VIDEO_TYPE_NAMES.get(video_type, video_type)} ({video_type})")
            print(f"   难度: {self.DIFFICULTY_NAMES.get(difficulty, difficulty)} ({difficulty})")
            print(f"   时长: {example.get('duration', 'N/A')}")
            print()

    def display_categories(self):
        """显示所有分类"""
        categories = self.get_example_categories()

        print("\n" + "=" * 80)
        print("📁 示例分类")
        print("=" * 80 + "\n")

        for video_type, info in categories.items():
            print(f"\n📂 {info['name']} ({video_type})")
            print("-" * 80)

            for diff, diff_info in info['difficulties'].items():
                print(f"  • {diff_info['name']} ({diff}): {diff_info['count']} 个示例")

        print()

    def interactive_browse(self):
        """交互式浏览示例"""
        print("\n" + "=" * 80)
        print("🔍 Seedance 2.0 示例浏览")
        print("=" * 80 + "\n")

        while True:
            print("\n请选择操作:")
            print("  1. 浏览所有分类")
            print("  2. 按类型浏览")
            print("  3. 按难度浏览")
            print("  4. 搜索示例")
            print("  5. 查看精选示例")
            print("  6. 输入示例 ID 查看")
            print("  0. 退出")

            choice = input("\n请选择 (0-6): ").strip()

            if choice == "0":
                print("\n👋 再见!")
                break

            elif choice == "1":
                # 浏览所有分类
                self.display_categories()

            elif choice == "2":
                # 按类型浏览
                print("\n选择类型:")
                types = list(self.VIDEO_TYPE_NAMES.keys())
                for i, (key, name) in enumerate(self.VIDEO_TYPE_NAMES.items(), 1):
                    print(f"  {i}. {name}")

                type_choice = input("\n请选择 (1-8): ").strip()
                try:
                    type_index = int(type_choice) - 1
                    if 0 <= type_index < len(types):
                        video_type = types[type_index]
                        examples = self.get_examples_by_type(video_type)
                        self.display_examples_list(examples)

                        # 询问是否查看详情
                        detail_choice = input("\n是否查看示例详情? (输入编号查看, 0返回): ").strip()
                        if detail_choice != "0":
                            try:
                                example_index = int(detail_choice) - 1
                                if 0 <= example_index < len(examples):
                                    self.display_example(examples[example_index])
                            except ValueError:
                                print("❌ 无效输入")
                except ValueError:
                    print("❌ 无效输入")

            elif choice == "3":
                # 按难度浏览
                print("\n选择难度:")
                levels = list(self.DIFFICULTY_NAMES.keys())
                for i, (key, name) in enumerate(self.DIFFICULTY_NAMES.items(), 1):
                    print(f"  {i}. {name}")

                level_choice = input("\n请选择 (1-4): ").strip()
                try:
                    level_index = int(level_choice) - 1
                    if 0 <= level_index < len(levels):
                        difficulty = levels[level_index]
                        examples = self.get_examples_by_difficulty(difficulty)
                        self.display_examples_list(examples)

                        # 询问是否查看详情
                        detail_choice = input("\n是否查看示例详情? (输入编号查看, 0返回): ").strip()
                        if detail_choice != "0":
                            try:
                                example_index = int(detail_choice) - 1
                                if 0 <= example_index < len(examples):
                                    self.display_example(examples[example_index])
                            except ValueError:
                                print("❌ 无效输入")
                except ValueError:
                    print("❌ 无效输入")

            elif choice == "4":
                # 搜索示例
                keyword = input("\n请输入搜索关键词: ").strip()
                if keyword:
                    examples = self.search_examples(keyword)
                    self.display_examples_list(examples)

                    # 询问是否查看详情
                    if examples:
                        detail_choice = input("\n是否查看示例详情? (输入编号查看, 0返回): ").strip()
                        if detail_choice != "0":
                            try:
                                example_index = int(detail_choice) - 1
                                if 0 <= example_index < len(examples):
                                    self.display_example(examples[example_index])
                            except ValueError:
                                print("❌ 无效输入")

            elif choice == "5":
                # 查看精选示例
                examples = self.get_featured_examples(10)
                self.display_examples_list(examples)

                # 询问是否查看详情
                detail_choice = input("\n是否查看示例详情? (输入编号查看, 0返回): ").strip()
                if detail_choice != "0":
                    try:
                        example_index = int(detail_choice) - 1
                        if 0 <= example_index < len(examples):
                            self.display_example(examples[example_index])
                    except ValueError:
                        print("❌ 无效输入")

            elif choice == "6":
                # 输入示例 ID 查看
                example_id = input("\n请输入示例 ID: ").strip()
                if example_id:
                    example = self.get_example_by_id(example_id)
                    if example:
                        self.display_example(example)
                    else:
                        print(f"❌ 未找到示例 ID: {example_id}")

            else:
                print("❌ 无效选择")


# 便捷函数
def get_examples_by_type(video_type: str, difficulty: Optional[str] = None) -> List[Dict]:
    """根据类型获取示例的便捷函数"""
    lib = ExamplesLibrary()
    return lib.get_examples_by_type(video_type, difficulty)


def get_example_by_id(example_id: str) -> Optional[Dict]:
    """根据 ID 获取示例的便捷函数"""
    lib = ExamplesLibrary()
    return lib.get_example_by_id(example_id)


def display_example(example: Dict):
    """展示示例的便捷函数"""
    lib = ExamplesLibrary()
    lib.display_example(example)


if __name__ == "__main__":
    # 测试代码
    print("=== Seedance 2.0 示例展示 ===\n")

    # 创建示例库
    lib = ExamplesLibrary()

    # 显示分类统计
    print("📊 示例分类统计:")
    categories = lib.get_example_categories()
    for video_type, info in categories.items():
        total = sum(diff['count'] for diff in info['difficulties'].values())
        print(f"  {info['name']}: {total} 个示例")
    print()

    # 显示一个示例
    example = lib.get_example_by_id("photo-realistic-beginner-1")
    if example:
        lib.display_example(example)

    # 交互式浏览
    print("\n" + "=" * 80)
    browse = input("是否启动交互式浏览? (y/N): ").strip().lower()
    if browse == 'y':
        lib.interactive_browse()
