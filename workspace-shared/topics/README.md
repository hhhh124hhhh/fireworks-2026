# Shared Topics Pool

Location: `D:\openclaw-data\.openclaw\workspace-shared\topics\`

## Purpose

This directory is the shared upstream topic source for the content matrix.

- upstream topic discovery writes here
- platform orchestrators read and assign from here
- platform production bots consume assigned topics from here
- status rollup for cross-platform work should remain visible here

## Source Of Truth Files

- `topics-pool-YYYYMMDD-HHMM.md`
  - point-in-time topic snapshots written by upstream intel runs
- `topics-pool.md`
  - latest stable shared topic pool reference
- `matrix-state.md`
  - cross-platform assignment and status rollup table
- `README.md`
  - workflow and field definitions

## Ownership

- `bot4` / `intel-officer`
  - writes shared topic snapshots
  - refreshes latest shared topic pool
- `bot1` / `main-lite`
  - reads latest shared topic pool
  - assigns platform ownership
  - updates `matrix-state.md`
  - detects empty runs, duplicate work, and stalled handoffs
- platform bots
  - consume only the topics assigned to them
  - write back status to `matrix-state.md` or their workspace state files

## Matrix Workflow

1. `bot4` writes the latest shared topic pool for the active batch.
2. `bot1` reads the latest pool and assigns topics by platform.
3. Each platform bot consumes only its assigned work.
4. Platform bots write completion, blocker, or empty-run state.
5. `bot1` summarizes matrix status and reassigns if needed.

## Assignment Rules

- one topic may have one primary owner
- one topic may have multiple platform targets only when the matrix owner explicitly marks it as multi-platform
- if a platform bot runs empty, `bot1` should reassign the next eligible topic
- if two bots are about to consume the same topic unintentionally, `bot1` should resolve the conflict before downstream work continues

## Matrix State Fields

Use these fields in `matrix-state.md`:

- `topic_id`
- `batch_id`
- `topic_title`
- `source_file`
- `owner_primary`
- `platform_targets`
- `status_overall`
- `status_wechat`
- `status_xhs`
- `status_course`
- `priority_rank`
- `assigned_by`
- `last_updated`
- `next_action`
- `notes`

## Status Values

Recommended values:

- `queued`
- `assigned`
- `in_progress`
- `render_ready`
- `draft_ready`
- `published`
- `blocked`
- `empty_run`
- `dropped`

## Current Platform Map

- `bot2` -> WeChat public-account pipeline
- `bot7` -> knowledge-product / tutorial / PPT pipeline
- future `bot8` -> Xiaohongshu pipeline if enabled

## Important Rule

Shared topics are upstream inputs.

- upstream writes topics
- `bot1` assigns topics
- downstream bots produce platform outputs

Downstream bots must not redefine ownership on their own when `matrix-state.md` already provides assignment.

---

## Bidirectional Sync (Local ↔ Cloud)

### Architecture

```
本地 bot4 ←→ GitHub ←→ 云端 bot4
         ↑
    local + cloud 分文件写入
         ↓
    merge-topics.js 合并
         ↓
    topics-pool.md (供消费者读取)
```

### File Naming

| File | Purpose |
|------|---------|
| `topics-pool-local-YYYYMMDD-HHMM.md` | 本地 bot4 写入 |
| `topics-pool-cloud-YYYYMMDD-HHMM.md` | 云端 bot4 写入 |
| `topics-pool-YYYYMMDD-HHMM.md` | 合并后的历史归档 |
| `topics-pool.md` | 合并后的固定名（供消费者读取） |

### Sync Mechanisms

1. **Cron** (每 5 分钟): `sync-topics.sh` runs via cron job
2. **Post-Commit Hook**: `.git/hooks/post-commit` auto-triggers sync after commit
3. **File Watcher** (实时): `watch-sync.js` monitors file changes and auto-syncs

### Sync Scripts

- `merge-topics.js` — 合并 local + cloud 选题池
- `sync-topics.sh` — pull → merge → push 完整流程
- `watch-sync.js` — 文件监控 + 自动同步
- `start-watch.sh` — 启动文件监控

### Usage

```bash
# 启动文件监控（实时同步）
bash start-watch.sh

# 或直接用 node
node watch-sync.js
```

### Merge Rules
- 按标题去重
- 按综合评分排序
- 标记来源（本地/云端）

---

## 🛡️ Fail-Fast 防御机制（2026-04-01）

为防止静默失败场景（脚本报错不退出、写入空文件、消费者无感知使用过期数据），已实现以下防御：

### 已修复的漏洞

| # | 漏洞 | 文件 | 修复内容 |
|---|------|------|----------|
| 1 | **merge 输出空文件无感知** | `merge-topics.js` | try/catch + exit code + 源文件/输出非空校验 |
| 2 | **Consumer 无感知使用过期数据** | `topic_pool.py` (两处) | MAX_TOPIC_AGE_HOURS=12 + `is_topic_fresh()` 检查 |
| 3 | **pipeline.py 永远返回成功** | `pipeline.py` | `sys.exit(0 if success else 1)` |
| 4 | **rss-grabber 空数据也写文件** | `rss-grabber.py` | 空 entries 跳过写文件 |
| 5 | **sync-from-cloud.sh 无文件校验** | `sync-from-cloud.sh` | `-s` 检查空文件 + SSH 超时 |
| 6 | **sync-and-merge.bat 不检查 exit code** | `sync-and-merge.bat` | 前一步失败后停止执行 |
| 7 | **watch-sync.js 失败无告警** | `watch-sync.js` | 失败时发送外部通知 |
| 8 | **git push 失败无告警** | `sync-topics.sh` | 失败时打印告警 |

### 下游不空转保护

**TopicPoolUnavailableError 异常机制**：

```
read_topic_pool()              select_top_topic()           CLI 入口
      │                              │                        │
      │ 策略1: merge 输出            │ 筛选 AI 相关            │
      │   ↓ 解析为空?               │   ↓ 去重               │
      │ 策略2: fallback raw         │   ↓ 评分排序           │
      │   ↓ 新鲜度检查失败?          │   ↓ TOP N             │
      │ 策略3: raw 解析为空?         │   ↓ 结果为空?          │
      │   ↓                          │   ↓                    │
      ├──── 全部失败 ─────────────────┼────────────────────────┤
      │         ↓                              ↓              │
      ↓                                    ↓                   ↓
抛出 TopicPoolUnavailableError   抛出 TopicPoolUnavailableError  捕获 → sys.exit(1)
```

**关键原则**：任何环节出问题都会 "fail fast"，Consumer 必须捕获异常，不允许静默空转。

### 仍需注意的边界情况

- checksum 校验（文件完整性）
- 端到端签名（merge 输出加 hash）
- 幂等性设计（重复执行结果一致）

这些是第二阶段迭代目标。

