/**

const {
  normalizeCategory,
  denormalizeCategory
} = require('./category-mapping');

// Get all categories (returns short names for UI)
function getAllCategories() {
  return Object.keys({
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
  });
}

// Get all full category names
function getAllFullCategories() {
  return Object.keys(templates);
}

// Get templates by category (supports both short and full names)
function getTemplatesByCategory(category) {
  const normalizedCategory = normalizeCategory(category);
  return templates[normalizedCategory] || [];
}

// Get all templates
function getAllTemplates() {
  return templates;
}

// Generate prompt for specific category and style
function generatePrompt(category, styleIndex, topic) {
  const normalizedCategory = normalizeCategory(category);
  const categoryTemplates = templates[normalizedCategory];
  if (!categoryTemplates || !categoryTemplates[styleIndex]) {
    throw new Error(`Invalid category or style index: ${category}, ${styleIndex}`);
  }

  const style = categoryTemplates[styleIndex];
  return {
    category: denormalizeCategory(normalizedCategory),
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
        category: denormalizeCategory(category),
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
    const normalizedCategory = normalizeCategory(category);
    const categoryTemplates = templates[normalizedCategory];
    if (categoryTemplates) {
      categoryTemplates.forEach((style) => {
        results.push({
          category: denormalizeCategory(normalizedCategory),
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
  getAllFullCategories,
  getTemplatesByCategory,
  getAllTemplates,
  generatePrompt,
  generateAllPrompts,
  generatePromptsForCategories,
  getTotalTemplateCount
};
