# Memory: Debugging - 调试经验记录

存储所有调试经验和问题解决方案。

## 使用方法

### 获取调试经验
\`\`\`
memory_get("debugging", "slack")
memory_get("debugging", "feishu")
memory_get("debugging", "general")
\`\`\`

### 搜索调试经验
\`\`\`
memory_search("Slack 连接问题")
\`\`\`

## 内容索引

### 飞书问题排查（2026-01-29）

**问题描述**：WebSocket 连接正常，机器人可以主动发送消息，但无法接收用户发送的消息

**问题原因**：
- 插件缺少 user_p2p_chat_entered_v1 事件处理器
- 飞书 App 需要正确配置事件订阅（长连接模式）

**解决方案**：
1. 修改 /root/.clawdbot/extensions/feishu/src/monitor.ts
   - 添加了 user_p2p_chat_entered_v1 事件处理器
   - 同时添加了 im.chat.access_event.user_p2p_chat_entered_v1 以防万一
   
2. 重启 Gateway 使修改生效

**修复结果**：✅ 成功

**调试方法总结**：
- 使用 clawdbot status 检查通道状态
- 使用 tail -f /tmp/clawdbot/clawdbot-2026-01-29.log 实时监控日志
- 关键日志标记：feishu: received message, feishu: dispatching to agent

### Slack 配置优化（2026-01-29）

**配置变更**：
- 在 /root/.clawdbot/clawdbot.json 中添加 requireMention: false

**效果**：✅ 机器人更主动，可以自动回复所有消息，不需要 @

### Slack Bot 问题解决（2026-02-02）

**问题描述**：Slack Bot 不回复

**根本原因**：MEMORY.md 太大（39K），超过 Agent 上下文限制（20K）

**解决方案**：
1. 增加上下文限制到 100k
2. 添加新频道 C0AC87MUENP

**验证**：✅ 消息发送测试成功

### Slack Bot missing_scope 错误（2026-02-02）

**错误信息**：An API error occurred: missing_scope

**根本原因**：Bot Token 缺少必需的 OAuth scopes

**解决状态**：用户确认权限完整，问题已解决（可能是 Gateway 重启后重新获取权限）

### 通用调试技巧

**日志位置**：
- 主日志：/tmp/clawdbot/clawdbot-YYYY-MM-DD.log
- 使用 tail -f 实时监控

**重启命令**：
- 使用 gateway 工具：gateway(action="restart")
- 使用 CLI：clawdbot gateway restart

**状态检查**：
- clawdbot status - 查看所有通道状态
- ps aux | grep openclaw-gateway - 查看 Gateway 进程
- ss -tulpn | grep 18789 - 查看端口监听

## 版本历史
- 2026-02-02: 初始版本
