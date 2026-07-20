#!/bin/bash
# Setup Smart Publisher

echo "🚀 Setting up Smart Skill Publisher..."
echo ""

# Check ClawdHub token
if [[ -z "$CLAWDHUB_TOKEN" ]]; then
  echo "⚠️  CLAWDHUB_TOKEN not found in environment"
  echo ""
  echo "Please set your ClawdHub token:"
  echo "  export CLAWDHUB_TOKEN='your_token_here'"
  echo ""
  echo "Or add to ~/.bashrc for persistence:"
  echo "  echo 'export CLAWDHUB_TOKEN=\"your_token_here\"' >> ~/.bashrc"
  echo ""
  exit 1
fi

# Login to ClawdHub
echo "🔐 Logging in to ClawdHub..."
echo "$CLAWDHUB_TOKEN" | clawdhub login --token -

if [[ $? -eq 0 ]]; then
  echo ""
  echo "✅ Login successful!"
  echo ""
  clawdhub whoami
else
  echo ""
  echo "❌ Login failed"
  exit 1
fi
