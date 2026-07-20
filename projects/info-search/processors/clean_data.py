#!/usr/bin/env python3
"""
数据清理器 - 去重、去噪、结构化

对搜索结果和提取的内容进行清理，包括 URL 去重、标题/内容去重（相似度检测）、
过滤空内容和无效 URL。

使用方法：
    from processors.clean_data import DataCleaner

    cleaner = DataCleaner()
    cleaned = cleaner.clean(search_results)
"""

import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Set, Tuple
from datetime import datetime
from urllib.parse import urlparse
import re

# 配置日志
LOG_DIR = Path("/root/clawd/logs/clean-data")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'clean-data.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class DataCleaner:
    """数据清理器 - 去重、去噪、结构化"""

    # 相似度阈值（0-1 之间，越大要求越严格）
    SIMILARITY_THRESHOLD = 0.7

    def __init__(self, similarity_threshold: float = 0.7):
        """
        初始化数据清理器

        Args:
            similarity_threshold: 相似度阈值（默认: 0.7）
                                 越高去重越严格（0.5-0.9 之间较合理）
        """
        self.similarity_threshold = similarity_threshold
        logger.info(f"数据清理器初始化完成（相似度阈值: {similarity_threshold}）")

    def normalize_url(self, url: str) -> str:
        """
        规范化 URL（用于去重）

        Args:
            url: 原始 URL

        Returns:
            规范化后的 URL
        """
        if not url:
            return ""

        url = url.strip()

        try:
            # 解析 URL
            parsed = urlparse(url)

            # 移除常见的追踪参数
            # (utm_source, utm_medium, utm_campaign, utm_content, utm_term)
            # (fbclid, gclid, _ga, etc.)
            track_params = {
                'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term',
                'fbclid', 'gclid', '_ga', '_gid', 'msclkid', 'campaign',
                'ref', 'source', 'mc_cid', 'mc_eid'
            }

            # 重建查询字符串（移除追踪参数）
            if parsed.query:
                query_params = []
                for param in parsed.query.split('&'):
                    if '=' in param:
                        key, value = param.split('=', 1)
                        if key not in track_params:
                            query_params.append(f"{key}={value}")

                new_query = '&'.join(query_params) if query_params else ''
            else:
                new_query = ''

            # 移除片段标识符（# 后面的部分）
            # 根据需要可以保留片段

            # 重建 URL（统一转为小写域名）
            normalized = (
                parsed.scheme.lower() + "://" +
                parsed.netloc.lower() +
                parsed.path +
                ("?" + new_query if new_query else '')
            )

            return normalized

        except Exception as e:
            logger.warning(f"URL 规范化失败: {url} - {str(e)}")
            return url.lower()

    def is_valid_url(self, url: str) -> bool:
        """
        检查 URL 是否有效

        Args:
            url: URL 字符串

        Returns:
            True 如果 URL 有效，否则 False
        """
        if not url or not url.strip():
            return False

        url = url.strip()

        # 检查基本格式
        if not re.match(r'^https?://', url, re.IGNORECASE):
            return False

        try:
            parsed = urlparse(url)
            # 必须有网络位置和路径
            if not parsed.netloc or not parsed.path:
                return False
            return True
        except Exception:
            return False

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度（基于简单的词重叠）

        Args:
            text1: 文本 1
            text2: 文本 2

        Returns:
            相似度（0-1 之间）
        """
        if not text1 or not text2:
            return 0.0

        # 转为小写
        text1 = text1.lower()
        text2 = text2.lower()

        # 分词（使用非字母数字字符作为分隔符）
        words1 = set(re.findall(r'\w+', text1))
        words2 = set(re.findall(r'\w+', text2))

        if not words1 or not words2:
            return 0.0

        # 计算交集和并集
        intersection = words1 & words2
        union = words1 | words2

        # Jaccard 相似度
        similarity = len(intersection) / len(union) if union else 0.0

        return similarity

    def remove_url_duplicates(self, results: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        URL 去重

        Args:
            results: 搜索结果列表

        Returns:
            (去重后的结果列表, 去重报告)
        """
        if not results:
            return results, {"removed_count": 0, "kept_count": 0}

        logger.info(f"开始 URL 去重（原始: {len(results)} 条）")

        seen_urls: Set[str] = []
        unique_results = []
        duplicates = []

        for result in results:
            url = result.get('url', '')
            normalized = self.normalize_url(url)

            if not normalized:
                duplicates.append(result)
                continue

            if normalized not in seen_urls:
                seen_urls.append(normalized)
                result['normalized_url'] = normalized
                unique_results.append(result)
            else:
                duplicates.append(result)
                logger.debug(f"移除重复 URL: {url}")

        report = {
            "removed_count": len(duplicates),
            "kept_count": len(unique_results),
            "duplicates": [r.get('url', '') for r in duplicates]
        }

        logger.info(f"URL 去重完成: 保留 {len(unique_results)} 条，移除 {len(duplicates)} 条")

        return unique_results, report

    def remove_content_duplicates(self, results: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        标题/内容去重（基于相似度）

        Args:
            results: 搜索结果列表

        Returns:
            (去重后的结果列表, 去重报告)
        """
        if not results:
            return results, {"removed_count": 0, "kept_count": 0}

        logger.info(f"开始内容去重（原始: {len(results)} 条，阈值: {self.similarity_threshold}）")

        unique_results = []
        duplicates = []

        for i, result in enumerate(results):
            is_duplicate = False

            # 获取标题和内容
            title = result.get('title', '')
            content = result.get('content', '')

            # 合并标题和内容用于比较
            text_to_compare = f"{title} {content}"

            if not text_to_compare.strip():
                # 空内容，标记为重复
                is_duplicate = True
            else:
                # 与已保留的结果比较
                for kept in unique_results:
                    kept_title = kept.get('title', '')
                    kept_content = kept.get('content', '')
                    kept_text = f"{kept_title} {kept_content}"

                    # 计算相似度
                    similarity = self.calculate_similarity(text_to_compare, kept_text)

                    if similarity >= self.similarity_threshold:
                        is_duplicate = True
                        logger.debug(
                            f"相似内容: '{title[:50]}...' 和 '{kept_title[:50]}...' "
                            f"(相似度: {similarity:.2f})"
                        )
                        break

            if is_duplicate:
                duplicates.append(result)
            else:
                unique_results.append(result)

        report = {
            "removed_count": len(duplicates),
            "kept_count": len(unique_results),
            "duplicates": [r.get('url', '') for r in duplicates]
        }

        logger.info(f"内容去重完成: 保留 {len(unique_results)} 条，移除 {len(duplicates)} 条")

        return unique_results, report

    def filter_invalid(self, results: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        过滤空内容和无效 URL

        Args:
            results: 搜索结果列表

        Returns:
            (过滤后的结果列表, 过滤报告)
        """
        if not results:
            return results, {"removed_count": 0, "kept_count": 0}

        logger.info(f"开始过滤无效内容（原始: {len(results)} 条）")

        valid_results = []
        invalid_results = []

        for result in results:
            is_valid = True
            reasons = []

            # 检查 URL
            url = result.get('url', '')
            if not url or not self.is_valid_url(url):
                is_valid = False
                reasons.append("无效 URL")

            # 检查标题和内容
            title = result.get('title', '')
            content = result.get('content', '')

            if not title or not title.strip():
                reasons.append("空标题")

            if not content or not content.strip():
                reasons.append("空内容")

            if is_valid and reasons:
                is_valid = False

            if is_valid:
                valid_results.append(result)
            else:
                result['invalid_reasons'] = reasons
                invalid_results.append(result)
                logger.debug(f"过滤无效结果: {url} - {', '.join(reasons)}")

        report = {
            "removed_count": len(invalid_results),
            "kept_count": len(valid_results),
            "invalid": [r.get('url', '') for r in invalid_results]
        }

        logger.info(f"过滤完成: 保留 {len(valid_results)} 条，移除 {len(invalid_results)} 条")

        return valid_results, report

    def clean(self, results: List[Dict], steps: List[str] = None) -> Dict:
        """
        执行完整的数据清理流程

        Args:
            results: 搜索结果列表
            steps: 清理步骤（可选），默认执行所有步骤
                   可选值: ['url', 'content', 'filter']

        Returns:
            清理结果字典，包含清理后的数据和报告

        示例:
            >>> cleaner = DataCleaner()
            >>> cleaned = cleaner.clean(search_results)
            >>> print(f"原始: {cleaned['original_count']}")
            >>> print(f"清理后: {cleaned['final_count']}")
            >>> print(f"报告: {cleaned['report']}")
        """
        if steps is None:
            steps = ['url', 'content', 'filter']

        logger.info(f"开始数据清理流程（步骤: {steps}）")

        current_results = results[:]
        reports = {}

        # 记录原始数量
        original_count = len(current_results)
        reports['original_count'] = original_count

        # 步骤 1: URL 去重
        if 'url' in steps:
            current_results, url_report = self.remove_url_duplicates(current_results)
            reports['url_dedup'] = url_report

        # 步骤 2: 内容去重
        if 'content' in steps:
            current_results, content_report = self.remove_content_duplicates(current_results)
            reports['content_dedup'] = content_report

        # 步骤 3: 过滤无效
        if 'filter' in steps:
            current_results, filter_report = self.filter_invalid(current_results)
            reports['filter'] = filter_report

        # 添加清理元数据
        cleaned_results = []
        for result in current_results:
            result['cleaned'] = True
            result['cleaned_timestamp'] = datetime.now().isoformat()
            cleaned_results.append(result)

        # 汇总报告
        final_count = len(cleaned_results)
        reports['final_count'] = final_count
        reports['total_removed'] = original_count - final_count
        reports['retention_rate'] = round(final_count / original_count * 100, 2) if original_count > 0 else 0

        logger.info(f"数据清理完成: {original_count} → {final_count} (保留率: {reports['retention_rate']}%)")

        return {
            'data': cleaned_results,
            'report': reports
        }

    def save_results(self, cleaned: Dict, output_file: str):
        """
        保存清理结果到文件

        Args:
            cleaned: 清理结果字典
            output_file: 输出文件路径
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(cleaned, f, ensure_ascii=False, indent=2)

        logger.info(f"结果已保存到: {output_path}")

    def format_report(self, report: Dict) -> str:
        """
        格式化清理报告

        Args:
            report: 报告字典

        Returns:
            格式化的报告字符串
        """
        output = []
        output.append("=" * 80)
        output.append("数据清理报告")
        output.append("=" * 80)
        output.append("")

        output.append(f"原始数量: {report['original_count']}")
        output.append(f"最终数量: {report['final_count']}")
        output.append(f"移除数量: {report['total_removed']}")
        output.append(f"保留率: {report['retention_rate']}%")
        output.append("")

        if 'url_dedup' in report:
            url_report = report['url_dedup']
            output.append("-" * 80)
            output.append("URL 去重:")
            output.append(f"  保留: {url_report['kept_count']}")
            output.append(f"  移除: {url_report['removed_count']}")
            output.append("")

        if 'content_dedup' in report:
            content_report = report['content_dedup']
            output.append("-" * 80)
            output.append("内容去重:")
            output.append(f"  保留: {content_report['kept_count']}")
            output.append(f"  移除: {content_report['removed_count']}")
            output.append("")

        if 'filter' in report:
            filter_report = report['filter']
            output.append("-" * 80)
            output.append("过滤无效:")
            output.append(f"  保留: {filter_report['kept_count']}")
            output.append(f"  移除: {filter_report['removed_count']}")
            output.append("")

        output.append("=" * 80)

        return "\n".join(output)


def main():
    """
    命令行入口

    用法:
        python3 clean_data.py <input_file> [options]

    选项:
        -o, --output FILE         保存清理结果到文件
        -s, --steps STEPS         清理步骤（逗号分隔: url,content,filter）
        -t, --threshold NUM       相似度阈值（默认: 0.7）
        --no-report               不显示详细报告

    示例:
        python3 clean_data.py results.json
        python3 clean_data.py results.json -o cleaned.json
        python3 clean_data.py results.json -s url,filter -t 0.8
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="数据清理器 - 去重、去噪、结构化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 clean_data.py results.json
  python3 clean_data.py results.json -o cleaned.json
  python3 clean_data.py results.json -s url,filter -t 0.8
        """
    )

    parser.add_argument("input_file", help="输入 JSON 文件（搜索结果列表）")
    parser.add_argument("-o", "--output", help="保存清理结果到文件")
    parser.add_argument("-s", "--steps", default="url,content,filter",
                        help="清理步骤（逗号分隔: url,content,filter，默认: url,content,filter）")
    parser.add_argument("-t", "--threshold", type=float, default=0.7,
                        help="相似度阈值（默认: 0.7）")
    parser.add_argument("--no-report", action="store_true",
                        help="不显示详细报告")

    args = parser.parse_args()

    # 读取输入文件
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"错误: 文件不存在: {args.input_file}")
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 确定数据格式
    if isinstance(data, list):
        results = data
    elif isinstance(data, dict) and 'data' in data:
        results = data['data']
    else:
        print(f"错误: 不支持的数据格式")
        sys.exit(1)

    if not results:
        print("错误: 输入数据为空")
        sys.exit(1)

    # 解析清理步骤
    steps = [s.strip() for s in args.steps.split(",")]
    valid_steps = ['url', 'content', 'filter']
    invalid_steps = [s for s in steps if s not in valid_steps]
    if invalid_steps:
        print(f"错误: 无效的清理步骤: {', '.join(invalid_steps)}")
        print(f"可用的步骤: {', '.join(valid_steps)}")
        sys.exit(1)

    # 创建清理器
    cleaner = DataCleaner(similarity_threshold=args.threshold)

    # 执行清理
    print(f"开始清理 {len(results)} 条数据\n")

    cleaned = cleaner.clean(results, steps=steps)

    # 显示报告
    if not args.no_report:
        report_text = cleaner.format_report(cleaned['report'])
        print(report_text)

    # 保存结果
    if args.output:
        cleaner.save_results(cleaned, args.output)
        print(f"\n结果已保存到: {args.output}")


if __name__ == "__main__":
    main()
