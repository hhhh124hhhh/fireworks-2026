"""
LLM-as-Judge 提示词质量评估模块
使用 Claude API 对提示词进行多维度质量评估
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from anthropic import Anthropic


class LLMJudge:
    """基于 LLM 的提示词质量评估器"""

    def __init__(self, config: Dict):
        """
        初始化评估器

        Args:
            config: 配置字典
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.enabled = config.get("enabled", True)

        if not self.enabled:
            self.logger.info("LLM Judge is disabled")
            return

        # 加载配置
        self.provider = config.get("provider", "anthropic")
        self.model = config.get("model", "claude-3-5-sonnet-20241022")
        self.api_key = os.getenv("ANTHROPIC_API_KEY") or config.get("api_key", "")
        self.criteria = config.get("evaluation_criteria", [
            "innovation", "practicality", "clarity", "reusability"
        ])
        self.output_file = config.get("output_file", "data/evaluation_results.json")
        self.batch_size = config.get("batch_size", 10)

        # 初始化客户端
        if self.provider == "anthropic" and self.api_key:
            try:
                self.client = Anthropic(api_key=self.api_key)
                self.logger.info(f"Anthropic client initialized with model: {self.model}")
            except Exception as e:
                self.logger.error(f"Failed to initialize Anthropic client: {e}")
                self.enabled = False
        else:
            self.client = None

        # 评估历史
        self.evaluation_history = []

    def _create_evaluation_prompt(self, prompt_text: str) -> str:
        """
        创建评估提示词

        Args:
            prompt_text: 待评估的提示词

        Returns:
            LLM 评估提示词
        """
        criteria_desc = {
            "innovation": "创新性 - 提示词的独特性和创造性",
            "practicality": "实用性 - 实际应用价值和效果",
            "clarity": "清晰度 - 表达的明确性和可理解性",
            "reusability": "可复用性 - 在不同场景下的适应性",
        }

        criteria_list = "\n".join([
            f"- {key}: {criteria_desc[key]}"
            for key in self.criteria
        ])

        evaluation_prompt = f"""你是一个专业的提示词质量评估专家。请对以下提示词进行多维度评估。

## 待评估的提示词
```
{prompt_text}
```

## 评估维度（每个维度 1-10 分）
{criteria_list}

## 评估要求
1. 对每个维度给出 1-10 分的评分
2. 计算总分（所有维度的平均分）
3. 提供具体、可操作的建议
4. 指出优点和需要改进的地方

## 输出格式（JSON）
```json
{{
    "innovation": <1-10>,
    "practicality": <1-10>,
    "clarity": <1-10>,
    "reusability": <1-10>,
    "total_score": <1-10>,
    "strengths": ["优点1", "优点2"],
    "weaknesses": ["缺点1", "缺点2"],
    "suggestions": ["建议1", "建议2"],
    "summary": "简要总结（1-2句话）"
}}
```

请严格按照 JSON 格式输出，不要包含其他内容。"""

        return evaluation_prompt

    def evaluate_single(self, prompt: Dict) -> Optional[Dict]:
        """
        评估单个提示词

        Args:
            prompt: 提示词字典，包含 'text' 字段

        Returns:
            评估结果字典
        """
        if not self.enabled or not self.client:
            return None

        prompt_text = prompt.get("text", prompt.get("prompt", ""))

        if not prompt_text:
            self.logger.warning("Prompt text is empty, skipping evaluation")
            return None

        try:
            # 创建评估提示词
            evaluation_prompt = self._create_evaluation_prompt(prompt_text)

            # 调用 Claude API
            self.logger.debug(f"Evaluating prompt: {prompt_text[:50]}...")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": evaluation_prompt
                }]
            )

            # 提取响应内容
            response_text = response.content[0].text

            # 解析 JSON 响应
            try:
                # 移除可能的 markdown 代码块标记
                response_text = response_text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]

                evaluation_result = json.loads(response_text.strip())

                # 添加元数据
                evaluation_result["prompt_text"] = prompt_text
                evaluation_result["prompt_source"] = prompt.get("source", "unknown")
                evaluation_result["evaluated_at"] = datetime.now().isoformat()
                evaluation_result["model_used"] = self.model

                self.logger.info(f"Evaluation completed with total score: {evaluation_result.get('total_score', 'N/A')}")
                return evaluation_result

            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse evaluation result as JSON: {e}")
                self.logger.debug(f"Raw response: {response_text}")
                return None

        except Exception as e:
            self.logger.error(f"Error during evaluation: {e}")
            return None

    def evaluate_batch(self, prompts: List[Dict], batch_size: Optional[int] = None) -> List[Dict]:
        """
        批量评估提示词

        Args:
            prompts: 提示词列表
            batch_size: 批次大小（可选，默认使用配置值）

        Returns:
            评估结果列表
        """
        if not self.enabled:
            self.logger.warning("LLM Judge is disabled, skipping batch evaluation")
            return []

        batch_size = batch_size or self.batch_size
        total_prompts = len(prompts)

        self.logger.info(f"Starting batch evaluation for {total_prompts} prompts (batch size: {batch_size})")

        results = []

        for i in range(0, total_prompts, batch_size):
            batch = prompts[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (total_prompts + batch_size - 1) // batch_size

            self.logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} prompts)")

            for prompt in batch:
                result = self.evaluate_single(prompt)
                if result:
                    results.append(result)

        # 更新历史记录
        self.evaluation_history.extend(results)

        # 保存结果
        self._save_results(results)

        # 生成统计报告
        self._generate_report(results)

        return results

    def _save_results(self, results: List[Dict]):
        """保存评估结果"""
        try:
            # 确保目录存在
            output_dir = os.path.dirname(self.output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # 加载现有结果
            existing_results = []
            if os.path.exists(self.output_file):
                try:
                    with open(self.output_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        existing_results = data.get("evaluations", [])
                except Exception as e:
                    self.logger.warning(f"Failed to load existing results: {e}")

            # 合并结果
            all_results = existing_results + results

            # 保存
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump({
                    "evaluations": all_results,
                    "total_count": len(all_results),
                    "last_updated": datetime.now().isoformat(),
                }, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Saved {len(results)} evaluations to {self.output_file}")

        except Exception as e:
            self.logger.error(f"Failed to save evaluation results: {e}")

    def _generate_report(self, results: List[Dict]):
        """生成评估报告"""
        if not results:
            return

        # 计算统计数据
        total = len(results)

        # 各维度平均分
        avg_scores = {}
        for criterion in self.criteria:
            scores = [r.get(criterion, 0) for r in results if criterion in r]
            avg_scores[criterion] = sum(scores) / len(scores) if scores else 0

        # 总分分布
        total_scores = [r.get("total_score", 0) for r in results if "total_score" in r]
        avg_total = sum(total_scores) / len(total_scores) if total_scores else 0

        # 分数分布
        score_distribution = {}
        for score_range in [(0, 4), (5, 6), (7, 8), (9, 10)]:
            low, high = score_range
            count = sum(1 for s in total_scores if low <= s <= high)
            score_distribution[f"{low}-{high}"] = count

        # 打印报告
        self.logger.info("=" * 60)
        self.logger.info("EVALUATION REPORT")
        self.logger.info("=" * 60)
        self.logger.info(f"Total evaluations: {total}")
        self.logger.info(f"Average total score: {avg_total:.2f}/10")
        self.logger.info("-" * 60)

        for criterion, avg in avg_scores.items():
            self.logger.info(f"Average {criterion}: {avg:.2f}/10")

        self.logger.info("-" * 60)
        self.logger.info("Score distribution:")
        for range_str, count in score_distribution.items():
            percentage = (count / total) * 100
            self.logger.info(f"  {range_str}: {count} ({percentage:.1f}%)")

        self.logger.info("=" * 60)

    def get_top_prompts(self, n: int = 10) -> List[Dict]:
        """
        获取评分最高的提示词

        Args:
            n: 返回数量

        Returns:
            Top N 提示词列表
        """
        if not self.evaluation_history:
            return []

        # 按 total_score 降序排序
        sorted_prompts = sorted(
            self.evaluation_history,
            key=lambda x: x.get("total_score", 0),
            reverse=True
        )

        return sorted_prompts[:n]

    def get_statistics(self) -> Dict:
        """获取评估统计信息"""
        if not self.evaluation_history:
            return {}

        avg_scores = {}
        for criterion in self.criteria:
            scores = [r.get(criterion, 0) for r in self.evaluation_history if criterion in r]
            avg_scores[criterion] = sum(scores) / len(scores) if scores else 0

        total_scores = [r.get("total_score", 0) for r in self.evaluation_history]
        avg_total = sum(total_scores) / len(total_scores) if total_scores else 0

        return {
            "total_evaluations": len(self.evaluation_history),
            "average_total_score": avg_total,
            "average_scores_by_criterion": avg_scores,
            "highest_score": max(total_scores) if total_scores else 0,
            "lowest_score": min(total_scores) if total_scores else 0,
        }
