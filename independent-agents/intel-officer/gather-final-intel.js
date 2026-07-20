// Final Night Intelligence Gathering - Round 4 (with chrome-devtools)
// Technology Dynamics Deep Dive - 2026-03-18

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const OUTPUT_FILE = 'C:\\Users\\Lenovo\\.openclaw\\workspace-content\\memory\\night-intel-round4.md';
const CHROME_DEVTOOLS_PORT = 9222;

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

// Check if Chrome is available
function checkChrome() {
  try {
    const res = execSync(`powershell -Command "Invoke-RestMethod -Uri 'http://127.0.0.1:${CHROME_DEVTOOLS_PORT}/json/version' -TimeoutSec 3"`, { encoding: 'utf8' });
    return true;
  } catch (e) {
    return false;
  }
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

// Hacker News API
function fetchHackerNewsTop(limit = 20) {
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

// RSS feed parser
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

  console.log('🔍 Final Night Intelligence Gathering - Round 4...');
  console.log('📅 Date:', new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }));
  console.log('');

  const chromeAvailable = checkChrome();
  console.log(`🌐 Chrome DevTools (port ${CHROME_DEVTOOLS_PORT}): ${chromeAvailable ? '✅ Available' : '❌ Not available'}`);
  console.log('');

  // 1. OpenClaw / AI Agent Framework
  console.log('1️⃣ Fetching OpenClaw releases...');
  const openclawReleases = await fetchGitHubReleases('openclaw-ai', 'openclaw', 5);
  const feishuPluginReleases = await fetchGitHubReleases('openclaw-data', 'feishu-openclaw-plugin', 5);
  report.sections.push({
    category: 'OpenClaw / AI Agent Framework',
    items: openclawReleases.length > 0 ? openclawReleases : feishuPluginReleases.length > 0 ? feishuPluginReleases : [
      { note: 'OpenClaw 是本地运行的 AI 代理框架', url: 'https://github.com/search?q=openclaw' },
      { note: '飞书插件：feishu-openclaw-plugin', url: 'https://github.com/openclaw-data/feishu-openclaw-plugin' }
    ]
  });

  // 2. Cursor Editor
  console.log('2️⃣ Fetching Cursor Editor...');
  const cursorReleases = await fetchGitHubReleases('getcursor', 'cursor', 5);
  report.sections.push({
    category: 'Cursor Editor',
    items: cursorReleases.length > 0 ? cursorReleases : [
      { note: 'Cursor 是基于 AI 的代码编辑器', url: 'https://www.cursor.com' },
      { note: '查看更新日志', url: 'https://www.cursor.com/changelog' }
    ]
  });

  // 3. AI Models News (via RSS)
  console.log('3️⃣ Fetching AI Model news...');
  const [openaiRSS, anthropicRSS, googleAiRSS] = await Promise.all([
    fetchRSS('https://openai.com/news/feed/'),
    fetchRSS('https://www.anthropic.com/news/feed'),
    fetchRSS('https://blog.google/technology/ai/feed/')
  ]);
  
  report.sections.push({
    category: 'AI Models News (OpenAI)',
    items: openaiRSS.slice(0, 5).length > 0 ? openaiRSS.slice(0, 5) : [{ note: 'Check openai.com/news' }]
  });
  report.sections.push({
    category: 'AI Models News (Anthropic)',
    items: anthropicRSS.slice(0, 5).length > 0 ? anthropicRSS.slice(0, 5) : [{ note: 'Check anthropic.com/news' }]
  });
  report.sections.push({
    category: 'AI Models News (Google)',
    items: googleAiRSS.slice(0, 5).length > 0 ? googleAiRSS.slice(0, 5) : [{ note: 'Check blog.google/technology/ai' }]
  });

  // 4. Feishu/Lark
  console.log('4️⃣ Fetching Feishu updates...');
  report.sections.push({
    category: '飞书 (Feishu/Lark)',
    items: [
      { note: '官方更新日志', url: 'https://open.feishu.cn/document/changelog' },
      { note: '飞书博客', url: 'https://www.feishu.cn/blog' },
      { note: '飞书开放平台', url: 'https://open.feishu.cn' }
    ]
  });

  // 5. Hacker News Top AI Stories
  console.log('5️⃣ Fetching Hacker News Top Stories...');
  const hnStories = await fetchHackerNewsTop(25);
  const aiStories = hnStories
    .filter(s => s && (s.title.toLowerCase().includes('ai') || s.title.toLowerCase().includes('llm') || s.title.toLowerCase().includes('model') || s.title.toLowerCase().includes('gpt') || s.title.toLowerCase().includes('claude') || s.title.toLowerCase().includes('agent') || s.title.toLowerCase().includes('mistral') || s.title.toLowerCase().includes('openai')))
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
    items: aiStories.length > 0 ? aiStories : [{ note: 'No AI-related stories in top 25' }]
  });

  // 6. Tech News RSS
  console.log('6️⃣ Fetching Tech News RSS...');
  const [techcrunchRSS, venturebeatRSS, wiredRSS] = await Promise.all([
    fetchRSS('https://techcrunch.com/feed/'),
    fetchRSS('https://venturebeat.com/feed/'),
    fetchRSS('https://www.wired.com/feed/rss')
  ]);
  
  report.sections.push({
    category: 'TechCrunch Latest',
    items: techcrunchRSS.slice(0, 5).length > 0 ? techcrunchRSS.slice(0, 5) : [{ note: 'Check techcrunch.com' }]
  });
  report.sections.push({
    category: 'VentureBeat Latest',
    items: venturebeatRSS.slice(0, 5).length > 0 ? venturebeatRSS.slice(0, 5) : [{ note: 'Check venturebeat.com' }]
  });
  report.sections.push({
    category: 'WIRED Latest',
    items: wiredRSS.slice(0, 5).length > 0 ? wiredRSS.slice(0, 5) : [{ note: 'Check wired.com' }]
  });

  // 7. Chinese Tech Sources
  console.log('7️⃣ Fetching Chinese Tech Sources...');
  const [kr36RSS, huxiuRSS] = await Promise.all([
    fetchRSS('https://36kr.com/feed'),
    fetchRSS('https://www.huxiu.com/rss/1.xml')
  ]);
  
  report.sections.push({
    category: '36 氪 (36Kr) - 科技创投',
    items: kr36RSS.slice(0, 5).length > 0 ? kr36RSS.slice(0, 5) : [{ note: 'Check 36kr.com' }]
  });
  report.sections.push({
    category: '虎嗅 (Huxiu) - 科技评论',
    items: huxiuRSS.slice(0, 5).length > 0 ? huxiuRSS.slice(0, 5) : [{ note: 'Check huxiu.com' }]
  });

  // 8. Duozhi.com AI+ Education (retry with longer timeout)
  console.log('8️⃣ Fetching Duozhi.com (AI+ Education)...');
  try {
    const duozhiRes = await fetchUrl('https://duozhi.com', 20000);
    const headlines = [];
    const titleRegex = /<h[23][^>]*>([^<]+)<\/h[23]>/g;
    let match;
    while ((match = titleRegex.exec(duozhiRes.data)) !== null) {
      if (headlines.length < 10) headlines.push({ title: match[1].trim() });
    }
    report.sections.push({
      category: '多知网 (Duozhi) - AI+ 教育',
      items: headlines.length > 0 ? headlines : [{ note: 'Site fetched, requires JavaScript', url: 'https://duozhi.com' }]
    });
  } catch (e) {
    report.sections.push({ 
      category: '多知网 (Duozhi) - AI+ 教育',
      items: [
        { note: '网站暂时无法访问，建议稍后使用浏览器查看', url: 'https://duozhi.com' },
        { note: '重点关注：AI 技术进展、AI+ 教育融合案例' }
      ]
    });
  }

  // Generate Markdown Report
  console.log('');
  console.log('📝 Generating final report...');
  
  let md = `# 🔍 夜间情报任务 4：技术动态深挖\n\n`;
  md += `**采集时间:** ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false })}\n`;
  md += `**任务 ID:** night-intel-round4\n`;
  md += `**时区:** Asia/Shanghai\n`;
  md += `**Chrome DevTools:** ${chromeAvailable ? '✅ 可用 (端口 9222)' : '❌ 不可用'}\n\n`;
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
  md += `## 📊 本次采集总结\n\n`;
  md += `### 数据来源\n`;
  md += `- GitHub API: 官方公开 API（未认证 60 次/小时）\n`;
  md += `- Hacker News Firebase API: 官方公开 API\n`;
  md += `- RSS Feeds: OpenAI, Anthropic, Google AI, TechCrunch, VentureBeat, WIRED, 36 氪，虎嗅\n`;
  md += `- 直接 HTTP: Duozhi 等\n\n`;
  
  md += `### 限制说明\n`;
  md += `- web_search (Brave API) 未配置\n`;
  md += `- Product Hunt 等需要 JavaScript 渲染的网站数据不完整\n`;
  md += `- 需要更深度抓取时使用 chrome-devtools (端口 9222)\n\n`;
  
  md += `### 下一步建议\n`;
  md += `1. 使用 chrome-devtools 抓取 Product Hunt 每日热榜\n`;
  md += `2. 使用 chrome-devtools 抓取 Duozhi 详细内容\n`;
  md += `3. 配置 Brave API 以支持 web_search\n`;
  md += `4. 添加更多中文平台监控（微博热搜、知乎热榜、抖音热榜）\n\n`;
  
  md += `---\n*Generated by Agent-X (情报官) | Night Intel Round 4 | Final*\n`;

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
