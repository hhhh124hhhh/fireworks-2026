# Matrix State

This file is the shared coordination table for cross-platform topic assignment.

## How To Use

- `bot1` updates assignment and next-action fields
- downstream platform bots update their own status fields
- use the latest shared topic snapshot as the source for new rows
- append or update rows instead of rewriting history blindly

## Status Table

### 🟢 已完成
| topic_id | batch_id | topic_title | owner_primary | platform | status | completed_at | notes |
|---|---|---|---|---|---|---|---|
| topic-20260319-0830-jike-01 | 20260319-0830 | AI 替代研究员（私募 Agent 实战） | bot8 | jike | published | 2026-03-19 11:26 | ✅ bot8 即刻发布成功，首次链路验证通过 |

### 🔄 进行中

*当前无进行中的任务*

> 💡 **提示：** 新任务应从最新的 `topics-pool-YYYYMMDD-HHMM.md` 中分配

### 📚 学习任务 (2026-03-21 08:40)

| topic_id | batch_id | topic_title | source_file | owner_primary | platform_targets | status_overall | status_wechat | status_toutiao | status_baijiahao | status_jike | status_xhs | status_zhihu | priority_rank | assigned_by | last_updated | next_action | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|
| growth-study-20260321 | growth-study | 内容增长共享知识库学习 | growth/README.md | bot2 | wechat | ✅完成 | ✅完成 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | bot1 | 2026-03-21 08:50 | 开始创作 | 40 分钟学习完成，报告已写入 |
| growth-study-20260321 | growth-study | 内容增长共享知识库学习 | growth/README.md | bot8 | jike | ✅完成 | ❌ | ❌ | ❌ | ✅完成 | ❌ | ❌ | ❌ | bot1 | 2026-03-21 08:48 | 开始创作 | 报告已写入 |

---

## 📋 历史任务归档

<details>
<summary>2026-03-21 临时任务（点击展开）</summary>

| topic_id | batch_id | topic_title | source_file | owner_primary | platform_targets | status_overall | notes |
|---|---|---|---|---|---|---|---|
| topic-20260321-1500-01 | 20260321-1500 | Claude 编程是赌博吗？HN 1424 评论热评 | topics-pool-20260321-1505.md | bot2 | wechat | completed | HN 1424 评论，已发布 |
| topic-20260321-1500-02 | 20260321-1500 | 为什么每个公司都要有自己的大模型 | topics-pool-20260321-1505.md | bot8 | jike | completed | 知乎 95 热评，已发布 |
| topic-20260321-1500-03 | 20260321-1500 | 贾佳：具身智能现在卡在什么地方 | topics-pool-20260321-1505.md | bot9 | xiaohongshu | completed | 知乎 42 热评，已发布 |

</details>

---

## 📚 学习任务归档

<details>
<summary>2026-03-21 增长学习（点击展开）</summary>

| topic_id | owner_primary | platform | status | notes |
|---|---|---|---|---|
| growth-study-20260321 | bot2 | wechat | ✅完成 | 40 分钟学习完成 |
| growth-study-20260321 | bot8 | jike | ✅完成 | 报告已写入 |

</details>

---

## 📋 临时任务/自动执行 (2026-03-21)

| topic_id | batch_id | topic_title | source_file | owner_primary | platform_targets | status_overall | status_wechat | status_toutiao | status_baijiahao | status_jike | status_xhs | status_zhihu | priority_rank | assigned_by | last_updated | next_action | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|
| topic-20260321-1500-01 | 20260321-1500 | Claude 编程是赌博吗？HN 1424 评论热评 | topics-pool-20260321-1505.md | bot2 | wechat | queued | queued | ❌ | ❌ | ❌ | ❌ | ❌ | 1 | bot1 | 2026-03-21 15:30 | bot2 创作，目标 20:00 | HN 1424 评论，历史热评 |
| topic-20260321-1500-02 | 20260321-1500 | 为什么每个公司都要有自己的大模型 | topics-pool-20260321-1505.md | bot8 | jike | queued | ❌ | ❌ | ❌ | queued | ❌ | ❌ | 2 | bot1 | 2026-03-21 15:30 | bot8 创作，目标 20:00 | 知乎 95 热评 |
| topic-20260321-1500-03 | 20260321-1500 | 贾佳：具身智能现在卡在什么地方 | topics-pool-20260321-1505.md | bot9 | xiaohongshu | queued | ❌ | ❌ | ❌ | ❌ | queued | ❌ | 3 | bot1 | 2026-03-21 15:30 | bot9 创作，目标 20:00 | 知乎 42 热评 |

---

## ⏸️ 暂停/搁置

| topic_id | batch_id | topic_title | source_file | owner_primary | platform_targets | status_overall | status_wechat | status_toutiao | status_baijiahao | status_jike | status_xhs | status_zhihu | paused_at | paused_by | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| topic-20260318-0830-05 | 20260318-0830 | 罗永浩西贝事件舆情追踪 | topics-pool-20260318-0830.md | bot2 | wechat | paused | paused | ❌ | ❌ | ❌ | ❌ | ❌ | 2026-03-18 15:30 | bot1 | 热点已过，暂停 |
| topic-20260317-0830-03 | 20260317-0830 | 3·15 晚会曝光汇总 | topics-pool-20260317-0830.md | bot2 | wechat | empty_run | empty_run | ❌ | ❌ | ❌ | ❌ | ❌ | 2026-03-17 09:30 | bot1 | cron 未运行，数据缺失 |

---

## Notes

### 数据源说明

**⚠️ 本文档只记录任务分配状态，不记录 Bot 注册信息**

- **Bot 注册表权威源：** `workspace-creator/memory/bot-registry.md`（14 bot 完整映射）
- **健康状态权威源：** `workspace-shared/docs/bot-dashboard-data.json`（实时健康监控）
- **本文档用途：** 追踪跨平台任务分配和状态

### 字段规范

- `owner_primary` should be a bot (bot2/bot8/bot9/bot12), not a person
- `platform_targets` should be one of: `wechat`, `toutiao`, `baijiahao`, `jike`, `xiaohongshu`, `zhihu`, `course`
- `owner_primary` should match the platform owner (见下方 Platform-to-Bot Mapping)
- `status_overall` should reflect the overall current state
- use `empty_run` when the topic was valid but produced no useful output
- use `blocked` when waiting on external dependency or human intervention
- bot2 三段式分发：同一选题可同时追踪 `status_wechat` / `status_toutiao` / `status_baijiahao` 三列状态
- **小红书独立**：bot9 负责小红书（强视觉图文笔记），不与公众号/头条/百家号混为"图文平台"
- **知识付费独立**：bot7 负责课程/付费内容（高客单价产品），不与免费内容分发混为一谈

### Platform-to-Bot Mapping（完整 14 bot）

| Platform | Owner Bot | Agent | Workspace |
|----------|-----------|-------|-----------|
| 微信公众号 | bot2 | content-lite | workspace-content-lite |
| 今日头条 | bot2 | content-lite | workspace-content-lite |
| 百家号 | bot2 | content-lite | workspace-content-lite |
| 即刻 | bot8 | multi-platform-operator | workspace-multi-platform-operator |
| 小红书 | bot9 | xiaohongshu-operator | workspace-xiaohongshu-operator |
| 知乎 | bot12 | zhihu-operator | workspace-zhihu-operator |
| 课程/知识付费 | bot7 | knowledge-pay-expert | workspace-knowledge-pay-expert |
| 热点采集 | bot4 | intel-officer | workspace-intel-officer |
| 视觉设计 | bot10 | visual-expert | workspace-visual-expert |
| 数据分析 | bot11 | growth-analyst | workspace-growth-analyst |
| 虚拟偶像孵化 | bot13 | manga-vision | workspace-manga-vision |
| 虚拟偶像 IP | bot14 | faye-idol | workspace-faye |
| 工程实现 | bot3 | zhuazhua-agent | workspace-zhuazhua |
| 治理/巡检 | bot5 | governance-officer | workspace-governance-officer |
| 矩阵调度 | bot1 | main-lite | workspace-main-lite |
| 元 agent | bot6 | creator | workspace-creator |

> 💡 **Bot 详细信息查询：** 读取 `workspace-creator/memory/bot-registry.md` 或 `workspace-shared/docs/bot-dashboard-data.json`
