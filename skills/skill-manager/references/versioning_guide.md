# Semantic Versioning Guide for Skills

## Overview

Semantic Versioning (SemVer) is a version numbering system that conveys meaning about the underlying changes in a skill. This guide explains how to properly version your skills.

## Version Format

Semantic Versioning follows the format: `MAJOR.MINOR.PATCH`

Example: `1.2.3`

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

## Version Numbering Rules

### MAJOR Version (X.0.0)

Increment the MAJOR version when you make incompatible changes to the skill's interface or behavior.

**Examples:**
- Removing or renaming commands
- Changing command-line interface
- Changing output format in a breaking way
- Modifying how the skill should be used

**Example:**
```
1.5.0 → 2.0.0
```

### MINOR Version (0.X.0)

Increment the MINOR version when you add functionality in a backwards-compatible manner.

**Examples:**
- Adding new commands or features
- Adding optional parameters to existing commands
- Adding new output formats
- Adding new capabilities that don't break existing usage

**Example:**
```
1.2.3 → 1.3.0
```

### PATCH Version (0.0.X)

Increment the PATCH version when you make backwards-compatible bug fixes.

**Examples:**
- Fixing bugs that don't change behavior
- Updating documentation
- Adding error messages
- Minor performance improvements

**Example:**
```
1.2.3 → 1.2.4
```

## Examples

### Bug Fix (PATCH)
```
Before: 1.2.3
After:  1.2.4
```

**Change**: Fixed issue where script fails on certain input.

### New Feature (MINOR)
```
Before: 1.2.3
After:  1.3.0
```

**Change**: Added new `--verbose` flag to output more details.

### Breaking Change (MAJOR)
```
Before: 1.2.3
After:  2.0.0
```

**Change**: Renamed `process` command to `analyze`.

## Pre-release Versions

Pre-release versions allow you to test changes before a stable release.

Format: `MAJOR.MINOR.PATCH-PRERELEASE`

Examples:
- `1.2.3-alpha`
- `1.2.3-beta.1`
- `1.2.3-rc.1`

### Pre-release Labels

- **alpha**: Early development, may have bugs
- **beta**: Feature complete, testing needed
- **rc** (Release Candidate): Ready for production, final testing

### Pre-release Ordering

Pre-release versions have lower precedence than the normal version:
```
1.2.3-alpha < 1.2.3-beta < 1.2.3-rc.1 < 1.2.3
```

## Build Metadata

You can append build metadata for internal tracking:

Format: `MAJOR.MINOR.PATCH+BUILD`

Example: `1.2.3+20260201`

Build metadata doesn't affect precedence:
```
1.2.3+20260201 == 1.2.3+20260202
```

## Version Files

Your skill should track version in two places:

### 1. SKILL.md Frontmatter

```yaml
---
name: my-skill
description: A helpful skill
version: 1.2.3
---
```

### 2. VERSION File (Optional)

Create a `VERSION` file in skill root:

```
1.2.3
```

### 3. version.json (Optional)

```json
{
  "version": "1.2.3",
  "changelog": [
    {
      "version": "1.2.3",
      "date": "2026-02-01",
      "changes": ["Fixed bug in script"]
    }
  ]
}
```

## Version Management Scripts

skill-manager provides scripts for version management:

### Initialize Version Tracking

```bash
python3 /root/clawd/skills/skill-manager/scripts/init_version.py /path/to/skill
```

This creates a `version.json` file.

### Bump Version

```bash
# Patch version (bug fix)
python3 /root/clawd/skills/skill-manager/scripts/bump_version.py /path/to/skill --type patch

# Minor version (new feature)
python3 /root/clawd/skills/skill-manager/scripts/bump_version.py /path/to/skill --type minor

# Major version (breaking change)
python3 /root/clawd/skills/skill-manager/scripts/bump_version.py /path/to/skill --type major
```

### View Version History

```bash
python3 /root/clawd/skills/skill-manager/scripts/version_history.py /path/to/skill
```

## Changelog Best Practices

### Format

Maintain a `CHANGELOG.md` file:

```markdown
# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.3] - 2026-02-01

### Added
- New `--verbose` flag
- Support for JSON output

### Fixed
- Fixed bug with file path handling

### Changed
- Improved error messages
- Updated documentation

## [1.2.0] - 2026-01-15

### Added
- New feature X
- New feature Y

## [1.0.0] - 2026-01-01

### Added
- Initial release
```

### Keep a Release Section for Each Version

Don't modify older changelog entries. Add new sections at the top.

### Categorize Changes

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Features that will be removed in future
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

## When to Version

### Always Version When Publishing

Each time you publish to ClawdHub, you should bump the version:
- If changes break compatibility: MAJOR
- If new features added: MINOR
- If only bug fixes: PATCH

### For Development Work

You can use pre-release versions during development:
- `1.2.3-alpha` for early testing
- `1.2.3-beta` for feature-complete testing
- `1.2.3-rc.1` for release candidate

### Hotfixes

If you discover a critical bug in a published version:
1. Create a branch from the previous version
2. Fix the bug
3. Bump PATCH version
4. Publish as hotfix

Example: `1.2.3` → `1.2.4`

## Version Compatibility

### Backwards Compatibility

Maintain backwards compatibility for MINOR and PATCH versions:
- Don't remove commands
- Don't change command-line interfaces
- Don't remove required parameters

### Deprecation Process

For MAJOR changes, follow deprecation process:

1. **Announce** in documentation
2. **Warn users** when using deprecated feature
3. **Provide migration guide**
4. **Remove in next MAJOR version**

Example:
```markdown
**Deprecated**: The `process` command will be removed in version 2.0.0. Use `analyze` instead.
```

## Dependency Versioning

When specifying skill dependencies, use version ranges:

### Exact Version
```json
{
  "dependencies": {
    "other-skill": "1.2.3"
  }
}
```

### Minimum Version
```json
{
  "dependencies": {
    "other-skill": ">=1.2.3"
  }
}
```

### Range
```json
{
  "dependencies": {
    "other-skill": ">=1.2.3 <2.0.0"
  }
}
```

### Caret Range (^)
```json
{
  "dependencies": {
    "other-skill": "^1.2.3"
  }
}
```

This allows updates >=1.2.3 but <2.0.0

### Tilde Range (~)
```json
{
  "dependencies": {
    "other-skill": "~1.2.3"
  }
}
```

This allows updates >=1.2.3 but <1.3.0

## Common Mistakes

### Mistake 1: Not Versioning Before Publishing

**Bad**: Publish version 1.0.0, make changes, publish again as 1.0.0

**Good**: Bump version to 1.0.1 before republishing

### Mistake 2: Overusing MAJOR Versions

**Bad**: Bumping to 2.0.0 for a minor feature

**Good**: Use MINOR version for backwards-compatible additions

### Mistake 3: Not Documenting Breaking Changes

**Bad**: Removing a command without warning in changelog

**Good**: Document deprecation in previous release, then remove in MAJOR

### Mistake 4: Inconsistent Versioning

**Bad**: SKILL.md says 1.2.3 but version.json says 1.2.4

**Good**: Keep version in sync across all files (use bump_version.py script)

## Quick Reference

| Change Type | Version Bump |
|-------------|--------------|
| Bug fix | PATCH |
| New feature | MINOR |
| Breaking change | MAJOR |
| Documentation update | PATCH |
| Performance improvement | PATCH or MINOR |
| Refactoring | PATCH |

## Resources

- Official SemVer specification: https://semver.org
- skill-manager scripts: `/root/clawd/skills/skill-manager/scripts/`
- Version control: Use Git tags for releases: `git tag v1.2.3`
