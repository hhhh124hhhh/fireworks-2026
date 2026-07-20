#!/bin/bash

# Improved Twitter Search Wrapper Script
# This script loads the Twitter API key and runs the improved search script

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/twitter_search_improved.py"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ Error: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi

# Try to load API key from shell config files
load_api_key() {
    local api_key=""

    # Check if TWITTER_API_KEY is already set
    if [ -n "$TWITTER_API_KEY" ]; then
        api_key="$TWITTER_API_KEY"
    else
        # Try to load from .bashrc
        if [ -f "$HOME/.bashrc" ]; then
            api_key=$(grep "^export TWITTER_API_KEY=" "$HOME/.bashrc" 2>/dev/null | cut -d'=' -f2 | tr -d '"')
        fi

        # Try to load from .zshrc if not found
        if [ -z "$api_key" ] && [ -f "$HOME/.zshrc" ]; then
            api_key=$(grep "^export TWITTER_API_KEY=" "$HOME/.zshrc" 2>/dev/null | cut -d'=' -f2 | tr -d '"')
        fi
    fi

    echo "$api_key"
}

# Check Python installation
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo "❌ Error: Python 3 is not installed"
        echo "   Please install Python 3 to use this script"
        exit 1
 fi

    # Check requests library
    if ! python3 -c "import requests" 2>/dev/null; then
        echo "⚠️  Warning: 'requests' library not found"
        echo "   Installing with pip..."
        pip3 install requests -q
    fi
}

# Main function
main() {
    # Load API key
    API_KEY=$(load_api_key)

    if [ -z "$API_KEY" ]; then
        echo "❌ Error: TWITTER_API_KEY not found"
        echo ""
        echo "Please set your Twitter API key:"
        echo "  1. Get an API key from https://twitterapi.io"
        echo "  2. Add it to your shell config:"
        echo "     echo 'export TWITTER_API_KEY=\"your_key_here\"' >> ~/.bashrc"
        echo "     source ~/.bashrc"
        echo ""
        echo "Or pass it as an argument: --api-key YOUR_KEY"
        exit 1
    fi

    # Check Python
    check_python

    # Run the Python script
    python3 "$PYTHON_SCRIPT" "$API_KEY" "$@"
}

# Run main function
main "$@"
