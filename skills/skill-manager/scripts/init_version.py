#!/usr/bin/env python3
"""Initialize version tracking for a skill."""

import sys
import os
import json
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    load_skill_metadata,
    print_success,
    print_error,
    print_info,
    ensure_dir
)


VERSION_FILE = "version.json"
VERSION_DIR = ".versions"


def init_version_tracking(skill_path: str) -> bool:
    """Initialize version tracking for a skill."""
    skill_path = Path(skill_path)
    version_dir = skill_path / VERSION_DIR
    version_file = version_dir / VERSION_FILE

    if version_file.exists():
        print_error("Version tracking already initialized for this skill.")
        return False

    # Create .versions directory
    ensure_dir(str(version_dir))

    # Load skill metadata
    try:
        metadata = load_skill_metadata(str(skill_path))
        skill_name = metadata.get('name', 'unknown')
    except Exception as e:
        print_error(f"Failed to load skill metadata: {e}")
        return False

    # Initialize version data
    version_data = {
        "skill_name": skill_name,
        "current_version": "0.1.0",
        "versions": [
            {
                "version": "0.1.0",
                "release_date": datetime.now().isoformat(),
                "changes": ["Initial version"],
                "type": "initial"
            }
        ]
    }

    # Write version file
    with open(version_file, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2)

    print_success(f"Version tracking initialized for {skill_name}")
    print_info(f"  Current version: 0.1.0")
    print_info(f"  Version file: {version_file}")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 init_version.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]

    if init_version_tracking(skill_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
