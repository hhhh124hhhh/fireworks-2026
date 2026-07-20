#!/usr/bin/env python3
"""Utility functions for skill-manager scripts."""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import difflib
import re


def load_skill_metadata(skill_path: str) -> Dict[str, Any]:
    """Load skill metadata from SKILL.md."""
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found at {skill_md}")

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse YAML frontmatter
    if content.startswith('---'):
        end_marker = content.find('\n---\n', 4)
        if end_marker != -1:
            frontmatter = content[4:end_marker]
            return yaml.safe_load(frontmatter)

    raise ValueError("Invalid SKILL.md: missing YAML frontmatter")


def load_skill_content(skill_path: str) -> str:
    """Load SKILL.md content only for performance."""
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return ""

    with open(skill_md, 'r', encoding='utf-8') as f:
        return f.read()


def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity ratio between two strings using difflib."""
    return difflib.SequenceMatcher(None, str1, str2).ratio()


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Convert to lowercase
    text = text.lower()
    return text.strip()


def get_all_skills(base_dir: str = "/root/clawd/skills") -> List[Path]:
    """Get all skill directories in the base directory."""
    base = Path(base_dir)
    skills = []

    for item in base.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item)

    return skills


def print_status(message: str, emoji: str = ""):
    """Print status message with emoji."""
    print(f"{emoji} {message}")


def print_success(message: str):
    """Print success message."""
    print_status(message, "✅")


def print_error(message: str):
    """Print error message."""
    print_status(message, "❌")


def print_warning(message: str):
    """Print warning message."""
    print_status(message, "⚠️")


def print_info(message: str):
    """Print info message."""
    print_status(message, "ℹ️")


def ensure_dir(path: str):
    """Ensure directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)
