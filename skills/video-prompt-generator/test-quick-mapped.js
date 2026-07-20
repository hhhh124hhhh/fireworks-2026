#!/usr/bin/env node

/**
 * Quick test for video prompt generator with category mapping
 */

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

function mapCategories(categories) {
  return categories.map(cat => categoryMapping[cat] || cat);
}

function unmapCategory(category) {
  return reverseCategoryMapping[category] || category;
}

const templates = require('./templates');

// Test prompt generation with mapping
const topic = "猫咪玩耍";
const shortCategories = ["landscape", "product"];
const mappedCategories = mapCategories(shortCategories);

console.log(`\n🎬 Testing Video Prompt Generator with Category Mapping\n`);
console.log(`Topic: ${topic}`);
console.log(`Short Categories: ${shortCategories.join(', ')}`);
console.log(`Mapped Categories: ${mappedCategories.join(', ')}\n`);

const prompts = templates.generatePromptsForCategories(mappedCategories, topic);

prompts.forEach((p, index) => {
  const shortCat = unmapCategory(p.category);
  console.log(`\n${index + 1}. [${shortCat}] ${p.style}`);
  console.log(`   ${p.prompt}`);
});

console.log(`\n✅ Generated ${prompts.length} prompts\n`);
