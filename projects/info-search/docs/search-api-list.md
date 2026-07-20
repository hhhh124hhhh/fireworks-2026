# 可用搜索 API 清单

## 免费搜索 API 优先级列表

### 优先级 1: Tavily Search ✅ 推荐

- **URL**: https://tavily.com
- **API 类型**: REST
- **免费额度**: 1,000 次搜索/月
- **Python SDK**: 有 (pip install tavily-python)
- **特点**: AI 优化搜索，专为 AI 代理设计
- **注册地址**: https://tavily.com

**配置步骤**:
```bash
# 1. 访问 https://tavily.com 注册账号
# 2. 获取 API Key
# 3. 配置环境变量
echo 'export TAVILY_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**测试**:
```bash
python3 -c "from tavily import TavilyClient; client = TavilyClient(); client.search('test')"
```

---

### 优先级 2: Brave Search ✅ 推荐

- **URL**: https://brave.com/search/api
- **API 类型**: REST
- **免费额度**: 2,000 次请求/月
- **Python SDK**: 有 (pip install brave)
- **特点**: 隐私保护，免费额度最大
- **注册地址**: https://api.search.brave.com/app/

**配置步骤**:
```bash
# 1. 访问 https://api.search.brave.com/app/ 注册账号
# 2. 获取 API Key
# 3. 配置环境变量
echo 'export BRAVE_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**配置 OpenClaw**:
```bash
openclaw configure --section web --key BRAVE_API_KEY --value "your-api-key-here"
```

**测试**:
```bash
curl -X GET "https://api.search.brave.com/res/v1/web/search?q=test" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: your-api-key-here"
```

---

### 优先级 3: SerpAPI

- **URL**: https://serpapi.com
- **API 类型**: REST
- **免费额度**: 100 次搜索/月
- **Python SDK**: 有 (pip install google-search-results)
- **特点**: Google/Bing 搜索包装器，免费额度较小
- **注册地址**: https://serpapi.com

**配置步骤**:
```bash
# 1. 访问 https://serpapi.com 注册账号
# 2. 获取 API Key
# 3. 配置环境变量
echo 'export SERPAPI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

---

### 优先级 4: Bing Search (Microsoft Azure)

- **URL**: https://www.microsoft.com/cognitive-services/bing-web-search-api
- **API 类型**: REST
- **免费额度**: 1,000 次交易/月
- **Python SDK**: 有 (pip install azure-cognitiveservices-search-websearch)
- **特点**: Microsoft Azure 服务，需要 Azure 账号
- **注册地址**: https://portal.azure.com

**配置步骤**:
```bash
# 1. 创建 Azure 账号
# 2. 在 Azure Portal 创建 Bing Search 资源
# 3. 获取 API Key
# 4. 配置环境变量
echo 'export BING_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

---

### 优先级 5: Google Custom Search

- **URL**: https://developers.google.com/custom-search
- **API 类型**: REST
- **免费额度**: 100 次搜索/天
- **Python SDK**: 有 (pip install google-api-python-client)
- **特点**: Google CSE，免费额度较小
- **注册地址**: https://programmablesearchengine.google.com

**配置步骤**:
```bash
# 1. 访问 https://programmablesearchengine.google.com
# 2. 创建自定义搜索引擎
# 3. 在 Google Cloud Console 启用 Custom Search API
# 4. 获取 API Key 和 CX ID
# 5. 配置环境变量
echo 'export GOOGLE_SEARCH_API_KEY="your-api-key-here"' >> ~/.bashrc
echo 'export GOOGLE_SEARCH_CX="your-cx-id-here"' >> ~/.bashrc
source ~/.bashrc
```

---

### 优先级 6: DuckDuckGo (非官方)

- **URL**: https://duckduckgo.com
- **API 类型**: HTML 抓取
- **免费额度**: 无限制
- **Python SDK**: 无（但实现简单）
- **特点**: 免费，但非官方 API，可能被限流
- **GitHub 项目**: https://github.com/deedy5/duckduckgo_search

**Python 实现**:
```python
import requests
from bs4 import BeautifulSoup

def duckduckgo_search(query, max_results=10):
    url = "https://duckduckgo.com/html/"
    params = {'q': query}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for result in soup.select('.result__a')[:max_results]:
        results.append({
            'title': result.text,
            'link': result['href']
        })

    return results
```

---

## 推荐配置顺序

1. **首选**: Tavily Search (1000 次/月，AI 优化)
2. **次选**: Brave Search (2000 次/月，隐私保护)
3. **备选**: SerpAPI (100 次/月，Google/Bing 包装)

**建议**: 同时配置 Tavily 和 Brave，可以获得总共 3000 次/月的免费额度。

---

## 当前配置状态

```bash
# 检查当前配置
echo "=== 搜索 API 配置状态 ==="
echo "TAVILY_API_KEY: ${TAVILY_API_KEY:0:10}..."  # 只显示前 10 个字符
echo "BRAVE_API_KEY: ${BRAVE_API_KEY:0:10}..."
echo "SERPAPI_API_KEY: ${SERPAPI_API_KEY:0:10}..."
echo "BING_API_KEY: ${BING_API_KEY:0:10}..."
echo "GOOGLE_SEARCH_API_KEY: ${GOOGLE_SEARCH_API_KEY:0:10}..."
```

---

## 集成到 Clawdbot

### 方法 1: 环境变量配置（推荐）

```bash
# 添加到 ~/.bashrc
cat >> ~/.bashrc << 'EOF'
# Search API Keys
export TAVILY_API_KEY="your-tavily-key"
export BRAVE_API_KEY="your-brave-key"
export SERPAPI_API_KEY="your-serpapi-key"
EOF

# 重新加载
source ~/.bashrc
```

### 方法 2: OpenClaw 配置（仅 Brave）

```bash
# 配置 Brave Search API
openclaw configure --section web --key BRAVE_API_KEY --value "your-brave-key"
```

### 方法 3: 项目特定配置

```bash
# 在项目目录创建 .env 文件
cat > /root/clawd/projects/info-search/.env << 'EOF'
TAVILY_API_KEY=your-tavily-key
BRAVE_API_KEY=your-brave-key
SERPAPI_API_KEY=your-serpapi-key
EOF

# 加载配置
source /root/clawd/projects/info-search/.env
```

---

## 测试脚本

创建测试脚本: `/root/clawd/projects/info-search/scripts/test-search-apis.sh`

```bash
#!/bin/bash
echo "=== 测试搜索 API 配置 ==="

# 测试 Tavily
if [ -n "$TAVILY_API_KEY" ]; then
    echo "✅ TAVILY_API_KEY 已配置"
else
    echo "❌ TAVILY_API_KEY 未配置"
fi

# 测试 Brave
if [ -n "$BRAVE_API_KEY" ]; then
    echo "✅ BRAVE_API_KEY 已配置"
else
    echo "❌ BRAVE_API_KEY 未配置"
fi

# 测试 SerpAPI
if [ -n "$SERPAPI_API_KEY" ]; then
    echo "✅ SERPAPI_API_KEY 已配置"
else
    echo "❌ SERPAPI_API_KEY 未配置"
fi
```

---

## 快速配置命令

```bash
# 1. 生成 API key 配置模板
cat > ~/.bashrc.search-keys << 'EOF'
# Search API Keys - 添加到 ~/.bashrc

# Tavily Search (推荐: 1000 次/月)
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxx"

# Brave Search (推荐: 2000 次/月)
export BRAVE_API_KEY="BSxxxxxxxxxxxxxxxxxxxxxxxx"

# SerpAPI (可选: 100 次/月)
export SERPAPI_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxx"
EOF

# 2. 手动编辑并添加到 ~/.bashrc
nano ~/.bashrc.search-keys

# 3. 合并到 ~/.bashrc
cat ~/.bashrc.search-keys >> ~/.bashrc

# 4. 重新加载
source ~/.bashrc
```

---

**更新时间**: 2026-02-05
**文档位置**: `/root/clawd/projects/info-search/docs/search-api-list.md`
