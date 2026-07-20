#!/bin/bash

# AI Prompt Harvester Setup Script
# This script helps set up the automated prompt harvesting system

set -e

echo "=========================================="
echo "AI Prompt Harvester Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check Python 3
echo "Checking Python 3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check Node.js and npm
echo ""
echo "Checking Node.js and npm..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js found: $NODE_VERSION"
else
    print_error "Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org"
    exit 1
fi

if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_status "npm found: $NPM_VERSION"
else
    print_error "npm is not installed"
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install requests python-dotenv 2>/dev/null
print_status "Python dependencies installed"

# Install ClawdHub CLI
echo ""
echo "Installing ClawdHub CLI..."
if ! command -v clawdhub &> /dev/null; then
    npm i -g clawdhub
    print_status "ClawdHub CLI installed"
else
    CLAWDHUB_VERSION=$(clawdhub --version 2>/dev/null || echo "unknown")
    print_status "ClawdHub CLI already installed: $CLAWDHUB_VERSION"
fi

# Check Twitter API Key
echo ""
echo "Checking Twitter API Key..."
if [ -z "$TWITTER_API_KEY" ]; then
    print_warning "TWITTER_API_KEY environment variable not set"
    echo ""
    echo "To get a Twitter API key:"
    echo "1. Visit https://twitterapi.io"
    echo "2. Sign up and get your API key"
    echo "3. Set it with:"
    echo ""
    echo "   export TWITTER_API_KEY='your_key_here'"
    echo ""
    echo "   Or add to ~/.bashrc:"
    echo "   echo 'export TWITTER_API_KEY=\"your_key_here\"' >> ~/.bashrc"
    echo "   source ~/.bashrc"
    echo ""
    read -p "Press Enter to continue after setting the API key, or Ctrl+C to exit..."
else
    print_status "TWITTER_API_KEY is set"
fi

# Check ClawdHub login
echo ""
echo "Checking ClawdHub authentication..."
if clawdhub whoami &> /dev/null; then
    CLAWDHUB_USER=$(clawdhub whoami 2>/dev/null)
    print_status "Logged in to ClawdHub as: $CLAWDHUB_USER"
else
    print_warning "Not logged in to ClawdHub"
    echo ""
    echo "To login to ClawdHub:"
    echo "   clawdhub login"
    echo ""
    read -p "Press Enter to continue after logging in, or Ctrl+C to exit..."
fi

# Set up scripts as executable
echo ""
echo "Setting up scripts..."
chmod +x *.py
print_status "Scripts made executable"

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p state skills-generated logs
print_status "Directories created"

# Test the modules
echo ""
echo "Testing modules..."
python3 evaluate.py
print_status "Evaluation module tested"

python3 convert_to_skill.py
print_status "Converter module tested"

python3 publish.py
print_status "Publisher module tested"

# Summary
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Quick Start:"
echo ""
echo "1. Test run (no publishing):"
echo "   python3 harvest.py --test"
echo ""
echo "2. Full run with auto-publish:"
echo "   python3 harvest.py --auto-publish"
echo ""
echo "3. Set up cron job (every 6 hours):"
echo "   crontab -e"
echo "   Add: 0 */6 * * * cd $(pwd) && /usr/bin/python3 harvest.py --auto-publish >> logs/\$(date +\\%Y\\%m\\%d).log 2>&1"
echo ""
echo "For more information, see README.md"
echo ""
