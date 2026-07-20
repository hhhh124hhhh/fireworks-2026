# Twitter Search Script Improvements - Quick Start

## What's New?

Based on your 2026-01-30 analysis, I've created an improved version of the Twitter search script that addresses:

✅ **Language noise** → Default English-only filtering (was 60% non-English)
✅ **Low relevance** → Smart query templates for AI topics (was "AI OR clawdbot")
✅ **Low quality** → Engagement filters (likes/retweets/replies)
✅ **Poor visibility** → Real-time progress and better error messages

## Quick Start

### 1. Test the Improved Script

```bash
cd /root/clawd/skills/twitter-search-skill/scripts

# Search for AI prompts with quality filters
./run_search_improved.sh --smart-query prompts \
  --lang en \
  --min-likes 10 \
  --min-retweets 5 \
  --max-results 100
```

### 2. Compare Results

The improved script will show:
```
🔍 Twitter Search (Improved)
==================================================
Query: "prompt engineering" OR "AI prompts" OR "ChatGPT prompts" OR "Claude prompts" lang:en min_faves:10 min_retweets:5 since:2025-12-31
Query type: Top
Max results: 100
Language filter: en
Min engagement: likes≥10, retweets≥5, replies≥0
==================================================

Fetching tweets with query: ...
  Page 1: 20 tweets after language filter
  Page 1: 20 -> 12 after engagement filter
  Total collected: 12/100
  ...

✅ Successfully fetched XX tweets.
```

### 3. Key Features

**Smart Query Templates:**
- `--smart-query prompts` → AI prompts, prompt engineering
- `--smart-query automation` → AI automation, workflows
- `--smart-query tools` → AI tools, startups
- `--smart-query clawdbot` → Clawdbot mentions

**Quality Filters:**
- `--lang en` → English only (default)
- `--min-likes N` → Minimum likes
- `--min-retweets N` → Minimum retweets
- `--min-replies N` → Minimum replies

## Recommended Queries for Your Use Case

### High-Quality AI Prompts (Skill Ideas)
```bash
./run_search_improved.sh --smart-query prompts \
  --lang en \
  --min-likes 50 \
  --min-retweets 20 \
  --min-replies 10 \
  --max-results 200
```

### AI Automation Trends
```bash
./run_search_improved.sh --smart-query automation \
  --lang en \
  --min-likes 30 \
  --min-retweets 15 \
  --max-results 300
```

### Clawdbot Brand Monitoring
```bash
./run_search_improved.sh --smart-query clawdbot \
  --query-type Latest \
  --lang en \
  --max-results 100
```

## Comparison: Before vs After

| Metric | Original (2026-01-30) | Improved (Expected) |
|--------|---------------------|---------------------|
| Total tweets | 20 | 200-500 |
| English content | 40% | 95%+ |
| Relevant tweets | 1-2 | 50-100+ |
| Noise ("ai" as interjection) | High | Very low |
| Progress visibility | Minimal | Real-time |
| Error messages | Generic | Specific |

## Files Added

1. **`twitter_search_improved.py`** - Enhanced search script
2. **`run_search_improved.sh`** - Wrapper with auto-loading
3. **`IMPROVEMENTS.md`** - Detailed documentation
4. **`README_IMPROVEMENTS.md`** - This quick start guide
5. **Updated `SKILL.md`** - Added improved script section

## Integration with Cron Jobs

To use the improved script in your cron jobs, update the job message:

```json
{
  "id": "x-twitter-prompts-scraper",
  "name": "Twitter/X AI Prompts Scraper (Improved)",
  "payload": {
    "kind": "message",
    "message": "Use improved script:\ncd /root/clawd/skills/twitter-search-skill/scripts\n./run_search_improved.sh --smart-query prompts --lang en --min-likes 10 --min-retweets 5 --max-results 500\nSave results to /root/clawd/data/x-scraping/\nGenerate analysis report\nReport findings to Slack #clawdbot"
  }
}
```

## Troubleshooting

**"Rate limit exceeded"**
- Wait 15-30 minutes before next request
- Consider upgrading API plan at twitterapi.io

**"No tweets found matching your criteria"**
- Lower engagement thresholds
- Try `--skip-lang-filter` to see all languages
- Check query syntax

**"Invalid API key"**
- Verify key at https://twitterapi.io
- Check `~/.bashrc`: `export TWITTER_API_KEY="your_key"`

## Next Steps

1. ✅ **Test** the improved script with different queries
2. 📊 **Compare** results with original data
3. ⚙️ **Update** cron jobs to use improved script
4. 📈 **Monitor** data quality for a few days
5. 🎯 **Adjust** thresholds based on actual results
6. 📝 **Document** best queries for your use cases

## Full Documentation

See `IMPROVEMENTS.md` for:
- Detailed feature comparison
- Advanced usage examples
- Integration guide
- Troubleshooting details
- Best practices

---

**Questions?** Check `IMPROVEMENTS.md` or refer to the updated `SKILL.md`
