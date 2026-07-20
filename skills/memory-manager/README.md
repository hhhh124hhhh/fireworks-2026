# Memory Manager 使用指南

## 快速开始

### 1. 列出所有 Memory Skills
```bash
python3 /root/clawd/scripts/memory-manager.py list
```

### 2. 搜索记忆内容
```bash
# 搜索所有记忆
python3 /root/clawd/scripts/memory-manager.py search "AI 提示词"

# 搜索特定 skill
python3 /root/clawd/scripts/memory-manager.py search "Slack" "memory-debugging"
```

### 3. 获取记忆内容
```bash
# 获取整个 skill
python3 /root/clawd/scripts/memory-manager.py get memory-projects

# 获取特定章节
python3 /root/clawd/scripts/memory-manager.py get memory-projects "ai-prompts"
```

### 4. 智能加载
```bash
# 根据上下文自动加载相关 skills
python3 /root/clawd/scripts/memory-manager.py smart-load "我要开发 AI 提示词评分系统"
```

### 5. 更新 Daily Memory 索引
```bash
python3 /root/clawd/scripts/memory-manager.py index
```

### 6. 自动记忆
```bash
# 记录一般信息
python3 /root/clawd/scripts/memory-manager.py memorize "重要决策：使用 SearXNG 作为主要搜索引擎"

# 系统会自动检测类型：
# - decision: 决策相关
# - config: 配置相关
# - solution: 解决方案相关
# - general: 一般信息
```

## Python API

### 初始化
```python
from memory_manager import MemoryManager

manager = MemoryManager()
```

### 列出 Skills
```python
skills = manager.memory_skills_list()
for skill in skills:
    print(f"{skill['name']}: {skill['type']}")
```

### 搜索
```python
results = manager.memory_search("AI 提示词")
for result in results:
    print(f"[{result['name']}:{result['line']}] {result['content']}")
```

### 获取内容
```python
# 获取整个 skill
content = manager.memory_get("memory-projects")

# 获取特定章节
content = manager.memory_get("memory-projects", "ai-prompts")
```

### 智能加载
```python
context = "我要调试 Slack 连接问题"
related = manager.memory_smart_load(context)
# 返回: ["MEMORY.md", "memory-debugging"]
```

### 自动记忆
```python
from memory_manager import auto_memorize

# 记录决策
file = auto_memorize("决定使用 Claude 作为主要 LLM", type="decision")

# 记录配置
file = auto_memorize("SearXNG URL: http://localhost:8080", type="config")

# 记录解决方案
file = auto_memorize("解决上下文溢出：使用子代理", type="solution")
```

### 创建索引
```python
from memory_manager import create_daily_memory_index

index = create_daily_memory_index()
print(f"总文件: {index['total_files']}")
print(f"总行数: {index['summary']['total_lines']}")
```

## Cron 任务

### Daily Memory 索引更新
- **时间**: 每天 00:00 (Asia/Shanghai)
- **ID**: daily-memory-index
- **功能**: 自动更新 daily memory 索引

## 最佳实践

### 1. 搜索优先
```python
# 先搜索，找到相关内容
results = manager.memory_search("关键词")

# 再根据搜索结果获取详细内容
for result in results:
    content = manager.memory_get(result['name'])
```

### 2. 智能加载
```python
# 复杂任务时，使用智能加载
related = manager.memory_smart_load("我要开发 AI 提示词评分系统")
# 返回相关 skills: ["MEMORY.md", "memory-projects"]

# 然后只加载需要的 skills
```

### 3. 自动记忆
```python
# 重要决策及时记录
auto_memorize("决定使用 SearXNG 作为主要搜索引擎", "decision")

# 配置变更及时记录
auto_memorize("SEARXNG_URL=http://localhost:8080", "config")

# 解决方案及时记录
auto_memorize("解决上下文溢出：使用子代理", "solution")
```

### 4. 定期索引
```python
# 每天自动更新索引（通过 cron）
# 也可以手动更新：
create_daily_memory_index()
```

## 索引格式

### Daily Memory 索引
```json
{
  "updated_at": "2026-02-03T07:50:00+08:00",
  "total_files": 9,
  "files": [
    {
      "date": "2026-02-03",
      "file": "/root/clawd/memory/2026-02-03.md",
      "title": "2026-02-03",
      "lines": 100,
      "size": 1024,
      "modified": "2026-02-03T07:30:00+08:00"
    }
  ],
  "summary": {
    "latest_date": "2026-02-03",
    "total_lines": 1608,
    "total_size": 51200
  }
}
```

## 集成到 OpenClaw

### 在对话中使用
```
用户: 我要查找关于 AI 提示词评分的信息

AI: 让我搜索一下记忆...
[执行 memory_search("AI 提示词评分")]

找到 6 条相关结果：
1. [memory-projects:16] AI 提示词评分系统
2. ...
```

### 自动记忆
```
用户: 决定使用 SearXNG 作为主要搜索引擎

AI: [自动调用 auto_memorize()]
✅ 已记忆到: /root/clawd/memory/2026-02-03.md (类型: decision)
```

## 状态监控

### 查看 Memory Skills 状态
```bash
python3 /root/clawd/scripts/memory-manager.py list
```

### 查看索引状态
```bash
cat /root/clawd/memory/daily-index.json | jq '.summary'
```

## 故障排除

### 问题：搜索不到内容
- 确认 MEMORY.md 和 memory skills 存在
- 检查文件编码是否为 UTF-8
- 尝试不同的关键词

### 问题：索引更新失败
- 检查 memory 目录是否存在
- 检查文件权限
- 手动运行 `python3 /root/clawd/scripts/memory-manager.py index`

### 问题：自动记忆失败
- 检查 memory 目录是否存在
- 检查文件权限
- 确认有足够的磁盘空间

## 未来优化

1. **语义搜索**: 使用 embeddings 进行语义搜索
2. **自动分类**: 自动为记忆内容添加标签
3. **智能总结**: 自动生成 daily memory 摘要
4. **定期清理**: 自动清理过期的 daily memory
5. **性能优化**: 使用数据库替代文件存储
