#!/usr/bin/env python3
"""Check for duplicate skills based on name, description, and content similarity."""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    load_skill_metadata,
    load_skill_content,
    calculate_similarity,
    normalize_text,
    get_all_skills,
    print_success,
    print_error,
    print_warning,
    print_info
)


# Similarity thresholds
NAME_SIMILARITY_THRESHOLD = 0.85
DESCRIPTION_SIMILARITY_THRESHOLD = 0.80
CONTENT_SIMILARITY_THRESHOLD = 0.75


def check_name_duplicates(skill_path: str, all_skills: list, threshold: float = NAME_SIMILARITY_THRESHOLD) -> list:
    """Check for skill name duplicates."""
    try:
        metadata = load_skill_metadata(skill_path)
        skill_name = metadata.get('name', '').lower()
    except Exception as e:
        print_error(f"Failed to load skill metadata: {e}")
        return []

    duplicates = []

    for other_skill in all_skills:
        if str(other_skill) == str(skill_path):
            continue

        try:
            other_metadata = load_skill_metadata(str(other_skill))
            other_name = other_metadata.get('name', '').lower()

            if skill_name == other_name:
                duplicates.append({
                    'type': 'exact_name_match',
                    'skill': str(other_skill),
                    'name': other_name,
                    'similarity': 1.0
                })
            else:
                similarity = calculate_similarity(skill_name, other_name)
                if similarity >= threshold:
                    duplicates.append({
                        'type': 'similar_name',
                        'skill': str(other_skill),
                        'name': other_name,
                        'similarity': similarity
                    })
        except Exception:
            continue

    return duplicates


def check_description_duplicates(skill_path: str, all_skills: list, threshold: float = DESCRIPTION_SIMILARITY_THRESHOLD) -> list:
    """Check for skill description duplicates."""
    try:
        metadata = load_skill_metadata(skill_path)
        skill_desc = normalize_text(metadata.get('description', ''))
    except Exception as e:
        print_error(f"Failed to load skill metadata: {e}")
        return []

    if not skill_desc:
        return []

    duplicates = []

    for other_skill in all_skills:
        if str(other_skill) == str(skill_path):
            continue

        try:
            other_metadata = load_skill_metadata(str(other_skill))
            other_desc = normalize_text(other_metadata.get('description', ''))

            if other_desc:
                similarity = calculate_similarity(skill_desc, other_desc)
                if similarity >= threshold:
                    duplicates.append({
                        'type': 'similar_description',
                        'skill': str(other_skill),
                        'description': other_desc[:100] + "...",
                        'similarity': similarity
                    })
        except Exception:
            continue

    return duplicates


def check_content_duplicates(skill_path: str, all_skills: list, threshold: float = CONTENT_SIMILARITY_THRESHOLD) -> list:
    """Check for skill content duplicates."""
    try:
        skill_content = load_skill_content(skill_path)
        skill_content = normalize_text(skill_content)
    except Exception as e:
        print_error(f"Failed to load skill content: {e}")
        return []

    if not skill_content:
        return []

    duplicates = []

    for other_skill in all_skills:
        if str(other_skill) == str(skill_path):
            continue

        try:
            other_content = load_skill_content(str(other_skill))
            other_content = normalize_text(other_content)

            if other_content:
                similarity = calculate_similarity(skill_content, other_content)
                if similarity >= threshold:
                    duplicates.append({
                        'type': 'similar_content',
                        'skill': str(other_skill),
                        'similarity': similarity
                    })
        except Exception:
            continue

    return duplicates


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 check_duplicates.py <skill-path>")
        sys.exit(1)

    skill_path = sys.argv[1]
    all_skills = get_all_skills()

    print_info(f"Checking for duplicates in: {skill_path}")
    print_info(f"Comparing against {len(all_skills)} skills\n")

    # Check name duplicates
    print("📋 Checking name duplicates...")
    name_dups = check_name_duplicates(skill_path, all_skills)

    # Check description duplicates
    print("📝 Checking description duplicates...")
    desc_dups = check_description_duplicates(skill_path, all_skills)

    # Check content duplicates
    print("📄 Checking content duplicates...")
    content_dups = check_content_duplicates(skill_path, all_skills)

    print(f"\n{'='*60}")
    print("DUPLICATE CHECK RESULTS")
    print(f"{'='*60}\n")

    total_issues = 0

    if name_dups:
        total_issues += len(name_dups)
        print_warning(f"Found {len(name_dups)} potential name duplicate(s):\n")
        for dup in name_dups:
            print(f"  • {dup['skill']}")
            print(f"    Name: {dup['name']}")
            print(f"    Similarity: {dup['similarity']:.2%}\n")

    if desc_dups:
        total_issues += len(desc_dups)
        print_warning(f"Found {len(desc_dups)} potential description duplicate(s):\n")
        for dup in desc_dups:
            print(f"  • {dup['skill']}")
            print(f"    Description: {dup['description']}")
            print(f"    Similarity: {dup['similarity']:.2%}\n")

    if content_dups:
        total_issues += len(content_dups)
        print_warning(f"Found {len(content_dups)} potential content duplicate(s):\n")
        for dup in content_dups:
            print(f"  • {dup['skill']}")
            print(f"    Similarity: {dup['similarity']:.2%}\n")

    if total_issues == 0:
        print_success("No duplicates found! ✨")
        return 0
    else:
        print_warning(f"\n⚠️  Found {total_issues} potential duplicate(s) total.")
        print("Please review and consider renaming, updating description, or merging skills.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
