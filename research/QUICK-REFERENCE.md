# AI 提示词收集与评估 - 快速参考指南

## 核心代码片段

### 1. 语义去重

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 初始化模型
model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_deduplicate(prompts, threshold=0.85):
    """
    使用语义相似度去重
    prompts: List[dict] - [{'text': '...', 'metadata': {...}}]
    threshold: float - 相似度阈值（推荐 0.85）
    """
    # 计算嵌入
    texts = [p['text'] for p in prompts]
    embeddings = model.encode(texts)

    # 计算相似度矩阵
    similarity_matrix = cosine_similarity(embeddings)

    # 去重
    unique_prompts = []
    seen_indices = set()

    for i, prompt in enumerate(prompts):
        if i in seen_indices:
            continue

        # 找到相似提示词
        similar = [j for j, sim in enumerate(similarity_matrix[i])
                 if sim > threshold]

        # 保留最长的
        best_idx = max(similar, key=lambda x: len(prompts[x]['text']))

        unique_prompts.append(prompts[best_idx])
        seen_indices.update(similar)

    return unique_prompts

# 使用
unique = semantic_deduplicate(collected_prompts)
print(f"去重: {len(collected_prompts)} → {len(unique)}")
```

### 2. GitHub 数据收集

```python
from github import Github

def collect_from_github(token, query, max_repos=20):
    """
    从 GitHub 收集提示词
    token: GitHub Personal Access Token
    query: 搜索查询
    max_repos: 最大仓库数
    """
    g = Github(token)

    # 搜索仓库
    repos = g.search_repos(
        query,
        sort="stars",
        order="desc"
    )

    prompts = []
    for repo in repos[:max_repos]:
        # 获取文件列表
        contents = repo.get_contents("")
        for content in contents:
            # 跳过非文本文件
            if not content.name.endswith(('.md', '.txt', '.py')):
                continue

            # 读取文件
            file_content = repo.get_contents(content.path)
            text = file_content.decoded_content.decode('utf-8')

            # 提取提示词（使用正则或 NLP）
            extracted = extract_prompts_from_text(text)

            prompts.extend(extracted)

    return prompts

# 使用
prompts = collect_from_github(
    GITHUB_TOKEN,
    "prompt engineering",
    max_repos=20
)
```

### 3. HuggingFace 数据集

```python
from huggingface_hub import list_datasets, login

def collect_from_huggingface(token, filter_term="prompts", limit=10):
    """
    从 HuggingFace 收集数据集
    """
    login(token=token)

    # 列出数据集
    datasets = list_datasets(
        filter=filter_term,
        limit=limit,
        sort="downloads",
        direction=-1
    )

    prompts = []
    for dataset in datasets:
        # 加载数据集
        from datasets import load_dataset
        ds = load_dataset(dataset.id, split='train')

        # 提取提示词
        for item in ds:
            if 'prompt' in item:
                prompts.append({
                    'text': item['prompt'],
                    'source': f'huggingface:{dataset.id}'
                })

    return prompts

# 使用
prompts = collect_from_huggingface(
    HF_TOKEN,
    filter_term="prompts"
)
```

### 4. LLM-as-Judge 评估

```python
import openai

client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

async def evaluate_with_llm(prompt_text):
    """
    使用 GPT-4 评估提示词质量
    """
    system_prompt = """
    评估以下提示词的质量（0-100分）：

    评分维度：
    1. 清晰度 (25分): 提示词是否明确、易懂？
    2. 完整性 (25分): 是否包含足够的上下文和示例？
    3. 实用性 (25分): 是否有实际应用价值？
    4. 创新性 (25分): 是否有独特的思路或技巧？

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

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"提示词: {prompt_text}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    result = json.loads(response.choices[0].message.content)
    return result

# 批量评估
async def batch_evaluate(prompts, batch_size=10):
    results = []
    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        tasks = [evaluate_with_llm(p['text']) for p in batch]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
    return results
```

### 5. 规则评分

```python
import re

def rule_based_score(prompt):
    """
    基于规则的质量评分
    """
    score = 0
    text = prompt['text']

    # 1. 长度适中 (20分)
    if 50 <= len(text) <= 500:
        score += 20
    elif len(text) > 500:
        score += 10

    # 2. 包含示例 (20分)
    if '例如' in text or 'example' in text.lower():
        score += 20

    # 3. 结构清晰 (20分)
    if any(marker in text for marker in ['1.', '-', '*', '•']):
        score += 20

    # 4. 明确的目标 (20分)
    if any(word in text for word in ['请', '创建', '生成', 'write', 'create']):
        score += 20

    # 5. 无敏感词 (20分)
    sensitive_words = ['密码', 'private', 'hack', 'exploit']
    if not any(word in text.lower() for word in sensitive_words):
        score += 20

    return score

# 快速过滤
def low_quality_filter(prompts, threshold=30):
    """过滤低质量提示词"""
    return [p for p in prompts if rule_based_score(p) > threshold]
```

## 安装命令

### 核心依赖

```bash
# 语义去重
pip install sentence-transformers scikit-learn

# LLM 评估
pip install openai anthropic

# GitHub API
pip install PyGithub

# HuggingFace
pip install huggingface_hub datasets

# RSS/搜索
pip install feedparser httpx

# 数据库
pip install asyncpg redis

# API 框架
pip install fastapi uvicorn

# 任务队列
pip install celery redis

# 评估工具
pip install promptfoo

# 监控
pip install langfuse
```

### NLP 工具

```bash
# spaCy
pip install spacy
python -m spacy download zh_core_web_sm
python -m spacy download en_core_web_sm

# NLTK
pip install nltk
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# 正则增强
pip install regex
```

## 配置示例

### promptfoo 配置

```yaml
# promptfooconfig.yaml
prompts:
  - id: writer_v1
    content: |
      你是一个专业的写作助手。请撰写一篇关于 {{topic}} 的文章。

  - id: writer_v2
    content: |
      作为一位经验丰富的作家，请创作一篇关于 {{topic}} 的文章。
      要求：
      1. 结构清晰，包含引言、正文、结论
      2. 语言生动，使用具体例子
      3. 逻辑连贯，层次分明

providers:
  - id: openai:gpt-4
    config:
      temperature: 0.7
      max_tokens: 2000

  - id: openai:gpt-3.5-turbo
    config:
      temperature: 0.7
      max_tokens: 2000

tests:
  - description: "AI 文章"
    vars:
      topic: "人工智能的未来"
    assert:
      - type: similar
        value: "人工智能技术进步"
        threshold: 0.7
      - type: contains
        value: "技术"

  - description: "环保文章"
    vars:
      topic: "环境保护"
    assert:
      - type: similar
        value: "生态保护措施"
        threshold: 0.7
```

运行：
```bash
promptfoo eval -c promptfooconfig.yaml -o html
```

### Langfuse 配置

```python
from langfuse import Langfuse

# 初始化
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
)

# 创建提示词版本
prompt = langfuse.create_prompt(
    name="writing_assistant",
    prompt="你是一个专业的写作助手，擅长撰写各类文章...",
    config={
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 2000
    }
)

# 记录评估
evaluation = langfuse.score(
    name="quality_score",
    value=0.85,
    comment="优秀的结构和语言表达",
    trace_id=prompt.id,
    prompt_id=prompt.id
)

# 查询版本历史
versions = langfuse.get_prompt_versions("writing_assistant")
for version in versions:
    print(f"Version {version.version}: {version.prompt[:50]}...")
```

## 数据库 Schema

### PostgreSQL + pgvector

```sql
-- 提示词表
CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    source VARCHAR(100),
    source_url TEXT,
    category VARCHAR(50),
    tags JSONB,
    rule_score INTEGER CHECK (rule_score >= 0 AND rule_score <= 100),
    llm_score JSONB,
    embedding VECTOR(384),  -- all-MiniLM-L6-v2 输出 384 维
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 评估表
CREATE TABLE evaluations (
    id SERIAL PRIMARY KEY,
    prompt_id INTEGER REFERENCES prompts(id),
    evaluator VARCHAR(50),  -- 'llm' or 'human'
    score JSONB,
    reasoning TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- A/B 测试表
CREATE TABLE ab_tests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    prompt_a_id INTEGER REFERENCES prompts(id),
    prompt_b_id INTEGER REFERENCES prompts(id),
    test_cases JSONB,
    results JSONB,
    winner INTEGER REFERENCES prompts(id),
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- 用户反馈表
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    prompt_id INTEGER REFERENCES prompts(id),
    user_id VARCHAR(100),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_prompts_category ON prompts(category);
CREATE INDEX idx_prompts_source ON prompts(source);
CREATE INDEX idx_prompts_embedding ON prompts USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_prompts_created_at ON prompts(created_at DESC);
```

## 常用查询

### 相似提示词搜索

```python
async def find_similar_prompts(conn, query_text, limit=10, threshold=0.7):
    """
    使用向量相似度搜索
    """
    # 计算查询嵌入
    embedding = model.encode(query_text)

    # 向量搜索
    query = """
        SELECT id, text, source, rule_score,
               1 - (embedding <=> $1) as similarity
        FROM prompts
        WHERE 1 - (embedding <=> $1) > $2
        ORDER BY similarity DESC
        LIMIT $3
    """

    async with conn.cursor() as cur:
        await cur.execute(query, (embedding.tolist(), threshold, limit))
        results = await cur.fetchall()

    return results
```

### 质量评分统计

```sql
SELECT
    category,
    AVG(rule_score) as avg_rule_score,
    AVG((llm_score->>'total_score')::float) as avg_llm_score,
    COUNT(*) as count
FROM prompts
GROUP BY category
ORDER BY avg_llm_score DESC;
```

### 热门提示词

```sql
SELECT
    p.id,
    p.text,
    p.source,
    AVG(f.rating) as avg_rating,
    COUNT(f.id) as feedback_count
FROM prompts p
LEFT JOIN feedback f ON p.id = f.prompt_id
WHERE f.created_at > NOW() - INTERVAL '7 days'
GROUP BY p.id
ORDER BY avg_rating DESC, feedback_count DESC
LIMIT 20;
```

## 监控指标

### 关键指标

```python
from prometheus_client import Counter, Histogram, Gauge

# 收集指标
prompts_collected = Counter('prompts_collected_total', 'Total prompts collected', ['source'])
prompts_deduplicated = Counter('prompts_deduplicated_total', 'Total prompts deduplicated')
prompts_evaluated = Counter('prompts_evaluated_total', 'Total prompts evaluated')

# 质量指标
avg_score = Gauge('prompt_avg_score', 'Average prompt score', ['type'])
high_quality_ratio = Gauge('prompt_high_quality_ratio', 'Ratio of high quality prompts')

# 性能指标
processing_time = Histogram('prompt_processing_seconds', 'Time spent processing prompts')
evaluation_time = Histogram('prompt_evaluation_seconds', 'Time spent evaluating prompts')

# 使用
prompts_collected.labels(source='github').inc(100)
avg_score.labels(type='rule').set(65.3)
processing_time.observe(1.5)
```

## 常见问题

### Q1: 语义去重太慢怎么办？

**A**: 使用 FAISS 加速
```python
import faiss

# 构建索引
index = faiss.IndexFlatIP(384)  # 384 维
index.add(embeddings)

# 搜索（更快）
distances, indices = index.search(query_embedding, k=10)
```

### Q2: LLM 评估成本高怎么办？

**A**: 混合策略
1. 规则评分预筛（< 30 分直接淘汰）
2. 批量评估（10 个提示词/次）
3. 使用 GPT-3.5 预筛，GPT-4 精评
4. 缓存相似提示词的评估结果

### Q3: 如何选择去重阈值？

**A**: 根据数据集调整
- 严格（0.9+）：去重率高，可能误杀
- 宽松（0.8-0.85）：平衡
- 实验：在验证集上测试不同阈值

### Q4: 支持中文提示词吗？

**A**: 支持
```python
# 使用多语言模型
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# 或者使用中文专用模型
model = SentenceTransformer('shibing624/text2vec-base-chinese')
```

## 下一步

1. **安装依赖**: 按照安装命令配置环境
2. **原型验证**: 实现语义去重 + LLM 评估原型
3. **数据库部署**: 设置 PostgreSQL + pgvector
4. **API 开发**: 实现 FastAPI 基础接口
5. **集成工具**: 部署 promptfoo + Langfuse

---

**更新**: 2026-01-31
**版本**: v1.0
