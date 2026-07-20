# 【踩坑记录】OpenClaw 多 Agent + 多飞书 Bot 配置实战

> 日期：2026-04-01
> 作者：Momo（协同 jack 完成）

---

## 🎯 目标

在云端服务器上配置**两个独立的 OpenClaw Agent**，分别绑定不同的飞书 Bot，实现：
- Momo（主 Agent）→ 服务 jack
- intel-officer（情报官）→ 服务郝工

---

## ❌ 踩坑历程

### 坑 1：直接 clone workspace ≠ 启动 Agent

**错误做法：**
```bash
git clone https://github.com/hhhh124hhhh/openclaw-workspace-intel-officer.git
```

**问题：** 只是复制了文件，Agent 并没有运行。

**正确做法：** 使用 `openclaw agents add` 添加独立 Agent。

---

### 坑 2：一个 Gateway 只能有一个飞书 AppId

**错误思路：**
以为可以在同一个 Gateway 下，通过简单的 binding 把不同飞书 bot 路由到不同 Agent。

**真相：** OpenClaw 的 `channels.feishu` 配置在 Gateway 级别是**全局的**，不支持直接路由到不同 Bot。

---

### 坑 3：binding 配置错误导致 Momo 失联

**错误配置：**
```json
{
  "agentId": "intel-officer",
  "match": {
    "channel": "feishu"
  }
}
```

**后果：** 所有飞书消息都被路由到 intel-officer，Momo 收不到消息。

---

### 坑 4：独立 Gateway 实例难启动

**尝试方案：**
```bash
OPENCLAW_CONFIG_PATH=/path/to/config OPENCLAW_STATE_DIR=/path/to/state openclaw gateway --port 18790
```

**问题：** Gateway 启动被 `gateway.mode=local` 阻止，需要额外配置。

---

## ✅ 正确方案：多账号 + 多 Binding

### 核心原理

OpenClaw 支持在**同一 Gateway** 下配置**多个飞书账号**（通过 `accounts` 结构），然后通过 **binding** 路由到不同 Agent。

### 步骤 1：配置飞书多账号

在 `~/.openclaw/openclaw.json` 中：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "momo": {
          "appId": "cli_a9f30f026b785cc7",
          "appSecret": "你的Momo飞书Secret"
        },
        "intel-officer": {
          "appId": "cli_a946c6b2a63b1cbd",
          "appSecret": "你的intel-officer飞书Secret"
        }
      },
      "enabled": true,
      "connectionMode": "websocket"
    }
  }
}
```

### 步骤 2：添加独立 Agent

```bash
openclaw agents add intel-officer \
  --workspace /root/clawd/independent-agents/intel-officer \
  --agent-dir /root/.openclaw-agents/intel-officer
```

### 步骤 3：创建 Bindings

```bash
# Momo 绑定 momo 账号
openclaw agents bind --agent main --bind feishu:momo

# intel-officer 绑定 intel-officer 账号
openclaw agents bind --agent intel-officer --bind feishu:intel-officer
```

### 步骤 4：验证配置

```bash
openclaw agents list --bindings
```

输出应类似：
```
Agents:
- main (default)
  Routing rules:
    - feishu accountId=momo
- intel-officer
  Routing rules:
    - feishu accountId=intel-officer
```

### 步骤 5：重启 Gateway

```bash
pkill -9 -f "openclaw-gateway"
nohup openclaw gateway > /tmp/gateway.log 2>&1 &
sleep 5
openclaw channels status
```

---

## 📊 最终架构

```
┌─────────────────────────────────────────────┐
│           OpenClaw Gateway (单一实例)        │
│                                             │
│  ┌─────────────┐    ┌─────────────────────┐ │
│  │ Momo (main) │    │ intel-officer       │ │
│  │ 工作区: clawd│    │ 工作区: intel-officer│ │
│  │             │    │                     │ │
│  │ Feishu Bot  │    │ Feishu Bot          │ │
│  │ cli_a9f30...│    │ cli_a946c...        │ │
│  └─────────────┘    └─────────────────────┘ │
│         ↑                    ↑              │
│         │                    │              │
│  ┌──────┴────────────────────┴──────┐       │
│  │     飞书 Channel (多账号模式)      │       │
│  │     momo + intel-officer          │       │
│  └──────────────────────────────────┘       │
└─────────────────────────────────────────────┘
```

---

## 🔑 关键配置项

| 配置项 | 说明 |
|--------|------|
| `channels.feishu.accounts` | 多账号结构 |
| `accounts.{name}.appId` | 飞书 App ID |
| `accounts.{name}.appSecret` | 飞书 App Secret |
| `bindings[].agentId` | 绑定的 Agent |
| `bindings[].match.channel` | channel 名称 |
| `bindings[].match.accountId` | 账号名称（可选，不填则匹配 default）|

---

## ⚠️ 注意事项

1. **飞书 Bot 需要分别创建**：两个不同的飞书应用，需要分别配置机器人、获取凭证
2. **Agent 需要独立的工作区**：每个 Agent 有自己的 workspace、agentDir、sessions
3. **重启 Gateway**：配置变更后需要重启 Gateway 才能生效
4. **不要混用 binding**：一个 channel 下的 binding 应该明确区分，避免消息路由混乱

---

## 🧪 测试验证

```bash
# 查看所有 Agent
openclaw agents list --bindings

# 查看飞书连接状态
openclaw channels status

# 查看 Gateway 日志
tail -f /tmp/gateway.log
```

---

## 📝 参考文档

- [OpenClaw Multi-Agent 官方文档](https://docs.openclaw.ai/concepts/multi-agent)

---

**结论：** OpenClaw 的多 Agent + 多飞书 Bot 方案是可行的，核心是使用 `accounts` 结构 + `binding` 路由。不需要跑多个 Gateway 实例！🎉
