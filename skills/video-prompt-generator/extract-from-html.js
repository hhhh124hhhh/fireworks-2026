#!/usr/bin/env node
/**
 * Extract promptTemplates from HTML and rebuild templates.js
 */

const fs = require('fs');
const { execSync } = require('child_process');

// Extract promptTemplates from HTML
console.log('🔄 Extracting promptTemplates from HTML...');

const htmlContent = fs.readFileSync('/tmp/hhhh124hhhh.github.io/video-prompt-generator.html', 'utf8');

// Find the promptTemplates object
const match = htmlContent.match(/const promptTemplates = \{[\s\S]*?\n        \};/s);

if (!match) {
  console.error('❌ Could not find promptTemplates in HTML');
  process.exit(1);
}

const promptTemplatesStr = match[0];
console.log('✅ promptTemplates extracted successfully!');
console.log(`✅ Length: ${promptTemplatesStr.length} characters`);

// Build the templates.js file
const templatesJS = `/**
 * Video Prompt Generator - Prompt Templates
 *
 * Organized by category with 10+ video-specific creative styles
 * Each template includes placeholders for dynamic topic insertion
 */

const templates = ${promptTemplatesStr.replace('const promptTemplates = ', '').replace('};', '')};

// Helper functions for Web UI compatibility
const categoryMapping = {
  'landscape': 'landscape',
  'product': 'product',
  'tech': 'tech',
  'emotional': 'emotional',
  'urban': 'urban',
  'food': 'food',
  'sports': 'sports',
  'ancient': 'ancient',
  'anime': 'anime',
  'abstract': 'abstract'
};

const reverseCategoryMapping = {
  'landscape': 'landscape',
  'product': 'product',
  'tech': 'tech',
  'emotional': 'emotional',
  'urban': 'urban',
  'food': 'food',
  'sports': 'sports',
  'ancient': 'ancient',
  'anime': 'anime',
  'abstract': 'abstract'
};

// Get all categories (short names)
function getAllCategories() {
  return Object.keys(categoryMapping);
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
    style: style.style,
    prompt: style.prompt.replace(/\{topic\}/g, topic)
  };
}

// Generate all prompts for a topic
function generateAllPrompts(topic) {
  const results = [];

  for (const [category, styles] of Object.entries(templates)) {
    styles.forEach((style, index) => {
      results.push({
        category: category,
        style: style.style,
        prompt: style.prompt.replace(/\{topic\}/g, topic)
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
          style: style.style,
          prompt: style.prompt.replace(/\{topic\}/g, topic)
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
  categoryMapping,
  reverseCategoryMapping,
  getAllCategories,
  getTemplatesByCategory,
  getAllTemplates,
  generatePrompt,
  generateAllPrompts,
  generatePromptsForCategories,
  getTotalTemplateCount
};
`;

// Write new templates.js
const outputPath = '/root/clawd/skills/video-prompt-generator/templates.js';
fs.writeFileSync(outputPath, templatesJS, 'utf8');

console.log(`✅ templates.js rebuilt successfully!`);
console.log(`✅ File written to: ${outputPath}`);

// Count categories and styles
let totalStyles = 0;
for (const category in JSON.parse(promptTemplatesStr.replace('const promptTemplates = ', '').replace('};', ''))) {
  const styles = JSON.parse(promptTemplatesStr.replace('const promptTemplates = ', '').replace('};', ''))[category];
  if (Array.isArray(styles)) {
    totalStyles += styles.length;
  }
}
console.log(`✅ Total categories: ${Object.keys(JSON.parse(promptTemplatesStr.replace('const promptTemplates = ', '').replace('};', ''))).length}`);
console.log(`✅ Total styles: ${totalStyles}`);
