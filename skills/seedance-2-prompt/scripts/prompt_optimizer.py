#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 提示词优化器
优化和改进用户输入的提示词
"""

import re
from typing import Dict, List, Optional
from template_library import TemplateLibrary


class PromptOptimizer:
    """提示词优化器"""

    # 万能公式的 8 个元素
    FORMULA_ELEMENTS = [
        "subject",      # 主体
        "action",       # 动作
        "scene",        # 场景
        "lighting",     # 光影
        "camera",       # 镜头语言
        "style",        # 风格
        "quality",      # 画质
        "constraints"   # 约束
    ]

    # 元素关键词库
    ELEMENT_KEYWORDS = {
        "lighting": [
            "光", "光效", "光影", "光线", "明暗", "对比度",
            "自然光", "晨光", "夕照", "灯光", "烛光", "霓虹"
        ],
        "camera": [
            "镜头", "特写", "中景", "远景", "广角", "跟拍",
            "推", "拉", "摇", "移", "升", "降", "环绕", "俯拍", "仰拍"
        ],
        "style": [
            "风格", "写实", "梦幻", "艺术", "科幻", "奇幻", "复古", "现代"
        ],
        "quality": [
            "画质", "高清", "4K", "8K", "电影级", "HDR", "超清", "精细"
        ],
        "constraints": [
            "流畅", "自然", "真实", "物理", "稳定", "连贯", "准确"
        ]
    }

    # 优化建议
    OPTIMIZATION_SUGGESTIONS = {
        "missing_subject": "建议添加明确的主体描述",
        "missing_action": "建议添加动作描述，让画面更生动",
        "missing_scene": "建议添加场景环境描述",
        "missing_lighting": "建议添加光影描述，增强画面氛围",
        "missing_camera": "建议添加镜头语言，指定拍摄角度或运镜方式",
        "missing_style": "建议添加风格描述，明确视频的整体风格",
        "missing_quality": "建议添加画质要求，如高清、4K等",
        "missing_constraints": "建议添加约束条件，如流畅、自然等",
        "too_short": "提示词过短，建议添加更多细节",
        "too_vague": "描述过于笼统，建议使用更具体的词语",
        "no_emotion": "可以添加情绪描述，增强情感表达",
        "no_temporal": "可以添加时间元素，如白天、夜晚等"
    }

    def __init__(self, template_lib: Optional[TemplateLibrary] = None):
        """
        初始化提示词优化器

        Args:
            template_lib: 模板库实例
        """
        self.template_lib = template_lib or TemplateLibrary()

    def optimize_prompt(
        self,
        user_prompt: str,
        difficulty: str = "INTERMEDIATE",
        auto_complete: bool = False
    ) -> Dict:
        """
        优化用户输入的提示词

        Args:
            user_prompt: 用户输入的提示词
            difficulty: 目标难度级别
            auto_complete: 是否自动补全缺失元素

        Returns:
            包含优化结果的字典
        """
        # 分析现有提示词
        analysis = self._analyze_prompt(user_prompt)

        # 生成优化建议
        suggestions = self._generate_suggestions(analysis, difficulty)

        # 根据万能公式补全提示词
        completed_prompt = self._complete_formula_prompt(user_prompt, analysis, difficulty)

        # 生成变体
        variants = self._generate_optimized_variants(user_prompt, analysis, difficulty)

        # 计算评分
        score = self._calculate_score(analysis, difficulty)

        result = {
            'original_prompt': user_prompt,
            'optimized_prompt': completed_prompt,
            'analysis': analysis,
            'suggestions': suggestions,
            'variants': variants,
            'score': score,
            'difficulty': difficulty
        }

        return result

    def _analyze_prompt(self, prompt: str) -> Dict:
        """
        分析提示词，提取现有元素

        Args:
            prompt: 提示词文本

        Returns:
            分析结果字典
        """
        analysis = {
            'length': len(prompt),
            'word_count': len(prompt.split()),
            'detected_elements': [],
            'missing_elements': [],
            'found_keywords': {},
            'issues': []
        }

        prompt_lower = prompt.lower()

        # 检测每个元素
        for element in self.FORMULA_ELEMENTS:
            if element == "subject" or element == "action":
                # 主体和动作难以用关键词检测，假设存在
                if len(prompt) > 5:
                    analysis['detected_elements'].append(element)
                    analysis['found_keywords'][element] = ["隐含"]
                else:
                    analysis['missing_elements'].append(element)
            else:
                # 检查关键词
                keywords = self.ELEMENT_KEYWORDS.get(element, [])
                found = [kw for kw in keywords if kw in prompt_lower]

                if found:
                    analysis['detected_elements'].append(element)
                    analysis['found_keywords'][element] = found
                else:
                    analysis['missing_elements'].append(element)

        # 其他分析
        if analysis['word_count'] < 5:
            analysis['issues'].append("too_short")
        else:
            analysis['issues'] = []

        return analysis

    def _generate_suggestions(self, analysis: Dict, difficulty: str) -> List[str]:
        """
        生成优化建议

        Args:
            analysis: 分析结果
            difficulty: 难度级别

        Returns:
            建议列表
        """
        suggestions = []

        # 根据缺失元素生成建议
        for element in analysis['missing_elements']:
            suggestion_key = f"missing_{element}"
            if suggestion_key in self.OPTIMIZATION_SUGGESTIONS:
                suggestions.append(self.OPTIMIZATION_SUGGESTIONS[suggestion_key])

        # 根据问题生成建议
        for issue in analysis.get('issues', []):
            if issue in self.OPTIMIZATION_SUGGESTIONS:
                suggestions.append(self.OPTIMIZATION_SUGGESTIONS[issue])

        # 根据难度调整建议
        if difficulty == "BEGINNER":
            # 初学者：只建议基本元素
            suggestions = [s for s in suggestions if any(
                kw in s for kw in ["主体", "动作", "场景"]
            )]
        elif difficulty in ["ADVANCED", "EXPERT"]:
            # 高级和专家：建议所有元素
            pass

        return suggestions

    def complete_formula_prompt(
        self,
        user_prompt: str,
        difficulty: str = "INTERMEDIATE"
    ) -> Dict:
        """
        根据万能公式补全提示词（公开接口）

        Args:
            user_prompt: 用户提示词
            difficulty: 难度级别

        Returns:
            补全结果字典
        """
        analysis = self._analyze_prompt(user_prompt)
        completed = self._complete_formula_prompt(user_prompt, analysis, difficulty)

        return {
            'original': user_prompt,
            'completed': completed,
            'analysis': analysis
        }

    def _complete_formula_prompt(
        self,
        user_prompt: str,
        analysis: Dict,
        difficulty: str
    ) -> str:
        """
        根据万能公式补全提示词（内部实现）

        Args:
            user_prompt: 用户提示词
            analysis: 分析结果
            difficulty: 难度级别

        Returns:
            补全后的提示词
        """
        completed = user_prompt

        # 根据难度决定补全哪些元素
        elements_to_add = []

        if difficulty == "BEGINNER":
            # 初学者：只补全风格和画质
            if "style" in analysis['missing_elements']:
                elements_to_add.append("写实风格")
            if "quality" in analysis['missing_elements']:
                elements_to_add.append("高清")

        elif difficulty == "INTERMEDIATE":
            # 中级：补全光影、镜头、风格、画质
            for element in ["lighting", "camera", "style", "quality"]:
                if element in analysis['missing_elements']:
                    elements_to_add.append(self._get_element_suggestion(element))

        elif difficulty in ["ADVANCED", "EXPERT"]:
            # 高级和专家：补全所有元素
            for element in analysis['missing_elements']:
                if element not in ["subject", "action"]:
                    elements_to_add.append(self._get_element_suggestion(element))

        # 添加补全的元素
        if elements_to_add:
            completed += "，" + "，".join(elements_to_add) + "。"

        return completed

    def _get_element_suggestion(self, element: str) -> str:
        """
        获取元素的默认建议

        Args:
            element: 元素名称

        Returns:
            建议文本
        """
        suggestions = {
            "lighting": "柔和光线",
            "camera": "自然镜头",
            "style": "写实风格",
            "quality": "高清",
            "constraints": "流畅自然"
        }
        return suggestions.get(element, "")

    def generate_variants(
        self,
        prompt: str,
        count: int = 3,
        difficulty: str = "INTERMEDIATE"
    ) -> List[Dict]:
        """
        生成提示词变体（公开接口）

        Args:
            prompt: 原始提示词
            count: 变体数量
            difficulty: 难度级别

        Returns:
            变体列表
        """
        analysis = self._analyze_prompt(prompt)
        variants = self._generate_optimized_variants(prompt, analysis, difficulty, count)

        return [
            {
                'variant': variant,
                'changes': self._describe_changes(prompt, variant, analysis)
            }
            for variant in variants
        ]

    def _generate_optimized_variants(
        self,
        prompt: str,
        analysis: Dict,
        difficulty: str,
        count: int = 3
    ) -> List[str]:
        """
        生成优化变体（内部实现）

        Args:
            prompt: 原始提示词
            analysis: 分析结果
            difficulty: 难度级别
            count: 变体数量

        Returns:
            变体列表
        """
        variants = []

        # 变体1：添加更多描述性词汇
        variant1 = self._enhance_descriptiveness(prompt, analysis)
        variants.append(variant1)

        # 变体2：调整风格
        variant2 = self._change_style(prompt, analysis)
        variants.append(variant2)

        # 变体3：补充缺失元素
        variant3 = self._complete_formula_prompt(prompt, analysis, difficulty)
        variants.append(variant3)

        return variants[:count]

    def _enhance_descriptiveness(self, prompt: str, analysis: Dict) -> str:
        """增强描述性"""
        enhanced = prompt

        # 添加常见的增强词汇
        if "优雅地" not in enhanced:
            enhanced = enhanced.replace("，", "，优雅地", 1)

        if "细腻地" not in enhanced and len(enhanced) > 20:
            enhanced = enhanced.replace("，", "，细腻地", 1)

        return enhanced

    def _change_style(self, prompt: str, analysis: Dict) -> str:
        """改变风格"""
        # 尝试添加或修改风格描述
        style_variations = [
            "梦幻风格",
            "电影风格",
            "艺术风格",
            "写实风格",
            "科幻风格"
        ]

        for style in style_variations:
            if style not in prompt:
                changed = prompt + "，" + style
                return changed

        return prompt

    def _describe_changes(self, original: str, variant: str, analysis: Dict) -> List[str]:
        """描述变体的变化"""
        changes = []

        if len(variant) > len(original):
            changes.append(f"增加了 {len(variant) - len(original)} 个字符")

        if "风格" in variant and "风格" not in original:
            changes.append("添加了风格描述")

        if "光线" in variant and "光线" not in original:
            changes.append("添加了光影描述")

        if "镜头" in variant and "镜头" not in original:
            changes.append("添加了镜头语言")

        if not changes:
            changes.append("轻微调整措辞")

        return changes

    def _calculate_score(self, analysis: Dict, difficulty: str) -> Dict:
        """
        计算提示词评分

        Args:
            analysis: 分析结果
            difficulty: 难度级别

        Returns:
            评分字典
        """
        # 基础分
        base_score = 60

        # 元素完整性加分
        total_elements = len(self.FORMULA_ELEMENTS)
        detected_elements = len(analysis['detected_elements'])
        element_score = int((detected_elements / total_elements) * 30)

        # 字数加分
        word_count = analysis['word_count']
        if word_count >= 10:
            word_score = 10
        elif word_count >= 5:
            word_score = 5
        else:
            word_score = 0

        # 计算总分
        total_score = base_score + element_score + word_score
        total_score = min(100, total_score)  # 限制最高100分

        # 根据难度调整
        if difficulty == "BEGINNER":
            total_score = min(100, total_score + 10)
        elif difficulty == "EXPERT":
            total_score = max(50, total_score - 10)

        return {
            'total': total_score,
            'elements': element_score,
            'length': word_score,
            'base': base_score,
            'detected_elements': detected_elements,
            'total_elements': total_elements
        }

    def print_optimization_report(self, result: Dict):
        """打印优化报告"""
        print("\n" + "=" * 80)
        print("📊 提示词优化报告")
        print("=" * 80 + "\n")

        # 原始提示词
        print("原始提示词:")
        print("-" * 80)
        print(result['original_prompt'])
        print()

        # 评分
        score = result['score']
        print(f"评分: {score['total']}/100")
        print(f"  - 元素完整性: {score['detected_elements']}/{score['total_elements']} (+{score['elements']})")
        print(f"  - 字数长度: {score['length']}")
        print()

        # 优化后的提示词
        print("优化后的提示词:")
        print("-" * 80)
        print(result['optimized_prompt'])
        print()

        # 建议和缺失元素
        if result.get('suggestions'):
            print("💡 优化建议:")
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"  {i}. {suggestion}")
            print()

        # 变体
        if result.get('variants'):
            print("🔄 提示词变体:")
            for i, variant in enumerate(result['variants'], 1):
                print(f"\n  变体 {i}:")
                print(f"  {variant}")
            print()

        # 分析详情
        analysis = result['analysis']
        print("🔍 分析详情:")
        print(f"  - 字数: {analysis['word_count']} 字")
        print(f"  - 已检测元素: {', '.join(analysis['detected_elements'])}")
        print(f"  - 缺失元素: {', '.join(analysis['missing_elements'])}")
        print()


# 便捷函数
def optimize_prompt(user_prompt: str, difficulty: str = "INTERMEDIATE", auto_complete: bool = False) -> Dict:
    """优化提示词的便捷函数"""
    optimizer = PromptOptimizer()
    return optimizer.optimize_prompt(user_prompt, difficulty, auto_complete)


def complete_formula_prompt(user_prompt: str, difficulty: str = "INTERMEDIATE") -> Dict:
    """补全万能公式提示词的便捷函数"""
    optimizer = PromptOptimizer()
    return optimizer.complete_formula_prompt(user_prompt, difficulty)


def generate_variants(prompt: str, count: int = 3, difficulty: str = "INTERMEDIATE") -> List[Dict]:
    """生成变体的便捷函数"""
    optimizer = PromptOptimizer()
    return optimizer.generate_variants(prompt, count, difficulty)


if __name__ == "__main__":
    # 测试代码
    print("=== Seedance 2.0 提示词优化器 ===\n")

    # 示例1：优化提示词
    print("示例1: 优化提示词")
    print("-" * 80)

    test_prompt = "一位女士在花园里"
    print(f"原始提示词: {test_prompt}\n")

    optimizer = PromptOptimizer()
    result = optimizer.optimize_prompt(test_prompt, difficulty="INTERMEDIATE")
    optimizer.print_optimization_report(result)

    # 示例2：交互式优化
    print("\n" + "=" * 80)
    print("是否优化自己的提示词? (y/N): ")
    choice = input().strip().lower()
    if choice == 'y':
        print("\n请输入你的提示词:")
        user_prompt = input("> ").strip()

        if user_prompt:
            print("\n选择难度级别 (1-4, 默认2):")
            print("  1. BEGINNER (初学者)")
            print("  2. INTERMEDIATE (中级)")
            print("  3. ADVANCED (高级)")
            print("  4. EXPERT (专家)")
            level_choice = input("> ").strip() or "2"

            difficulty_map = {"1": "BEGINNER", "2": "INTERMEDIATE", "3": "ADVANCED", "4": "EXPERT"}
            difficulty = difficulty_map.get(level_choice, "INTERMEDIATE")

            result = optimizer.optimize_prompt(user_prompt, difficulty=difficulty)
            optimizer.print_optimization_report(result)
