#!/usr/bin/env python3
"""
Main Harvester Script
Orchestrates the entire AI prompt harvesting and skill publishing process.
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from search_x import TwitterSearcher
from evaluate import PromptEvaluator
from convert_to_skill import PromptToSkillConverter
from publish import SkillPublisher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIHarvester:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.state_dir = self.base_dir / "state"
        self.state_dir.mkdir(exist_ok=True)

        # Load state
        self.processed_prompts = self._load_state("processed_prompts.json", set())
        self.published_skills = self._load_state("published_skills.json", [])

        # Initialize components
        self._check_api_key()
        self.searcher = TwitterSearcher(os.environ["TWITTER_API_KEY"])
        self.evaluator = PromptEvaluator()
        self.converter = PromptToSkillConverter(self.base_dir / "skills-generated")
        self.publisher = SkillPublisher()

    def _check_api_key(self):
        """Check if Twitter API key is configured."""
        if "TWITTER_API_KEY" not in os.environ:
            logger.error("TWITTER_API_KEY environment variable not set")
            logger.error("Set it with: export TWITTER_API_KEY='your_key_here'")
            sys.exit(1)

    def _load_state(self, filename: str, default):
        """Load state from file."""
        filepath = self.state_dir / filename
        if filepath.exists():
            with open(filepath, "r") as f:
                return json.load(f)
        return default

    def _save_state(self, filename: str, data):
        """Save state to file."""
        filepath = self.state_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _is_already_processed(self, prompt_text: str) -> bool:
        """Check if prompt was already processed."""
        # Simple hash-based check
        text_hash = hash(prompt_text)
        return str(text_hash) in self.processed_prompts

    def _mark_as_processed(self, prompt_text: str):
        """Mark prompt as processed."""
        text_hash = str(hash(prompt_text))
        self.processed_prompts.add(text_hash)

    def _is_skill_published(self, skill_name: str) -> bool:
        """Check if skill was already published."""
        return any(skill["name"] == skill_name for skill in self.published_skills)

    def _record_run(self, stats: dict):
        """Record this run's statistics."""
        record_file = self.state_dir / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(record_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

    def run(self, auto_publish: bool = False):
        """
        Run the complete harvesting pipeline.

        Args:
            auto_publish: If True, automatically publish skills. If False, only create them.
        """
        logger.info("=" * 60)
        logger.info("Starting AI Prompt Harvesting Pipeline")
        logger.info("=" * 60)

        stats = {
            "start_time": datetime.now().isoformat(),
            "searched": 0,
            "evaluated": 0,
            "high_quality": 0,
            "converted": 0,
            "published": 0,
            "errors": []
        }

        try:
            # Step 1: Search for prompts
            logger.info("\n[Step 1/4] Searching X for AI prompts...")
            raw_prompts = self.searcher.search_prompts(max_results_per_query=50)
            stats["searched"] = len(raw_prompts)
            logger.info(f"Found {len(raw_prompts)} raw prompts")

            # Filter already processed prompts
            new_prompts = [p for p in raw_prompts if not self._is_already_processed(p["text"])]
            logger.info(f"Filtered to {len(new_prompts)} new prompts")

            if not new_prompts:
                logger.info("No new prompts to process. Exiting.")
                return

            # Step 2: Evaluate quality
            logger.info("\n[Step 2/4] Evaluating prompt quality...")
            evaluated_prompts = self.evaluator.evaluate_batch(new_prompts)
            stats["evaluated"] = len(evaluated_prompts)
            logger.info(f"Evaluated {len(evaluated_prompts)} prompts")

            # Deduplicate
            deduplicated = self.evaluator.deduplicate_prompts(evaluated_prompts)
            logger.info(f"Deduplicated to {len(deduplicated)} unique prompts")

            # Filter by quality
            high_quality, low_quality = self.evaluator.filter_by_quality(deduplicated)
            stats["high_quality"] = len(high_quality)
            logger.info(f"Found {len(high_quality)} high-quality prompts (>= 7.0/10)")
            logger.info(f"Found {len(low_quality)} low-quality prompts (< 7.0/10)")

            # Step 3: Convert to skills
            logger.info("\n[Step 3/4] Converting high-quality prompts to skills...")
            created_skills = self.converter.convert_prompts_to_skills(high_quality)

            # Filter already published skills
            new_skills = [s for s in created_skills if not self._is_skill_published(s["name"])]
            stats["converted"] = len(new_skills)

            logger.info(f"Created {len(created_skills)} skills")
            logger.info(f"Filtered to {len(new_skills)} unpublished skills")

            if not new_skills:
                logger.info("No new skills to publish. Exiting.")
                self._save_processed_prompts(new_prompts)
                return

            # Step 4: Publish to ClawdHub (optional)
            if auto_publish:
                logger.info("\n[Step 4/4] Publishing skills to ClawdHub...")
                publish_stats = self.publisher.publish_batch(new_skills)
                stats["published"] = publish_stats["success"]
                stats["errors"].extend(f"Publish error: {skill_info.get('name', 'unknown')}"
                                       for skill_info in new_skills
                                       if skill_info["name"] not in [s["name"] for s in publish_stats.get("published_skills", [])])

                # Save publish record
                self.publisher.save_publish_record(publish_stats)

                logger.info(f"Published {publish_stats['success']}/{publish_stats['total']} skills")
            else:
                logger.info("\n[Step 4/4] Skipping auto-publish (skills ready for review)")
                logger.info("Skill directories created in: skills-generated/")
                logger.info("Review and publish manually with:")
                for skill in new_skills:
                    logger.info(f"  clawdhub publish {skill['directory']}")

            # Mark prompts as processed
            self._save_processed_prompts(new_prompts)

        except Exception as e:
            logger.error(f"Error during harvesting: {e}", exc_info=True)
            stats["errors"].append(str(e))

        # Finalize
        stats["end_time"] = datetime.now().isoformat()
        stats["duration_seconds"] = (datetime.fromisoformat(stats["end_time"]) -
                                     datetime.fromisoformat(stats["start_time"])).total_seconds()

        self._record_run(stats)

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("Harvesting Complete!")
        logger.info("=" * 60)
        logger.info(f"Searched: {stats['searched']} prompts")
        logger.info(f"Evaluated: {stats['evaluated']} prompts")
        logger.info(f"High Quality: {stats['high_quality']} prompts")
        logger.info(f"Converted: {stats['converted']} skills")
        logger.info(f"Published: {stats['published']} skills")
        logger.info(f"Duration: {stats['duration_seconds']:.1f} seconds")

        if stats["errors"]:
            logger.warning(f"\nErrors encountered: {len(stats['errors'])}")

    def _save_processed_prompts(self, prompts: list):
        """Save prompts as processed."""
        for prompt in prompts:
            self._mark_as_processed(prompt["text"])
        self._save_state("processed_prompts.json", list(self.processed_prompts))


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="AI Prompt Harvester for Clawdbot Skills")
    parser.add_argument("--auto-publish", action="store_true",
                        help="Automatically publish skills to ClawdHub")
    parser.add_argument("--test", action="store_true",
                        help="Run in test mode (don't publish)")

    args = parser.parse_args()

    harvester = AIHarvester()

    if args.test:
        logger.info("Running in TEST mode - no publishing will occur")
        harvester.run(auto_publish=False)
    else:
        harvester.run(auto_publish=args.auto_publish)


if __name__ == "__main__":
    main()
