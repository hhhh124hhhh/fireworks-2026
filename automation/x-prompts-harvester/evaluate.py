#!/usr/bin/env python3
"""
Prompt Quality Evaluation Module
Evaluates the quality of prompts using the prompt-optimizer skill.
"""

import os
import json
import re
from typing import List, Dict, Tuple
from datetime import datetime

class PromptEvaluator:
    def __init__(self):
        self.min_score = 5.0  # Minimum score to consider
        self.quality_threshold = 7.0  # Threshold for high-quality prompts

    def evaluate_prompt(self, prompt_text: str) -> Dict:
        """
        Evaluate a single prompt across multiple dimensions.

        Args:
            prompt_text: The prompt text to evaluate

        Returns:
            Dictionary with scores and analysis
        """
        scores = {
            "clarity": self._evaluate_clarity(prompt_text),
            "specificity": self._evaluate_specificity(prompt_text),
            "structure": self._evaluate_structure(prompt_text),
            "completeness": self._evaluate_completeness(prompt_text),
            "utility": self._evaluate_utility(prompt_text)
        }

        # Calculate average
        scores["average"] = sum(scores.values()) / len(scores)

        # Determine quality tier
        if scores["average"] >= 8.0:
            scores["tier"] = "high"
        elif scores["average"] >= 7.0:
            scores["tier"] = "good"
        elif scores["average"] >= 5.0:
            scores["tier"] = "medium"
        else:
            scores["tier"] = "low"

        return scores

    def _evaluate_clarity(self, text: str) -> float:
        """Evaluate how clear and understandable the prompt is."""
        score = 5.0

        # Check for clear instructions
        if "you are" in text.lower() or "act as" in text.lower():
            score += 1.5

        # Check for明确的目标
        goal_indicators = ["your task is", "i want you to", "please", "help me"]
        if any(indicator in text.lower() for indicator in goal_indicators):
            score += 1.0

        # Penalize overly complex sentences
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_sentence_length > 30:
            score -= 1.0

        return min(10.0, max(0.0, score))

    def _evaluate_specificity(self, text: str) -> float:
        """Evaluate how specific the requirements and constraints are."""
        score = 5.0

        # Check for specific details
        specificity_indicators = [
            "in the style of", "approximately", "at least", "no more than",
            "include", "exclude", "focus on", "emphasize", "avoid"
        ]
        matches = sum(1 for indicator in specificity_indicators if indicator in text.lower())
        score += matches * 0.5

        # Check for format specifications
        if any(word in text.lower() for word in ["format", "structure", "bullet", "paragraph"]):
            score += 1.0

        # Check for examples
        if "for example" in text.lower() or "example:" in text.lower():
            score += 1.0

        return min(10.0, max(0.0, score))

    def _evaluate_structure(self, text: str) -> float:
        """Evaluate the organization and structure of the prompt."""
        score = 5.0

        # Check for numbered steps
        if re.search(r'\d+\.', text):
            score += 1.5

        # Check for bullet points or lists
        if "•" in text or "-" in text or "*" in text:
            score += 1.0

        # Check for sections with headers
        if re.search(r'\n#+ ', text):
            score += 1.5

        # Check for clear intro-body-conclusion structure
        lines = text.split('\n')
        if len(lines) > 3:
            score += 1.0

        return min(10.0, max(0.0, score))

    def _evaluate_completeness(self, text: str) -> float:
        """Evaluate if the prompt contains all necessary context."""
        score = 5.0

        # Check for context/background
        context_indicators = ["context", "background", "given that", "assume"]
        if any(indicator in text.lower() for indicator in context_indicators):
            score += 1.0

        # Check for target audience
        audience_indicators = ["for a", "to a", "audience", "reader", "user"]
        if any(indicator in text.lower() for indicator in audience_indicators):
            score += 1.0

        # Check for constraints or limitations
        constraint_indicators = ["must not", "avoid", "do not", "constraint", "limit"]
        if any(indicator in text.lower() for indicator in constraint_indicators):
            score += 1.0

        # Check length - too short may be incomplete
        if len(text) > 200:
            score += 1.0

        return min(10.0, max(0.0, score))

    def _evaluate_utility(self, text: str) -> float:
        """Evaluate the practical utility and use cases."""
        score = 5.0

        # Check for actionable tasks
        action_indicators = ["write", "create", "generate", "analyze", "summarize", "translate"]
        if any(indicator in text.lower() for indicator in action_indicators):
            score += 1.5

        # Check for reusable patterns
        if any(indicator in text.lower() for indicator in ["template", "pattern", "framework"]):
            score += 1.0

        # Check for specific domains/industries
        domain_indicators = ["business", "marketing", "code", "data", "finance", "healthcare"]
        if any(indicator in text.lower() for indicator in domain_indicators):
            score += 0.5

        # Check for output quality indicators
        quality_indicators = ["professional", "compelling", "engaging", "clear", "concise"]
        if any(indicator in text.lower() for indicator in quality_indicators):
            score += 1.0

        return min(10.0, max(0.0, score))

    def evaluate_batch(self, prompts: List[Dict]) -> List[Dict]:
        """
        Evaluate a batch of prompts.

        Args:
            prompts: List of prompt dictionaries with 'text' field

        Returns:
            List of prompts with added evaluation scores
        """
        for prompt in prompts:
            scores = self.evaluate_prompt(prompt["text"])
            prompt["evaluation"] = scores

        return prompts

    def filter_by_quality(self, prompts: List[Dict], min_score: float = None) -> Tuple[List[Dict], List[Dict]]:
        """
        Filter prompts by quality score.

        Args:
            prompts: List of evaluated prompts
            min_score: Minimum score threshold (defaults to self.quality_threshold)

        Returns:
            Tuple of (high_quality_prompts, low_quality_prompts)
        """
        if min_score is None:
            min_score = self.quality_threshold

        high_quality = [p for p in prompts if p["evaluation"]["average"] >= min_score]
        low_quality = [p for p in prompts if p["evaluation"]["average"] < min_score]

        return high_quality, low_quality

    def deduplicate_prompts(self, prompts: List[Dict], similarity_threshold: float = 0.85) -> List[Dict]:
        """
        Remove duplicate or highly similar prompts.

        Args:
            prompts: List of prompts
            similarity_threshold: Similarity threshold for deduplication

        Returns:
            List of deduplicated prompts
        """
        unique_prompts = []
        seen_texts = set()

        for prompt in prompts:
            # Simple deduplication by exact match first
            text = prompt["text"]
            if text in seen_texts:
                continue

            # Check for similarity with existing prompts
            is_similar = False
            for existing in unique_prompts:
                similarity = self._calculate_similarity(text, existing["text"])
                if similarity >= similarity_threshold:
                    is_similar = True
                    # Keep the one with higher engagement
                    if self._get_engagement_score(prompt) > self._get_engagement_score(existing):
                        unique_prompts.remove(existing)
                        unique_prompts.append(prompt)
                    break

            if not is_similar:
                seen_texts.add(text)
                unique_prompts.append(prompt)

        return unique_prompts

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple similarity between two texts."""
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union)

    def _get_engagement_score(self, prompt: Dict) -> float:
        """Calculate engagement score for a prompt."""
        metrics = prompt.get("metrics", {})
        retweets = metrics.get("retweet_count", 0)
        likes = metrics.get("like_count", 0)
        replies = metrics.get("reply_count", 0)

        # Weighted engagement score
        return retweets * 2.0 + likes * 1.0 + replies * 1.5


def main():
    """Main function for testing."""
    # Test with sample prompts
    sample_prompts = [
        {
            "text": "You are a professional email writer. Write a persuasive email to a potential client highlighting the benefits of our new product. Keep it under 200 words and include a clear call-to-action.",
            "metrics": {"retweet_count": 50, "like_count": 200, "reply_count": 10}
        },
        {
            "text": "Write something good.",
            "metrics": {"retweet_count": 5, "like_count": 20, "reply_count": 2}
        }
    ]

    evaluator = PromptEvaluator()

    print("=== Prompt Quality Evaluation ===\n")

    for i, prompt in enumerate(sample_prompts, 1):
        print(f"Prompt {i}:")
        print(f"Text: {prompt['text'][:100]}...")

        scores = evaluator.evaluate_prompt(prompt["text"])

        print(f"Quality Score: {scores['average']:.2f}/10")
        print(f"Tier: {scores['tier']}")
        print(f"  Clarity: {scores['clarity']:.2f}")
        print(f"  Specificity: {scores['specificity']:.2f}")
        print(f"  Structure: {scores['structure']:.2f}")
        print(f"  Completeness: {scores['completeness']:.2f}")
        print(f"  Utility: {scores['utility']:.2f}")
        print()


if __name__ == "__main__":
    main()
