# ClawdHub API Reference

## Overview

ClawdHub is the official registry for Clawdbot Skills. This document covers the ClawdHub CLI usage and API.

## Installation

```bash
npm install -g clawdhub
```

## Configuration

### Authentication

ClawdHub uses token-based authentication. Configure your token:

```bash
clawdhub login
```

This will prompt for your credentials and save the token to `~/.config/clawdhub/config.json`.

### Configuration File

Location: `~/.config/clawdhub/config.json`

```json
{
  "token": "clh_xxxxxxxxxxxxxxxxxxxx",
  "registry": "https://www.clawhub.ai/api"
}
```

## CLI Commands

### `clawdhub list`

List all available skills in the registry.

```bash
clawdhub list
```

**Options:**
- `--registry <url>`: Specify registry URL
- `--limit <n>`: Limit number of results
- `--search <term>`: Search skills by name

### `clawdhub search`

Search for skills by keyword.

```bash
clawdhub search "video generation"
```

**Options:**
- `--registry <url>`: Specify registry URL
- `--limit <n>`: Limit number of results

### `clawdhub info`

Get detailed information about a skill.

```bash
clawdhub info skill-name
```

**Output:**
- Skill name and description
- Version information
- Author/maintainer
- Download statistics

### `clawdhub install`

Install a skill from ClawdHub.

```bash
clawdhub install skill-name
```

**Options:**
- `--registry <url>`: Specify registry URL
- `--version <version>`: Install specific version
- `--global`: Install globally (default: local)

**Installation Location:**
- Local: `./skills/` (project directory)
- Global: `/root/clawd/skills/` (system directory)

### `clawdhub publish`

Publish a skill to ClawdHub.

```bash
clawdhub publish skill-file.skill
```

**Options:**
- `--registry <url>`: Specify registry URL
- `--token <token>`: Override token (not recommended)
- `--private`: Publish as private skill

**Prerequisites:**
- Skill must be packaged as `.skill` file (zip archive)
- Skill must have valid `name` and `description` in frontmatter
- Token must be valid and have publish permissions

### `clawdhub update`

Update an existing skill.

```bash
clawdhub update skill-name --version 1.1.0
```

**Options:**
- `--registry <url>`: Specify registry URL
- `--version <version>`: New version number
- `--file <path>`: Skill file to upload

### `clawdhub unpublish`

Remove a skill from ClawdHub.

```bash
clawdhub unpublish skill-name
```

**Options:**
- `--registry <url>`: Specify registry URL
- `--force`: Skip confirmation

**⚠️ Warning**: This operation is irreversible.

### `clawdhub whoami`

Check current authentication status.

```bash
clawdhub whoami
```

**Output:**
```json
{
  "username": "your-username",
  "email": "your-email@example.com",
  "permissions": ["read", "write", "publish"]
}
```

## Packaging Skills

Before publishing, skills must be packaged using the `package_skill.py` script:

```bash
python3 ~/.clawdbot/scripts/package_skill.py /path/to/skill
```

This creates a `.skill` file (zip archive) containing:
- SKILL.md
- scripts/
- references/
- assets/

## Registry URLs

| Environment | URL |
|-------------|-----|
| Production  | `https://www.clawhub.ai/api` |
| Development | (Contact Clawdbot team) |

**Note**: Always use the production URL for publishing skills.

## Best Practices

### 1. Always Pre-flight Before Publishing

```bash
# Run all checks
python3 /root/clawd/skills/skill-manager/scripts/preflight.py /path/to/skill

# Then package and publish
python3 /root/clawd/skills/skill-manager/scripts/release.py /path/to/skill
```

### 2. Use Semantic Versioning

- **Major** (1.0.0 → 2.0.0): Breaking changes
- **Minor** (1.0.0 → 1.1.0): New features, backward compatible
- **Patch** (1.0.0 → 1.0.1): Bug fixes, backward compatible

### 3. Verify Before Publishing

Always test your skill locally before publishing:
1. Install locally: `clawdhub install my-skill.skill`
2. Test functionality
3. Verify metadata
4. Check for hardcoded paths or sensitive info

### 4. Check Token Status

```bash
clawdhub whoami
```

Verify you have publish permissions before attempting to publish.

### 5. Use Correct Registry

Always specify the registry URL to avoid publishing to the wrong environment:

```bash
clawdhub publish my-skill.skill --registry https://www.clawhub.ai/api
```

## Troubleshooting

### Issue: "Unauthorized"

**Cause**: Invalid or expired token.

**Solution**:
```bash
# Re-authenticate
clawdhub login
# Check status
clawdhub whoami
```

### Issue: "Invalid Skill Format"

**Cause**: SKILL.md missing frontmatter or invalid structure.

**Solution**:
```bash
# Validate skill
python3 ~/.clawdbot/scripts/package_skill.py /path/to/skill

# Check for errors and fix before publishing
```

### Issue: "Skill Already Exists"

**Cause**: A skill with the same name already exists.

**Solution**:
- Rename your skill
- Use `clawdhub search` to find existing names
- Choose a unique, descriptive name

### Issue: "Publish Timeout"

**Cause**: Network issues or large skill file.

**Solution**:
- Check network connectivity
- Compress assets if possible
- Try again later

## API Endpoints (for Developers)

### GET /skills

List all skills.

**Response:**
```json
{
  "skills": [
    {
      "name": "skill-name",
      "description": "Skill description",
      "version": "1.0.0",
      "author": "username",
      "downloads": 100
    }
  ]
}
```

### GET /skills/:name

Get skill details.

### POST /skills

Publish new skill.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/zip
```

**Body**: Skill file (.skill)

### PUT /skills/:name

Update skill.

### DELETE /skills/:name

Unpublish skill.

## Rate Limits

| Operation | Limit |
|-----------|-------|
| List/Read | 100 requests/hour |
| Search    | 100 requests/hour |
| Publish   | 10 requests/hour |
| Update    | 10 requests/hour |

## Support

For issues or questions about ClawdHub:
- Documentation: https://docs.clawdbot.com
- Community: https://discord.gg/clawd
- GitHub: https://github.com/clawdbot/clawdbot
