#!/bin/bash
# Smart Skill Publisher with Quality Check
# Usage: ./smart-publish.sh ./skill-path --slug my-skill --name "My Skill" --version 1.0.0

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
SKILL_PATH=""
SLUG=""
NAME=""
VERSION=""
CHANGELOG=""
SKIP_CHECK=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --slug)
      SLUG="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    --version)
      VERSION="$2"
      shift 2
      ;;
    --changelog)
      CHANGELOG="$2"
      shift 2
      ;;
    --skip-check)
      SKIP_CHECK=true
      shift
      ;;
    *)
      if [[ -z "$SKILL_PATH" ]]; then
        SKILL_PATH="$1"
      fi
      shift
      ;;
  esac
done

# Validation
if [[ -z "$SKILL_PATH" ]]; then
  echo -e "${RED}Error: Skill path required${NC}"
  echo "Usage: $0 ./skill-path --slug my-skill --name \"My Skill\" --version 1.0.0 [--changelog \"Changes\"] [--skip-check]"
  exit 1
fi

if [[ ! -d "$SKILL_PATH" ]]; then
  echo -e "${RED}Error: Skill path not found: $SKILL_PATH${NC}"
  exit 1
fi

SKILL_PATH=$(realpath "$SKILL_PATH")

echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${BLUE}  🚀 Smart Skill Publisher${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""
echo -e "📁 Skill: ${GREEN}$SKILL_PATH${NC}"
echo -e "🏷️  Slug: ${YELLOW}${SLUG:-auto}${NC}"
echo -e "📦 Version: ${YELLOW}${VERSION:-auto}${NC}"
echo ""

# Step 1: Quality Check with Claude
if [[ "$SKIP_CHECK" == false ]]; then
  echo -e "${BLUE}───────────────────────────────────────${NC}"
  echo -e "${BLUE}  🔍 STEP 1: Quality Check${NC}"
  echo -e "${BLUE}───────────────────────────────────────${NC}"
  echo ""

  # Create temp directory for the check
  CHECK_DIR=$(mktemp -d)

  # Copy skill files to check directory (isolate from workspace)
  cp -r "$SKILL_PATH"/* "$CHECK_DIR/"

  # Run Claude Code in background
  echo -e "${YELLOW}Running Claude Code quality check...${NC}"
  echo ""

  cat > "$CHECK_DIR/check_prompt.md" << 'EOF'
You are a Clawdbot Skill Quality Reviewer. Your task is to review this skill for publication quality.

## Review Checklist

### 1. SKILL.md Quality
- [ ] Has clear name and description
- [ ] Contains usage instructions
- [ ] Has examples (code blocks or commands)
- [ ] Documented dependencies (if any)
- [ ] Clear metadata section

### 2. Code Quality
- [ ] Follows Clawdbot skill conventions
- [ ] No hardcoded paths or secrets
- [ ] Error handling (where applicable)
- [ ] Clean, readable code

### 3. Best Practices
- [ ] Tool calls use correct patterns
- [ ] No security issues
- [ ] Proper documentation
- [ ] No deprecated APIs

### 4. Ready for Publishing
- [ ] All required files present (SKILL.md minimum)
- [ ] Metadata section valid
- [ ] Can be installed without errors
- [ ] Works as documented

## Output Format

Provide a structured review:

```markdown
# Skill Quality Review

## Overall Score: X/10

## Critical Issues (must fix before publish)
- None / [list]

## Warnings (should fix)
- None / [list]

## Suggestions (nice to have)
- None / [list]

## Recommendation
- ✅ APPROVE for publish
- ❌ REJECT - critical issues found

## Summary
[Brief summary]
```

Review the skill in this directory.
EOF

  # Run Claude Code in background
  cd "$CHECK_DIR"
  claude -p "Check the skill quality following the instructions in check_prompt.md. Be thorough but practical." &
  CLAUDE_PID=$!

  # Wait for completion with timeout (5 minutes)
  TIMEOUT=300
  ELAPSED=0

  while kill -0 $CLAUDE_PID 2>/dev/null; do
    sleep 5
    ELAPSED=$((ELAPSED + 5))
    if [[ $ELAPSED -ge $TIMEOUT ]]; then
      echo -e "${RED}Timeout: Quality check took too long${NC}"
      kill $CLAUDE_PID 2>/dev/null
      exit 1
    fi
  done

  # Capture output
  echo ""
  echo -e "${GREEN}✓ Quality check complete${NC}"
  echo ""

  # Clean up
  cd - > /dev/null
  rm -rf "$CHECK_DIR"

  # Note: In real implementation, we'd parse Claude's output here
  echo -e "${YELLOW}⚠️  Note: Quality check ran. In production, review will be parsed to auto-approve/reject.${NC}"
  echo ""
else
  echo -e "${YELLOW}⏭️  Skipping quality check (--skip-check flag)${NC}"
  echo ""
fi

# Step 2: User Confirmation
echo -e "${BLUE}───────────────────────────────────────${NC}"
echo -e "${BLUE}  ✋ STEP 2: Confirmation${NC}"
echo -e "${BLUE}───────────────────────────────────────${NC}"
echo ""

echo -e "Ready to publish:"
echo -e "  Path: ${GREEN}$SKILL_PATH${NC}"
echo -e "  Slug: ${YELLOW}${SLUG:-auto}${NC}"
echo -e "  Name: ${YELLOW}${NAME:-auto}${NC}"
echo -e "  Version: ${YELLOW}${VERSION:-auto}${NC}"
echo ""

read -p "Proceed with publish? (y/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
  echo -e "${RED}❌ Publish cancelled${NC}"
  exit 0
fi

echo ""

# Step 3: Publish to ClawdHub
echo -e "${BLUE}───────────────────────────────────────${NC}"
echo -e "${BLUE}  📤 STEP 3: Publishing to ClawdHub${NC}"
echo -e "${BLUE}───────────────────────────────────────${NC}"
echo ""

# Build publish command
PUBLISH_CMD="clawdhub publish \"$SKILL_PATH\""

if [[ -n "$SLUG" ]]; then
  PUBLISH_CMD="$PUBLISH_CMD --slug \"$SLUG\""
fi

if [[ -n "$NAME" ]]; then
  PUBLISH_CMD="$PUBLISH_CMD --name \"$NAME\""
fi

if [[ -n "$VERSION" ]]; then
  PUBLISH_CMD="$PUBLISH_CMD --version \"$VERSION\""
fi

if [[ -n "$CHANGELOG" ]]; then
  PUBLISH_CMD="$PUBLISH_CMD --changelog \"$CHANGELOG\""
fi

echo -e "${YELLOW}Running: $PUBLISH_CMD${NC}"
echo ""

# Execute publish command
if eval "$PUBLISH_CMD"; then
  echo ""
  echo -e "${GREEN}═══════════════════════════════════════${NC}"
  echo -e "${GREEN}  ✅ Publish successful!${NC}"
  echo -e "${GREEN}═══════════════════════════════════════${NC}"
  exit 0
else
  echo ""
  echo -e "${RED}❌ Publish failed${NC}"
  exit 1
fi
