#!/usr/bin/env python3
"""Validate that all skill dependencies are met."""

import sys
import os
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    load_skill_metadata,
    get_all_skills,
    print_success,
    print_error,
    print_info,
    print_warning
)


DEPENDENCIES_FILE = ".dependencies.json"


def load_dependencies(skill_path: str) -> dict:
    """Load dependencies file or return empty dict."""
    deps_file = Path(skill_path) / DEPENDENCIES_FILE
    if deps_file.exists():
        with open(deps_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"dependencies": []}


def check_version_constraint(installed_version: str, constraint: str) -> bool:
    """Check if installed version satisfies constraint."""
    if constraint == '*':
        return True

    # Simple version comparison (supports >=, <=, >, <, ==)
    try:
        if constraint.startswith('>='):
            required = constraint[2:]
            return parse_version(installed_version) >= parse_version(required)
        elif constraint.startswith('<='):
            required = constraint[2:]
            return parse_version(installed_version) <= parse_version(required)
        elif constraint.startswith('>'):
            required = constraint[1:]
            return parse_version(installed_version) > parse_version(required)
        elif constraint.startswith('<'):
            required = constraint[1:]
            return parse_version(installed_version) < parse_version(required)
        elif constraint.startswith('=='):
            required = constraint[2:]
            return parse_version(installed_version) == parse_version(required)
        else:
            # Exact match
            return installed_version == constraint
    except:
        return False


def parse_version(version_str: str) -> tuple:
    """Parse version string into tuple."""
    parts = version_str.split('.')
    return tuple(int(p) for p in parts)


def get_installed_skill_version(skill_name: str, base_dir: str = "/root/clawd/skills") -> tuple:
    """Get installed skill version."""
    all_skills = get_all_skills(base_dir)

    for skill_path in all_skills:
        try:
            metadata = load_skill_metadata(str(skill_path))
            if metadata.get('name', '').lower() == skill_name.lower():
                # Check if skill has version tracking
                version_file = skill_path / ".versions" / "version.json"
                if version_file.exists():
                    with open(version_file, 'r', encoding='utf-8') as f:
                        version_data = json.load(f)
                        return (True, version_data.get('current_version', '0.0.0'))
                else:
                    # No version tracking
                    return (True, '0.0.0')
        except:
            continue

    return (False, None)


def validate_dependencies(skill_path: str) -> bool:
    """Validate all dependencies for a skill."""
    skill_path = Path(skill_path)

    # Load skill metadata
    try:
        metadata = load_skill_metadata(str(skill_path))
        skill_name = metadata.get('name', 'Unknown')
    except Exception as e:
        print_error(f"Failed to load skill metadata: {e}")
        return False

    print_info(f"Validating dependencies for: {skill_name}\n")

    # Load dependencies
    deps_data = load_dependencies(str(skill_path))
    dependencies = deps_data.get('dependencies', [])

    if not dependencies:
        print_success("No dependencies to validate ✨")
        return True

    print(f"📦 Checking {len(dependencies)} dependenc(ies)...\n")

    all_valid = True

    for dep in dependencies:
        dep_name = dep['name']
        dep_version = dep.get('version', '*')

        is_installed, installed_version = get_installed_skill_version(dep_name)

        if not is_installed:
            all_valid = False
            print_error(f"❌ {dep_name} (required: {dep_version})")
            print_info(f"    Status: NOT INSTALLED\n")
        else:
            if check_version_constraint(installed_version, dep_version):
                print_success(f"✅ {dep_name} (required: {dep_version}, installed: {installed_version})")
            else:
                all_valid = False
                print_error(f"❌ {dep_name} (required: {dep_version}, installed: {installed_version})")
                print_info(f"    Status: VERSION MISMATCH\n")

    print(f"{'='*60}")

    if all_valid:
        print_success("All dependencies satisfied! ✨")
        return True
    else:
        print_warning("Some dependencies are not satisfied")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_dependencies.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]

    if validate_dependencies(skill_path):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
