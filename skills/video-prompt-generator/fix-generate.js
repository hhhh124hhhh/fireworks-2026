#!/usr/bin/env node
/**
 * Fix generate.js by adding category mapping
 */

const fs = require('fs');
const generatePath = '/root/clawd/skills/video-prompt-generator/generate.js';

// Read the file
const content = fs.readFileSync(generatePath, 'utf8');

// Find the import section and add category mapping after it
const importSection = `} = require('./templates');`;

const categoryMappingCode = `
} = require('./templates');

// Category mapping for short names (used by Web UI)
const categoryMapping = {
  'landscape': 'landscapeScenery',
  'product': 'productShowcase',
  'tech': 'techFuture',
  'emotional': 'emotionalStory',
  'urban': 'urbanLife',
  'food': 'foodCooking',
  'sports': 'sportsFitness',
  'ancient': 'ancientChinese',
  'anime': 'animeStyle',
  'abstract': 'abstractArt'
};

const reverseCategoryMapping = {
  'landscapeScenery': 'landscape',
  'productShowcase': 'product',
  'techFuture': 'tech',
  'emotionalStory': 'emotional',
  'urbanLife': 'urban',
  'foodCooking': 'food',
  'sportsFitness': 'sports',
  'ancientChinese': 'ancient',
  'animeStyle': 'anime',
  'abstractArt': 'abstract'
};

// Helper functions for category mapping
function mapCategory(category) {
  return categoryMapping[category] || category;
}

function mapCategories(categories) {
  return categories.map(cat => categoryMapping[cat] || cat);
}

function unmapCategory(category) {
  return reverseCategoryMapping[category] || category;
}`;

// Replace the import section
if (content.includes(importSection)) {
  const newContent = content.replace(importSection, categoryMappingCode);
  
  // Write the fixed content
  fs.writeFileSync(generatePath, newContent, 'utf8');
  
  console.log('✅ generate.js fixed successfully!');
  console.log('✅ Category mapping added!');
  console.log('\nNext steps:');
  console.log('1. Test prompt generation: node generate.js --topic "猫咪玩耍" --categories "landscape"');
  console.log('2. Start API server: node generate.js --server --port 3000');
  console.log('3. Open Web UI in browser');
} else {
  console.log('❌ Could not find import section in generate.js');
  process.exit(1);
}
