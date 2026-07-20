// Night Intelligence Gathering Script - Round 4
// Technology Dynamics Deep Dive - 2026-03-18

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const OUTPUT_FILE = 'C:\\Users\\Lenovo\\.openclaw\\workspace-content\\memory\\night-intel-round4.md';

// Helper to fetch URL content
function fetchUrl(url, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    lib.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      },
      timeout
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data }));
    }).on('error', reject).on('timeout', () => reject(new Error('Timeout')));
  });
}

// GitHub API for releases (no auth needed for public repos)
function fetchGitHubReleases(owner, repo, limit = 5) {
  return fetchUrl(`https://api.github.com/repos/${owner}/${repo}/releases?per_page=${limit}`, 8000)
    .then(res => {
      if (res.status === 200) {
        return JSON.parse(res.data).map(r => ({
          name: r.name || r.tag_name,
          published_at: r.published_at,
          url: r.html_url,
          description: (r.body || '').split('\n')[0]?.slice(0, 200)
        }));
      }
      return [];
    });
}

// Hacker News API (official, no auth needed)
function fetchHackerNewsTop(limit = 10) {
  return fetchUrl(`https://hacker-news.firebaseio.com/v0/topstories.json`, 8000)
    .then(res => {
      const ids = JSON.parse(res.data).slice(0, limit);
      return Promise.all(ids.map(id => 
        fetchUrl(`https://hacker-news.firebaseio.com/v0/item/${id}.json`, 5000)
          .then(r => r.status === 200 ? JSON.parse(r.data) : null)
      ));
    });
}

// Product Hunt (scrape from public page)
async function fetchProductHuntTop() {
  try {
    const today = new Date();
    const dateStr = `${today.getFullYear()}/${today.getMonth()+1}/${today.getDate()}`;
    const res = await fetchUrl(`https://www.producthunt.com/leaderboard/daily/${dateStr}`, 10000);
    // Basic extraction - in production would use proper HTML parser
    return [{ note: 'Product Hunt data requires browser rendering', url: `https://www.producthunt.com/leaderboard/daily/${dateStr}` }];
  } catch (e) {
    return [{ note: 'Fetch failed: ' + e.message }];
  }
}

// Main gathering function
async function gatherIntelligence() {
  const report = {
    timestamp: new Date().toISOString(),
    timezone: 'Asia/Shanghai',
    sections: []
  };

  console.log('🔍 Starting Night Intelligence Gathering - Round 4...');
  console.log('📅 Date:', new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }));
  console.log('');

  // 1. OpenClaw / AI Agent Framework
  console.log('1️⃣ Fetching OpenClaw / AI Agent updates...');
  try {
    const openclawReleases = await fetchGitHubReleases('openclaw-ai', 'openclaw', 5);
    report.sections.push({
      category: 'OpenClaw / AI Agent Framework',
      items: openclawReleases.length > 0 ? openclawReleases : [{ note: 'No recent releases found or API rate limited' }]
    });
  } catch (e) {
    report.sections.push({ category: 'OpenClaw', items: [{ error: e.message }] });
  }

  // 2. Cursor Editor
  console.log('2️⃣ Fetching Cursor Editor updates...');
  try {
    const cursorReleases = await fetchGitHubReleases('getcursor', 'cursor', 5);
    report.sections.push({
      category: 'Cursor Editor',
      items: cursorReleases.length > 0 ? cursorReleases : [{ note: 'Check https://www.cursor.com/changelog' }]
    });
  } catch (e) {
    report.sections.push({ category: 'Cursor', items: [{ error: e.message }] });
  }

  // 3. AI Models (GPT/Claude/Gemini)
  console.log('3️⃣ Fetching AI Model updates...');
  try {
    const anthropicReleases = await fetchGitHubReleases('anthropics', 'claude-api-examples', 3);
    report.sections.push({
      category: 'AI Models (GPT/Claude/Gemini)',
      items: [
        { note: 'Check official sources:', urls: [
          'https://openai.com/news/',
          'https://www.anthropic.com/news',
          'https://blog.google/technology/ai/'
        ]}
      ]
    });
  } catch (e) {
    report.sections.push({ category: 'AI Models', items: [{ error: e.message }] });
  }

  // 4. Feishu/Lark Updates
  console.log('4️⃣ Fetching Feishu updates...');
  report.sections.push({
    category: '飞书 (Feishu/Lark)',
    items: [
      { note: 'Check official sources:', urls: [
        'https://www.feishu.cn/blog',
        'https://open.feishu.cn/document/changelog'
      ]}
    ]
  });

  // 5. Hacker News Top AI Stories
  console.log('5️⃣ Fetching Hacker News Top Stories...');
  try {
    const hnStories = await fetchHackerNewsTop(15);
    const aiStories = hnStories
      .filter(s => s && (s.title.toLowerCase().includes('ai') || s.title.toLowerCase().includes('llm') || s.title.toLowerCase().includes('model') || s.title.toLowerCase().includes('gpt') || s.title.toLowerCase().includes('claude')))
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
      category: 'Hacker News - AI Top Stories',
      items: aiStories.length > 0 ? aiStories : [{ note: 'No AI-related stories in top 15' }]
    });
  } catch (e) {
    report.sections.push({ category: 'Hacker News', items: [{ error: e.message }] });
  }

  // 6. Duozhi.com AI+ Education
  console.log('6️⃣ Fetching Duozhi.com AI+ Education...');
  try {
    const duozhiRes = await fetchUrl('https://duozhi.com', 10000);
    report.sections.push({
      category: '多知网 (Duozhi) - AI+ 教育',
      items: [{ note: 'Site fetched, requires HTML parsing for details', url: 'https://duozhi.com', status: duozhiRes.status }]
    });
  } catch (e) {
    report.sections.push({ category: 'Duozhi', items: [{ error: e.message }] });
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
        md += `- 📌 ${item.note}${item.urls ? '\n  ' + item.urls.map(u => `  - ${u}`).join('\n') : ''}\n`;
      } else if (item.error) {
        md += `- ❌ Error: ${item.error}\n`;
      } else if (item.name) {
        md += `- **${item.name}**\n`;
        md += `  - 📅 Published: ${new Date(item.published_at).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n`;
        md += `  - 🔗 [View Release](${item.url})\n`;
        if (item.description) md += `  - ${item.description}\n`;
      } else if (item.title) {
        md += `- **${item.title}**\n`;
        md += `  - 👍 ${item.points} points | 💬 ${item.comments} comments\n`;
        md += `  - 🕐 ${new Date(item.time).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n`;
        md += `  - 🔗 [Link](${item.url})\n`;
      } else if (item.url) {
        md += `- 🔗 [${item.url}](${item.url})${item.status ? ` (Status: ${item.status})` : ''}\n`;
      }
    }
    md += `\n`;
  }

  md += `---\n\n`;
  md += `## 📊 数据来源说明\n\n`;
  md += `- GitHub Releases API: 官方公开 API，无需认证\n`;
  md += `- Hacker News Firebase API: 官方公开 API\n`;
  md += `- 其他来源需浏览器自动化抓取（受限于 API 配置）\n\n`;
  md += `## ⚠️ 注意事项\n\n`;
  md += `- web_search (Brave API) 未配置，改用直接 API 调用\n`;
  md += `- 部分网站需要 JavaScript 渲染，需使用 chrome-devtools 进一步抓取\n`;
  md += `- GitHub API 有速率限制（未认证 60 次/小时）\n\n`;
  md += `---\n*Generated by Agent-X (情报官) | Night Intel Round 4*\n`;

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
