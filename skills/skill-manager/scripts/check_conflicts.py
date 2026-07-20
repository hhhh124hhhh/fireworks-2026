#!/usr/bin/env python3
"""Check for conflicts between skill dependencies."""

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


def collect_all_dependencies(skill_path: str, base_dir: str = "/root/clawd/skills", visited: set = None) -> dict:
    """Collect all dependencies recursively (including transitive)."""
    if visited is None:
        visited = set()

    skill_path = str(skill_path)
    skill_key = skill_path

    if skill_key in visited:
        return {}

    visited.add(skill_key)

    # Load dependencies
    deps_data = load_dependencies(skill_path)
    dependencies = deps_data.get('dependencies', [])

    result = {}

    for dep in dependencies:
        dep_name = dep['name']
        dep_version = dep.get('version', '*')

        # Record this dependency
        if dep_name not in result:
            result[dep_name] = []

        result[dep_name].append({
            'version': dep_version,
            'source': skill_path
        })

        # Find the dependency skill and check its dependencies
        all_skills = get_all_skills(base_dir)
        for skill in all_skills:
            try:
                metadata = load_skill_metadata(str(skill))
                if metadata.get('name', '').lower() == dep_name.lower():
                    # Recursively collect transitive dependencies
                    transitive = collect_all_dependencies(str(skill), base_dir, visited)
                    for trans_dep_name, trans_versions in transitive.items():
                        if trans_dep_name not in result:
                            result[trans_dep_name] = []
                        result[trans_dep_name].extend(trans_versions)
                    break
            except:
                continue

    return result


def check_version_conflicts(dependencies: dict) -> list:
    """Check for version conflicts in dependencies."""
    conflicts = []

    for dep_name, versions in dependencies.items():
        if len(versions) > 1:
            # Multiple versions required - check for conflicts
            version_strs = [v['version'] for v in versions]
            sources = [v['source'] for v in versions]

            if len(set(version_strs)) > 1:
                conflicts.append({
                    'dependency': dep_name,
                    'conflicting_versions': version_strs,
                    'sources': sources
                })

    return conflicts


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_conflicts.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]

    print_info(f"Checking dependency conflicts for: {skill_path}\n")

    # Collect all dependencies (direct and transitive)
    all_dependencies = collect_all_dependencies(skill_path)

    # Check for conflicts
    conflicts = check_version_conflicts(all_dependencies)

    print(f"{'='*60}")
    print("DEPENDENCY CONFLICT CHECK")
    print(f"{'='*60}\n")

    if conflicts:
        print_warning(f"Found {len(conflicts)} conflict(s):\n")

        for conflict in conflicts:
            print_error(f"❌ Dependency: {conflict['dependency']}")
            print_info(f"   Conflicting versions:")
            for i, (version, source) in enumerate(zip(conflict['conflicting_versions'], conflict['sources'])):
                print(f"     {i+1}. {version} (from {Path(source).name})")
            print()

        print_warning("These conflicts may cause unexpected behavior.")
        print("Consider updating dependencies to use compatible versions.")
        return 1
    else:
        print_success("No dependency conflicts found! ✨")
        return 0


if __name__ == "__main__":
    main()
