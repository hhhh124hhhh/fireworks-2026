#!/usr/bin/env node

/**
 * Quick test for video prompt generator
 */

const {
  generatePromptsForCategories,
  getAllCategories
} = require('./templates');

// Test prompt generation
const topic = "猫咪玩耍";
const categories = ["landscape"];

console.log(`\n🎬 Testing Video Prompt Generator\n`);
console.log(`Topic: ${topic}`);
console.log(`Categories: ${categories.join(', ')}\n`);

const prompts = generatePromptsForCategories(categories, topic);

prompts.forEach((p, index) => {
  console.log(`\n${index + 1}. [${p.category}] ${p.style}`);
  console.log(`   ${p.prompt}`);
});

console.log(`\n✅ Generated ${prompts.length} prompts\n`);
