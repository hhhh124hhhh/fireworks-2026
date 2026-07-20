#!/usr/bin/env python3
"""
WeChat Cover Prompt Quality Scorer

Automatically scores WeChat cover prompts based on four dimensions:
- Technical Quality (0-10)
- Commercial Value (0-10)
- WeChat Compatibility (0-10)
- Uniqueness (0-10)

Usage:
    python3 score_prompt.py "<prompt>"
"""

import sys
import re
import json
from typing import Dict, Tuple

class PromptScorer:
    """Score WeChat cover prompts for quality and commercial viability."""

    def __init__(self, prompt: str):
        self.prompt = prompt.lower()
        self.original_prompt = prompt

    def score_technical_quality(self) -> Tuple[float, str]:
        """Score technical specifications and parameters."""
        score = 0.0
        feedback = []

        # Aspect ratio (critical)
        if '900x383' in self.prompt or '2.35:1' in self.prompt or '--ar 2.35:1' in self.prompt:
            score += 3.0
            feedback.append("✓ Correct aspect ratio specified (2.35:1 or 900×383px)")
        else:
            feedback.append("✗ Missing aspect ratio - add '--ar 2.35:1' or '900x383 aspect ratio'")

        # Resolution/quality
        if any(term in self.prompt for term in ['4k', '8k', 'high resolution', 'high quality', 'ultra hd']):
            score += 2.0
            feedback.append("✓ Resolution/quality specified")
        else:
            feedback.append("✗ Add resolution spec (4K, 8K, high quality)")

        # Style/medium
        if any(term in self.prompt for term in ['photograph', 'illustration', '3d', 'render', 'digital art', 'vector']):
            score += 2.0
            feedback.append("✓ Style/medium specified")
        else:
            feedback.append("✗ Specify style/medium (photography, illustration, 3D, etc.)")

        # Technical details
        technical_terms = ['lighting', 'camera', 'depth of field', 'focus', 'contrast', 'gradient']
        technical_count = sum(1 for term in technical_terms if term in self.prompt)
        score += min(technical_count * 0.5, 3.0)
        if technical_count > 0:
            feedback.append(f"✓ {technical_count} technical details present")

        return min(score, 10.0), "\n".join(feedback)

    def score_commercial_value(self) -> Tuple[float, str]:
        """Score business potential and marketability."""
        score = 0.0
        feedback = []

        # Industry/category
        industries = {
            'business': 2.0, 'finance': 2.0, 'fintech': 2.0, 'investment': 2.0,
            'technology': 2.0, 'ai': 2.0, 'saas': 2.0, 'software': 2.0,
            'retail': 1.5, 'ecommerce': 1.5, 'e-commerce': 1.5,
            'education': 1.5, 'course': 1.5, 'tutorial': 1.5,
            'healthcare': 1.5, 'medical': 1.5, 'wellness': 1.5,
            'food': 1.0, 'travel': 1.0, 'fashion': 1.0, 'lifestyle': 1.0
        }

        industry_match = False
        for industry, points in industries.items():
            if industry in self.prompt:
                score += points
                feedback.append(f"✓ Industry specified: {industry}")
                industry_match = True
                break

        if not industry_match:
            feedback.append("✗ Specify industry/category for better commercial targeting")

        # Professional aesthetic
        if any(term in self.prompt for term in ['professional', 'corporate', 'premium', 'luxury', 'high-quality']):
            score += 2.0
            feedback.append("✓ Professional aesthetic")
        else:
            feedback.append("✗ Add professional/brand-safe keywords")

        # Scalability indicators
        scalable_terms = ['template', 'cover', 'banner', 'official account', 'design']
        if any(term in self.prompt for term in scalable_terms):
            score += 2.0
            feedback.append("✓ Scalable template structure")

        # Clear use case
        use_case_terms = ['cover', 'banner', 'header', 'promo', 'ad', 'marketing']
        if any(term in self.prompt for term in use_case_terms):
            score += 1.0
            feedback.append("✓ Clear use case identified")

        # Brand-safe
        if 'adult' not in self.prompt and 'nsfw' not in self.prompt:
            score += 1.0
            feedback.append("✓ Brand-safe content")

        return min(score, 10.0), "\n".join(feedback)

    def score_wechat_compatibility(self) -> Tuple[float, str]:
        """Score WeChat-specific optimization."""
        score = 0.0
        feedback = []

        # Dimensions (most critical)
        if '900x383' in self.prompt or '2.35:1' in self.prompt or '--ar 2.35:1' in self.prompt:
            score += 4.0
            feedback.append("✓ Correct dimensions (900×383px or 2.35:1)")
        else:
            feedback.append("✗ CRITICAL: Add '900x383 aspect ratio' or '--ar 2.35:1'")

        # Text space
        if any(term in self.prompt for term in ['headline space', 'text space', 'text area', 'clean text', 'title space']):
            score += 3.0
            feedback.append("✓ Text placeholder specified")
        else:
            feedback.append("✗ Add text space (e.g., 'clean headline space on left')")

        # WeChat context
        if any(term in self.prompt for term in ['wechat', 'official account', 'social media']):
            score += 2.0
            feedback.append("✓ WeChat context included")
        else:
            feedback.append("✗ Add 'WeChat official account' for platform optimization")

        # Contrast for text
        if 'contrast' in self.prompt:
            score += 1.0
            feedback.append("✓ Contrast mentioned for text readability")

        return min(score, 10.0), "\n".join(feedback)

    def score_uniqueness(self) -> Tuple[float, str]:
        """Score originality and differentiation."""
        score = 0.0
        feedback = []

        # Generic indicators (lower score)
        generic_patterns = [
            r'cover for.*',
            r'.*design.*',
            r'.*background.*'
        ]

        generic_count = sum(1 for pattern in generic_patterns if re.search(pattern, self.prompt))
        if generic_count > 0:
            score -= 1.0
            feedback.append(f"⚠ Generic patterns detected ({generic_count}) - add unique elements")

        # Unique elements
        unique_terms = [
            'blockchain', 'neural', 'geometric', 'abstract', 'visualization',
            'gradient', 'glowing', 'interconnected', 'topology', 'network'
        ]
        unique_count = sum(1 for term in unique_terms if term in self.prompt)
        if unique_count > 0:
            score += min(unique_count * 2.0, 6.0)
            feedback.append(f"✓ {unique_count} unique/creative elements present")

        # Color combinations
        colors = ['blue', 'green', 'gold', 'purple', 'cyan', 'emerald', 'navy']
        color_count = sum(1 for color in colors if color in self.prompt)
        if color_count >= 2:
            score += 2.0
            feedback.append("✓ Creative color combination")
        elif color_count == 1:
            score += 1.0
            feedback.append("✓ Color scheme specified (try combining 2+ colors)")

        # Specific details
        specific_patterns = [
            r'\d+x\d+',  # Dimensions
            r'--ar\s+\d+\.?\d*:\d+\.?\d*',  # Aspect ratio
            r'[a-z]+\s+and\s+[a-z]+',  # Color combinations
        ]
        specific_count = sum(1 for pattern in specific_patterns if re.search(pattern, self.prompt))
        score += min(specific_count * 1.0, 2.0)

        # Length indicator (longer prompts tend to be more specific)
        word_count = len(self.prompt.split())
        if word_count > 20:
            score += 1.0
            feedback.append("✓ Good level of detail")

        return min(max(score, 0.0), 10.0), "\n".join(feedback)

    def generate_improvements(self, scores: Dict[str, float]) -> str:
        """Generate specific improvement suggestions."""
        improvements = []

        if scores['Technical Quality'] < 8.0:
            improvements.append("Add technical specs: '--ar 2.35:1', '4K quality', lighting details")

        if scores['Commercial Value'] < 8.0:
            improvements.append("Specify industry clearly, add professional/brand-safe keywords")

        if scores['WeChat Compatibility'] < 9.0:
            improvements.append("CRITICAL: Add '900x383 aspect ratio' or '--ar 2.35:1', specify text space")

        if scores['Uniqueness'] < 7.0:
            improvements.append("Add unique elements, creative color combinations, specific details")

        return "\n".join([f"• {imp}" for imp in improvements]) if improvements else "✓ No major improvements needed"

    def score(self) -> Dict:
        """Generate comprehensive score report."""
        tech_score, tech_feedback = self.score_technical_quality()
        comm_score, comm_feedback = self.score_commercial_value()
        wechat_score, wechat_feedback = self.score_wechat_compatibility()
        unique_score, unique_feedback = self.score_uniqueness()

        scores = {
            'Technical Quality': tech_score,
            'Commercial Value': comm_score,
            'WeChat Compatibility': wechat_score,
            'Uniqueness': unique_score
        }

        overall_score = sum(scores.values()) / len(scores)

        return {
            'scores': scores,
            'overall_score': overall_score,
            'feedback': {
                'Technical Quality': tech_feedback,
                'Commercial Value': comm_feedback,
                'WeChat Compatibility': wechat_feedback,
                'Uniqueness': unique_feedback
            },
            'improvements': self.generate_improvements(scores),
            'quality_level': self._get_quality_level(overall_score)
        }

    def _get_quality_level(self, score: float) -> str:
        """Determine quality level based on overall score."""
        if score >= 9.0:
            return "Excellent (Ready for commercial use)"
        elif score >= 7.0:
            return "Good (Minor improvements recommended)"
        elif score >= 5.0:
            return "Fair (Needs optimization)"
        else:
            return "Poor (Significant rework required)"

def print_score_report(report: Dict, prompt: str):
    """Print formatted score report."""
    print("\n" + "="*70)
    print("WECHAT COVER PROMPT QUALITY SCORE")
    print("="*70)
    print(f"\nPrompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    print(f"\n{'='*70}")

    # Overall score
    overall = report['overall_score']
    print(f"\n📊 OVERALL SCORE: {overall:.2f}/10")
    print(f"   Quality Level: {report['quality_level']}")
    print(f"\n{'='*70}")

    # Dimension scores
    print("\n📈 Dimension Scores:")
    print("-"*70)
    for dimension, score in report['scores'].items():
        bar = "█" * int(score)
        empty = "░" * (10 - int(score))
        print(f"\n{dimension}:")
        print(f"  Score: {score:.2f}/10")
        print(f"  Visual: [{bar}{empty}]")

        # Feedback
        feedback = report['feedback'][dimension]
        print(f"  Feedback:")
        for line in feedback.split('\n'):
            print(f"    {line}")

    # Improvements
    if report['improvements']:
        print(f"\n{'='*70}")
        print("\n💡 Suggested Improvements:")
        print(report['improvements'])

    print(f"\n{'='*70}\n")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 score_prompt.py \"<prompt>\"")
        print("\nExample:")
        print('  python3 score_prompt.py "A professional corporate cover for WeChat official account, 900x383 aspect ratio, --ar 2.35:1"')
        sys.exit(1)

    prompt = sys.argv[1]
    scorer = PromptScorer(prompt)
    report = scorer.score()
    print_score_report(report, prompt)

if __name__ == "__main__":
    main()
