# 使用示例

本文档展示如何使用 info-search 项目的各个组件。

## 目录

- [快速开始](#快速开始)
- [关键词搜索](#关键词搜索)
- [内容提取](#内容提取)
- [数据清理](#数据清理)
- [完整工作流](#完整工作流)

---

## 快速开始

### 1. 关键词搜索

```bash
# 基本搜索
python3 strategies/keyword_search.py "Python 编程"

# 指定结果数量
python3 strategies/keyword_search.py "AI 技术" -n 10

# 指定搜索源
python3 strategies/keyword_search.py "机器学习" -s tavily,baidu

# 尝试所有搜索源
python3 strategies/keyword_search.py "深度学习" --all

# 保存结果为 JSON
python3 strategies/keyword_search.py "数据分析" -o results.json -f json
```

### 2. 内容提取

```bash
# 从单个 URL 提取内容
python3 processors/extract_content.py "https://example.com/article"

# 批量提取（从文件读取 URL 列表）
echo "https://example.com/page1" > urls.txt
echo "https://example.com/page2" >> urls.txt
python3 processors/extract_content.py -i urls.txt

# 保存结果
python3 processors/extract_content.py -i urls.txt -o extracted.json
```

### 3. 数据清理

```bash
# 清理搜索结果
python3 processors/clean_data.py results.json

# 保存清理结果
python3 processors/clean_data.py results.json -o cleaned.json

# 自定义清理步骤
python3 processors/clean_data.py results.json -s url,filter

# 调整相似度阈值
python3 processors/clean_data.py results.json -t 0.8
```

---

## 关键词搜索

### Python API

```python
from strategies.keyword_search import KeywordSearch

# 创建搜索器
searcher = KeywordSearch()

# 基本搜索
results = searcher.search("Python 编程", max_results=5)
for result in results:
    print(f"{result['title']} - {result['url']}")

# 指定搜索源
results = searcher.search(
    "AI 技术",
    max_results=10,
    sources=["tavily", "baidu"]
)

# 尝试所有搜索源
all_results = searcher.search_all("机器学习")
for source, results in all_results.items():
    print(f"{source}: {len(results)} 个结果")

# 保存结果
searcher.save_results(results, "output.json")

# 格式化输出
markdown_output = searcher.format_results(results, format="markdown")
print(markdown_output)
```

### 输出示例

```json
[
  {
    "title": "什么是Python？- Python 语言简介 - AWS",
    "url": "https://aws.amazon.com/cn/what-is/python/",
    "content": "Python 是一种编程语言，广泛用于Web 应用程序...",
    "source": "tavily",
    "timestamp": "2026-02-14T21:29:20.448095",
    "search_query": "Python 编程",
    "search_timestamp": "2026-02-14T21:29:20.448480",
    "search_strategy": "keyword"
  }
]
```

---

## 内容提取

### Python API

```python
from processors.extract_content import ContentExtractor

# 创建提取器
extractor = ContentExtractor()

# 从单个 URL 提取
results = extractor.extract("https://example.com/article")
for result in results:
    if result['success']:
        print(f"成功: {len(result['content'])} 字符")
    else:
        print(f"失败: {result['error']}")

# 批量提取
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]
results = extractor.extract(urls)

# 从搜索结果提取
from strategies.keyword_search import KeywordSearch

searcher = KeywordSearch()
search_results = searcher.search("Python 教程", max_results=5)
extracted = extractor.extract_from_search_results(search_results, max_results=3)

# 保存结果
extractor.save_results(results, "extracted.json")

# 格式化输出
markdown_output = extractor.format_results(results, format="markdown")
print(markdown_output)
```

### 输出示例

```json
[
  {
    "url": "https://example.com/article",
    "success": true,
    "content": "# 文章标题\n\n这是文章的主要内容...",
    "format": "markdown",
    "error": null,
    "timestamp": "2026-02-14T21:30:00.000000"
  }
]
```

---

## 数据清理

### Python API

```python
from processors.clean_data import DataCleaner

# 创建清理器
cleaner = DataCleaner(similarity_threshold=0.7)

# 完整清理流程
cleaned = cleaner.clean(search_results)

# 查看报告
report = cleaned['report']
print(f"原始: {report['original_count']}")
print(f"最终: {report['final_count']}")
print(f"保留率: {report['retention_rate']}%")

# 自定义清理步骤
cleaned = cleaner.clean(
    search_results,
    steps=['url', 'filter']  # 只执行 URL 去重和过滤
)

# 单独执行某个步骤
# URL 去重
results, url_report = cleaner.remove_url_duplicates(results)

# 内容去重
results, content_report = cleaner.remove_content_duplicates(results)

# 过滤无效
results, filter_report = cleaner.filter_invalid(results)

# 保存结果
cleaner.save_results(cleaned, "cleaned.json")

# 格式化报告
report_text = cleaner.format_report(cleaned['report'])
print(report_text)
```

### 输出示例

```json
{
  "data": [
    {
      "title": "文章标题",
      "url": "https://example.com/article",
      "content": "文章内容...",
      "source": "tavily",
      "timestamp": "2026-02-14T21:29:20.448095",
      "normalized_url": "https://example.com/article",
      "cleaned": true,
      "cleaned_timestamp": "2026-02-14T21:30:00.000000"
    }
  ],
  "report": {
    "original_count": 10,
    "final_count": 7,
    "total_removed": 3,
    "retention_rate": 70.0,
    "url_dedup": {
      "removed_count": 2,
      "kept_count": 10
    },
    "content_dedup": {
      "removed_count": 1,
      "kept_count": 8
    },
    "filter": {
      "removed_count": 0,
      "kept_count": 7
    }
  }
}
```

---

## 完整工作流

### 示例 1: 研究某个主题

```python
#!/usr/bin/env python3
"""
完整工作流示例：研究某个主题
"""

from strategies.keyword_search import KeywordSearch
from processors.extract_content import ContentExtractor
from processors.clean_data import DataCleaner
import json

# 1. 搜索
searcher = KeywordSearch()
print("步骤 1: 搜索关键词...")
results = searcher.search("Claude AI 编程", max_results=10)
print(f"找到 {len(results)} 个结果")

# 2. 提取内容
extractor = ContentExtractor()
print("\n步骤 2: 提取内容...")
extracted = extractor.extract_from_search_results(results, max_results=5)
print(f"成功提取 {sum(1 for r in extracted if r['success'])} 个页面")

# 3. 数据清理
cleaner = DataCleaner(similarity_threshold=0.7)
print("\n步骤 3: 清理数据...")

# 合并搜索结果和提取内容
cleaned_data = cleaner.clean(results)
print(f"清理后保留 {cleaned['report']['final_count']} 条结果")

# 4. 保存结果
output_file = "/tmp/claude-ai-research.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"\n完成！结果已保存到: {output_file}")
```

### 示例 2: 批量研究多个主题

```bash
#!/bin/bash
# 批量研究脚本

TOPICS=("Python 编程" "AI 技术" "机器学习" "数据分析")
OUTPUT_DIR="/tmp/research-results"

mkdir -p "$OUTPUT_DIR"

for topic in "${TOPICS[@]}"; do
    echo "研究主题: $topic"

    # 1. 搜索
    python3 strategies/keyword_search.py "$topic" -n 10 -f json \
        -o "$OUTPUT_DIR/${topic// /_}_search.json"

    # 2. 清理
    python3 processors/clean_data.py "$OUTPUT_DIR/${topic// /_}_search.json" \
        -o "$OUTPUT_DIR/${topic// /_}_cleaned.json"

    echo "完成: $topic"
done

echo "所有主题研究完成！"
echo "结果保存在: $OUTPUT_DIR"
```

### 示例 3: 集成到自动化流程

```python
#!/usr/bin/env python3
"""
每日 AI 研究自动化流程
"""

from strategies.keyword_search import KeywordSearch
from processors.extract_content import ContentExtractor
from processors.clean_data import DataCleaner
from datetime import datetime
import json

# 配置
TOPICS = [
    "Claude AI updates",
    "GPT-5 news",
    "AI programming tools"
]
OUTPUT_DIR = Path("/root/clawd/memory/ai-research")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def daily_research():
    """执行每日研究"""
    date = datetime.now().strftime("%Y-%m-%d")
    print(f"开始每日研究: {date}\n")

    all_results = []

    for topic in TOPICS:
        print(f"研究主题: {topic}")

        # 搜索
        searcher = KeywordSearch()
        results = searcher.search(topic, max_results=5)

        # 清理
        cleaner = DataCleaner()
        cleaned = cleaner.clean(results)

        # 添加到总结果
        all_results.extend(cleaned['data'])

        print(f"找到 {len(cleaned['data'])} 条结果\n")

    # 保存总结果
    output_file = OUTPUT_DIR / f"research-{date}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'date': date,
            'topics': TOPICS,
            'total_results': len(all_results),
            'results': all_results
        }, f, ensure_ascii=False, indent=2)

    print(f"研究完成！结果已保存到: {output_file}")
    return output_file

if __name__ == "__main__":
    daily_research()
```

---

## 高级用法

### 1. 自定义搜索源顺序

```python
from strategies.keyword_search import KeywordSearch

# 只使用特定搜索源
searcher = KeywordSearch(default_sources=["baidu", "searxng"])
results = searcher.search("Python 教程")
```

### 2. 批量内容提取（并行）

```python
from processors.extract_content import ContentExtractor

extractor = ContentExtractor()

# 从搜索结果提取，限制数量
results = searcher.search("AI 新闻", max_results=20)
extracted = extractor.extract_from_search_results(results, max_results=10)
```

### 3. 高级数据清理

```python
from processors.clean_data import DataCleaner

# 更严格的去重
cleaner = DataCleaner(similarity_threshold=0.8)

# 只执行特定步骤
cleaned = cleaner.clean(results, steps=['url', 'filter'])
```

### 4. 生成报告

```python
from strategies.keyword_search import KeywordSearch
from processors.clean_data import DataCleaner

searcher = KeywordSearch()
results = searcher.search("Python 编程", max_results=10)

cleaner = DataCleaner()
cleaned = cleaner.clean(results)

# 生成 Markdown 报告
report = f"""
# Python 编程研究报告

## 搜索结果统计
- 原始数量: {cleaned['report']['original_count']}
- 最终数量: {cleaned['report']['final_count']}
- 保留率: {cleaned['report']['retention_rate']}%

## 清理详情
- URL 去重: 移除 {cleaned['report']['url_dedup']['removed_count']} 条
- 内容去重: 移除 {cleaned['report']['content_dedup']['removed_count']} 条
- 过滤无效: 移除 {cleaned['report']['filter']['removed_count']} 条

## 主要结果
"""
for result in cleaned['data'][:5]:
    report += f"- [{result['title']}]({result['url']})\n"

print(report)
```

---

## 常见问题

### Q: 如何配置搜索源的 API Key？

A: 搜索源的配置文件位于 `/root/clawd/.config/data-sources/`:

- `tavily.conf` - Tavily API Key
- `searxng.conf` - SearXNG 服务 URL
- `baidu.conf` - 百度 AI 搜索 API Key

### Q: 如何提高搜索结果的质量？

A: 可以通过以下方式：

1. 使用更精确的搜索关键词
2. 调整数据清理的相似度阈值（0.5-0.9 之间）
3. 使用特定搜索源而不是自动 fallback
4. 限制搜索结果数量，只获取最相关的

### Q: 如何处理提取失败的内容？

A: 内容提取器会自动处理失败情况：

```python
results = extractor.extract(urls)

for result in results:
    if result['success']:
        print(f"成功: {result['url']}")
    else:
        print(f"失败: {result['error']}")
```

### Q: 如何集成到现有的自动化流程？

A: 可以通过以下方式集成：

1. **Cron Job**: 定时执行脚本
2. **Python Module**: 作为模块导入使用
3. **Shell Script**: 批量处理多个主题
4. **OpenClaw Workflow**: 集成到 OpenClaw 工作流

---

## 参考文档

- [README.md](./README.md) - 项目概述
- [IMPROVEMENT-PLAN.md](./IMPROVEMENT-PLAN.md) - 改进计划
- [IMPLEMENTATION-ROADMAP.md](./IMPLEMENTATION-ROADMAP.md) - 实施路线图

---

*最后更新: 2026-02-14*
