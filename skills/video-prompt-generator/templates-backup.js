/**
 * Video Prompt Generator - Prompt Templates
 *
 * Organized by category with 10+ video-specific creative styles
 * Each template includes placeholders for dynamic topic insertion
 */

const templates = {
// Category mapping for UI (short names)
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

function normalizeCategory(category) {
  return categoryMapping[category] || category;
}

function denormalizeCategory(category) {
  return reverseCategoryMapping[category] || category;
}
  landscapeScenery: [
    {
      name: "Serene Mountain Sunrise",
      template: (topic) =>
        `Cinematic video of ${topic} at sunrise over misty mountains, golden hour light breaking through clouds, slow camera movement revealing scenic panorama, dramatic lighting with soft shadows, 4K quality, peaceful and majestic atmosphere`
    },
    {
      name: "Ocean Sunset Drone Shot",
      template: (topic) =>
        `Aerial drone shot of ${topic} by the ocean at sunset, golden and orange hues reflecting on water, slow descent toward coastline, cinematic composition, romantic and peaceful mood, seagulls flying in background`
    },
    {
      name: "Forest Canopy Walkthrough",
      template: (topic) =>
        `First-person camera walking through ${topic} in lush forest, sunlight filtering through green canopy, dappled light patterns on path, immersive and serene atmosphere, gentle ambient sound, natural and organic feel`
    },
    {
      name: "Urban City Timelapse",
      template: (topic) =>
        `Timelapse video of ${topic} in modern city center, day-to-night transition, buildings lighting up, cars flowing like light rivers, dynamic energy, vibrant urban atmosphere, cyberpunk aesthetic`
    },
    {
      name: "Seasonal Cherry Blossom",
      template: (topic) =>
        `${topic} surrounded by falling cherry blossom petals, gentle spring breeze, soft pink and white flowers, romantic and dreamy atmosphere, slow motion capture of petals dancing in air`
    }
  ],

  productShowcase: [
    {
      name: "Cinematic Product Reveal",
      template: (topic) =>
        `Slow cinematic reveal of ${topic} with dramatic lighting, rotating 360-degree showcase, sleek black background, premium product photography aesthetic, professional and sophisticated presentation`
    },
    {
      name: "Lifestyle Product Usage",
      template: (topic) =>
        `${topic} in authentic lifestyle setting, person using product naturally, candid shot, warm natural lighting, relatable and aspirational atmosphere, product in focus with soft background blur`
    },
    {
      name: "E-commerce Flat Lay",
      template: (topic) =>
        `Flat lay video of ${topic} on clean marble surface, subtle floating motion, minimal props, soft shadows, premium product photography, elegant and sophisticated aesthetic`
    },
    {
      name: "Exploded View Animation",
      template: (topic) =>
        `${topic} in exploded 3D view, components floating and assembling, clean white background, technical and informative, smooth animation, product understanding and assembly process`
    },
    {
      name: "Unboxing Experience",
      template: (topic) =>
        `First-person unboxing experience of ${topic}, box opening with excitement, product reveal, packaging details, premium feel, celebratory and joyful atmosphere`
    }
  ],

  techFuture: [
    {
      name: "Cyberpunk Neon City",
      template: (topic) =>
        `${topic} in cyberpunk cityscape at night, neon lights reflecting on wet streets, holographic displays, flying cars in background, futuristic and edgy atmosphere, Blade Runner aesthetic`
    },
    {
      name: "AI Digital Interface",
      template: (topic) =>
        `${topic} with floating AI interface elements, holographic data visualizations, neural network patterns, futuristic tech aesthetic, blue and cyan lighting, innovative and cutting-edge`
    },
    {
      name: "Space Station View",
      template: (topic) =>
        `${topic} aboard space station, Earth visible through window, zero gravity floating, stars and nebula in background, awe-inspiring and cosmic, cinematic sci-fi aesthetic`
    },
    {
      name: "Digital Glitch Art",
      template: (topic) =>
        `${topic} with digital glitch effects, pixelated distortions, RGB color splits, cyberpunk aesthetic, tech-forward design, edgy and contemporary`
    },
    {
      name: "Futuristic Laboratory",
      template: (topic) =>
        `${topic} in advanced laboratory setting, holographic displays, robotic arms, clean white and blue color scheme, innovative and scientific, high-tech research aesthetic`
    }
  ],

  emotionalStory: [
    {
      name: "Romantic Moonlight Scene",
      template: (topic) =>
        `${topic} under moonlight, romantic and intimate, soft silver lighting, emotional connection, slow camera movements, love story atmosphere`
    },
    {
      name: "Nostalgic Vintage Film",
      template: (topic) =>
        `${topic} in vintage film aesthetic, sepia tones, warm nostalgic feeling, memory and reminiscence, classic and timeless`
    },
    {
      name: "Inspiring Journey",
      template: (topic) =>
        `${topic} representing journey and growth, dramatic landscape transition, hopeful music, motivational energy, rising from challenge to triumph`
    },
    {
      name: "Bittersweet Goodbye",
      template: (topic) =>
        `${topic} in bittersweet farewell scene, emotional and touching, mix of sadness and hope, intimate close-up, authentic feeling`
    },
    {
      name: "Celebration and Joy",
      template: (topic) =>
        `${topic} in moment of pure celebration, confetti and joy, bright happy colors, genuine happiness and excitement`
    }
  ],

  urbanLife: [
    {
      name: "Street Cafe Morning",
      template: (topic) =>
        `${topic} in bustling street cafe scene, morning sunlight, people enjoying coffee, vibrant urban energy, authentic and relatable, cozy and welcoming atmosphere`
    },
    {
      name: "Modern Office Workspace",
      template: (topic) =>
        `${topic} in stylish modern office, clean desk setup with plants, productivity and focus, natural lighting, contemporary work-from-home aesthetic`
    },
    {
      name: "Night City Walking",
      template: (topic) =>
        `${topic} walking through city at night, neon lights reflecting, urban exploration, cinematic composition, mysterious and alluring`
    },
    {
      name: "Subway Commute",
      template: (topic) =>
        `${topic} in subway commute scene, underground lighting, authentic daily life, movement and energy, urban realism`
    },
    {
      name: "Rooftop City View",
      template: (topic) =>
        `${topic} with city skyline view, golden hour sunset, urban lifestyle, aspirational and freeing, epic and cinematic`
    }
  ],

  foodCooking: [
    {
      name: "Food Preparation Close-up",
      template: (topic) =>
        `Close-up video of ${topic} preparation, fresh ingredients, sharp knife movements, appetizing food photography, mouth-watering detail, professional culinary aesthetic`
    },
    {
      name: "Cooking Process",
      template: (topic) =>
        `${topic} cooking in modern kitchen, steam rising, sizzling sounds, chef preparing with expertise, appetizing and inviting, culinary expertise showcase`
    },
    {
      name: "Plating Presentation",
      template: (topic) =>
        `Elegant plating of ${topic} on white plate, artistic arrangement, garnish details, fine dining aesthetic, professional and sophisticated`
    },
    {
      name: "Farm to Table",
      template: (topic) =>
        `${topic} from farm to table journey, fresh ingredients, natural setting, organic and sustainable, authentic and wholesome`
    },
    {
      name: "Food Porn Aesthetic",
      template: (topic) =>
        `Slow-motion video of ${topic} with dramatic lighting, glistening textures, extreme close-up, food porn aesthetic, irresistible and appetizing`
    }
  ],

  sportsFitness: [
    {
      name: "Dynamic Sports Action",
      template: (topic) =>
        `${topic} in dynamic sports action, fast movement, intense energy, competitive spirit, slow-motion capture of key moments, athletic excellence`
    },
    {
      name: "Gym Workout Routine",
      template: (topic) =>
        `${topic} in modern gym setting, dedicated workout routine, fitness motivation, energy and determination, healthy lifestyle promotion`
    },
    {
      name: "Outdoor Adventure",
      template: (topic) =>
        `${topic} in outdoor adventure setting, nature background, active lifestyle, freedom and exploration, inspiring and energetic`
    },
    {
      name: "Yoga and Meditation",
      template: (topic) =>
        `${topic} in peaceful yoga or meditation scene, calm and centered, natural lighting, mindfulness and wellness, serene atmosphere`
    },
    {
      name: "Team Spirit",
      template: (topic) =>
        `${topic} capturing team spirit and camaraderie, group celebration, unity and collaboration, uplifting and motivational`
    }
  ],

  ancientChinese: [
    {
      name: "Traditional Chinese Garden",
      template: (topic) =>
        `${topic} in traditional Chinese garden, ancient architecture, koi pond, cherry blossoms, serene and timeless, cultural authenticity`
    },
    {
      name: "Hanfu Costume Showcase",
      template: (topic) =>
        `${topic} wearing elegant Hanfu costume, flowing fabric, traditional Chinese setting, cultural heritage, graceful and poetic`
    },
    {
      name: "Ink Wash Painting Style",
      template: (topic) =>
        `${topic} in traditional Chinese ink wash painting aesthetic, brush stroke textures, monochromatic with color accents, artistic and cultural`
    },
    {
      name: "Ancient Architecture",
      template: (topic) =>
        `${topic} with ancient Chinese architecture background, traditional patterns, cultural symbolism, historical and majestic`
    },
    {
      name: "Wuxia Martial Arts",
      template: (topic) =>
        `${topic} in wuxia martial arts scene, flowing movements, traditional Chinese setting, heroic and cinematic, ancient martial arts aesthetic`
    }
  ],

  animeStyle: [
    {
      name: "Anime Opening Style",
      template: (topic) =>
        `${topic} in anime opening sequence style, vibrant colors, dynamic action poses, speed lines, anime aesthetic, energetic and stylized`
    },
    {
      name: "Kawaii Chibi Character",
      template: (topic) =>
        `${topic} as cute kawaii chibi character, big expressive eyes, soft rounded shapes, adorable and appealing, playful and fun`
    },
    {
      name: "Fantasy School Life",
      template: (topic) =>
        `${topic} in anime fantasy school life setting, colorful classrooms, magical elements, slice of life with fantasy twist`
    },
    {
      name: "Mecha Robot Battle",
      template: (topic) =>
        `${topic} in epic mecha robot battle scene, glowing energy beams, dramatic explosions, sci-fi anime aesthetic, intense and spectacular`
    },
    {
      name: "Magical Girl Transformation",
      template: (topic) =>
        `${topic} in magical girl transformation scene, sparkles and light effects, flowing ribbons, magical and whimsical, anime aesthetic`
    }
  ],

  abstractArt: [
    {
      name: "Liquid Abstract Art",
      template: (topic) =>
        `${topic} morphing in liquid abstract art, flowing colors, organic shapes, dreamy and surreal, artistic and experimental`
    },
    {
      name: "Geometric Patterns",
      template: (topic) =>
        `${topic} with geometric pattern overlay, repeating shapes, clean lines, mathematical beauty, modern and minimalist`
    },
    {
      name: "Particle Explosion",
      template: (topic) =>
        `${topic} with particle explosion effects, glowing points, burst of energy, dynamic and vibrant, futuristic and stunning`
    },
    {
      name: "Ink in Water",
      template: (topic) =>
        `${topic} with ink dropping into water, swirling patterns, organic diffusion, artistic and meditative, black and white aesthetic`
    },
    {
      name: "Fractal Zoom",
      template: (topic) =>
        `${topic} zooming into fractal patterns, infinite detail, mathematical beauty, psychedelic and mesmerizing, trippy and abstract`
    }
  ]
};

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
    throw new Error(`Invalid category or style index: ${category}, ${styleIndex}`);
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
