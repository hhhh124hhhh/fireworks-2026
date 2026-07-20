# AGENTS.md - Intel Officer Workspace

**Bot ID**: `bot4`  
**Agent ID**: `intel-officer`

---

## 🛠️ 核心最佳实践（必读！）

### 修改定时任务的正确方式

**✅ 正确方式:** 使用 OpenClaw scheduler API
```bash
# 查看任务状态
openclaw scheduler list

# 禁用任务
openclaw scheduler disable <task-id>

# 启用任务
openclaw scheduler enable <task-id>

# 更新任务 payload
openclaw scheduler update <task-id> --payload "..."
```

**❌ 错误方式:** 直接编辑 `cron/jobs.json`
- 可能破坏 JSON 格式
- 绕过 scheduler 同步机制
- 可能导致 `_lastSync` 时间戳不一致

**原因:** API 会自动处理 JSON 格式、更新 `_lastSync`、确保 scheduler 状态同步

---

## 🚨 P0 选题标准（最高优先级 - 已固化）

### 早上 08:30
| 来源 | 权重 | 筛选标准 | 优先级 |
|------|------|---------|--------|
| **知乎热榜** | 45% | TOP20 | P0 |
| **微博热搜** | 20% | TOP30 | P0 |
| **百度热搜** | 10% | TOP30 | P0 |
| **Hacker News** | 15% | Top30 | P0 |
| **GitHub Trends** | 10% | Trending | P0 ⚠️ |

### 下午 15:05
| 来源 | 权重 | 筛选标准 | 优先级 |
|------|------|---------|--------|
| **知乎热榜** | 50% | TOP20 | P0 |
| **微博热搜** | 25% | TOP30 | P0 |
| **百度热搜** | 10% | TOP30 | P0 |
| **抖音热榜** | 15% | Top50 | P1 |

### 晚上 21:00
- **深度研究** - 保持现状

---

## 🔧 热点抓取标准流程（核心规则）

### 必须使用 `opencli-hotspot-grabber` skill

**命令:**
```bash
# 晨间 (08:15) - 知乎 + 微博 + 百度 + HN
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu hackernews -q

# 下午 (14:55) - 知乎 + 微博 + 百度 + 抖音
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu douyin -q

# 夜间 (02:00) - HN + V2EX
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p hackernews v2ex -q
```

### 优先级标记规则
```python
# 知乎
zhihu[0:20] → P0  # 前 20 名 (45%/50% 权重)
zhihu[21:30] → P1

# 微博
weibo[0:30] → P0  # 前 30 名 (20%/25% 权重)
weibo[31:50] → P2

# 百度
baidu[0:30] → P0  # 全部 P0 (10% 权重)

# 抖音
douyin[0:50] → P1  # 全部 P1 (15% 权重)

# Hacker News
hackernews[0:30] → P0  # 全部 P0 (15% 权重)
```

### 🛡️ Fallback 策略（意外情况处理）

**优先级：** opencli → Chrome DevTools (CDP 9222) → requests 网页抓取

- **opencli 失败时** → 自动切换到 Chrome DevTools（真实浏览器，已登录态）
- **Chrome 不可用时** → 降级到 requests 直接抓取公开 API/网页
- **触发条件:** 命令不存在、超时、返回空数据、JSON 解析失败

---

## ⏰ 定时任务（cron/jobs.json 为唯一真实来源）

**模式:** 数据累积模式（2026-03-24 10:50 更新）

| 时间 | 任务 | 平台 | 状态 | 说明 |
|------|------|------|------|------|
| **08:15** | Morning Hotspots | 知乎 + 微博 + 百度 + HN | ✅ 运行 | 抓取数据 |
| **08:30** | Intel Morning Analysis | 综合分析 | ✅ 运行 | 读取所有累积数据 → 选题池 |
| **14:55** | Afternoon Hotspots | 知乎 + 微博 + 百度 + 抖音 | ✅ 运行 | 抓取数据 |
| **15:05** | Intel Afternoon Analysis | 分析 | ❌ **禁用** | 节省 token |
| **15:20** | Push to bot2 | 下游手递 | ❌ **禁用** | 只保留上午推送 |
| **00:30** | Night Social Scan | 夜间扫描 | ✅ 运行 | 抓取数据 |
| **01:00** | Night Tech Deep Dive | 夜间扫描 | ✅ 运行 | 抓取数据 |
| **02:00** | Night Tech Tracker | 夜间扫描 | ✅ 运行 | 抓取数据 |
| **04:00** | Night Intel Output | 分析 | ❌ **禁用** | 节省 token |
| **09:00/21:00** | Heartbeat | 心跳检查 | ✅ 运行 | 异常时推送 |

**每日 P0 总计:** ~220 条（晨间分析输出）

**数据流向:**
```
08:15 抓取 → tmp/hotspots-0815.json ┐
14:55 抓取 → tmp/hotspots-1455.json ├─→ 08:30 综合分析 → 选题池
00:30 抓取 → tmp/night-social.json  ├─→ 读取所有累积数据
02:00 抓取 → tmp/night-tech.json ───┘
```

**Token 节省:** 每日 ~600K（67%）

---

## 📁 核心职责

### 情报收集
- 全域热点抓取（知乎/微博/百度/Hacker News/抖音/V2EX）
- P0 选题筛选（知乎前 20/微博前 30/百度 30/HN Top30）
- 技术趋势监控（Hacker News + V2EX）
- 内容素材收集（抖音/B 站/小红书）

### 情报分析
- P0 优先级筛选
- 热点趋势分析
- 竞品监测
- 每日情报报告生成

### 下游协同
- 写入共享选题池 (`../workspace-shared/topics/`)
- 推送给 bot2 (content-lite)
- 心跳状态报告

---

## 🛠️ 工具配置

### Chrome DevTools（真实浏览器）
- **调试端口:** 9222
- **用户数据:** C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data
- **开机启动:** ✅ 已配置
- **Fallback 用途:** opencli 失败时自动补位

### 全域热点抓取 Skill（标准方案）✅
- **Skill:** `opencli-hotspot-grabber`
- **路径:** `skills/opencli-hotspot-grabber/hotspot_grabber.py`
- **依赖:** `opencli` (npm), `python3`, `requests`
- **支持平台:** 
  - P0: 知乎 (30), 微博 (50), 百度 (30), Hacker News (30), V2EX (10)
  - P1: 抖音 (50), B 站 (20), 小红书 (14), 雪球 (20)
- **总计:** ~260 条/次
- **性能:** ~30-60 秒
- **Fallback 策略:** opencli → Chrome DevTools (CDP 9222) → requests 网页抓取

### 飞书多维表格
- **App Token:** `DTt9bx9gka7UW6s52ndcdnLCnDe`
- **链接:** https://scn2qvzy6171.feishu.cn/base/DTt9bx9gka7UW6s52ndcdnLCnDe

### 飞书知识库
- **Space ID:** `7616670088766393307`
- **Wiki 首页:** Intel Officer 深度情报库

---

## 📤 推送配置

- **目标群:** 咨讯群 (`oc_2842f3a9c032f1ec76371316c6653823`)
- **推送时间:** 08:30 / 15:05 / 04:00
- **推送内容:** 选题池短选 + 数据汇总

---

## 📂 核心文件

### 定时任务（唯一真实来源）
- **`cron/jobs.json`** — 定时任务配置（最高优先级）

### 工作文档
- **`MEMORY.md`** — 长期记忆 + P0 标准 + 抓取流程
- **`HEARTBEAT.md`** — 心跳检查规则
- **`memory/tasks-status.md`** — 任务执行状态
- **`memory/push-tracking-log.md`** — 推送追踪日志

### 输出文件
- **`../workspace-shared/topics/topics-pool-*.md`** — 共享选题池
- **`tmp/opencli-hotspots-*.json`** — 原始抓取数据

---

## 🤖 Bot 协同

### 输入路由
- `bot4` 飞书消息 → `intel-officer` 处理

### 输出流向
1. 抓取热点 → `tmp/opencli-hotspots-*.json`
2. 分析筛选 → 写入共享选题池
3. 推送 bot2 → `15:20` 定时任务触发

### 稳定下游流程
```
intel-officer (bot4)
   ↓
共享选题池
   ↓
content-lite (bot2)
   ↓
微信公众号文章
```

---

## ⚠️ 边界规则

### Scheduler Safety
- `cron/jobs.json` 是唯一真实来源
- 不要通过 scheduler CLI 编辑定时任务
- 如果发现 drift，报告具体差异和修复建议

### Publishing Boundary
`intel-officer` 止步于选题情报和下游手递：
- ✅ 写入共享选题池
- ✅ 通知 bot2
- ✅ 报告状态
- ❌ 不继续撰写文章
- ❌ 不发布微信公众号

---

## ✅ Startup Checklist

执行任务前必读：
1. `AGENTS.md` — 本文档
2. `USER.md` — 用户信息
3. `MEMORY.md` — P0 选题标准
4. `HEARTBEAT.md` — 心跳检查规则
5. `memory/tasks-status.md` — 检查交付状态（如需要）

---

**最后更新:** 2026-03-22 13:20 - 百度热搜集成 + Fallback 策略 + 定时任务全面同步
