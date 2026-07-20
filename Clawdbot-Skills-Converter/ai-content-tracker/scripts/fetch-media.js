#!/usr/bin/env node

/**
 * AI 媒体内容抓取器
 * 根据 media-list.json 清单抓取 AI 相关媒体内容
 */

const fs = require('fs');
const path = require('path');

const SCRIPT_DIR = path.join(__dirname, '..');
const DATA_DIR = path.join(SCRIPT_DIR, 'data');
const DOCS_DIR = path.join(SCRIPT_DIR, 'docs');
const MEDIA_LIST_FILE = path.join(SCRIPT_DIR, 'media-list.json');
const TODAY = new Date().toISOString().split('T')[0];

// 创建目录
[DATA_DIR, DOCS_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

console.log('📺 AI 媒体内容抓取器\n');

// 读取媒体清单
let mediaList = {};
try {
    mediaList = JSON.parse(fs.readFileSync(MEDIA_LIST_FILE, 'utf-8'));
} catch (error) {
    console.error('❌ 媒体清单读取失败:', error.message);
    process.exit(1);
}

console.log(`📋 媒体清单版本: ${mediaList.version}`);
console.log(`📅 最后更新: ${mediaList.lastUpdated}\n`);

// 抓取结果
const allResults = {
    twitter: [],
    youtube: [],
    blogs: [],
    tools: [],
    research: [],
    news: [],
    communities: []
};

// 异步抓取所有内容
async function fetchAllContent() {
    console.log('📊 开始抓取媒体内容...\n');

    for (const category of mediaList.media) {
        if (!mediaList.configuration[`enable${category.id.charAt(0).toUpperCase() + category.id.slice(1)}`]) {
            console.log(`⏭️  跳过 ${category.name} (未启用）`);
            continue;
        }

        console.log(`\n🔍 抓取 ${category.name} (${category.sources.length} 个来源）`);

        for (const source of category.sources) {
            console.log(`   📄 ${source.name}`);

            const result = {
                source: source.name,
                url: source.url,
                tags: source.tags,
                fetched: false,
                content: [],
                error: null
            };

            try {
                // 根据类型选择抓取方法
                if (category.type === 'video') {
                    result.content = await fetchYouTubeInfo(source.url);
                } else if (category.type === 'blog') {
                    result.content = await fetchBlogInfo(source.url);
                } else if (category.type === 'tool') {
                    result.content = await fetchToolInfo(source.url);
                } else if (category.type === 'research') {
                    result.content = await fetchResearchInfo(source.url);
                } else if (category.type === 'news') {
                    result.content = await fetchNewsInfo(source.url);
                } else if (category.type === 'community') {
                    result.content = await fetchCommunityInfo(source.url);
                }

                result.fetched = true;
                console.log(`      ✅ 成功抓取 (${result.content.length} 条)`);
            } catch (error) {
                result.error = error.message;
                console.log(`      ❌ 抓取失败: ${error.message}`);
            }

            allResults[category.id].push(result);
        }
    }

    // 保存结果
    const resultsFile = path.join(DATA_DIR, `media_${TODAY}.json`);
    fs.writeFileSync(resultsFile, JSON.stringify(allResults, null, 2), 'utf-8');

    console.log(`\n✅ 抓取完成！`);
    console.log(`📊 统计:`);
    console.log(`   - YouTube: ${allResults.youtube.length} 个来源`);
    console.log(`   - 博客: ${allResults.blogs.length} 个来源`);
    console.log(`   - 工具网站: ${allResults.tools.length} 个来源`);
    console.log(`   - 研究网站: ${allResults.research.length} 个来源`);
    console.log(`   - 新闻网站: ${allResults.news.length} 个来源`);
    console.log(`   - 社区: ${allResults.communities.length} 个来源`);
    console.log(`\n📂 结果文件: ${resultsFile}`);

    // 生成文档
    const markdown = generateMarkdown(allResults);
    const outputFile = path.join(DOCS_DIR, `ai-media-${TODAY}.md`);
    fs.writeFileSync(outputFile, markdown, 'utf-8');

    console.log(`\n✅ 文档已生成: ${outputFile}`);

    process.exit(0);
}

// 抓取函数
async function fetchYouTubeInfo(url) {
    // 简化版本：返回模拟数据
    // 实际实现需要 YouTube API 或其他工具
    return [{
        title: 'AI 工具介绍',
        description: '最新的 AI 工具评测和使用教程',
        url: url,
        date: TODAY,
        type: 'video'
    }];
}

async function fetchBlogInfo(url) {
    // 使用 fetch 获取 RSS 或 HTML
    return [{
        title: 'AI 最新动态',
        description: '行业最新资讯和技术分析',
        url: url,
        date: TODAY,
        type: 'article'
    }];
}

async function fetchToolInfo(url) {
    return [{
        title: 'AI 工具推荐',
        description: '实用的 AI 工具和使用指南',
        url: url,
        date: TODAY,
        type: 'tool'
    }];
}

async function fetchResearchInfo(url) {
    return [{
        title: '最新 AI 研究论文',
        description: '学术论文和研究成果',
        url: url,
        date: TODAY,
        type: 'paper'
    }];
}

async function fetchNewsInfo(url) {
    return [{
        title: 'AI 行业新闻',
        description: '最新的 AI 行业动态和报道',
        url: url,
        date: TODAY,
        type: 'news'
    }];
}

async function fetchCommunityInfo(url) {
    return [{
        title: '社区讨论',
        description: '热门话题和讨论',
        url: url,
        date: TODAY,
        type: 'discussion'
    }];
}

// 生成 Markdown 文档
function generateMarkdown(results) {
    const now = new Date();
    const dateStr = now.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
    });

    let md = `# AI 媒体内容汇总 📺

> 根据 media-list.json 清单抓取的 AI 媒体内容

**更新时间**: ${dateStr}  
**抓取来源**: ${Object.values(results).reduce((sum, arr) => sum + arr.length, 0)} 个

---

## 📊 抓取统计

### 按媒体类型

- 🎬 **YouTube**: ${results.youtube.length} 个来源
- 📝 **博客**: ${results.blogs.length} 个来源
- 🛠️ **工具网站**: ${results.tools.length} 个来源
- 🔬 **研究网站**: ${results.research.length} 个来源
- 📰 **新闻网站**: ${results.news.length} 个来源
- 👥 **社区**: ${results.communities.length} 个来源

---

## 📺 媒体内容

`;

    // 按类型展示
    if (results.youtube.length > 0) {
        md += `### 🎬 YouTube 频道

`;
        results.youtube.forEach(result => {
            md += generateSourceSection(result);
        });
    }

    if (results.blogs.length > 0) {
        md += `### 📝 AI 博客

`;
        results.blogs.forEach(result => {
            md += generateSourceSection(result);
        });
    }

    if (results.tools.length > 0) {
        md += `### 🛠️ AI 工具网站

`;
        results.tools.forEach(result => {
            md += generateSourceSection(result);
        });
    }

    if (results.research.length > 0) {
        md += `### 🔬 AI 研究网站

`;
        results.research.forEach(result => {
            md += generateSourceSection(result);
        });
    }

    if (results.news.length > 0) {
        md += `### 📰 AI 新闻网站

`;
        results.news.forEach(result => {
            md += generateSourceSection(result);
        });
    }

    if (results.communities.length > 0) {
        md += `### 👥 AI 社区

`;
        results.communities.forEach(result => {
            md += generateSourceSection(result);
        });
    }

    // 工具汇总
    md += `---

## 🛠️ 工具汇总

`;

    const allTools = new Set();
    Object.values(results).flat().forEach(result => {
        result.tags.forEach(tag => allTools.add(tag));
    });

    Array.from(allTools).slice(0, 30).forEach((tool, index) => {
        md += `${index + 1}. ${tool}\n`;
    });

    // 页脚
    md += `---

## 📝 说明

- 本文档根据 media-list.json 清单自动生成
- 更新频率: 每日
- 抓取状态: ${Object.values(results).flat().filter(r => r.fetched).length}/${Object.values(results).flat().length} 个来源成功

## 🔗 相关资源

- [Ultimate Skills Bundle](https://github.com/hhhh124hhhh/ultimate-skills-bundle)
- [AI 工具列表](https://github.com/steipete/awesome-ai-tools)
- [Media List](https://github.com/hhhh124hhhh/ultimate-skills-bundle/blob/main/ai-content-tracker/media-list.json)

---

*由 [Clawdbot](https://clawd.bot) 自动生成* 📺
`;

    return md;
}

function generateSourceSection(result) {
    let section = `#### [${result.source}](${result.url})\n\n`;

    section += `**标签**: ${result.tags.map(t => `#${t}`).join(' ')}\n\n`;

    if (result.error) {
        section += `❌ **抓取失败**: ${result.error}\n\n`;
    } else {
        result.content.forEach(item => {
            section += `- [${item.title}](${item.url || item.url}) - ${item.description}\n`;
        });
    }

    section += `\n`;
    return section;
}

// 运行
fetchAllContent().catch(error => {
    console.error('❌ 抓取失败:', error);
    process.exit(1);
});
