# HEARTBEAT.md — AI Team Health Monitor

This file coordinates the daily/heartbeat execution cycle for the AI team. It's read by Monica (the orchestrator) at each heartbeat to determine what state the team is in and what needs to happen next.

---

## Current System State

```yaml
last_check: "2026-03-04T12:30:00Z"
next_scheduled: "2026-03-04T18:00:00Z"
cycle_count: 1
system_status: "healthy"

# Today's Execution Log
2026-03-04:
  08:00:
    agent: "老刘"
    status: "completed"
    output: "intel/raw/2026-03-04-raw-intel.md"
    details: "收集了 12 条情报 (工具 5 / 案例 2 / 资讯 5)"
  
  10:00:
    agent: "阿强"
    status: "completed"
    input: "intel/raw/2026-03-04-raw-intel.md"
    output: "intel/DAILY-INTEL.md"
    details: "筛选出 Top 3 情报，产出完整分析报告"
  
  12:30:
    agent: "Monica"
    status: "monitoring"
    action: "system_check"
    result: "all_agents_completed_successfully"

# Next Cycle Predictions
next_cycle_tasks:
  - agent: "老刘"
    scheduled: "2026-03-05T00:00:00Z"
    estimated_duration: "2 hours"
  
  - agent: "阿强"
    scheduled: "2026-03-05T02:30:00Z"
    depends_on: "老刘"
    estimated_duration: "2 hours"
```

---

## Daily Execution Cycle

The AI team operates on a daily cycle with these phases:

### Phase 1: Intelligence Gathering (00:00 - 02:00)
**Agent:** 老刘 (Researcher)  
**Task:** Collect raw AI intelligence

**Inputs:**
- None (starts the chain)

**Outputs:**
- `intel/raw/YYYY-MM-DD-raw-intel.md`
- `intel/data/YYYY-MM-DD-*.json`

**Checklist:**
- [ ] Product Hunt AI category checked
- [ ] GitHub Trending AI repos checked
- [ ] Twitter/X AI accounts monitored
- [ ] Chinese sources checked (知乎, 公众号)
- [ ] At least 10 raw intel items collected
- [ ] Files written to correct locations

---

### Phase 2: Analysis & Curation (02:00 - 04:00)
**Agent:** 阿强 (Analyst)  
**Task:** Analyze raw intel, produce curated daily report

**Inputs:**
- `intel/raw/YYYY-MM-DD-raw-intel.md` (from 老刘)
- `intel/data/YYYY-MM-DD-*.json`

**Outputs:**
- `intel/DAILY-INTEL.md` (main output for content creators)
- `intel/analysis/YYYY-MM-DD-deep-dive.md` (2-3x per week)

**Checklist:**
- [ ] Raw intel file read completely
- [ ] Top 3-5 most important items identified
- [ ] Trend analysis completed
- [ ] Content creator recommendations written
- [ ] DAILY-INTEL.md written to correct location
- [ ] Personal memory file updated

---

### Phase 3: Content Creation (04:00 - 06:00)
**Agents:** 小凯 (X/Twitter), 小美 (LinkedIn)  
**Task:** Create platform-specific content from daily intel

**Inputs:**
- `intel/DAILY-INTEL.md` (from 阿强)

**Outputs:**
- `deliverables/kelly-drafts/YYYY-MM-DD-tweets.md` (小凯)
- `deliverables/rachel-drafts/YYYY-MM-DD-linkedin.md` (小美)

**Checklist (每个 content creator):**
- [ ] DAILY-INTEL.md read completely
- [ ] 3-5 content drafts created
- [ ] Platform-appropriate voice used
- [ ] Drafts written to correct location
- [ ] Personal memory file updated

---

## Phase 4: Orchestration & Review (Continuous)
**Agent:** Monica (CEO/Orchestrator)  
**Task:** Monitor system state, ensure handoffs happen

**Responsibilities:**
1. **Check file timestamps** — Who's waiting? Who's done?
2. **Verify handoffs** — Did 老刘 finish before 阿强 started?
3. **Monitor for blockages** — Is someone stuck waiting?
4. **Update HEARTBEAT.md** — Log current system state

**Daily Checklist:**
- [ ] Check if `intel/raw/` has new files from 老刘
- [ ] Check if `intel/DAILY-INTEL.md` has been updated by 阿强
- [ ] Check if `deliverables/` has new content from 小凯/小美
- [ ] Verify all files have recent timestamps
- [ ] Update HEARTBEAT.md with current state
- [ ] Note any blockages or delays

---

## System States

```yaml
# Healthy - all agents running normally
status: healthy
last_activity: "2026-03-04T05:30:00Z"
next_check: "2026-03-04T06:00:00Z"

# Blocked - an agent is waiting
status: blocked
blocked_agent: "阿强"
waiting_for: "老刘"
reason: "intel/raw/2026-03-04-raw-intel.md not found"
since: "2026-03-04T02:00:00Z"

# Error - system malfunction
status: error
error_agent: "小凯"
error_type: "output_write_failed"
details: "deliverables/kelly-drafts/ is not writable"
```

---

## Recovery Procedures

### If an agent doesn't produce output:

1. **Check memory file** — Did they log any issues?
2. **Check input** — Did they have valid input to work with?
3. **Wait one cycle** — Some delays are temporary
4. **Flag for review** — If problem persists

### If file handoffs fail:

1. **Verify file paths** — Are agents reading/writing to correct locations?
2. **Check timestamps** — Is the "ready" file actually fresh?
3. **Review SOUL.md** — Did the agent misunderstand their output location?

### System restart procedure:

1. Check all agent directories exist
2. Verify all required subdirectories exist
3. Clear stale lock files (if any)
4. Update HEARTBEAT.md with restart timestamp
5. Resume normal operation

---

## Performance Metrics

Track over time:

- **Cycle time** — How long does full loop take? (target: <6 hours)
- **Handoff success rate** — % of cycles where all handoffs succeed
- **Content quality score** — Review samples of output quality
- **Agent health** — % of cycles where each agent produces output

---

## Changelog

- 2026-03-04: Initial system definition
- [Future updates logged here]

---

*HEARTBEAT.md is the system state of truth. Read it at the start of every cycle.*
*Last updated: 2026-03-04 by System*