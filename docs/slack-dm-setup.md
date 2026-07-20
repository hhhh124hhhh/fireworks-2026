# Slack 私聊（DM）配置指南

## 📱 Slack 私聊 vs 频道

| 类型 | Channel ID 格式 | 示例 |
|------|----------------|------|
| 公共频道 | C 开头 | C0ABSK92X4G |
| 私有频道 | G 开头 | G0123456789 |
| 私聊（DM） | D 开头 | D0123456789 |

---

## 🔍 获取你的 Slack DM Channel ID

### 方法 1: 通过 Slack API（推荐）

1. 访问 https://api.slack.com/methods/conversations.list
2. 使用你的 Bot Token 调用 API
3. 查找 `type: "im"` 的会话

**curl 示例**:
```bash
curl -X POST \
  -H "Authorization: Bearer xoxb-10368920017285-10390963540401-IEWDdK63GDAbG1Gs1r0yX9WF" \
  -H "Content-Type: application/json" \
  https://slack.com/api/conversations.list?types=im
```

**返回示例**:
```json
{
  "ok": true,
  "channels": [
    {
      "id": "D0123456789",
      "name": "YOUR_USERNAME",
      "type": "im",
      "user": "U1234567890"
    }
  ]
}
```

### 方法 2: 通过 Clawdbot 测试

让我帮你查找你的 DM channel ID：

---

## ⚙️ 配置步骤

### 1. 获取 DM Channel ID

请提供你的 Slack 用户名，我帮你查找对应的 DM channel ID。

### 2. 修改配置文件

编辑 `~/.clawdbot/clawdbot.json`，在 `channels.slack.channels` 中添加：

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "channels": {
        "D0123456789": {
          "allow": true
        },
        "#general": {
          "allow": true
        }
      }
    }
  }
}
```

### 3. 重启 Clawdbot

```bash
clawdbot gateway restart
```

---

## 📝 测试私聊

配置完成后，发送测试消息：

```bash
# 方式 1: 使用 clawdbot message
clawdbot message send --channel slack --target D0123456789 --message "测试私聊"

# 方式 2: 使用脚本
python3 /root/clawd/scripts/test-slack.py
```

---

## 💡 使用建议

### 私聊适合发送：
- 🔍 任务进度报告
- 📊 定期统计信息
- ⚠️ 错误和警告
- 💬 日常对话

### 频道适合发送：
- 📢 公共通知
- 🎉 成功消息
- 🤖 自动化报告

---

## 🔧 混合模式配置

可以同时配置私聊和频道，实现双模式通知：

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "requireMention": false,
      "groupPolicy": "allowlist",
      "channels": {
        "D0123456789": {
          "allow": true,
          "notify": true
        },
        "C0ABSK92X4G": {
          "allow": true,
          "notify": false
        }
      }
    }
  }
}
```

---

## 📋 下一步

1. 请告诉我你的 Slack 用户名
2. 我帮你查找 DM channel ID
3. 配置完成后重启服务
4. 测试私聊功能

---

*需要我帮你查找 DM Channel ID 吗？*
