#!/usr/bin/env python3
"""Add a dependency to a skill."""

import sys
import os
import json
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import print_success, print_error, print_info


DEPENDENCIES_FILE = ".dependencies.json"


def load_dependencies(skill_path: str) -> dict:
    """Load dependencies file or return empty dict."""
    deps_file = Path(skill_path) / DEPENDENCIES_FILE
    if deps_file.exists():
        with open(deps_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"dependencies": []}


def save_dependencies(skill_path: str, data: dict):
    """Save dependencies file."""
    deps_file = Path(skill_path) / DEPENDENCIES_FILE
    with open(deps_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def add_dependency(skill_path: str, dependency_name: str, version_constraint: str = None) -> bool:
    """Add a dependency to a skill."""
    skill_path = Path(skill_path)
    deps_file = skill_path / DEPENDENCIES_FILE

    # Load existing dependencies
    deps_data = load_dependencies(str(skill_path))
    dependencies = deps_data['dependencies']

    # Check if dependency already exists
    for dep in dependencies:
        if dep['name'] == dependency_name:
            print_error(f"Dependency '{dependency_name}' already exists")
            return False

    # Add new dependency
    new_dep = {
        'name': dependency_name,
        'version': version_constraint or '*',
        'added_date': datetime.now().isoformat()
    }

    dependencies.append(new_dep)
    deps_data['dependencies'] = dependencies

    # Save
    save_dependencies(str(skill_path), deps_data)

    version_str = f" (version: {version_constraint})" if version_constraint else ""
    print_success(f"Added dependency: {dependency_name}{version_str}")
    print_info(f"  Dependencies file: {deps_file}")

    return True


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 add_dependency.py <skill-path> --dependency <skill-name>")
        print("       python3 add_dependency.py <skill-path> --dependency <skill-name> --version \">=1.0.0\"")
        sys.exit(1)

    skill_path = sys.argv[1]
    dependency_name = None
    version_constraint = None

    # Parse arguments
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '--dependency' and i + 1 < len(sys.argv):
            dependency_name = sys.argv[i + 1]
        elif sys.argv[i] == '--version' and i + 1 < len(sys.argv):
            version_constraint = sys.argv[i + 1]

    if not dependency_name:
        print_error("--dependency is required")
        sys.exit(1)

    if add_dependency(skill_path, dependency_name, version_constraint):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
