#!/usr/bin/env python3
"""Publish a skill to ClawdHub."""

import sys
import os
import subprocess
from pathlib import Path
import json

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import print_success, print_error, print_warning, print_info, ensure_dir


def load_clawdhub_config() -> dict:
    """Load ClawdHub configuration."""
    config_path = Path.home() / ".config" / "clawdhub" / "config.json"

    if not config_path.exists():
        print_error("ClawdHub config not found. Please run 'clawdhub login' first.")
        return None

    with open(config_path, 'r') as f:
        return json.load(f)


def check_clawdhub_token() -> bool:
    """Check if ClawdHub token is valid."""
    try:
        result = subprocess.run(
            ['clawdhub', 'list'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return True
        else:
            print_warning("ClawdHub token may be invalid. Will attempt to publish anyway.")
            return True  # Continue anyway

    except FileNotFoundError:
        print_error("clawdhub CLI not found. Please install it first.")
        return False
    except subprocess.TimeoutExpired:
        print_warning("ClawdHub CLI timeout. Will attempt to publish anyway.")
        return True  # Continue anyway
    except Exception as e:
        print_warning(f"Error checking ClawdHub token: {e}")
        return True  # Continue anyway


def package_skill(skill_path: str, output_dir: str = None) -> str:
    """Package skill into .skill file."""
    skill_path = Path(skill_path)

    if not skill_path.exists():
        print_error(f"Skill path not found: {skill_path}")
        return None

    # Determine output directory
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = skill_path.parent / "dist"

    ensure_dir(str(output_path))

    # Run package_skill.py
    package_script = Path.home() / ".clawdbot" / "scripts" / "package_skill.py"

    if not package_script.exists():
        print_error("package_skill.py not found. Please ensure Clawdbot is properly installed.")
        return None

    cmd = [sys.executable, str(package_script), str(skill_path), str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print_success("Skill packaged successfully")

        # Find the generated .skill file
        skill_files = list(output_path.glob("*.skill"))
        if skill_files:
            skill_file = skill_files[0]
            print_info(f"Package: {skill_file}")
            return str(skill_file)
        else:
            print_error("No .skill file found after packaging")
            return None
    else:
        print_error("Skill packaging failed")
        if result.stderr:
            print(result.stderr)
        return None


def publish_to_clawdhub(skill_file: str, registry: str = "https://www.clawhub.ai/api") -> bool:
    """Publish .skill file to ClawdHub."""
    skill_file = Path(skill_file)

    if not skill_file.exists():
        print_error(f"Skill file not found: {skill_file}")
        return False

    print_info(f"Publishing {skill_file.name} to ClawdHub...")
    print(f"Registry: {registry}")

    # Run clawdhub publish
    cmd = ['clawdhub', 'publish', str(skill_file), '--registry', registry]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            print_success("Skill published to ClawdHub successfully! ✨")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print_error("Failed to publish to ClawdHub")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print_error("Publish timeout. Please try again later.")
        return False
    except Exception as e:
        print_error(f"Error publishing to ClawdHub: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 publish.py <skill-path> [--registry <url>] [--output <dir>]")
        print("\nOptions:")
        print("  --registry <url>  ClawdHub registry URL (default: https://www.clawhub.ai/api)")
        print("  --output <dir>    Output directory for .skill file (default: ../dist)")
        sys.exit(1)

    skill_path = sys.argv[1]

    # Parse optional arguments
    registry = "https://www.clawhub.ai/api"
    output_dir = None

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '--registry' and i + 1 < len(sys.argv):
            registry = sys.argv[i + 1]
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]

    print_info(f"Publishing skill: {skill_path}")
    print("="*60 + "\n")

    # Check ClawdHub token
    print("🔐 Checking ClawdHub token...")
    if not check_clawdhub_token():
        sys.exit(1)

    # Package skill
    print(f"\n📦 Packaging skill...")
    skill_file = package_skill(skill_path, output_dir)

    if not skill_file:
        sys.exit(1)

    # Publish to ClawdHub
    print(f"\n🚀 Publishing to ClawdHub...")
    success = publish_to_clawdhub(skill_file, registry)

    if success:
        print(f"\n{'='*60}")
        print_success("Skill published successfully!")
        print_info(f"Skill file: {skill_file}")
        print(f"{'='*60}\n")
        return 0
    else:
        print(f"\n{'='*60}")
        print_error("Failed to publish skill")
        print(f"{'='*60}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
