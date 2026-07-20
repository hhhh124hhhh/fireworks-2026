#!/usr/bin/env node

/**
 * Twitter 推文转换成 Clawdbot Skill
 * 从收集的推文中提取有价值的提示词模板，转换成可发布的 Skill
 */

const fs = require('fs');
const path = require('path');

// 导入去重管理模块
const { isTweetConverted, recordConvertedSkill } = require('./dedup-manager.js');

// 推文数据源
const TWEET_DATA_PATHS = [
  '/root/clawd/ai-prompt-marketplace/reports/twitter-report-2026-01-30-0920.json',
  '/root/clawd/ai-prompt-marketplace/reports/high-value-tweets.json',
  '/root/clawd/memory/twitter_search_ai_prompts.json'
];

// 输出目录
const OUTPUT_DIR = '/root/clawd/generated-skills';

/**
 * 分析推文是否适合转换成 Skill
 */
function analyzeTweetForSkillConversion(tweet) {
  const scores = {
    hasPromptTemplate: 0,
    hasUsefulContent: 0,
    isTechnical: 0,
    isTutorial: 0,
    engagement: 0
  };

  const text = tweet.text || '';
  const likes = tweet.metrics?.likes || 0;
  const retweets = tweet.metrics?.retweets || 0;
  const bookmarks = tweet.metrics?.bookmarks || 0;

  // 检查是否包含提示词模板
  if (text.includes('prompt:') || text.includes('Prompt:') || text.includes('{')) {
    scores.hasPromptTemplate += 50;
  }
  if (text.includes('"type":') || text.includes('"prompt"')) {
    scores.hasPromptTemplate += 30;
  }

  // 检查是否有实用内容
  if (text.includes('step-by-step') || text.includes('guide') || text.includes('how to')) {
    scores.hasUsefulContent += 30;
  }
  if (text.includes('template') || text.includes('framework')) {
    scores.hasUsefulContent += 20;
  }

  // 检查技术深度
  if (text.includes('engineering') || text.includes('optimization') || text.includes('API')) {
    scores.isTechnical += 20;
  }

  // 检查是否教程
  if (text.includes('Here is') || text.includes('Follow these steps') || text.match(/\d+\./)) {
    scores.isTutorial += 20;
  }

  // 互动得分（归一化）
  scores.engagement = Math.min(100, (likes + retweets * 2 + bookmarks * 3) / 100);

  // 计算总分
  const totalScore = Object.values(scores).reduce((sum, val) => sum + val, 0);

  return {
    ...scores,
    totalScore,
    shouldConvert: totalScore >= 100 && scores.hasPromptTemplate >= 30
  };
}

/**
 * 从推文提取提示词内容
 */
function extractPromptFromTweet(tweet) {
  const text = tweet.text || '';

  // 尝试提取 JSON 格式的提示词
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    try {
      return JSON.parse(jsonMatch[0]);
    } catch (e) {
      // 不是有效的 JSON，返回原始文本
      return jsonMatch[0];
    }
  }

  // 尝试提取 "Prompt:" 之后的内容
  const promptMatch = text.match(/Prompt:\s*([\s\S]*)/i);
  if (promptMatch) {
    return promptMatch[1].trim();
  }

  return null;
}

/**
 * 生成 SKILL.md 文件
 */
function generateSkillMD(tweet, analysis) {
  const prompt = extractPromptFromTweet(tweet);
  const author = tweet.author?.username || 'unknown';
  const url = tweet.url;

  let skillContent = `# AI ${prompt ? 'Prompt Template' : 'Content'} Skill

## Description
This skill was converted from a Twitter post by @${author}.
Original: ${url}

## Source Statistics
- Likes: ${tweet.metrics?.likes || 0}
- Retweets: ${tweet.metrics?.retweets || 0}
- Bookmarks: ${tweet.metrics?.bookmarks || 0}

## Content
`;

  if (typeof prompt === 'object') {
    skillContent += `\`\`\`json\n${JSON.stringify(prompt, null, 2)}\n\`\`\`\n\n`;
  } else if (prompt) {
    skillContent += `\`\`\`\n${prompt}\n\`\`\`\n\n`;
  }

  skillContent += `## Original Tweet
${tweet.text}

---

*Generated on ${new Date().toISOString()}*
`;

  return skillContent;
}

/**
 * 生成 Skill 文件名
 */
function generateSkillName(tweet) {
  const text = tweet.text || '';
  const author = tweet.author?.username || 'unknown';

  // 尝试从推文中提取关键词
  const keywords = text.match(/\b(prompt|template|guide|framework|engineering|image|text|chatgpt|claude|ai)\b/gi) || [];

  let name;
  if (keywords.length > 0) {
    const keyword = keywords[0].toLowerCase();
    name = `${keyword}-from-${author}`;
  } else {
    name = `ai-skill-from-${author}`;
  }

  return name.toLowerCase().replace(/[^a-z0-9-]/g, '-');
}

/**
 * 主函数
 */
async function main() {
  console.log('🔍 开始分析推文数据...\n');

  // 确保输出目录存在
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const allTweets = [];

  // 读取所有推文数据
  for (const filePath of TWEET_DATA_PATHS) {
    try {
      const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      if (data.tweets && Array.isArray(data.tweets)) {
        allTweets.push(...data.tweets);
      } else if (Array.isArray(data)) {
        allTweets.push(...data);
      }
      console.log(`✓ 已加载 ${filePath}`);
    } catch (e) {
      console.warn(`✗ 跳过 ${filePath}: ${e.message}`);
    }
  }

  console.log(`\n📊 总共加载了 ${allTweets.length} 条推文\n`);

  // 分析每条推文
  const analysisResults = [];
  for (const tweet of allTweets) {
    const analysis = analyzeTweetForSkillConversion(tweet);
    if (analysis.totalScore >= 50) { // 至少有些价值
      analysisResults.push({
        tweet,
        analysis
      });
    }
  }

  console.log(`📈 分析完成，${analysisResults.length} 条推文有一定价值\n`);

  // 按分数排序
  analysisResults.sort((a, b) => b.analysis.totalScore - a.analysis.totalScore);

  // 显示 Top 10
  console.log('🏆 Top 10 推文排名：\n');
  analysisResults.slice(0, 10).forEach((result, index) => {
    const { tweet, analysis } = result;
    const author = tweet.author?.username || 'unknown';
    const preview = (tweet.text || '').substring(0, 60).replace(/\n/g, ' ');

    console.log(`${index + 1}. @${author} - ${analysis.totalScore.toFixed(0)}分`);
    console.log(`   预览: ${preview}...`);
    console.log(`   提示词模板: ${analysis.hasPromptTemplate > 0 ? '✓' : '✗'}`);
    console.log(`   实用性: ${analysis.hasUsefulContent > 0 ? '✓' : '✗'}`);
    console.log(`   建议转换: ${analysis.shouldConvert ? '✓ 是' : '✗ 否'}\n`);
  });

  // 转换符合条件的推文
  const convertCandidates = analysisResults.filter(r => r.analysis.shouldConvert);
  console.log(`\n📝 发现 ${convertCandidates.length} 条推文适合转换成 Skill\n`);

  if (convertCandidates.length === 0) {
    console.log('⚠️  没有找到足够高质量的推文进行转换');
    console.log('💡 建议：');
    console.log('   1. 使用更具体的搜索查询（如 "prompt engineering template"）');
    console.log('   2. 搜索 #promptengineering 标签');
    console.log('   3. 手动筛选优质推文内容');
    return;
  }

  // 生成 Skill 文件
  let convertedCount = 0;
  let skippedCount = 0;
  for (const result of convertCandidates) {
    const { tweet, analysis } = result;

    // 检查推文是否已转换
    if (isTweetConverted(tweet)) {
      skippedCount++;
      console.log(`⊘ 跳过 (已转换): ${tweet.url}`);
      continue;
    }

    const skillName = generateSkillName(tweet);
    const skillContent = generateSkillMD(tweet, analysis);

    const skillPath = path.join(OUTPUT_DIR, `${skillName}.md`);
    fs.writeFileSync(skillPath, skillContent, 'utf8');

    // 记录转换的 Skill
    recordConvertedSkill(tweet, skillName);

    convertedCount++;
    console.log(`✓ 已生成: ${skillName}.md`);
  }

  console.log(`\n✅ 转换完成！生成了 ${convertedCount} 个 Skill 文件`);
  console.log(`⊘ 跳过 ${skippedCount} 个已转换的推文`);
  console.log(`📁 输出目录: ${OUTPUT_DIR}`);

  // 生成汇总报告
  const reportPath = path.join(OUTPUT_DIR, 'conversion-report.md');
  const reportContent = generateReport(analysisResults, convertCandidates);
  fs.writeFileSync(reportPath, reportContent, 'utf8');
  console.log(`📊 汇总报告: ${reportPath}`);
}

/**
 * 生成转换报告
 */
function generateReport(allResults, convertedResults) {
  let report = `# Twitter 推文到 Skill 转换报告

生成时间: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}

## 📊 统计概览

- 分析推文总数: ${allResults.length}
- 有价值推文: ${allResults.length}
- 适合转换: ${convertedResults.length}
- 实际转换: ${convertedResults.length}

## 🏆 Top 10 推文详情

`;

  allResults.slice(0, 10).forEach((result, index) => {
    const { tweet, analysis } = result;
    const author = tweet.author?.username || 'unknown';
    const likes = tweet.metrics?.likes || 0;
    const retweets = tweet.metrics?.retweets || 0;

    report += `### ${index + 1}. @${author}

- **总分**: ${analysis.totalScore.toFixed(0)}
- **互动数据**: ${likes} 点赞, ${retweets} 转发
- **包含提示词模板**: ${analysis.hasPromptTemplate > 0 ? '✓' : '✗'}
- **实用内容**: ${analysis.hasUsefulContent > 0 ? '✓' : '✗'}
- **技术深度**: ${analysis.isTechnical > 0 ? '✓' : '✗'}
- **教程类型**: ${analysis.isTutorial > 0 ? '✓' : '✗'}
- **建议转换**: ${analysis.shouldConvert ? '✓ 是' : '✗ 否'}

**推文内容**:
${(tweet.text || '').substring(0, 300)}...

**链接**: ${tweet.url || 'N/A'}

---

`;
  });

  report += `## 📝 已转换的 Skills

`;

  convertedResults.forEach((result, index) => {
    const { tweet } = result;
    const skillName = generateSkillName(tweet);
    const author = tweet.author?.username || 'unknown';

    report += `${index + 1}. ${skillName}.md (来源: @${author})\n`;
  });

  report += `\n## 💡 改进建议

1. **搜索优化**: 使用更精确的查询词（如 "prompt engineering template", "AI prompt framework"）
2. **标签过滤**: 专门搜索 #promptengineering, #AIPrompts 标签
3. **作者筛选**: 关注已知的高质量提示词工程专家
4. **手动筛选**: 结合自动化分析，人工审核高质量内容

---

*报告自动生成*`;

  return report;
}

// 运行主函数
main().catch(console.error);
