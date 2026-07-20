#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 模板更新模块
从指定 URL 或搜索结果获取最新模板，更新本地模板库
"""

import sys
import json
import logging
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# 导入 web_fetch 功能
try:
    # 尝试导入 web_fetch（如果可用）
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # 这里只是类型检查，实际使用时会通过其他方式
        pass
    WEB_FETCH_AVAILABLE = False
except ImportError:
    WEB_FETCH_AVAILABLE = False

# 添加 info-search 脚本路径到 Python 路径（用于搜索）
INFO_SEARCH_SCRIPTS = Path("/root/clawd/projects/info-search/scripts")
sys.path.insert(0, str(INFO_SEARCH_SCRIPTS))

# 导入 search_wrapper（可选）
try:
    from search_wrapper import search
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False

# 配置日志
LOG_DIR = Path("/root/clawd/skills/seedance-2-prompt/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'update_templates.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# 模板库路径
TEMPLATE_DATA_PATH = Path("/root/clawd/skills/seedance-2-prompt/data/templates.json")


class TemplateUpdater:
    """模板更新器"""

    def __init__(self):
        """初始化模板更新器"""
        self.templates = self._load_local_templates()
        self.update_stats = {
            'added': 0,
            'updated': 0,
            'skipped': 0,
            'failed': 0
        }

    def _load_local_templates(self) -> Dict:
        """
        加载本地模板库

        Returns:
            模板库字典
        """
        try:
            if TEMPLATE_DATA_PATH.exists():
                with open(TEMPLATE_DATA_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 如果文件不存在，返回空字典
                return {'templates': [], 'last_updated': None}
        except Exception as e:
            logger.error(f"加载本地模板失败: {str(e)}")
            return {'templates': [], 'last_updated': None}

    def _save_local_templates(self):
        """保存本地模板库"""
        try:
            # 确保目录存在
            TEMPLATE_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

            # 添加更新时间戳
            self.templates['last_updated'] = datetime.now().isoformat()

            # 保存到文件
            with open(TEMPLATE_DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, ensure_ascii=False, indent=2)

            logger.info(f"模板库已保存到: {TEMPLATE_DATA_PATH}")

        except Exception as e:
            logger.error(f"保存本地模板失败: {str(e)}")
            raise

    def _generate_template_id(self, template: Dict) -> str:
        """
        为模板生成唯一 ID

        Args:
            template: 模板数据

        Returns:
            唯一 ID
        """
        # 使用提示词内容生成哈希值
        content = template.get('prompt', '')
        if content:
            hash_value = hashlib.md5(content.encode('utf-8')).hexdigest()[:8]
            return f"online-{hash_value}"

        # 如果没有提示词，使用标题生成
        title = template.get('title', '')
        if title:
            hash_value = hashlib.md5(title.encode('utf-8')).hexdigest()[:8]
            return f"online-{hash_value}"

        # 最后使用时间戳
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"online-{timestamp}"

    def _template_exists(self, template_id: str) -> bool:
        """
        检查模板是否已存在

        Args:
            template_id: 模板 ID

        Returns:
            是否存在
        """
        for t in self.templates.get('templates', []):
            if t.get('id') == template_id:
                return True
        return False

    def _normalize_template(self, template: Dict) -> Dict:
        """
        标准化模板格式

        Args:
            template: 原始模板数据

        Returns:
            标准化后的模板数据
        """
        normalized = {
            'id': template.get('id') or self._generate_template_id(template),
            'name': template.get('name', '未命名模板'),
            'title': template.get('title', ''),
            'prompt': template.get('prompt', ''),
            'video_type': template.get('video_type', 'photo-realistic'),
            'difficulty': template.get('difficulty', 'INTERMEDIATE'),
            'description': template.get('description', ''),
            'tags': template.get('tags', []),
            'duration': template.get('duration', '5-10s'),
            'source': template.get('source', 'online'),
            'created_at': template.get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat()
        }

        return normalized

    def fetch_templates_from_url(self, url: str) -> List[Dict]:
        """
        从指定 URL 获取模板

        注意：此功能依赖于 web_fetch 工具，当前未实现
        实际使用时需要集成 web_fetch 功能

        Args:
            url: 模板来源 URL

        Returns:
            模板列表
        """
        logger.warning(f"从 URL 获取模板功能尚未实现: {url}")
        logger.info("建议使用 --search 选项来搜索在线提示词")

        # 这里是伪代码，实际使用时需要集成 web_fetch
        # content = web_fetch(url)
        # templates = parse_templates_from_content(content)
        # return templates

        return []

    def fetch_templates_from_search(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        从搜索结果获取模板

        Args:
            query: 搜索查询
            max_results: 最大结果数量

        Returns:
            模板列表
        """
        if not SEARCH_AVAILABLE:
            logger.error("搜索功能不可用，无法获取模板")
            return []

        logger.info(f"通过搜索获取模板: {query}")

        try:
            # 使用 search-wrapper 搜索
            results = search(query, max_results=max_results)

            # 转换搜索结果为模板格式
            templates = []
            for result in results:
                if result.get('source') == 'error':
                    continue

                template = {
                    'name': result.get('title', '未命名模板')[:100],
                    'title': result.get('title', ''),
                    'prompt': result.get('content', '')[:500],
                    'video_type': self._extract_video_type(result.get('title', '') + ' ' + result.get('content', '')),
                    'difficulty': self._extract_difficulty(result.get('title', '') + ' ' + result.get('content', '')),
                    'description': result.get('content', '')[:300],
                    'tags': self._extract_tags(result.get('title', '') + ' ' + result.get('content', '')),
                    'source': 'online-search',
                    'url': result.get('url', '')
                }

                templates.append(template)

            logger.info(f"从搜索结果获取 {len(templates)} 个模板")
            return templates

        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            return []

    def _extract_video_type(self, text: str) -> str:
        """
        从文本中提取视频类型

        Args:
            text: 文本内容

        Returns:
            视频类型
        """
        video_types = {
            "photo-realistic": ["超逼真", "写实", "photorealistic"],
            "character-consistency": ["角色", "人物", "character"],
            "camera-movement": ["运镜", "镜头", "camera"],
            "creative-effects": ["特效", "创意", "effects"],
            "storytelling": ["剧情", "故事", "story"],
            "audio-sync": ["音频", "声音", "audio"],
            "one-shot": ["一镜", "单镜头", "one shot"],
            "emotion-performance": ["情绪", "表演", "emotion"]
        }

        text_lower = text.lower()

        for video_type, keywords in video_types.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    return video_type

        return "photo-realistic"

    def _extract_difficulty(self, text: str) -> str:
        """
        从文本中提取难度级别

        Args:
            text: 文本内容

        Returns:
            难度级别
        """
        if "初学者" in text or "简单" in text or "入门" in text or "beginner" in text.lower():
            return "BEGINNER"
        elif "高级" in text or "复杂" in text or "advanced" in text.lower():
            return "ADVANCED"
        elif "专家" in text or "极致" in text or "expert" in text.lower():
            return "EXPERT"

        return "INTERMEDIATE"

    def _extract_tags(self, text: str) -> List[str]:
        """
        从文本中提取标签

        Args:
            text: 文本内容

        Returns:
            标签列表
        """
        common_tags = [
            "Seedance 2.0", "AI", "视频", "提示词",
            "photo-realistic", "camera", "lighting"
        ]

        tags = []
        text_lower = text.lower()

        for tag in common_tags:
            if tag.lower() in text_lower:
                tags.append(tag)

        return tags

    def update_local_templates(self, new_templates: List[Dict], force: bool = False) -> int:
        """
        更新本地模板库

        Args:
            new_templates: 新模板列表
            force: 是否强制更新（覆盖已存在的模板）

        Returns:
            更新的模板数量
        """
        logger.info(f"开始更新模板库，新模板数量: {len(new_templates)}")

        for new_template in new_templates:
            try:
                # 标准化模板
                normalized = self._normalize_template(new_template)
                template_id = normalized['id']

                # 检查模板是否已存在
                if self._template_exists(template_id):
                    if not force:
                        logger.info(f"跳过已存在的模板: {template_id}")
                        self.update_stats['skipped'] += 1
                        continue
                    else:
                        logger.info(f"更新已存在的模板: {template_id}")
                        # 移除旧模板
                        self.templates['templates'] = [
                            t for t in self.templates['templates']
                            if t.get('id') != template_id
                        ]
                        self.update_stats['updated'] += 1
                else:
                    logger.info(f"添加新模板: {template_id}")
                    self.update_stats['added'] += 1

                # 添加到模板库
                self.templates['templates'].append(normalized)

            except Exception as e:
                logger.error(f"处理模板失败: {str(e)}")
                self.update_stats['failed'] += 1

        # 保存更新后的模板库
        self._save_local_templates()

        # 打印统计信息
        logger.info("更新统计:")
        logger.info(f"  - 新增: {self.update_stats['added']}")
        logger.info(f"  - 更新: {self.update_stats['updated']}")
        logger.info(f"  - 跳过: {self.update_stats['skipped']}")
        logger.info(f"  - 失败: {self.update_stats['failed']}")
        logger.info(f"  - 当前模板总数: {len(self.templates.get('templates', []))}")

        return self.update_stats['added'] + self.update_stats['updated']

    def get_stats(self) -> Dict:
        """
        获取更新统计信息

        Returns:
            统计信息字典
        """
        return self.update_stats.copy()


def update_from_url(url: str, force: bool = False):
    """
    从 URL 更新模板

    Args:
        url: 模板来源 URL
        force: 是否强制更新
    """
    print("\n" + "=" * 80)
    print("📥 Seedance 2.0 模板更新（从 URL）")
    print("=" * 80 + "\n")

    print(f"URL: {url}")
    print(f"强制更新: {'是' if force else '否'}")
    print("\n" + "-" * 80)
    print("🚀 正在获取模板...")
    print("-" * 80 + "\n")

    updater = TemplateUpdater()

    # 从 URL 获取模板
    templates = updater.fetch_templates_from_url(url)

    if not templates:
        print("❌ 未获取到模板")
        print("\n可能的原因:")
        print("  - URL 不正确")
        print("  - web_fetch 功能未实现")
        print("\n建议:")
        print("  - 使用 --search 选项来搜索在线提示词")
        return

    # 更新模板库
    count = updater.update_local_templates(templates, force)

    # 显示统计信息
    stats = updater.get_stats()
    print("\n" + "=" * 80)
    print(f"✅ 模板更新完成，共更新 {count} 个模板")
    print("=" * 80)
    print(f"新增: {stats['added']}")
    print(f"更新: {stats['updated']}")
    print(f"跳过: {stats['skipped']}")
    print(f"失败: {stats['failed']}")


def update_from_search(
    query: str,
    max_results: int = 10,
    force: bool = False
):
    """
    从搜索结果更新模板

    Args:
        query: 搜索查询
        max_results: 最大结果数量
        force: 是否强制更新
    """
    print("\n" + "=" * 80)
    print("📥 Seedance 2.0 模板更新（从搜索）")
    print("=" * 80 + "\n")

    print(f"搜索查询: {query}")
    print(f"最大结果数: {max_results}")
    print(f"强制更新: {'是' if force else '否'}")
    print("\n" + "-" * 80)
    print("🚀 正在搜索...")
    print("-" * 80 + "\n")

    updater = TemplateUpdater()

    # 从搜索获取模板
    templates = updater.fetch_templates_from_search(query, max_results)

    if not templates:
        print("❌ 未获取到模板")
        print("\n可能的原因:")
        print("  - 搜索关键词不匹配")
        print("  - 搜索源不可用")
        print("\n建议:")
        print("  - 尝试使用更通用的关键词")
        print("  - 检查 search-wrapper 配置")
        return

    print(f"\n✅ 成功获取 {len(templates)} 个模板\n")

    # 显示预览
    print("-" * 80)
    print("模板预览:")
    print("-" * 80)
    for i, template in enumerate(templates[:3], 1):
        print(f"\n[{i}] {template.get('name', '未命名')}")
        print(f"    类型: {template.get('video_type')}")
        print(f"    难度: {template.get('difficulty')}")
        print(f"    提示词: {template.get('prompt', '')[:100]}...")

    # 询问用户是否继续
    print(f"\n还有 {len(templates) - 3} 个模板未显示")
    choice = input("\n是否继续更新模板库? (y/N): ").strip().lower()

    if choice != 'y':
        print("已取消更新")
        return

    # 更新模板库
    print("\n" + "-" * 80)
    print("正在更新模板库...")
    print("-" * 80 + "\n")

    count = updater.update_local_templates(templates, force)

    # 显示统计信息
    stats = updater.get_stats()
    print("\n" + "=" * 80)
    print(f"✅ 模板更新完成，共更新 {count} 个模板")
    print("=" * 80)
    print(f"新增: {stats['added']}")
    print(f"更新: {stats['updated']}")
    print(f"跳过: {stats['skipped']}")
    print(f"失败: {stats['failed']}")


def main():
    """
    命令行入口

    用法:
        python3 update_templates.py --url <URL> [options]
        python3 update_templates.py --search <query> [options]

    选项:
        --url <URL>: 从指定 URL 获取模板
        --search <query>: 搜索并添加新模板
        -n, --num <max_results>: 最大结果数量（仅用于 --search）
        -f, --force: 强制更新（覆盖已存在的模板）

    示例:
        python3 update_templates.py --url https://example.com/templates
        python3 update_templates.py --search "最新 Seedance 2.0 提示词" -n 10
    """
    if len(sys.argv) < 3:
        print("用法: python3 update_templates.py --url <URL> [options]")
        print("      python3 update_templates.py --search <query> [options]")
        print("")
        print("选项:")
        print("  --url <URL>                   从指定 URL 获取模板")
        print("  --search <query>              搜索并添加新模板")
        print("  -n, --num <max_results>       最大结果数量（仅用于 --search，默认: 10）")
        print("  -f, --force                  强制更新（覆盖已存在的模板）")
        print("")
        print("示例:")
        print("  python3 update_templates.py --url https://example.com/templates")
        print("  python3 update_templates.py --search '最新 Seedance 2.0 提示词' -n 10")
        print("  python3 update_templates.py --search '人物肖像' -f")
        sys.exit(1)

    # 解析参数
    url = None
    search_query = None
    max_results = 10
    force = False

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]

        if arg == '--url' and i + 1 < len(sys.argv):
            url = sys.argv[i + 1]
            i += 2
        elif arg == '--search' and i + 1 < len(sys.argv):
            search_query = sys.argv[i + 1]
            i += 2
        elif arg in ['-n', '--num'] and i + 1 < len(sys.argv):
            try:
                max_results = int(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"错误: 无效的结果数量 '{sys.argv[i + 1]}'")
                sys.exit(1)
        elif arg in ['-f', '--force']:
            force = True
            i += 1
        else:
            i += 1

    # 执行更新
    if url:
        update_from_url(url, force)
    elif search_query:
        update_from_search(search_query, max_results, force)
    else:
        print("错误: 必须指定 --url 或 --search")
        sys.exit(1)


if __name__ == "__main__":
    main()
