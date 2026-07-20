#!/bin/bash
# Smart Skill Publisher v2 - Full Automation with Claude Review
# Usage: ./smart-publish-v2.sh ./skill-path --slug my-skill --name "My Skill" --version 1.0.0

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Config
CLAUDE_MODEL=${CLAUDE_MODEL:-"claude"}
REVIEW_TIMEOUT=300
MAX_RETRIES=3

# Parse arguments
SKILL_PATH=""
SLUG=""
NAME=""
VERSION=""
CHANGELOG=""
AUTO_PUBLISH=false
FORCE_PUBLISH=false

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
    --auto)
      AUTO_PUBLISH=true
      shift
      ;;
    --force)
      FORCE_PUBLISH=true
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
  echo "Usage: $0 ./skill-path --slug my-slug --name \"My Skill\" --version 1.0.0 [--auto] [--force]"
  exit 1
fi

SKILL_PATH=$(realpath "$SKILL_PATH")
SKILL_NAME=$(basename "$SKILL_PATH")

# Helper: Print banner
print_banner() {
  local title="$1"
  echo -e "${BLUE}═══════════════════════════════════════${NC}"
  echo -e "${BLUE}  $title${NC}"
  echo -e "${BLUE}═══════════════════════════════════════${NC}"
}

# Helper: Print step
print_step() {
  local step="$1"
  echo ""
  echo -e "${CYAN}▶ $step${NC}"
}

# Helper: Check command exists
command_exists() {
  command -v "$1" &> /dev/null
}

# Start
print_banner "🚀 Smart Skill Publisher v2"
echo ""
echo -e "📁 Skill:    ${GREEN}$SKILL_PATH${NC}"
echo -e "🏷️  Slug:     ${YELLOW}${SLUG:-auto}${NC}"
echo -e "📦 Name:     ${YELLOW}${NAME:-auto}${NC}"
echo -e "🔢 Version:  ${YELLOW}${VERSION:-auto}${NC}"
echo -e "🤖 Auto:     ${YELLOW}${AUTO_PUBLISH}${NC}"
echo ""

# Check if coding agent is available
if ! command_exists claude && ! command_exists codex; then
  echo -e "${RED}Error: Neither 'claude' nor 'codex' command found${NC}"
  echo "Please install a coding agent:"
  echo "  - Claude Code: npm install -g @anthropic-ai/claude-code"
  echo "  - Codex CLI: see documentation"
  exit 1
fi

# Check if skill directory has SKILL.md
if [[ ! -f "$SKILL_PATH/SKILL.md" ]]; then
  echo -e "${RED}Error: SKILL.md not found in skill directory${NC}"
  echo "A skill must have at least a SKILL.md file"
  exit 1
fi

# Check if clawdhub CLI is installed
if ! command_exists clawdhub; then
  echo -e "${YELLOW}Warning: clawdhub CLI not found${NC}"
  echo "Installing clawdhub CLI..."
  npm install -g clawdhub
  if [[ $? -ne 0 ]]; then
    echo -e "${RED}Failed to install clawdhub CLI${NC}"
    exit 1
  fi
fi

# Check if logged in
if ! clawdhub whoami &> /dev/null; then
  echo -e "${YELLOW}Not logged in to ClawdHub${NC}"
  echo "Please login first:"
  echo "  clawdhub login"
  exit 1
fi

# STEP 1: Quality Review
if [[ "$FORCE_PUBLISH" == false ]]; then
  print_step "STEP 1: Running Quality Review"
  echo -e "${YELLOW}Analyzing skill with Claude...${NC}"
  echo ""

  # Create temp directory for isolated review
  REVIEW_DIR=$(mktemp -d)
  cp -r "$SKILL_PATH"/* "$REVIEW_DIR/"

  # Create structured prompt
  cat > "$REVIEW_DIR/review_prompt.md" << 'EOF'
You are a Clawdbot Skill Quality Reviewer. Review this skill for publication.

## Review the following areas:

1. **SKILL.md Quality**
   - Clear name and description
   - Complete usage instructions
   - Working examples
   - Documented dependencies
   - Valid metadata section

2. **Code Quality** (if code exists)
   - Follows Clawdbot conventions
   - No hardcoded secrets
   - Proper error handling
   - Clean, readable

3. **Best Practices**
   - Correct tool usage patterns
   - No security issues
   - Proper documentation
   - No deprecated APIs

4. **Publish Readiness**
   - All required files present
   - Can be installed without errors
   - Works as documented

## CRITICAL: Output Format

You MUST output your review in this EXACT format at the end:

```
CLAWDBOT_REVIEW_START
{
  "overall_score": <number 1-10>,
  "critical_issues": <array of strings or empty>,
  "warnings": <array of strings or empty>,
  "suggestions": <array of strings or empty>,
  "recommendation": "APPROVE" or "REJECT",
  "summary": "<brief summary>"
}
CLAWDBOT_REVIEW_END
```

Example:
```
CLAWDBOT_REVIEW_START
{
  "overall_score": 9,
  "critical_issues": [],
  "warnings": ["Consider adding error handling examples"],
  "suggestions": ["Add more edge case examples"],
  "recommendation": "APPROVE",
  "summary": "Well-documented skill with clear instructions. Ready for publish."
}
CLAWDBOT_REVIEW_END
```

Review the skill now. End with the JSON block.
EOF

  # Run Claude in background to avoid TTY issues
  cd "$REVIEW_DIR"

  # Choose the right agent
  AGENT_CMD=""
  if command_exists claude; then
    AGENT_CMD="claude --print \"Review this skill following review_prompt.md. End with the JSON block.\""
  elif command_exists codex; then
    AGENT_CMD="codex exec \"Review this skill following review_prompt.md. End with the JSON block.\""
  fi

  # Run in background
  bash -c "$AGENT_CMD" > "$REVIEW_DIR/review_output.txt" 2>&1 &
  AGENT_PID=$!

  # Wait for completion
  ELAPSED=0
  while kill -0 $AGENT_PID 2>/dev/null; do
    sleep 5
    ELAPSED=$((ELAPSED + 5))
    echo -ne "\r${YELLOW}⏳ Reviewing... ${ELAPSED}s${NC}"

    if [[ $ELAPSED -ge $REVIEW_TIMEOUT ]]; then
      echo ""
      echo -e "${RED}Timeout: Review took too long${NC}"
      kill $AGENT_PID 2>/dev/null
      cd - > /dev/null
      rm -rf "$REVIEW_DIR"
      exit 1
    fi
  done

  echo ""

  # Extract JSON output
  if grep -q "CLAWDBOT_REVIEW_START" "$REVIEW_DIR/review_output.txt" 2>/dev/null; then
    REVIEW_JSON=$(sed -n '/CLAWDBOT_REVIEW_START/,/CLAWDBOT_REVIEW_END/p' "$REVIEW_DIR/review_output.txt" | sed '1d;$d')

    # Parse JSON (using jq if available, else simple grep)
    if command_exists jq; then
      SCORE=$(echo "$REVIEW_JSON" | jq -r '.overall_score // "N/A"')
      RECOMMENDATION=$(echo "$REVIEW_JSON" | jq -r '.recommendation // "UNKNOWN"')
      CRITICAL=$(echo "$REVIEW_JSON" | jq -r '.critical_issues[]?' 2>/dev/null || echo "None")
      SUMMARY=$(echo "$REVIEW_JSON" | jq -r '.summary // "No summary"')
    else
      SCORE=$(echo "$REVIEW_JSON" | grep -oP '"overall_score":\s*\K[0-9]+' || echo "N/A")
      RECOMMENDATION=$(echo "$REVIEW_JSON" | grep -oP '"recommendation":\s*"\K[^"]+' || echo "UNKNOWN")
      CRITICAL=$(echo "$REVIEW_JSON" | grep -oP '"critical_issues":\s*\[[^\]]*\]' | grep -oP '"[^"]+"' || echo "None")
      SUMMARY=$(echo "$REVIEW_JSON" | grep -oP '"summary":\s*"\K[^"]+' || echo "No summary")
    fi

    # Display review results
    echo ""
    echo -e "${BLUE}───────────────────────────────────────${NC}"
    echo -e "${BLUE}  📊 Review Results${NC}"
    echo -e "${BLUE}───────────────────────────────────────${NC}"
    echo ""
    echo -e "Score: ${CYAN}$SCORE/10${NC}"
    echo -e "Recommendation: ${CYAN}$RECOMMENDATION${NC}"
    echo -e ""
    echo -e "Critical Issues: ${YELLOW}${CRITICAL}${NC}"
    echo -e "Summary: ${CYAN}$SUMMARY${NC}"
    echo ""

    # Full output
    echo -e "${BLUE}Full Review:${NC}"
    cat "$REVIEW_DIR/review_output.txt"
    echo ""

    # Clean up
    cd - > /dev/null
    rm -rf "$REVIEW_DIR"

    # Check recommendation
    if [[ "$RECOMMENDATION" == "REJECT" ]]; then
      echo -e "${RED}❌ Review failed: Critical issues found${NC}"
      echo "Please fix the issues and try again, or use --force to override"
      exit 1
    fi

    if [[ ! "$AUTO_PUBLISH" == true ]]; then
      echo -e "${YELLOW}Review passed!${NC}"
      read -p "Proceed with publish? (y/N): " CONFIRM
      if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ Publish cancelled${NC}"
        exit 0
      fi
    fi

  else
    # Fallback: couldn't parse JSON, show full output and ask
    echo -e "${YELLOW}⚠️  Could not parse automated review${NC}"
    echo ""
    echo -e "${BLUE}Full review output:${NC}"
    cat "$REVIEW_DIR/review_output.txt"
    echo ""

    cd - > /dev/null
    rm -rf "$REVIEW_DIR"

    if [[ ! "$AUTO_PUBLISH" == true ]]; then
      read -p "Continue with publish anyway? (y/N): " CONFIRM
      if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ Publish cancelled${NC}"
        exit 0
      fi
    fi
  fi
else
  print_step "Skipping review (--force mode)"
fi

# STEP 2: Publish to ClawdHub
print_step "STEP 2: Publishing to ClawdHub"
echo ""

# Build publish command
PUBLISH_CMD="clawdhub publish \"$SKILL_PATH\""

[[ -n "$SLUG" ]] && PUBLISH_CMD="$PUBLISH_CMD --slug \"$SLUG\""
[[ -n "$NAME" ]] && PUBLISH_CMD="$PUBLISH_CMD --name \"$NAME\""
[[ -n "$VERSION" ]] && PUBLISH_CMD="$PUBLISH_CMD --version \"$VERSION\""
[[ -n "$CHANGELOG" ]] && PUBLISH_CMD="$PUBLISH_CMD --changelog \"$CHANGELOG\""

echo -e "${YELLOW}Command: $PUBLISH_CMD${NC}"
echo ""

# Execute publish
if eval "$PUBLISH_CMD"; then
  echo ""
  print_banner "✅ Publish Successful!"
  echo ""
  echo -e "${GREEN}Your skill is now live on ClawdHub!${NC}"
  echo ""
  exit 0
else
  echo ""
  echo -e "${RED}❌ Publish failed${NC}"
  exit 1
fi
