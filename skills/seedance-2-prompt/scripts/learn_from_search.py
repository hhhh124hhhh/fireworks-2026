#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从网络搜索学习 Seedance 2.0 提示词
使用 searXNG 搜索并提取有效的提示词模式
"""

import sys
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# 添加脚本路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from smart_expansion import SceneTemplateLibrary, detect_emotion, detect_environment
from search_online import search_prompts

# 配置日志
LOG_DIR = SCRIPT_DIR.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'learn_from_search.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def search_and_learn(
    query: str,
    max_results: int = 10,
    auto_save: bool = True,
    scene_name: Optional[str] = None
) -> Dict:
    """
    搜索 Seedance 2.0 提示词并学习

    Args:
        query: 搜索查询词
        max_results: 最大搜索结果数量
        auto_save: 是否自动保存到模板库
        scene_name: 场景名称（可选，如果未提供则使用 query）

    Returns:
        学习结果字典
    """
    result = {
        'query': query,
        'found': False,
        'results_count': 0,
        'templates_learned': 0,
        'templates': [],
        'errors': []
    }

    try:
        logger.info(f"开始搜索: {query}")

        # 使用 search_online.py 搜索
        search_results = search_prompts(
            query=query,
            video_type="photo-realistic",
            difficulty="INTERMEDIATE",
            max_results=max_results
        )

        if not search_results:
            logger.warning(f"搜索 '{query}' 未返回结果")
            result['errors'].append("搜索未返回结果")
            return result

        result['found'] = True
        result['results_count'] = len(search_results)
        logger.info(f"找到 {len(search_results)} 个结果")

        # 分析搜索结果并提取模板
        learned_templates = []
        scene_name_to_use = scene_name or query

        for idx, search_result in enumerate(search_results):
            try:
                template = _extract_template_from_search(
                    search_result,
                    scene_name=f"{scene_name_to_use}_搜索{idx+1}",
                    query=query
                )

                if template:
                    learned_templates.append(template)
                    logger.info(f"提取模板 {idx+1}: {template.get('name', 'N/A')}")

            except Exception as e:
                logger.error(f"处理搜索结果 {idx+1} 失败: {e}")
                result['errors'].append(f"处理结果 {idx+1} 失败: {str(e)}")

        result['templates'] = learned_templates
        result['templates_learned'] = len(learned_templates)

        # 自动保存到模板库
        if auto_save and learned_templates:
            library = SceneTemplateLibrary()
            saved_count = 0

            for template in learned_templates:
                try:
                    success = library.add_template(
                        name=template['name'],
                        template=template,
                        emotion_type=template.get('emotion')
                    )
                    if success:
                        saved_count += 1
                except Exception as e:
                    logger.error(f"保存模板失败: {e}")
                    result['errors'].append(f"保存模板失败: {str(e)}")

            logger.info(f"已保存 {saved_count}/{len(learned_templates)} 个模板到模板库")

        return result

    except Exception as e:
        logger.error(f"搜索和学习失败: {e}")
        result['errors'].append(f"搜索和学习失败: {str(e)}")
        return result


def _extract_template_from_search(
    search_result: Dict,
    scene_name: str,
    query: str
) -> Optional[Dict]:
    """
    从搜索结果中提取模板

    Args:
        search_result: 搜索结果字典
        scene_name: 场景名称
        query: 原始查询词

    Returns:
        提取的模板字典，如果无法提取则返回 None
    """
    try:
        # 获取提示词文本
        prompt_text = search_result.get('prompt', '')
        if not prompt_text:
            return None

        # 简单的模板提取策略：将整个提示词作为 main_action
        # 更复杂的策略可以解析提示词结构

        # 检测情感和环境
        emotion = detect_emotion(prompt_text)
        environment = detect_environment(prompt_text)

        # 创建模板
        template = {
            "name": scene_name,
            "emotion": emotion,
            "environment": environment,
            "intro": f"从网络搜索 '{query}' 学习到的场景",
            "main_action": prompt_text,
            "emotion_rise": "情感逐渐升级，细节更加丰富",
            "conclusion": "场景收尾，画面淡出",
            "tags": ["网络搜索", query],
            "source": search_result.get('url', 'unknown'),
            "learned_at": datetime.now().isoformat()
        }

        return template

    except Exception as e:
        logger.error(f"提取模板失败: {e}")
        return None


def batch_learn_from_search(
    queries: List[str],
    max_results: int = 10,
    auto_save: bool = True
) -> Dict:
    """
    批量从网络搜索学习

    Args:
        queries: 搜索查询词列表
        max_results: 每个查询的最大结果数量
        auto_save: 是否自动保存到模板库

    Returns:
        批量学习结果字典
    """
    result = {
        'total_queries': len(queries),
        'successful_queries': 0,
        'total_results': 0,
        'total_templates_learned': 0,
        'details': []
    }

    for query in queries:
        logger.info(f"\n批量学习 - 处理查询: {query}")
        learn_result = search_and_learn(query, max_results, auto_save)

        if learn_result['found']:
            result['successful_queries'] += 1
            result['total_results'] += learn_result['results_count']
            result['total_templates_learned'] += learn_result['templates_learned']

        result['details'].append({
            'query': query,
            'success': learn_result['found'],
            'results_count': learn_result['results_count'],
            'templates_learned': learn_result['templates_learned']
        })

    return result


def export_learned_templates(output_path: Optional[str] = None) -> bool:
    """
    导出学习到的模板到 JSON 文件

    Args:
        output_path: 输出文件路径（可选，默认为 learned_templates.json）

    Returns:
        是否导出成功
    """
    try:
        library = SceneTemplateLibrary()

        if output_path is None:
            output_path = SCRIPT_DIR / "data" / "learned_templates.json"

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 导出所有模板
        data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "total_templates": library._count_templates()
            },
            "templates": library.list_templates()
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"已导出模板到 {output_path}")
        return True

    except Exception as e:
        logger.error(f"导出模板失败: {e}")
        return False


if __name__ == "__main__":
    # 测试代码
    print("=== Seedance 2.0 网络搜索学习系统 ===\n")

    # 测试单个查询
    print("📝 测试单个查询学习:")
    test_query = "竹林打斗场景"
    result = search_and_learn(test_query, max_results=3, auto_save=False)

    print(f"  查询: {result['query']}")
    print(f"  找到结果: {result['found']}")
    print(f"  结果数量: {result['results_count']}")
    print(f"  学习模板数: {result['templates_learned']}")
    print()

    if result['templates']:
        print(f"  学习到的模板示例:")
        for i, template in enumerate(result['templates'][:2], 1):
            print(f"    {i}. {template.get('name', 'N/A')}")
            print(f"       情感: {template.get('emotion')}, 环境: {template.get('environment')}")
            print(f"       来源: {template.get('source', 'N/A')}")
        print()

    # 测试批量查询
    print("📚 测试批量查询学习:")
    test_queries = ["浪漫约会", "城市夜景", "武侠打斗"]
    batch_result = batch_learn_from_search(test_queries, max_results=2, auto_save=False)

    print(f"  总查询数: {batch_result['total_queries']}")
    print(f"  成功查询数: {batch_result['successful_queries']}")
    print(f"  总结果数: {batch_result['total_results']}")
    print(f"  总学习模板数: {batch_result['total_templates_learned']}")
    print()

    print("✅ 测试完成！")
