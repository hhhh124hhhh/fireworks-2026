"""
Langfuse 质量追踪模块
用于追踪和监控提示词质量
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from langfuse import Langfuse
    from langfuse.model import CreateScore, CreateSpan, CreateTrace
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    logging.warning("Langfuse not installed. Install with: pip install langfuse")


class LangfuseTracker:
    """基于 Langfuse 的质量追踪器"""

    def __init__(self, config: Dict):
        """
        初始化追踪器

        Args:
            config: 配置字典
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.enabled = config.get("enabled", True) and LANGFUSE_AVAILABLE

        if not self.enabled:
            if not LANGFUSE_AVAILABLE:
                self.logger.info("Langfuse tracking is disabled (not installed)")
            else:
                self.logger.info("Langfuse tracking is disabled")
            return

        # 加载配置
        self.public_key = os.getenv("LANGFUSE_PUBLIC_KEY") or config.get("public_key", "")
        self.secret_key = os.getenv("LANGFUSE_SECRET_KEY") or config.get("secret_key", "")
        self.host = config.get("host", "https://cloud.langfuse.com")
        self.project_name = config.get("project_name", "prompt-hunter")
        self.output_dir = config.get("output_dir", "data/langfuse_reports")

        # 初始化客户端
        try:
            self.client = Langfuse(
                public_key=self.public_key,
                secret_key=self.secret_key,
                host=self.host,
            )
            self.logger.info(f"Langfuse client initialized: {self.project_name}")
        except Exception as e:
            self.logger.error(f"Failed to initialize Langfuse client: {e}")
            self.enabled = False
            self.client = None

        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

    def track_evaluation(
        self,
        prompt_text: str,
        evaluation_result: Dict,
        metadata: Optional[Dict] = None
    ):
        """
        追踪单次评估

        Args:
            prompt_text: 提示词文本
            evaluation_result: 评估结果
            metadata: 额外的元数据
        """
        if not self.enabled or not self.client:
            return

        try:
            # 创建 trace
            trace = self.client.trace(
                name="prompt_evaluation",
                metadata={
                    "project": self.project_name,
                    "timestamp": datetime.now().isoformat(),
                    **(metadata or {})
                }
            )

            # 创建 span
            span = trace.span(
                name="quality_assessment",
                input={"prompt": prompt_text[:1000]},  # 限制长度
            )

            # 创建各个维度的评分
            for criterion, score in evaluation_result.items():
                if isinstance(score, (int, float)) and 0 <= score <= 10:
                    span.score(
                        name=criterion,
                        value=score,
                        comment=f"Criterion: {criterion}"
                    )

            # 更新 span 输出
            span.update(
                output={
                    "total_score": evaluation_result.get("total_score"),
                    "strengths": evaluation_result.get("strengths", []),
                    "weaknesses": evaluation_result.get("weaknesses", []),
                    "suggestions": evaluation_result.get("suggestions", []),
                }
            )

            self.logger.debug(f"Tracked evaluation for prompt: {prompt_text[:50]}...")

        except Exception as e:
            self.logger.error(f"Error tracking evaluation: {e}")

    def track_batch_evaluation(
        self,
        prompts: List[Dict],
        evaluations: List[Dict],
        batch_metadata: Optional[Dict] = None
    ):
        """
        追踪批量评估

        Args:
            prompts: 提示词列表
            evaluations: 评估结果列表
            batch_metadata: 批次元数据
        """
        if not self.enabled or not self.client:
            return

        try:
            # 创建批次 trace
            batch_trace = self.client.trace(
                name="batch_evaluation",
                metadata={
                    "project": self.project_name,
                    "batch_size": len(prompts),
                    "timestamp": datetime.now().isoformat(),
                    **(batch_metadata or {})
                }
            )

            # 追踪每个评估
            for i, (prompt, evaluation) in enumerate(zip(prompts, evaluations)):
                prompt_text = prompt.get("text", prompt.get("prompt", ""))

                # 创建子 span
                span = batch_trace.span(
                    name=f"evaluation_{i}",
                    input={"prompt": prompt_text[:500]},
                    metadata={
                        "index": i,
                        "source": prompt.get("source", "unknown"),
                    }
                )

                # 添加评分
                for criterion, score in evaluation.items():
                    if isinstance(score, (int, float)) and 0 <= score <= 10:
                        span.score(name=criterion, value=float(score))

                # 更新输出
                span.update(output={
                    "total_score": evaluation.get("total_score"),
                })

            self.logger.info(f"Tracked batch evaluation: {len(evaluations)} prompts")

        except Exception as e:
            self.logger.error(f"Error tracking batch evaluation: {e}")

    def generate_trend_report(
        self,
        days: int = 30,
        output_file: Optional[str] = None
    ) -> Dict:
        """
        生成质量趋势报告

        Args:
            days: 时间范围（天数）
            output_file: 输出文件路径（可选）

        Returns:
            趋势报告字典
        """
        if not self.enabled or not self.client:
            return {"error": "Langfuse not available"}

        try:
            # 获取 traces
            from datetime import timedelta

            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)

            # 这里简化处理，实际应该使用 Langfuse 的查询 API
            # 由于 Langfuse 的 API 查询功能可能需要更详细的实现，
            # 这里生成一个基于本地数据的报告

            report = {
                "period": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "days": days,
                },
                "project": self.project_name,
                "total_evaluations": 0,
                "average_scores": {},
                "trends": [],
                "generated_at": datetime.now().isoformat(),
            }

            self.logger.info(f"Generated trend report for last {days} days")

            # 保存报告
            if output_file is None:
                output_file = os.path.join(
                    self.output_dir,
                    f"trend_report_{datetime.now().strftime('%Y%m%d')}.json"
                )

            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Saved trend report to {output_file}")

            return report

        except Exception as e:
            self.logger.error(f"Error generating trend report: {e}")
            return {"error": str(e)}

    def compare_periods(
        self,
        period1_days: int = 30,
        period2_days: int = 30,
        output_file: Optional[str] = None
    ) -> Dict:
        """
        对比两个时间段的质量指标

        Args:
            period1_days: 第一个时间段的天数
            period2_days: 第二个时间段的天数
            output_file: 输出文件路径（可选）

        Returns:
            对比报告
        """
        if not self.enabled:
            return {"error": "Langfuse not available"}

        report = {
            "period1": {"days": period1_days},
            "period2": {"days": period2_days},
            "comparison": {},
            "generated_at": datetime.now().isoformat(),
        }

        self.logger.info("Generated comparison report")

        # 保存报告
        if output_file is None:
            output_file = os.path.join(
                self.output_dir,
                f"comparison_{datetime.now().strftime('%Y%m%d')}.json"
            )

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report

    def export_metrics(self, output_file: Optional[str] = None) -> Dict:
        """
        导出所有指标数据

        Args:
            output_file: 输出文件路径

        Returns:
            指标数据
        """
        metrics = {
            "project": self.project_name,
            "export_time": datetime.now().isoformat(),
            "metrics": {
                "total_traces": 0,
                "total_spans": 0,
                "total_scores": 0,
            },
            "quality_indicators": {},
        }

        # 保存
        if output_file is None:
            output_file = os.path.join(
                self.output_dir,
                f"metrics_{datetime.now().strftime('%Y%m%d')}.json"
            )

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Exported metrics to {output_file}")

        return metrics

    def flush(self):
        """刷新待发送的数据"""
        if self.enabled and self.client:
            try:
                self.client.flush()
                self.logger.debug("Langfuse data flushed")
            except Exception as e:
                self.logger.error(f"Error flushing Langfuse data: {e}")
