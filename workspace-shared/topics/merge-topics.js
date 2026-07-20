#!/usr/bin/env node
/**
 * merge-topics.js
 * 合并 local 和 cloud 选题池为统一版
 *
 * 读取: topics-pool-local-*.md, topics-pool-cloud-*.md
 *       (兼容固定名: topics-pool-local.md, topics-pool-cloud.md)
 * 输出: topics-pool.md (合并后统一版)
 *
 * 合并规则:
 * - 保留所有选题（去重 by 标题）
 * - 按综合评分排序
 * - 标记来源 (local/cloud)
 */

const fs = require('fs');
const path = require('path');

const REPO_DIR = __dirname;

function glob(pattern) {
  const files = fs.readdirSync(REPO_DIR)
    .filter(f => fs.statSync(path.join(REPO_DIR, f)).isFile())
    .filter(f => {
      const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
      return regex.test(f);
    })
    .map(f => path.join(REPO_DIR, f));
  return files;
}

function extractTopics(content, source) {
  const results = [];
  const seen = new Set();

  function addTopic(title, score, topicSource, raw) {
    if (title && !seen.has(title)) {
      seen.add(title);
      results.push({ title: title.trim(), score, source: topicSource, heat: '', collectTime: '', keywords: '', angles: '', status: '', raw: raw.trim(), poolSource: source });
    }
  }

  // 格式 1: ### 选题 1️⃣：标题（兼容旧格式）
  const oldRegex = /### 选题 [1-9]️⃣[：:]\s*(.+)/g;
  let match;
  while ((match = oldRegex.exec(content)) !== null) {
    const scoreMatch = content.substring(match.index).match(/\*\*综合评分:\*\*\s*([\d.]+)\/10/);
    const title = match[1].trim();
    const score = scoreMatch ? parseFloat(scoreMatch[1]) : 7;
    addTopic(title, score, '知乎/微博/百度/HN', match[0]);
  }

  // 格式 2: ### 序号. 标题（topics-pool-20260401-0832.md 格式，支持 1-99）
  const numTitleRegex = /###\s+\d+[.]\s+(.+)/g;
  while ((match = numTitleRegex.exec(content)) !== null) {
    const title = match[1].replace(/[🚀🔍💡📊🌍⚡🔐🏢📱💹]+/g, '').trim();
    if (title && !title.includes('精选') && !title.includes('数据快照') && !title.includes('标签分类')) {
      addTopic(title, 7, '知乎/微博/百度/HN', match[0]);
    }
  }

  // 格式 3: 1. [标题](链接) - **平台** (AI: 分数, 质量：+分数)（pipeline.py 格式）
  const linkRegex = /[1-9]+[.]\s+\[([^\]]+)\]\([^)]+\)\s*-\s*\*\*([^*]+)\*\*/g;
  while ((match = linkRegex.exec(content)) !== null) {
    const title = match[1].trim();
    const platform = match[2].trim();
    const aiMatch = content.substring(match.index).match(/AI:\s*([\d.]+)/);
    const qualityMatch = content.substring(match.index).match(/质量[：:]([+-]?\d+)/);
    let score = 5;
    if (aiMatch && qualityMatch) {
      score = Math.min(10, Math.max(0, (parseFloat(aiMatch[1]) * 10 + parseInt(qualityMatch[1])) / 2));
    } else if (aiMatch) {
      score = parseFloat(aiMatch[1]) * 10;
    }
    addTopic(title, score, platform, match[0]);
  }

  // 格式 4: 🔴 **[HN]** 标题 或 1. 🔴 标题（topics-pool-cloud 格式）
  const emojiTitleRegex = /(?:[1-9]+[.]\s+)?[\u{1F300}-\u{1F9FF}]\s*\*\*\[[^\]]+\]\*\*\s*([^\n-](?:[^\n-]*(?:\n\s*-\s*[^\n]+)?)*)/gu;
  while ((match = emojiTitleRegex.exec(content)) !== null) {
    const title = match[1].replace(/\n\s*-\s*/g, ' ').replace(/[*🔴🟢🟡\[\]]/g, '').trim();
    if (title && title.length > 3) {
      const platformMatch = content.substring(match.index).match(/\*\*\[([^\]]+)\]\*\*/);
      const platform = platformMatch ? platformMatch[1] : 'HN';
      addTopic(title, 7, platform, match[0]);
    }
  }

  // 格式 5: 仅标题行（1. 标题 - **平台** 无链接）
  const simpleRegex = /^[1-9]+[.]\s+([^-\[\]]+?)\s*-\s*\*\*([^*]+)\*\*\s*$/gm;
  while ((match = simpleRegex.exec(content)) !== null) {
    const title = match[1].replace(/[🚀🔍💡📊🌍⚡🔐🏢📱💹]/g, '').trim();
    const platform = match[2].trim();
    if (title && title.length > 3 && !title.includes('优先级') && !title.includes('评分基准')) {
      addTopic(title, 5, platform, match[0]);
    }
  }

  return results;
}

function mergeTopics() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  const hh = String(now.getHours()).padStart(2, '0');
  const mm = String(now.getMinutes()).padStart(2, '0');
  const dateStr = `${y}${m}${d}-${hh}${mm}`;
  const outputPath = path.join(REPO_DIR, `topics-pool-merged-${dateStr}.md`);

  // 读取 local pool
  // 1. topics-pool-local.md (固定名，可能有内容)
  // 2. topics-pool-local-YYYYMMDD-HHMM.md (cloud intel-officer 输出)
  // 3. topics-pool-YYYYMMDD-HHMM.md (今日有实质内容的原始文件，需要排除 merge 输出)
  const today = `${y}${m}${d}`;
  const knownGood = [
    'topics-pool-20260401-0832.md',  // 今日 08:32 原始分析
  ];
  const localFiles = [
    ...glob('topics-pool-local-*.md').filter(f => f.includes(today)),
    path.join(REPO_DIR, 'topics-pool-local.md'),
    ...knownGood.map(f => path.join(REPO_DIR, f)).filter(f => fs.existsSync(f))
  ].filter(f => fs.existsSync(f));

  // 读取 cloud pool
  const cloudFiles = [
    ...glob('topics-pool-cloud-*.md').filter(f => f.includes(today)),
    path.join(REPO_DIR, 'topics-pool-cloud.md')
  ].filter(f => fs.existsSync(f));

  // 修复1: 校验源文件非空
  const sourceFiles = [...localFiles, ...cloudFiles].filter(f => fs.existsSync(f));
  if (sourceFiles.length === 0) {
    console.error('[ERROR] No source files found');
    process.exit(1);
  }

  // 提取所有 topics
  const allTopics = [];
  const seen = new Map();

  localFiles.forEach(f => {
    const content = fs.readFileSync(f, 'utf-8');
    extractTopics(content, 'local').forEach(t => {
      if (t.title && !seen.has(t.title)) {
        seen.set(t.title, true);
        allTopics.push(t);
      }
    });
  });

  cloudFiles.forEach(f => {
    const content = fs.readFileSync(f, 'utf-8');
    extractTopics(content, 'cloud').forEach(t => {
      if (t.title && !seen.has(t.title)) {
        seen.set(t.title, true);
        allTopics.push(t);
      }
    });
  });

  // 按评分排序
  allTopics.sort((a, b) => b.score - a.score);

  // 生成 frontmatter
  const todayStr = `${y}${m}${d}`;
  const nowStr = now.toISOString().replace(/T/, ' ').substring(0, 19) + '+08:00';
  const frontmatter = `---
sync:
  version: 2
  repo: https://github.com/hhhh124hhhh/openclaw-topics-sync
  branch: main
  last_merge: ${nowStr}
  local_files: ${localFiles.length}
  cloud_files: ${cloudFiles.length}
  merged_total: ${allTopics.length}
---

# 📝 共享选题池 (Shared Topics Pool)

**最后更新:** ${nowStr}
**本地选题:** ${localFiles.length} 个文件
**云端选题:** ${cloudFiles.length} 个文件
**合并后:** ${allTopics.length} 条
**推送对象:** content-agent (bot2)

---

## 🎯 今日 AI 相关热点选题（按评分排序）

`;

  // 生成 topics
  const emoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'];
  let topicsText = '';

  allTopics.forEach((t, i) => {
    const num = emoji[Math.min(i, emoji.length - 1)];
    const sourceTag = t.poolSource === 'local' ? '【本地】' : '【云端】';
    const lines = t.raw.split('\n');
    const header = lines[0];
    const rest = lines.slice(1).join('\n');
    topicsText += `${header} ${sourceTag}\n${rest}\n\n`;
  });

  const output = frontmatter + topicsText + `---\n\n**情报来源:**\n- 本地: ${localFiles.map(f => path.basename(f)).join(', ') || '无'}\n- 云端: ${cloudFiles.map(f => path.basename(f)).join(', ') || '无'}\n`;

  // 修复1: 校验输出非空
  if (allTopics.length === 0) {
    console.error('[ERROR] Merged 0 topics, skipping output');
    process.exit(1);
  }

  fs.writeFileSync(outputPath, output, 'utf-8');

  // 同时输出固定名文件供消费者读取（topics-pool-YYYYMMDD.md）
  const latestPath = path.join(REPO_DIR, `topics-pool-${todayStr}.md`);
  fs.writeFileSync(latestPath, output, 'utf-8');

  console.log(`[merge-topics] 完成: 本地${localFiles.length} + 云端${cloudFiles.length} = ${allTopics.length} 条`);
  console.log(`  Local: ${localFiles.map(f => path.basename(f)).join(', ') || '无'}`);
  console.log(`  Cloud: ${cloudFiles.map(f => path.basename(f)).join(', ') || '无'}`);
}

// 修复1: 包装整个 mergeTopics() in try/catch
try {
  mergeTopics();
  process.exit(0);
} catch (err) {
  console.error('[ERROR] merge failed:', err.message);
  process.exit(1);
}
