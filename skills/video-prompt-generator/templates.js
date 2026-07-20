/**
 * Video Prompt Generator - Prompt Templates
 *
 * Organized by category with 10+ video-specific creative styles
 * Each template includes placeholders for dynamic topic insertion
 */

const templates = {
  landscape: [
    {
      style: "Serene Mountain Sunrise",
      emoji: "🏔️",
      prompt: (topic) => `Cinematic video of ${topic} at sunrise over misty mountains, golden hour light breaking through clouds, slow camera movement revealing scenic panorama, dramatic lighting with soft shadows, 4K quality, peaceful and majestic atmosphere`
    },
    {
      style: "Ocean Sunset Drone Shot",
      emoji: "🌊",
      prompt: (topic) => `Aerial drone shot of ${topic} by the ocean at sunset, golden and orange hues reflecting on water, slow descent toward coastline, cinematic composition, romantic and peaceful mood, seagulls flying in background`
    },
    {
      style: "Forest Canopy Walkthrough",
      emoji: "🌲",
      prompt: (topic) => `First-person camera walking through ${topic} in lush forest, sunlight filtering through green canopy, dappled light patterns on path, immersive and serene atmosphere, gentle ambient sound, natural and organic feel`
    },
    {
      style: "Urban City Timelapse",
      emoji: "🏙",
      prompt: (topic) => `Timelapse video of ${topic} in modern city center, day-to-night transition, buildings lighting up, cars flowing like light rivers, dynamic energy, vibrant urban atmosphere, cyberpunk aesthetic`
    },
    {
      style: "Seasonal Cherry Blossom",
      emoji: "🌸",
      prompt: (topic) => `${topic} surrounded by falling cherry blossom petals, gentle spring breeze, soft pink and white flowers, romantic and dreamy atmosphere, slow motion capture of petals dancing in air`
    }
  ],
  product: [
    {
      style: "Cinematic Product Reveal",
      emoji: "📦",
      prompt: (topic) => `Slow cinematic reveal of ${topic} with dramatic lighting, rotating 360-degree showcase, sleek black background, premium product photography aesthetic, professional and sophisticated presentation`
    },
    {
      style: "Lifestyle Product Usage",
      emoji: "📱",
      prompt: (topic) => `${topic} in authentic lifestyle setting, person using product naturally, candid shot, warm natural lighting, relatable and aspirational atmosphere, product in focus with soft background blur`
    },
    {
      style: "E-commerce Flat Lay",
      emoji: "📦",
      prompt: (topic) => `Flat lay video of ${topic} on clean marble surface, subtle floating motion, minimal props, soft shadows, premium product photography, elegant and sophisticated aesthetic`
    },
    {
      style: "Exploded View Animation",
      emoji: "🔧",
      prompt: (topic) => `${topic} in exploded 3D view, components floating and assembling, clean white background, technical and informative, smooth animation, product understanding and assembly process`
    },
    {
      style: "Unboxing Experience",
      emoji: "📦",
      prompt: (topic) => `First-person unboxing experience of ${topic}, box opening with excitement, product reveal, packaging details, premium feel, celebratory and joyful atmosphere`
    }
  ],
  tech: [
    {
      style: "Cyberpunk Neon City",
      emoji: "🌃",
      prompt: (topic) => `${topic} in cyberpunk cityscape at night, neon lights reflecting on wet streets, holographic displays, flying cars in background, futuristic and edgy atmosphere, Blade Runner aesthetic`
    },
    {
      style: "AI Digital Interface",
      emoji: "🤖",
      prompt: (topic) => `${topic} with floating AI interface elements, holographic data visualizations, neural network patterns, futuristic tech aesthetic, blue and cyan lighting, innovative and cutting-edge`
    },
    {
      style: "Space Station View",
      emoji: "🚀",
      prompt: (topic) => `${topic} aboard space station, Earth visible through window, zero gravity floating, stars and nebula in background, awe-inspiring and cosmic, cinematic sci-fi aesthetic`
    },
    {
      style: "Digital Glitch Art",
      emoji: "📺",
      prompt: (topic) => `${topic} with digital glitch effects, pixelated distortions, RGB color splits, cyberpunk aesthetic, tech-forward design, edgy and contemporary`
    },
    {
      style: "Futuristic Laboratory",
      emoji: "🔬",
      prompt: (topic) => `${topic} in advanced laboratory setting, holographic displays, robotic arms, clean white and blue color scheme, innovative and scientific, high-tech research aesthetic`
    }
  ],
  emotional: [
    {
      style: "Romantic Moonlight Scene",
      emoji: "🌙",
      prompt: (topic) => `${topic} under moonlight, romantic and intimate, soft silver lighting, emotional connection, slow camera movements, love story atmosphere`
    },
    {
      style: "Nostalgic Vintage Film",
      emoji: "🎞",
      prompt: (topic) => `${topic} in vintage film aesthetic, sepia tones, warm nostalgic feeling, memory and reminiscence, classic and timeless`
    },
    {
      style: "Inspiring Journey",
      emoji: "🌟",
      prompt: (topic) => `${topic} representing journey and growth, dramatic landscape transition, hopeful music, motivational energy, rising from challenge to triumph`
    },
    {
      style: "Bittersweet Goodbye",
      emoji: "💔",
      prompt: (topic) => `${topic} in bittersweet farewell scene, emotional and touching, mix of sadness and hope, intimate close-up, authentic feeling`
    },
    {
      style: "Celebration and Joy",
      emoji: "🎉",
      prompt: (topic) => `${topic} in moment of pure celebration, confetti and joy, bright happy colors, genuine happiness and excitement`
    }
  ],
  urban: [
    {
      style: "Street Cafe Morning",
      emoji: "☕",
      prompt: (topic) => `${topic} in bustling street cafe scene, morning sunlight, people enjoying coffee, vibrant urban energy, authentic and relatable, cozy and welcoming atmosphere`
    },
    {
      style: "Modern Office Workspace",
      emoji: "💼",
      prompt: (topic) => `${topic} in stylish modern office, clean desk setup with plants, productivity and focus, natural lighting, contemporary work-from-home aesthetic`
    },
    {
      style: "Night City Walking",
      emoji: "🌃",
      prompt: (topic) => `${topic} walking through city at night, neon lights reflecting, urban exploration, cinematic composition, mysterious and alluring`
    },
    {
      style: "Subway Commute",
      emoji: "🚇",
      prompt: (topic) => `${topic} in subway commute scene, underground lighting, authentic daily life, movement and energy, urban realism`
    },
    {
      style: "Rooftop City View",
      emoji: "🌆",
      prompt: (topic) => `${topic} with city skyline view, golden hour sunset, urban lifestyle, aspirational and freeing, epic and cinematic`
    }
  ],
  food: [
    {
      style: "Food Preparation Close-up",
      emoji: "🍽",
      prompt: (topic) => `Close-up video of ${topic} preparation, fresh ingredients, sharp knife movements, appetizing food photography, mouth-watering detail, professional culinary aesthetic`
    },
    {
      style: "Cooking Process",
      emoji: "👨‍🍳",
      prompt: (topic) => `${topic} cooking in modern kitchen, steam rising, sizzling sounds, chef preparing with expertise, appetizing and inviting, culinary expertise showcase`
    },
    {
      style: "Plating Presentation",
      emoji: "🍴",
      prompt: (topic) => `Elegant plating of ${topic} on white plate, artistic arrangement, garnish details, fine dining aesthetic, professional and sophisticated`
    },
    {
      style: "Farm to Table",
      emoji: "🌱",
      prompt: (topic) => `${topic} from farm to table journey, fresh ingredients, natural setting, organic and sustainable, authentic and wholesome`
    },
    {
      style: "Food Porn Aesthetic",
      emoji: "📸",
      prompt: (topic) => `Slow-motion video of ${topic} with dramatic lighting, glistening textures, extreme close-up, food porn aesthetic, irresistible and appetizing`
    }
  ],
  sports: [
    {
      style: "Dynamic Sports Action",
      emoji: "⚽",
      prompt: (topic) => `${topic} in dynamic sports action, fast movement, intense energy, competitive spirit, slow-motion capture of key moments, athletic excellence`
    },
    {
      style: "Gym Workout Routine",
      emoji: "🏋",
      prompt: (topic) => `${topic} in modern gym setting, dedicated workout routine, fitness motivation, energy and determination, healthy lifestyle promotion`
    },
    {
      style: "Outdoor Adventure",
      emoji: "🏔",
      prompt: (topic) => `${topic} in outdoor adventure setting, nature background, active lifestyle, freedom and exploration, inspiring and energetic`
    },
    {
      style: "Yoga and Meditation",
      emoji: "🧘",
      prompt: (topic) => `${topic} in peaceful yoga or meditation scene, calm and centered, natural lighting, mindfulness and wellness, serene atmosphere`
    },
    {
      style: "Team Spirit",
      emoji: "🏆",
      prompt: (topic) => `${topic} capturing team spirit and camaraderie, group celebration, unity and collaboration, uplifting and motivational`
    }
  ],
  ancient: [
    {
      style: "Traditional Chinese Garden",
      emoji: "🏯",
      prompt: (topic) => `${topic} in traditional Chinese garden, ancient architecture, koi pond, cherry blossoms, serene and timeless, cultural authenticity`
    },
    {
      style: "Hanfu Costume Showcase",
      emoji: "👘",
      prompt: (topic) => `${topic} wearing elegant Hanfu costume, flowing fabric, traditional Chinese setting, cultural heritage, graceful and poetic`
    },
    {
      style: "Ink Wash Painting Style",
      emoji: "🖌️",
      prompt: (topic) => `${topic} in traditional Chinese ink wash painting aesthetic, brush stroke textures, monochromatic with color accents, artistic and cultural`
    },
    {
      style: "Ancient Architecture",
      emoji: "🏛️",
      prompt: (topic) => `${topic} with ancient Chinese architecture background, traditional patterns, cultural symbolism, historical and majestic`
    },
    {
      style: "Wuxia Martial Arts",
      emoji: "⚔",
      prompt: (topic) => `${topic} in wuxia martial arts scene, flowing movements, traditional Chinese setting, heroic and cinematic, ancient martial arts aesthetic`
    }
  ],
  anime: [
    {
      style: "Anime Opening Style",
      emoji: "🎬",
      prompt: (topic) => `${topic} in anime opening sequence style, vibrant colors, dynamic action poses, speed lines, anime aesthetic, energetic and stylized`
    },
    {
      style: "Kawaii Chibi Character",
      emoji: "😊",
      prompt: (topic) => `${topic} as cute kawaii chibi character, big expressive eyes, soft rounded shapes, adorable and appealing, playful and fun`
    },
    {
      style: "Fantasy School Life",
      emoji: "🏫",
      prompt: (topic) => `${topic} in anime fantasy school life setting, colorful classrooms, magical elements, slice of life with fantasy twist`
    },
    {
      style: "Mecha Robot Battle",
      emoji: "🤖",
      prompt: (topic) => `${topic} in epic mecha robot battle scene, glowing energy beams, dramatic explosions, sci-fi anime aesthetic, intense and spectacular`
    },
    {
      style: "Magical Girl Transformation",
      emoji: "✨",
      prompt: (topic) => `${topic} in magical girl transformation scene, sparkles and light effects, flowing ribbons, magical and whimsical, anime aesthetic`
    }
  ],
  abstract: [
    {
      style: "Liquid Abstract Art",
      emoji: "💧",
      prompt: (topic) => `${topic} morphing in liquid abstract art, flowing colors, organic shapes, dreamy and surreal, artistic and experimental`
    },
    {
      style: "Geometric Patterns",
      emoji: "🔷",
      prompt: (topic) => `${topic} with geometric pattern overlay, repeating shapes, clean lines, mathematical beauty, modern and minimalist`
    },
    {
      style: "Particle Explosion",
      emoji: "💥",
      prompt: (topic) => `${topic} with particle explosion effects, glowing points, burst of energy, dynamic and vibrant, futuristic and stunning`
    },
    {
      style: "Ink in Water",
      emoji: "🖌️",
      prompt: (topic) => `${topic} with ink dropping into water, swirling patterns, organic diffusion, artistic and meditative, black and white aesthetic`
    },
    {
      style: "Fractal Zoom",
      emoji: "🌀",
      prompt: (topic) => `${topic} zooming into fractal patterns, infinite detail, mathematical beauty, psychedelic and mesmerizing, trippy and abstract`
    }
  ]
};

// Get all categories (short names)
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
    style: style.style,
    prompt: style.prompt(topic)
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
        prompt: style.prompt(topic)
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
          prompt: style.prompt(topic)
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
