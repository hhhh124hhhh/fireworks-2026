# AI 提示词系统 (x-prompt-hunter)

> 🎯 智能提示词管理平台 - 集成语义去重、多源抓取、LLM 评估和实时追踪

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📖 简介

AI 提示词系统是一个功能完整的提示词管理平台，帮助你从多个来源收集、清理、评估和追踪高质量的 AI 提示词。

### 核心功能

- 🔄 **语义去重**: 使用 sentence-transformers 智能过滤重复提示词
- 🌐 **多源抓取**: 一键从 GitHub 和 HuggingFace 获取优质提示词
- ⚖️ **LLM 评估**: 基于 Claude API 的专业质量评估
- 📊 **质量追踪**: Langfuse 实时监控和趋势分析

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /root/clawd/skills/x-prompt-hunter
pip install -r requirements.txt
```

### 2. 配置环境变量

在 `~/.bashrc` 或 `.env` 中设置：

```bash
# Claude API (评估功能必需)
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# 可选：抓取功能
export GITHUB_TOKEN="your_github_token"
export HUGGINGFACE_TOKEN="your_huggingface_token"

# 可选：质量追踪
export LANGFUSE_PUBLIC_KEY="your_langfuse_public_key"
export LANGFUSE_SECRET_KEY="your_langfuse_secret_key"
```

### 3. 运行完整流程

```bash
python3 main.py pipeline --query "creative writing" --limit 50 --evaluate-limit 20
```

## 📚 功能详解

### 语义去重

```bash
python3 main.py deduplicate --input data/prompts.json
```

**特性:**
- 使用 `all-MiniLM-L6-v2` 模型
- 默认相似度阈值 0.85
- 自动记录去重日志

### 数据抓取

```bash
# 从所有源抓取
python3 main.py fetch --query "system prompt" --limit 100

# 只从 GitHub 抓取
python3 main.py fetch --source github --limit 50
```

**支持的数据源:**
- GitHub 仓库 (awesome-chatgpt-prompts, fabric)
- HuggingFace 数据集
- 自定义仓库和数据集

### LLM 评估

```bash
python3 main.py evaluate --input data/prompts.json --batch-size 10
```

**评估维度:**
- 创新性 (Innovation)
- 实用性 (Practicality)
- 清晰度 (Clarity)
- 可复用性 (Reusability)

### 质量追踪

```bash
# 生成趋势报告
python3 main.py report --type trend --days 30

# 对比两个时间段
python3 main.py report --type comparison --days1 30 --days2 60

# 导出所有指标
python3 main.py report --type metrics
```

## 📁 项目结构

```
x-prompt-hunter/
├── main.py                      # 主入口
├── config.yaml                  # 配置文件
├── requirements.txt             # 依赖列表
├── SKILL.md                     # 技能文档
├── TECHNICAL_UPGRADES.md        # 技术升级文档
├── README.md                    # 本文件
├── src/                         # 源代码
│   ├── __init__.py
│   ├── semantic_dedup.py        # 语义去重模块
│   ├── github_hf_fetcher.py     # 数据源抓取
│   ├── llm_judge.py             # LLM 评估
│   └── langfuse_tracker.py      # Langfuse 追踪
├── data/                        # 数据目录
│   ├── prompts.json
│   ├── deduplication_log.json
│   ├── evaluation_results.json
│   └── langfuse_reports/
└── logs/                        # 日志目录
    └── prompt_hunter.log
```

## ⚙️ 配置说明

### config.yaml

```yaml
# 语义去重配置
semantic_dedup:
  enabled: true
  model_name: "all-MiniLM-L6-v2"
  similarity_threshold: 0.85

# GitHub 配置
github:
  enabled: true
  repos:
    - "f/awesome-chatgpt-prompts"
  search_keywords: ["prompt", "template"]

# HuggingFace 配置
huggingface:
  enabled: true
  datasets:
    - "Gustavosta/Stable-Diffusion-Prompts"

# LLM 评估配置
llm_judge:
  enabled: true
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
  batch_size: 10

# Langfuse 配置
langfuse:
  enabled: true
  project_name: "prompt-hunter"
  output_dir: "data/langfuse_reports"

# 日志配置
logging:
  level: "INFO"
  file: "logs/prompt_hunter.log"
```

## 🎯 使用场景

### 场景 1: 收集创意写作提示词

```bash
# 1. 抓取
python3 main.py fetch --query "creative writing prompts" --limit 100

# 2. 去重
python3 main.py deduplicate

# 3. 评估
python3 main.py evaluate --batch-size 5

# 4. 查看结果
cat data/evaluation_results.json | jq '.evaluations | sort_by(.total_score) | reverse | .[0:5]'
```

### 场景 2: 定期质量监控

```bash
# 每周运行
python3 main.py pipeline --query "system prompt" --limit 50

# 对比质量趋势
python3 main.py report --type comparison --days1 7 --days2 14
```

### 场景 3: 构建领域专用提示词库

```yaml
# 编辑 config.yaml 添加领域特定仓库
github:
  repos:
    - "f/awesome-chatgpt-prompts"
    - "your-org/medical-prompts"      # 医疗领域
    - "your-org/legal-prompts"        # 法律领域
```

## 📊 输出说明

### 提示词格式

```json
{
  "text": "Your prompt here",
  "source": "github:repo-name",
  "data_source": "github",
  "extracted_at": "2024-01-31T12:00:00Z"
}
```

### 评估结果格式

```json
{
  "innovation": 8.5,
  "practicality": 9.0,
  "clarity": 8.0,
  "reusability": 7.5,
  "total_score": 8.25,
  "strengths": ["创意独特", "结构清晰"],
  "weaknesses": ["可复用性待提升"],
  "suggestions": ["增加使用示例"],
  "summary": "整体质量优秀的提示词"
}
```

## 🔧 故障排查

### 问题：模型下载慢

```bash
# 使用清华镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sentence-transformers
```

### 问题：API 调用失败

```bash
# 检查密钥
echo $ANTHROPIC_API_KEY

# 查看日志
tail -f logs/prompt_hunter.log
```

### 问题：Langfuse 数据不同步

```bash
# 验证密钥
python3 -c "from langfuse import Langfuse; print(Langfuse())"
```

## 📖 文档

- **[SKILL.md](SKILL.md)** - Clawdbot 技能文档
- **[TECHNICAL_UPGRADES.md](TECHNICAL_UPGRADES.md)** - 技术升级详细文档

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

## 🔗 相关链接

- [sentence-transformers](https://www.sbert.net/)
- [Claude API](https://docs.anthropic.com/)
- [Langfuse](https://langfuse.com/)
- [HuggingFace Datasets](https://huggingface.co/datasets)

---

**版本**: 1.0.0
**更新**: 2024-01-31
