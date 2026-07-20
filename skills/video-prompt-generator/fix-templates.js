#!/usr/bin/env node

/**
 * Quick fix for templates.js - Remove the broken category mapping code
 */

const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'templates.js');
const backupPath = path.join(__dirname, 'templates.py');

// Try to get templates from Python file
const { execSync } = require('child_process');

try {
  // Run Python to export templates
  const pythonCode = `
import json
import sys
sys.path.insert(0, '${__dirname}')
import templates

# Build template structure from VIDEO_STYLES
result = {}
for key, value in templates.VIDEO_STYLES.items():
    if isinstance(value, dict) and 'styles' in value:
        result[key] = value['styles']

print(json.dumps(result, indent=2, ensure_ascii=False))
`;

  const output = execSync(`python3 -c "${pythonCode}"`, { encoding: 'utf8' });
  console.log('Extracted templates from Python');
  console.log(output.substring(0, 500));
} catch (error) {
  console.error('Failed to extract from Python:', error.message);
}
