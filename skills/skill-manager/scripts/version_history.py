#!/usr/bin/env python3
"""Display version history for a skill."""

import sys
import os
import json
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import print_success, print_error, print_info, print_warning


VERSION_FILE = ".versions/version.json"


def display_version_history(skill_path: str) -> bool:
    """Display version history for a skill."""
    skill_path = Path(skill_path)
    version_file = skill_path / VERSION_FILE

    if not version_file.exists():
        print_error("Version tracking not initialized. Run init_version.py first.")
        return False

    # Load version data
    with open(version_file, 'r', encoding='utf-8') as f:
        version_data = json.load(f)

    skill_name = version_data.get('skill_name', 'Unknown')
    current_version = version_data.get('current_version', 'Unknown')
    versions = version_data.get('versions', [])

    print(f"{'='*60}")
    print(f"Version History: {skill_name}")
    print(f"{'='*60}\n")

    print(f"📍 Current Version: {current_version}\n")
    print("📜 Version History:\n")

    # Display versions in reverse chronological order
    for version_info in reversed(versions):
        version = version_info['version']
        release_date = version_info['release_date']
        changes = version_info.get('changes', [])

        # Parse and format date
        try:
            dt = datetime.fromisoformat(release_date)
            date_str = dt.strftime('%Y-%m-%d %H:%M')
        except:
            date_str = release_date

        # Check if this is the current version
        is_current = version == current_version
        prefix = "★ " if is_current else "  "

        print(f"{prefix}v{version} ({date_str})")

        for change in changes:
            print(f"      • {change}")

        print()

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 version_history.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]

    if display_version_history(skill_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
