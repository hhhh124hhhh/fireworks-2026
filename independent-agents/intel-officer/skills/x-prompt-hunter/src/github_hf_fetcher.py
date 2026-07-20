"""
GitHub 和 HuggingFace 数据源抓取模块
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional

import requests
from datasets import load_dataset
from github import Github, GithubException

# 导入 URL 去重器
from url_dedup import URLDedup


class PromptFetcher:
    """统一的提示词数据源抓取器"""

    def __init__(self, config: Dict):
        """
        初始化抓取器

        Args:
            config: 配置字典
        """
        self.logger = logging.getLogger(__name__)
        self.config = config

        # GitHub 配置
        self.github_enabled = config.get("github", {}).get("enabled", False)
        self.github_token = os.getenv("GITHUB_TOKEN") or config.get("github", {}).get("token", "")
        self.github_config = config.get("github", {})

        # HuggingFace 配置
        self.hf_enabled = config.get("huggingface", {}).get("enabled", False)
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN") or config.get("huggingface", {}).get("token", "")
        self.hf_config = config.get("huggingface", {})

        # 初始化 GitHub 客户端
        if self.github_enabled and self.github_token:
            try:
                self.github_client = Github(self.github_token)
                self.logger.info("GitHub client initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize GitHub client: {e}")
                self.github_enabled = False
        else:
            self.github_client = None

        # 初始化 URL 去重器
        self.url_dedup = URLDedup(config.get("url_dedup", {}))

    def fetch_from_github(self, query: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        从 GitHub 抓取提示词

        Args:
            query: 搜索查询（可选）
            limit: 返回数量限制

        Returns:
            提示词列表
        """
        if not self.github_enabled:
            self.logger.warning("GitHub fetching is disabled")
            return []

        prompts = []
        repos = self.github_config.get("repos", [])

        try:
            for repo_name in repos[:2]:  # 限制仓库数量
                self.logger.info(f"Fetching from GitHub repo: {repo_name}")

                try:
                    repo = self.github_client.get_repo(repo_name)

                    # 获取仓库内容
                    contents = repo.get_contents("")

                    for content_item in contents:
                        if content_item.type == "file":
                            # 读取文件内容
                            file_content = content_item.decoded_content.decode("utf-8")

                            # 解析提示词
                            extracted = self._extract_prompts_from_text(
                                file_content,
                                source=f"github:{repo_name}",
                                file_path=content_item.path
                            )
                            prompts.extend(extracted)

                except GithubException as e:
                    self.logger.warning(f"Failed to fetch from repo {repo_name}: {e}")

            # 如果有搜索查询，执行 GitHub 代码搜索
            if query:
                search_prompts = self._search_github(query, limit // 2)
                prompts.extend(search_prompts)

        except Exception as e:
            self.logger.error(f"Error fetching from GitHub: {e}")

        # 使用 URL 去重
        filtered_prompts = self.url_dedup.filter_prompts(prompts, save_after=True)

        self.logger.info(f"Successfully fetched {len(filtered_prompts)} prompts from GitHub (after dedup)")
        return filtered_prompts[:limit]

    def _search_github(self, query: str, limit: int) -> List[Dict]:
        """在 GitHub 上搜索提示词"""
        prompts = []
        keywords = self.github_config.get("search_keywords", ["prompt", "template"])

        for keyword in keywords:
            search_query = f"{query} {keyword} in:file"

            try:
                results = self.github_client.search_code(search_query)

                for i, result in enumerate(results):
                    if i >= limit:
                        break

                    try:
                        # 获取文件内容
                        file_content = result.decoded_content.decode("utf-8")

                        # 提取提示词
                        extracted = self._extract_prompts_from_text(
                            file_content,
                            source=f"github:search:{result.repository.full_name}",
                            file_path=result.path
                        )
                        prompts.extend(extracted[:2])  # 每个文件最多取2个

                    except Exception as e:
                        self.logger.debug(f"Failed to read file {result.path}: {e}")

            except Exception as e:
                self.logger.warning(f"GitHub search failed for keyword '{keyword}': {e}")

        return prompts

    def _extract_prompts_from_text(self, text: str, source: str, file_path: str) -> List[Dict]:
        """从文本中提取提示词"""
        prompts = []

        # 常见的提示词模式
        patterns = [
            r'"([^"]{20,300})"',  # 双引号包裹的文本
            r'`([^`]{20,300})`',  # 反引号包裹的文本
            r'## Prompt:?\s*\n+(.+?)(?=\n##|\n---|\Z)',  # Markdown 标题格式
            r'>\s*(.+)',  # 引用格式
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)

            for match in matches:
                prompt_text = match.strip()

                # 过滤：长度和内容检查
                if 20 <= len(prompt_text) <= 500:
                    prompts.append({
                        "text": prompt_text,
                        "source": source,
                        "file_path": file_path,
                        "extracted_at": datetime.now().isoformat(),
                    })

                    if len(prompts) >= 10:  # 每个文本最多提取10个
                        break

            if len(prompts) >= 10:
                break

        return prompts

    def fetch_from_huggingface(self, query: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """
        从 HuggingFace 数据集抓取提示词

        Args:
            query: 搜索查询（可选）
            limit: 返回数量限制

        Returns:
            提示词列表
        """
        if not self.hf_enabled:
            self.logger.warning("HuggingFace fetching is disabled")
            return []

        prompts = []
        datasets = self.hf_config.get("datasets", [])

        try:
            for dataset_name in datasets[:2]:  # 限制数据集数量
                self.logger.info(f"Fetching from HuggingFace dataset: {dataset_name}")

                try:
                    # 加载数据集（限制行数）
                    dataset = load_dataset(dataset_name, split=f"train[:{limit//2}]")

                    # 遍历数据集
                    for item in dataset:
                        # 查找提示词字段
                        prompt_text = self._extract_prompt_from_item(item)

                        if prompt_text:
                            prompts.append({
                                "text": prompt_text,
                                "source": f"huggingface:{dataset_name}",
                                "extracted_at": datetime.now().isoformat(),
                            })

                            if len(prompts) >= limit:
                                break

                except Exception as e:
                    self.logger.warning(f"Failed to load dataset {dataset_name}: {e}")

        except Exception as e:
            self.logger.error(f"Error fetching from HuggingFace: {e}")

        # 使用 URL 去重
        filtered_prompts = self.url_dedup.filter_prompts(prompts, save_after=True)

        self.logger.info(f"Successfully fetched {len(filtered_prompts)} prompts from HuggingFace (after dedup)")
        return filtered_prompts[:limit]

    def _extract_prompt_from_item(self, item: Dict) -> Optional[str]:
        """从数据集条目中提取提示词"""
        # 常见的提示词字段名
        prompt_fields = [
            "prompt", "text", "content", "description",
            "instruction", "input", "query", "message"
        ]

        for field in prompt_fields:
            if field in item:
                value = item[field]
                if isinstance(value, str) and 20 <= len(value) <= 1000:
                    return value.strip()

        return None

    def fetch_all(self, query: Optional[str] = None, limit_per_source: int = 50) -> Dict[str, List[Dict]]:
        """
        从所有数据源抓取提示词

        Args:
            query: 搜索查询（可选）
            limit_per_source: 每个数据源的返回数量限制

        Returns:
            {source_name: prompts_list}
        """
        results = {}

        # 从 GitHub 抓取
        if self.github_enabled:
            github_prompts = self.fetch_from_github(query, limit_per_source)
            results["github"] = github_prompts

        # 从 HuggingFace 抓取
        if self.hf_enabled:
            hf_prompts = self.fetch_from_huggingface(query, limit_per_source)
            results["huggingface"] = hf_prompts

        # 合并所有提示词
        all_prompts = []
        for source, source_prompts in results.items():
            for prompt in source_prompts:
                prompt["data_source"] = source
                all_prompts.append(prompt)

        results["all"] = all_prompts

        self.logger.info(f"Total prompts fetched: {len(all_prompts)}")
        return results

    def save_prompts(self, prompts: List[Dict], output_file: str):
        """
        保存提示词到文件

        Args:
            prompts: 提示词列表
            output_file: 输出文件路径
        """
        try:
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(prompts, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Saved {len(prompts)} prompts to {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to save prompts: {e}")
