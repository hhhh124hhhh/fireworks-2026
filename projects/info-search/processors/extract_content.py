#!/usr/bin/env python3
"""
内容提取器 - 从 URL 提取主要内容

使用内置的 web_fetch 工具从 URL 提取内容，支持批量提取。

使用方法：
    from processors.extract_content import ContentExtractor

    extractor = ContentExtractor()
    results = extractor.extract(["https://example.com/page1", "https://example.com/page2"])
"""

import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime
import traceback

# 配置日志
LOG_DIR = Path("/root/clawd/logs/extract-content")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'extract-content.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class ContentExtractor:
    """内容提取器 - 从 URL 提取主要内容"""

    def __init__(self, default_format: str = "markdown"):
        """
        初始化内容提取器

        Args:
            default_format: 默认输出格式（markdown 或 text）
        """
        self.default_format = default_format
        logger.info(f"内容提取器初始化完成（默认格式: {default_format}）")

    def _extract_single_url(self, url: str, extract_mode: str = "markdown", max_chars: int = 100000) -> Dict:
        """
        从单个 URL 提取内容（内部方法）

        Args:
            url: 要提取的 URL
            extract_mode: 提取模式（markdown 或 text）
            max_chars: 最大字符数限制

        Returns:
            提取结果字典
        """
        result = {
            "url": url,
            "success": False,
            "content": "",
            "format": extract_mode,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        if not url or not url.strip():
            result["error"] = "URL 为空"
            return result

        url = url.strip()

        # 尝试导入 web_fetch 工具
        try:
            # 注意：在 OpenClaw 环境中，web_fetch 是内置工具
            # 这里我们通过直接调用主接口来实现
            from importlib import import_module

            # 尝试获取 web_fetch 工具
            # 这里使用 subprocess 调用 openclaw web_fetch
            import subprocess

            cmd = ["openclaw", "web-fetch", url]
            if extract_mode:
                cmd.extend(["--extract-mode", extract_mode])
            if max_chars:
                cmd.extend(["--max-chars", str(max_chars)])

            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if proc.returncode == 0:
                    content = proc.stdout.strip()

                    # 检查是否是工具输出（MEDIA: 开头的行）
                    if content.startswith("MEDIA:"):
                        # 移除 MEDIA: 前缀
                        content = content[6:].strip()

                    # 检查是否包含错误信息
                    if "error" in content.lower() or "failed" in content.lower():
                        result["error"] = f"提取失败: {content[:500]}"
                        logger.warning(f"提取失败（URL: {url}）: {result['error'][:100]}")
                    else:
                        result["success"] = True
                        result["content"] = content
                        logger.info(f"成功提取内容（URL: {url}，长度: {len(content)} 字符）")
                else:
                    result["error"] = f"命令执行失败（退出码: {proc.returncode}）: {proc.stderr[:500]}"
                    logger.error(f"命令执行失败（URL: {url}）: {result['error'][:100]}")

            except subprocess.TimeoutExpired:
                result["error"] = "提取超时（60秒）"
                logger.error(f"提取超时（URL: {url}）")
            except Exception as e:
                result["error"] = f"执行异常: {str(e)}"
                logger.error(f"执行异常（URL: {url}）: {result['error'][:100]}")

        except ImportError as e:
            result["error"] = f"无法导入必要模块: {str(e)}"
            logger.error(f"导入模块失败: {result['error']}")

        except Exception as e:
            result["error"] = f"未知错误: {str(e)}"
            logger.error(f"未知错误（URL: {url}）: {result['error']}")

        return result

    def extract(
        self,
        urls: Union[str, List[str]],
        extract_mode: Optional[str] = None,
        max_chars: int = 100000
    ) -> List[Dict]:
        """
        从 URL 列表提取内容（支持批量提取）

        Args:
            urls: 单个 URL 或 URL 列表
            extract_mode: 提取模式（markdown 或 text），默认使用 self.default_format
            max_chars: 最大字符数限制

        Returns:
            提取结果列表

        示例:
            >>> extractor = ContentExtractor()
            >>> results = extractor.extract(["https://example.com/page1", "https://example.com/page2"])
            >>> for r in results:
            ...     if r['success']:
            ...         print(f"{r['url']}: {len(r['content'])} 字符")
        """
        # 统一转换为列表
        if isinstance(urls, str):
            urls = [urls]

        if not urls:
            logger.warning("URL 列表为空")
            return []

        # 使用指定的提取模式或默认模式
        mode = extract_mode or self.default_format

        logger.info(f"开始批量提取内容（共 {len(urls)} 个 URL，模式: {mode}）")

        results = []

        for i, url in enumerate(urls, 1):
            logger.info(f"[{i}/{len(urls)}] 提取: {url}")

            result = self._extract_single_url(url, mode, max_chars)
            results.append(result)

        # 统计结果
        success_count = sum(1 for r in results if r['success'])
        fail_count = len(results) - success_count

        logger.info(f"提取完成: {success_count} 成功, {fail_count} 失败")

        return results

    def extract_from_search_results(self, search_results: List[Dict], max_results: int = 10) -> List[Dict]:
        """
        从搜索结果中提取内容

        Args:
            search_results: 搜索结果列表
            max_results: 最多提取的 URL 数量

        Returns:
            提取结果列表

        示例:
            >>> searcher = KeywordSearch()
            >>> extractor = ContentExtractor()
            >>> search_results = searcher.search("Python 编程")
            >>> extracted = extractor.extract_from_search_results(search_results, max_results=5)
        """
        # 提取 URL
        urls = [r['url'] for r in search_results if r.get('url') and r['url'].strip()]

        # 限制数量
        urls = urls[:max_results]

        if not urls:
            logger.warning("搜索结果中没有有效的 URL")
            return []

        logger.info(f"从搜索结果提取内容（共 {len(urls)} 个 URL）")

        # 批量提取
        results = self.extract(urls)

        # 将原始搜索结果信息添加到提取结果中
        url_to_result = {r['url']: r for r in search_results}

        for result in results:
            original = url_to_result.get(result['url'])
            if original:
                result['title'] = original.get('title', '')
                result['source'] = original.get('source', '')
                result['search_query'] = original.get('search_query', '')

        return results

    def save_results(self, results: List[Dict], output_file: str):
        """
        保存提取结果到文件

        Args:
            results: 提取结果列表
            output_file: 输出文件路径

        示例:
            >>> extractor = ContentExtractor()
            >>> results = extractor.extract(["https://example.com"])
            >>> extractor.save_results(results, "output.json")
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        logger.info(f"结果已保存到: {output_path}")

    def format_results(self, results: List[Dict], format: str = "text") -> str:
        """
        格式化提取结果

        Args:
            results: 提取结果列表
            format: 格式类型（text, json, markdown）

        Returns:
            格式化的字符串
        """
        if format == "json":
            return json.dumps(results, ensure_ascii=False, indent=2)

        elif format == "markdown":
            output = []
            output.append(f"# 内容提取结果（共 {len(results)} 条）\n")

            success_results = [r for r in results if r['success']]
            fail_results = [r for r in results if not r['success']]

            if success_results:
                output.append("## ✅ 成功提取的内容\n")
                for i, result in enumerate(success_results, 1):
                    output.append(f"### {i}. {result.get('title', result['url'])}")
                    output.append(f"- **URL**: {result['url']}")
                    if result.get('source'):
                        output.append(f"- **来源**: {result['source']}")
                    output.append(f"- **格式**: {result['format']}")
                    output.append(f"- **长度**: {len(result['content'])} 字符")
                    output.append(f"- **时间**: {result['timestamp']}")
                    output.append(f"\n**内容预览**:\n")
                    output.append(f"```\n{result['content'][:500]}\n```")
                    output.append("")
                    output.append("---")
                    output.append("")

            if fail_results:
                output.append("\n## ❌ 提取失败的内容\n")
                for i, result in enumerate(fail_results, 1):
                    output.append(f"### {i}. {result['url']}")
                    output.append(f"- **错误**: {result['error']}")
                    output.append(f"- **时间**: {result['timestamp']}")
                    output.append("")
                    output.append("---")
                    output.append("")

            return "\n".join(output)

        else:  # text (默认)
            output = []
            output.append(f"内容提取结果（共 {len(results)} 条）\n")

            for i, result in enumerate(results, 1):
                status = "✅" if result['success'] else "❌"
                output.append(f"{status} [{i}] {result['url']}")

                if result['success']:
                    output.append(f"    格式: {result['format']}")
                    output.append(f"    长度: {len(result['content'])} 字符")
                    if result.get('title'):
                        output.append(f"    标题: {result['title']}")
                    if result.get('source'):
                        output.append(f"    来源: {result['source']}")
                    output.append(f"    预览: {result['content'][:100]}...")
                else:
                    output.append(f"    错误: {result['error']}")

                output.append("")

            return "\n".join(output)


def main():
    """
    命令行入口

    用法:
        python3 extract_content.py <url> [options]

    选项:
        -i, --input FILE         从文件读取 URL 列表（每行一个 URL）
        -f, --format FORMAT      输出格式（markdown 或 text，默认: markdown）
        -m, --max-chars NUM       最大字符数限制（默认: 100000）
        -o, --output FILE        保存结果到文件
        -v, --verbose            显示完整内容

    示例:
        python3 extract_content.py "https://example.com/article"
        python3 extract_content.py -i urls.txt -o results.json
        python3 extract_content.py "https://example.com" -f markdown -v
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="内容提取器 - 从 URL 提取主要内容",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 extract_content.py "https://example.com/article"
  python3 extract_content.py -i urls.txt -o results.json
  python3 extract_content.py "https://example.com" -f markdown -v
        """
    )

    parser.add_argument("url", nargs="?", help="要提取的 URL")
    parser.add_argument("-i", "--input", help="从文件读取 URL 列表（每行一个 URL）")
    parser.add_argument("-f", "--format", choices=["markdown", "text"],
                        default="markdown", help="提取格式（默认: markdown）")
    parser.add_argument("-m", "--max-chars", type=int, default=100000,
                        help="最大字符数限制（默认: 100000）")
    parser.add_argument("-o", "--output", help="保存结果到文件")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="显示完整内容")

    args = parser.parse_args()

    # 获取 URL 列表
    urls = []

    if args.input:
        # 从文件读取
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"错误: 文件不存在: {args.input}")
            sys.exit(1)

        with open(input_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]

        print(f"从文件读取 {len(urls)} 个 URL\n")

    elif args.url:
        urls = [args.url]

    else:
        parser.print_help()
        sys.exit(1)

    if not urls:
        print("错误: 没有指定 URL")
        sys.exit(1)

    # 创建提取器
    extractor = ContentExtractor(default_format=args.format)

    # 执行提取
    print(f"开始提取内容（共 {len(urls)} 个 URL）\n")

    results = extractor.extract(urls, extract_mode=args.format, max_chars=args.max_chars)

    # 格式化输出
    if args.verbose:
        # 显示完整内容
        for result in results:
            print(f"\n{'='*80}")
            print(f"URL: {result['url']}")
            print(f"{'='*80}")

            if result['success']:
                print(f"\n{result['content']}")
            else:
                print(f"\n❌ 错误: {result['error']}")
    else:
        # 显示摘要
        formatted = extractor.format_results(results, "text")
        print(formatted)

    # 保存结果
    if args.output:
        extractor.save_results(results, args.output)
        print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    main()
