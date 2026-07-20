# bot4 热点采集增强方案

**创建时间**: 2026-03-23 10:37
**目标**: 增强 intel-officer 的热点采集能力，作为主要选题来源

---

## 现状分析

### 已有能力 ✅

**热点抓取脚本**: `opencli-hotspot-grabber/hotspot_grabber.py`

**支持平台** (8 个):
- P0 技术趋势：Hacker News, V2EX, arXiv
- P1 内容素材：B 站，小红书，雪球，知乎
- P2 社会热点：微博

**定时任务**:
- 02:00 夜间海外技术
- 08:15 晨间热点
- 14:55 下午热点
- 21:00 心跳检查

**输出**: `tmp/opencli-hotspots-YYYYMMDD-HHMMSS.json`

---

## 增强方案

### 1. 扩展平台覆盖

#### 新增平台（优先级排序）

| 平台 | 类型 | 优先级 | 预期数据量 | 用途 |
|------|------|--------|-----------|------|
| **Product Hunt** | 科技产品 | ⭐⭐⭐⭐⭐ | 20 条/天 | AI 工具选题 |
| **Twitter/X** | 社交媒体 | ⭐⭐⭐⭐⭐ | 50 条/天 | 实时热点 |
| **YouTube** | 视频 | ⭐⭐⭐⭐ | 30 条/天 | 视频选题 |
| **抖音** | 短视频 | ⭐⭐⭐⭐ | 50 条/天 | 短视频选题 |
| **微信公众号** | 文章 | ⭐⭐⭐⭐ | 30 条/天 | 竞品分析 |
| **即刻** | 社区 | ⭐⭐⭐ | 30 条/天 | 补充素材 |
| **36Kr** | 科技媒体 | ⭐⭐⭐ | 20 条/天 | 行业资讯 |
| **虎嗅** | 科技媒体 | ⭐⭐⭐ | 20 条/天 | 深度观点 |

**新增后总计**: 16 个平台，~400 条/天

---

### 2. 智能分析增强

#### 当前问题
- ❌ 只抓取，不分析
- ❌ 重复内容多
- ❌ 缺少趋势判断
- ❌ 缺少 AI 相关筛选

#### 增强功能

**A. 去重与聚合**
```python
# 基于标题相似度去重
- SimHash 算法检测重复内容
- 相似话题聚合（如多个媒体报道同一事件）
- 跨平台重复检测（同一内容在多平台出现）
```

**B. AI 相关性评分**
```python
# 自动识别 AI 相关内容
- 关键词匹配（AI, LLM, GPT, Claude, 大模型...）
- 分类模型判断（AI/非 AI）
- 优先级提升（AI 内容 × 1.5 权重）
```

**C. 趋势判断**
```python
# 识别上升热点
- 对比昨日同期数据
- 计算热度增长率
- 标记"上升中"话题
```

**D. 自动标签**
```python
# 为每条热点打标签
- 技术领域（AI/前端/后端/数据...）
- 内容类型（教程/产品/新闻/观点...）
- 平台来源（国内/海外）
- 优先级（P0/P1/P2）
```

---

### 3. 输出格式增强

#### 当前格式
```json
{
  "timestamp": "2026-03-23 10:00:00",
  "platforms": {...},
  "summary": {...},
  "errors": []
}
```

#### 增强格式
```json
{
  "timestamp": "2026-03-23 10:00:00",
  "platforms": {...},
  "summary": {
    "total": 400,
    "ai_related": 120,
    "trending": 35,
    "duplicates_removed": 45
  },
  "analysis": {
    "top_topics": ["AI 工具", "大模型", "Agent"],
    "trending_topics": ["Sora", "GPT-5", "多模态"],
    "category_distribution": {
      "AI": 30%,
      "前端": 15%,
      "产品": 20%,
      "其他": 35%
    }
  },
  "recommendations": [
    {
      "topic": "Sora 竞品分析",
      "reason": "多平台热度上升快",
      "priority": "P0",
      "sources": ["Twitter", "YouTube", "36Kr"]
    }
  ],
  "errors": []
}
```

---

### 4. 工作流增强

#### 当前流程
```
抓取 → JSON → 人工分析 → 选题池
```

#### 增强流程
```
抓取 → 去重 → AI 筛选 → 趋势分析 → 自动标签 → 推荐选题 → 选题池
   ↓                                                            ↓
错误处理 ←───────────────────────────────────────────────────← 人工修正
```

---

## 实施计划

### 短期（本周）

1. ✅ **同步站点经验到 bot4**
   - 复制 `site-patterns/` 到 bot4 工作区
   - 或直接使用共享目录

2. ✅ **添加 Product Hunt 支持**
   - 高优先级（AI 工具选题）
   - 已有 opencli 命令支持

3. ✅ **添加去重功能**
   - SimHash 算法
   - 跨平台重复检测

4. ✅ **添加 AI 相关性评分**
   - 关键词匹配
   - 优先级提升

---

### 中期（本月）

1. ⏸️ **添加 Twitter/X 支持**
   - 实时热点监控
   - 需要登录态

2. ⏸️ **添加趋势分析**
   - 对比历史数据
   - 计算热度增长率

3. ⏸️ **添加自动标签**
   - 技术领域分类
   - 内容类型分类

4. ⏸️ **添加推荐系统**
   - 基于热度推荐选题
   - 基于趋势推荐选题

---

### 长期

1. ⏸️ **机器学习模型**
   - 训练选题成功率预测模型
   - 基于历史数据优化推荐

2. ⏸️ **自动化选题**
   - P0 选题自动写入选题池
   - 自动分配给内容 Bot

3. ⏸️ **反馈闭环**
   - 追踪选题发布后数据
   - 优化推荐算法

---

## 代码实现

### 去重模块（SimHash）

```python
# hotspot_dedup.py
import simhash

def dedup_hotspots(items, threshold=3):
    """
    基于 SimHash 去重
    threshold: 海明距离阈值，越小越严格
    """
    deduped = []
    hashes = {}
    
    for item in items:
        # 生成 SimHash
        h = simhash.Simhash(extract_features(item['title']))
        
        # 检查是否重复
        is_dup = False
        for existing_hash, existing_item in hashes.items():
            if h.distance(existing_hash) <= threshold:
                # 重复，保留优先级高的
                if get_priority(item) > get_priority(existing_item):
                    hashes[existing_hash] = item
                is_dup = True
                break
        
        if not is_dup:
            hashes[h] = item
            deduped.append(item)
    
    return deduped

def extract_features(text):
    """提取文本特征用于 SimHash"""
    # 分词、去停用词等
    return text.lower().split()
```

---

### AI 相关性评分

```python
# ai_scorer.py
AI_KEYWORDS = [
    'AI', '人工智能', 'LLM', '大模型', 'GPT', 'Claude', 'Gemini',
    'Agent', '智能体', '多模态', 'AIGC', '生成式 AI',
    'Machine Learning', 'Deep Learning', 'NLP', 'CV'
]

def score_ai_relevance(item):
    """
    计算 AI 相关性评分 (0-1)
    """
    text = (item['title'] + ' ' + item.get('description', '')).lower()
    
    # 关键词匹配
    matches = sum(1 for kw in AI_KEYWORDS if kw.lower() in text)
    score = min(matches / 5, 1.0)  # 最多 5 个关键词
    
    # 分类模型（可选）
    # if score > 0.3:
    #     score = max(score, ai_classifier.predict(text))
    
    return score

def is_ai_related(item, threshold=0.3):
    """判断是否为 AI 相关内容"""
    return score_ai_relevance(item) >= threshold
```

---

### 趋势分析

```python
# trend_analyzer.py
def analyze_trend(current_items, historical_items, hours=24):
    """
    分析热点趋势
    current_items: 当前热点
    historical_items: 历史热点（过去 N 小时）
    """
    trends = []
    
    for item in current_items:
        # 计算热度增长率
        current_score = item.get('score', 0)
        historical_avg = get_historical_average(historical_items, item['title'])
        
        if historical_avg > 0:
            growth_rate = (current_score - historical_avg) / historical_avg
        else:
            growth_rate = 1.0 if current_score > 0 else 0.0
        
        # 标记趋势
        trend = {
            'item': item,
            'growth_rate': growth_rate,
            'is_trending': growth_rate > 0.5,  # 增长 50% 以上
            'trend_level': 'hot' if growth_rate > 1.0 else 'rising' if growth_rate > 0.5 else 'stable'
        }
        trends.append(trend)
    
    return sorted(trends, key=lambda x: x['growth_rate'], reverse=True)
```

---

## 目录结构

```
workspace-intel-officer/skills/opencli-hotspot-grabber/
├── hotspot_grabber.py          # 主脚本（已有）
├── hotspot_dedup.py            # 去重模块（新增）
├── ai_scorer.py                # AI 评分模块（新增）
├── trend_analyzer.py           # 趋势分析模块（新增）
├── recommendation_engine.py    # 推荐引擎（新增）
├── site-patterns/              # 站点经验（同步）
│   ├── xiaohongshu.md
│   ├── zhihu.md
│   ├── weibo.md
│   └── bilibili.md
├── README.md                   # 使用说明
├── SKILL.md                    # Skill 说明
└── requirements.txt            # Python 依赖
```

---

## 依赖安装

```bash
# 新增 Python 依赖
pip install simhash-python
pip install scikit-learn  # 用于分类模型（可选）
pip install jieba  # 中文分词
```

---

## 测试计划

### 单元测试
- [ ] 去重模块测试
- [ ] AI 评分模块测试
- [ ] 趋势分析模块测试

### 集成测试
- [ ] 完整流程测试（抓取→去重→分析→推荐）
- [ ] 性能测试（400 条数据处理时间 < 30 秒）

### 人工验证
- [ ] 去重效果验证
- [ ] AI 评分准确性验证
- [ ] 推荐选题质量验证

---

## 预期效果

| 指标 | 当前 | 增强后 | 提升 |
|------|------|--------|------|
| **平台覆盖** | 8 个 | 16 个 | +100% |
| **日采集量** | 235 条 | ~400 条 | +70% |
| **重复率** | ~20% | <5% | -75% |
| **AI 相关识别** | 0% | 90%+ | +∞ |
| **选题推荐** | 0 个 | 5-10 个/天 | +∞ |
| **人工分析时间** | 30 分钟 | 10 分钟 | -67% |

---

## 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 新平台反爬 | 中 | 中 | 使用站点经验，降低频率 |
| 去重误杀 | 低 | 中 | 调整 SimHash 阈值 |
| AI 评分不准 | 中 | 低 | 人工校正 + 持续优化 |
| 性能下降 | 低 | 中 | 异步处理，增量分析 |

---

**创建者**: bot3 (zhuazhua-agent)
**版本**: v1.0.0
