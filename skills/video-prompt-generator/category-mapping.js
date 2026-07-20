/**
 * Category Mapping
 *
 * Maps short category names to full internal names
 * This allows UI to use shorter, more user-friendly names
 */

// Short name -> Full name mapping
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

// Full name -> Short name mapping (reverse)
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

// Normalize category name (short -> full)
function normalizeCategory(category) {
  return categoryMapping[category] || category;
}

// Denormalize category name (full -> short)
function denormalizeCategory(category) {
  return reverseCategoryMapping[category] || category;
}

module.exports = {
  categoryMapping,
  reverseCategoryMapping,
  normalizeCategory,
  denormalizeCategory
};
