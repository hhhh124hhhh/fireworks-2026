---
name: x-prompt-hunter
description: AI 提示词系统 - 集成语义去重、多源抓取、LLM 评估和 Langfuse 追踪
metadata: {"clawdbot":{"emoji":"🎯","requires":{"anyBins":["python3"]},"env":["GITHUB_TOKEN","HUGGINGFACE_TOKEN","ANTHROPIC_API_KEY","LANGFUSE_PUBLIC_KEY","LANGFUSE_SECRET_KEY"]}}
---

# AI 提示词系统 (x-prompt-hunter)

**数据发现层** - 智能的提示词管理平台，集成了语义去重、多源抓取、LLM 质量评估和实时追踪功能。

**架构定位**：
```
┌─────────────────────┐
│ x-prompt-hunter     │ ← 数据发现层（去重+评估）
└─────────┬───────────┘
        │ 高质量提示词
        ▼
┌─────────────────────┐
│ prompt-to-skill-    │ ← 转换发布层（SKILL.md + ClawdHub）
│ converter          │
└─────────────────────┘
```

**与 prompt-to-skill-converter 的关系**：
- 本技能负责：去重、评估、生成高质量提示词列表
- prompt-to-skill-converter 负责：将高质量提示词转换为 Skills 并发布到 ClawdHub
- 建议工作流：先使用 x-prompt-hunter 生成高质量提示词，然后使用 prompt-to-skill-converter 进行转换和发布

## 功能特性

### 1. 语义去重 🔄
- 使用 `sentence-transformers` 计算提示词之间的语义相似度
- 默认相似度阈值 0.85，可配置
- 自动过滤重复或高度相似的提示词
- 保存详细的去重记录用于追踪

**用途：**
- 清理重复的提示词库
- 提高提示词集合的多样性
- 减少冗余存储和计算

### 2. 多源数据抓取 🌐
- **GitHub API**：从优质仓库抓取提示词
  - 支持指定仓库列表
  - 代码搜索功能
  - 自动解析多种格式
- **HuggingFace API**：访问高质量提示词数据集
  - 支持多个数据集
  - 批量加载和处理
  - 自动提取提示词字段
- **统一搜索接口**：一键从所有源获取提示词

**用途：**
- 扩展提示词库
- 收集社区优质提示词
- 持续更新提示词资源

### 3. LLM-as-Judge 评估框架 ⚖️
- 使用 **Claude API** 进行专业评估
- 四大评估维度：
  - **创新性** (1-10分)：独特性和创造性
  - **实用性** (1-10分)：实际应用价值
  - **清晰度** (1-10分)：表达明确性
  - **可复用性** (1-10分)：场景适应性
- 批量评估功能
- 生成详细的质量报告

**用途：**
- 评估提示词质量
- 筛选高质量提示词
- 获取改进建议

### 4. Langfuse 质量追踪 📊
- 实时追踪每次评估的详细数据
- 生成质量趋势报告
- 对比不同时间段的质量指标
- 支持自定义指标和分析

**用途：**
- 监控提示词质量变化
- 追踪系统性能
- 生成可视化报告

## 安装依赖

```bash
cd /root/clawd/skills/x-prompt-hunter
pip install -r requirements.txt
```

**主要依赖：**
- `sentence-transformers` - 语义相似度计算
- `PyGithub` - GitHub API
- `datasets` - HuggingFace 数据集
- `anthropic` - Claude API
- `langfuse` - 质量追踪
- `pyyaml` - 配置管理

## 环境变量

在 `~/.bashrc` 或 `.env` 文件中配置以下变量：

```bash
# GitHub API (可选，用于抓取 GitHub 提示词)
export GITHUB_TOKEN="your_github_token"

# HuggingFace Token (可选，用于访问数据集)
export HUGGINGFACE_TOKEN="your_huggingface_token"

# Claude API (必需，用于评估功能)
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# Langfuse (可选，用于质量追踪)
export LANGFUSE_PUBLIC_KEY="your_public_key"
export LANGFUSE_SECRET_KEY="your_secret_key"
```

**获取 API 密钥：**
- GitHub: Settings → Developer settings → Personal access tokens
- HuggingFace: Account settings → Access tokens
- Anthropic: https://console.anthropic.com/
- Langfuse: https://cloud.langfuse.com/

## 使用方法

### 1. 运行完整流程 (推荐)

```bash
python3 /root/clawd/skills/x-prompt-hunter/main.py pipeline \
  --query "creative writing" \
  --limit 50 \
  --batch-size 10 \
  --evaluate-limit 20
```

这将执行：
- 从所有数据源抓取提示词
- 语义去重
- 评估前20个提示词
- 生成质量报告

### 2. 单独使用各功能

#### 抓取提示词
```bash
python3 main.py fetch --query "chatbot prompt" --limit 100
```

#### 语义去重
```bash
python3 main.py deduplicate --input data/prompts.json --output data/prompts_clean.json
```

#### 评估提示词
```bash
python3 main.py evaluate --input data/prompts.json --batch-size 10
```

#### 生成报告
```bash
# 趋势报告
python3 main.py report --type trend --days 30

# 对比报告
python3 main.py report --type comparison --days1 30 --days2 30

# 导出指标
python3 main.py report --type metrics
```

### 3. 使用配置文件

编辑 `config.yaml` 自定义所有参数：

```yaml
semantic_dedup:
  similarity_threshold: 0.85
  model_name: "all-MiniLM-L6-v2"

llm_judge:
  model: "claude-3-5-sonnet-20241022"
  batch_size: 10

langfuse:
  project_name: "prompt-hunter"
```

## 配置说明

### config.yaml 结构

```yaml
# 语义去重配置
semantic_dedup:
  enabled: true
  model_name: "all-MiniLM-L6-v2"
  similarity_threshold: 0.85
  log_file: "data/deduplication_log.json"

# GitHub 配置
github:
  enabled: true
  token: ""  # 从环境变量读取
  repos:
    - "f/awesome-chatgpt-prompts"
  output_file: "data/github_prompts.json"

# HuggingFace 配置
huggingface:
  enabled: true
  datasets:
    - "Gustavosta/Stable-Diffusion-Prompts"
  output_file: "data/hf_prompts.json"

# LLM 评估配置
llm_judge:
  enabled: true
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
  output_file: "data/evaluation_results.json"

# Langfuse 追踪配置
langfuse:
  enabled: true
  project_name: "prompt-hunter"
  output_dir: "data/langfuse_reports"
```

## 输出文件

所有输出文件保存在 `data/` 目录：

- `prompts.json` - 抓取的原始提示词
- `prompts_deduplicated.json` - 去重后的提示词
- `deduplication_log.json` - 去重日志
- `evaluation_results.json` - 评估结果
- `langfuse_reports/` - Langfuse 报告
  - `trend_report_YYYYMMDD.json` - 趋势报告
  - `comparison_YYYYMMDD.json` - 对比报告
  - `metrics_YYYYMMDD.json` - 指标数据

日志文件：`logs/prompt_hunter.log`

## 示例工作流

### 场景1：收集并评估创意提示词

```bash
# 1. 抓取
python3 main.py fetch --query "creative writing prompts" --limit 100

# 2. 去重
python3 main.py deduplicate

# 3. 评估（前30个）
python3 main.py evaluate --batch-size 5 | head -n 10

# 4. 生成报告
python3 main.py report --type trend
```

### 场景2：持续监控质量

```bash
# 每周运行完整流程
python3 main.py pipeline --query "system prompt" --limit 50

# 对比本周与上周
python3 main.py report --type comparison --days1 7 --days2 14
```

## 高级用法

### 自定义语义去重阈值

编辑 `config.yaml`：
```yaml
semantic_dedup:
  similarity_threshold: 0.90  # 更严格
```

### 添加新的 GitHub 仓库

```yaml
github:
  repos:
    - "f/awesome-chatgpt-prompts"
    - "your-org/your-repo"  # 添加新仓库
```

### 添加新的 HuggingFace 数据集

```yaml
huggingface:
  datasets:
    - "Gustavosta/Stable-Diffusion-Prompts"
    - "your-dataset-name"  # 添加新数据集
```

## 故障排查

### 问题：sentence-transformers 模型下载慢

**解决：** 预先下载模型或使用镜像
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sentence-transformers
```

### 问题：Claude API 评估失败

**检查：**
1. `ANTHROPIC_API_KEY` 是否正确设置
2. API key 是否有足够余额
3. 查看日志 `logs/prompt_hunter.log`

### 问题：Langfuse 追踪失败

**检查：**
1. Langfuse 公钥和私钥是否正确
2. 网络连接是否正常
3. 查看 Langfuse 控制台

## 技术架构

```
x-prompt-hunter/
├── main.py                 # 主入口
├── config.yaml            # 配置文件
├── requirements.txt       # 依赖
├── src/
│   ├── semantic_dedup.py   # 语义去重
│   ├── github_hf_fetcher.py # 数据源抓取
│   ├── llm_judge.py       # LLM 评估
│   └── langfuse_tracker.py # Langfuse 追踪
├── data/                  # 数据目录
│   ├── prompts.json
│   ├── evaluation_results.json
│   └── ...
└── logs/                  # 日志目录
    └── prompt_hunter.log
```

## 性能优化建议

1. **批量评估**：调整 `batch_size` 以平衡速度和API成本
2. **限制抓取**：合理设置 `limit` 避免过量数据
3. **去重阈值**：根据需求调整 `similarity_threshold`
4. **增量更新**：定期运行而非全量抓取

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License
