#!/bin/bash
#
# Setup Twitter Scan Cron Job
# WeChat Cover Generator Skill
#
# This script sets up an automated cron job to scan Twitter for AI prompts
# every 6 hours (at 00:00, 06:00, 12:00, 18:00 UTC)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCAN_SCRIPT="$SCRIPT_DIR/scan_twitter_prompts.py"
CRON_SCHEDULE="0 */6 * * *"  # Every 6 hours

echo "=================================="
echo "Twitter Scan Cron Job Setup"
echo "WeChat Cover Generator Skill"
echo "=================================="
echo ""

# Check if scan script exists
if [ ! -f "$SCAN_SCRIPT" ]; then
    echo -e "${RED}Error: Scan script not found at $SCAN_SCRIPT${NC}"
    exit 1
fi

# Make scan script executable
chmod +x "$SCAN_SCRIPT"
echo -e "${GREEN}✓ Made scan script executable${NC}"

# Create log directory
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"
echo -e "${GREEN}✓ Created log directory: $LOG_DIR${NC}"

# Create cron job command
CRON_COMMAND="$CRON_SCHEDULE $SCAN_SCRIPT >> $LOG_DIR/cron.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$SCAN_SCRIPT"; then
    echo -e "${YELLOW}! Cron job already exists${NC}"
    echo "Current cron job:"
    crontab -l 2>/dev/null | grep "$SCAN_SCRIPT"
    echo ""
    read -p "Do you want to replace it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled. Keeping existing cron job."
        exit 0
    fi

    # Remove existing cron job
    crontab -l 2>/dev/null | grep -v "$SCAN_SCRIPT" | crontab -
    echo -e "${GREEN}✓ Removed existing cron job${NC}"
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_COMMAND") | crontab -
echo -e "${GREEN}✓ Added new cron job${NC}"

# Show the cron job
echo ""
echo "Active cron jobs for this skill:"
echo "--------------------------------"
crontab -l 2>/dev/null | grep "$SCAN_SCRIPT"
echo "--------------------------------"
echo ""

# Verify cron service is running
if ! pgrep -x "cron" > /dev/null && ! pgrep -x "crond" > /dev/null; then
    echo -e "${YELLOW}! Warning: Cron service doesn't appear to be running${NC}"
    echo "You may need to start it with: sudo systemctl start cron"
    echo "or: sudo service cron start"
fi

# Show manual run command
echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Automatic scanning will run:"
echo "  - Schedule: Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)"
echo "  - Log file: $LOG_DIR/cron.log"
echo ""
echo "To manually run the scanner now:"
echo "  $SCAN_SCRIPT"
echo ""
echo "To view scan results:"
echo "  cat $SCRIPT_DIR/extracted_prompts.json"
echo ""
echo "To view logs:"
echo "  cat $LOG_DIR/cron.log"
echo ""
echo "To remove the cron job later:"
echo "  crontab -e"
echo "  # Then delete the line containing: $SCAN_SCRIPT"
echo ""
