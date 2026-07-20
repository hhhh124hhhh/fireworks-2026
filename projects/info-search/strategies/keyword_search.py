#!/usr/bin/env python3
"""
关键词搜索策略 - 整合多个搜索源

使用 search-wrapper.py 作为后端，提供统一的搜索接口。

使用方法：
    from strategies.keyword_search import KeywordSearch

    searcher = KeywordSearch()
    results = searcher.search("Python 编程", max_results=5)
"""

import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
SCRIPTS_PATH = PROJECT_ROOT / "scripts"

try:
    # 尝试使用相对路径导入
    import sys
    sys.path.insert(0, str(SCRIPTS_PATH))
    import search_wrapper
    search = search_wrapper.search
    search_all_sources = search_wrapper.search_all_sources
except ImportError:
    # 如果相对导入失败，使用绝对导入
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "search_wrapper",
        str(SCRIPTS_PATH / "search-wrapper.py")
    )
    search_wrapper_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search_wrapper_module)
    search = search_wrapper_module.search
    search_all_sources = search_wrapper_module.search_all_sources

# 配置日志
LOG_DIR = Path("/root/clawd/logs/keyword-search")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'keyword-search.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class KeywordSearch:
    """关键词搜索策略"""

    # 支持的搜索源
    AVAILABLE_SOURCES = ["tavily", "baidu", "searxng", "brave"]

    def __init__(self, default_sources: Optional[List[str]] = None):
        """
        初始化搜索器

        Args:
            default_sources: 默认使用的搜索源列表（可选）
                            如果不指定，使用 search-wrapper 的默认 Fallback 顺序
        """
        self.default_sources = default_sources
        logger.info(f"关键词搜索策略初始化完成（默认源: {default_sources or '自动 Fallback'}）")

    def search(
        self,
        query: str,
        max_results: int = 5,
        timeout: int = 30,
        sources: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        执行搜索

        Args:
            query: 搜索关键词
            max_results: 返回结果数量限制
            timeout: 超时时间（秒）
            sources: 指定使用的搜索源（可选）

        Returns:
            统一格式的搜索结果列表

        示例:
            >>> searcher = KeywordSearch()
            >>> results = searcher.search("Python 编程", max_results=5)
            >>> for r in results:
            ...     print(f"{r['title']} - {r['source']}")
        """
        if not query or not query.strip():
            logger.warning("搜索查询为空")
            return []

        # 使用指定的搜索源或默认源
        search_sources = sources or self.default_sources

        logger.info(f"关键词搜索: '{query}' (max={max_results}, sources={search_sources or 'auto'})")

        # 调用 search-wrapper
        results = search(
            query=query,
            max_results=max_results,
            timeout=timeout,
            sources=search_sources
        )

        # 添加搜索元数据
        timestamp = datetime.now().isoformat()
        for result in results:
            result['search_query'] = query
            result['search_timestamp'] = timestamp
            result['search_strategy'] = 'keyword'

        logger.info(f"返回 {len(results)} 个结果")
        return results

    def search_all(
        self,
        query: str,
        max_results: int = 5,
        timeout: int = 30
    ) -> Dict[str, List[Dict]]:
        """
        尝试所有搜索源

        Args:
            query: 搜索关键词
            max_results: 返回结果数量限制
            timeout: 超时时间（秒）

        Returns:
            字典，键为搜索源名称，值为结果列表

        示例:
            >>> searcher = KeywordSearch()
            >>> all_results = searcher.search_all("Python 编程")
            >>> for source, results in all_results.items():
            ...     print(f"{source}: {len(results)} 个结果")
        """
        logger.info(f"尝试所有搜索源: '{query}'")

        all_results = search_all_sources(query, max_results, timeout)

        # 添加搜索元数据
        timestamp = datetime.now().isoformat()
        for source_name, results in all_results.items():
            for result in results:
                result['search_query'] = query
                result['search_timestamp'] = timestamp
                result['search_strategy'] = 'keyword'

        return all_results

    def save_results(self, results: List[Dict], output_file: str):
        """
        保存搜索结果到文件

        Args:
            results: 搜索结果列表
            output_file: 输出文件路径

        示例:
            >>> searcher = KeywordSearch()
            >>> results = searcher.search("Python 编程")
            >>> searcher.save_results(results, "output.json")
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        logger.info(f"结果已保存到: {output_path}")

    def format_results(self, results: List[Dict], format: str = "text") -> str:
        """
        格式化搜索结果

        Args:
            results: 搜索结果列表
            format: 格式类型（text, json, markdown）

        Returns:
            格式化的字符串

        示例:
            >>> searcher = KeywordSearch()
            >>> results = searcher.search("Python 编程")
            >>> print(searcher.format_results(results, format="markdown"))
        """
        if format == "json":
            return json.dumps(results, ensure_ascii=False, indent=2)

        elif format == "markdown":
            output = []
            output.append(f"# 搜索结果（共 {len(results)} 条）\n")
            for i, result in enumerate(results, 1):
                output.append(f"## {i}. {result['title']}")
                output.append(f"- **来源**: {result['source']}")
                output.append(f"- **URL**: {result['url']}")
                if result.get('content'):
                    output.append(f"- **内容**: {result['content'][:200]}...")
                output.append("")
            return "\n".join(output)

        else:  # text (默认)
            output = []
            output.append(f"找到 {len(results)} 个结果:\n")
            for i, result in enumerate(results, 1):
                output.append(f"[{i}] {result['title']}")
                output.append(f"    来源: {result['source']}")
                output.append(f"    URL: {result['url']}")
                if result.get('content'):
                    output.append(f"    内容: {result['content'][:100]}...")
                output.append("")
            return "\n".join(output)


def main():
    """
    命令行入口

    用法:
        python3 keyword_search.py <query> [options]

    选项:
        -n, --num-results NUM     结果数量（默认: 5）
        -s, --sources SOURCES     搜索源，逗号分隔（如: tavily,baidu,searxng）
        -a, --all                 尝试所有搜索源
        -o, --output FILE         保存结果到文件
        -f, --format FORMAT       输出格式（text, json, markdown）
        -v, --verbose             显示详细内容

    示例:
        python3 keyword_search.py "Python 编程"
        python3 keyword_search.py "AI 技术" -n 10 -s tavily,baidu
        python3 keyword_search.py "机器学习" --all -o results.json -f json
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="关键词搜索策略 - 整合多个搜索源",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 keyword_search.py "Python 编程"
  python3 keyword_search.py "AI 技术" -n 10 -s tavily,baidu
  python3 keyword_search.py "机器学习" --all -o results.json -f json
        """
    )

    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("-n", "--num-results", type=int, default=5,
                        help="结果数量（默认: 5）")
    parser.add_argument("-s", "--sources", help="搜索源，逗号分隔（如: tavily,baidu,searxng）")
    parser.add_argument("-a", "--all", action="store_true",
                        help="尝试所有搜索源")
    parser.add_argument("-o", "--output", help="保存结果到文件")
    parser.add_argument("-f", "--format", choices=["text", "json", "markdown"],
                        default="text", help="输出格式（默认: text）")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="显示详细内容")

    args = parser.parse_args()

    # 解析搜索源
    sources = None
    if args.sources:
        sources = [s.strip() for s in args.sources.split(",")]
        # 验证搜索源
        invalid_sources = [s for s in sources if s not in KeywordSearch.AVAILABLE_SOURCES]
        if invalid_sources:
            print(f"错误: 无效的搜索源: {', '.join(invalid_sources)}")
            print(f"可用的搜索源: {', '.join(KeywordSearch.AVAILABLE_SOURCES)}")
            sys.exit(1)

    # 创建搜索器
    searcher = KeywordSearch()

    # 执行搜索
    if args.all:
        print(f"尝试所有搜索源: '{args.query}'\n")
        all_results = searcher.search_all(args.query, args.num_results)

        # 显示所有搜索源的结果
        for source_name, results in all_results.items():
            print(f"\n{'='*80}")
            print(f"{source_name.upper()} ({len(results)} 个结果):")
            print('='*80)
            if results:
                formatted = searcher.format_results(results, args.format)
                print(formatted)
            else:
                print("无结果\n")
    else:
        print(f"搜索: '{args.query}'\n")
        results = searcher.search(args.query, args.num_results, sources=sources)

        # 格式化输出
        formatted = searcher.format_results(results, args.format)
        print(formatted)

        # 保存结果
        if args.output:
            searcher.save_results(results, args.output)
            print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    main()
