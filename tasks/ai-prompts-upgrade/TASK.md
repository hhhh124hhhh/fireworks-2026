# AI 提示词技术升级任务

## 任务概述

根据 `/root/clawd/research/ai-prompts-industry-research.md` 的研究报告，需要实现以下四个核心功能。

---

## 任务 1: 引入 sentence-transformers 实现语义去重

### 目标
实现基于语义相似度的提示词去重系统，替代当前简单的字符串匹配去重。

### 具体要求

1. **安装依赖**
   ```bash
   pip install sentence-transformers scikit-learn numpy
   ```

2. **核心功能**
   - 使用预训练模型：`all-MiniLM-L6-v2`
   - 计算提示词文本的嵌入向量
   - 使用余弦相似度计算文本间的语义相似度
   - 设置去重阈值：0.85（相似度 > 0.85 视为重复）
   - 保留相似组中评分最高或最长的提示词

3. **代码结构**
   ```
   /root/clawd/services/semantic-dedup/
   ├── __init__.py
   ├── deduplicator.py      # 核心去重逻辑
   ├── models.py            # 模型加载和管理
   ├── config.py            # 配置参数
   └── README.md            # 使用文档
   ```

4. **关键函数**
   ```python
   class SemanticDeduplicator:
       def __init__(self, model_name='all-MiniLM-L6-v2', threshold=0.85):
           """初始化去重器"""
           pass

       def encode_texts(self, texts):
           """批量计算文本嵌入"""
           pass

       def deduplicate(self, prompts):
           """去重提示词列表"""
           pass

       def find_similar_groups(self, embeddings, threshold=0.85):
           """查找相似文本组"""
           pass
   ```

5. **性能优化**
   - 批量计算嵌入（batch_size=32）
   - 缓存已计算的嵌入
   - 支持增量去重

6. **测试**
   - 创建测试数据集（包含明显重复和语义相似的文本）
   - 验证去重准确率 > 90%
   - 测试处理速度（1000条文本 < 10秒）

---

## 任务 2: 集成 GitHub API 和 HuggingFace

### 目标
扩展数据源，从 GitHub 和 HuggingFace 获取高质量提示词。

### 具体要求

1. **GitHub API 集成**
   ```bash
   pip install PyGithub
   ```

   - 搜索高星仓库（关键词：prompt engineering, AI prompts）
   - 下载仓库内容（README、.md 文件、scripts）
   - 提取提示词相关内容
   - 遵守 API 速率限制（5000 req/h 认证用户）

2. **HuggingFace 集成**
   ```bash
   pip install huggingface_hub datasets
   ```

   - 访问提示词相关数据集
   - 下载数据集内容
   - 解析并提取提示词
   - 处理不同的数据格式（JSON, CSV, Parquet）

3. **代码结构**
   ```
   /root/clawd/services/data-collector/
   ├── __init__.py
   ├── github_collector.py   # GitHub API 集成
   ├── huggingface_collector.py  # HuggingFace 集成
   ├── base_collector.py     # 基础收集器类
   └── README.md
   ```

4. **关键函数**
   ```python
   class GitHubCollector:
       def search_repos(self, query, min_stars=100, limit=20):
           """搜索仓库"""
           pass

       def extract_prompts_from_repo(self, repo_url):
           """从仓库提取提示词"""
           pass

   class HuggingFaceCollector:
       def search_datasets(self, query, limit=10):
           """搜索数据集"""
           pass

       def extract_prompts_from_dataset(self, dataset_id):
           """从数据集提取提示词"""
           pass
   ```

5. **高质量数据源**
   - GitHub: `f/awesome-chatgpt-prompts` (170k stars)
   - HuggingFace: `fka/awesome-chatgpt-prompts`
   - HuggingFace: `data-is-better-together/10k_prompts_ranked`

6. **错误处理**
   - API 速率限制处理（自动重试）
   - 网络错误重试机制
   - 数据格式异常处理

---

## 任务 3: 实现 LLM-as-Judge 评估框架

### 目标
使用 LLM (GPT-4) 对提示词进行多维度质量评估。

### 具体要求

1. **评估维度**
   - 清晰度 (25分): 提示词是否明确、易懂
   - 完整性 (25分): 是否包含足够的上下文和示例
   - 实用性 (25分): 是否有实际应用价值
   - 创新性 (25分): 是否有独特的思路或技巧

2. **代码结构**
   ```
   /root/clawd/services/llm-evaluator/
   ├── __init__.py
   ├── evaluator.py         # 评估器核心
   ├── prompts.py           # 评估提示词模板
   ├── cost_tracker.py      # API 成本追踪
   └── README.md
   ```

3. **关键函数**
   ```python
   class LLMEvaluator:
       def __init__(self, model='gpt-4'):
           """初始化评估器"""
           pass

       async def evaluate_prompt(self, prompt_text):
           """评估单个提示词"""
           pass

       async def evaluate_batch(self, prompts, batch_size=10):
           """批量评估提示词"""
           pass

       def calculate_cost(self, num_prompts):
           """计算预估成本"""
           pass
   ```

4. **评估提示词模板**
   ```python
   EVALUATION_SYSTEM_PROMPT = """
   你是一位专业的 AI 提示词质量评估专家。

   请评估以下提示词的质量，从 0-100 打分：

   评分维度（每项 25 分）：
   1. 清晰度: 提示词是否明确、易懂，没有歧义
   2. 完整性: 是否包含足够的上下文、示例和约束条件
   3. 实用性: 是否有实际应用价值，能否解决具体问题
   4. 创新性: 是否有独特的思路、技巧或新颖的表达方式

   请以 JSON 格式返回：
   {
     "total_score": 85,
     "clarity": 20,
     "completeness": 22,
     "usefulness": 23,
     "innovation": 20,
     "reasoning": "说明理由..."
   }
   """
   ```

5. **成本优化**
   - 批量评估（10个提示词/次）
   - 使用 GPT-3.5 预筛，GPT-4 精评
   - 缓存相似提示词的评估结果

6. **与现有系统集成**
   - 与 `/root/clawd/scripts/evaluate-prompts-quality.js` 整合
   - 规则评分 + LLM 评分的混合评估
   - 规则评分 < 30 的直接淘汰，不调用 LLM

---

## 任务 4: 部署 Langfuse 进行质量追踪

### 目标
集成 Langfuse 进行提示词版本管理、评估追踪和持续监控。

### 具体要求

1. **安装和配置**
   ```bash
   pip install langfuse
   ```

2. **配置文件**
   ```python
   # /root/clawd/config/langfuse_config.py
   LANGFUSE_PUBLIC_KEY = "pk-..."
   LANGFUSE_SECRET_KEY = "sk-..."
   LANGFUSE_HOST = "https://cloud.langfuse.com"  # 或自托管地址
   ```

3. **代码结构**
   ```
   /root/clawd/services/langfuse-tracker/
   ├── __init__.py
   ├── tracker.py           # 追踪器核心
   ├── prompt_manager.py     # 提示词版本管理
   ├── metrics_collector.py # 指标收集
   └── README.md
   ```

4. **关键功能**
   - 提示词版本管理（记录每次修改）
   - 评估结果追踪（记录 LLM 评估结果）
   - 用户反馈收集（评分、评论）
   - 性能指标监控（处理速度、成功率）
   - 质量趋势分析（评分变化趋势）

5. **关键函数**
   ```python
   class LangfuseTracker:
       def track_prompt_version(self, prompt_id, version, content):
           """追踪提示词版本"""
           pass

       def log_evaluation(self, prompt_id, evaluation_result):
           """记录评估结果"""
           pass

       def log_user_feedback(self, prompt_id, user_id, rating, comment):
           """记录用户反馈"""
           pass

       def get_prompt_versions(self, prompt_id):
           """获取提示词版本历史"""
           pass

       def get_quality_trends(self, days=30):
           """获取质量趋势"""
           pass
   ```

6. **集成到评估流程**
   ```python
   # 在评估完成后自动记录
   tracker.log_evaluation(
       prompt_id=prompt['id'],
       evaluation_result={
           "score": llm_score,
           "rule_score": rule_score,
           "dimensions": dimensions
       }
   )
   ```

7. **Dashboard**
   - Langfuse 提供现成的可视化界面
   - 查看提示词版本对比
   - 分析评估结果分布
   - 监控系统健康状况

---

## 执行优先级

按照以下顺序执行（依赖关系）：

1. **任务 1**: 语义去重（基础功能）
2. **任务 2**: GitHub/HuggingFace 集成（数据源扩展）
3. **任务 3**: LLM-as-Judge 评估（质量提升）
4. **任务 4**: Langfuse 部署（监控追踪）

---

## 输出要求

### 每个任务完成后输出：

1. **代码文件**
   - 完整可用的代码
   - 中文注释
   - 错误处理和日志

2. **文档**
   - README.md（使用说明）
   - API 文档（如需要）
   - 配置说明

3. **测试**
   - 单元测试（使用 pytest）
   - 测试报告
   - 性能基准

4. **报告**
   - 功能总结
   - 已知问题
   - 后续建议

### 最终输出：

- `/root/clawd/reports/ai-prompts-upgrade-summary.md`
  - 四个任务的完成情况
  - 整体架构说明
  - 使用指南
  - 下一步计划

---

## 注意事项

1. **使用中文注释和文档**
2. **代码要有错误处理和日志记录**
3. **遵守 API 速率限制**
4. **优化 LLM API 成本**
5. **代码要可测试、可维护**
6. **遇到问题及时报告，不要卡住**
7. **定期保存进度**

---

## 预期成果

### 短期（1-2 周）

- ✅ 语义去重系统上线
- ✅ GitHub/HuggingFace 数据源集成
- ✅ LLM 评估框架可用
- ✅ Langfuse 监控部署

### 中期（3-4 周）

- 数据收集量提升 200%
- 去重准确率 > 90%
- 评估准确率 > 85%
- 建立质量追踪体系

---

## 开始执行

请按照上述要求逐个实现这四个任务。每个任务完成后，向主会话报告进度和成果。
