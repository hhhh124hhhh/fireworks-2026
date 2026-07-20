#!/usr/bin/env python3
"""
Prompt to Skill Converter Module
Converts high-quality prompts into Clawdbot Skills.
"""

import os
import json
import re
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

class PromptToSkillConverter:
    def __init__(self, output_dir: str = "skills-generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_skill_name(self, prompt: Dict) -> str:
        """
        Generate a skill name from the prompt.

        Args:
            prompt: Prompt dictionary

        Returns:
            Skill name in kebab-case
        """
        text = prompt["text"].lower()

        # Extract key keywords
        keywords = []

        # Look for action verbs
        action_verbs = ["write", "create", "generate", "analyze", "summarize", "translate",
                       "design", "build", "code", "optimize", "improve", "help"]

        for verb in action_verbs:
            if verb in text:
                keywords.append(verb)
                break

        # Look for target/domain
        domains = ["email", "code", "article", "blog", "story", "essay", "summary",
                   "analysis", "review", "business", "marketing", "content", "copy",
                   "product", "sales", "data", "report"]

        for domain in domains:
            if domain in text:
                keywords.append(domain)
                break

        # Look for style/quality
        styles = ["persuasive", "professional", "compelling", "engaging", "clear",
                 "creative", "technical", "concise", "detailed"]

        for style in styles:
            if style in text:
                keywords.append(style)
                break

        # Build name
        if len(keywords) >= 2:
            name = "-".join(keywords[:2])
        elif len(keywords) == 1:
            name = keywords[0]
        else:
            name = "ai-assistant"

        # Ensure it's valid
        name = re.sub(r'[^a-z0-9-]', '-', name)
        name = re.sub(r'-+', '-', name).strip('-')

        return name

    def generate_skill_description(self, prompt: Dict) -> str:
        """
        Generate a skill description from the prompt.

        Args:
            prompt: Prompt dictionary

        Returns:
            Skill description
        """
        text = prompt["text"]
        score = prompt["evaluation"]["average"]

        # Extract main purpose
        purpose = self._extract_purpose(text)

        desc = f"AI-powered {purpose} assistant. "

        # Add quality indicators
        if score >= 8.0:
            desc += "High-quality prompt optimization with "
        elif score >= 7.0:
            desc += "Effective prompt for "

        # Add use cases
        use_cases = self._extract_use_cases(text)
        if use_cases:
            desc += f"Ideal for {', '.join(use_cases[:3])}. "

        desc += "Use when you need help with " + purpose.lower() + " tasks."

        return desc

    def _extract_purpose(self, text: str) -> str:
        """Extract the main purpose from prompt text."""
        # Look for key action verbs
        actions = {
            "write": "writing",
            "create": "creating",
            "generate": "generating",
            "analyze": "analyzing",
            "summarize": "summarizing",
            "translate": "translating",
            "design": "designing",
            "build": "building",
            "code": "coding",
            "optimize": "optimizing",
            "improve": "improving"
        }

        text_lower = text.lower()
        for verb, purpose in actions.items():
            if verb in text_lower:
                return purpose

        return "AI assistance"

    def _extract_use_cases(self, text: str) -> List[str]:
        """Extract potential use cases from prompt."""
        use_cases = []

        # Email-related
        if "email" in text.lower():
            use_cases.extend(["email writing", "client communication"])

        # Code-related
        if "code" in text.lower() or "programming" in text.lower():
            use_cases.extend(["code generation", "code review"])

        # Writing-related
        if "write" in text.lower() or "article" in text.lower():
            use_cases.extend(["content creation", "article writing"])

        # Business-related
        if "business" in text.lower() or "marketing" in text.lower():
            use_cases.extend(["business communication", "marketing copy"])

        # Analysis-related
        if "analyze" in text.lower() or "analysis" in text.lower():
            use_cases.extend(["data analysis", "report generation"])

        # Default use case
        if not use_cases:
            use_cases.append("AI-powered assistance")

        return use_cases[:4]

    def create_skill_content(self, prompt: Dict, optimized_prompt: Optional[str] = None) -> str:
        """
        Create the SKILL.md content for a prompt.

        Args:
            prompt: Prompt dictionary with evaluation
            optimized_prompt: Optional optimized version of the prompt

        Returns:
            SKILL.md content
        """
        name = self.generate_skill_name(prompt)
        description = self.generate_skill_description(prompt)
        original_text = prompt["text"]
        score = prompt["evaluation"]["average"]
        tweet_url = prompt.get("url", "")

        # Use optimized prompt if provided, otherwise use original
        final_prompt = optimized_prompt if optimized_prompt else original_text

        skill_content = f"""---
name: {name}
description: {description}
---

# {self._format_title(name)}

## Quick Start

### When to Use This Skill

Use this skill when you need help with:
- {self._format_title(name)}
- {self._extract_purpose(original_text)}
- {', '.join(self._extract_use_cases(original_text)[:2])}

### Quality Score

This skill is based on a high-quality prompt (Score: {score:.1f}/10).

## The Optimized Prompt

Below is the optimized prompt that powers this skill. This prompt has been evaluated and refined for maximum effectiveness.

### Prompt Text

```
{final_prompt}
```

### Why This Works

This prompt scores highly on multiple dimensions:
- **Clarity** ({prompt['evaluation']['clarity']:.1f}/10): Clear and understandable instructions
- **Specificity** ({prompt['evaluation']['specificity']:.1f}/10): Specific requirements and constraints
- **Structure** ({prompt['evaluation']['structure']:.1f}/10): Well-organized and logical
- **Completeness** ({prompt['evaluation']['completeness']:.1f}/10): Contains necessary context
- **Utility** ({prompt['evaluation']['utility']:.1f}/10): Practical and actionable

## Usage Tips

1. **Customize as needed**: Feel free to modify the prompt for your specific use case
2. **Provide context**: Add relevant background information for better results
3. **Iterate**: Ask for revisions until you get the desired output
4. **Be specific**: More detailed instructions lead to better outputs

## Origin

This skill was created from a popular AI prompt shared on X ({tweet_url}).
The original prompt has been evaluated and optimized for use with Clawdbot.

---

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Quality score: {score:.1f}/10*
"""

        return skill_content

    def _format_title(self, name: str) -> str:
        """Convert kebab-case to Title Case."""
        return " ".join(word.capitalize() for word in name.split("-"))

    def convert_prompts_to_skills(self, high_quality_prompts: List[Dict]) -> List[Dict]:
        """
        Convert high-quality prompts to skill packages.

        Args:
            high_quality_prompts: List of evaluated prompts with high quality

        Returns:
            List of created skill information
        """
        created_skills = []

        for prompt in high_quality_prompts:
            try:
                # Generate skill metadata
                skill_name = self.generate_skill_name(prompt)
                skill_dir = self.output_dir / skill_name
                skill_dir.mkdir(exist_ok=True)

                # Create SKILL.md
                skill_content = self.create_skill_content(prompt)
                skill_file = skill_dir / "SKILL.md"

                with open(skill_file, "w", encoding="utf-8") as f:
                    f.write(skill_content)

                # Generate version
                version = "1.0." + datetime.now().strftime("%Y%m%d")

                skill_info = {
                    "name": skill_name,
                    "display_name": self._format_title(skill_name),
                    "version": version,
                    "directory": str(skill_dir),
                    "quality_score": prompt["evaluation"]["average"],
                    "source_url": prompt.get("url", ""),
                    "created_at": datetime.now().isoformat()
                }

                created_skills.append(skill_info)

                print(f"✓ Created skill: {skill_name}")

            except Exception as e:
                print(f"✗ Error creating skill for prompt: {e}")
                continue

        return created_skills

    def optimize_prompt(self, prompt_text: str, evaluation: Dict) -> str:
        """
        Simple prompt optimization based on evaluation.

        Args:
            prompt_text: Original prompt text
            evaluation: Evaluation scores

        Returns:
            Optimized prompt text
        """
        optimized = prompt_text

        # Add structure if score is low
        if evaluation["structure"] < 6.0:
            # Add clear sections
            if "##" not in optimized:
                optimized = f"## Task\n{optimized}\n\n## Requirements\n- Be specific and clear\n- Provide actionable output"

        # Add specificity if score is low
        if evaluation["specificity"] < 6.0:
            if "approximately" not in optimized.lower() and "about" not in optimized.lower():
                optimized = optimized + "\n\nNote: Be specific about length, format, and style preferences."

        # Add clarity if score is low
        if evaluation["clarity"] < 6.0:
            optimized = "You are a helpful AI assistant. " + optimized

        return optimized


def main():
    """Main function for testing."""
    # Test with sample prompt
    sample_prompt = {
        "text": "You are a professional email writer. Write a persuasive email to a potential client highlighting the benefits of our new product. Keep it under 200 words and include a clear call-to-action.",
        "url": "https://x.com/i/status/123456789",
        "metrics": {"retweet_count": 50, "like_count": 200, "reply_count": 10},
        "evaluation": {
            "clarity": 8.0,
            "specificity": 7.5,
            "structure": 6.0,
            "completeness": 7.0,
            "utility": 8.5,
            "average": 7.4,
            "tier": "good"
        }
    }

    converter = PromptToSkillConverter()

    print("=== Prompt to Skill Conversion ===\n")

    # Test name generation
    skill_name = converter.generate_skill_name(sample_prompt)
    print(f"Generated Skill Name: {skill_name}")

    # Test description generation
    description = converter.generate_skill_description(sample_prompt)
    print(f"\nDescription: {description}")

    # Test skill content creation
    print("\n=== Generated SKILL.md Preview ===")
    skill_content = converter.create_skill_content(sample_prompt)
    print(skill_content[:500] + "...")


if __name__ == "__main__":
    main()
