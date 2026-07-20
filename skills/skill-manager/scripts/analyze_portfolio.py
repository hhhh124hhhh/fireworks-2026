#!/usr/bin/env python3
"""Analyze entire skill portfolio for quality, duplicates, and issues."""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    load_skill_metadata,
    print_success, print_error, print_warning, print_info
)


def analyze_portfolio(base_dir: str = "/root/clawd/skills") -> Dict[str, Any]:
    """Analyze all skills in the portfolio."""
    base = Path(base_dir)

    if not base.exists():
        print_error(f"Skills directory not found: {base_dir}")
        return None

    skills = list(base.iterdir())

    # Filter to only skill directories (has SKILL.md)
    skill_dirs = [s for s in skills if s.is_dir() and (s / "SKILL.md").exists()]

    print_info(f"Found {len(skill_dirs)} skills\n")

    results = {
        'total_skills': len(skill_dirs),
        'skills': [],
        'issues': defaultdict(list),
        'statistics': {}
    }

    # Analyze each skill
    for skill_dir in sorted(skill_dirs):
        skill_name = skill_dir.name
        print(f"Analyzing: {skill_name}")

        skill_info = {
            'name': skill_name,
            'path': str(skill_dir),
            'metadata': None,
            'has_name': False,
            'has_description': False,
            'has_scripts': False,
            'has_references': False,
            'has_assets': False,
            'issues': []
        }

        try:
            # Load metadata
            metadata = load_skill_metadata(str(skill_dir))
            skill_info['metadata'] = metadata

            # Check name
            if 'name' in metadata and metadata['name']:
                skill_info['has_name'] = True
            else:
                skill_info['issues'].append('Missing name')
                results['issues']['missing_name'].append(skill_name)

            # Check description
            if 'description' in metadata and metadata['description']:
                skill_info['has_description'] = True
            else:
                skill_info['issues'].append('Missing description')
                results['issues']['missing_description'].append(skill_name)

            # Check structure
            if (skill_dir / "scripts").exists():
                skill_info['has_scripts'] = True
            if (skill_dir / "references").exists():
                skill_info['has_references'] = True
            if (skill_dir / "assets").exists():
                skill_info['has_assets'] = True

        except Exception as e:
            skill_info['issues'].append(f'Error loading: {e}')
            results['issues']['load_errors'].append(skill_name)

        results['skills'].append(skill_info)

    # Calculate statistics
    with_name = sum(1 for s in results['skills'] if s['has_name'])
    with_description = sum(1 for s in results['skills'] if s['has_description'])
    with_scripts = sum(1 for s in results['skills'] if s['has_scripts'])
    with_references = sum(1 for s in results['skills'] if s['has_references'])
    with_assets = sum(1 for s in results['skills'] if s['has_assets'])

    results['statistics'] = {
        'with_name': with_name,
        'with_description': with_description,
        'with_scripts': with_scripts,
        'with_references': with_references,
        'with_assets': with_assets,
        'missing_name': len(results['issues']['missing_name']),
        'missing_description': len(results['issues']['missing_description']),
        'load_errors': len(results['issues']['load_errors']),
    }

    return results


def print_summary(results: Dict[str, Any]):
    """Print analysis summary."""
    print("\n" + "="*60)
    print("PORTFOLIO ANALYSIS SUMMARY")
    print("="*60 + "\n")

    stats = results['statistics']

    print("📊 Statistics")
    print("-" * 40)
    print(f"  Total skills: {results['total_skills']}")
    print(f"  With name: {stats['with_name']} ({stats['with_name']/results['total_skills']*100:.1f}%)")
    print(f"  With description: {stats['with_description']} ({stats['with_description']/results['total_skills']*100:.1f}%)")
    print(f"  With scripts: {stats['with_scripts']} ({stats['with_scripts']/results['total_skills']*100:.1f}%)")
    print(f"  With references: {stats['with_references']} ({stats['with_references']/results['total_skills']*100:.1f}%)")
    print(f"  With assets: {stats['with_assets']} ({stats['with_assets']/results['total_skills']*100:.1f}%)")

    print("\n⚠️  Issues")
    print("-" * 40)
    if stats['missing_name'] > 0:
        print(f"  Missing name: {stats['missing_name']}")
    if stats['missing_description'] > 0:
        print(f"  Missing description: {stats['missing_description']}")
    if stats['load_errors'] > 0:
        print(f"  Load errors: {stats['load_errors']}")

    if all(v == 0 for v in [stats['missing_name'], stats['missing_description'], stats['load_errors']]):
        print("  None! ✨")

    print("\n" + "="*60 + "\n")


def print_issues_report(results: Dict[str, Any]):
    """Print detailed issues report."""
    if not any(results['issues'].values()):
        return

    print("="*60)
    print("DETAILED ISSUES REPORT")
    print("="*60 + "\n")

    for issue_type, skill_names in results['issues'].items():
        if skill_names:
            print(f"⚠️  {issue_type.upper()}")
            print(f"   ({len(skill_names)} skills)\n")

            for skill_name in sorted(skill_names):
                print(f"  • {skill_name}")

            print()

    print("="*60 + "\n")


def save_report(results: Dict[str, Any], output_file: str = None):
    """Save analysis report to JSON file."""
    if output_file is None:
        output_file = "/root/clawd/data/portfolio-analysis.json"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)

    print_info(f"Analysis report saved to: {output_file}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Analyze skill portfolio')
    parser.add_argument('--dir', default='/root/clawd/skills', help='Skills directory')
    parser.add_argument('--output', help='Output JSON file for report')
    parser.add_argument('--verbose', action='store_true', help='Show skill details')

    args = parser.parse_args()

    results = analyze_portfolio(args.dir)

    if results is None:
        sys.exit(1)

    print_summary(results)
    print_issues_report(results)

    if args.verbose:
        print("="*60)
        print("SKILL DETAILS")
        print("="*60 + "\n")

        for skill in results['skills']:
            print(f"📁 {skill['name']}")
            print(f"   Path: {skill['path']}")
            print(f"   Has name: {skill['has_name']}")
            print(f"   Has description: {skill['has_description']}")
            print(f"   Has scripts: {skill['has_scripts']}")
            print(f"   Has references: {skill['has_references']}")
            print(f"   Has assets: {skill['has_assets']}")

            if skill['issues']:
                print(f"   Issues: {', '.join(skill['issues'])}")

            print()

    if args.output:
        save_report(results, args.output)

    # Exit code based on whether there are critical issues
    critical_issues = results['statistics']['missing_name'] + results['statistics']['load_errors']
    if critical_issues > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
