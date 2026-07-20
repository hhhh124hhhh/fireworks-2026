#!/usr/bin/env python3
"""Complete release workflow: preflight checks + package + publish."""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import print_success, print_error, print_warning, print_info


def run_preflight(skill_path: str) -> bool:
    """Run pre-flight checks."""
    print(f"\n{'='*60}")
    print("STEP 1: PRE-FLIGHT CHECKS")
    print(f"{'='*60}\n")

    preflight_script = "/root/clawd/skills/skill-manager/scripts/preflight.py"
    result = os.system(f"python3 {preflight_script} {skill_path}")
    return result == 0


def run_package(skill_path: str, output_dir: str = None) -> bool:
    """Package skill."""
    print(f"\n{'='*60}")
    print("STEP 2: PACKAGE SKILL")
    print(f"{'='*60}\n")

    publish_script = "/root/clawd/skills/skill-manager/scripts/publish.py"

    if output_dir:
        cmd = f"python3 {publish_script} {skill_path} --output {output_dir}"
    else:
        cmd = f"python3 {publish_script} {skill_path}"

    # Publish will handle packaging
    result = os.system(cmd)
    return result == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 release.py <skill-path> [--output <dir>]")
        print("\nOptions:")
        print("  --output <dir>  Output directory for .skill file (default: ../dist)")
        print("\nWorkflow:")
        print("  1. Run pre-flight checks (duplication, quality, dependencies)")
        print("  2. Package skill into .skill file")
        print("  3. Publish to ClawdHub")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = None

    if len(sys.argv) >= 4 and sys.argv[2] == '--output':
        output_dir = sys.argv[3]

    print_info(f"Starting release workflow for: {skill_path}")
    print("="*60)

    # Step 1: Pre-flight checks
    if not run_preflight(skill_path):
        print("\n" + "="*60)
        print_error("Release failed: Pre-flight checks did not pass")
        print_warning("Please fix the issues above and try again")
        print("="*60 + "\n")
        sys.exit(1)

    # Step 2: Package and publish
    print_info("\nPre-flight checks passed! Proceeding to packaging and publishing...")
    print_info("Note: This will publish to ClawdHub. Make sure you're ready.\n")

    response = input("Continue with packaging and publishing? [y/N]: ")
    if response.lower() not in ['y', 'yes']:
        print_warning("Release cancelled by user")
        sys.exit(1)

    if not run_package(skill_path, output_dir):
        print("\n" + "="*60)
        print_error("Release failed: Packaging or publishing error")
        print("="*60 + "\n")
        sys.exit(1)

    # Success
    print("\n" + "="*60)
    print_success("🎉 Release completed successfully!")
    print_info(f"Skill: {skill_path}")
    print("="*60 + "\n")


if __name__ == "__main__":
    sys.exit(main())
