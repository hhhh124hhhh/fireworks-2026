# HEARTBEAT.md - Intel Officer

Read this file first during heartbeat turns.

## Rules

- `cron/jobs.json` is the only live scheduler source of truth.
- Heartbeat checks status and reports drift; it does not repair scheduler config by itself.
- If there is no new risk, delivery failure, or missing handoff, reply `HEARTBEAT_OK`.

## What To Check

### Chrome DevTools (CDP port 9222)

- Check if Chrome debug port 9222 is listening: `Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 5`
- If unreachable, report: `⚠️ Chrome CDP port 9222 is not responding. Browser automation tasks may fail.`
- Do NOT attempt to restart Chrome — report only.

### Pipeline Skills Health

#### opencli CLI
- **Check:** `opencli --version`
- **Expected:** v1.1.1 or later
- **Report if:** Command not found or version < 1.0

#### gh CLI (GitHub)
- **Check:** `gh auth status`
- **Expected:** Logged in
- **Report if:** Not authenticated

#### BeautifulSoup4 (Python)
- **Check:** `python -c "from bs4 import BeautifulSoup; print('OK')"`
- **Expected:** OK
- **Report if:** Module not found

### Hotspot Grab Data (opencli-hotspot-grabber)

- **Morning grab (08:15):** Check `tmp/opencli-hotspots-*.json` exists for today
  - Command: `python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu hackernews -q`
  - Expected: ~140 items (zhihu:30, weibo:50, baidu:30, hn:30)
  
- **Afternoon grab (14:55):** Check `tmp/opencli-hotspots-*.json` exists for today
  - Command: `python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu douyin -q`
  - Expected: ~170 items (zhihu:30, weibo:50, baidu:30, douyin:50)

- **Night grab (02:00):** Check `tmp/opencli-hotspots-*.json` exists for today
  - Command: `python skills/opencli-hotspot-grabber/hotspot_grabber.py -p hackernews v2ex -q`
  - Expected: ~40 items (hn:30, v2ex:10)

### Expansion Sources (扩源平台)

- **GitHub Trending:** Check `tmp/opencli-hotspots-*.json` contains github platform data
  - Command: `python skills/opencli-hotspot-grabber/hotspot_grabber.py -p github -q`
  - Expected: 25-30 items (P0)
  - Report if: < 10 items or parse error

- **Product Hunt:** (待实现)
  - Expected: 15-20 items (P1)

- **Twitter/Reddit:** (需要登录态，待验证)
  - Expected: 15-20 items each (P1)

### Scheduler status

- `08:15` — Morning Hotspot Grab (opencli-hotspot-grabber)
- `08:30` — Morning Intel Analysis → Shared topics
- `14:55` — Afternoon Hotspot Grab (opencli-hotspot-grabber)
- `15:05` — Afternoon Intel Analysis → Shared topics
- `15:20` — Downstream push to `bot2`
- `21:00` — Heartbeat check

### Shared topic flow

- Latest shared topic file exists in `../workspace-shared/topics/`
- File naming: `topics-pool-YYYYMMDD-HHMM.md`
- Latest intel output is reflected in the shared topic pool
- Downstream handoff to `bot2` was delivered when expected

### Runtime files

- `memory/tasks-status.md` — Task execution status
- `memory/push-tracking-log.md` — Delivery tracking log
- `memory/heartbeat-state.json` — Heartbeat state cache

## Reporting Rule

Stay silent when:

- Chrome CDP 9222 is responsive
- Scheduled tasks are healthy
- Hotspot grab data exists (`tmp/opencli-hotspots-*.json`)
- Shared topics are present and fresh (today's date)
- The latest downstream handoff succeeded

Report only when:

- Chrome CDP 9222 is not responding
- Hotspot grab data is missing or stale (>2 hours old)
- A scheduled run failed
- The shared topic file is missing or stale
- The `15:20` handoff to `bot2` failed
- A concrete drift exists between runtime and docs
