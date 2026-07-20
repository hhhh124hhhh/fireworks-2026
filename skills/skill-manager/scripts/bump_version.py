#!/usr/bin/env python3
"""Bump skill version (major, minor, or patch)."""

import sys
import os
import json
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    print_success,
    print_error,
    print_info,
    print_warning
)


VERSION_FILE = ".versions/version.json"
CHANGE_TYPES = ['major', 'minor', 'patch']


def parse_version(version_str: str) -> tuple:
    """Parse version string into major, minor, patch."""
    parts = version_str.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version_str}")
    return tuple(int(p) for p in parts)


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version tuple as string."""
    return f"{major}.{minor}.{patch}"


def bump_version(skill_path: str, bump_type: str, change_notes: list = None) -> bool:
    """Bump skill version."""
    if bump_type not in CHANGE_TYPES:
        print_error(f"Invalid bump type: {bump_type}. Must be one of: {', '.join(CHANGE_TYPES)}")
        return False

    skill_path = Path(skill_path)
    version_file = skill_path / VERSION_FILE

    if not version_file.exists():
        print_error("Version tracking not initialized. Run init_version.py first.")
        return False

    # Load version data
    with open(version_file, 'r', encoding='utf-8') as f:
        version_data = json.load(f)

    current_version = version_data['current_version']
    major, minor, patch = parse_version(current_version)

    # Bump version
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    else:  # patch
        patch += 1

    new_version = format_version(major, minor, patch)

    # Add version history
    version_entry = {
        "version": new_version,
        "release_date": datetime.now().isoformat(),
        "changes": change_notes or [f"Bumped {bump_type} version"],
        "type": bump_type,
        "previous_version": current_version
    }

    version_data['versions'].append(version_entry)
    version_data['current_version'] = new_version

    # Write updated version data
    with open(version_file, 'w', encoding='utf-8') as f:
        json.dump(version_data, f, indent=2)

    print_success(f"Version bumped from {current_version} to {new_version}")
    print_info(f"  Type: {bump_type}")
    if change_notes:
        print_info(f"  Changes: {', '.join(change_notes)}")

    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 bump_version.py <skill-path> --type <major|minor|patch>")
        print("       python3 bump_version.py <skill-path> --type <major|minor|patch> --note \"change description\"")
        sys.exit(1)

    skill_path = sys.argv[1]
    bump_type = None
    change_notes = []

    # Parse arguments
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '--type' and i + 1 < len(sys.argv):
            bump_type = sys.argv[i + 1]
        elif sys.argv[i] == '--note' and i + 1 < len(sys.argv):
            change_notes.append(sys.argv[i + 1])

    if not bump_type:
        print_error("--type is required")
        sys.exit(1)

    if bump_version(skill_path, bump_type, change_notes):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
