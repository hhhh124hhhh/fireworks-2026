# 定时任务配置更新报告 - PIPELINE v2.0

**更新时间:** 2026-03-28 22:17  
**更新人:** intel-officer  
**状态:** ✅ 已完成

---

## 📋 更新内容

### 1. 晨间抓取任务（08:15）

**任务 ID:** `c5a84000-2342-47f4-81f0-ec9ee0df5dbf`

**变更前:**
```bash
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu hackernews -q -o tmp
```

**变更后:**
```bash
python skills/opencli-hotspot-grabber/pipeline.py --grab \
  -p zhihu weibo baidu hackernews github \
  -o tmp -q
```

**变化:**
- ✅ 使用新管道 `pipeline.py`
- ✅ 新增 GitHub 平台（25 条）
- ✅ 预期输出：~140-165 条

---

### 2. 下午抓取任务（14:55）

**任务 ID:** `c3737991-8597-44c8-b548-1906c4968f9a`

**变更前:**
```bash
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu douyin -q -o tmp
```

**变更后:**
```bash
python skills/opencli-hotspot-grabber/pipeline.py --grab \
  -p zhihu weibo baidu douyin \
  -o tmp -q
```

**变化:**
- ✅ 使用新管道 `pipeline.py`
- ✅ 预期输出：~160 条

---

### 3. 晨间分析任务（08:30）

**任务 ID:** `f91a96b6-3d38-4426-b34c-d9c30ca57c49`

**变更前:**
```bash
# 详细说明（包含规则说明）
1) Read ALL accumulated data...
2) Filter ONLY AI-relevant topics using ai_filter_rules.md...
3) Apply quality scoring rules (2026-03-28 optimization)...
   - Negative list: ...
   - Positive list: ...
4) Deduplicate...
5) Rank and write...
6) Announce...
```

**变更后:**
```bash
python skills/opencli-hotspot-grabber/pipeline.py --analyze \
  -i tmp/opencli-hotspots-*.json \
  --output-pool ../workspace-shared/topics/topics-pool-$(date +%Y%m%d)-0830.md \
  --mode morning

Pipeline auto:
- Reads all tmp/opencli-hotspots-*.json
- Filters AI/tech topics only
- Applies quality scoring (built-in)
- Ranks by final_score
- Writes P0/P1/P2 sorted topics
```

**变化:**
- ✅ 简化 payload（规则已固化到代码）
- ✅ 不再依赖文档（ai_filter_rules.md 等）
- ✅ 单命令完成全流程

---

## 📊 任务配置总览

| 时间 | 任务 | 平台 | 命令 | 状态 |
|------|------|------|------|------|
| **08:15** | Morning Grab | 知乎 + 微博 + 百度 + HN + GitHub | `pipeline.py --grab` | ✅ 已更新 |
| **08:30** | Morning Analysis | 综合分析 | `pipeline.py --analyze` | ✅ 已更新 |
| **14:55** | Afternoon Grab | 知乎 + 微博 + 百度 + 抖音 | `pipeline.py --grab` | ✅ 已更新 |
| **15:05** | Afternoon Analysis | - | 禁用 | ⏸️ 保持禁用 |
| **15:20** | Push to bot2 | - | 禁用 | ⏸️ 保持禁用 |
| **21:00** | Heartbeat | 心跳检查 | - | ✅ 保持运行 |

---

## 🎯 优化效果

### 简化前
```
定时任务 payload (复杂)
  ↓
读取 MEMORY.md 规则
  ↓
读取 ai_filter_rules.md
  ↓
手动实现筛选/评分/排序
  ↓
写选题池
```

### 简化后
```
定时任务 payload (单命令)
  ↓
pipeline.py 自动执行
  ↓
输出选题池
```

---

## ✅ 验证结果

```bash
# JSON 格式验证
✅ OK: jobs.json valid

# 文件完整性
✅ cron/jobs.json - 已更新
✅ skills/opencli-hotspot-grabber/pipeline.py - 已测试
✅ skills/opencli-hotspot-grabber/skill.json - v2.0 配置
```

---

## 📋 生效时间

**下次执行:** 2026-03-29 08:15（晨间抓取）

**验证重点:**
1. 08:15 抓取是否成功（~140-165 条）
2. 08:30 分析是否成功（AI 筛选 + 质量评分）
3. 选题池格式是否正确（P0/P1/P2 分组）
4. 推送是否正常（下游 bot2）

---

## 🔄 回滚方案（如需）

如果新管道出现问题，可临时回滚到旧版：

```bash
# 晨间抓取回滚
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu hackernews -q -o tmp

# 分析任务回滚
# 需要手动实现筛选/评分/排序逻辑
```

---

## 📝 文件清单

### 已更新
- ✅ `cron/jobs.json` - 定时任务配置

### 已创建（本次升级）
- ✅ `skills/opencli-hotspot-grabber/pipeline.py` - 主管道
- ✅ `skills/opencli-hotspot-grabber/skill.json` - v2.0 配置
- ✅ `skills/opencli-hotspot-grabber/README_v2.md` - 使用文档
- ✅ `skills/opencli-hotspot-grabber/FULL_TEST_REPORT.md` - 测试报告

---

**更新完成时间:** 2026-03-28 22:18  
**状态:** ✅ 生产就绪  
**下次验证:** 2026-03-29 08:15
