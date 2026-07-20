# Twitter Search Script Improvements

## Overview

The improved Twitter search script (`twitter_search_improved.py`) addresses the issues identified in the 2026-01-30 analysis:

### Issues Found
1. **Low relevance**: Query "AI OR clawdbot" was too broad
2. **Multi-language noise**: 60% non-English content
3. **Low engagement quality**: Many tweets with minimal interaction
4. **API rate limits**: Only 20 tweets fetched

### Improvements Made

#### 1. Smart Query Templates
Predefined queries for common AI topics:
- `prompts`: AI prompts, prompt engineering, ChatGPT/Claude prompts
- `automation`: AI automation, workflows, agents, tools
- `tools`: AI tools, software, applications, startups
- `clawdbot`: Clawdbot-specific searches

#### 2. Language Filtering
- Default: English only (`--lang en`)
- Can be customized to any language code
- Option to skip language filter in query (`--skip-lang-filter`)

#### 3. Engagement Filtering
- `--min-likes N`: Minimum like count (default: 0)
- `--min-retweets N`: Minimum retweet count (default: 0)
- `--min-replies N`: Minimum reply count (default: 0)
- Filters are applied after fetching to avoid API limitations

#### 4. Better Error Handling
- Clear rate limit detection (429 errors)
- Invalid API key detection (401 errors)
- Helpful error messages for troubleshooting

#### 5. Real-time Progress
- Shows page-by-page progress
- Displays filter results (e.g., "20 -> 15 after engagement filter")
- Total collected count

## Usage Examples

### Basic Usage with Smart Query

```bash
# Search for AI prompts with minimum engagement
./scripts/run_search_improved.sh --smart-query prompts --min-likes 10 --min-retweets 5

# Search for AI automation tools (English only)
./scripts/run_search_improved.sh --smart-query automation --lang en

# Search for Clawdbot mentions
./scripts/run_search_improved.sh --smart-query clawdbot
```

### Advanced Custom Query

```bash
# Custom query with strict filters
./scripts/run_search_improved.sh "\"prompt engineering\" OR \"ChatGPT prompts\"" \
  --min-likes 20 \
  --min-retweets 10 \
  --min-replies 5 \
  --lang en \
  --max-results 100
```

### Different Output Formats

```bash
# Get full JSON with all tweets
./scripts/run_search_improved.sh --smart-query prompts --format json --max-results 1000

# Get summary statistics only (default)
./scripts/run_search_improved.sh --smart-query prompts --format summary
```

### Query Type Selection

```bash
# Top tweets (relevance-ranked, default)
./scripts/run_search_improved.sh --smart-query prompts --query-type Top

# Latest tweets (chronological)
./scripts/run_search_improved.sh --smart-query prompts --query-type Latest
```

## Recommended Queries for Your Use Case

Based on the 2026-01-30 analysis findings, here are recommended queries:

### 1. High-Quality AI Prompts
```bash
./scripts/run_search_improved.sh --smart-query prompts \
  --min-likes 50 \
  --min-retweets 20 \
  --min-replies 10 \
  --lang en \
  --max-results 500
```

**Rationale**: High engagement filters out low-quality "ai" as interjections.

### 2. AI Automation Trends
```bash
./scripts/run_search_improved.sh --smart-query automation \
  --min-likes 30 \
  --min-retweets 15 \
  --lang en \
  --max-results 300
```

**Rationale**: Focus on actionable automation content for potential skills.

### 3. Emerging AI Tools
```bash
./scripts/run_search_improved.sh --smart-query tools \
  --query-type Latest \
  --min-likes 10 \
  --lang en \
  --max-results 200
```

**Rationale**: Use Latest to catch new tools before they go viral.

### 4. Clawdbot Brand Monitoring
```bash
./scripts/run_search_improved.sh --smart-query clawdbot \
  --query-type Latest \
  --lang en
```

**Rationale**: Monitor any mentions (even with low engagement).

## Comparison: Original vs Improved

| Feature | Original | Improved |
|---------|----------|----------|
| Default query | User must provide | Smart templates available |
| Language filter | No | Yes (default: English) |
| Engagement filter | No | Yes (likes/retweets/replies) |
| Progress feedback | Minimal | Real-time page-by-page |
| Error messages | Generic | Specific (rate limit, invalid key) |
| Filter application | Query only | Query + post-fetch filtering |
| Multi-language handling | No | Yes, with filtering |

## Integration with Cron Jobs

Update your cron job configuration to use the improved script:

```json
{
  "id": "x-twitter-prompts-scraper",
  "name": "Twitter/X AI Prompts Scraper (Improved)",
  "sessionTarget": "main",
  "schedule": {
    "kind": "interval",
    "everyMs": 28800000
  },
  "payload": {
    "kind": "message",
    "message": "Run Twitter search for AI prompts using the improved script:\n1. Use smart query: prompts\n2. Apply filters: lang=en, min-likes=10, min-retweets=5\n3. Save results to /root/clawd/data/x-scraping/\n4. Generate analysis report\n5. Report key findings to Slack #clawdbot"
  },
  "enabled": false
}
```

## Expected Results

Based on improved filtering:

### Before (2026-01-30)
- 20 tweets total
- 60% non-English
- 1-2 relevant tweets
- Many "ai" as interjection

### After (Expected)
- 200-500 tweets (within rate limits)
- 95%+ English
- 50-100+ relevant tweets
- High engagement only
- Quality > quantity

## Troubleshooting

### Rate Limit (429 Error)
```
Error: Rate limit exceeded. Please wait before making more requests.
```
**Solution**: Wait 15-30 minutes before next request. Consider upgrading API plan.

### No Results Found
```
No tweets found matching your criteria.
```
**Solutions**:
- Lower engagement thresholds
- Try different query terms
- Use `--skip-lang-filter` to see all languages
- Check if your query syntax is correct

### Invalid API Key (401 Error)
```
Error: Invalid API key. Please check your TWITTER_API_KEY.
```
**Solution**:
1. Verify your API key at https://twitterapi.io
2. Check `~/.bashrc` for correct format: `export TWITTER_API_KEY="your_key"`

## Next Steps

1. **Test the improved script** with different query combinations
2. **Compare results** with original data to validate improvements
3. **Update cron jobs** to use the improved script
4. **Monitor data quality** for a few days
5. **Adjust thresholds** based on actual results
6. **Document best queries** for different use cases

## Contributing

To add new smart query templates:

1. Edit `SMART_QUERIES` dict in `twitter_search_improved.py`
2. Add new topic with array of query strings
3. Test with `--smart-query YOUR_TOPIC`
4. Document usage here
