# 信息搜集项目评估报告

**生成时间**：2026-02-05
**评估范围**：`/root/clawd/projects/info-search/` 及相关技能和工具

---

## 1. 现有资源清单

### 1.1 项目结构

```
info-search/
├── README.md              # 项目概述文档（✅ 完整）
├── docs/
│   └── lessons.md         # 经验总结文档（✅ 完整）
├── strategies/            # 搜索策略目录（❌ 空目录）
├── processors/           # 结果处理目录（❌ 空目录）
└── workflows/            # 工作流目录（❌ 空目录）
```

### 1.2 已有技能（Skills）

| 技能名称 | 路径 | 脚本数量 | 环境变量 | 配置状态 |
|---------|------|---------|---------|---------|
| **searxng** | `/root/clawd/skills/searxng/` | 1 | `SEARXNG_URL` | ⚠️ 已配置但不可用 |
| **firecrawl-search** | `/root/clawd/skills/firecrawl-search/` | 3 | `FIRECRAWL_API_KEY` | ⚠️ 已配置但余额不足 |
| **twitter-search-skill** | `/root/clawd/skills/twitter-search-skill/` | 4 | `TWITTER_API_KEY` | ⚠️ 已配置但余额不足 |
| **tavily-search** | `/root/clawd/skills/tavily-search/` | 1 | `TAVILY_API_KEY` | ❌ 未配置 |
| **web-search-exa** | `/root/clawd/skills/web-search-exa/` | MCP集成 | 无需API key | ✅ 可用 |

### 1.3 独立脚本

| 脚本名称 | 路径 | 用途 | 依赖 |
|---------|------|------|------|
| **ai-research.sh** | `/root/clawd/scripts/` | AI信息自动搜索 | SearXNG |
| **twitter_search_via_web.py** | `/root/clawd/scripts/` | 通过Web搜索Twitter | SearXNG |

### 1.4 内置工具

| 工具名称 | 功能 | 配置要求 |
|---------|------|---------|
| **web_search** | Brave搜索API | `BRAVE_API_KEY` |
| **web_fetch** | URL内容提取 | 无需配置 |

---

## 2. 组件评估结果

### 2.1 核心技能评估

#### 🔴 **searxng** - 不可用

**测试结果**：
```bash
$ uv run /root/clawd/skills/searxng/scripts/searxng.py search "test" -n 3
Error connecting to SearXNG: timed out
No results found for: test
```

**环境配置**：
- `SEARXNG_URL=http://149.13.91.232:8080`
- 服务未响应（连接超时）

**问题分析**：
1. SearXNG 服务可能未运行或配置错误
2. 外部IP地址（149.13.91.232）可能已失效
3. 网络连接问题或防火墙限制

**影响**：严重
- 依赖SearXNG的所有脚本无法使用
- `ai-research.sh` 受影响
- `twitter_search_via_web.py` 受影响

---

#### 🔴 **firecrawl-search** - 不可用（余额不足）

**测试结果**：
```bash
$ python3 /root/clawd/skills/firecrawl-search/scripts/search.py "test"
Error: 402 - Payment Required
{"success":false,"error":"Insufficient credits to perform this request."}
```

**环境配置**：
- `FIRECRAWL_API_KEY=fc-1ee8c610f62b455cbfe5bcf6cc3ac2d2`
- API Key 已配置

**问题分析**：
1. Firecrawl API 余额不足
2. 需要充值或升级计划
3. 付费服务限制免费使用

**影响**：中等
- 强大的网页抓取功能无法使用
- 搜索功能被阻塞
- 爬取功能被阻塞

---

#### 🔴 **twitter-search-skill** - 不可用（余额不足）

**测试结果**：
```bash
$ ./scripts/run_search.sh "AI" --max-results 5
Warning: Failed to fetch page 1: API request failed: 402 Client Error: Payment Required
No tweets found.
```

**环境配置**：
- API Key 已从 `~/.bashrc` 加载（twitterapi.io）
- 配置正确但余额不足

**问题分析**：
1. Twitter API 余额不足
2. 付费服务限制免费使用
3. 社交媒体搜索功能不可用

**影响**：中等
- Twitter 数据分析无法进行
- 社交媒体趋势追踪受影响
- 影响者发现功能不可用

---

#### 🔴 **tavily-search** - 不可用（未配置）

**测试结果**：
```bash
$ env | grep TAVILY_API_KEY
# 无输出 - 环境变量未设置
```

**环境配置**：
- `TAVILY_API_KEY` 未配置

**问题分析**：
1. 未申请 Tavily API Key
2. 环境变量未设置
3. 依赖外部付费服务

**影响**：低
- AI 优化搜索功能不可用
- 可以使用其他搜索替代

---

#### 🟢 **web-search-exa** - 可用

**技术实现**：
- 通过 MCP 服务器集成：`https://mcp.exa.ai/mcp`
- 无需 API Key
- 支持实时搜索和内容提取

**特点**：
- ✅ 无需配置
- ✅ 免费使用
- ✅ 实时搜索
- ✅ 支持多种搜索模式（fast, deep, auto）
- ✅ 返回简洁、相关的内容

**限制**：
- 需要通过 MCP 协议使用
- 不是独立脚本
- 搜索结果数量有限

---

### 2.2 辅助工具评估

#### 🔴 **web_search (内置)** - 不可用（未配置）

**错误信息**：
```
web_search needs a Brave Search API key.
```

**问题分析**：
- `BRAVE_API_KEY` 未配置
- 需要申请 Brave Search API

**影响**：中等
- 内置搜索功能无法使用
- 限制自动化的搜索能力

---

#### 🟢 **web_fetch (内置)** - 可用

**功能**：
- URL 内容提取（HTML → markdown/text）
- 支持最大字符数限制
- 轻量级页面访问

**用途**：
- 提取网页内容
- 生成摘要
- 文档抓取

---

### 2.3 独立脚本评估

#### 🔴 **ai-research.sh** - 不可用

**依赖**：SearXNG 服务
**问题**：SearXNG 服务不可用
**影响**：AI 信息自动搜索无法执行

---

#### 🔴 **twitter_search_via_web.py** - 不可用

**依赖**：SearXNG 服务
**问题**：SearXNG 服务不可用
**影响**：通过 Web 搜索 Twitter 内容的功能无法使用

---

## 3. 不可用组件问题分析

### 3.1 服务层问题

| 问题组件 | 问题类型 | 严重程度 | 根本原因 |
|---------|---------|---------|---------|
| **SearXNG** | 服务不可用 | 🔴 严重 | 服务未运行或配置错误 |
| **Firecrawl** | API余额不足 | 🟡 中等 | 付费服务限制 |
| **Twitter API** | API余额不足 | 🟡 中等 | 付费服务限制 |
| **Tavily** | 未配置 | 🟢 轻微 | 未申请API Key |
| **Brave Search** | 未配置 | 🟡 中等 | 未申请API Key |

### 3.2 项目层问题

**项目状态**：
- ✅ 文档完整，规划清晰
- ❌ 实际实现为空
- ❌ 工作流未实现
- ❌ 搜索策略未实现
- ❌ 结果处理未实现

**问题总结**：
1. **文档与实现不匹配** - 项目文档描述了完整的架构，但实际目录为空
2. **依赖外部服务** - 核心功能依赖多个付费服务（Firecrawl、Twitter、Tavily）
3. **单一失败点** - SearXNG 作为本地搜索服务，一旦失效影响多个组件
4. **缺乏Fallback机制** - 各技能没有备用搜索源

### 3.3 资源分配问题

**当前资源状态**：
- 付费API余额不足：2个（Firecrawl、Twitter）
- 未配置API：2个（Tavily、Brave）
- 服务不可用：1个（SearXNG）
- 可用资源：2个（web-search-exa、web_fetch）

**成本预估**：
- Firecrawl: $29-99/月（根据使用量）
- Twitter API: $100-5000/月（根据等级）
- Tavily: 免费额度有限
- SearXNG: 免费（需自己部署）

---

## 4. 修复/替换计划

### 4.1 紧急修复（1-2天）

#### 任务 1：修复 SearXNG 服务 🔴 高优先级

**目标**：恢复本地搜索服务

**方案选择**：

**方案 A：重启现有服务**
```bash
# 检查服务状态
systemctl status searxng
docker ps | grep searxng

# 重启服务
systemctl restart searxng
# 或
docker restart searxng-container
```

**方案 B：重新部署 SearXNG**
```bash
# 使用 Docker 部署
git clone https://github.com/searxng/searxng.git
cd searxng
docker compose up -d
```

**方案 C：切换到 localhost**
- 修改 `.env.d/` 中的配置：`SEARXNG_URL=http://localhost:8080`
- 确保本地服务运行

**验证步骤**：
```bash
# 测试服务响应
curl http://localhost:8080/search?q=test&format=json
```

**预期结果**：SearXNG 服务可用，能够返回搜索结果

---

#### 任务 2：配置 web-search-exa MCP 🟢 高优先级

**目标**：确保可用的搜索工具正常工作

**步骤**：
1. 确认 MCP 服务器已连接
2. 测试搜索功能
3. 集成到工作流中

**验证**：
```python
# 通过 MCP 协议测试
web_search_exa({"query": "test", "numResults": 3})
```

---

### 4.2 短期替代方案（3-7天）

#### 任务 1：集成 Brave Search API 🟡 中优先级

**目标**：配置内置 web_search 工具

**步骤**：
1. 申请 Brave Search API Key（免费额度）
   - 访问：https://brave.com/search/api/
   - 注册账号，获取 API Key

2. 配置环境变量
   ```bash
   echo 'export BRAVE_API_KEY="your_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. 测试功能
   ```bash
   web_search "test"
   ```

**预期结果**：内置搜索功能可用

---

#### 任务 2：创建 Fallback 搜索策略 🟡 中优先级

**目标**：为各技能添加备用搜索源

**实现方案**：

```python
# 伪代码：通用搜索策略
class UniversalSearch:
    def __init__(self):
        self.sources = [
            {'name': 'exa', 'enabled': True, 'priority': 1},
            {'name': 'brave', 'enabled': True, 'priority': 2},
            {'name': 'searxng', 'enabled': True, 'priority': 3},
        ]

    def search(self, query, max_results=10):
        for source in sorted(self.sources, key=lambda x: x['priority']):
            if not source['enabled']:
                continue

            try:
                results = self._search_with_source(source['name'], query, max_results)
                if results:
                    return results
            except Exception as e:
                print(f"Failed to search with {source['name']}: {e}")
                continue

        return []

    def _search_with_source(self, source, query, max_results):
        # 实现各个搜索源的调用
        pass
```

**应用范围**：
- `searxng` skill 添加 Exa/Brave fallback
- `firecrawl-search` 添加 Exa/Brave fallback
- `tavily-search` 添加 Exa/Brave fallback

---

### 4.3 中期改进计划（1-2周）

#### 任务 1：实现基础工作流 🟡 中优先级

**目标**：填补空目录，实现规划中的功能

**优先级排序**：

1. **AI 研究搜索** (`workflows/ai-research.sh`)
   ```bash
   # 功能：自动搜索 AI 相关信息
   # 搜索源：Exa + Brave + SearXNG
   # 输出：JSON 报告保存到 memory/ai-research/
   ```

2. **关键词搜索策略** (`strategies/keyword-search.py`)
   ```python
   # 功能：多源关键词搜索
   # 搜索源：Exa, Brave, SearXNG
   # 结果合并与去重
   ```

3. **内容提取器** (`processors/extract-content.py`)
   ```python
   # 功能：从 URL 提取主要内容
   # 工具：web_fetch + readability
   # 输出：纯文本 / markdown
   ```

4. **数据清理器** (`processors/clean-data.py`)
   ```python
   # 功能：清理搜索结果
   # 去重、去噪、结构化
   ```

5. **质量评估器** (`processors/evaluate-quality.py`)
   ```python
   # 功能：评估内容质量
   # 指标：完整性、丰富度、可靠性
   ```

---

#### 任务 2：语义搜索（计划中）🟢 低优先级

**目标**：实现基于向量的语义搜索

**技术方案**：
1. 集成向量数据库（ChromaDB 或 Qdrant）
2. 使用嵌入模型（sentence-transformers）
3. 实现语义相似度搜索

**实施步骤**：
```python
# 伪代码
class SemanticSearch:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_db = ChromaDB()

    def search(self, query, k=10):
        query_embedding = self.embedder.encode(query)
        results = self.vector_db.search(query_embedding, k=k)
        return results

    def add_document(self, doc_id, content):
        embedding = self.embedder.encode(content)
        self.vector_db.add(doc_id, embedding)
```

---

#### 任务 3：迭代搜索（计划中）🟢 低优先级

**目标**：根据初步结果优化搜索词

**实现思路**：
```python
# 伪代码
class IterativeSearch:
    def search(self, initial_query, max_rounds=3):
        results = []
        query = initial_query

        for round in range(max_rounds):
            # 执行搜索
            round_results = self._search(query)
            results.extend(round_results)

            # 分析结果，优化查询
            if self._should_optimize(results):
                query = self._optimize_query(results)
            else:
                break

        return self._deduplicate(results)

    def _optimize_query(self, results):
        # 提取关键词
        keywords = self._extract_keywords(results)
        # 生成新查询
        return " OR ".join(keywords)
```

---

### 4.4 长期规划（1-2月）

#### 任务 1：知识图谱 🟢 低优先级

**目标**：建立领域知识图谱

**技术选型**：
- Neo4j 或 Memgraph
- 实体关系抽取
- 图数据库查询

#### 任务 2：智能推荐 🟢 低优先级

**目标**：基于历史数据推荐相关内容

**实现思路**：
- 用户画像
- 协同过滤
- 内容推荐

#### 任务 3：自定义工作流 🟢 低优先级

**目标**：支持用户定义自己的工作流

**实现方案**：
- YAML 配置文件
- 工作流引擎
- 可视化编辑器

---

## 5. 开发优先级建议

### 5.1 紧急任务（24小时内）

| 优先级 | 任务 | 预计时间 | 价值 |
|--------|------|---------|------|
| 🔴 P0 | 修复 SearXNG 服务 | 1-2小时 | 恢复核心搜索能力 |
| 🔴 P0 | 测试 web-search-exa | 30分钟 | 确认可用工具 |
| 🟡 P1 | 配置 Brave Search API | 1小时 | 增加备用搜索源 |

### 5.2 短期任务（3-7天）

| 优先级 | 任务 | 预计时间 | 价值 |
|--------|------|---------|------|
| 🟡 P1 | 实现通用搜索策略 | 4-6小时 | 提高可用性 |
| 🟡 P1 | 实现 AI 研究工作流 | 2-3小时 | 自动化信息搜集 |
| 🟡 P2 | 实现关键词搜索策略 | 2-3小时 | 完善搜索功能 |
| 🟢 P2 | 实现内容提取器 | 2-3小时 | 数据处理能力 |
| 🟢 P3 | 实现数据清理器 | 1-2小时 | 数据质量提升 |

### 5.3 中期任务（1-2周）

| 优先级 | 任务 | 预计时间 | 价值 |
|--------|------|---------|------|
| 🟢 P3 | 实现质量评估器 | 3-4小时 | 内容质量控制 |
| 🟢 P4 | 实现语义搜索 | 8-12小时 | 提升搜索精度 |
| 🟢 P4 | 实现迭代搜索 | 4-6小时 | 智能化优化 |

### 5.4 长期任务（1-2月）

| 优先级 | 任务 | 预计时间 | 价值 |
|--------|------|---------|------|
| 🟢 P5 | 建立知识图谱 | 2-3周 | 深度语义理解 |
| 🟢 P5 | 智能推荐系统 | 1-2周 | 个性化体验 |
| 🟢 P6 | 自定义工作流 | 2-3周 | 灵活性提升 |

---

## 6. 资源需求评估

### 6.1 成本估算

| 服务 | 免费额度 | 付费计划 | 建议 |
|------|---------|---------|------|
| **SearXNG** | 无限（自部署） | 免费 | ✅ 使用此方案 |
| **web-search-exa** | 有限（MCP） | 待确认 | ✅ 优先使用 |
| **Brave Search** | 2,000次/月 | $0.0025/次 | ✅ 申请免费额度 |
| **Firecrawl** | 500次/月 | $29-99/月 | ⚠️ 暂不充值 |
| **Twitter API** | 有限 | $100-5000/月 | ⚠️ 暂不充值 |
| **Tavily** | 1,000次/月 | $0.001/次 | ✅ 申请免费额度 |

### 6.2 技术资源

| 资源类型 | 现有需求 | 建议配置 |
|---------|---------|---------|
| **存储空间** | ~100MB（缓存） | 1GB |
| **内存** | 未知 | 2GB+ |
| **CPU** | 未知 | 2核+ |
| **网络带宽** | 中等 | 高（搜索频繁） |

---

## 7. 风险评估与缓解

### 7.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| **SearXNG 无法恢复** | 严重 | 中 | 配置多个备用搜索源 |
| **API 余额持续不足** | 中等 | 高 | 使用免费服务优先 |
| **付费服务涨价** | 中等 | 低 | 自建服务为主 |
| **网络连接不稳定** | 轻微 | 中 | 实现重试机制 |

### 7.2 项目风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| **文档与实现不匹配** | 中等 | 高 | 立即开始实现工作流 |
| **过度依赖外部服务** | 严重 | 中 | 建立自建服务优先 |
| **功能复杂度过高** | 中等 | 中 | 分阶段实现，MVP优先 |
| **用户需求变化** | 轻微 | 低 | 保持架构灵活性 |

---

## 8. 推荐行动计划

### 第一阶段：紧急恢复（24小时）

1. **修复 SearXNG 服务**
   ```bash
   # 执行命令
   docker ps | grep searxng
   # 或
   systemctl status searxng
   ```

2. **测试 web-search-exa**
   - 确认 MCP 连接
   - 执行测试搜索

3. **申请 Brave Search API**
   - 访问：https://brave.com/search/api/
   - 获取 API Key

### 第二阶段：基础实现（3-7天）

1. **实现通用搜索策略**
   - 多源搜索集成
   - 自动 fallback
   - 结果合并

2. **实现 AI 研究工作流**
   - 自动搜索
   - 结果保存
   - 报告生成

3. **实现基础处理器**
   - 内容提取
   - 数据清理
   - 质量评估

### 第三阶段：功能完善（1-2周）

1. **实现语义搜索**
   - 向量数据库
   - 嵌入模型
   - 相似度搜索

2. **实现迭代搜索**
   - 查询优化
   - 多轮搜索
   - 结果筛选

3. **完善文档**
   - 使用指南
   - API 文档
   - 示例代码

---

## 9. 成功指标

### 9.1 短期指标（1周内）

- [x] SearXNG 服务恢复并稳定运行
- [x] 至少 2 个搜索源可用（SearXNG + Exa/Brave）
- [x] AI 研究工作流正常运行
- [x] 搜索结果成功率 > 95%

### 9.2 中期指标（1月内）

- [x] 3 个搜索策略实现（关键词、语义、迭代）
- [x] 3 个处理器实现（提取、清理、评估）
- [x] 2 个工作流实现（AI 研究、市场调研）
- [x] 平均搜索时间 < 3秒

### 9.3 长期指标（3月内）

- [x] 知识图谱建立
- [x] 智能推荐系统上线
- [x] 自定义工作流支持
- [x] 用户满意度 > 4.5/5.0

---

## 10. 总结

### 10.1 核心发现

1. **项目状态**：文档完整，实现缺失
2. **资源可用性**：5个技能中只有1个可用
3. **依赖问题**：过度依赖付费服务
4. **单一失败点**：SearXNG 失效影响多个组件

### 10.2 关键建议

1. **立即行动**：修复 SearXNG 服务
2. **优先使用免费服务**：web-search-exa、Brave Search
3. **实现 fallback 机制**：避免单点失败
4. **分阶段实现**：MVP 优先，逐步完善

### 10.3 项目展望

信息搜集项目是一个有价值的方向，但目前处于规划阶段，需要：

1. 填补实现空白（空目录）
2. 建立稳定的基础设施
3. 实现核心工作流
4. 提供用户友好的接口

**预计完成时间**：基础功能 1-2周，完整功能 1-2月

---

**报告结束**
*评估人：Clawdbot AI Assistant*
*评估日期：2026-02-05*
