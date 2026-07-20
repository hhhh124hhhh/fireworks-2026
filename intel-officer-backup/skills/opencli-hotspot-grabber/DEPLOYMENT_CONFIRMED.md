# ✅ 部署确认 - P0 选题标准全面固化

**固化时间:** 2026-03-21 20:00  
**执行时间:** 明天 (2026-03-22) 自动开始

---

## 📌 P0 选题标准（已固化到所有文件）

### 早上 08:30
| 来源 | 权重 | 筛选标准 | 优先级 |
|------|------|---------|--------|
| **知乎热榜** | 50% | TOP20 | P0 ✅ |
| **微博热搜** | 20% | TOP30 | P0 ✅ |
| **Hacker News** | 15% | Top30 | P0 ✅ |
| **GitHub Trends** | 15% | Trending | P0 ⚠️ |

### 下午 15:05
| 来源 | 权重 | 筛选标准 | 优先级 |
|------|------|---------|--------|
| **知乎热榜** | 60% | TOP20 | P0 ✅ |
| **微博热搜** | 30% | TOP30 | P0 ✅ |
| **抖音热榜** | 10% | Top50 | P1 ✅ |

### 晚上 21:00
- **深度研究** - 保持现状

---

## 📁 已更新的文件

| 文件 | 更新内容 | 状态 |
|------|---------|------|
| **MEMORY.md** | P0 选题标准 + 抓取流程 | ✅ 已固化 |
| **AGENTS.md** | P0 选题标准 + 工作规则 | ✅ 已固化 |
| **CORE_RULES.md** | 完整抓取标准流程 | ✅ 已固化 |
| **hotspot_grabber.py** | 优先级标记逻辑 | ✅ 已修改 |
| **cron/jobs.json** | 定时任务配置 | ✅ 已配置 |

---

## 🔧 优先级标记代码（已实现）

```python
# 知乎 - 前 20 名 P0
def grab_zhihu(self, limit: int = 30):
    for i, item in enumerate(data):
        item['priority'] = 'P0' if i < 20 else 'P1'

# 微博 - 前 30 名 P0
def grab_weibo(self, limit: int = 50):
    for i, item in enumerate(data):
        item['priority'] = 'P0' if i < 30 else 'P2'

# 抖音 - 全部 P1
def grab_douyin(self, limit: int = 50):
    for item in data:
        item['priority'] = 'P1'

# Hacker News - 全部 P0
def grab_hackernews(self, limit: int = 30):
    for item in data:
        item['priority'] = 'P0'
```

---

## ⏰ 定时任务（已配置）

| 时间 | 任务 | 平台 | 命令 |
|------|------|------|------|
| **02:00** | Night Overseas Tech | HN + V2EX | `python ... -p hackernews v2ex -q` |
| **08:15** | Morning Hotspots | 知乎 + 微博 + HN | `python ... -p zhihu weibo hackernews -q` |
| **08:30** | Intel Morning Analysis | 分析 + 推送 | 自动执行 |
| **14:55** | Afternoon Hotspots | 知乎 + 微博 + 抖音 | `python ... -p zhihu weibo douyin -q` |
| **15:05** | Intel Afternoon Analysis | 分析 + 推送 | 自动执行 |
| **21:00** | Heartbeat | 心跳检查 | 自动执行 |

---

## 📊 预期产出

### 晨间 (08:30)
- 知乎：30 条 → **P0: 20 条** (前 20)
- 微博：50 条 → **P0: 30 条** (前 30)
- HN: 30 条 → **P0: 30 条** (全部)
- **P0 小计:** ~80 条

### 下午 (15:05)
- 知乎：30 条 → **P0: 20 条** (前 20)
- 微博：50 条 → **P0: 30 条** (前 30)
- 抖音：50 条 → **P1: 50 条** (全部)
- **P0 小计:** ~50 条

### 夜间 (02:00)
- HN: 30 条 → **P0: 30 条**
- V2EX: 10 条 → **P0: 10 条**
- **P0 小计:** ~40 条

**每日 P0 总计:** ~170 条

---

## 📤 推送配置

| 时间 | 推送目标 | 推送内容 |
|------|---------|---------|
| **08:30** | 咨讯群 | 晨间选题池 + P0 选题推荐 |
| **15:05** | 咨讯群 | 下午选题池 + P0 选题推荐 |
| **04:00** | 咨讯群 | 夜间情报汇总 + P0 技术选题 |

**推送群:** 咨讯群 (`oc_2842f3a9c032f1ec76371316c6653823`)

---

## ✅ 验证清单

- [x] P0 选题标准已固化到 MEMORY.md
- [x] P0 选题标准已固化到 AGENTS.md
- [x] 优先级标记代码已修改 (知乎前 20/微博前 30)
- [x] 抖音热榜抓取已添加
- [x] 定时任务已配置 (08:15/14:55 平台调整)
- [x] 推送目标已配置 (咨讯群)
- [x] 核心规则文档已更新 (CORE_RULES.md)

---

## 🚀 明天开始自动执行

**无需任何手动操作！**

1. **02:00** - 自动抓取 Hacker News + V2EX
2. **08:15** - 自动抓取知乎 + 微博 + HN
3. **08:30** - 自动分析 + 推送晨间情报
4. **14:55** - 自动抓取知乎 + 微博 + 抖音
5. **15:05** - 自动分析 + 推送下午情报
6. **21:00** - 自动心跳检查

---

## 📞 异常处理

如果某天抓取失败，会收到告警推送，检查：

```bash
# 1. 检查 Chrome CDP
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 3

# 2. 检查 opencli
opencli --version
opencli doctor

# 3. 检查 Python
python --version
```

---

**部署完成！明天醒来自动执行！** 🎉

**最后更新:** 2026-03-21 20:00  
**维护者:** intel-officer
