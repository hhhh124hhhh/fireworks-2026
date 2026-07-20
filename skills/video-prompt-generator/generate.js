#!/usr/bin/env node

/**
 * Video Prompt Generator - Main Script
 *
 * Generate high-quality video prompts and optionally create videos using Grok Imagine API
 * Supports 10+ video styles with enhancement and batch generation
 *
 * New Features:
 * - History management with localStorage
 * - Search and filter functionality
 * - Export to JSON/Markdown
 * - Video generation API server
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const http = require('http');
const url = require('url');

// Import templates
const {
  getAllCategories,
  getTemplatesByCategory,
  generateAllPrompts,
  generatePromptsForCategories,
  generatePrompt,
  getTotalTemplateCount

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
}

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m'
};

// Create readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Question wrapper for promises
function question(prompt) {
  return new Promise((resolve) => {
    rl.question(prompt, (answer) => {
      resolve(answer.trim());
    });
  });
}

// Clear screen
function clearScreen() {
  console.clear();
}

// Print header
function printHeader() {
  console.log(`\n${colors.cyan}${colors.bright}╔════════════════════════════════════════════════════════════╗${colors.reset}`);
  console.log(`${colors.cyan}${colors.bright}║          🎬 VIDEO PROMPT GENERATOR v1.0              ║${colors.reset}`);
  console.log(`${colors.cyan}${colors.bright}║          Generate High-Quality Video Prompts       ║${colors.reset}`);
  console.log(`${colors.cyan}${colors.bright}╚════════════════════════════════════════════════════════════╝${colors.reset}\n`);
}

// Print error message
function printError(message) {
  console.log(`\n${colors.red}✗ Error: ${message}${colors.reset}\n`);
}

// Print success message
function printSuccess(message) {
  console.log(`\n${colors.green}✓ ${message}${colors.reset}\n`);
}

// Print info message
function printInfo(message) {
  console.log(`${colors.blue}ℹ ${message}${colors.reset}`);
}

// Print warning message
function printWarning(message) {
  console.log(`${colors.yellow}⚠ ${message}${colors.reset}`);
}

// Validate topic
function validateTopic(topic) {
  if (!topic || topic.length === 0) {
    throw new Error('Topic cannot be empty');
  }
  if (topic.length > 200) {
    throw new Error('Topic too long (max 200 characters)');
  }
  return topic;
}

// Enhance prompt with video-specific details
function enhancePrompt(prompt, enhancements = {}) {
  let enhanced = prompt;

  // Add lighting
  if (enhancements.lighting) {
    enhanced += `, ${enhancements.lighting}`;
  }

  // Add camera movement
  if (enhancements.camera) {
    enhanced += `, ${enhancements.camera}`;
  }

  // Add mood
  if (enhancements.mood) {
    enhanced += `, ${enhancements.mood}`;
  }

  // Add technical specs
  if (enhancements.technical) {
    enhanced += `, ${enhancements.technical}`;
  }

  return enhanced;
}

// Call Grok Imagine API to generate video
async function generateVideoWithGrok(prompt, options = {}) {
  const {
    duration = 5,
    aspectRatio = '16:9',
    resolution = '720p'
  } = options;

  printInfo(`Generating video with Grok Imagine API...`);
  printInfo(`Prompt: ${prompt.substring(0, 100)}...`);
  printInfo(`Duration: ${duration}s, Aspect Ratio: ${aspectRatio}, Resolution: ${resolution}`);

  // Call Python script
  return new Promise((resolve, reject) => {
    const args = [
      'video',
      `"${prompt}"`,
      `--duration ${duration}`,
      `--aspect-ratio ${aspectRatio}`,
      `--resolution ${resolution}`
    ];

    const scriptPath = path.join(__dirname, '..', 'grok-imagine', 'grok-imagine.py');
    const pythonCmd = `python3 ${scriptPath} ${args.join(' ')}`;

    exec(pythonCmd, (error, stdout, stderr) => {
      if (error) {
        printError(`Grok Imagine API call failed: ${error.message}`);
        reject(error);
        return;
      }

      if (stderr) {
        printError(`Grok Imagine API error: ${stderr}`);
        reject(new Error(stderr));
        return;
      }

      // Parse output for video URL
      const videoUrlMatch = stdout.match(/Video URL:\s*(https?:\/\/[^\s]+)/);
      if (videoUrlMatch) {
        printSuccess(`Video generated successfully!`);
        console.log(`${colors.cyan}Video URL: ${colors.bright}${videoUrlMatch[1]}${colors.reset}\n`);
        resolve({
          success: true,
          url: videoUrlMatch[1],
          prompt,
          duration,
          aspectRatio,
          resolution
        });
      } else {
        printWarning('Video generation completed but no URL found in output');
        resolve({
          success: true,
          output: stdout,
          prompt,
          duration,
          aspectRatio,
          resolution
        });
      }
    });
  });
}

// Display category menu
function displayCategoryMenu() {
  const categories = getAllCategories();
  console.log(`${colors.bright}Available Video Categories:${colors.reset}\n`);

  categories.forEach((cat, index) => {
    const styles = getTemplatesByCategory(cat);
    const categoryEmojis = {
      landscapeScenery: '🌄',
      productShowcase: '📦',
      techFuture: '🤖',
      emotionalStory: '💖',
      urbanLife: '🏙',
      foodCooking: '🍜',
      sportsFitness: '🏃',
      ancientChinese: '🏛️',
      animeStyle: '🎨',
      abstractArt: '🎭'
    };
    console.log(`  ${colors.cyan}${index + 1}.${colors.reset} ${categoryEmojis[cat] || '📹'} ${colors.bright}${cat}${colors.reset} (${styles.length} styles)`);
  });

  console.log(`\n${colors.dim}Total: ${getTotalTemplateCount()} video styles${colors.reset}\n`);
}

// Display styles for selected category
function displayStylesMenu(category) {
  const styles = getTemplatesByCategory(category);
  console.log(`\n${colors.bright}${category} Styles:${colors.reset}\n`);

  styles.forEach((style, index) => {
    console.log(`  ${colors.cyan}${index + 1}.${colors.reset} ${colors.bright}${style.name}${colors.reset}`);
  });
}

// Save prompts to file
function savePrompts(prompts, filename = 'video-prompts.json') {
  const data = JSON.stringify(prompts, null, 2);
  fs.writeFileSync(filename, data, 'utf8');
  printSuccess(`Saved ${prompts.length} prompts to ${filename}`);
}

// Interactive mode
async function interactiveMode() {
  clearScreen();
  printHeader();

  // Get topic
  const topic = await question(`${colors.yellow}Enter your video topic (e.g., "cat playing", "sunset over ocean"): ${colors.reset}`);
  const validatedTopic = validateTopic(topic);

  console.log();
  displayCategoryMenu();

  // Get category selection
  const categoryChoice = await question(`${colors.yellow}Select category (1-${getAllCategories().length}, or 'all'): ${colors.reset}`);

  const categories = getAllCategories();
  let selectedCategories = [];

  if (categoryChoice.toLowerCase() === 'all') {
    selectedCategories = categories;
    printInfo('All categories selected');
  } else {
    const categoryIndex = parseInt(categoryChoice) - 1;
    if (categoryIndex >= 0 && categoryIndex < categories.length) {
      selectedCategories = [categories[categoryIndex]];
      printInfo(`Selected: ${categories[categoryIndex]}`);
    } else {
      printError('Invalid category selection');
      return;
    }
  }

  // Get enhancement options
  console.log();
  printInfo('Prompt Enhancement Options (optional):');
  const addEnhancements = await question(`${colors.yellow}Add enhancements? (y/n): ${colors.reset}`);
  let enhancements = {};

  if (addEnhancements.toLowerCase() === 'y') {
    const lighting = await question(`${colors.yellow}Lighting (e.g., "golden hour", "soft"): ${colors.reset}`);
    const camera = await question(`${colors.yellow}Camera (e.g., "slow zoom", "pan right"): ${colors.reset}`);
    const mood = await question(`${colors.yellow}Mood (e.g., "cinematic", "dreamy"): ${colors.reset}`);
    const technical = await question(`${colors.yellow}Technical (e.g., "4K quality", "slow motion"): ${colors.reset}`);

    if (lighting) enhancements.lighting = lighting;
    if (camera) enhancements.camera = camera;
    if (mood) enhancements.mood = mood;
    if (technical) enhancements.technical = technical;
  }

  // Generate prompts
  console.log();
  printInfo('Generating prompts...\n');

  const prompts = generatePromptsForCategories(selectedCategories, validatedTopic);

  // Apply enhancements
  const enhancedPrompts = prompts.map(p => ({
    ...p,
    prompt: enhancePrompt(p.prompt, enhancements)
  }));

  // Display results
  enhancedPrompts.forEach((p, index) => {
    console.log(`\n${colors.bright}${colors.cyan}[${index + 1}] ${p.style}${colors.reset}`);
    console.log(`  ${colors.dim}Category: ${p.category}${colors.reset}`);
    console.log(`  ${colors.white}Prompt: ${colors.reset}${p.prompt}`);
  });

  // Save option
  console.log();
  const saveOption = await question(`${colors.yellow}Save prompts to file? (y/n): ${colors.reset}`);

  if (saveOption.toLowerCase() === 'y') {
    const filename = await question(`${colors.yellow}Filename (default: video-prompts.json): ${colors.reset}`);
    savePrompts(enhancedPrompts, filename || 'video-prompts.json');
  }

  // Generate video option
  console.log();
  const generateOption = await question(`${colors.yellow}Generate video with Grok Imagine API? (y/n): ${colors.reset}`);

  if (generateOption.toLowerCase() === 'y') {
    // Get video options
    const duration = await question(`${colors.yellow}Duration (seconds, 1-15, default 5): ${colors.reset}`);
    const aspectRatio = await question(`${colors.yellow}Aspect Ratio (16:9, 4:3, 1:1, default 16:9): ${colors.reset}`);
    const resolution = await question(`${colors.yellow}Resolution (720p/480p, default 720p): ${colors.reset}`);

    // Select prompt to use
    const promptIndex = await question(`${colors.yellow}Which prompt to use? (1-${enhancedPrompts.length}): ${colors.reset}`);
    const selectedIndex = parseInt(promptIndex) - 1;

    if (selectedIndex >= 0 && selectedIndex < enhancedPrompts.length) {
      const selectedPrompt = enhancedPrompts[selectedIndex];
      console.log();
      printInfo(`Using: ${selectedPrompt.style}\n`);

      try {
        await generateVideoWithGrok(selectedPrompt.prompt, {
          duration: parseInt(duration) || 5,
          aspectRatio: aspectRatio || '16:9',
          resolution: resolution || '720p'
        });
      } catch (error) {
        printError(`Video generation failed: ${error.message}`);
      }
    } else {
      printError('Invalid prompt selection');
    }
  }

  console.log();
  rl.close();
}

// Command line mode
async function commandLineMode(args) {
  const topic = args.topic || args._[0];
  if (!topic) {
    printError('Topic is required. Use --topic <topic>');
    process.exit(1);
  }

  const validatedTopic = validateTopic(topic);

  // Generate prompts
  let prompts;

  if (args.all) {
    printInfo('Generating prompts for all categories...\n');
    prompts = generateAllPrompts(validatedTopic);
  } else if (args.categories) {
    const selectedCategories = args.categories.split(',').map(c => c.trim());
    printInfo(`Generating prompts for categories: ${selectedCategories.join(', ')}\n`);
    prompts = generatePromptsForCategories(selectedCategories, validatedTopic);
  } else {
    printError('Please specify --all or --categories <list>');
    process.exit(1);
  }

  // Apply enhancements if provided
  let enhancedPrompts = prompts;
  if (args.lighting || args.camera || args.mood || args.technical) {
    const enhancements = {};
    if (args.lighting) enhancements.lighting = args.lighting;
    if (args.camera) enhancements.camera = args.camera;
    if (args.mood) enhancements.mood = args.mood;
    if (args.technical) enhancements.technical = args.technical;

    enhancedPrompts = prompts.map(p => ({
      ...p,
      prompt: enhancePrompt(p.prompt, enhancements)
    }));
  }

  // Display results
  enhancedPrompts.forEach((p, index) => {
    console.log(`\n${colors.bright}${colors.cyan}[${index + 1}] ${p.style}${colors.reset}`);
    console.log(`  ${colors.dim}Category: ${p.category}${colors.reset}`);
    console.log(`  ${colors.white}Prompt: ${colors.reset}${p.prompt}`);
  });

  // Save if requested
  if (args.output) {
    savePrompts(enhancedPrompts, args.output);
  }

  // Generate video if requested
  if (args.generateVideo) {
    console.log();
    printInfo(`Generating video with Grok Imagine API...\n`);

    try {
      await generateVideoWithGrok(enhancedPrompts[0].prompt, {
        duration: parseInt(args.duration) || 5,
        aspectRatio: args.aspectRatio || '16:9',
        resolution: args.resolution || '720p'
      });
    } catch (error) {
      printError(`Video generation failed: ${error.message}`);
      process.exit(1);
    }
  }
}

// Main function
async function main() {
  // Parse command line arguments
  const args = parseArgs(process.argv.slice(2));

  if (args.interactive || process.argv.length === 2) {
    // Interactive mode
    await interactiveMode();
  } else {
    // Command line mode
    await commandLineMode(args);
  }
}

// Simple argument parser
function parseArgs(argv) {
  const args = {
    _: []
  };

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];

    switch (arg) {
      case '--interactive':
      case '-i':
        args.interactive = true;
        break;
      case '--topic':
      case '-t':
        args.topic = argv[++i];
        break;
      case '--style':
      case '-s':
        args.style = argv[++i];
        break;
      case '--categories':
      case '-c':
        args.categories = argv[++i];
        break;
      case '--all':
      case '-a':
        args.all = true;
        break;
      case '--variants':
      case '-n':
        args.variants = parseInt(argv[++i]);
        break;
      case '--lighting':
        args.lighting = argv[++i];
        break;
      case '--camera':
        args.camera = argv[++i];
        break;
      case '--mood':
        args.mood = argv[++i];
        break;
      case '--technical':
        args.technical = argv[++i];
        break;
      case '--duration':
        args.duration = parseInt(argv[++i]);
        break;
      case '--aspect-ratio':
        args.aspectRatio = argv[++i];
        break;
      case '--resolution':
        args.resolution = argv[++i];
        break;
      case '--generate-video':
      case '-g':
        args.generateVideo = true;
        break;
      case '--output':
      case '-o':
        args.output = argv[++i];
        break;
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
        break;
      default:
        if (!arg.startsWith('--')) {
          args._.push(arg);
        }
    }
  }

  return args;
}

// Print help
function printHelp() {
  console.log(`
${colors.bright}Video Prompt Generator - Generate high-quality video prompts${colors.reset}

${colors.cyan}Usage:${colors.reset}
  node generate.js [options]

${colors.cyan}Interactive Mode:${colors.reset}
  node generate.js

${colors.cyan}Command Line Options:${colors.reset}
  --topic, -t <topic>        Video topic (required)
  --style, -s <style>        Specific style
  --categories, -c <list>      Comma-separated categories
  --all, -a                   Generate all categories
  --variants, -n <num>        Generate N variants
  --lighting <text>            Add lighting enhancement
  --camera <text>              Add camera movement
  --mood <text>               Add mood
  --technical <text>            Add technical specs
  --duration <seconds>          Video duration (1-15)
  --aspect-ratio <ratio>        Aspect ratio (16:9, 4:3, 1:1)
  --resolution <res>            Resolution (720p, 480p)
  --generate-video, -g         Generate video with Grok Imagine
  --output, -o <file>         Save to file
  --interactive, -i             Interactive mode
  --help, -h                   Show this help

${colors.cyan}Examples:${colors.reset}
  # Generate all prompts for a topic
  node generate.js --topic "cat playing" --all

  # Generate for specific categories
  node generate.js --topic "sunset" --categories "landscape,product"

  # Generate with enhancements
  node generate.js --topic "product showcase" --lighting "golden hour" --camera "slow zoom"

  # Generate video with Grok Imagine
  node generate.js --topic "cat playing" --style "Serene Mountain Sunrise" --generate-video --duration 10

${colors.cyan}Categories:${colors.reset}
  landscape, product, tech, emotional, urban, food, sports, ancient, anime, abstract

${colors.cyan}Video API:${colors.reset}
  Requires: XAI_API_KEY environment variable
  Uses: Grok Imagine API (xAI)
`);
}

// ====== API Server for Web Interface ======

/**
 * Start HTTP server for video generation API
 */
function startApiServer(port = 3000) {
  const server = http.createServer(async (req, res) => {
    // Parse URL
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;

    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    // Handle OPTIONS
    if (req.method === 'OPTIONS') {
      res.writeHead(200);
      res.end();
      return;
    }

    // Route: /api/generate-video
    if (pathname === '/api/generate-video' && req.method === 'POST') {
      try {
        let body = '';
        req.on('data', chunk => {
          body += chunk.toString();
        });

        req.on('end', async () => {
          try {
            const { prompt, duration = 5, aspectRatio = '16:9', resolution = '720p' } = JSON.parse(body);

            printInfo(`API Request: Generate video`);
            printInfo(`Prompt: ${prompt.substring(0, 100)}...`);
            printInfo(`Duration: ${duration}s, Aspect Ratio: ${aspectRatio}, Resolution: ${resolution}`);

            // Call Grok Imagine API
            const result = await generateVideoWithGrok(prompt, {
              duration: parseInt(duration),
              aspectRatio,
              resolution
            });

            if (result.success) {
              res.writeHead(200, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify(result));
            } else {
              res.writeHead(500, { 'Content-Type': 'application/json' });
              res.end(JSON.stringify({ error: 'Video generation failed', details: result }));
            }
          } catch (error) {
            printError(`API Error: ${error.message}`);
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: error.message }));
          }
        });
      } catch (error) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: error.message }));
      }
    }
    // Route: /api/status
    else if (pathname === '/api/status' && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        status: 'running',
        service: 'Video Prompt Generator API',
        version: '2.0.0',
        features: ['prompt-generation', 'video-generation', 'history', 'search', 'export']
      }));
    }
    // 404
    else {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Not found' }));
    }
  });

  server.listen(port, () => {
    console.log(`\n${colors.green}✓ API Server running on port ${port}${colors.reset}`);
    console.log(`${colors.cyan}ℹ Endpoints:${colors.reset}`);
    console.log(`  POST /api/generate-video - Generate video`);
    console.log(`  GET  /api/status        - Service status`);
    console.log(`\n${colors.dim}Press Ctrl+C to stop server${colors.reset}\n`);
  });

  return server;
}

// ====== Export Functions for Web Interface ======

/**
 * Export history to JSON
 */
function exportHistoryToJson(historyData) {
  return JSON.stringify({
    exportedAt: new Date().toISOString(),
    recordCount: historyData.length,
    history: historyData
  }, null, 2);
}

/**
 * Export history to Markdown
 */
function exportHistoryToMarkdown(historyData) {
  let markdown = `# 视频提示词历史记录\n\n`;
  markdown += `**导出时间**: ${new Date().toLocaleString('zh-CN')}\n`;
  markdown += `**记录数量**: ${historyData.length}\n\n`;
  markdown += `---\n\n`;

  historyData.forEach((record, recordIndex) => {
    markdown += `## 记录 ${recordIndex + 1}: ${record.topic}\n\n`;
    markdown += `**生成时间**: ${new Date(record.timestamp).toLocaleString('zh-CN')}\n`;
    markdown += `**提示词数量**: ${record.promptCount}\n`;
    markdown += `**分类**: ${record.categories.join(', ')}\n\n`;

    record.prompts.forEach((prompt) => {
      markdown += `### ${prompt.style} ${prompt.emoji}\n\n`;
      markdown += `**分类**: ${prompt.category}\n\n`;
      markdown += `\`\`\`\n${prompt.prompt}\n\`\`\`\n\n`;
    });

    markdown += `---\n\n`;
  });

  return markdown;
}

/**
 * Export current prompts to JSON
 */
function exportPromptsToJson(prompts, topic) {
  return JSON.stringify({
    topic: topic,
    generatedAt: new Date().toISOString(),
    promptCount: prompts.length,
    prompts: prompts
  }, null, 2);
}

/**
 * Export current prompts to Markdown
 */
function exportPromptsToMarkdown(prompts, topic) {
  let markdown = `# 视频提示词\n\n`;
  markdown += `**主题**: ${topic}\n`;
  markdown += `**生成时间**: ${new Date().toLocaleString('zh-CN')}\n`;
  markdown += `**提示词数量**: ${prompts.length}\n\n`;
  markdown += `---\n\n`;

  prompts.forEach((prompt, index) => {
    markdown += `## ${index + 1}. ${prompt.style} ${prompt.emoji}\n\n`;
    markdown += `**分类**: ${prompt.category}\n\n`;
    markdown += `**提示词**:\n\n`;
    markdown += `\`\`\`\n${prompt.prompt}\n\`\`\`\n\n`;
    markdown += `---\n\n`;
  });

  return markdown;
}

// ====== CLI: Server Command ======

// Check if --server flag is present
if (process.argv.includes('--server') || process.argv.includes('-s')) {
  const portIndex = process.argv.indexOf('--port') !== -1 ? process.argv.indexOf('--port') + 1 : -1;
  const port = portIndex !== -1 ? parseInt(process.argv[portIndex]) : 3000;

  startApiServer(port);
  process.exit(0);
}

// Run main
main().catch(error => {
  printError(error.message);
  process.exit(1);
});
