# AI Prompts Collector

这个目录存储定期收集的 AI 提示词相关信息。

## 文件说明

- `collected.jsonl` - 收集的数据（JSON Lines 格式，每行一个 JSON 对象）
- `summaries.json` - 每日汇总数据

## 数据格式

每个收集条目包含：
```json
{
  "type": "search",
  "timestamp": "2026-01-29T12:00:00Z",
  "queries_count": 5,
  "data": [
    {
      "query": "AI prompt engineering tips",
      "result_count": 5,
      "results": [...]
    }
  ]
}
```
