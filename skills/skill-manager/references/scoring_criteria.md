# Quality Scoring Criteria

## Scoring Overview

The skill quality scoring system evaluates skills across three main categories:
- **Documentation** (60 points)
- **Structure** (25 points)
- **Code Quality** (25 points)

Total: 110 points

## Documentation (60 points)

### Has Name (10 points)
- Valid name present in YAML frontmatter
- Name length: 2-50 characters
- Name is descriptive and unique

### Has Description (10 points)
- Valid description present in YAML frontmatter
- Description length: 20-500 characters

### Description Quality (15 points)
- **Length**: Longer descriptions are preferred
  - 50-100 chars: 5 points
  - 100-150 chars: 8 points
  - 150+ chars: 15 points

- **Specificity**: Description includes use cases or triggers
  - Mentions "when user needs", "use when", "supports"
  - Specific use cases or examples

### Has Instructions (15 points)
- Body content exists after YAML frontmatter
- Content length: 50+ characters

### Instruction Quality (10 points)
- **Code Examples**: Includes code blocks (```python, etc.) - 3 points
- **Sections**: Clear organization with headings (#) - 3 points
  - 3+ sections: 3 points
  - 2 sections: 2 points
  - 1 section: 1 point
- **Lists**: Uses bullet or numbered lists - 2 points
- **Length**: Body content length - 2 points
  - 500+ chars: 2 points
  - 200+ chars: 1 point

## Structure (25 points)

### Has Scripts (5 points)
- `scripts/` directory exists
- Contains at least one executable file (.py, .sh, etc.)

### Has References (5 points)
- `references/` directory exists
- Contains at least one .md file

### Has Assets (5 points)
- `assets/` directory exists
- Contains at least one file

### Proper Structure (10 points)
- Follows standard skill directory layout:
  ```
  skill-name/
  ├── SKILL.md (required)
  ├── scripts/ (optional)
  ├── references/ (optional)
  └── assets/ (optional)
  ```

## Code Quality (25 points)

### Scripts Executable (5 points)
- All scripts in `scripts/` have executable permissions
- Scripts can be run directly

### No Hardcoded Paths (10 points)
- No hardcoded paths like `/root/clawd`, `/home/`, etc.
- Paths should be relative or configurable

### No Sensitive Info (10 points)
- No API keys, passwords, tokens, secrets
- No hardcoded credentials
- Uses environment variables or config files

## Grade Calculation

| Score Range | Grade |
|-------------|-------|
| 90-110      | A+    |
| 85-89       | A     |
| 80-84       | B+    |
| 70-79       | B     |
| 60-69       | C+    |
| 50-59       | C     |
| 0-49        | F     |

**Passing Grade**: B (70 points) or higher

## Improving Your Score

### Documentation
- Add a clear, descriptive name
- Write a detailed description (150+ chars)
- Include specific use cases in description
- Add code examples in the body
- Organize with clear sections and lists
- Provide step-by-step instructions

### Structure
- Add scripts if the skill needs automation
- Create references for detailed documentation
- Include assets (templates, icons, etc.)

### Code Quality
- Make scripts executable (`chmod +x script.sh`)
- Avoid hardcoded paths - use relative paths
- Use environment variables for credentials
- Never commit API keys or secrets

## Common Issues and Fixes

### Issue: "Missing name or description"
**Fix**: Add `name` and `description` fields to YAML frontmatter

```yaml
---
name: my-skill
description: A clear description of what this skill does and when to use it.
---
```

### Issue: "Description lacks specificity"
**Fix**: Add use cases or triggers to description

```yaml
---
description: Process documents using OCR. Use when you need to extract text from PDFs or images.
---
```

### Issue: "Hardcoded paths"
**Fix**: Use relative paths or environment variables

```python
# Bad
path = "/root/clawd/data/file.txt"

# Good
import os
path = os.path.join(os.path.dirname(__file__), "../data/file.txt")

# Or
import os
path = os.getenv("MY_SKILL_DATA_PATH", "./data/file.txt")
```

### Issue: "Scripts not executable"
**Fix**: Make scripts executable

```bash
chmod +x scripts/*.py
chmod +x scripts/*.sh
```

### Issue: "Sensitive info detected"
**Fix**: Move credentials to environment variables

```python
# Bad
api_key = "sk-1234567890abcdef"

# Good
import os
api_key = os.getenv("MY_API_KEY")
if not api_key:
    raise ValueError("MY_API_KEY environment variable not set")
```
