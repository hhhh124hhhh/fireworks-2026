# Slack 私聊快速设置

## 🚀 最简单的方法：直接给 Bot 发消息

### 步骤 1: 在 Slack 中私聊你的 Bot

1. 打开 Slack
2. 在搜索框输入你的 Bot 名称
3. 点击发送消息
4. 发送任何内容（如 "hello"）

这会自动创建 Bot 和你的 DM channel！

---

## 🔍 获取你的 DM Channel ID

### 方法 1: 使用浏览器开发者工具

1. 在 Slack 中与 Bot 私聊
2. 按 F12 打开开发者工具
3. 切换到 "Network" 标签
4. 刷新页面
5. 找到以 `conversations.info` 开头的请求
6. 查看 URL 中的 `channel` 参数
7. 格式通常是 `D` 开头，如 `D0123456789`

### 方法 2: 查看网页 URL

1. 在 Slack 中与 Bot 私聊
2. 查看浏览器地址栏
3. URL 格式类似：`https://workspace.slack.com/archives/D0123456789`
4. `D0123456789` 就是 DM Channel ID

---

## ⚙️ 配置 Clawdbot

### 1. 编辑配置文件

```bash
nano ~/.clawdbot/clawdbot.json
```

### 2. 添加 DM Channel

在 `channels.slack.channels` 中添加你的 DM ID：

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "channels": {
        "D0123456789": {
          "allow": true
        },
        "C0ABSK92X4G": {
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

## 🧪 测试

### 使用 Clawdbot 命令

```bash
clawdbot message send --channel slack --target D0123456789 --message "私聊测试成功！"
```

### 使用测试脚本

```bash
python3 /root/clawd/scripts/test-slack.py
```

---

## 💡 完整示例

假设你的 DM Channel ID 是 `D0123456789`：

### 配置文件

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "requireMention": false,
      "groupPolicy": "allowlist",
      "channels": {
        "D0123456789": {
          "allow": true
        }
      }
    }
  }
}
```

### 发送消息

```bash
# 发送到私聊
clawdbot message send --channel slack --target D0123456789 --message "这是一条私聊消息"

# 发送到频道
clawdbot message send --channel slack --target C0ABSK92X4G --message "这是一条频道消息"
```

---

## 📊 推荐配置

### 私聊 + 频道双模式

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
          "description": "个人 DM"
        },
        "C0ABSK92X4G": {
          "allow": true,
          "description": "工作频道"
        }
      }
    }
  }
}
```

### 私聊用于：

✅ **推荐私聊发送**：
- 个人任务进度
- 错误和警告
- 定期统计报告
- 敏感信息

❌ **推荐频道发送**：
- 公共通知
- 成功消息
- 自动化报告摘要

---

## 🔧 故障排查

### 问题 1: 收不到消息

**检查**：
1. DM Channel ID 是否正确（D 开头）
2. Clawdbot 是否重启
3. Bot 是否在 Slack 中被拉黑

### 问题 2: 找不到 DM Channel ID

**解决**：
1. 确保已在 Slack 中给 Bot 发过消息
2. 查看 Slack API logs：`clawdbot logs | grep slack`

### 问题 3: 消息发送到错误的地方

**解决**：
1. 检查 `--target` 参数
2. 确认 Channel ID 格式（D=DM, C=频道, G=群组）

---

## 📝 下一步

1. ✅ 在 Slack 中给 Bot 发消息创建 DM
2. ✅ 获取 DM Channel ID（D 开头）
3. ✅ 配置到 `clawdbot.json`
4. ✅ 重启 Clawdbot
5. ✅ 测试发送消息

---

## 💬 需要帮助？

如果你找到了 DM Channel ID，告诉我格式，我帮你配置！

或者提供：
- 你的 Slack 用户名
- 你的 Slack Workspace 名称

我可以尝试其他方法获取 ID。

---

*快速配置指南*
