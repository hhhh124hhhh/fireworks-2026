#!/bin/bash
# Install AI Prompts Skills from local directory

SKILLS_DIR="/root/clawd/dist/skills"

echo "========================================"
echo "AI Prompts Skills Installation Script"
echo "========================================"
echo ""

# Check if skills directory exists
if [ ! -d "$SKILLS_DIR" ]; then
    echo "❌ Error: Skills directory not found: $SKILLS_DIR"
    exit 1
fi

# Count .skill files
TOTAL=$(find "$SKILLS_DIR" -name "*.skill" -type f 2>/dev/null | wc -l)
echo "Found $TOTAL .skill files"
echo ""

# Option 1: Install via ClawdHub (recommended if published)
echo "Option 1: Install from ClawdHub (recommended)"
echo "----------------------------------------------"
echo "Run this to install all skills:"
echo "  cd $SKILLS_DIR"
echo "  for skill in *.skill; do"
echo "    slug=\${skill%.skill}"
echo "    echo \"Installing \$slug...\""
echo "    clawdhub install \$slug"
echo "  done"
echo ""

# Option 2: Install manually (extract to local skills directory)
echo "Option 2: Manual installation (extract locally)"
echo "------------------------------------------------"
echo "Run this to extract all skills to local skills directory:"
echo "  cd $SKILLS_DIR"
echo "  for skill in *.skill; do"
echo "    skill_name=\${skill%.skill}"
echo "    echo \"Extracting \$skill_name...\""
echo "    mkdir -p ~/.clawdbot/skills/\$skill_name"
echo "    unzip -q \$skill -d ~/.clawdbot/skills/\$skill_name"
echo "  done"
echo ""

# Option 3: List all skills
echo "Option 3: List all available skills"
echo "------------------------------------"
echo "Available skills:"
find "$SKILLS_DIR" -maxdepth 1 -name "*.skill" -type f -printf "%f\n" | sed 's/.skill$//' | nl
echo ""

echo "========================================"
echo "Installation Guide Complete"
echo "========================================"
