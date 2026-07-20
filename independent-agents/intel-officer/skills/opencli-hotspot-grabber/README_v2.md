# OpenCLI 情报处理管道 v2.0

**一站式情报处理管道** - 整合热点抓取、AI 筛选、质量评分、智能排序、选题池生成全流程。

---

## 🚀 快速开始

### 完整管道（推荐）
```powershell
# 晨间模式（知乎 + 微博 + 百度 + HN）
python skills/opencli-hotspot-grabber/pipeline.py --full -p zhihu weibo baidu hackernews --output-pool topics-pool-0830.md --mode morning

# 下午模式（知乎 + 微博 + 百度 + 抖音）
python skills/opencli-hotspot-grabber/pipeline.py --full -p zhihu weibo baidu douyin --output-pool topics-pool-1505.md --mode afternoon
```

### 分步执行
```powershell
# 步骤 1: 只抓取
python skills/opencli-hotspot-grabber/pipeline.py --grab -p zhihu weibo baidu hackernews -o tmp

# 步骤 2: 只分析（从已有 JSON）
python skills/opencli-hotspot-grabber/pipeline.py --analyze -i tmp/opencli-hotspots-*.json --output-pool topics-pool.md --mode morning
```

---

## 📋 功能特性

### 1. 热点抓取
- ✅ 支持 9 个平台：知乎、微博、百度、Hacker News、GitHub、V2EX、抖音、Lobsters、Dev.to
- ✅ 自动 Fallback：opencli → Chrome DevTools → requests
- ✅ JSON 输出：`tmp/opencli-hotspots-YYYYMMDD-HHMMSS.json`

### 2. AI 话题筛选
- ✅ 基于关键词匹配 AI/科技相关话题
- ✅ 排除非 AI 内容（油价、政治、体育、娱乐等）
- ✅ 支持自定义 AI 关键词库

**AI 关键词分类:**
- 核心 AI 术语（LLM、Agent、大模型）
- AI 产品（ChatGPT、Claude、Cursor）
- 科技扩展（芯片、半导体、GitHub、网络安全）

### 3. 质量评分（2026-03-28 优化）
**正面清单（加分）:**
- ✅ 实战教程（"5 个步骤"） +10 分
- ✅ 踩坑总结（"新手坑"） +8 分
- ✅ 工具实测（"亲测好用"） +8 分
- ✅ 职场场景（"省 X 小时"） +5 分
- ✅ 具体数字（"5 个"、"90%"） +5 分

**负面清单（减分）:**
- ❌ "XX 战略" / "XX 格局" -20 分
- ❌ 宏观报告（"产业报告"） -15 分
- ❌ 学术争议（"论文争议"） -10 分
- ❌ 纯技术无场景 -15 分

### 4. 智能排序
**综合评分公式:**
```
final_score = AI 评分×0.4 + 质量评分×0.3 + 平台权重×0.2 + 热度×0.1
```

**平台权重（MEMORY.md 标准）:**
| 平台 | 权重 |
|------|------|
| 知乎 | 50% |
| Hacker News | 20% |
| 微博 | 15% |
| GitHub | 10% |
| 百度 | 5% |

### 5. 选题池生成
**输出格式:**
```markdown
# 选题池 - 2026-03-28 08:30

## 🔥 P0 选题（TOP 20）
1. [标题](链接) - **知乎** (AI: 0.85, 质量：+15)
   - ✅ 实战教程、具体数字

## 📌 P1 选题（TOP 30）
...

## 📊 数据汇总
- 总抓取：140 条
- AI 相关：85 条
- P0 选题：20 条
- P1 选题：30 条
```

---

## 🔧 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--grab` | 只抓取 | `--grab -p zhihu weibo` |
| `--analyze` | 只分析 | `--analyze -i tmp/*.json` |
| `--full` | 完整管道 | `--full -p zhihu weibo` |
| `-p, --platforms` | 平台列表 | `-p zhihu baidu hn` |
| `-o, --output` | 抓取输出目录 | `-o tmp` |
| `--output-pool` | 选题池输出路径 | `--output-pool topics-pool.md` |
| `-i, --input` | 分析模式输入文件 | `-i tmp/hotspots-*.json` |
| `--mode` | 分析模式 | `--mode morning/afternoon/night` |
| `-q, --quiet` | 安静模式 | `-q` |

---

## 📊 输出文件

### 抓取输出
- **路径:** `tmp/opencli-hotspots-YYYYMMDD-HHMMSS.json`
- **格式:** JSON
- **内容:** 各平台原始热点数据

### 选题池输出
- **路径:** `../workspace-shared/topics/topics-pool-YYYYMMDD-HHMM.md`
- **格式:** Markdown
- **内容:** 排序后的选题列表（P0/P1/P2 分组）

---

## 🧪 测试

```powershell
# 测试 AI 筛选
python skills/opencli-hotspot-grabber/pipeline.py --grab -p zhihu -o tmp
python skills/opencli-hotspot-grabber/pipeline.py --analyze -i tmp/opencli-hotspots-*.json --output-pool test-pool.md

# 检查 AI 相关性
python -c "from pipeline import AIFilter; f = AIFilter(); print(f.is_ai_related('GPT-5 发布'))"
```

---

## 🔄 定时任务集成

### 晨间分析（08:30）
```json
{
  "payload": "python skills/opencli-hotspot-grabber/pipeline.py --full -p zhihu weibo baidu hackernews --output-pool ../workspace-shared/topics/topics-pool-0830.md --mode morning"
}
```

### 下午分析（15:05）
```json
{
  "payload": "python skills/opencli-hotspot-grabber/pipeline.py --full -p zhihu weibo baidu douyin --output-pool ../workspace-shared/topics/topics-pool-1505.md --mode afternoon"
}
```

---

## 📝 版本历史

### v2.0.0 (2026-03-28)
- ✅ 整合 AI 筛选、质量评分、排序到管道
- ✅ 固化 MEMORY.md 选题规则到代码
- ✅ 支持完整管道模式（--full）
- ✅ 优化选题池输出格式

### v1.0.0 (2026-03-24)
- ✅ 基础热点抓取功能
- ✅ 支持 opencli + Chrome Fallback
- ✅ AI 话题筛选规则

---

## 🛠️ 开发说明

### 模块结构
```
skills/opencli-hotspot-grabber/
├── pipeline.py          # 主管道（v2.0 新增）
├── hotspot_grabber.py   # 抓取器（v1.0）
├── ai_scorer.py         # AI 评分器
├── ai_filter_rules.md   # AI 筛选规则文档
└── skill.json           # Skill 配置
```

### 核心类
- `IntelligencePipeline` - 主管道类
- `AIFilter` - AI 话题筛选器
- `QualityScorer` - 质量评分器
- `TopicRanker` - 选题排序器
- `TopicPoolWriter` - 选题池生成器

---

**最后更新:** 2026-03-28 21:55  
**维护:** intel-officer  
**状态:** ✅ 生产就绪
