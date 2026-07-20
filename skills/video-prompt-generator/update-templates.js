#!/usr/bin/env node

const fs = require('fs');

// Read the original file
const content = fs.readFileSync('templates.js', 'utf8');

// Find the module.exports section and replace it
const newExports = `
module.exports = {
  templates,
  categoryMapping: {
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
  },
  reverseCategoryMapping: {
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
  },
  normalizeCategory: function(category) {
    return this.categoryMapping[category] || category;
  },
  denormalizeCategory: function(category) {
    return this.reverseCategoryMapping[category] || category;
  },
  getAllCategories,
  getAllFullCategories,
  getTemplatesByCategory,
  getAllTemplates,
  generatePrompt,
  generateAllPrompts,
  generatePromptsForCategories,
  getTotalTemplateCount
};`;

// Add getAllFullCategories function before module.exports
const getAllFullCategories = `
// Get all full category names
function getAllFullCategories() {
  return Object.keys(templates);
}
`;

// Helper to modify getTemplatesByCategory to use mapping
const modifiedGetTemplatesByCategory = `
// Get templates by category (supports both short and full names)
function getTemplatesByCategory(category) {
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
  const normalizedCategory = categoryMapping[category] || category;
  return templates[normalizedCategory] || [];
}
`;

const reverseCategoryMapping = `
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
`;

// Modify getAllCategories to return short names
const modifiedGetAllCategories = `
// Get all categories (returns short names for UI)
function getAllCategories() {
  return ['landscape', 'product', 'tech', 'emotional', 'urban', 'food', 'sports', 'ancient', 'anime', 'abstract'];
}
`;

// Update generatePrompt
const modifiedGeneratePrompt = `
// Generate prompt for specific category and style
function generatePrompt(category, styleIndex, topic) {
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

  const normalizedCategory = categoryMapping[category] || category;
  const categoryTemplates = templates[normalizedCategory];
  if (!categoryTemplates || !categoryTemplates[styleIndex]) {
    throw new Error(\`Invalid category or style index: \${category}, \${styleIndex}\`);
  }

  const style = categoryTemplates[styleIndex];
  return {
    category: reverseCategoryMapping[normalizedCategory] || normalizedCategory,
    style: style.name,
    prompt: style.template(topic)
  };
}
`;

// Update generateAllPrompts
const modifiedGenerateAllPrompts = `
// Generate all prompts for a topic
function generateAllPrompts(topic) {
  const results = [];
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

  for (const [category, styles] of Object.entries(templates)) {
    styles.forEach((style, index) => {
      results.push({
        category: reverseCategoryMapping[category] || category,
        style: style.name,
        prompt: style.template(topic)
      });
    });
  }

  return results;
}
`;

// Update generatePromptsForCategories
const modifiedGeneratePromptsForCategories = `
// Generate prompts for specific categories
function generatePromptsForCategories(categories, topic) {
  const results = [];
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

  categories.forEach(category => {
    const normalizedCategory = categoryMapping[category] || category;
    const categoryTemplates = templates[normalizedCategory];
    if (categoryTemplates) {
      categoryTemplates.forEach((style) => {
        results.push({
          category: reverseCategoryMapping[normalizedCategory] || normalizedCategory,
          style: style.name,
          prompt: style.template(topic)
        });
      });
    }
  });

  return results;
}
`;

// Apply replacements
let newContent = content
  .replace(/\/\/ Get all categories[\s\S]*?function getAllCategories\(\) \{[\s\S]*?^\}/m, modifiedGetAllCategories.trim())
  .replace(/\/\/ Get templates by category[\s\S]*?function getTemplatesByCategory\(category\) \{[\s\S]*?^\}/m, modifiedGetTemplatesByCategory.trim())
  .replace(/\/\/ Generate prompt for specific category and style[\s\S]*?function generatePrompt\(category, styleIndex, topic\) \{[\s\S]*?^\}/m, modifiedGeneratePrompt.trim())
  .replace(/\/\/ Generate all prompts for a topic[\s\S]*?function generateAllPrompts\(topic\) \{[\s\S]*?^\}/m, modifiedGenerateAllPrompts.trim())
  .replace(/\/\/ Generate prompts for specific categories[\s\S]*?function generatePromptsForCategories\(categories, topic\) \{[\s\S]*?^\}/m, modifiedGeneratePromptsForCategories.trim())
  .replace(/module\.exports = \{[\s\S]*?\};$/, newExports.trim());

// Insert getAllFullCategories before module.exports
newContent = newContent.replace(
  /(module\.exports = \{)/,
  `${getAllFullCategories.trim()}\n\n$1`
);

// Write the new content
fs.writeFileSync('templates.js', newContent);

console.log('✅ templates.js updated successfully!');
