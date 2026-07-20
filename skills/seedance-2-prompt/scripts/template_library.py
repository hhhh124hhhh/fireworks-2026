#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 提示词模板库
提供模板的加载、查询和管理功能
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path


class TemplateLibrary:
    """模板库管理类"""

    def __init__(self, data_path: Optional[str] = None):
        """
        初始化模板库

        Args:
            data_path: 模板数据文件路径，默认为当前目录下的 data/templates.json
        """
        if data_path is None:
            # 默认路径：相对于脚本所在目录的 data/templates.json
            script_dir = Path(__file__).parent
            data_path = script_dir / "data" / "templates.json"

        self.data_path = Path(data_path)
        self.templates = self._load_templates()

    def _load_templates(self) -> List[Dict]:
        """从文件加载模板数据"""
        if not self.data_path.exists():
            return []

        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('templates', [])
        except Exception as e:
            print(f"加载模板失败: {e}")
            return []

    def _save_templates(self) -> bool:
        """保存模板到文件"""
        try:
            # 确保目录存在
            self.data_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump({'templates': self.templates}, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存模板失败: {e}")
            return False

    def get_all_templates(self) -> List[Dict]:
        """获取所有模板"""
        return self.templates

    def get_template_by_id(self, template_id: str) -> Optional[Dict]:
        """
        根据 ID 获取模板

        Args:
            template_id: 模板 ID

        Returns:
            模板字典，如果不存在则返回 None
        """
        for template in self.templates:
            if template.get('id') == template_id:
                return template
        return None

    def get_templates_by_type(self, video_type: str) -> List[Dict]:
        """
        根据视频类型获取模板列表

        Args:
            video_type: 视频类型（如 'photo-realistic', 'character-consistency' 等）

        Returns:
            匹配的模板列表
        """
        return [t for t in self.templates if t.get('video_type') == video_type]

    def get_templates_by_difficulty(self, difficulty: str) -> List[Dict]:
        """
        根据难度获取模板列表

        Args:
            difficulty: 难度级别（'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'）

        Returns:
            匹配的模板列表
        """
        return [t for t in self.templates if t.get('difficulty') == difficulty]

    def get_templates_by_type_and_difficulty(self, video_type: str, difficulty: str) -> List[Dict]:
        """
        根据视频类型和难度获取模板列表

        Args:
            video_type: 视频类型
            difficulty: 难度级别

        Returns:
            匹配的模板列表
        """
        return [
            t for t in self.templates
            if t.get('video_type') == video_type and t.get('difficulty') == difficulty
        ]

    def search_templates(self, keyword: str) -> List[Dict]:
        """
        根据关键词搜索模板

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的模板列表
        """
        keyword = keyword.lower()
        results = []

        for template in self.templates:
            # 搜索名称、提示词、标签
            search_fields = [
                template.get('name', ''),
                template.get('prompt', ''),
                ' '.join(template.get('tags', []))
            ]

            if any(keyword in field.lower() for field in search_fields):
                results.append(template)

        return results

    def save_custom_template(self, template: Dict) -> bool:
        """
        保存自定义模板

        Args:
            template: 模板字典，必须包含 id, name, video_type, difficulty, prompt 等字段

        Returns:
            是否保存成功
        """
        # 检查必要字段
        required_fields = ['id', 'name', 'video_type', 'difficulty', 'prompt']
        if not all(field in template for field in required_fields):
            print("缺少必要字段: " + ", ".join(required_fields))
            return False

        # 检查 ID 是否已存在
        if self.get_template_by_id(template['id']):
            print(f"模板 ID '{template['id']}' 已存在")
            return False

        # 添加默认字段
        default_fields = {
            'tags': [],
            'duration': '5-10s',
            'elements': {}
        }
        for field, default_value in default_fields.items():
            if field not in template:
                template[field] = default_value

        self.templates.append(template)
        return self._save_templates()

    def update_template(self, template_id: str, updates: Dict) -> bool:
        """
        更新现有模板

        Args:
            template_id: 模板 ID
            updates: 要更新的字段字典

        Returns:
            是否更新成功
        """
        for i, template in enumerate(self.templates):
            if template.get('id') == template_id:
                # 更新字段
                for key, value in updates.items():
                    if key in template:
                        template[key] = value
                return self._save_templates()

        print(f"未找到模板 ID '{template_id}'")
        return False

    def delete_template(self, template_id: str) -> bool:
        """
        删除模板

        Args:
            template_id: 模板 ID

        Returns:
            是否删除成功
        """
        for i, template in enumerate(self.templates):
            if template.get('id') == template_id:
                self.templates.pop(i)
                return self._save_templates()

        print(f"未找到模板 ID '{template_id}'")
        return False

    def get_video_types(self) -> List[str]:
        """获取所有视频类型"""
        types = set()
        for template in self.templates:
            video_type = template.get('video_type')
            if video_type:
                types.add(video_type)
        return sorted(list(types))

    def get_difficulties(self) -> List[str]:
        """获取所有难度级别"""
        difficulties = set()
        for template in self.templates:
            difficulty = template.get('difficulty')
            if difficulty:
                difficulties.add(difficulty)
        return sorted(list(difficulties))

    def get_template_count(self) -> int:
        """获取模板总数"""
        return len(self.templates)

    def get_stats(self) -> Dict:
        """获取模板库统计信息"""
        stats = {
            'total_templates': len(self.templates),
            'video_types': self.get_video_types(),
            'difficulties': self.get_difficulties(),
            'type_distribution': {},
            'difficulty_distribution': {}
        }

        # 统计每个类型的模板数
        for vtype in stats['video_types']:
            stats['type_distribution'][vtype] = len(self.get_templates_by_type(vtype))

        # 统计每个难度的模板数
        for diff in stats['difficulties']:
            stats['difficulty_distribution'][diff] = len(self.get_templates_by_difficulty(diff))

        return stats

    def print_template(self, template: Dict):
        """打印模板信息"""
        print("\n" + "=" * 80)
        print(f"模板名称: {template.get('name', 'N/A')}")
        print(f"模板 ID:  {template.get('id', 'N/A')}")
        print(f"视频类型: {template.get('video_type', 'N/A')}")
        print(f"难度级别: {template.get('difficulty', 'N/A')}")
        print(f"推荐时长: {template.get('duration', 'N/A')}")
        print(f"标签:     {', '.join(template.get('tags', []))}")
        print("-" * 80)
        print("提示词:")
        print(template.get('prompt', 'N/A'))
        print("-" * 80)
        print("元素组成:")
        elements = template.get('elements', {})
        if elements:
            for key, value in elements.items():
                print(f"  {key}: {value}")
        else:
            print("  (无)")
        print("=" * 80 + "\n")


# 便捷函数
def load_templates(data_path: Optional[str] = None) -> TemplateLibrary:
    """加载模板库的便捷函数"""
    return TemplateLibrary(data_path)


def get_template_by_type(video_type: str, difficulty: Optional[str] = None, data_path: Optional[str] = None) -> List[Dict]:
    """根据类型和难度获取模板的便捷函数"""
    lib = TemplateLibrary(data_path)
    if difficulty:
        return lib.get_templates_by_type_and_difficulty(video_type, difficulty)
    else:
        return lib.get_templates_by_type(video_type)


def save_custom_template(template: Dict, data_path: Optional[str] = None) -> bool:
    """保存自定义模板的便捷函数"""
    lib = TemplateLibrary(data_path)
    return lib.save_custom_template(template)


if __name__ == "__main__":
    # 测试代码
    print("=== Seedance 2.0 提示词模板库 ===\n")

    # 加载模板库
    lib = TemplateLibrary()
    print(f"✓ 加载了 {lib.get_template_count()} 个模板\n")

    # 显示统计信息
    stats = lib.get_stats()
    print("📊 统计信息:")
    print(f"  总模板数: {stats['total_templates']}")
    print(f"  视频类型: {', '.join(stats['video_types'])}")
    print(f"  难度级别: {', '.join(stats['difficulties'])}\n")

    # 按类型显示
    print("📁 按类型分布:")
    for vtype, count in stats['type_distribution'].items():
        print(f"  {vtype}: {count} 个")
    print()

    # 按难度显示
    print("🎯 按难度分布:")
    for diff, count in stats['difficulty_distribution'].items():
        print(f"  {diff}: {count} 个")
    print()

    # 获取一个示例模板
    sample = lib.get_template_by_id("photo-realistic-beginner-1")
    if sample:
        lib.print_template(sample)
