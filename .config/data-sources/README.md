# 数据源配置中心

**位置**: `/root/clawd/.config/data-sources/`

## 概述

这是 Clawdbot AI 信息收集项目的共享数据源配置中心，统一管理所有数据源的配置，避免重复配置，提高维护效率。

## 配置文件

### 1. SearXNG 配置 (`searxng.conf`)

本地隐私搜索引擎配置，用于 Web 搜索。

**主要配置项**:
- `SEARXNG_URL`: SearXNG 实例地址（默认: `http://localhost:8080`）
- `DEFAULT_RESULTS_COUNT`: 默认搜索结果数量
- `PROXY`: 代理设置
- `CACHE_DIR`: 缓存目录

**使用方法**:
```bash
source /root/clawd/.config/data-sources/searxng.conf
# 使用 $SEARXNG_URL 等
```

### 2. Tavily 配置 (`tavily.conf`)

Tavily Search API 配置，用于 AI 研究项目的深度搜索。

**主要配置项**:
- `TAVILY_API_KEY`: Tavily API Key
- `DEFAULT_RESULTS_COUNT`: 默认搜索结果数量
- `SEARCH_DEPTH`: 搜索深度（basic/advanced）
- `MAX_CALLS_PER_MONTH`: API 使用限制（免费版 1000 次/月）

**使用方法**:
```bash
source /root/clawd/.config/data-sources/tavily.conf
# 使用 $TAVILY_API_KEY 等
```

### 3. Twitter API 配置 (`twitter.conf`)

Twitter/X API 配置，用于社交媒体数据收集。

**主要配置项**:
- `TWITTER_API_KEY`: Twitter API Key（从环境变量读取）
- `DEFAULT_RESULTS_COUNT`: 默认搜索结果数量
- `RATE_LIMIT_PER_MINUTE`: 每分钟速率限制

**使用方法**:
```bash
source /root/clawd/.config/data-sources/twitter.conf
# 使用 $TWITTER_API_KEY 等
```

## 使用示例

### 在 Shell 脚本中使用

```bash
#!/bin/bash

# 加载配置
source /root/clawd/.config/data-sources/searxng.conf

# 使用配置
echo "SearXNG URL: $SEARXNG_URL"
echo "搜索结果数量: $DEFAULT_RESULTS_COUNT"
```

### 在 Python 脚本中使用

```python
import os
from pathlib import Path

# 加载环境变量
config_file = Path("/root/clawd/.config/data-sources/searxng.conf")
with open(config_file) as f:
    for line in f:
        if line.startswith('SEARXNG_URL='):
            searxng_url = line.split('=')[1].strip('"')
            break

print(f"SearXNG URL: {searxng_url}")
```

## 相关脚本

- **数据源管理脚本**: `/root/clawd/scripts/data-source-manager.sh`
- **Content Discovery Assistant**: `/root/clawd/projects/info-search/workflows/content-hotspot-collector-v5.sh`
- **AI Research Hub**: `/root/clawd/projects/info-search/workflows/ai-research-extended.sh`

## 项目使用此配置

1. **Content Discovery Assistant**: 使用 SearXNG 收集热点
2. **AI Research Hub**: 使用 Tavily + SearXNG + Twitter API 进行深度研究
3. **未来项目**: 可以直接引用此配置

## 维护说明

- 添加新数据源：在此目录创建新的配置文件
- 更新配置：直接编辑对应的配置文件
- 备份配置：建议定期备份此目录

## 注意事项

1. **API Key 安全**:
   - 不要在 Git 仓库中提交包含真实 API Key 的配置文件
   - 使用环境变量存储敏感信息（如 Twitter API Key）
   - 在 `.gitignore` 中添加配置文件（如果包含敏感信息）

2. **缓存管理**:
   - 定期清理缓存目录
   - 设置合理的缓存 TTL

3. **日志管理**:
   - 定期清理日志文件
   - 监控日志大小

---

**最后更新**: 2026-02-08  
**维护者**: Momo 🔧
