#!/usr/bin/env node

/**
 * AI 内容文档生成器
 * 从抓取的 Tweets 生成 Markdown 文档
 */

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = path.join(__dirname, '..');
const DATA_DIR = path.join(SCRIPT_DIR, 'data');
const DOCS_DIR = path.join(SCRIPT_DIR, 'docs');
const CONFIG_FILE = path.join(SCRIPT_DIR, 'config.json');

const TODAY = new Date().toISOString().split('T')[0];

// 创建目录
[DATA_DIR, DOCS_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

console.log('📝 生成 AI 玩法内容文档...\n');

// 读取配置
let config = {};
try {
    config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
} catch (error) {
    console.error('❌ 配置文件读取失败:', error.message);
    process.exit(1);
}

// 扫描数据目录
const dataFiles = fs.readdirSync(DATA_DIR)
    .filter(file => file.startsWith('tweets_') && file.endsWith('.json'))
    .sort()
    .reverse();

console.log(`📂 找到 ${dataFiles.length} 个数据文件\n`);

if (dataFiles.length === 0) {
    console.log('⚠️  没有找到数据文件');
    process.exit(0);
}

// 合并所有数据
const allTweets = [];

dataFiles.forEach(file => {
    try {
        const filePath = path.join(DATA_DIR, file);
        const content = fs.readFileSync(filePath, 'utf-8');
        const tweets = JSON.parse(content);

        if (Array.isArray(tweets)) {
            allTweets.push(...tweets);
        }
    } catch (error) {
        console.error(`⚠️  无法解析文件: ${file}`, error.message);
    }
});

console.log(`✅ 共 ${allTweets.length} 条推文\n`);

// 生成 Markdown 文档
const markdown = generateMarkdown(allTweets);

// 保存文档
const outputFile = path.join(DOCS_DIR, `ai-content-${TODAY}.md`);
fs.writeFileSync(outputFile, markdown, 'utf-8');

console.log(`✅ 文档已生成: ${outputFile}\n`);
console.log(`📊 统计:`);
console.log(`   - 总推文数: ${allTweets.length}`);
console.log(`   - 数据文件数: ${dataFiles.length}`);
console.log(`   - 生成时间: ${TODAY}\n`);

function generateMarkdown(tweets) {
    const now = new Date();
    const dateStr = now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
    });

    let md = `# AI 玩法内容汇总 🤖

> 自动抓取和汇总 AI 玩法相关内容

**更新时间**: ${dateStr}  
**推文数量**: ${tweets.length} 条

---

## 📊 统计信息

- 📅 抓取日期: ${TODAY}
- 🐦 来源: X (Twitter)
- 🔍 搜索主题: AI工具、AI玩法、ChatGPT技巧等
- 📊 推文总数: ${tweets.length}

---

## 🔥 热门内容

`;

    // 按热度排序
    const sortedTweets = tweets.sort((a, b) => {
        const likesA = a.favorite_count || 0;
        const likesB = b.favorite_count || 0;
        return likesB - likesA;
    });

    // Top 10
    md += `### Top 10 最受欢迎

`;

    sortedTweets.slice(0, 10).forEach((tweet, index) => {
        md += `${index + 1}. ${formatTweet(tweet)}\n\n`;
    });

    // 分类展示
    md += `---

## 📂 内容分类

`;

    const categories = categorizeTweets(tweets);

    Object.entries(categories).forEach(([category, categoryTweets]) => {
        md += `### ${category} (${categoryTweets.length})\n\n`;

        categoryTweets.slice(0, 5).forEach(tweet => {
            md += `- ${formatTweet(tweet)}\n\n`;
        });

        if (categoryTweets.length > 5) {
            md += `_还有 ${categoryTweets.length - 5} 条..._\n\n`;
        }
    });

    // 工具汇总
    md += `---

## 🛠️ 提及的工具

`;

    const tools = extractTools(tweets);
    tools.slice(0, 20).forEach((tool, index) => {
        md += `${index + 1}. ${tool}\n`;
    });

    // 媒体清单
    md += `---

## 📹 媒体清单

`;

    const media = extractMedia(tweets);
    media.forEach(item => {
        md += `- ${item}\n`;
    });

    // 页脚
    md += `---

## 📝 说明

- 本文档由自动化系统生成
- 数据来源: X (Twitter)
- 更新频率: 每日
- 内容基于关键词搜索，可能包含不相关信息

## 🔗 相关资源

- [Ultimate Skills Bundle](https://github.com/hhhh124hhhh/ultimate-skills-bundle)
- [AI 工具列表](https://github.com/steipete/awesome-ai-tools)
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

---

*由 [Clawdbot](https://clawd.bot) 自动生成* 🤖
`;

    return md;
}

function formatTweet(tweet) {
    const author = tweet.author?.screen_name || 'unknown';
    const text = tweet.text || tweet.full_text || '';
    const url = `https://x.com/${author}/status/${tweet.id_str}`;
    const likes = tweet.favorite_count || 0;
    const retweets = tweet.retweet_count || 0;

    return `[@${author}](${url}) "${text}"` +
           `\n   👍 ${likes} · 🔄 ${retweets}`;
}

function categorizeTweets(tweets) {
    const categories = {
        'AI工具提示': [],
        '使用技巧': [],
        '工具推荐': [],
        '新闻动态': [],
        '其他': []
    };

    tweets.forEach(tweet => {
        const text = (tweet.text || tweet.full_text || '').toLowerCase();

        if (text.includes('工具') || text.includes('tool')) {
            categories['工具推荐'].push(tweet);
        } else if (text.includes('技巧') || text.includes('tip') || text.includes('技巧')) {
            categories['使用技巧'].push(tweet);
        } else if (text.includes('提示词') || text.includes('prompt')) {
            categories['AI工具提示'].push(tweet);
        } else if (text.includes('新') || text.includes('发布') || text.includes('发布')) {
            categories['新闻动态'].push(tweet);
        } else {
            categories['其他'].push(tweet);
        }
    });

    return categories;
}

function extractTools(tweets) {
    const tools = new Set();

    tweets.forEach(tweet => {
        const text = tweet.text || tweet.full_text || '';

        // 提取 @mentions
        const mentions = text.match(/@(\w+)/g) || [];
        mentions.forEach(m => {
            const tool = m.replace('@', '');
            if (tool !== 'openai' && tool !== 'chatgpt') {
                tools.add(tool);
            }
        });
    });

    return Array.from(tools);
}

function extractMedia(tweets) {
    const media = [];

    tweets.forEach(tweet => {
        if (tweet.entities?.media) {
            tweet.entities.media.forEach(m => {
                media.push(m.display_url || m.expanded_url || '视频/图片');
            });
        }
    });

    return [...new Set(media)];
}
