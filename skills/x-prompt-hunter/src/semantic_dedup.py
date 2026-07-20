"""
语义去重模块
使用 sentence-transformers 计算提示词之间的语义相似度
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticDedup:
    """基于 sentence-transformers 的语义去重器"""

    def __init__(self, config: Dict):
        """
        初始化语义去重器

        Args:
            config: 配置字典
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.enabled = config.get("enabled", True)

        if not self.enabled:
            self.logger.info("Semantic deduplication is disabled")
            return

        # 加载配置
        self.model_name = config.get("model_name", "all-MiniLM-L6-v2")
        self.similarity_threshold = config.get("similarity_threshold", 0.85)
        self.batch_size = config.get("batch_size", 32)
        self.log_file = config.get("log_file", "data/deduplication_log.json")

        # 确保日志目录存在
        os.makedirs(os.path.dirname(self.log_file) if os.path.dirname(self.log_file) else ".", exist_ok=True)

        # 加载模型
        self.logger.info(f"Loading sentence-transformers model: {self.model_name}")
        try:
            self.model = SentenceTransformer(self.model_name)
            self.logger.info("Model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise

        # 去重记录
        self.deduplication_log = self._load_log()

    def _load_log(self) -> Dict:
        """加载去重日志"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load log file: {e}, creating new log")
        return {
            "processed_prompts": 0,
            "removed_prompts": 0,
            "similarity_pairs": [],
            "last_updated": None,
        }

    def _save_log(self):
        """保存去重日志"""
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(self.deduplication_log, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save log file: {e}")

    def _compute_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        计算文本嵌入向量

        Args:
            texts: 文本列表

        Returns:
            嵌入向量矩阵
        """
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=self.batch_size,
                show_progress_bar=True,
                convert_to_numpy=True,
            )
            return embeddings
        except Exception as e:
            self.logger.error(f"Failed to compute embeddings: {e}")
            raise

    def _compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        计算两个嵌入向量的余弦相似度

        Args:
            embedding1: 第一个嵌入向量
            embedding2: 第二个嵌入向量

        Returns:
            相似度分数 (0-1)
        """
        # 归一化
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        # 余弦相似度
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        return float(similarity)

    def deduplicate(self, prompts: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        对提示词列表进行去重

        Args:
            prompts: 提示词列表，每个元素包含至少 'text' 字段

        Returns:
            (去重后的提示词列表, 去重统计信息)
        """
        if not self.enabled or len(prompts) <= 1:
            return prompts, {"removed": 0, "kept": len(prompts)}

        self.logger.info(f"Starting deduplication for {len(prompts)} prompts")

        # 提取文本
        texts = [prompt.get("text", prompt.get("prompt", "")) for prompt in prompts]

        # 计算嵌入向量
        embeddings = self._compute_embeddings(texts)

        # 去重逻辑
        kept_indices = set()
        removed_indices = set()
        similarity_pairs = []

        for i in range(len(prompts)):
            if i in removed_indices:
                continue

            # 默认保留第一个
            kept_indices.add(i)

            # 检查与后面的相似度
            for j in range(i + 1, len(prompts)):
                if j in removed_indices:
                    continue

                similarity = self._compute_similarity(embeddings[i], embeddings[j])

                if similarity >= self.similarity_threshold:
                    # 相似度过高，移除后面的
                    removed_indices.add(j)
                    similarity_pairs.append({
                        "index_i": i,
                        "index_j": j,
                        "similarity": similarity,
                        "text_i": texts[i][:100] + "..." if len(texts[i]) > 100 else texts[i],
                        "text_j": texts[j][:100] + "..." if len(texts[j]) > 100 else texts[j],
                    })

        # 构建结果
        deduplicated_prompts = [prompts[i] for i in sorted(kept_indices)]
        removed_prompts = [prompts[i] for i in sorted(removed_indices)]

        # 更新日志
        self.deduplication_log["processed_prompts"] += len(prompts)
        self.deduplication_log["removed_prompts"] += len(removed_prompts)
        self.deduplication_log["similarity_pairs"].extend(similarity_pairs)
        self.deduplication_log["last_updated"] = str(datetime.datetime.now())
        self._save_log()

        # 统计信息
        stats = {
            "original_count": len(prompts),
            "kept_count": len(deduplicated_prompts),
            "removed_count": len(removed_prompts),
            "removal_rate": len(removed_prompts) / len(prompts) if prompts else 0,
        }

        self.logger.info(
            f"Deduplication completed: {stats['kept_count']} kept, "
            f"{stats['removed_count']} removed ({stats['removal_rate']:.2%})"
        )

        return deduplicated_prompts, stats

    def check_similarity(self, text1: str, text2: str) -> float:
        """
        检查两个文本的相似度

        Args:
            text1: 第一个文本
            text2: 第二个文本

        Returns:
            相似度分数 (0-1)
        """
        if not self.enabled:
            return 0.0

        embeddings = self._compute_embeddings([text1, text2])
        return self._compute_similarity(embeddings[0], embeddings[1])


# 导入 datetime 用于时间戳
import datetime
