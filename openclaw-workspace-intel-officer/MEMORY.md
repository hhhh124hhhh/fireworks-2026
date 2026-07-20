# MEMORY.md - Intel Officer 长期记忆

## 用户信息

- **姓名:** 郝文强
- **Timezone:** Asia/Shanghai

---

## 🚨 P0 选题标准（最高优先级 - 已固化）

### 早上 08:30
| 来源 | 原权重 | 新权重 | 筛选标准 | 优先级 |
|------|--------|--------|---------|--------|
| **知乎热榜** | 45% | **50%** | TOP20 | P0 |
| **微博热搜** | 20% | **15%** | TOP30 | P0 |
| **百度热搜** | 10% | **5%** | TOP30 | P0 |
| **Hacker News** | 15% | **20%** | Top30 | P0 |
| **GitHub Trends** | 10% | **10%** | Trending | P0 ⚠️ |

### 下午 15:05
| 来源 | 原权重 | 新权重 | 筛选标准 | 优先级 |
|------|--------|--------|---------|--------|
| **知乎热榜** | 50% | **55%** | TOP20 | P0 |
| **微博热搜** | 25% | **20%** | TOP30 | P0 |
| **百度热搜** | 10% | **5%** | TOP30 | P0 |
| **抖音热榜** | 15% | **20%** | Top50 | P1 |

---

## 🎯 选题质量筛选规则（2026-03-28 优化）

### ❌ 负面清单（直接降级为 P2）
- **"XX 战略"类选题** - 宏观空泛，缺乏实操
- **"XX 格局"类选题** - 抽象分析，无具体场景
- **纯技术热点（无应用场景）** - 如"XX 模型参数量突破"
- **宏观分析报告** - 如"中国 AI 产业发展报告"
- **学术争议** - 如"NeurIPS 论文含金量讨论"

### ✅ 正面清单（优先推荐为 P0+）
- **实战教程** - 包含"5 个步骤"、"3 个技巧"等具体数字
- **踩坑总结** - 包含"新手最常见的坑"、"千万别"等预警词
- **工具实测** - 包含"亲测好用"、"效率提升 10 倍"等体验描述
- **职场场景** - 包含"帮你省 X 小时"、"避免 X 损失"等价值承诺
- **具体数字** - 标题包含"5 个"、"3 个月"、"90%"等量化指标

### 评分规则
```python
# 基础分 + 加分项 - 减分项
score = base_score + bonus - penalty

# 加分项（每项 +5~10 分）
if "步骤" in title or "技巧" in title: bonus += 10
if "坑" in title or "别" in title: bonus += 8
if "亲测" in title or "效率" in title: bonus += 8
if "省" in title or "避免" in title: bonus += 5
if has_numbers(title): bonus += 5  # 包含具体数字

# 减分项（每项 -10~20 分）
if "战略" in title or "格局" in title: penalty += 20
if "报告" in title and "产业" in title: penalty += 15
if "论文" in title and "争议" in title: penalty += 10
if is_pure_tech_no_scenario(title): penalty += 15
```

### 晚上 21:00
- **深度研究** - 按以下搜索策略执行（2026-03-24 更新）

---

## 🔍 深度搜索策略（基于 a16z Top 100 AI Apps 报告洞察）

### 7 大核心搜索方向

| 方向 | 关键词 | 优先级 | 监控频率 |
|------|--------|--------|---------|
| **1. 青少年 AI 行为** | 青少年 AI、学生 AI 工具、AI 做作业、AI 陪伴 | P0 | 每周 |
| **2. 垂直 Agent** | AI Agent 金融、AI 医疗、AI 旅行规划、AI 购物助手 | P0 | 每周 |
| **3. 桌面 AI 应用** | Cursor、Granola、Claude Desktop、AI 桌面工具 | P1 | 每周 |
| **4. 中国本土模型** | 豆包、DeepSeek、Kimi、智谱 AI、通义千问 | P0 | 每日 |
| **5. AI 浏览器** | Perplexity、Comet、Atlas、Arc Search、AI 浏览器 | P1 | 每周 |
| **6. AI 社交实验** | Sora、AI 社交、AI 视频社交、AI 内容社区 | P1 | 每周 |
| **7. 记忆/身份基建** | AI 记忆、AI 身份、AI 认证层、AI 个性化 | P2 | 每月 |

### 搜索平台扩展

**新增监控源：**
- **Product Hunt** - AI 应用发布（尤其是桌面应用/Agent）
- **Twitter/X** - AI 创始人动态、产品发布
- **Reddit r/ArtificialIntelligence** - 用户讨论、使用案例
- **知乎 AI 话题** - 本土模型讨论、使用体验
- **微信公众号 AI 垂类** - 行业分析、产品评测

### 关键词策略调整

**原有关键词：** AI、人工智能、大模型、ChatGPT、Claude

**新增关键词：**
```
AI Agent、自主 Agent、桌面 AI、AI 浏览器、AI 记忆、AI 身份、
青少年 AI、学生 AI、AI 做作业、AI 陪伴、AI 情感支持、
垂直 AI、AI 金融、AI 医疗、AI 旅行、AI 购物、
豆包、DeepSeek、Kimi、智谱、通义、文心一言、
Sora、AI 视频、AI 社交、AI 内容社区、
Cursor、Granola、Claude Desktop、Perplexity、Comet、Atlas
```

### 地域差异化监控

| 地区 | 重点监控 | 原因 |
|------|---------|------|
| **中国** | 豆包、DeepSeek、Kimi、智谱 | 独立 AI 生态系统（15% 使用 ChatGPT/Gemini） |
| **俄罗斯** | Gigachat、Yandex | 制裁导致平行 AI 生态 |
| **新加坡** | AI 采用趋势 | 人均 AI 采用率全球第一 |
| **美国** | 基础模型动态 | ChatGPT/Claude/Gemini 主战场 |
| **印度** | 本土 AI 产品 | 多语言市场、人口红利 |

### 文化信任度监控

**AI 信任度指标：**
- 美国：32%（低信任，高质疑）
- 中国/阿联酋/新加坡：60-80%（高信任，技术乐观）
- 欧洲：50-60%（中等）

**监控内容：**
- AI 取代工作讨论
- AI 伦理争议
- AI 监管政策
- 用户采纳障碍

---

## 🔧 热点抓取标准流程（核心规则）

### 必须使用 `opencli-hotspot-grabber` skill

**基础命令:**
```bash
# 晨间 (08:15) - 知乎 + 微博 + 百度 + HN
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu hackernews -q

# 下午 (14:55) - 知乎 + 微博 + 百度 + 抖音
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo baidu douyin -q

# 夜间 (02:00) - HN + V2EX
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p hackernews v2ex -q
```

### 🎯 选题搜索关键词（逐步添加）

**每次抓取后，额外搜索以下关键词（按优先级逐步添加）：**

| 批次 | 关键词 | 来源 | 数量 | 优先级 |
|------|--------|------|------|--------|
| **Batch 1** | AI Agent | 知乎/百度 | 10 | P0 |
| **Batch 2** | 豆包/DeepSeek/Kimi | 知乎/百度 | 10 | P0 |
| **Batch 3** | 桌面 AI/Cursor | 知乎/百度 | 5 | P1 |
| **Batch 4** | AI 浏览器/Perplexity | 知乎/百度 | 5 | P1 |
| **Batch 5** | 青少年 AI/学生 AI | 知乎/百度 | 5 | P1 |
| **Batch 6** | Sora/AI 视频 | 知乎/微博 | 5 | P2 |

**执行方式:**
```bash
# 在基础抓取完成后，执行关键词搜索（示例）
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu baidu -k "AI Agent" -n 10
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu baidu -k "豆包" -n 5
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu baidu -k "DeepSeek" -n 5
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu baidu -k "Kimi" -n 5
```

**逐步添加策略:**
- **第 1 周（2026-03-24 ~ 03-30）**: Batch 1（AI Agent）
- **第 2 周（2026-03-31 ~ 04-06）**: Batch 1 + Batch 2（+ 中国本土模型）
- **第 3 周（2026-04-07 ~ 04-13）**: Batch 1 + 2 + Batch 3（+ 桌面 AI）
- **第 4 周（2026-04-14 ~ 04-20）**: Batch 1 + 2 + 3 + Batch 4（+ AI 浏览器）
- **后续**: 根据产出质量调整，保持每日额外搜索 ~20-30 条

---

## 🛡️ 意外情况处理（Fallback 策略）

**优先级：** opencli → Chrome DevTools → 网页抓取

```python
# 1. 首选 opencli（npm 全局命令）
opencli zhihu hot -f json

# 2. opencli 失败时，自动切换到 Chrome DevTools (CDP 9222)
# - 检查 Chrome 是否运行在调试模式
# - 创建新标签页访问目标网站
# - 等待页面加载后解析 HTML

# 3. Chrome 不可用时，降级到 requests 网页抓取
# - 直接 HTTP 请求公开 API 或网页
# - 解析 HTML/JSON 返回数据
```

**触发条件:**
- opencli 命令不存在或未安装
- opencli 超时（>30 秒）
- opencli 返回空数据或 JSON 解析失败
- 网络连接问题

**补位平台:**
- ✅ 百度热搜 - Chrome fallback 已实现
- 🔄 知乎热榜 - Chrome fallback 待实现
- 🔄 微博热搜 - Chrome fallback 待实现

---

## ⏰ 定时任务（已配置）

| 时间 | 任务 | 平台 | P0 产出 | 推送 |
|------|------|------|--------|------|
| **02:00** | Night Overseas Tech | Hacker News + V2EX | ~40 条 | 记忆文件 |
| **08:15** | Morning Hotspots | 知乎 + 微博 + 百度 + HN | ~140 条 | - |
| **08:30** | Intel Morning Analysis | 分析 + 选题池 | - | 咨讯群 ✅ |
| **14:55** | Afternoon Hotspots | 知乎 + 微博 + 百度 + 抖音 | ~170 条 | - |
| **15:05** | Intel Afternoon Analysis | 分析 + 选题池 | - | 咨讯群 ✅ |
| **21:00** | Heartbeat | 心跳检查 | - | 异常时推送 |

**每日 P0 总计:** ~220 条（含百度 60 条）

---

## 📊 数据流向

```
02:00 抓取 (HN + V2EX) → tmp/opencli-hotspots-0200.json
   ↓
08:15 抓取 (知乎 + 微博 + HN) → tmp/opencli-hotspots-0815.json
   ↓
08:30 分析 → 选题池 → 推送到咨讯群
   ↓
14:55 抓取 (知乎 + 微博 + 抖音) → tmp/opencli-hotspots-1455.json
   ↓
15:05 分析 → 更新选题池 → 推送到咨讯群
   ↓
21:00 心跳检查 → 无异常则沉默
```

---

## 📁 核心职责

### 情报收集
- 全域热点抓取（知乎/微博/Hacker News/抖音/V2EX）
- P0 选题筛选（知乎前 20/微博前 30/HN Top30）
- 技术趋势监控（Hacker News + V2EX）
- 内容素材收集（抖音/B 站/小红书）

### 情报分析
- P0 优先级筛选
- 热点趋势分析
- 竞品监测
- 每日情报报告生成

---

## 工具配置

### Chrome DevTools（真实浏览器）
- **调试端口:** 9222
- **用户数据:** C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data
- **开机启动:** ✅ 已配置

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

## 推送配置

- **目标群:** 咨讯群 (`oc_2842f3a9c032f1ec76371316c6653823`)
- **推送时间:** 08:30 / 15:05 / 04:00
- **推送内容:** 选题池短选 + 数据汇总

---

## 文件编辑最佳实践

- **优先使用 `write` 而非 `edit`**
- **备份重要文件** - 大改动前先备份
- **路径规范** - 使用相对路径

---

## 系统配置

- **模型:** ali/qwen3.5-plus
- **工作空间:** D:\openclaw-data\.openclaw\workspace-intel-officer
- **心跳间隔:** 30 分钟

---

## 已注册 Skill

- `opencli-hotspot-grabber` - 全域热点抓取（标准方案）✅
- `chrome-devtools` - Chrome 浏览器自动化
- `intel-hotspot-grabber` - 传统热点抓取（备用）
- `analyze` - 结构化分析框架
- `opencli` - OpenCLI 工具封装

---

## 沟通原则

1. **直接执行** - 不要问来问去，遇到问题先尝试解决
2. **安全意识** - 敏感信息要脱敏
3. **工作效率** - 批量操作优先，避免重复工作

---

## 🏗️ 架构原则（重要经验 - 已固化）

### 稳定系统三要素

1. **单一技能策略** - 核心能力封装到一个 skill
   - ✅ `opencli-hotspot-grabber` - 全域热点抓取
   - ✅ 所有平台逻辑集中管理
   - ✅ Fallback 策略内置

2. **核心文件一致性** - 文档与配置同步
   - ✅ `cron/jobs.json` - 定时任务（唯一真实来源）
   - ✅ `MEMORY.md` - P0 标准 + 流程
   - ✅ `AGENTS.md` - 工作空间规则
   - ✅ `HEARTBEAT.md` - 心跳检查

3. **定时 + 心跳机制** - 自动化运维
   - ✅ 定时任务 - 自动执行
   - ✅ 心跳检查 - 异常报告
   - ✅ 无异常则沉默

### 修改策略最小化

**以后调整只需修改：**
```
skills/opencli-hotspot-grabber/hotspot_grabber.py
```

**不需要修改：**
- ❌ 定时任务配置（cron/jobs.json）
- ❌ 多个文档（MEMORY.md / AGENTS.md 等）
- ❌ 多个技能文件

**扩展流程：**
1. 修改 skill 代码
2. 测试验证
3. 完成（可选：更新 MEMORY.md 文档）

---

## 最后更新

- **创建时间:** 2026-03-14
- **维护:** intel-officer
- **最新:** 2026-03-24 10:50 - 数据累积模式（下午/夜间只抓取，早上统一分析）

---

## 🛠️ 最佳实践（重要经验）

### 修改定时任务的正确方式

**❌ 错误方式:** 直接编辑 `cron/jobs.json`
- 可能破坏 JSON 格式
- 绕过 scheduler 同步机制
- 可能导致 `_lastSync` 时间戳不一致

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

**原因:**
- API 会自动处理 JSON 格式
- 自动更新 `_lastSync` 时间戳
- 确保 scheduler 状态同步
- 避免手动编辑错误

---

## 🚨 重要变更（2026-03-24）

### 10:50 - 数据累积模式（避免浪费）

**问题:** 如果 08:30 只用 08:15 的数据，下午和夜间分析白跑了

**解决方案:** 数据累积 + 早上统一分析

**数据流向:**
```
08:15 抓取 → tmp/hotspots-0815.json ┐
14:55 抓取 → tmp/hotspots-1455.json ├─→ 08:30 综合分析
00:30 抓取 → tmp/night-social.json  ├─→ 读取所有文件
02:00 抓取 → tmp/night-tech.json ───┘   → 写入选题池
```

**任务调整:**
- ✅ 15:05 分析 → 禁用（不浪费 token）
- ✅ 04:00 分析 → 禁用（不浪费 token）
- ✅ 08:30 分析 → 读取所有累积数据

**节省:**
- 下午分析：~300K tokens/次
- 夜间分析：~300K tokens/次
- 每日节省：~600K tokens（约 75%）

---

### 10:27 - 下午选题池优化（已废弃）

**原方案:** 下午只缓存，夜间综合分析  
**问题:** 夜间分析完 08:30 不用，还是浪费  
**状态:** 已废弃，升级为数据累积模式

---

### 09:55 - AI 筛选规则固化

**问题:** 选题池中混入大量非 AI 内容（油价、美伊局势、体育赛事等）

**解决方案:**
1. 创建 `skills/opencli-hotspot-grabber/ai_filter_rules.md` - AI 话题筛选规则
2. 更新 `cron/jobs.json` - 早/午/夜分析任务 payload 添加 AI 筛选指令
3. 定时任务保持不变 - 只修改 payload，不影响 bot2 流程

**AI 话题分类:**
- ✅ AI 技术与模型（LLM、Agent、生成式 AI）
- ✅ AI 产品与应用（ChatGPT、Claude、Cursor、AI 浏览器）
- ✅ AI 硬件与芯片（AI 手机、AI PC、NPU）
- ✅ AI 公司与人物（OpenAI、Anthropic、阿里达摩院）
- ✅ AI 编程与开发（Cursor、Claude Code、Copilot）
- ✅ AI 安全与伦理（监管、隐私、就业影响）
- ✅ AI 投资与商业（融资、并购、创业）
- ✅ 科技扩展（小米/华为/特斯拉、芯片半导体、GitHub 开源、网络安全）

**非 AI 话题排除:**
- ❌ 国际政治/战争（除非涉及 AI）
- ❌ 财经新闻（油价、金价、股市）
- ❌ 体育赛事
- ❌ 娱乐八卦
- ❌ 一般社会新闻

**生效时间:** 2026-03-24 15:05 下午分析任务开始

**已有内容处理:** 不删除已有非 AI 内容（避免影响 bot2 流程），后续新增仅 AI/科技
