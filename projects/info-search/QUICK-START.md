# Info-Search 项目改进规划 - 快速开始

**生成时间**: 2026-02-14

---

## 🚀 立即开始（今天开始）

### 第一步：修复 SearXNG 服务（2-3 小时）

```bash
# 1. 检查服务状态
systemctl status searxng
docker ps | grep searxng

# 2. 重启服务
systemctl restart searxng
# 或
docker restart searxng-container

# 3. 验证服务
curl http://localhost:8080/search?q=test&format=json

# 4. 如果失败，重新部署 SearXNG
cd /opt/searxng  # 或你的 SearXNG 安装目录
docker-compose down
docker-compose up -d
```

### 第二步：修复 Slack/Feishu 推送（1-2 小时）

```bash
# 1. 检查 message 工具用法
message --help

# 2. 修复推送脚本
vi /root/clawd/projects/info-search/workflows/push-ai-research-summary.sh

# 3. 修改推送命令（示例）
# 替换原有的 --message-from-stdin 为：
message send \
  --target "#info-search" \
  --message "$(cat $SUMMARY_FILE)" \
  --channel slack

# 4. 测试推送
bash /root/clawd/projects/info-search/workflows/push-ai-research-summary.sh
```

### 第三步：实现 Tavily Fallback 机制（3-4 小时）

创建文件 `strategies/keyword-search-with-fallback.py`:

```python
#!/usr/bin/env python3
"""
多源搜索策略（支持 Fallback）
搜索源优先级：Tavily → SearXNG → Exa → Brave
"""

import os
import json
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchStrategy:
    def __init__(self):
        self.sources = [
            {'name': 'tavily', 'priority': 1, 'enabled': True},
            {'name': 'searxng', 'priority': 2, 'enabled': True},
            {'name': 'exa', 'priority': 3, 'enabled': True},
            {'name': 'brave', 'priority': 4, 'enabled': True},
        ]

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        执行搜索，自动降级到备用搜索源
        """
        sorted_sources = sorted(self.sources, key=lambda x: x['priority'])

        for source in sorted_sources:
            if not source['enabled']:
                continue

            try:
                logger.info(f"尝试使用 {source['name']} 搜索: {query}")
                results = self._search_with_source(source['name'], query, max_results)

                if results:
                    logger.info(f"✅ {source['name']} 搜索成功，找到 {len(results)} 条结果")
                    return results
                else:
                    logger.warning(f"⚠️  {source['name']} 未返回结果，尝试下一个源")

            except Exception as e:
                logger.warning(f"❌ {source['name']} 搜索失败: {e}，尝试下一个源")
                continue

        logger.error(f"所有搜索源均失败")
        return []

    def _search_with_source(self, source_name: str, query: str, max_results: int) -> List[Dict]:
        """
        使用指定搜索源执行搜索
        """
        if source_name == 'tavily':
            return self._search_tavily(query, max_results)
        elif source_name == 'searxng':
            return self._search_searxng(query, max_results)
        elif source_name == 'exa':
            return self._search_exa(query, max_results)
        elif source_name == 'brave':
            return self._search_brave(query, max_results)
        else:
            raise ValueError(f"未知的搜索源: {source_name}")

    def _search_tavily(self, query: str, max_results: int) -> List[Dict]:
        """使用 Tavily API 搜索"""
        try:
            from tavily import TavilyClient
            api_key = os.environ.get('TAVILY_API_KEY')

            if not api_key:
                raise ValueError("TAVILY_API_KEY 未配置")

            client = TavilyClient(api_key=api_key)
            result = client.search(query, max_results=max_results, search_depth="advanced")

            results = []
            for item in result.get('results', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('content', ''),
                    'score': item.get('score', 0),
                    'source': 'tavily'
                })

            return results

        except Exception as e:
            logger.error(f"Tavily 搜索失败: {e}")
            raise

    def _search_searxng(self, query: str, max_results: int) -> List[Dict]:
        """使用 SearXNG 搜索"""
        try:
            import requests

            url = os.environ.get('SEARXNG_URL', 'http://localhost:8080')
            params = {
                'q': query,
                'format': 'json',
                'language': 'en',
                'results': max_results
            }

            response = requests.get(f"{url}/search", params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            for item in data.get('results', [])[:max_results]:
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('content', ''),
                    'score': item.get('score', 0),
                    'source': 'searxng'
                })

            return results

        except Exception as e:
            logger.error(f"SearXNG 搜索失败: {e}")
            raise

    def _search_exa(self, query: str, max_results: int) -> List[Dict]:
        """使用 Exa 搜索（通过 MCP）"""
        try:
            # 注意：Exa 通过 MCP 集成，这里需要调用 MCP 工具
            # 实际实现需要根据 OpenClaw 的 MCP 接口调整
            logger.warning("Exa 搜索需要通过 MCP 集成，暂未实现")
            return []

        except Exception as e:
            logger.error(f"Exa 搜索失败: {e}")
            raise

    def _search_brave(self, query: str, max_results: int) -> List[Dict]:
        """使用 Brave Search 搜索"""
        try:
            import requests

            api_key = os.environ.get('BRAVE_API_KEY')

            if not api_key:
                raise ValueError("BRAVE_API_KEY 未配置")

            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip',
                'X-Subscription-Token': api_key
            }
            params = {
                'q': query,
                'count': max_results
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            for item in data.get('web', {}).get('results', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('url', ''),
                    'content': item.get('snippet', ''),
                    'score': 0,
                    'source': 'brave'
                })

            return results

        except Exception as e:
            logger.error(f"Brave 搜索失败: {e}")
            raise


if __name__ == "__main__":
    # 测试搜索
    strategy = SearchStrategy()
    results = strategy.search("AI updates 2026", max_results=5)

    print(f"找到 {len(results)} 条结果:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   来源: {result['source']}")
        print(f"   URL: {result['url']}")
        print(f"   内容: {result['content'][:100]}...")
```

---

## 📅 本周完成（7 天内）

### 第 4 天：配置 Brave Search API（1 小时）

```bash
# 1. 申请 Brave Search API Key
# 访问：https://brave.com/search/api/
# 注册账号，获取免费 API Key

# 2. 配置环境变量
echo 'export BRAVE_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc

# 3. 测试
python3 << EOF
import requests
import os

api_key = os.environ.get('BRAVE_API_KEY')
url = "https://api.search.brave.com/res/v1/web/search"
headers = {
    'Accept': 'application/json',
    'X-Subscription-Token': api_key
}
params = {'q': 'test', 'count': 3}

response = requests.get(url, headers=headers, params=params)
print(response.json())
EOF
```

### 第 5-6 天：实现基本结果处理器（4-6 小时）

创建 `processors/` 目录下的三个脚本：

1. **processors/extract-content.py** - 内容提取
2. **processors/clean-data.py** - 数据清理
3. **processors/evaluate-quality.py** - 质量评估

参考示例代码（详见 IMPROVEMENT-PLAN.md）

### 第 7 天：测试和文档（2-3 小时）

```bash
# 1. 测试 AI 研究工作流
bash /root/clawd/projects/info-search/workflows/ai-research-extended.sh

# 2. 测试内容热点收集
bash /root/clawd/projects/info-search/workflows/content-hotspot-collector-v6.sh

# 3. 更新文档
# - 更新 README.md
# - 记录问题和解决方案
# - 更新 CHANGELOG.md
```

---

## 📊 进度跟踪

### 本周任务清单

- [ ] 第 1 天：修复 SearXNG 服务
- [ ] 第 1 天：修复 Slack/Feishu 推送
- [ ] 第 1 天：实现 Tavily Fallback 机制
- [ ] 第 4 天：配置 Brave Search API
- [ ] 第 5-6 天：实现基本结果处理器
- [ ] 第 7 天：测试和文档更新

### 短期目标（1-2 周）

**完整性提升**: 65% → 75%

**工作量**: 15-22 小时

**关键里程碑**:
- ✅ 所有 P0 任务完成
- ✅ SearXNG 服务稳定运行
- ✅ Slack/Feishu 推送正常工作
- ✅ Tavily Fallback 机制实现
- ✅ 基本的结果处理器可用

---

## 🔧 常见问题

### Q1: SearXNG 服务如何重新部署？

```bash
# 使用 Docker 部署
git clone https://github.com/searxng/searxng.git
cd searxng

# 复制配置文件
cp searxng/settings.yml .local/settings.yml

# 修改配置
vi .local/settings.yml
# 设置 server: bind_address: "0.0.0.0"
# 设置 server: secret_key: "your_secret_key"

# 启动服务
docker compose up -d

# 验证
curl http://localhost:8080/search?q=test&format=json
```

### Q2: Tavily API 如何配置？

```bash
# 1. 申请 API Key
# 访问：https://tavily.com/
# 注册账号，获取免费 API Key（1,000 次/月）

# 2. 配置环境变量
echo 'export TAVILY_API_KEY="your_key_here"' >> ~/.bashrc
source ~/.bashrc

# 3. 创建配置文件
mkdir -p /root/clawd/.config/data-sources
cat > /root/clawd/.config/data-sources/tavily.conf << EOF
#!/bin/bash
export TAVILY_API_KEY="your_key_here"
EOF

# 4. 测试
python3 << EOF
from tavily import TavilyClient
client = TavilyClient(api_key="your_key_here")
result = client.search("test", max_results=3)
print(result)
EOF
```

### Q3: 如何测试推送功能？

```bash
# 1. 手动测试推送
SUMMARY_FILE="/tmp/test-summary.md"
cat > $SUMMARY_FILE << EOF
# 测试推送

这是一条测试消息。
EOF

# 2. 推送到 Slack
message send \
  --target "#info-search" \
  --message "$(cat $SUMMARY_FILE)" \
  --channel slack

# 3. 推送到 Feishu
message send \
  --target "your_feishu_target" \
  --message "$(cat $SUMMARY_FILE)" \
  --channel feishu
```

---

## 📚 相关文档

- **[完整改进规划](./IMPROVEMENT-PLAN.md)** - 详细的改进计划（13,650 字）
- **[实施路线图](./IMPLEMENTATION-ROADMAP.md)** - 简洁的实施路线图
- **[任务清单](./TASK-CHECKLIST.md)** - 可追踪的任务清单
- **[规划总结](./PLANNING-SUMMARY.md)** - 规划执行摘要

---

**快速开始指南结束**
*更新时间：2026-02-14*
