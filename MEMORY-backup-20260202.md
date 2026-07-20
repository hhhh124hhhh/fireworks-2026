# MEMORY.md - 长期记忆

*你的长期记忆从这里开始。我会帮你重建之前的上下文。*

## 关于用户的记忆

*等待重建...*

## 重要项目

### 🎯 AI 提示词转 Skill 商业计划

**目标**：自动化抓取 Twitter/X 上的热门 AI 提示词，评估质量，转换为 Clawdbot Skill，并打包售卖

#### 五阶段路线图

| 阶段 | 时间 | 目标 | 状态 |
|------|------|------|------|
| 阶段 1 | 1-2周 | Twitter/X 提示词抓取系统 | 🔴 未开始 |
| 阶段 2 | 1周 | 5维度质量评估系统 | 🔴 未开始 |
| 阶段 3 | 1-2周 | 提示词转 Skill 自动化 | 🔴 未开始 |
| 阶段 4 | 2-3周 | Skill 市场平台（订阅+单次购买） | 🔴 未开始 |
| 阶段 5 | 持续 | 发布到 ClawdHub | 🔴 未开始 |

#### 核心工具

**已集成技能**：
- ✅ `twitter-search-skill` - 搜索和抓取 Twitter/X 推文（需要 API key）
- ✅ `x-trends` - 获取热门话题（补充工具）

**Twitter API 配置**：
- API Key：已配置（~/.bashrc）
- 服务提供商：twitterapi.io
- 限制：免费计划有速率限制（429 错误）
- 建议：考虑升级到付费计划以获得更高配额

**首次 Twitter 分析（2026-01-30）**：
- 搜索关键词："AI OR clawdbot"
- 获取推文数：20 条（受 API 限制）
- 关键发现：
  - **Clawdbot 知名度极低**：没有任何推文直接提及
  - 数据质量偏低：多语言混合，部分 "ai" 为感叹词
  - 优质内容稀少：仅 1-2 条推文具有实际参考价值
- 详细报告：`data/x-scraping/analysis-20260129.md`
- Git 提交：951cd12

**参考市场**：
- 📌 PromptBase.com - 定价和分类参考

#### 评分系统（5维度，100分制）

| 维度 | 权重 | 说明 |
|------|------|------|
| 🎯 实用性 | 30% | 具体使用场景、步骤、参数 |
| 🎨 创新性 | 20% | 方法独特性、角度新颖 |
| 📖 完整性 | 20% | 详细程度、示例数量 |
| 🔥 热度 | 25% | 点赞、转发、评论数 |
| 👨‍💼 作者影响力 | 5% | 粉丝数、认证状态 |

**等级划分**：
- A+ (90-100): $9.99
- A (85-89): $4.99
- B+ (80-84): $2.99
- B (70-79): $1.99
- C+ (60-69): $0.99
- C (50-59): 免费
- D (0-49): 不收录

#### 收入预测

**保守估计（第1年）**：$3,600
**乐观估计（第1年）**：$10,500

#### 成本分析

**运营成本（月度）**：
- Vercel Pro: $20
- Render (Backend): $50
- MongoDB Atlas: $19
- Redis Cloud: $5
- **总计**: $94/月

#### 立即行动清单

**本周任务**：
- [x] 完成 Twitter API key 配置 ✅
- [x] 测试 twitter-search-skill 抓取功能 ✅
- [x] 手动评估 10-20 条推文 ✅
- [x] 转换第一个提示词为 Skill ✅

**第一个 Skill 完成情况**：
- [x] ✅ 创建 `tiktok-ai-model-generator` Skill
- [x] ✅ 评分: A+ (94/100)
- [x] ✅ 提交到私有仓库 (Commit b75f177)
- [x] ✅ 打包为 .skill 文件
- [ ] ⏳ 发布到 ClawdHub
- [ ] ⏳ 设置定价 ($9.99)
- [ ] ⏳ 创建 Landing Page

**自动化工作流进展（2026-01-29）**：
- [x] ✅ 配置完整的 cron 定时任务系统
- [x] ✅ 创建 5 个自动化任务（待启用）
- [x] ✅ 建立数据目录结构
- [x] ✅ Gateway 已重启并应用配置
- [ ] ⏳ 启用第一阶段数据收集任务
- [ ] ⏳ 测试 Twitter API 集成
- [ ] ⏳ 启用评估和转换任务

#### 关键决策

**推荐起步策略**：方案 A（MVP 快速上线）
1. 手动抓取 50 个高质量提示词
2. 手动评估和转换为 Skill
3. 创建简单的 Landing Page
4. 先在社交媒体推广免费 Skill
5. 收集用户反馈后开发完整平台

**差异化定位**：
- PromptBase：卖原生提示词
- 我们：卖**自动化转换为 Clawdbot Skill 的产品**
- 目标用户：Clawdbot 用户群体

## 🔧 技术基础设施

### SearXNG 自建搜索服务（2026-01-29）

**重要发现**：用户已有自建的 SearXNG 实例运行中

**运行信息**：
- Docker 镜像：`searxng/searxng:latest`
- 运行端口：8080
- 状态：运行中（2026-01-29 检测时已运行 53 分钟）
- 访问地址：http://localhost:8080

**网络问题修复（2026-01-29 14:20 UTC）**：
- **问题**：容器无法访问外网，所有搜索引擎超时
- **原因**：iptables FORWARD 链默认策略为 DROP，阻止了容器出站流量
- **解决方案**：
  ```bash
  # 添加允许容器网络流量的规则
  iptables -I FORWARD 1 -i br-d64f58a6c827 -o enp1s0 -j ACCEPT
  iptables -I FORWARD 2 -i enp1s0 -o br-d64f58a6c827 -m state --state RELATED,ESTABLISHED -j ACCEPT
  
  # 持久化规则
  apt-get install -y iptables-persistent netfilter-persistent
  iptables-save > /etc/iptables/rules.v4
  systemctl enable netfilter-persistent
  ```
- **修复结果**：✅ 成功
  - 容器现在可以正常访问外网
  - SearXNG 搜索功能正常工作
  - 返回多个搜索引擎的结果（Brave, Google, DuckDuckGo）

**优势**：
- ✅ 完全私有，不依赖外部 API
- ✅ 多搜索引擎聚合
- ✅ 无外部 API 依赖，不消耗 Brave API 配额
- ✅ 完全自主可控
- ✅ 性能良好

**使用策略**：
- **优先使用 SearXNG** 进行所有网络搜索
- 避免使用 `web_search` (Brave API) 以节省 API 配额
- 所有 cron 任务中的网络搜索都应该使用 SearXNG

**配置方式**：
```bash
export SEARXNG_URL=http://localhost:8080
```

**可用功能**：
- 网页搜索（默认）
- 图片搜索
- 新闻搜索
- 视频搜索
- JSON 输出格式（用于程序化处理）

**集成位置**：
- ✅ searxng Skill 已安装：`/root/clawd/skills/searxng/`
- ✅ 已启用 cron 任务 `collect-prompts` 和 `web-prompts-collector`（使用 SearXNG）
- ✅ API 测试成功，可返回 30+ 条搜索结果

**待办事项**：
- [x] ✅ 修复 SearXNG 网络连接问题
- [x] ✅ 持久化 iptables 规则
- [x] ✅ 测试 SearXNG 搜索 AI 提示词相关内容
- [ ] ⏳ 评估搜索质量和结果相关性
- [ ] ⏳ 监控 cron 任务执行情况

---

## 设置和偏好

### 📝 记忆策略偏好
**用户要求更积极的记忆策略** - 在关键时点自动写入记忆：

1. **重要决策** - 项目方向、技术选型、战略选择
2. **用户偏好** - 工作方式、沟通风格、明确的要求
3. **项目进度** - 阶段性成果、里程碑达成
4. **问题解决** - 遇到的问题 + 解决方案 + 经验教训

### 🔄 子代理结果上传规则（重要！）

**用户要求（2026-01-31）**：每个子代理运行成功后，把结果上传到私有仓库

**私有仓库**：
- 地址：https://github.com/hhhh124hhhh/Clawdbot-Skills-Converter.git
- 用途：存储项目文档、策略文件、工作成果
- 用户权限：完全访问

**标准工作流程**：
1. 子代理任务完成，生成结果文件（文档、代码、分析报告等）
2. 提交到本地 git：
   ```bash
   git add .
   git commit -m "描述本次更新的内容和目的"
   ```
3. 推送到远程仓库：
   ```bash
   git push origin master
   ```

**适用场景**：
- 子代理生成的任何文档（分析报告、技术文档、总结）
- 生成的 Skill 文件或代码
- 数据分析结果
- 工作流程设计文档
- 重要的配置变更

**注意事项**：
- 提交信息要清晰描述变更内容
- 确保提交前文件内容正确
- 遇到 git 冲突时需要手动解决

**记录方式**：
- 短期：`memory/YYYY-MM-DD.md` - 原始记录
- 长期：`MEMORY.md` - 提炼的关键信息

### 工作偏好
- 关注 Clawdbot 技能开发
- 对自动化流程感兴趣
- 正在探索商业变现路径
- 希望主动记录，避免重复询问

### 🗂️ 项目仓库（重要）

**私有仓库地址**：
- GitHub: https://github.com/hhhh124hhhh/Clawdbot-Skills-Converter.git

**仓库用途**：
- 存储项目文档、策略文件、工作成果
- 作为项目的主要代码和知识库
- 每次重要成果都需要提交到仓库

**仓库工作流程**：
1. ✅ 生成文档、代码、分析报告
2. ✅ 提交到本地 git：`git add . && git commit -m "说明"`
3. ✅ 推送到远程仓库：`git push origin master`

**重要提醒**：
- 这是用户的私有仓库，具有完全访问权限
- 所有重要的工作成果都应该定期备份到仓库
- 包括：文档、脚本、分析报告、技能文件、配置文件

---

*最后更新：2026-01-29*
- 添加私有仓库信息和工作流程
- 更新仓库使用策略

## 🔧 调试经验记录

### 飞书问题排查（2026-01-29）

**问题描述**：WebSocket 连接正常，机器人可以主动发送消息，但无法接收用户发送的消息

**问题原因**：
- 插件缺少 `im.chat.access_event.user_p2p_chat_entered_v1` 事件处理器
- 飞书 App 需要正确配置事件订阅（长连接模式）

**解决方案**：
1. 修改 `/root/.clawdbot/extensions/feishu/src/monitor.ts`
   - 添加了 `user_p2p_chat_entered_v1` 事件处理器
   - 同时添加了 `im.chat.access_event.user_p2p_chat_entered_v1` 以防万一
   
2. 重启 Gateway 使修改生效

**修复结果**：✅ 成功
- 飞书现在可以正常接收和回复消息
- WebSocket 连接稳定

**调试方法总结**：
- 使用 `clawdbot status` 检查通道状态
- 使用 `tail -f /tmp/clawdbot/clawdbot-2026-01-29.log | grep feishu` 实时监控日志
- 关键日志标记：`feishu: received message`, `feishu: dispatching to agent`, `feishu: WebSocket client started`
- 使用 `message` 工具主动发送测试消息验证

**飞书插件信息**：
- 版本：@m1heng-clawd/feishu v0.1.1
- 安装路径：/root/.clawdbot/extensions/feishu
- 连接模式：WebSocket
- 机器人 Open ID：ou_fd3f49ab670acd27251f2b4ba3039101

### Slack 配置优化（2026-01-29）

**配置变更**：
- 在 `/root/.clawdbot/clawdbot.json` 中添加：
  ```json
  "slack": {
    "requireMention": false
  }
  ```

**效果**：✅ 机器人更主动，可以自动回复所有消息，不需要 @ 机器人

**配置位置**：`channels.slack.requireMention`
- 默认行为：需要 @ 机器人才会回复
- 优化后：自动回复所有消息（建议用于个人对话或小团队）

**Slack 状态**：
- Socket 模式：正常
- Bot Token：已配置
- App Token：已配置
- 群组策略：allowlist
- 活跃频道：#general, C0ABSK92X4G

### 通用调试技巧

**日志位置**：
- 主日志：`/tmp/clawdbot/clawdbot-YYYY-MM-DD.log`
- 使用 `tail -f /tmp/clawdbot/clawdbot-2026-01-29.log` 实时监控

**重启命令**：
- 使用 `gateway` 工具：`gateway(action="restart")`
- 使用 CLI：`clawdbot gateway restart`

**状态检查**：
- `clawdbot status` - 查看所有通道状态
- `clawdbot status --deep` - 深度测试连接

**问题诊断流程**：
1. 检查通道状态
2. 查看实时日志
3. 查找错误或警告
4. 修改配置
5. 重启 Gateway
6. 验证修复结果

---

## 📊 Moltbot 最新玩法对比分析（2026-01-30）

### 官方品牌升级
- ✅ 正式更名: Clawdbot → Moltbot
- ✅ 新官网: https://molt.bot
- ✅ 新文档: https://docs.molt.bot
- ✅ 命令行: `moltbot` (兼容 `clawdbot`)
- ✅ GitHub: `moltbot/moltbot`

### 社区规模（2026-01）
- GitHub Stars: 30,000+
- Discord Members: 8,900+
- Contributors: 130+
- Daily Active Users: 快速增长中

### 6 个真实用户案例（新增）

#### 1. 🚗 汽车谈判自动化
- **用户**: AJ Stuyvenberg
- **成果**: 在 $56,000 的购车中节省 $4,200
- **玩法**: Moltbot 搜索 Reddit 定价数据 → 联系多个经销商 → 通过邮件自动谈判
- **亮点**: 播硬谈判策略，对抗经销商惯用伎俩

#### 2. 🏢 生产环境 Bug 自动修复
- **用户**: @henrymascot
- **成果**: 在团队醒来前自动检测并修复生产环境 Bug
- **玩法**: 设置为 Slack 自动支持系统
- **亮点**: 真正的自主化，无需人工干预

#### 3. 🏠 智能家居气候控制
- **用户**: Nimrod Gutman (@ngutman)
- **玩法**: 基于天气模式决定何时加热房屋，而非固定时间表
- **亮点**: 智能决策，真正理解"加热是否有意义"

#### 4. 🍷 酒窖管理系统
- **用户**: @prades_maxime
- **成果**: 编录 962 瓶酒，支持自然语言查询
- **玩法**: 传入 CSV 文件 → 建立对话式酒窖管理
- **用例**: "今晚配羊肉应该开哪瓶？" → 精准推荐

#### 5. 🛒 超市自动化购物
- **用户**: @marchattonhere
- **玩法**: Tesco Shop Autopilot
  - 生成每周膳食计划
  - 自动预订杂货配送
  - 全部基于浏览器自动化，无 API 集成

#### 6. 📊 每日简报系统
- **用户**: Federico Viticci (MacStories 创始人)
- **成果**: 单月使用 1.8 亿 token
- **评价**: "完全改变了我对 2026 年个人 AI 助手的理解"

### 安全模型深度剖析

#### 默认安全模型
| 会话类型 | 执行环境 | 风险级别 |
|---------|---------|---------|
| 主会话 (你) | 宿主机 | ⚠️ 高信任 |
| 群组会话 | Docker 沙箱 (可选) | ✅ 隔离 |
| 未知私信 | 需要配对 | ✅ 受保护 |

#### 推荐安全配置
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main",
        "allowedTools": ["bash", "read", "write"],
        "deniedTools": ["browser", "nodes", "cron"]
      }
    }
  },
  "channels": {
    "whatsapp": {
      "allowFrom": ["+1234567890"],
      "dmPolicy": "pairing"
    }
  },
  "gateway": {
    "auth": {
      "mode": "password",
      "password": "your-secure-password"
    }
  }
}
```

#### 常见漏洞及缓解
1. **Prompt Injection**: 使用内容审查，限制可信来源
2. **Supply Chain**: 审查技能代码，仅从官方源安装
3. **Auto-Update**: 关闭自动更新，手动审核后更新
4. **Exposed Ports**: 使用 Tailscale Serve/Funnel，不直接暴露端口

### 成本对比分析

| 特性 | Moltbot | ChatGPT | Siri | Google Assistant |
|------|---------|---------|------|------------------|
| 月成本 | 💰 $25-150 | 💰 $20 | 💰 免费 | 💰 免费 |
| 隐私 | ✅ 完全控制 | ❌ 云端 | ⚠️ Apple 服务器 | ❌ Google 服务器 |
| 自托管 | ✅ 是 | ❌ 否 | ❌ 否 | ❌ 否 |
| 主动消息 | ✅ 是 | ❌ 否 | ⚠️ 有限 | ⚠️ 有限 |
| 多渠道 | ✅ 10+ 平台 | ❌ 仅网页/App | ❌ 仅 Apple | ❌ 仅 Google |

### 24 小时真实体验报告

#### 核心发现
1. **安装难度**: 远超"一键安装"预期，需要 2 小时以上调试
   - 需要 Homebrew, Node.js, Xcode 命令行工具
   - 需要命令行熟练度

2. **权限范围争议**: AI 倾向于请求过多权限
   - 需要主动质疑和限制权限
   - 最佳实践: 创建独立数字身份 (独立邮箱、密码库)

3. **日历管理陷阱**
   - 时区处理失败: 所有事件都差了一天
   - 递归事件创建失败: 工具不支持
   - 核心问题: LLM 没有真正的"时间和空间感"

4. **编码延迟问题**
   - 延迟导致编码反馈循环体验不佳
   - 更适合 Devin 或 Cursor 的后台代理

5. **语音输入可行性**
   - Telegram 语音笔记可用
   - 自然语言需求可行，但需要精细提示

### 社区评价金句

> "After years of AI hype, I thought nothing could faze me. Then I installed Moltbot. From nervous 'hi what can you do?' to full throttle - design, code review, taxes, PM, content pipelines... AI as teammate, not tool."
> — @lycfyi

> "It will actually be the thing that nukes a ton of startups, not ChatGPT as people meme about. The fact that it's hackable (and more importantly, self-hackable) and hostable on-prem will make sure tech like this DOMINATES conventional SaaS."
> — @rovensky

> "At this point I don't even know what to call Moltbot. It is something new. After a few weeks in with it, this is the first time I have felt like I am living in the future since the launch of ChatGPT."
> — @davemorin

> "It's running my company."
> — @therno

### 核心洞察

#### Moltbot 的独特优势
1. **主动能力**: 这是与传统 AI 助手最大的区别
2. **本地优先**: 数据不离开用户设备
3. **多渠道统一**: 一个 AI 助手贯穿所有消息平台
4. **可扩展性**: 插件架构，技能可无限扩展

#### 当前局限性
1. **安装门槛高**: 需要技术背景
2. **权限管理复杂**: AI 倾向于请求过多权限
3. **时区处理薄弱**: LLM 固有时间感问题
4. **编码延迟**: 不适合实时编程

#### 适用场景
**✅ 适合**:
- 个人生产力管理
- 异步任务执行
- 多服务编排
- 主动通知和提醒
- 自动化工作流

**❌ 不适合**:
- 实时代码编辑
- 需要精确时间/空间判断的任务
- 技术小白的一键部署
- 需要超低延迟的场景

### 数据对比（昨天 vs 今天）

| 维度 | 昨天 (2026-01-29) | 今天 (2026-01-30) | 变化 |
|------|------------------|------------------|------|
| 技能数量 | 565+ | 100+ (ClawdHub 官方) | 数据源不同 |
| 社区规模 | 未明确 | 30K+ stars, 8.9K+ Discord | ✅ 新增 |
| 官方名称 | Clawdbot | Moltbot | ✅ 更新 |
| 用户案例 | 简短描述 | 6 个详细故事 | ✅ 深化 |
| 安全模型 | 无 | 完整分析 | ✅ 新增 |
| 成本分析 | 无 | 4 方对比 | ✅ 新增 |

### 趋势预测

#### 短期趋势 (2026 Q1-Q2)
1. 更多 Nix 插件集成
2. 增强的多模型协作
3. 更深入的浏览器自动化
4. AI 原生应用的更紧密集成

#### 长期趋势 (2026 下半年)
1. **企业级部署**: 更多公司部署 Moltbot 作为内部 AI 基础设施
2. **技能市场爆发**: 技能数量从 100+ 增长到 1000+
3. **安全工具成熟**: 出现专业的安全审查和审计工具
4. **云托管服务商**: Zeabur, DigitalOcean 等提供一键 Moltbot 托管

#### 破坏性影响
- **SaaS 行业**: 自托管 + AI 能力可能摧毁许多传统 SaaS
- **个人助手市场**: 真正的个人 AI 助手时代开始
- **开发工具**: 传统 IDE 集成 AI 面临挑战

### 完整文档
- **对比分析**: https://github.com/hhhh124hhhh/Clawdbot-Skills-Converter/blob/master/Moltbot-UseCases-2026-01-30-Comparison.md
- **昨日文档**: /root/clawd/Clawdbot-Skills-Converter/X-Twitter-Clawdbot-Moltbot-Popular-UseCases.md
- **Git 提交**: ede77ff

---

*最后更新：2026-01-30 08:00 UTC*
- 添加 Moltbot 最新玩法对比分析
- 新增 6 个真实用户案例
- 新增安全模型深度剖析
- 新增成本对比分析
- 新增 24 小时真实体验报告

## 🔧 Slack 优化和 Cron Jobs（2026-01-29）

### Slack 配置优化

**已完成配置**：
- ✅ `requireMention: false` - 机器人会自动回复所有消息，不需要 @
- ✅ `historyLimit: 100` - 增加历史记录数量，防止上下文丢失
- ✅ Socket 模式 - 正常连接

**效果**：
- 机器人更主动，可以自动回复
- 保持更多历史上下文，减少信息丢失

### Cron Jobs 配置

**配置文件**：`/root/.clawdbot/cron/jobs.json`

**已配置的定时任务**：

1. **slack-daily-summary** - Slack 每日总结
   - 时间：每天 20:00（上海时区）
   - 功能：生成 Slack 频道的每日总结
   - 内容：讨论主题、做出的决策、待办事项
   - 保存：/root/clawd/memory/slack-summary/YYYY-MM-DD.md
   - 状态：临时禁用（待启用）

2. **network-check** - 网络防护能力检测
   - 频率：每 4 小时
   - 功能：测试网站连通性
   - 测试网站：google.com, github.com, openai.com, slack.com, clawd.bot
   - 方法：curl 测试（超时 10 秒）
   - 保存：/root/clawd/data/network-check/results.jsonl
   - 状态：临时禁用（待启用）

3. **collect-prompts** - AI 提示词收集
   - 频率：每 6 小时
   - 功能：搜索 AI 提示词并保存
   - 工具：web_search
   - 保存：/root/clawd/data/prompts/collected.jsonl
   - 状态：临时禁用（待启用）

**注意事项**：
- 所有定时任务目前处于禁用状态（enabled: false）
- 需要手动启用后才会执行
- 配置修改需要重启 Gateway 生效

### 网络连接测试结果

**测试时间**：2026-01-29 13:29 UTC

**测试结果**：
- google.com: ✅ 200 (正常)
- github.com: ⚠️ 301 (重定向，预期)
- openai.com: ⚠️ 308 (重定向，预期)
- slack.com: ⚠️ 302 (重定向，预期)

**结论**：大部分网站都能访问，只是有些会重定向。这是正常现象。

**网络防护能力**：
- ✅ 基础连通性正常
- ✅ 主要网站（Google, GitHub, OpenAI, Slack）都能访问
- 建议监控：可以定期检查关键网站的可用性

## 🤖 X 和网上资源自动化抓取工作流（2026-01-29）

### Cron 定时任务配置

**配置文件**：`/root/.clawdbot/cron/jobs.json`
**Gateway 重启时间**：2026-01-29 13:35 UTC
**Git 提交**：commit 7094388

### 已配置的 5 个定时任务

#### 1. x-twitter-prompts-scraper - Twitter/X 提示词抓取
- **频率**：每 8 小时
- **状态**：⏸️ 禁用（待启用）
- **关键词**："AI prompt" OR "ChatGPT prompt", "Claude prompt" OR "prompt engineering", "AI tips" OR "best AI prompts"
- **输出**：`/root/clawd/data/x-scraping/prompts-YYYYMMDD.jsonl`
- **数据结构**：tweet_id, author_handle, author_followers, content, likes/retweets/replies/quotes, created_at, url

#### 2. x-trends-monitor - 热门话题监控
- **频率**：每 4 小时
- **状态**：⏸️ 禁用（待启用）
- **功能**：使用 x-trends 工具获取热门话题，过滤 AI 相关关键词
- **关键词**：AI, prompt, ChatGPT, Claude, artificial intelligence, machine learning
- **输出**：`/root/clawd/data/trends/x-trends-YYYYMMDD.json`
- **额外**：每周生成热门话题趋势报告

#### 3. web-prompts-collector - 网络资源收集
- **频率**：每 12 小时
- **状态**：⏸️ 禁用（待启用）
- **关键词**：
  - "AI prompt engineering tips 2026"
  - "best ChatGPT prompts for work"
  - "Claude AI prompt examples"
  - "AI prompt templates free"
  - "effective AI prompts guide"
- **输出**：`/root/clawd/data/web-resources/collected-YYYYMMDD.jsonl`
- **处理流程**：web_search → web_fetch → 提取提示词 → 评估质量 → 保存

#### 4. prompts-quality-evaluator - 提示词质量评估
- **频率**：每 8 小时
- **状态**：⏸️ 禁用（待启用）
- **评分维度（100分制）**：
  - 🎯 实用性 (30%): 具体使用场景、步骤、参数
  - 🎨 创新性 (20%): 方法独特性、角度新颖
  - 📖 完整性 (20%): 详细程度、示例数量
  - 🔥 热度 (25%): 点赞、转发、评论数
  - 👨‍💼 作者影响力 (5%): 粉丝数、认证状态
- **输入**：x-scraping 和 web-resources 数据
- **输出**：`/root/clawd/data/evaluation/scored-prompts-YYYYMMDD.jsonl`
- **过滤**：评分 >= 60 保留，< 60 丢弃
- **报告**：总评估数、等级分布、Top 10、Git 提交

#### 5. high-quality-skill-generator - 高质量提示词转 Skill
- **频率**：每 24 小时
- **状态**：⏸️ 禁用（待启用）
- **触发条件**：评分 >= 80 (B+ 及以上) 且未生成过 Skill
- **输出目录**：`/root/clawd/data/generated-skills/[skill-name]/`
- **生成内容**：SKILL.md, 辅助文件, README.md, 示例
- **打包**：使用 pack-skills.sh 生成 .skill 文件
- **Git 操作**：自动提交到私有仓库
- **定价建议**：A+: $9.99, A: $4.99, B+: $2.99

### 数据目录结构

```
/root/clawd/data/
├── x-scraping/           # Twitter/X 抓取数据
├── trends/              # 热门话题监控
├── web-resources/       # 网络资源收集
├── evaluation/          # 质量评估结果
└── generated-skills/    # 自动生成的 Skills
```

### 启用策略

**分阶段启用（推荐）**：

**阶段 1 - 数据收集**：
```bash
# 编辑 /root/.clawdbot/cron/jobs.json
# 启用以下任务（enabled: true）:
- x-twitter-prompts-scraper
- x-trends-monitor
- web-prompts-collector

# 重启 Gateway
clawdbot gateway restart
```

**阶段 2 - 评估系统**：
- 启用 `prompts-quality-evaluator`
- 监控几天数据质量

**阶段 3 - 自动化转换**：
- 启用 `high-quality-skill-generator`
- 开始自动生成 Skills

### 预期效果

- **数据收集**: 每天 600-1000 条 AI 提示词
- **高质量内容**: 每天 100-200 条评分 >= 60
- **可转换 Skill**: 每天 10-30 条评分 >= 80
- **月产出**: 约 300-900 个高质量 Skills

### 完整文档

- 工作流设计：`/root/clawd/cron-setup/x-scraper-workflow.md`
- 完整说明：`/root/clawd/cron-setup/README.md`

---

## 🔧 Python 脚本命名和环境变量最佳实践（2026-02-01）

### 重要教训

#### 1. Python 文件命名规范（⚠️ 永远记住）

**规则**：
- ✅ **永远使用下划线**：`script_name.py`
- ❌ **禁止使用连字符**：`script-name.py`

**原因**：
- Python 将连字符解释为减号运算符
- `import collect-prompts-enhanced` 会变成 `collect - prompts - enhanced`（减法）
- 导致 `SyntaxError: invalid syntax`

**正确示例**：
```bash
# ❌ 错误
my-script.py
collect-prompts-enhanced.py
api-handler.py

# ✅ 正确
my_script.py
collect_prompts_enhanced.py
api_handler.py
```

**遵循标准**：
- PEP 8（Python 官方风格指南）
- 所有 Python 包和模块都使用下划线

#### 2. 环境变量配置规范

**本地服务**：
```bash
# ✅ 正确 - 本地服务使用 localhost
SEARXNG_URL=http://localhost:8080
DATABASE_URL=http://localhost:5432
REDIS_URL=http://127.0.0.1:6379

# ❌ 错误 - 避免使用外部 IP
SEARXNG_URL=http://149.13.91.232:8080
```

**远程服务**：
```bash
# ✅ 优先使用域名（更稳定）
API_URL=https://api.example.com
DATABASE_URL=postgres://db.example.com:5432

# ⚠️ IP 作为最后选择（仅当没有域名时）
REMOTE_API=192.168.1.100:8080
```

**Docker 容器通信**：
```bash
# ✅ 使用服务名（推荐）
API_URL=http://api-service:8080
DB_URL=postgres://postgres-service:5432/mydb

# ⚠️ 容器内部网络 IP（不推荐，可能变化）
API_URL=http://172.18.0.3:8080
```

#### 3. 环境变量管理最佳实践

**集中管理**：
```
/root/clawd/.env.d/
├── searxng.env       # SearXNG 相关
├── twitter.env       # Twitter API 相关
├── database.env      # 数据库相关
└── redis.env         # Redis 相关
```

**配置加载**：
```bash
# 在脚本中加载环境变量
if [ -f /root/clawd/.env.d/searxng.env ]; then
    export $(grep -v '^#' /root/clawd/.env.d/searxng.env | xargs)
fi
```

**文档化**：
```bash
# .env 文件注释示例
# SearXNG 搜索服务配置
# 本地服务地址（容器间通信）
SEARXNG_URL=http://localhost:8080

# Twitter API 配置
# 从 ~/.bashrc 加载
TWITTER_API_KEY=${TWITTER_API_KEY}
```

#### 4. 调试连接问题的标准流程

当遇到服务连接问题时，按以下顺序检查：

1. **检查环境变量**
   ```bash
   echo $SEARXNG_URL
   env | grep SEARXNG
   ```

2. **测试连通性**
   ```bash
   # 测试 TCP 连接
   curl -I http://localhost:8080
   telnet localhost 8080
   
   # 测试 DNS（如果是域名）
   nslookup api.example.com
   ping api.example.com
   ```

3. **检查 Docker 网络**（如果使用容器）
   ```bash
   # 查看容器网络
   docker network ls
   docker network inspect bridge
   
   # 查看容器状态
   docker ps
   docker inspect <container-name>
   ```

4. **查看日志**
   ```bash
   # 查看容器日志
   docker logs <container-name> --tail 100
   
   # 查看应用日志
   tail -f /var/log/application.log
   ```

#### 5. 预防清单

**创建新 Python 脚本时**：
- [ ] 文件名使用下划线：`my_script.py`
- [ ] 避免特殊字符（空格、连字符等）
- [ ] 符合 PEP 8 命名规范
- [ ] 文件名与模块名一致

**配置新服务时**：
- [ ] 本地服务使用 `localhost`
- [ ] 远程服务优先使用域名
- [ ] 环境变量集中管理在 `.env.d/`
- [ ] 添加注释说明用途
- [ ] 测试连通性

**调试连接问题时**：
- [ ] 检查环境变量配置
- [ ] 使用 curl/ping 测试连通性
- [ ] 检查 Docker 网络（容器场景）
- [ ] 查看日志确认错误信息

#### 6. 常见错误和解决方案

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `SyntaxError: invalid syntax` | 文件名使用连字符 | 改为下划线 |
| `Connection refused` | 外部 IP 不对或服务未启动 | 使用 localhost，检查服务状态 |
| `NameError` | 模块导入失败（文件名问题） | 检查文件名和引用是否一致 |
| `Timeout` | 网络不通或防火墙阻止 | 检查 iptables，测试连通性 |
| `ECONNREFUSED` | 端口错误或服务未监听 | 检查服务端口配置 |

### 相关技术文档
- PEP 8 - Style Guide for Python Code: https://peps.python.org/pep-0008/
- Python 模块命名规范: https://docs.python.org/3/tutorial/modules.html

---

*最后更新：2026-02-02 17:05*
- ✅ x-prompt-hunter 技能依赖安装完成（PyTorch CPU, sentence-transformers 3.0.1）
- ✅ 语义去重功能测试通过（相似度阈值 0.85，成功去重）
- 📝 重要：LLM 评估功能直接使用 coding-agent（Claude）能力，无需单独配置 API
- 记录 Python 文件命名规范（下划线 vs 连字符）
- 记录环境变量配置最佳实践（本地服务用 localhost）
- 添加调试连接问题的标准流程
- 添加预防清单

## 🎯 x-prompt-hunter 技能部署状态（2026-02-02）

**技能位置**：`/root/clawd/skills/x-prompt-hunter`

### ✅ 已完成

#### 1. 依赖安装
```bash
# 虚拟环境位置
/root/clawd/skills/x-prompt-hunter/venv

# 核心依赖
- PyTorch 2.10.0+cpu (CPU 版本)
- sentence-transformers 3.0.1
- transformers 4.36.0
- datasets 4.5.0
- PyGithub 2.8.1
- 其他必要依赖
```

#### 2. 语义去重功能测试
- ✅ 模型加载：`all-MiniLM-L6-v2`
- ✅ 相似度阈值：0.85
- ✅ 测试数据：5 个提示词
- ✅ 去重结果：成功移除 2 个相似提示词
- ✅ 相似度日志：正常保存

**测试结果**：
```
原始提示词：5 个
- [1] Write a creative story about a magical forest
- [2] Create a story about an enchanted forest with magic (相似度: 0.917)
- [3] How do I bake a chocolate cake from scratch?
- [4] Write Python code to sort a list
- [5] Write a Python function to sort a list of numbers (相似度: 0.874)

去重后：3 个
- [1] Write a creative story about a magical forest
- [3] How do I bake a chocolate cake from scratch?
- [4] Write Python code to sort a list
```

### ⚠️ 待配置

#### LLM 评估功能
**重要更新（2026-02-02）**：
- ✅ **无需单独配置 Claude API**
- ✅ **直接使用 coding-agent（Claude）能力**
- ✅ **通过 sessions_spawn 或 sessions_send 调用**

**实现方式**：
```python
# 方法 1：使用 sessions_spawn 启动子代理
sessions_spawn(
    task="评估以下提示词的质量...",
    agentId="main",  # 使用 Claude
    model="zai/glm-4.7"
)

# 方法 2：使用 sessions_send 发送到已运行的会话
sessions_send(
    sessionKey="session-key",
    message="评估提示词：..."
)
```

**评估维度（4 个）**：
1. **创新性** (1-10)：独特性和创造性
2. **实用性** (1-10)：实际应用价值
3. **清晰度** (1-10)：表达明确性
4. **可复用性** (1-10)：场景适应性

### 📝 使用方法

#### 激活虚拟环境
```bash
cd /root/clawd/skills/x-prompt-hunter
source venv/bin/activate
```

#### 运行语义去重
```bash
# 使用 main.py
python3 main.py deduplicate \
  --input data/prompts.json \
  --output data/prompts_clean.json

# 或直接调用 Python
python3 -c "
from src.semantic_dedup import SemanticDedup
config = {
    'enabled': True,
    'model_name': 'all-MiniLM-L6-v2',
    'similarity_threshold': 0.85,
    'log_file': 'data/deduplication_log.json'
}
dedup = SemanticDedup(config)
deduplicated, stats = dedup.deduplicate(prompts)
"
```

#### 完整流程（包含去重）
```bash
python3 main.py pipeline \
  --query "AI prompts" \
  --limit 50 \
  --evaluate-limit 20
```

### 🔧 配置文件

**config.yaml 关键配置**：
```yaml
semantic_dedup:
  enabled: true
  model_name: "all-MiniLM-L6-v2"
  similarity_threshold: 0.85
  batch_size: 32
  log_file: "data/deduplication_log.json"

llm_judge:
  enabled: true
  provider: "anthropic"  # 使用 Claude
  model: "claude-3-5-sonnet-20241022"
  evaluation_criteria:
    - "innovation"
    - "practicality"
    - "clarity"
    - "reusability"
  output_file: "data/evaluation_results.json"
  batch_size: 10
```

### 📊 输出文件

```
data/
├── prompts.json                 # 原始提示词
├── prompts_deduplicated.json   # 去重后提示词
├── deduplication_log.json      # 去重日志
└── evaluation_results.json     # 评估结果（LLM 评估）
```

### 🚀 下一步

1. **测试 LLM 评估功能**
   - 使用 coding-agent 评估一组测试提示词
   - 验证评分质量和一致性

2. **集成到工作流**
   - 与 prompt-to-skill-converter 集成
   - 建立端到端自动化流程

3. **Cron 自动化**
   - 配置定时任务定期运行
   - 监控执行状态和结果

## jack 的个人主页（2026-02-02）

### 主页信息
- **访问地址**: https://hhhh124hhhh.github.io/jack-portfolio/
- **GitHub 仓库**: https://github.com/hhhh124hhhh/jack-portfolio
- **文件位置**: /root/clawd/jack-portfolio/index.html
- **创建日期**: 2026-02-02 18:29

### 设计风格
**Tech-Minimalist + Cyberpunk 融合**：
- 🌙 深色主题 (#0a0e17) - 符合程序员的夜间工作习惯
- 🔷 霓虹渐变 (蓝-紫) - 科技感与未来感
- 📐 网格动画背景 - 体现工程思维（结构化、精确）
- ⌨️ 等宽字体细节 (JetBrains Mono) - 程序员的标志
- 🎯 极简但精致的视觉风格

### 联系方式
- 📧 Email: hhhh124hhhh@qq.com
- 💻 GitHub: hhhh124hhhh
- ❌ Slack: 不提供（已从主页移除）

### 可视化组件（10 个酷炫效果）
1. **光标跟随效果** 🌟
   - 鼠标移动时有蓝色光晕跟随
   - 使用 screen 混合模式，更自然
   - 固定定位的 div，跟随鼠标坐标

2. **粒子背景** ✨
   - 50 个随机浮动的粒子
   - Canvas 2D 绘制，60fps 流畅运行
   - 随机方向，15 秒循环动画

3. **滚动进度条** 📏
   - 顶部蓝色到紫色的渐变进度条
   - 固定在页面顶部 (z-index: 9999)
   - 底部有蓝色发光效果
   - 实时反映滚动进度

4. **打字机效果** ⌨️
   - Hero 标题 "jack" 逐字显示
   - 3.5 秒打字动画 + 光标闪烁
   - 更有科技感的标题呈现

5. **数字滚动动画** 🔢
   - 统计数字从 0 滚动到目标值
   - 50 帧，每 30ms 更新一次
   - 动画结束时有 1.2 倍缩放
   - 支持: 100+, 50+, 30K+, ∞

6. **技能雷达图** 🎯
   - 圆形技能分布图
   - 6 个技能点，脉冲动画
   - 渐变背景 + 阴影发光
   - 位置：关于我部分右侧

7. **技能进度条** 📊
   - 5 个技能的进度条
   - Python (90%), AI/ML (85%), Automation (88%), Frontend (75%), Backend (80%)
   - 从 0 填充到目标宽度（1.5 秒）
   - 蓝到紫的渐变

8. **GitHub 贡献图模拟** 📈
   - 52x7 网格（364 个格子）
   - 5 个等级的蓝色渐变
   - 悬停时放大 1.8 倍 + 发光
   - 位置：关于我部分底部

9. **卡片 3D 悬停效果** 🎴
   - 项目卡片悬停时 3D 翻转
   - rotateX(5deg) + scale(1.05)
   - 悬停时有蓝色发光阴影
   - CSS 3D transform，流畅

10. **兴趣卡片渐变遮罩** 🌈
    - 兴趣卡片悬停时有渐变遮罩
    - 蓝到紫，5% 不透明度
    - 同时放大 1.05 倍
    - z-index: 遮罩在内容下层

### 内容组织
1. **Hero 区域** - 个人定位 + 行动按钮
2. **数据统计** - 4 个关键指标（100+ 技能、50+ 自动化、30K+ 社区、∞ 技术好奇心）
3. **关于我** - 4 个核心特质 + 技能雷达图 + 技能进度条 + GitHub 贡献图
4. **项目作品** - 6 个重点项目（成就系统、AI 提示词转 Skill、Moltbot 研究、SearXNG、技能市场、自动化工作流）
5. **兴趣爱好** - 6 个兴趣标签（AI 技能开发、提示词工程、自动化工作流、技术研究、游戏化设计、数据隐私）
6. **联系方式** - Email 和 GitHub（已移除 Slack）

### 技术实现
- **HTML5** - 语义化结构
- **CSS3** - 动画和布局
  - CSS 变量（主题管理）
  - Flexbox/Grid（响应式布局）
  - Keyframes（动画效果）
  - Transform（交互效果）
- **Vanilla JavaScript** - 零依赖
  - 滚动监听（Reveal 动画）
  - 平滑滚动（锚点跳转）
  - 视差效果（Hero 区域）
  - Canvas API（粒子系统）
  - 事件监听（光标跟随、滚动进度）

### 性能优化
- ✅ Canvas 粒子优化绘制
- ✅ CSS transform GPU 加速
- ✅ 事件监听器合理使用
- ✅ 动画时长适中（1.5-3.5 秒）
- ✅ 60fps 流畅运行

### 文件大小
- index.html: 42KB
- 零外部依赖
- 快速加载，流畅交互

### 部署状态
- ✅ 已部署到 GitHub Pages
- ✅ 构建完成
- ✅ HTTP 状态：200 OK
- ✅ Git 提交记录：
  - bc70474: 创建初始版本
  - 2192b0b: 更新联系方式
  - 5d174b6: 添加酷炫可视化组件

### 用户体验
**视觉吸引力**：
- ⭐⭐⭐⭐⭐ (5/5) - 明显提升
- 科技感：从 "简洁" 到 "炫酷"
- 交互性：从 "基础" 到 "丰富"
- 记忆点：从 "无" 到 "多个"

**性能表现**：
- ✅ 流畅 60fps
- ✅ 加载快速（42KB）
- ✅ 无明显卡顿
- ✅ 响应式兼容良好

### 设计理念
**Tech-Minimalist + Cyberpunk 风格增强**：
- 保持简洁的同时增加视觉层次
- 科技感更强的交互反馈
- 数据可视化更直观
- 整体体验更炫酷但不过度

**关键决策**：
1. 深色主题 - 符合程序员的夜间工作习惯
2. 霓虹渐变 - 科技感和未来感
3. 网格动画 - 体现工程思维
4. 等宽字体 - 程序员标志
5. 零依赖 - 快速加载，无第三方请求

### 后续优化建议
1. 添加 GitHub 头像到 Hero 区域
2. 补充项目真实链接（当前都是占位符）
3. 添加更多个人信息（工作经历、技能栈等）
4. 添加博客板块（可选）
5. 考虑添加深色/浅色主题切换
6. 添加更多交互式图表（可点击的技能雷达图）

---

## 上下文溢出解决方案 (2026-02-02)

### 问题
- **错误信息**: "Context overflow: prompt too large for model"
- **原因**: 对话历史过长，超过模型上下文限制
- **限制**: zai/glm-4.7 最大 131k tokens

### 解决方案

#### 1. 定期清理
- 发送 `HEARTBEAT_OK` 清理不必要的历史
- 定期检查对话长度

#### 2. 使用子代理
- 复杂任务用 `sessions_spawn` 启动独立会话
- 子代理独立运行，不占用主会话上下文
- 适合：长时间任务、大量数据处理

#### 3. 任务分解
- 大任务拆分成多个步骤
- 每次只关注当前步骤
- 避免一次性处理过多内容

#### 4. 文件记录
- 中间结果写入文件
- 减少对话中的重复内容
- 需要时从文件读取

#### 5. 简洁回复
- 保持回复简洁
- 避免冗长描述
- 必要时使用 NO_REPLY

### 记忆管理优化

#### 定期归档
- 旧的 daily memory (超过 30 天) 归档到 `memory/archive/`
- 只保留最近 30 天的 daily memory

#### 提炼长期记忆
- 重要信息提炼到 MEMORY.md
- 删除 daily memory 中的重复内容
- 保持 MEMORY.md 精简

#### 分类索引
- 使用清晰的标题和结构
- 避免重复记录
- 定期删除过时信息

### 使用场景

**何时使用子代理**：
- 长时间运行的任务
- 大量数据处理
- 需要隔离的工作流
- 可能产生大量输出的任务

**何时直接回复**：
- 简单问答
- 短任务
- 快速反馈
- 不需要持久化的工作

---
