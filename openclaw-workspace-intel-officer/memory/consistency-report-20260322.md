# Intel Officer 核心文件一致性梳理报告

**生成时间:** 2026-03-22 13:25:00  
**梳理范围:** cron/jobs.json, MEMORY.md, AGENTS.md, HEARTBEAT.md, hotspot_grabber.py

---

## ✅ 一致性状态（已全部同步）

| 文件 | 状态 | 最后更新 | 说明 |
|------|------|---------|------|
| **cron/jobs.json** | ✅ 一致 | 2026-03-22 13:10 | 定时任务（唯一真实来源） |
| **MEMORY.md** | ✅ 一致 | 2026-03-22 13:10 | P0 标准 + 抓取流程 |
| **AGENTS.md** | ✅ 一致 | 2026-03-22 13:20 | 工作空间规则（刚更新） |
| **HEARTBEAT.md** | ✅ 一致 | 2026-03-22 13:25 | 心跳检查规则（刚更新） |
| **hotspot_grabber.py** | ✅ 一致 | 2026-03-22 13:05 | 抓取脚本（含百度 + Fallback） |

---

## 📊 定时任务配置（cron/jobs.json）

### 晨间流程
| 时间 | 任务 | 平台 | 输出 |
|------|------|------|------|
| **08:15** | Hotspot Grab - Morning Data | 知乎 + 微博 + 百度 + HN | `tmp/opencli-hotspots-*.json` |
| **08:30** | Intel Morning Analysis | 分析 + 选题池 | `topics-pool-YYYYMMDD-HHMM.md` |

### 下午流程
| 时间 | 任务 | 平台 | 输出 |
|------|------|------|------|
| **14:55** | Hotspot Grab - Afternoon Data | 知乎 + 微博 + 百度 + 抖音 | `tmp/opencli-hotspots-*.json` |
| **15:05** | Intel Afternoon Analysis | 分析 + 选题池 | `topics-pool-YYYYMMDD-HHMM.md` |
| **15:20** | Push Topics To Content | 下游手递 | bot2 通知 |

### 夜间流程
| 时间 | 任务 | 平台 | 输出 |
|------|------|------|------|
| **00:30** | Night Social Scan | 微博 + 知乎 + 小红书 | `memory/night-social-scan.md` |
| **01:00** | Night Tech Deep Dive | OpenClaw/Cursor/GPT | `memory/night-intel-round4.md` |
| **02:00** | Night Tech Tracker | HN + V2EX + arXiv | `memory/night-tech-tracker.md` |
| **04:00** | Night Intel Output | 整合输出 | `topics-pool-YYYYMMDD-HHMM.md` |

### 心跳检查
| 时间 | 任务 | 说明 |
|------|------|------|
| **09:00** | Morning Heartbeat | 检查晨间执行状态 |
| **21:00** | Evening Heartbeat | 检查全天执行状态 |

---

## 🎯 P0 选题标准（已统一）

### 早上 08:30
| 来源 | 权重 | 筛选标准 | 优先级 |
|------|------|---------|--------|
| 知乎热榜 | 45% | TOP20 | P0 |
| 微博热搜 | 20% | TOP30 | P0 |
| 百度热搜 | 10% | TOP30 | P0 |
| Hacker News | 15% | Top30 | P0 |
| GitHub Trends | 10% | Trending | P0 ⚠️ |

### 下午 15:05
| 来源 | 权重 | 筛选标准 | 优先级 |
|------|------|---------|--------|
| 知乎热榜 | 50% | TOP20 | P0 |
| 微博热搜 | 25% | TOP30 | P0 |
| 百度热搜 | 10% | TOP30 | P0 |
| 抖音热榜 | 15% | Top50 | P1 |

**每日 P0 总计:** ~220 条（含百度 60 条）

---

## 🛠️ 热点抓取技能（opencli-hotspot-grabber）

### 支持平台
| 平台 | 数量 | 优先级 | 抓取方式 |
|------|------|--------|---------|
| 知乎 | 30 | 前 20=P0 | opencli |
| 微博 | 50 | 前 30=P0 | opencli |
| 百度 | 30 | 全部 P0 | 网页抓取 ✅ |
| Hacker News | 30 | 全部 P0 | opencli |
| V2EX | 30 | 全部 P0 | opencli |
| 抖音 | 50 | 全部 P1 | opencli |
| B 站 | 20 | 全部 P1 | opencli |
| 小红书 | 20 | 全部 P1 | opencli |
| 雪球 | 20 | 全部 P1 | opencli |

**总计:** ~260 条/次

### Fallback 策略
```
opencli (首选)
   ↓ 失败
Chrome DevTools (CDP 9222)
   ↓ 失败
requests 网页抓取
```

**触发条件:**
- opencli 命令不存在或未安装
- opencli 超时（>30 秒）
- opencli 返回空数据或 JSON 解析失败
- 网络连接问题

---

## 📝 修复记录

### 2026-03-22 13:20 - AGENTS.md 更新
**问题:** AGENTS.md 还是旧版本，缺少百度和 Fallback 策略  
**修复:**
- ✅ 更新 P0 标准（加入百度 10%）
- ✅ 更新抓取命令（加入百度）
- ✅ 加入 Fallback 策略说明
- ✅ 更新定时任务表格
- ✅ 更新数据流向图

### 2026-03-22 13:25 - HEARTBEAT.md 更新
**问题:** 心跳检查未包含 opencli-hotspot-grabber 数据检查  
**修复:**
- ✅ 加入 Hotspot Grab Data 检查项
- ✅ 明确晨间/下午/夜间抓取时间和平台
- ✅ 更新 Scheduler status 时间节点
- ✅ 更新 Reporting Rule

---

## 🔍 验证测试

### 抓取测试（2026-03-22 13:18）
```bash
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu -q
```
**结果:**
- ✅ 知乎：30 items (opencli)
- ✅ 微博：50 items (opencli)
- ✅ 百度：30 items (网页抓取)
- ✅ 总计：110 items
- ✅ 输出：`tmp/opencli-hotspots-20260322-131831.json`

### 选题池写入测试
**结果:**
- ✅ 文件：`../workspace-shared/topics/topics-pool-20260322-1318.md`
- ✅ 格式：符合历史规范
- ✅ 内容：P0 选题 + 创作建议 + 数据摘要

---

## 📋 核心文件职责

| 文件 | 职责 | 优先级 |
|------|------|--------|
| `cron/jobs.json` | 定时任务配置（唯一真实来源） | ⭐⭐⭐⭐⭐ |
| `MEMORY.md` | 长期记忆 + P0 标准 + 抓取流程 | ⭐⭐⭐⭐ |
| `AGENTS.md` | 工作空间规则 + Startup Checklist | ⭐⭐⭐⭐ |
| `HEARTBEAT.md` | 心跳检查规则 | ⭐⭐⭐ |
| `hotspot_grabber.py` | 热点抓取脚本 | ⭐⭐⭐⭐⭐ |

---

## ✅ 结论

**全部核心文件已同步一致！**

- ✅ 定时任务配置正确（cron/jobs.json）
- ✅ P0 标准统一（含百度 10%）
- ✅ 抓取流程统一（opencli-hotspot-grabber）
- ✅ Fallback 策略已实现并文档化
- ✅ 心跳检查规则已更新

**系统稳定性:** 🟢 稳定，可放心运行定时任务

---

**梳理完成时间:** 2026-03-22 13:25  
**维护者:** intel-officer
