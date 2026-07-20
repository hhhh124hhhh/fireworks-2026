#!/usr/bin/env python3
"""Pre-flight checks before publishing a skill to ClawdHub."""

import sys
import os
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import print_success, print_error, print_warning, print_info


def run_check(check_name: str, script_path: str, skill_path: str) -> bool:
    """Run a single check script."""
    print(f"\n🔍 Running {check_name}...")
    result = os.system(f"python3 {script_path} {skill_path} > /tmp/check_{check_name}.txt 2>&1")
    if result == 0:
        print_success(f"{check_name}: PASSED")
        return True
    else:
        print_error(f"{check_name}: FAILED")
        # Show error output
        try:
            with open(f"/tmp/check_{check_name}.txt", 'r') as f:
                error_output = f.read()
                if error_output:
                    print(f"   {error_output}")
        except:
            pass
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 preflight.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]

    print_info(f"Running pre-flight checks for: {skill_path}")
    print("="*60)

    # Track results
    results = {}

    # Run checks
    results['duplicate_check'] = run_check(
        "duplicate_check",
        "/root/clawd/skills/skill-manager/scripts/check_duplicates.py",
        skill_path
    )

    results['quality_check'] = run_check(
        "quality_check",
        "/root/clawd/skills/skill-manager/scripts/score_quality.py",
        skill_path
    )

    # Dependency validation (optional - only if dependencies exist)
    skill_dir = Path(skill_path)
    deps_file = skill_dir / "dependencies.json"
    if deps_file.exists():
        results['dependency_validation'] = run_check(
            "dependency_validation",
            "/root/clawd/skills/skill-manager/scripts/validate_dependencies.py",
            skill_path
        )
    else:
        print_info("\nℹ️  No dependencies to validate")

    # Conflict check (optional)
    results['conflict_check'] = run_check(
        "conflict_check",
        "/root/clawd/skills/skill-manager/scripts/check_conflicts.py",
        skill_path
    )

    # Summary
    print("\n" + "="*60)
    print("PRE-FLIGHT CHECK SUMMARY")
    print("="*60 + "\n")

    all_passed = True
    for check_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {check_name:30s}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "="*60 + "\n")

    if all_passed:
        print_success("All pre-flight checks passed! ✨")
        print_info("You can now publish the skill to ClawdHub.")
        return 0
    else:
        print_error("Some pre-flight checks failed.")
        print_warning("Please fix the issues above before publishing.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
