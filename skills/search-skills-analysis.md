# 搜索技能 SearXNG 集成分析报告

生成时间：2026-01-31

## 概述

根据用户偏好（TOOLS.md），用户更倾向于使用 searXNG 而不是其他搜索服务（如 Brave Search API）。本报告分析已发布到 clawdhub 的搜索技能，评估添加 searXNG 支持的可行性和建议。

## 已发布的搜索技能

### 1. firecrawl-search (1.0.0)

**当前实现**：
- 使用 Firecrawl API
- 需要 `FIRECRAWL_API_KEY` 环境变量
- Python 脚本实现
- 功能：搜索、爬取、抓取网站

**特点**：
- 强大的网页抓取能力
- 支持 JS 渲染页面
- 结构化数据提取
- 付费服务（但有免费额度）

**searXNG 集成建议**：
✅ **适合添加**
- 可以添加 searXNG 作为 fallback 搜索选项
- 当 API key 未配置时自动使用 searXNG
- 保持 Firecrawl 的爬取能力

**实施方案**：
1. 检查 `FIRECRAWL_API_KEY` 是否设置
2. 如果未设置，使用 searXNG 进行搜索
3. 如果已设置，继续使用 Firecrawl
4. 更新文档说明两种模式

---

### 2. tavily-search (1.0.0)

**当前实现**：
- 使用 Tavily API
- 需要 `TAVILY_API_KEY` 环境变量
- Node.js 脚本实现
- 功能：AI 优化搜索、内容提取

**特点**：
- 专为 AI 代理优化
- 返回简洁、相关的内容
- 支持深度搜索模式
- 付费服务（但有免费额度）

**searXNG 集成建议**：
✅ **适合添加**
- 可以添加 searXNG 作为备选搜索方式
- 当 API key 未配置时使用 searXNG
- 保留 Tavily 的 AI 优化特性

**实施方案**：
1. 检查 `TAVILY_API_KEY` 是否设置
2. 如果未设置，使用 searXNG 进行搜索
3. 如果已设置，继续使用 Tavily
4. 更新文档说明双模式支持

---

### 3. web-search-exa (1.0.1)

**当前实现**：
- 使用 Exa MCP 服务器
- 无需 API key
- 通过 MCP 协议集成
- 功能：实时搜索、内容提取

**特点**：
- 实时搜索，获取最新内容
- 无需 API key
- 快速内容提取
- MCP 标准协议

**searXNG 集成建议**：
⚠️ **不建议修改**
- Exa 已经是免费的搜索服务
- 通过 MCP 协议集成，更符合 Clawdbot 架构
- searXNG 和 Exa 功能重叠度高
- 两者都无需 API key，不需要 fallback

**替代方案**：
- 创建一个新的 "universal-search" 技能
- 集成 searXNG、Exa、Brave 等多个搜索源
- 允许用户选择或自动切换

---

## 综合建议

### 优先级 1：更新 firecrawl-search (1.0.0 → 1.1.0)
**理由**：
- Firecrawl 功能强大但需要 API key
- 添加 searXNG fallback 可以让用户无需 API key 就能使用
- 爬取功能仍然是 Firecrawl 独有

### 优先级 2：更新 tavily-search (1.0.0 → 1.1.0)
**理由**：
- Tavily 专为 AI 优化，但需要 API key
- 添加 searXNG fallback 可以降低使用门槛
- 保持 AI 优化特性的同时提供基础搜索

### 优先级 3：创建统一搜索技能（新技能）
**建议名称**：`universal-search`
**功能**：
- 集成 searXNG（首选）、Exa、Brave 等多个搜索源
- 自动选择或手动指定搜索源
- 统一的接口和输出格式
- 支持搜索源优先级配置

### 优先级 4：保持 web-search-exa 不变
**理由**：
- 已经是 MCP 标准集成
- 无需 API key
- 功能完整

## 实施计划

### 阶段 1：更新现有技能
1. ✅ 修改 firecrawl-search 添加 searXNG fallback
2. ✅ 修改 tavily-search 添加 searXNG fallback
3. ✅ 更新版本号到 1.1.0
4. ✅ 测试两种模式的切换
5. ✅ 发布到 clawdhub

### 阶段 2：创建统一搜索技能
1. ⏳ 设计 universal-search 架构
2. ⏳ 实现多搜索源集成
3. ⏳ 添加搜索源优先级配置
4. ⏳ 测试所有搜索源
5. ⏳ 发布到 clawdhub

### 阶段 3：文档更新
1. ⏳ 更新 searXNG 技能文档
2. ⏳ 创建搜索技能比较文档
3. ⏳ 更新用户指南

## 技术细节

### searXNG 集成方式

**对于 firecrawl-search**：
```python
# 检查 API key
api_key = os.environ.get("FIRECRAWL_API_KEY")

if api_key:
    # 使用 Firecrawl
    result = firecrawl_search(query, api_key)
else:
    # 使用 searXNG fallback
    result = searxng_search(query)
```

**对于 tavily-search**：
```javascript
// 检查 API key
const apiKey = process.env.TAVILY_API_KEY;

if (apiKey) {
  // 使用 Tavily
  result = await tavilySearch(query, apiKey);
} else {
  // 使用 searXNG fallback
  result = await searxngSearch(query);
}
```

### searXNG 调用方式

**Python**：
```python
import requests

def searxng_search(query, limit=10):
    url = os.environ.get("SEARXNG_URL", "http://localhost:8080")
    params = {
        "q": query,
        "format": "json",
        "engines": "google,bing,duckduckgo"
    }
    resp = requests.get(f"{url}/search", params=params)
    return resp.json()
```

**Node.js**：
```javascript
import process from 'node:process';

async function searxngSearch(query) {
  const url = process.env.SEARXNG_URL || 'http://localhost:8080';
  const params = new URLSearchParams({
    q: query,
    format: 'json',
    engines: 'google,bing,duckduckgo'
  });
  const resp = await fetch(`${url}/search?${params}`);
  return await resp.json();
}
```

## 风险评估

### 低风险
- ✅ searXNG 已安装并配置
- ✅ 添加 fallback 不破坏现有功能
- ✅ 向后兼容（有 API key 继续使用原服务）

### 中风险
- ⚠️ searXNG 可能需要不同的结果格式处理
- ⚠️ 需要测试不同搜索场景的兼容性

### 高风险
- ❌ 无明显高风险

## 结论

建议按以下顺序实施：
1. 优先更新 firecrawl-search 和 tavily-search
2. 添加 searXNG 作为 fallback 选项
3. 创建统一搜索技能作为长期解决方案
4. 保持 web-search-exa 不变（MCP 标准集成）

这样可以：
- 降低用户使用门槛（无需 API key 也能搜索）
- 保持现有付费服务的独特功能
- 提供统一的搜索体验
- 遵循用户偏好（searXNG 优先）
