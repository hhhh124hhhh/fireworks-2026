#!/usr/bin/env python3
"""
Twitter (X) Prompt Scanner for WeChat Cover Generator

Scans X (Twitter) for high-quality AI image generation prompts,
extracts promising examples, and saves them for integration.

Usage:
    python3 scan_twitter_prompts.py
"""

import json
import os
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TwitterPromptScanner:
    """Scan X for AI art prompts and extract high-quality examples."""

    def __init__(self):
        self.output_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_file = os.path.join(self.output_dir, "extracted_prompts.json")
        self.log_file = os.path.join(self.output_dir, "scan_log.txt")

        # Configuration
        self.queries = [
            "AI art prompt",
            "Midjourney prompt template",
            "Stable Diffusion prompt",
            "WeChat cover AI",
            "Chinese AI art prompt",
            "AI image generation prompt"
        ]

        self.min_likes = 100
        self.min_retweets = 20
        self.max_results_per_query = 50

        # Load existing prompts for deduplication
        self.existing_prompts = self._load_existing_prompts()

    def _load_existing_prompts(self) -> set:
        """Load existing prompts to avoid duplicates."""
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {p['prompt'] for p in data.get('prompts', [])}
            except Exception as e:
                self._log(f"Warning: Could not load existing prompts: {e}")
        return set()

    def _log(self, message: str):
        """Write to log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"
        print(log_line.strip())

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)

    def _search_twitter(self, query: str) -> List[Dict]:
        """Search Twitter for prompts using bird CLI (if available)."""
        prompts = []

        # Try using bird CLI if available
        try:
            # Check if bird CLI is installed
            subprocess.run(['bird', '--version'],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         check=True)

            self._log(f"Searching Twitter for: {query}")

            # Search command
            cmd = ['bird', 'search', '--count', str(self.max_results_per_query), query]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0 and result.stdout:
                # Parse bird output (simplified parsing)
                tweets = self._parse_bird_output(result.stdout)
                prompts.extend(tweets)

        except FileNotFoundError:
            self._log("Bird CLI not found. Using placeholder data for demonstration.")
            prompts = self._get_placeholder_prompts(query)

        except Exception as e:
            self._log(f"Error searching Twitter for '{query}': {e}")

        # Filter by engagement
        filtered = [
            p for p in prompts
            if p.get('likes', 0) >= self.min_likes
            or p.get('retweets', 0) >= self.min_retweets
        ]

        self._log(f"Found {len(prompts)} tweets, {len(filtered)} meet engagement criteria")
        return filtered

    def _parse_bird_output(self, output: str) -> List[Dict]:
        """Parse bird CLI output into structured data."""
        prompts = []

        # Simplified parsing - in real implementation, this would parse actual JSON/structured output
        lines = output.split('\n')

        for line in lines:
            # Look for prompt-like patterns in tweets
            if any(keyword in line.lower() for keyword in ['prompt', 'midjourney', 'stable diffusion']):
                # Extract prompt-like text (simplified)
                if ':' in line or 'prompt' in line.lower():
                    prompt_text = self._extract_prompt_text(line)
                    if prompt_text and len(prompt_text) > 20:  # Minimum reasonable length
                        prompts.append({
                            'prompt': prompt_text,
                            'source': 'Twitter search',
                            'likes': 150,  # Placeholder - would be parsed from actual output
                            'retweets': 30,
                            'date': datetime.now().isoformat(),
                            'url': '',
                            'category': self._categorize_prompt(prompt_text)
                        })

        return prompts

    def _extract_prompt_text(self, text: str) -> Optional[str]:
        """Extract prompt text from tweet content."""
        # Look for patterns like:
        # "Prompt: ..." or "The prompt is: ..."
        # or content between quotes

        import re

        # Pattern 1: "Prompt: ..."
        match = re.search(r'prompt[:\s]+(.+)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Pattern 2: Content in quotes
        match = re.search(r'"([^"]{20,})"', text)
        if match:
            return match.group(1)

        # Pattern 3: Look for descriptive sentences (heuristic)
        if ' and ' in text and len(text) > 50:
            return text.strip()

        return None

    def _categorize_prompt(self, prompt: str) -> str:
        """Categorize prompt by content."""
        prompt_lower = prompt.lower()

        categories = {
            'business': ['business', 'corporate', 'finance', 'fintech', 'investment'],
            'technology': ['ai', 'tech', 'software', 'digital', 'cyber'],
            'lifestyle': ['food', 'travel', 'fashion', 'lifestyle', 'wellness'],
            'education': ['education', 'learn', 'tutorial', 'course'],
            'artistic': ['art', 'design', 'creative', 'abstract', 'surreal']
        }

        for category, keywords in categories.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return category

        return 'general'

    def _get_placeholder_prompts(self, query: str) -> List[Dict]:
        """Get placeholder prompts for demonstration (when Twitter API unavailable)."""
        self._log(f"Using placeholder prompts for query: {query}")

        placeholders = [
            {
                'prompt': "A professional business cover for WeChat official account, minimalist design with geometric shapes, navy blue and silver color scheme, clean text space, 900x383 aspect ratio, --ar 2.35:1",
                'source': 'placeholder',
                'likes': 1500,
                'retweets': 300,
                'date': datetime.now().isoformat(),
                'url': '',
                'category': 'business'
            },
            {
                'prompt': "Modern fintech cover with blockchain network visualization, interconnected glowing nodes, deep blue and emerald green gradients, clean headline space on left, 900x383 aspect ratio --ar 2.35:1",
                'source': 'placeholder',
                'likes': 1200,
                'retweets': 250,
                'date': datetime.now().isoformat(),
                'url': '',
                'category': 'technology'
            },
            {
                'prompt': "Vibrant food photography cover, close-up shot of steaming cuisine, warm natural lighting, shallow depth of field, clean text space on left, magazine-quality, 900x383 aspect ratio --ar 2.35:1",
                'source': 'placeholder',
                'likes': 800,
                'retweets': 150,
                'date': datetime.now().isoformat(),
                'url': '',
                'category': 'lifestyle'
            }
        ]

        # Return filtered by query relevance
        query_lower = query.lower()
        if 'business' in query_lower or 'finance' in query_lower:
            return [placeholders[0]]
        elif 'tech' in query_lower or 'ai' in query_lower:
            return [placeholders[1]]
        elif 'food' in query_lower or 'lifestyle' in query_lower:
            return [placeholders[2]]
        else:
            return placeholders

    def _evaluate_prompt_quality(self, prompt_data: Dict) -> float:
        """Evaluate prompt quality (0-10)."""
        prompt = prompt_data.get('prompt', '').lower()

        score = 0.0

        # Technical quality
        if '900x383' in prompt or '2.35:1' in prompt:
            score += 3.0
        if '4k' in prompt or 'high quality' in prompt:
            score += 2.0
        if any(word in prompt for word in ['photograph', 'illustration', 'render', '3d']):
            score += 2.0

        # WeChat optimization
        if 'wechat' in prompt or 'official account' in prompt:
            score += 2.0
        if 'headline space' in prompt or 'text space' in prompt:
            score += 2.0

        # Specificity
        if len(prompt.split()) > 20:
            score += 1.0

        return min(score, 10.0)

    def _adapt_for_wechat(self, prompt: str) -> str:
        """Adapt a prompt for WeChat cover specifications."""
        adapted = prompt

        # Add aspect ratio if missing
        if '2.35:1' not in adapted and '900x383' not in adapted:
            adapted += ", 900x383 aspect ratio --ar 2.35:1"

        # Add WeChat context if missing
        if 'wechat' not in adapted.lower() and 'official account' not in adapted.lower():
            adapted = "for WeChat official account, " + adapted

        # Add text space if missing
        if 'headline space' not in adapted.lower() and 'text space' not in adapted.lower():
            adapted += ", clean headline space on left side"

        # Add quality if missing
        if '4k' not in adapted and 'high quality' not in adapted:
            adapted += ", 4K quality"

        return adapted

    def run(self):
        """Run the scanning process."""
        self._log("="*70)
        self._log("Starting Twitter prompt scan")
        self._log("="*70)

        all_prompts = []

        # Search for each query
        for query in self.queries:
            self._log(f"\n--- Processing query: {query} ---")
            prompts = self._search_twitter(query)

            # Evaluate and adapt prompts
            for prompt_data in prompts:
                prompt_text = prompt_data['prompt']

                # Skip duplicates
                if prompt_text in self.existing_prompts:
                    continue

                # Evaluate quality
                quality_score = self._evaluate_prompt_quality(prompt_data)
                prompt_data['quality_score'] = quality_score

                # Adapt for WeChat if needed
                prompt_data['adapted_prompt'] = self._adapt_for_wechat(prompt_text)

                # Only keep high-quality prompts
                if quality_score >= 5.0:
                    all_prompts.append(prompt_data)

            # Add delay between queries to avoid rate limiting
            time.sleep(2)

        # Deduplicate
        unique_prompts = []
        seen_prompts = set()
        for prompt in all_prompts:
            if prompt['prompt'] not in seen_prompts:
                unique_prompts.append(prompt)
                seen_prompts.add(prompt['prompt'])

        self._log(f"\n--- Scan Complete ---")
        self._log(f"Total unique high-quality prompts found: {len(unique_prompts)}")

        # Save results
        if unique_prompts:
            self._save_prompts(unique_prompts)
        else:
            self._log("No new high-quality prompts found in this scan")

        self._log("="*70)

        return unique_prompts

    def _save_prompts(self, prompts: List[Dict]):
        """Save prompts to output file."""
        # Load existing data
        existing_data = {'prompts': [], 'last_scan': None}
        if os.path.exists(self.output_file):
            try:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except Exception as e:
                self._log(f"Warning: Could not load existing data: {e}")

        # Add new prompts
        existing_prompts_set = {p['prompt'] for p in existing_data['prompts']}
        new_prompts = [p for p in prompts if p['prompt'] not in existing_prompts_set]
        existing_data['prompts'].extend(new_prompts)

        # Update metadata
        existing_data['last_scan'] = datetime.now().isoformat()
        existing_data['total_prompts'] = len(existing_data['prompts'])

        # Save
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            self._log(f"Saved {len(new_prompts)} new prompts to {self.output_file}")
            self._log(f"Total prompts in library: {existing_data['total_prompts']}")

        except Exception as e:
            self._log(f"Error saving prompts: {e}")

def main():
    """Main entry point."""
    print("\n" + "="*70)
    print("TWITTER PROMPT SCANNER")
    print("WeChat Cover Generator Skill")
    print("="*70 + "\n")

    scanner = TwitterPromptScanner()

    try:
        prompts = scanner.run()

        # Print summary
        print(f"\nScan Summary:")
        print(f"  High-quality prompts found: {len(prompts)}")

        if prompts:
            print(f"\nTop 3 prompts:")
            for i, prompt in enumerate(prompts[:3], 1):
                print(f"\n  {i}. Quality: {prompt['quality_score']:.1f}/10")
                print(f"     Category: {prompt['category']}")
                print(f"     Likes: {prompt['likes']}")
                print(f"     Prompt: {prompt['prompt'][:80]}...")

        print(f"\nResults saved to: {scanner.output_file}")
        print(f"Log saved to: {scanner.log_file}")

    except KeyboardInterrupt:
        print("\n\nScan interrupted by user")
    except Exception as e:
        print(f"\nError during scan: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
