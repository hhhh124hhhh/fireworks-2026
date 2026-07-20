# OpenCLI 情报处理管道 v2.0 - 升级报告

## 📦 改造内容

### 1. 核心文件更新

| 文件 | 变更 | 说明 |
|------|------|------|
| `skill.json` | ✅ 更新 | 版本 1.0 → 2.0，添加管道功能描述 |
| `pipeline.py` | ✅ 新增 | 主管道脚本（21KB，整合全流程） |
| `README_v2.md` | ✅ 新增 | v2.0 使用文档 |
| `jobs.json` | ✅ 更新 | 08:30 任务 payload 改为调用管道 |

### 2. 功能整合（全部固化到代码）

**原流程（靠文档 + payload 传递规则）:**
```
定时任务 payload → 读 MEMORY.md → 读 ai_filter_rules.md → 手动筛选 → 手动评分
```

**新流程（管道自动化）:**
```
pipeline.py --full
  ├─ 读取 JSON (自动 glob)
  ├─ AI 筛选 (AIFilter 类，内置关键词库)
  ├─ 质量评分 (QualityScorer 类，内置正面/负面清单)
  ├─ 智能排序 (TopicRanker 类，内置平台权重)
  └─ 写选题池 (TopicPoolWriter 类，自动生成 Markdown)
```

### 3. 规则固化（不再依赖文档）

#### AI 筛选规则（内置到 `AIFilter` 类）
```python
AI_KEYWORDS = {
    'core': ['AI', 'LLM', '大模型', 'Agent', ...],
    'products': ['ChatGPT', 'Claude', 'Cursor', 'Kimi', ...],
    'tech': ['芯片', '半导体', 'GitHub', '网络安全', ...]
}

NON_AI_KEYWORDS = [
    '油价', '金价', '战争', '政治', '体育', '娱乐', ...
]
```

#### 质量评分规则（内置到 `QualityScorer` 类）
```python
# 正面清单（加分）
POSITIVE_RULES = [
    ['步骤', '技巧', '方法'] → +10 分，
    ['坑', '别', '避免'] → +8 分，
    ['亲测', '实测', '效率'] → +8 分，
    ['省', '节省', '时间'] → +5 分，
    [数字] → +5 分
]

# 负面清单（减分）
NEGATIVE_RULES = [
    ['战略', '格局', '宏观'] → -20 分，
    ['报告', '产业', '白皮书'] → -15 分，
    ['论文', '争议', '学术'] → -10 分
]
```

#### 平台权重（内置到 `TopicRanker` 类）
```python
platform_weights = {
    'zhihu': 0.50,      # 50%
    'hackernews': 0.20, # 20%
    'weibo': 0.15,      # 15%
    'github': 0.10,     # 10%
    'baidu': 0.05,      # 5%
}
```

---

## 🚀 使用方式

### 定时任务调用（08:30）
```bash
python skills/opencli-hotspot-grabber/pipeline.py --full \
  -p zhihu weibo baidu hackernews github \
  --output-pool ../workspace-shared/topics/topics-pool-$(date +%Y%m%d)-0830.md \
  --mode morning
```

### 手动测试
```powershell
# 测试完整管道
python skills/opencli-hotspot-grabber/pipeline.py --full -p zhihu weibo baidu --output-pool test-pool.md

# 测试 AI 筛选
python -c "from pipeline import AIFilter; f=AIFilter(); print(f.is_ai_related('GPT-5 发布'))"

# 测试质量评分
python -c "from pipeline import QualityScorer; s=QualityScorer(); print(s.score('5 个步骤学会 AI'))"
```

---

## 📊 输出示例

### 选题池 Markdown
```markdown
# 选题池 - 2026-03-28 08:30

## 🔥 P0 选题（TOP 20）
1. [GPT-5 即将发布，性能提升 10 倍](https://...) - **知乎** (AI: 0.85, 质量：+15)
   - ✅ 实战教程、具体数字

2. [新手用 AI 最常见的 5 个坑](https://...) - **知乎** (AI: 0.78, 质量：+13)
   - ✅ 踩坑总结、具体数字

## 📌 P1 选题（TOP 30）
...

## 📊 数据汇总
- 总抓取：140 条
- AI 相关：85 条
- P0 选题：20 条
- P1 选题：30 条
- P2 选题：10 条

### 平台分布
- zhihu: 45 条
- hackernews: 28 条
- weibo: 22 条
- github: 15 条
- baidu: 10 条
```

---

## ✅ 优势对比

| 维度 | 改造前 | 改造后 |
|------|--------|--------|
| **规则位置** | MEMORY.md + ai_filter_rules.md | 管道代码内建 |
| **修改方式** | 改文档 + 改 payload | 只改管道代码 |
| **可测试性** | ❌ 难以单元测试 | ✅ 可独立测试每个类 |
| **可复用性** | ❌ 仅 intel-officer 用 | ✅ 其他 agent 可调用 |
| **容错性** | ❌ 依赖人工读文档 | ✅ 代码自动执行 |
| **调试难度** | ❌ 需要查多个文件 | ✅ 管道日志清晰 |

---

## 🔄 下一步建议

### 1. 测试验证（2026-03-29 晨间）
```powershell
# 08:15 抓取后，手动运行管道测试
python skills/opencli-hotspot-grabber/pipeline.py --analyze \
  -i tmp/opencli-hotspots-*.json \
  --output-pool test-pool-0329.md \
  --mode morning
```

### 2. 定时任务切换（2026-03-30 正式）
- 当前：payload 仍保留详细说明（向后兼容）
- 建议：测试无误后，简化为单行命令

### 3. 扩展功能（可选）
- [ ] 添加 `push-notifier` 模块（自动推送 bot2）
- [ ] 添加去重优化（跨天去重、语义去重）
- [ ] 添加历史对比（与昨天选题池对比，标注重复）

---

## 📝 文件清单

```
skills/opencli-hotspot-grabber/
├── pipeline.py              ✅ 新增 - 主管道（21KB）
├── hotspot_grabber.py       ✅ 保留 - 抓取器
├── ai_scorer.py             ✅ 保留 - AI 评分器
├── ai_filter_rules.md       ✅ 保留 - 规则文档（供参考）
├── skill.json               ✅ 更新 - v2.0 配置
├── README_v2.md             ✅ 新增 - v2.0 文档
└── UPGRADE_REPORT.md        ✅ 本文档
```

---

**升级完成时间:** 2026-03-28 21:58  
**测试状态:** ⏳ 待验证（建议 08:15 抓取后手动测试）  
**正式切换:** 2026-03-30 晨间分析任务
