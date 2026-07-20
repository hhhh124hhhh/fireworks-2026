# Memory: Tech Infrastructure - 技术基础设施

存储所有技术基础设施的详细配置信息。

## 使用方法

### 获取 SearXNG 配置
\`\`\`
memory_get("tech", "searxng")
\`\`\`

### 获取 Gateway 配置
\`\`\`
memory_get("tech", "gateway")
\`\`\`

## 内容索引

### SearXNG 自建搜索服务

**运行信息**：
- Docker 镜像：`searxng/searxng:latest`
- 运行端口：8080
- 状态：✅ 运行中
- 访问地址：http://localhost:8080

**网络问题修复（2026-01-29 14:20 UTC）**：
- 问题：容器无法访问外网
- 原因：iptables FORWARD 链默认策略为 DROP
- 解决方案：
  \`\`\`bash
  iptables -I FORWARD 1 -i br-d64f58a6c827 -o enp1s0 -j ACCEPT
  iptables -I FORWARD 2 -i enp1s0 -o br-d64f58a6c827 -m state --state RELATED,ESTABLISHED -j ACCEPT
  iptables-save > /etc/iptables/rules.v4
  \`\`\`

**使用策略**：
- 优先使用 SearXNG 进行所有网络搜索
- 避免使用 web_search (Brave API) 以节省 API 配额

**配置方式**：
\`\`\`bash
export SEARXNG_URL=http://localhost:8080
\`\`\`

### Gateway 配置

**当前配置**：
- 运行端口：18789 (127.0.0.1)
- Agent 上下文限制：100k 字符
- 主要模型：zai/glm-4.7 (131k tokens)
- thinking: low
- timeout: 60000ms
- maxConcurrent: 2

**通道配置**：
- Slack: ✅ enabled, socket mode
- Feishu: ✅ enabled
- QQ: ⏸️ 待配置

### 重要 API Keys

**Twitter/X API**：
- 服务提供商：twitterapi.io
- 配置位置：~/.bashrc
- 环境变量：TWITTER_API_KEY

**ClawdHub Token**：
- Token: clh_Ki_M1Xiws5Qzi83gqdZhYG3jXSuZOnEfQOxhaRsjHcw
- Registry: https://www.clawhub.ai/api
- 更新时间：2026-02-01

## 版本历史
- 2026-02-02: 初始版本
