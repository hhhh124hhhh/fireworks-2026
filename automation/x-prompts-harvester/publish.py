#!/usr/bin/env python3
"""
Skill Publisher Module
Publishes generated skills to ClawdHub.
"""

import os
import json
import subprocess
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

class SkillPublisher:
    def __init__(self):
        self.workdir = Path.cwd()

    def check_clawdhub_installed(self) -> bool:
        """Check if clawdhub CLI is installed."""
        try:
            result = subprocess.run(
                ["clawdhub", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False

    def package_skill(self, skill_dir: Path) -> Optional[str]:
        """
        Package a skill using package_skill.py.

        Args:
            skill_dir: Path to skill directory

        Returns:
            Path to packaged .skill file, or None if failed
        """
        try:
            # Find package_skill.py in Clawdbot skills directory
            package_script = Path("/usr/lib/node_modules/clawdbot/skills/skill-creator/scripts/package_skill.py")

            if not package_script.exists():
                print(f"Warning: package_skill.py not found at {package_script}")
                return None

            # Run packaging script
            result = subprocess.run(
                ["python3", str(package_script), str(skill_dir)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode != 0:
                print(f"Packaging failed for {skill_dir.name}: {result.stderr}")
                return None

            # Find the generated .skill file
            skill_files = list(self.workdir.glob(f"{skill_dir.name}.skill"))
            if skill_files:
                return str(skill_files[0])

            print(f"Warning: No .skill file generated for {skill_dir.name}")
            return None

        except Exception as e:
            print(f"Error packaging skill {skill_dir.name}: {e}")
            return None

    def publish_skill(self, skill_info: Dict, skill_file: str) -> bool:
        """
        Publish a skill to ClawdHub.

        Args:
            skill_info: Skill information dictionary
            skill_file: Path to .skill file

        Returns:
            True if published successfully, False otherwise
        """
        name = skill_info["name"]
        display_name = skill_info["display_name"]
        version = skill_info["version"]
        quality_score = skill_info["quality_score"]

        # Generate changelog
        changelog = self._generate_changelog(skill_info)

        try:
            # Publish using clawdhub CLI
            cmd = [
                "clawdhub", "publish", skill_file,
                "--slug", name,
                "--name", display_name,
                "--version", version,
                "--changelog", changelog
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                print(f"Publishing failed for {name}: {result.stderr}")
                return False

            print(f"✓ Published: {name} v{version}")
            return True

        except Exception as e:
            print(f"Error publishing skill {name}: {e}")
            return False

    def _generate_changelog(self, skill_info: Dict) -> str:
        """Generate changelog for skill."""
        quality_score = skill_info["quality_score"]
        source_url = skill_info.get("source_url", "")

        changelog = f"Initial release"

        if quality_score >= 8.0:
            changelog += ". High-quality prompt optimization."
        elif quality_score >= 7.0:
            changelog += ". Effective and well-structured prompt."

        if source_url:
            changelog += f"\n\nBased on popular AI prompt from X."

        return changelog

    def determine_price(self, skill_info: Dict) -> float:
        """
        Determine pricing for a skill based on quality.

        Args:
            skill_info: Skill information with quality score

        Returns:
            Price in USD
        """
        quality_score = skill_info["quality_score"]

        if quality_score >= 8.0:
            return 5.0  # $5-10 for high quality
        elif quality_score >= 7.0:
            return 3.0  # $3-5 for good quality
        else:
            return 1.0  # $1-3 for basic skills

    def publish_batch(self, skills_to_publish: List[Dict]) -> Dict:
        """
        Publish a batch of skills to ClawdHub.

        Args:
            skills_to_publish: List of skill information dictionaries

        Returns:
            Dictionary with publish statistics
        """
        if not self.check_clawdhub_installed():
            print("Error: clawdhub CLI is not installed")
            print("Install with: npm i -g clawdhub")
            return {
                "success": 0,
                "failed": 0,
                "total": 0
            }

        stats = {
            "success": 0,
            "failed": 0,
            "total": len(skills_to_publish),
            "published_skills": []
        }

        for skill_info in skills_to_publish:
            skill_dir = Path(skill_info["directory"])

            print(f"\nProcessing: {skill_info['name']}")

            # Package skill
            skill_file = self.package_skill(skill_dir)
            if not skill_file:
                print(f"✗ Failed to package: {skill_info['name']}")
                stats["failed"] += 1
                continue

            # Publish skill
            if self.publish_skill(skill_info, skill_file):
                stats["success"] += 1
                stats["published_skills"].append({
                    "name": skill_info["name"],
                    "version": skill_info["version"],
                    "price": self.determine_price(skill_info),
                    "published_at": datetime.now().isoformat()
                })
            else:
                stats["failed"] += 1

        return stats

    def save_publish_record(self, stats: Dict, record_file: str = "state/published_skills.json"):
        """
        Save publishing record to file.

        Args:
            stats: Publishing statistics
            record_file: Path to record file
        """
        record_path = Path(record_file)
        record_path.parent.mkdir(exist_ok=True)

        # Load existing records
        existing_records = []
        if record_path.exists():
            with open(record_path, "r") as f:
                existing_records = json.load(f)

        # Add new records
        new_records = stats.get("published_skills", [])
        existing_records.extend(new_records)

        # Save
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(existing_records, f, indent=2, ensure_ascii=False)

        print(f"\nSaved publish record to {record_file}")


def main():
    """Main function for testing."""
    publisher = SkillPublisher()

    print("=== ClawdHub Skill Publisher ===\n")

    # Check if clawdhub is installed
    if publisher.check_clawdhub_installed():
        print("✓ ClawdHub CLI is installed")
    else:
        print("✗ ClawdHub CLI is not installed")
        print("  Install with: npm i -g clawdhub")


if __name__ == "__main__":
    main()
