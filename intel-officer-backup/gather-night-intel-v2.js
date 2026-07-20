// Enhanced Night Intelligence Gathering - Round 4
// Technology Dynamics Deep Dive - 2026-03-18

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const OUTPUT_FILE = 'C:\\Users\\Lenovo\\.openclaw\\workspace-content\\memory\\night-intel-round4.md';

// Helper to fetch URL content
function fetchUrl(url, timeout = 10000, headers = {}) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const defaultHeaders = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      ...headers
    };
    
    lib.get(url, { headers: defaultHeaders, timeout }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data, headers: res.headers }));
    }).on('error', reject).on('timeout', () => reject(new Error('Timeout')));
  });
}

// GitHub API for releases
function fetchGitHubReleases(owner, repo, limit = 5) {
  return fetchUrl(`https://api.github.com/repos/${owner}/${repo}/releases?per_page=${limit}`, 8000, {
    'Accept': 'application/vnd.github.v3+json'
  })
  .then(res => {
    if (res.status === 200) {
      const releases = JSON.parse(res.data);
      return releases.map(r => ({
        name: r.name || r.tag_name,
        published_at: r.published_at,
        url: r.html_url,
        description: (r.body || '').split('\n')[0]?.slice(0, 200)
      }));
    }
    return [];
  })
  .catch(() => []);
}

// GitHub trending (scrape from page)
async function fetchGitHubTrending(language = '') {
  try {
    const url = language ? `https://github.com/trending/${language}?since=daily` : 'https://github.com/trending?since=daily';
    const res = await fetchUrl(url, 10000);
    // Basic HTML parsing for trending repos
    const repos = [];
    const repoRegex = /<a href="\/([^"]+)" class="text-bold">/g;
    let match;
    while ((match = repoRegex.exec(res.data)) !== null) {
      if (repos.length < 10) repos.push(match[1]);
    }
    return repos.map(r => ({ repo: r, url: `https://github.com/${r}` }));
  } catch (e) {
    return [{ note: 'Fetch failed: ' + e.message }];
  }
}

// Hacker News API
function fetchHackerNewsTop(limit = 15) {
  return fetchUrl(`https://hacker-news.firebaseio.com/v0/topstories.json`, 8000)
    .then(res => {
      const ids = JSON.parse(res.data).slice(0, limit);
      return Promise.all(ids.map(id => 
        fetchUrl(`https://hacker-news.firebaseio.com/v0/item/${id}.json`, 5000)
          .then(r => r.status === 200 ? JSON.parse(r.data) : null)
          .catch(() => null)
      ));
    });
}

// Product Hunt daily leaderboard
async function fetchProductHuntDaily() {
  try {
    const today = new Date();
    const dateStr = `${today.getFullYear()}/${today.getMonth()+1}/${today.getDate()}`;
    const res = await fetchUrl(`https://www.producthunt.com/leaderboard/daily/${dateStr}`, 12000);
    // Extract basic info from HTML
    const products = [];
    const nameRegex = /data-test="post-name">([^<]+)</g;
    let match;
    while ((match = nameRegex.exec(res.data)) !== null) {
      if (products.length < 10) products.push({ name: match[1].trim() });
    }
    return products.length > 0 ? products : [{ note: 'Requires JavaScript rendering', url: `https://www.producthunt.com/leaderboard/daily/${dateStr}` }];
  } catch (e) {
    return [{ note: 'Fetch failed: ' + e.message, url: 'https://www.producthunt.com' }];
  }
}

// RSS/Atom feed parser (basic)
function parseFeed(xml) {
  const items = [];
  const itemRegex = /<item>[\s\S]*?<\/item>/g;
  const titleRegex = /<title>([^<]+)<\/title>/;
  const linkRegex = /<link>([^<]+)<\/link>/;
  const pubDateRegex = /<pubDate>([^<]+)<\/pubDate>/;
  const descRegex = /<description>([^<]+)<\/description>/;
  
  let itemMatch;
  while ((itemMatch = itemRegex.exec(xml)) !== null) {
    const item = itemMatch[0];
    const title = titleRegex.exec(item);
    const link = linkRegex.exec(item);
    const pubDate = pubDateRegex.exec(item);
    const desc = descRegex.exec(item);
    
    if (title && link) {
      items.push({
        title: title[1],
        link: link[1],
        pubDate: pubDate ? pubDate[1] : null,
        description: desc ? desc[1].slice(0, 200) : null
      });
    }
    if (items.length >= 10) break;
  }
  return items;
}

// Fetch RSS feeds
async function fetchRSS(url) {
  try {
    const res = await fetchUrl(url, 10000);
    if (res.status === 200) return parseFeed(res.data);
    return [];
  } catch (e) {
    return [];
  }
}

// Main gathering function
async function gatherIntelligence() {
  const report = {
    timestamp: new Date().toISOString(),
    timezone: 'Asia/Shanghai',
    sections: []
  };

  console.log('🔍 Enhanced Night Intelligence Gathering - Round 4...');
  console.log('📅 Date:', new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }));
  console.log('');

  // 1. GitHub Trending (AI/ML)
  console.log('1️⃣ Fetching GitHub Trending (JavaScript/Python)...');
  const jsTrending = await fetchGitHubTrending('javascript');
  const pythonTrending = await fetchGitHubTrending('python');
  report.sections.push({
    category: 'GitHub Trending - JavaScript',
    items: jsTrending
  });
  report.sections.push({
    category: 'GitHub Trending - Python',
    items: pythonTrending
  });

  // 2. OpenClaw / AI Agent Framework
  console.log('2️⃣ Fetching OpenClaw releases...');
  const openclawReleases = await fetchGitHubReleases('openclaw-ai', 'openclaw', 5);
  const openclawDataReleases = await fetchGitHubReleases('openclaw-data', 'feishu-openclaw-plugin', 5);
  report.sections.push({
    category: 'OpenClaw / AI Agent Framework',
    items: openclawReleases.length > 0 ? openclawReleases : openclawDataReleases.length > 0 ? openclawDataReleases : [{ note: 'Check GitHub directly', url: 'https://github.com/search?q=openclaw' }]
  });

  // 3. Cursor Editor
  console.log('3️⃣ Fetching Cursor Editor...');
  const cursorReleases = await fetchGitHubReleases('getcursor', 'cursor', 5);
  report.sections.push({
    category: 'Cursor Editor',
    items: cursorReleases.length > 0 ? cursorReleases : [{ note: 'Check changelog', url: 'https://www.cursor.com/changelog' }]
  });

  // 4. AI Models News (via RSS)
  console.log('4️⃣ Fetching AI Model news...');
  const openaiRSS = await fetchRSS('https://openai.com/news/feed/');
  const anthropicNews = await fetchRSS('https://www.anthropic.com/news/feed');
  report.sections.push({
    category: 'AI Models News (OpenAI)',
    items: openaiRSS.length > 0 ? openaiRSS : [{ note: 'Check openai.com/news' }]
  });
  report.sections.push({
    category: 'AI Models News (Anthropic)',
    items: anthropicNews.length > 0 ? anthropicNews : [{ note: 'Check anthropic.com/news' }]
  });

  // 5. Feishu/Lark
  console.log('5️⃣ Fetching Feishu updates...');
  report.sections.push({
    category: '飞书 (Feishu/Lark)',
    items: [
      { note: '官方更新日志', url: 'https://open.feishu.cn/document/changelog' },
      { note: '飞书博客', url: 'https://www.feishu.cn/blog' }
    ]
  });

  // 6. Hacker News Top AI Stories
  console.log('6️⃣ Fetching Hacker News Top Stories...');
  const hnStories = await fetchHackerNewsTop(20);
  const aiStories = hnStories
    .filter(s => s && (s.title.toLowerCase().includes('ai') || s.title.toLowerCase().includes('llm') || s.title.toLowerCase().includes('model') || s.title.toLowerCase().includes('gpt') || s.title.toLowerCase().includes('claude') || s.title.toLowerCase().includes('agent')))
    .slice(0, 10)
    .map(s => ({
      title: s.title,
      points: s.score,
      comments: s.descendants || 0,
      url: s.url || `https://news.ycombinator.com/item?id=${s.id}`,
      by: s.by,
      time: new Date(s.time * 1000).toISOString()
    }));
  report.sections.push({
    category: 'Hacker News - AI/Agent Top Stories',
    items: aiStories.length > 0 ? aiStories : [{ note: 'No AI-related stories in top 20' }]
  });

  // 7. Product Hunt Daily
  console.log('7️⃣ Fetching Product Hunt Daily...');
  const phProducts = await fetchProductHuntDaily();
  report.sections.push({
    category: 'Product Hunt - Daily Top Products',
    items: phProducts
  });

  // 8. Tech News RSS
  console.log('8️⃣ Fetching Tech News RSS...');
  const techcrunchRSS = await fetchRSS('https://techcrunch.com/feed/');
  const venturebeatRSS = await fetchRSS('https://venturebeat.com/feed/');
  report.sections.push({
    category: 'TechCrunch Latest',
    items: techcrunchRSS.slice(0, 5).length > 0 ? techcrunchRSS.slice(0, 5) : [{ note: 'Check techcrunch.com' }]
  });
  report.sections.push({
    category: 'VentureBeat Latest',
    items: venturebeatRSS.slice(0, 5).length > 0 ? venturebeatRSS.slice(0, 5) : [{ note: 'Check venturebeat.com' }]
  });

  // 9. Duozhi.com AI+ Education
  console.log('9️⃣ Fetching Duozhi.com...');
  try {
    const duozhiRes = await fetchUrl('https://duozhi.com', 15000);
    // Extract headlines
    const headlines = [];
    const titleRegex = /<h[23][^>]*>([^<]+)<\/h[23]>/g;
    let match;
    while ((match = titleRegex.exec(duozhiRes.data)) !== null) {
      if (headlines.length < 10) headlines.push({ title: match[1].trim() });
    }
    report.sections.push({
      category: '多知网 (Duozhi) - AI+ 教育',
      items: headlines.length > 0 ? headlines : [{ note: 'Site fetched, requires deeper parsing', url: 'https://duozhi.com' }]
    });
  } catch (e) {
    report.sections.push({ category: 'Duozhi', items: [{ error: e.message, url: 'https://duozhi.com' }] });
  }

  // Generate Markdown Report
  console.log('');
  console.log('📝 Generating report...');
  
  let md = `# 🔍 夜间情报任务 4：技术动态深挖\n\n`;
  md += `**采集时间:** ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false })}\n`;
  md += `**任务 ID:** night-intel-round4\n`;
  md += `**时区:** Asia/Shanghai\n\n`;
  md += `---\n\n`;

  for (const section of report.sections) {
    md += `## ${section.category}\n\n`;
    for (const item of section.items) {
      if (item.note) {
        md += `- 📌 ${item.note}${item.url ? ` - [Link](${item.url})` : ''}\n`;
      } else if (item.error) {
        md += `- ❌ Error: ${item.error}${item.url ? ` - [Link](${item.url})` : ''}\n`;
      } else if (item.name) {
        md += `- **${item.name}**\n`;
        if (item.published_at) md += `  - 📅 Published: ${new Date(item.published_at).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n`;
        if (item.url) md += `  - 🔗 [View](${item.url})\n`;
        if (item.description) md += `  - ${item.description}\n`;
      } else if (item.title) {
        md += `- **${item.title}**\n`;
        if (item.points !== undefined) md += `  - 👍 ${item.points} points | 💬 ${item.comments} comments\n`;
        if (item.pubDate) md += `  - 📅 ${new Date(item.pubDate).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n`;
        if (item.time) md += `  - 🕐 ${new Date(item.time).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n`;
        if (item.link || item.url) md += `  - 🔗 [Link](${item.link || item.url})\n`;
        if (item.description) md += `  - ${item.description}\n`;
      } else if (item.repo) {
        md += `- **${item.repo}** - [View on GitHub](${item.url})\n`;
      } else if (item.url) {
        md += `- 🔗 [${item.url}](${item.url})\n`;
      }
    }
    md += `\n`;
  }

  md += `---\n\n`;
  md += `## 📊 数据来源说明\n\n`;
  md += `- GitHub API: 官方公开 API（未认证 60 次/小时限制）\n`;
  md += `- Hacker News Firebase API: 官方公开 API\n`;
  md += `- RSS Feeds: 各官方站点公开订阅源\n`;
  md += `- 直接 HTTP 抓取：Product Hunt, Duozhi 等\n\n`;
  md += `## ⚠️ 注意事项\n\n`;
  md += `- web_search (Brave API) 未配置，改用直接 API 调用和 RSS\n`;
  md += `- 部分网站需要 JavaScript 渲染，数据可能不完整\n`;
  md += `- 需要更深度抓取时使用 chrome-devtools (端口 9222)\n\n`;
  md += `---\n*Generated by Agent-X (情报官) | Night Intel Round 4 | Enhanced*\n`;

  // Ensure directory exists
  const dir = path.dirname(OUTPUT_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Write report
  fs.writeFileSync(OUTPUT_FILE, md, 'utf8');
  console.log(`✅ Report saved to: ${OUTPUT_FILE}`);
  console.log('');
  console.log(md);
  
  return report;
}

// Run
gatherIntelligence().catch(console.error);
