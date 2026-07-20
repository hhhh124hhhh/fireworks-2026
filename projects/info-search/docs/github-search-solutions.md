# GitHub 上的搜索解决方案

## 问题总结

**DuckDuckGo 限流原因**：
- DuckDuckGo 是隐私搜索引擎，没有公开的搜索 API
- SearXNG 使用 HTML 抓取方式获取结果
- 这种方式容易触发反爬虫机制
- 错误：`httpx.ConnectTimeout: html.duckduckgo.com`
- 暂停时间：`suspended_time=3600`（1 小时）

---

## 解决方案 1：使用代理（最简单）

### GitHub 项目：duckduckgo_search_api
- **仓库**：https://github.com/deedy5/duckduckgo_search_api
- **描述**：部署一个从 DuckDuckGo 搜索引擎拉取数据的 API
- **特点**：
  - 支持代理配置（SOCKS5, HTTP）
  - 可配置超时时间
  - Docker 部署支持

**配置示例**：
```bash
# 克隆项目
git clone https://github.com/deedy5/duckduckgo_search_api.git
cd duckduckgo_search_api

# 设置代理（可选）
# 编辑 main.py
TIMEOUT = 20
PROXY = "socks5://user:password@geo.iproyal.com:32325"

# 使用 Docker 部署
docker-compose up --build
```

**优点**：
- ✅ 简单易用
- ✅ 支持代理避免 IP 限流
- ✅ Docker 部署方便

**缺点**：
- ⚠️ 需要代理服务器（额外成本）
- ⚠️ 仍然依赖 DuckDuckGo（可能继续被限流）

---

## 解决方案 2：使用官方搜索 API（推荐）

### 2.1 Tavily Search

**特点**：
- 免费额度：1,000 次搜索/月
- API 类型：REST
- Python SDK：有
- 特点：AI 优化搜索，专为 AI 代理设计

**注册地址**：https://tavily.com

**配置步骤**：
```bash
# 1. 注册并获取 API Key
# 访问 https://tavily.com

# 2. 安装 SDK
pip install tavily-python

# 3. 配置环境变量
echo 'export TAVILY_API_KEY="tvly-your-key-here"' >> ~/.bashrc
source ~/.bashrc

# 4. 测试
python3 << 'EOF'
from tavily import TavilyClient
client = TavilyClient()
result = client.search("test", max_results=5)
print(result)
EOF
```

### 2.2 Brave Search

**特点**：
- 免费额度：2,000 次请求/月
- API 类型：REST
- Python SDK：有
- 特点：隐私保护，免费额度最大

**注册地址**：https://api.search.brave.com/app/

**配置步骤**：
```bash
# 1. 注册并获取 API Key
# 访问 https://api.search.brave.com/app/

# 2. 配置环境变量
echo 'export BRAVE_API_KEY="BS-your-key-here"' >> ~/.bashrc
source ~/.bashrc

# 3. 配置 OpenClaw（可选）
openclaw configure --section web --key BRAVE_API_KEY --value "your-brave-key"

# 4. 测试
curl -X GET "https://api.search.brave.com/res/v1/web/search?q=test" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: your-api-key-here"
```

### 2.3 SerpAPI

**特点**：
- 免费额度：100 次搜索/月
- API 类型：REST
- Python SDK：有
- 特点：Google/Bing 搜索包装器

**注册地址**：https://serpapi.com/

**配置步骤**：
```bash
# 1. 注册并获取 API Key
# 访问 https://serpapi.com/

# 2. 安装 SDK
pip install google-search-results

# 3. 配置环境变量
echo 'export SERPAPI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

# 4. 测试
python3 << 'EOF'
from google_search_results import GoogleSearchResults
search = GoogleSearchResults({"q": "test"})
results = search.get_dict()
print(results)
EOF
```

**推荐组合**：Tavily (1000/月) + Brave (2000/月) = **3,000 次/月免费搜索**

---

## 解决方案 3：替代搜索引擎

### 3.1 Whoogle（Google 搜索）

**仓库**：https://github.com/benbusby/whoogle-search
- **Stars**：11.3k
- **描述**：自托管、无广告、隐私保护的元搜索引擎
- **特点**：
  - 无广告或赞助内容
  - 无 JavaScript
  - 无 Cookie
  - 无 IP 跟踪
  - 支持 Tor 和 HTTP/SOCKS 代理
  - 自动旋转 User Agent
  - JSON API 输出

**部署**：
```bash
# Docker 部署
docker run --publish 5000:5000 --detach --name whoogle-search benbusby/whoogle-search:latest

# 或使用代理
docker run --publish 5000:5000 --detach --name whoogle-search \
  -e WHOOGLE_PROXY_TYPE=socks5 \
  -e WHOOGLE_PROXY_LOC=ip:port \
  benbusby/whoogle-search:latest
```

**⚠️ 重要警告**：
> **Since 16 January 2025, Google has been attacking ability to perform search queries without JavaScript enabled.**
> **This is a breaking change that may mean the end for Whoogle.**

**状态**：可能无法继续使用

### 3.2 Araa-search（Qwant + 多搜索引擎）

**仓库**：https://github.com/Extravi/araa-search
- **Stars**：318
- **描述**：隐私保护的元搜索引擎，提供完整的 API 支持
- **特点**：
  - 自托管
  - 无广告
  - 强大的安全性
  - 利用 Qwant 搜索结果
  - 完整 API 支持

**部署**：
```bash
# 克隆项目
git clone https://github.com/Extravi/araa-search.git
cd araa-search

# 按照 README 部署
# 需要查看项目文档
```

---

## 解决方案 4：User Agent 旋转（SearXNG 内部方案）

### 原理
- SearXNG 使用固定的 User-Agent
- DuckDuckGo 识别并限流同一个 User-Agent 的大量请求

### 实现方法
修改 SearXNG 配置，启用 User Agent 旋转：

```yaml
# /root/clawd/skills/searxng/config/settings.yml

# 启用多个 User-Agent 轮换
# 或配置代理
```

### Whoogle 的 User Agent 生成工具
Whoogle 包含一个自动生成和验证 User Agent 的工具：

```bash
# 克隆 Whoogle 项目
git clone https://github.com/benbusby/whoogle-search.git
cd whoogle-search

# 生成 User Agent
python misc/generate_uas.py 100 > my_uas.txt

# 验证 User Agent
python misc/check_google_user_agents.py my_uas.txt --output working_uas.txt

# 使用 working UAs
export WHOOGLE_UA_LIST_FILE=./working_uas.txt
```

**特点**：
- 自动生成 10 个 Opera User Agents
- 随机旋转避免检测
- 测试工具验证可用性
- 支持自定义 UA 列表

---

## 解决方案 5：多源聚合

### GitHub 项目：searxng/searx
- **仓库**：https://github.com/searxng/searxng
- **Stars**：24.6k
- **描述**：免费的互联网元搜索引擎，聚合各种搜索服务和数据库的结果
- **特点**：
  - 多搜索引擎聚合
  - 用户不被跟踪
  - 支持自托管
  - 可配置多种搜索引擎

**修改配置以启用其他搜索引擎**：
```yaml
# /etc/searxng/settings.yml

# 启用其他需要 API key 的搜索引擎
# 或者添加新的搜索引擎源
```

---

## 推荐方案（按优先级）

### 高优先级（立即执行）

1. **配置官方 API**（最稳定）
   - Tavily: 1000 次/月
   - Brave: 2000 次/月
   - 总计：3000 次/月
   - ✅ 不会被限流
   - ✅ API 响应快速

2. **配置代理绕过限流**（如果坚持使用 DuckDuckGo）
   - 使用 duckduckgo_search_api 项目
   - 需要代理服务器
   - ⚠️ 可能仍然被限流

### 中优先级（长期）

3. **部署替代搜索引擎**
   - Whoogle（⚠️ 可能已被 Google 破坏）
   - Araa-search（需要更多测试）

4. **优化 SearXNG 配置**
   - 启用 User Agent 旋转
   - 配置多源聚合

---

## 快速开始脚本

### 脚本 1：配置 Tavily + Brave

```bash
#!/bin/bash

# 1. 获取 API Keys（需要手动操作）
echo "========================================="
echo "请访问以下网址获取 API Keys："
echo "  - Tavily: https://tavily.com"
echo "  - Brave: https://api.search.brave.com/app/"
echo "========================================"
echo ""
read -p "输入 Tavily API Key: " TAVILY_KEY
read -p "输入 Brave API Key: " BRAVE_KEY

# 2. 配置环境变量
cat >> ~/.bashrc << 'EOF'

# Search API Keys - 配置于 $(date +%Y-%m-%d)
export TAVILY_API_KEY="$TAVILY_KEY"
export BRAVE_API_KEY="$BRAVE_KEY"

EOF

# 3. 重新加载
source ~/.bashrc

# 4. 测试 API
echo ""
echo "测试 Tavily..."
python3 << 'EOF'
from tavily import TavilyClient
client = TavilyClient(api_key="${TAVILY_API_KEY}")
result = client.search("test", max_results=3)
print("✅ Tavily 工作正常！" if result else "❌ Tavily 配置失败")
EOF

echo ""
echo "测试 Brave..."
curl -s -X GET "https://api.search.brave.com/res/v1/web/search?q=test" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: ${BRAVE_API_KEY}" | jq '.web.results | length' \
  && echo "✅ Brave 工作正常！" || echo "❌ Brave 配置失败"

echo ""
echo "========================================="
echo "配置完成！"
echo "免费额度："
echo "  - Tavily: 1,000 次/月"
echo "  - Brave: 2,000 次/月"
echo "  - 总计: 3,000 次/月"
echo "========================================="
```

### 脚本 2：部署 Whoogle（备用方案）

```bash
#!/bin/bash

# 部署 Whoogle
echo "========================================="
echo "部署 Whoogle 搜索引擎"
echo "========================================="

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装"
    exit 1
fi

# 拉取镜像
echo "拉取 Whoogle 镜像..."
docker pull benbusby/whoogle-search:latest

# 运行容器
echo "启动 Whoogle 容器..."
docker run --publish 5000:5000 \
  --detach \
  --name whoogle-search \
  --restart unless-stopped \
  benbusby/whoogle-search:latest

# 等待启动
sleep 5

# 测试
echo "测试 Whoogle..."
curl -s http://localhost:5000/search?q=test | head -20

echo ""
echo "========================================="
echo "Whoogle 部署完成！"
echo "访问地址: http://localhost:5000"
echo "========================================="
```

### 脚本 3：部署 duckduckgo_search_api（带代理）

```bash
#!/bin/bash

# 部署 DuckDuckGo 搜索 API（带代理）
echo "========================================="
echo "部署 DuckDuckGo 搜索 API"
echo "========================================="

# 获取代理配置
read -p "代理地址 (例如: socks5://user:pass@ip:port): " PROXY

if [ -z "$PROXY" ]; then
    echo "⚠️  未配置代理，可能仍然被限流"
fi

# 克隆项目
echo "克隆项目..."
git clone https://github.com/deedy5/duckduckgo_search_api.git /opt/duckduckgo_search_api

cd /opt/duckduckgo_search_api

# 配置代理（如果提供）
if [ -n "$PROXY" ]; then
    echo "配置代理: $PROXY"
    sed -i "s|PROXY = \"\"|PROXY = \"$PROXY\"|" main.py
fi

# 构建并运行
echo "构建并启动..."
docker-compose up -d --build

# 测试
sleep 5
echo "测试 API..."
curl -s "http://localhost:8000/text?q=test&max_results=3"

echo ""
echo "========================================="
echo "部署完成！"
echo "API 地址: http://localhost:8000"
echo "========================================="
```

---

## 总结

| 方案 | 难度 | 成本 | 稳定性 | 推荐度 |
|------|--------|------|----------|----------|
| **Tavily + Brave** | 低 | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| DuckDuckGo + 代理 | 中 | 代理费 | ⭐⭐ | ⭐⭐ |
| Whoogle | 低 | 免费 | ❌ 可能失败 | ⭐ |
| Araa-search | 高 | 免费 | ❓ 未测试 | ⭐⭐ |

**最佳方案**：配置 Tavily 和 Brave Search API

---

**更新时间**：2026-02-05 22:36 GMT+8
**文档位置**：`/root/clawd/projects/info-search/docs/github-search-solutions.md`
