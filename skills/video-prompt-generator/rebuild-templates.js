#!/usr/bin/env node
/**
 * Rebuild templates.js from Python templates.py
 */

const fs = require('fs');
const { execSync } = require('child_process');

// Run Python to extract templates
const pythonCode = `
import sys
import json
sys.path.insert(0, '/root/clawd/skills/video-prompt-generator')
import templates

# Build template structure from VIDEO_STYLES
result = {}
for key, value in templates.VIDEO_STYLES.items():
    if isinstance(value, dict) and 'styles' in value:
        result[key] = value['styles']

print(json.dumps(result, indent=2, ensure_ascii=False))
`;

try {
  console.log('🔄 Extracting templates from Python...');
  const output = execSync(`python3 -c "${pythonCode}"`, { encoding: 'utf8' });
  console.log('✅ Templates extracted successfully!');
  
  // Parse the JSON
  const templatesData = JSON.parse(output);
  
  // Generate JavaScript file content
  let jsContent = `/**
 * Video Prompt Generator - Prompt Templates
 *
 * Organized by category with 10+ video-specific creative styles
 * Each template includes placeholders for dynamic topic insertion
 */

const templates = ${JSON.stringify(templatesData, null, 2)};

// Get all categories
function getAllCategories() {
  return Object.keys(templates);
}

// Get templates by category
function getTemplatesByCategory(category) {
  return templates[category] || [];
}

// Get all templates
function getAllTemplates() {
  return templates;
}

// Generate prompt for specific category and style
function generatePrompt(category, styleIndex, topic) {
  const categoryTemplates = templates[category];
  if (!categoryTemplates || !categoryTemplates[styleIndex]) {
    throw new Error(\`Invalid category or style index: \${category}, \${styleIndex}\`);
  }

  const style = categoryTemplates[styleIndex];
  return {
    category: category,
    style: style.name,
    prompt: style.template(topic)
  };
}

// Generate all prompts for a topic
function generateAllPrompts(topic) {
  const results = [];

  for (const [category, styles] of Object.entries(templates)) {
    styles.forEach((style, index) => {
      results.push({
        category: category,
        style: style.name,
        prompt: style.template(topic)
      });
    });
  }

  return results;
}

// Generate prompts for specific categories
function generatePromptsForCategories(categories, topic) {
  const results = [];

  categories.forEach(category => {
    const categoryTemplates = templates[category];
    if (categoryTemplates) {
      categoryTemplates.forEach((style) => {
        results.push({
          category: category,
          style: style.name,
          prompt: style.template(topic)
        });
      });
    }
  });

  return results;
}

// Get count of total templates
function getTotalTemplateCount() {
  let count = 0;
  for (const category in templates) {
    count += templates[category].length;
  }
  return count;
}

module.exports = {
  templates,
  getAllCategories,
  getTemplatesByCategory,
  getAllTemplates,
  generatePrompt,
  generateAllPrompts,
  generatePromptsForCategories,
  getTotalTemplateCount
};
`;

  // Write the new templates.js file
  fs.writeFileSync('/root/clawd/skills/video-prompt-generator/templates.js', jsContent, 'utf8');
  
  console.log('✅ templates.js rebuilt successfully!');
  console.log('✅ File written to: /root/clawd/skills/video-prompt-generator/templates.js');
  console.log(`\n✅ Total categories: ${Object.keys(templatesData).length}`);
  
  let totalStyles = 0;
  for (const category in templatesData) {
    totalStyles += templatesData[category].length;
  }
  console.log(`✅ Total styles: ${totalStyles}`);
  
} catch (error) {
  console.error('❌ Error:', error.message);
  process.exit(1);
}
