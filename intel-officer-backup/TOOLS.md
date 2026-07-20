# TOOLS.md - 情报官工具配置

## 🚨 已知限制与替代方案（重要）

### Brave Search API — 订阅过期
- **状态:** ❌ `SUBSCRIPTION_TOKEN_INVALID`（422 错误）
- **影响:** `web_search` 工具不可用
- **替代方案（按优先级）:**
  1. **exec + PowerShell Invoke-RestMethod** — host 权限直接发 HTTP 请求，无限制
  2. **chrome-devtools (CDP 9222)** — 真实 Chrome 新开标签页抓取，已登录态
  3. **DuckDuckGo HTML** — 脚本 `grab-hotspots-v2.ps1` 中已实现，但反爬不稳定
  4. **tikhub-scraper skill** — 抖音/小红书/视频号/公众号
  5. **weibo_hotspot_analyzer skill** — 微博热搜
- **配置位置:** 需要郝工在 OpenClaw Gateway 配置中更新 Brave API key
- **⚠️ 不要尝试用 web_search，每次都会报错浪费 token**

### web_fetch — Sandbox 网络隔离
- **状态:** ❌ `Blocked: resolves to private/internal/special-use IP address`
- **根因:** `web_fetch` 工具在 OpenClaw sandbox 环境中运行，sandbox 的 DNS 解析被限制在内部/回环地址段，无法解析外部域名。这是 OpenClaw 的安全沙箱设计，不是 bug。
- **影响:** `web_fetch` 无法访问任何外部站点
- **与 bot4 exec deny 无关:** 虽然 bot4 配置了 `tools.deny: ["exec"]`，但 `web_fetch` 的 sandbox 限制是全局行为，所有 bot 的 `web_fetch` 都受影响
- **替代方案（按优先级）:**
  1. **exec + PowerShell** — 在 host 环境执行 `Invoke-RestMethod` / `Invoke-WebRequest`，直接走宿主机网络，无限制
  2. **chrome-devtools (CDP 9222)** — `navigate_page` + `take_snapshot`，真实 Chrome 浏览器访问
  3. **browser 工具（openclaw profile）** — OpenClaw 独立浏览器（端口 18800），有网络但无登录态
  4. **grab-hotspots-v2.ps1** — 已封装好的 PowerShell 脚本，exec 调用即可
- **⚠️ 不要尝试用 web_fetch 抓外部网页，每次都会被拦截浪费 token**
- **示例（host 权限抓取）:**
  ```powershell
  # 抓网页 HTML
  $resp = Invoke-WebRequest -Uri "https://example.com" -UseBasicParsing -TimeoutSec 15
  $resp.Content

  # 抓 JSON API
  $data = Invoke-RestMethod -Uri "https://api.example.com/data" -TimeoutSec 15
  $data | ConvertTo-Json

  # 带UA的抓取（防反爬）
  $headers = @{ "User-Agent" = "Mozilla/5.0 ..." }
  Invoke-RestMethod -Uri "https://example.com" -Headers $headers -TimeoutSec 15
  ```

---

## 📊 飞书多维表格 - 热门内容素材库
**App Token:** `DTt9bx9gka7UW6s52ndcdnLCnDe`
**链接:** https://scn2qvzy6171.feishu.cn/base/DTt9bx9gka7UW6s52ndcdnLCnDe

### 表1: 热门内容素材 (tblyIetlgprLVs0V)
**用途:** 存储各平台热搜热门内容原始数据
**字段:** 标题 (PK) | 平台 (单选：微博/小红书/视频号/知乎/公众号/Product Hunt) | 排名 | 点赞数 | 评论数 | 收藏数 | 链接 | 抓取时间 | 关键词

### 表2: 提炼情报 (tblnnynER4WjrMQV)
**用途:** 经过分析提炼的高价值情报
**字段:** 日期 (PK) | 分类 | 标题 | 摘要 | 认知提炼 | 来源 | 原文链接 | 相关度 | 行动建议 | 采集批次 | 处理状态

### 表3: 原始情报 (tbl97RKEz1h5uHJX)
**用途:** 从各渠道采集的原始情报
**字段:** 采集批次 (PK) | 采集时间 | 搜索关键词 | 信息源 | 标题 | 原文内容 | 原文链接

### 表4: 清洗情报 (tblnpKvIOTZ6sZNt)
**用途:** 经过清洗去重后的情报
**字段:** 采集批次 (PK) | 清洗时间 | 分类 | 标题 | 摘要 | 来源 | 原文链接 | 可信度 | 去重标记 | 处理状态

### 数据流向
```
原始情报 → 清洗情报 → 提炼情报
   ↘ 热门内容素材库（热搜/热榜数据独立存储）
```

---

## 📚 飞书知识库 - Intel Officer 深度情报库
**Space ID:** `7616670088766393307`
**Wiki 首页:** https://scn2qvzy6171.feishu.cn/wiki/QVbgw2xMziyLwekmXxvcfkminAz

---

## 🌐 浏览器配置（真实 Chrome）

### 已登录平台
| 平台 | 账号 | 状态 | Cookie 持久化 |
|------|------|------|--------------|
| **知乎** | 职场创造社区 (Lv3) | ✅ 已登录 | ✅ 是 |
| **微博** | 已登录 | ✅ 已登录 | ✅ 是 |
| **Product Hunt** | 无需登录 | ✅ 可访问 | - |
| **百度** | 无需登录 | ✅ 可访问 | - |

### Chrome DevTools 配置
**技能路径:** `C:\Users\Lenovo\AppData\Local\nvm\v22.22.0\node_modules\openclaw\skills\chrome-devtools\`

**启动方式 1：PowerShell 脚本（推荐）**
```powershell
cd C:\Users\Lenovo\AppData\Local\nvm\v22.22.0\node_modules\openclaw\skills\chrome-devtools
.\start-chrome-debug.ps1
```

**启动方式 2：命令行**
```powershell
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data"
```

**连接配置:**
- **CDP 端口:** 9222
- **WebSocket:** ws://127.0.0.1:9222/devtools/browser/...
- **HTTP API:** http://127.0.0.1:9222/json/list

### 可用工具
| 工具 | 端口 | 用途 | 登录状态 |
|------|------|------|----------|
| **chrome-devtools** | 9222 | 真实 Chrome（已登录） | ✅ 知乎/微博 |
| **browser (openclaw)** | 18800 | OpenClaw 独立浏览器 | ❌ 未登录 |

### ⚠️ 浏览器自动化规范
- ✅ **始终在新标签页中操作** — `create_new_tab()` → 操作 → `close_tab()`
- ❌ **不要覆盖用户原始页面**
- ❌ **不要关闭用户打开的标签页**

---

## 🔧 OpenCLI - 网站/社交媒体操作（新增）

**安装:** `npm install -g @jackwener/opencli`  
**版本:** 1.1.1  
**GitHub:** https://github.com/jackwener/opencli

### 常用命令（情报采集）

```powershell
# 微博热搜
opencli weibo hot --limit 30 -f json

# 知乎热榜
opencli zhihu hot --limit 20 -f json

# B 站热门
opencli bilibili hot --limit 20 -f json

# 即刻首页
opencli jike feed --limit 20 -f json

# Hacker News
opencli hackernews top --limit 20 -f json

# V2EX 热门
opencli v2ex hot --limit 20 -f json

# Twitter 趋势
opencli twitter trending --limit 20 -f json
```

### 使用场景
- ✅ **补充热点来源** - 微博/知乎/B 站/即刻/HackerNews
- ✅ **快速采集** - 比 Chrome DevTools 更轻量
- ✅ **JSON 输出** - `-f json` 便于解析
- ⚠️ **需要登录** - 部分平台需要登录态

### 诊断命令
```powershell
opencli doctor          # 诊断问题
opencli list            # 查看所有可用命令
```

---

## 🔍 热点抓取脚本（v2 - 推荐）

**脚本:** `scripts/grab-hotspots-v2.ps1`
**运行:** `powershell -File scripts/grab-hotspots-v2.ps1 [-Quiet]`
**输出:** `tmp/hotspots-v2-YYYYMMDD-HHMM.json`

| 平台 | 来源 | 数量 | 状态 |
|------|------|------|------|
| 微博 | `weibo.com/ajax/side/hotSearch` | Top 50 | ✅ 公开 API |
| 知乎 | `tophub.today/n/mproPpoq6O` | Top 50 | ✅ 网页解析 |
| 百度 | `top.baidu.com/board?tab=realtime` | Top 30 | ✅ 网页解析 |
| DuckDuckGo | `html.duckduckgo.com` | ~9 | ⚠️ 反爬不稳定 |

**总计:** ~130 条（微博50 + 知乎50 + 百度30）

---

## 📋 情报工作流
### 抓取阶段
1. 各平台热搜 → 写入「热门内容素材」表（或脚本 JSON）
2. 关键词搜索 → 写入「原始情报」表

### 清洗阶段
3. 去重 + 分类 → 写入「清洗情报」表

### 提炼阶段
4. 认知提炼 + 行动建议 → 写入「提炼情报」表
5. 生成选题 → 推送到 content-agent

### 推送阶段
6. 热点分析报告 → 飞书文档 → 推送给郝工
7. 选题池 → 飞书多维表格 + content-agent

---

## 🛡️ 风控注意事项
- ✅ 使用真实浏览器降低风控概率
- ✅ 已登录状态降低验证码出现率
- ⚠️ 避免高频请求（间隔至少 5 秒）
- ⚠️ 遇到验证码时手动处理

---

<!-- OPENCLAW-CAPABILITY-START -->
## Agent Capabilities

### Registered Skills
- intel-hotspot-grabber: Hotspot collection across Weibo, Zhihu, Baidu and other monitored sources.
- chrome-devtools: Shared real-Chrome browser automation with persistent cookies.
- jd-collector: Collector used when intel tasks need JD product and market signals.
- analyze: 结构化分析框架 - 数据/代码/文本/策略/视角五维分析
- **opencli**: 浏览器/网站操作 CLI - 社交媒体/新闻/金融数据/内容平台自动化

### Shared MCP Expectations
- Shared config: D:\openclaw-data\.openclaw\workspace-main-lite\config\mcporter.json
- chrome-devtools: required. Usage doc: D:\openclaw-data\.openclaw\workspace-main-lite\config\chrome-devtools-mcp-usage.md

### Local Tool Notes
- Use intel-hotspot-grabber for recurring hotspot collection before inventing manual scraping steps.
- Use chrome-devtools only against the shared real Chrome on port 9222 and avoid concurrent heavy runs.
- Intel-officer may recommend scheduler or capability changes, but the control plane and human own the actual maintenance.

### Capability Workflow
- Read config/capabilities.json before changing skills or tool access.
- Use openclaw-capability-admin to register skills and document MCP dependencies.
- Verify after each change instead of assuming the workspace can already use the tool.
<!-- OPENCLAW-CAPABILITY-END -->
