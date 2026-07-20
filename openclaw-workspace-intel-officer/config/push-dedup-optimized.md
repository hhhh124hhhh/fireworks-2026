# Push Dedup Optimized

## Schedule
- Morning report: 09:00 Asia/Shanghai
- Midday report: disabled
- Evening report: 21:00 Asia/Shanghai when a matching cron job is added or updated

## Hard Rules
1. The same hotspot may be pushed at most two times in one day.
2. Hotspots older than 24 hours are skipped unless a major reversal happened.
3. If there is no new information since the morning report, do not push an evening duplicate.

## Output Shape
### Morning
- Top 3 facts only
- 1-2 topic suggestions

### Evening
- New developments since morning only
- One deep analysis under 500 words

