#!/bin/bash
# Test Bird CLI search for AI prompts

set -e

echo "=========================================="
echo "Testing Bird CLI Search"
echo "=========================================="
echo ""

# Check authentication
echo "1. Checking authentication..."
if bird whoami &> /dev/null; then
    echo "✓ Authenticated as: $(bird whoami --plain)"
else
    echo "✗ Authentication failed. Please configure Bird CLI first."
    exit 1
fi

echo ""
echo "2. Testing search for AI prompts..."
echo ""

# Search queries
queries=(
    '"ChatGPT prompt" OR "AI prompt"'
    '"Claude prompt" OR "Claude AI"'
    '"prompt engineering" OR "prompt template"'
    '"best prompt" OR "effective prompt"'
)

mkdir -p logs
timestamp=$(date +%Y%m%d_%H%M%S)
logfile="logs/bird_test_${timestamp}.json"

# Run searches and save results
echo "Running searches and saving to $logfile..."
echo "[" > "$logfile"

first=true
for query in "${queries[@]}"; do
    echo "Searching: $query"
    if ! $first; then
        echo "," >> "$logfile"
    fi

    bird search "$query" -n 10 --json --no-color >> "$logfile"
    first=false
done

echo "]" >> "$logfile"

echo ""
echo "✓ Search complete. Results saved to $logfile"
echo ""
echo "3. Sample results:"
echo ""

# Display first few results
jq -r '.[] | select(.text) | "\(.url)\n\(.text[0:100])...\n"' "$logfile" 2>/dev/null | head -20 || echo "Unable to parse JSON results"

echo ""
echo "=========================================="
echo "Test Complete!"
echo "=========================================="
