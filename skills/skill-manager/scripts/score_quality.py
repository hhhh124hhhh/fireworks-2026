#!/usr/bin/env python3
"""Score skill quality based on documentation, code quality, testing, and best practices."""

import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import load_skill_metadata, print_success, print_error, print_warning, print_info


# Quality scoring criteria (100 points total)
SCORING = {
    'documentation': {
        'has_name': 10,
        'has_description': 10,
        'description_quality': 15,  # Length, specificity, clarity
        'has_instructions': 15,     # Body content
        'instruction_quality': 10   # Clear examples, steps
    },
    'structure': {
        'has_scripts': 5,
        'has_references': 5,
        'has_assets': 5,
        'proper_structure': 10      # Correct directory layout
    },
    'code_quality': {
        'scripts_executable': 5,
        'no_hardcoded_paths': 10,   # No /root/clawd, etc.
        'no_sensitive_info': 10     # No API keys, passwords
    }
}


def check_name(metadata: Dict) -> Tuple[int, str]:
    """Check if skill has a valid name."""
    name = metadata.get('name', '')
    if name and len(name) > 2 and len(name) < 50:
        return SCORING['documentation']['has_name'], "Valid name present"
    return 0, "Missing or invalid name (must be 2-50 chars)"


def check_description(metadata: Dict) -> Tuple[int, str]:
    """Check if skill has a valid description."""
    desc = metadata.get('description', '')
    if desc and len(desc) > 20 and len(desc) < 500:
        return SCORING['documentation']['has_description'], "Valid description present"
    return 0, "Missing or invalid description (must be 20-500 chars)"


def check_description_quality(metadata: Dict) -> Tuple[int, str]:
    """Check description quality based on length and specificity."""
    desc = metadata.get('description', '')
    score = 0
    issues = []

    # Check length
    if len(desc) < 50:
        issues.append("Description too short (< 50 chars)")
    elif len(desc) < 100:
        score += 5
        issues.append("Description could be more detailed")
    else:
        score += 8
        if len(desc) >= 150:
            score += 7  # Bonus for detailed description

    # Check for specificity (triggers/use cases)
    specificity_patterns = [
        r'when (user|Claude|you) need',
        r'use (when|if|to|for)',
        r'for (tasks?|queries?|requests?)',
        r'supports? \w+',
        r'(provides?|enables?|offers?)'
    ]
    if any(re.search(p, desc, re.IGNORECASE) for p in specificity_patterns):
        score += 2
    else:
        issues.append("Description lacks specificity/use cases")

    final_score = min(score, SCORING['documentation']['description_quality'])
    message = f"Score: {final_score}/{SCORING['documentation']['description_quality']}"
    if issues:
        message += f" - {', '.join(issues)}"

    return final_score, message


def check_instructions(skill_path: Path) -> Tuple[int, str]:
    """Check if skill has body instructions."""
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return 0, "SKILL.md not found"

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if content after frontmatter exists
    if '---' in content:
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            if len(body) > 50:
                return SCORING['documentation']['has_instructions'], "Body content present"
            return 0, "Body content too short or missing"
        else:
            return 0, "No body content after frontmatter"

    return 0, "Invalid SKILL.md format (no frontmatter)"


def check_instruction_quality(skill_path: Path) -> Tuple[int, str]:
    """Check instruction quality."""
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return 0, "SKILL.md not found"

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    score = 0
    issues = []

    # Extract body
    if '---' in content:
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2].strip()
        else:
            return 0, "No body content"
    else:
        return 0, "No frontmatter found"

    # Check for code examples
    if re.search(r'```[\w]*', body):
        score += 3
    else:
        issues.append("No code examples")

    # Check for sections
    sections = re.findall(r'^#+\s+\w+', body, re.MULTILINE)
    if len(sections) >= 3:
        score += 3
    elif len(sections) >= 2:
        score += 2
    elif len(sections) >= 1:
        score += 1
    else:
        issues.append("No clear sections")

    # Check for lists (steps, items)
    if re.search(r'^\s*[-*+]\s+', body, re.MULTILINE):
        score += 2
    else:
        issues.append("No lists (steps/items)")

    # Check length
    if len(body) >= 500:
        score += 2
    elif len(body) >= 200:
        score += 1

    final_score = min(score, SCORING['documentation']['instruction_quality'])
    message = f"Score: {final_score}/{SCORING['documentation']['instruction_quality']}"
    if issues:
        message += f" - {', '.join(issues)}"

    return final_score, message


def check_structure(skill_path: Path) -> Tuple[int, str]:
    """Check skill directory structure."""
    score = 0

    # Check for scripts
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        scripts = list(scripts_dir.glob("*.py"))
        if scripts:
            score += SCORING['structure']['has_scripts']
        else:
            score += 2  # Partial credit for empty scripts dir
    else:
        score += 3  # Partial credit (documentation-only skills)

    # Check for references
    refs_dir = skill_path / "references"
    if refs_dir.exists() and refs_dir.is_dir():
        refs = list(refs_dir.glob("*.md"))
        if refs:
            score += SCORING['structure']['has_references']
        else:
            score += 2  # Partial credit
    else:
        score += 3  # Partial credit

    # Check for assets
    assets_dir = skill_path / "assets"
    if assets_dir.exists() and assets_dir.is_dir():
        assets = list(assets_dir.iterdir())
        if assets:
            score += SCORING['structure']['has_assets']
        else:
            score += 2  # Partial credit
    else:
        score += 3  # Partial credit

    return score, f"Score: {score}/{sum(SCORING['structure'].values())}"


def check_code_quality(skill_path: Path) -> Tuple[int, str]:
    """Check for code quality issues."""
    score = SCORING['code_quality']['scripts_executable']  # Start with baseline
    issues = []

    # Check scripts for executable bit
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.py"):
            if script.is_file():
                # Check if executable
                if not os.access(script, os.X_OK):
                    issues.append(f"{script.name} not executable")

    # Check for hardcoded paths
    problematic_paths = ['/root/clawd', '/home/', '/tmp/']
    skill_files = list(skill_path.rglob("*.py")) + list(skill_path.rglob("*.sh")) + list(skill_path.rglob("*.md"))

    path_issues = []
    for file in skill_files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for path in problematic_paths:
                if path in content and path != '/tmp/':
                    path_issues.append(f"{file.name}: {path}")

    if path_issues:
        score = 0  # Fail if hardcoded paths found
        issues.append(f"Hardcoded paths: {', '.join(path_issues[:3])}")
    else:
        score += SCORING['code_quality']['no_hardcoded_paths']

    # Check for sensitive info (API keys, passwords, tokens)
    sensitive_patterns = [
        r'api[_-]?key\s*[=:]\s*["\'][\w-]+["\']',
        r'password\s*[=:]\s*["\'][\w-]+["\']',
        r'token\s*[=:]\s*["\'][\w-]+["\']',
        r'secret\s*[=:]\s*["\'][\w-]+["\']',
        r'SK_\w+\s*=\s*["\'][\w-]+["\']',
        r'Bearer\s+[\w-]+',
    ]

    sensitive_issues = []
    for file in skill_files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern in sensitive_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    sensitive_issues.append(f"{file.name}: potential sensitive info")

    if sensitive_issues:
        score = 0  # Fail if sensitive info found
        issues.append(f"Sensitive info: {', '.join(sensitive_issues[:3])}")
    else:
        score += SCORING['code_quality']['no_sensitive_info']

    final_score = min(score, sum(SCORING['code_quality'].values()))
    message = f"Score: {final_score}/{sum(SCORING['code_quality'].values())}"
    if issues:
        message += f" - {', '.join(issues)}"

    return final_score, message


def calculate_grade(score: int) -> str:
    """Calculate letter grade based on score."""
    if score >= 90:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 80:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C+"
    elif score >= 50:
        return "C"
    else:
        return "F"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 score_quality.py <skill-path>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print_error(f"Skill path not found: {skill_path}")
        sys.exit(1)

    print_info(f"Scoring skill quality: {skill_path}\n")

    try:
        metadata = load_skill_metadata(str(skill_path))
    except Exception as e:
        print_error(f"Failed to load skill metadata: {e}")
        sys.exit(1)

    # Run all checks
    results = {}

    results['name'] = check_name(metadata)
    results['description'] = check_description(metadata)
    results['description_quality'] = check_description_quality(metadata)
    results['instructions'] = check_instructions(skill_path)
    results['instruction_quality'] = check_instruction_quality(skill_path)
    results['structure'] = check_structure(skill_path)
    results['code_quality'] = check_code_quality(skill_path)

    # Calculate total score
    total_score = sum(score for score, _ in results.values())
    max_score = sum(SCORING[category][key] for category in SCORING for key in SCORING[category])
    percentage = (total_score / max_score) * 100
    grade = calculate_grade(total_score)

    # Print results
    print("="*60)
    print("QUALITY SCORE REPORT")
    print("="*60)
    print(f"\n📊 Total Score: {total_score}/{max_score} ({percentage:.1f}%)")
    print(f"🎯 Grade: {grade}\n")

    print("Documentation")
    print("-" * 40)
    for category in ['name', 'description', 'description_quality', 'instructions', 'instruction_quality']:
        score, msg = results[category]
        emoji = "✅" if score > 0 else "❌"
        print(f"  {emoji} {category}: {score} - {msg}")

    print("\nStructure")
    print("-" * 40)
    score, msg = results['structure']
    emoji = "✅" if score > 0 else "❌"
    print(f"  {emoji} structure: {score} - {msg}")

    print("\nCode Quality")
    print("-" * 40)
    score, msg = results['code_quality']
    emoji = "✅" if score > 0 else "❌"
    print(f"  {emoji} code_quality: {score} - {msg}")

    print(f"\n{'='*60}\n")

    # Return exit code
    if total_score >= 70:  # Passing grade: B or higher
        print_success(f"Skill passes quality check (Grade: {grade})")
        return 0
    else:
        print_warning(f"Skill needs improvement (Grade: {grade})")
        return 1


if __name__ == "__main__":
    sys.exit(main())
