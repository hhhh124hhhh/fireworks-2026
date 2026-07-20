# Search Wrapper - 统一搜索接口

自动 Fallback 的多搜索源包装器，避免单一搜索源失败导致系统不可用。

## 功能特性

- ✅ **多搜索源支持**: Tavily → 百度 → SearXNG → Brave
- ✅ **自动 Fallback**: 第一个搜索源失败自动切换到下一个
- ✅ **统一接口**: 所有搜索源返回相同格式的结果
- ✅ **错误处理**: 完善的错误日志和异常处理
- ✅ **超时控制**: 可配置的超时时间
- ✅ **灵活配置**: 支持配置文件和环境变量

## 安装

无需额外依赖，使用 Python 标准库。

```bash
cd /root/clawd/projects/info-search/scripts
chmod +x search-wrapper.py
```

## 配置

配置文件位置: `/root/clawd/.config/data-sources/`

### Tavily 配置 (tavily.conf)
```bash
TAVILY_API_KEY="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"
TIMEOUT=30
```

### 百度搜索配置（环境变量）
```bash
export BAIDU_API_KEY="your-baidu-api-key"
```

### SearXNG 配置 (searxng.conf)
```bash
SEARXNG_URL="http://localhost:8080"
TIMEOUT=30
```

### Brave 配置（可选）
```bash
# 免费版无需 API Key
BRAVE_API_KEY=""  # 可选
```

### 环境变量（可选）
```bash
export TAVILY_API_KEY="your-key"
export BAIDU_API_KEY="your-baidu-api-key"
export SEARXNG_URL="http://localhost:8080"
export BRAVE_API_KEY="your-key"  # 可选
```

## 使用方法

### 1. 命令行使用

```bash
# 基本搜索
./search-wrapper.py "Python 编程" 5

# 尝试所有搜索源
./search-wrapper.py "AI 技术" 3 --all

# 显示详细内容
./search-wrapper.py "机器学习" 2 --verbose
```

### 2. Python API

```python
from search_wrapper import search, search_all_sources, print_results

# 基本搜索
results = search("Python 编程", max_results=5)

# 处理结果
for result in results:
    print(f"{result['title']} - {result['url']}")

# 指定搜索源
results = search("关键词", sources=["tavily", "brave"])

# 只使用百度搜索
results = search("关键词", sources=["baidu"])

# 尝试所有搜索源
all_results = search_all_sources("关键词")

for source, results in all_results.items():
    print(f"{source}: {len(results)} 个结果")
```

## API 参考

### search()

统一的搜索接口，自动 Fallback。

**参数:**
- `query` (str): 搜索查询
- `max_results` (int, 默认 5): 最大结果数量
- `timeout` (int, 默认 30): 超时时间（秒）
- `sources` (List[str], 可选): 指定使用的搜索源列表

**返回:**
- `List[Dict]`: 搜索结果列表

**示例:**
```python
results = search("Python", max_results=10, timeout=20)
```

### search_all_sources()

尝试所有搜索源，返回所有结果（用于比较和测试）。

**参数:**
- `query` (str): 搜索查询
- `max_results` (int, 默认 5): 最大结果数量
- `timeout` (int, 默认 30): 超时时间（秒）

**返回:**
- `Dict[str, List[Dict]]`: 字典，键为搜索源名称，值为结果列表

**示例:**
```python
all_results = search_all_sources("Python")
print(f"Tavily: {len(all_results['tavily'])} 个结果")
print(f"百度: {len(all_results['baidu'])} 个结果")
print(f"SearXNG: {len(all_results['searxng'])} 个结果")
print(f"Brave: {len(all_results['brave'])} 个结果")
```

## 结果格式

所有搜索源返回统一格式：

```python
[
    {
        "title": "结果标题",
        "url": "https://example.com",
        "content": "内容摘要...",
        "source": "tavily",  # 或 "baidu", "searxng", "brave"
        "timestamp": "2026-02-14T12:34:56.789123"
    },
    ...
]
```

**source 字段可能的值**：
- `tavily`: Tavily 搜索
- `baidu`: 百度搜索
- `searxng`: SearXNG 本地搜索
- `brave`: Brave 搜索
- `error`: 搜索失败时的错误信息

## Fallback 机制

默认搜索顺序：

1. **Tavily** (优先)
   - 高质量搜索结果
   - API Key 已配置
   - 超时或错误 → Fallback 到百度

2. **百度搜索** (Fallback 1)
   - 百度 AI 搜索 API
   - 支持中文搜索优化
   - API Key 需通过环境变量 `BAIDU_API_KEY` 配置
   - 失败 → Fallback 到 SearXNG

3. **SearXNG** (Fallback 2)
   - 本地搜索服务
   - 开源、免费
   - 失败 → Fallback 到 Brave

4. **Brave Search API** (Fallback 3)
   - 免费版无需 API Key
   - 隐私保护
   - 最后的备选方案

如果所有搜索源都失败，返回包含错误信息的空结果：

```python
[{
    "title": "搜索失败",
    "url": "",
    "content": "所有搜索源都失败:\n  - tavily: 错误信息\n  - baidu: 错误信息\n  - searxng: 错误信息...",
    "source": "error",
    "timestamp": "2026-02-14T12:34:56.789123"
}]
```

## 日志

日志位置: `/root/clawd/logs/search-wrapper/search-wrapper.log`

日志级别:
- `INFO`: 正常操作（搜索开始、成功、失败）
- `WARNING**: 非致命错误（搜索源不可用）
- `ERROR`: 严重错误（API 错误、超时等）

**示例日志:**
```
2026-02-14 20:47:24,206 - __main__ - INFO - 开始搜索: 'Python 编程' (max_results=3, timeout=30)
2026-02-14 20:47:24,206 - __main__ - INFO - 尝试使用 tavily 搜索...
2026-02-14 20:47:24,206 - __main__ - INFO - [Tavily] 开始搜索: Python 编程
2026-02-14 20:47:25,461 - __main__ - INFO - [Tavily] 成功返回 3 个结果
2026-02-14 20:47:25,462 - __main__ - INFO - ✓ tavily 搜索成功，返回 3 个结果
```

## 错误处理

所有搜索错误都被捕获并记录，不会导致程序崩溃。

**常见错误:**
- `Tavily API Key 未配置`: 检查 tavily.conf 配置
- `SearXNG URL 未配置`: 检查 searxng.conf 配置
- `HTTP 错误`: 网络连接问题或 API 限制
- `URL 错误`: 搜索源服务不可用
- `超时错误`: 搜索响应时间过长，会自动 Fallback

## 使用示例

### 示例 1：基本搜索（自动选择搜索源）

```python
from search_wrapper import search

results = search("北京天气预报")
for r in results:
    print(f"{r['title']} - {r['source']}")
```

### 示例 2：只使用百度搜索

```python
from search_wrapper import search

# 专门使用百度搜索
results = search("人工智能", sources=["baidu"])
for r in results:
    print(f"{r['title']}: {r['url']}")
```

### 示例 3：比较所有搜索源

```python
from search_wrapper import search_all_sources

all_results = search_all_sources("机器学习")

print(f"Tavily: {len(all_results['tavily'])} 个结果")
print(f"百度: {len(all_results['baidu'])} 个结果")
print(f"SearXNG: {len(all_results['searxng'])} 个结果")
print(f"Brave: {len(all_results['brave'])} 个结果")
```

### 示例 4：测试 Fallback 机制

```python
from search_wrapper import search

# 禁用 Tavily，会自动 Fallback 到百度
import os
os.environ['TAVILY_API_KEY'] = ''

results = search("Python 编程")
# 结果将来自百度搜索
```

## 故障排除

### Tavily 搜索失败

1. 检查 API Key 是否正确配置
2. 检查 API 配额是否用完（免费版 1000 次/月）
3. 检查网络连接

### 百度搜索失败

1. 检查环境变量 `BAIDU_API_KEY` 是否设置：
   ```bash
   echo $BAIDU_API_KEY
   ```

2. 如果未设置，在 ~/.bashrc 中添加：
   ```bash
   export BAIDU_API_KEY="your-api-key"
   ```

3. 重新加载配置：
   ```bash
   source ~/.bashrc
   ```

4. 检查 API Key 是否有效，是否有配额限制

5. 检查日志文件了解详细错误：
   ```bash
   tail -f /root/clawd/logs/search-wrapper/search-wrapper.log
   ```

### SearXNG 搜索失败

1. 检查 SearXNG 服务是否运行:
   ```bash
   curl http://localhost:8080/config
   ```

2. 检查配置文件中的 URL 是否正确

3. 检查防火墙设置

### Brave 搜索失败

1. Brave 免费版可能有访问限制
2. 如果需要，可以申请 API Key

## 性能优化

1. **缓存结果**: 实现本地缓存，避免重复搜索
2. **并发搜索**: 可以同时尝试多个搜索源，取最快的结果
3. **智能 Fallback**: 根据历史成功率动态调整搜索源顺序

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可

MIT License
