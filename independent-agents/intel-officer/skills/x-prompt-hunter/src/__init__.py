"""
AI 提示词系统
Version: 1.0.0
"""

# 延迟导入 SemanticDedup（仅在需要时导入）
# 这样可以在禁用语义去重时避免安装 sentence-transformers
SemanticDedup = None

def get_semantic_dedup():
    """按需加载 SemanticDedup 类"""
    global SemanticDedup
    if SemanticDedup is None:
        from .semantic_dedup import SemanticDedup as SD
        SemanticDedup = SD
    return SemanticDedup

from .github_hf_fetcher import PromptFetcher
from .llm_judge import LLMJudge
from .langfuse_tracker import LangfuseTracker

__version__ = "1.0.0"
__all__ = [
    "get_semantic_dedup",
    "PromptFetcher",
    "LLMJudge",
    "LangfuseTracker",
]
