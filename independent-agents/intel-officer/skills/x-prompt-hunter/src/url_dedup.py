"""
URL 去重模块
在写入前检查 URL 是否已存在，使用 Set 跟踪已处理的 URL
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional, Set


class URLDedup:
    """基于 URL 的去重器"""

    def __init__(self, config: Dict):
        """
        初始化 URL 去重器

        Args:
            config: 配置字典
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.enabled = config.get("enabled", True)

        if not self.enabled:
            self.logger.info("URL deduplication is disabled")
            self.processed_urls = set()
            return

        # 加载配置
        self.url_store_file = config.get("url_store_file", "data/processed_urls.json")
        self.max_store_size = config.get("max_store_size", 100000)  # 最多存储 10 万个 URL

        # 确保目录存在
        os.makedirs(os.path.dirname(self.url_store_file) if os.path.dirname(self.url_store_file) else ".", exist_ok=True)

        # 加载已处理的 URL
        self.processed_urls = self._load_urls()

        self.logger.info(f"URL deduplication initialized: {len(self.processed_urls)} URLs already processed")

    def _load_urls(self) -> Set[str]:
        """从文件加载已处理的 URL"""
        if os.path.exists(self.url_store_file):
            try:
                with open(self.url_store_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    urls = set(data.get("urls", []))
                    self.logger.info(f"Loaded {len(urls)} processed URLs from {self.url_store_file}")
                    return urls
            except Exception as e:
                self.logger.warning(f"Failed to load URL store file: {e}, starting fresh")
        return set()

    def _save_urls(self):
        """保存已处理的 URL 到文件"""
        try:
            data = {
                "urls": list(self.processed_urls),
                "count": len(self.processed_urls),
                "last_updated": self._get_timestamp()
            }

            with open(self.url_store_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.logger.debug(f"Saved {len(self.processed_urls)} URLs to {self.url_store_file}")
        except Exception as e:
            self.logger.error(f"Failed to save URL store file: {e}")

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _generate_url_key(self, prompt: Dict) -> Optional[str]:
        """
        根据提示词生成唯一的 URL key

        Args:
            prompt: 提示词字典

        Returns:
            URL key 字符串，如果无法生成则返回 None
        """
        # 尝试从不同的字段提取唯一标识符
        possible_keys = []

        # 1. 如果有明确的 url 字段
        if "url" in prompt:
            possible_keys.append(prompt["url"])

        # 2. 使用 source + file_path 组合（GitHub 文件）
        if "source" in prompt and "file_path" in prompt:
            possible_keys.append(f"{prompt['source']}::{prompt['file_path']}")

        # 3. 使用 source + text hash（HuggingFace 数据集）
        if "source" in prompt and "text" in prompt:
            import hashlib
            text_hash = hashlib.md5(prompt["text"].encode()).hexdigest()[:16]
            possible_keys.append(f"{prompt['source']}::{text_hash}")

        # 4. 使用 data_source + source 组合
        if "data_source" in prompt and "source" in prompt:
            possible_keys.append(f"{prompt['data_source']}::{prompt['source']}")

        # 5. 如果有 id 字段
        if "id" in prompt:
            possible_keys.append(f"id:{prompt['id']}")

        # 6. 如果有 row_id 字段（HuggingFace 数据集）
        if "row_id" in prompt:
            possible_keys.append(f"row:{prompt['row_id']}")

        # 返回找到的第一个有效 key
        for key in possible_keys:
            if key and len(key) > 0:
                return key

        return None

    def is_processed(self, prompt: Dict) -> bool:
        """
        检查提示词是否已经处理过

        Args:
            prompt: 提示词字典

        Returns:
            True 如果已经处理过，False 否则
        """
        if not self.enabled:
            return False

        url_key = self._generate_url_key(prompt)

        if url_key is None:
            self.logger.warning(f"Cannot generate URL key for prompt: {prompt}")
            return False

        is_processed = url_key in self.processed_urls

        if is_processed:
            self.logger.debug(f"URL already processed: {url_key}")

        return is_processed

    def mark_as_processed(self, prompt: Dict):
        """
        标记提示词为已处理

        Args:
            prompt: 提示词字典
        """
        if not self.enabled:
            return

        url_key = self._generate_url_key(prompt)

        if url_key is None:
            self.logger.warning(f"Cannot generate URL key for prompt: {prompt}")
            return

        if url_key not in self.processed_urls:
            self.processed_urls.add(url_key)
            self.logger.debug(f"Marked URL as processed: {url_key}")

    def filter_prompts(self, prompts: List[Dict], save_after: bool = True) -> List[Dict]:
        """
        过滤掉已经处理过的提示词，并标记新提示词为已处理

        Args:
            prompts: 提示词列表
            save_after: 是否在处理后保存 URL 存储

        Returns:
            过滤后的提示词列表（只包含新的）
        """
        if not self.enabled:
            return prompts

        self.logger.info(f"Filtering {len(prompts)} prompts...")

        filtered_prompts = []
        duplicate_count = 0

        for prompt in prompts:
            if self.is_processed(prompt):
                duplicate_count += 1
            else:
                filtered_prompts.append(prompt)
                self.mark_as_processed(prompt)

        self.logger.info(
            f"Filtered {duplicate_count} duplicate prompts, "
            f"kept {len(filtered_prompts)} new prompts"
        )

        # 保存 URL 存储
        if save_after:
            self._save_urls()

        return filtered_prompts

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            "enabled": self.enabled,
            "total_processed": len(self.processed_urls),
            "store_file": self.url_store_file,
            "last_updated": self._get_timestamp() if self.enabled else None,
        }

    def clear_urls(self, confirm: bool = False):
        """
        清空已处理的 URL 列表

        Args:
            confirm: 确认清空操作
        """
        if not confirm:
            raise ValueError("Must confirm clear operation by setting confirm=True")

        self.processed_urls.clear()
        self._save_urls()
        self.logger.warning("Cleared all processed URLs")

    def export_urls(self, output_file: str = None) -> List[str]:
        """
        导出已处理的 URL 列表

        Args:
            output_file: 输出文件路径（可选）

        Returns:
            URL 列表
        """
        urls = sorted(list(self.processed_urls))

        if output_file:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    for url in urls:
                        f.write(f"{url}\n")
                self.logger.info(f"Exported {len(urls)} URLs to {output_file}")
            except Exception as e:
                self.logger.error(f"Failed to export URLs: {e}")

        return urls

    def import_urls(self, input_file: str):
        """
        从文件导入 URL 列表

        Args:
            input_file: 输入文件路径
        """
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                urls = [line.strip() for line in f if line.strip()]

            self.processed_urls.update(urls)
            self._save_urls()

            self.logger.info(f"Imported {len(urls)} URLs from {input_file}")
        except Exception as e:
            self.logger.error(f"Failed to import URLs: {e}")
            raise
