# Slack 私聊完整解决方案

## 🎯 目标

将 Clawdbot 配置为通过 Slack 私聊（DM）发送消息，避免群聊频道的干扰。

---

## 📱 Slack Channel ID 格式说明

| 类型 | ID 前缀 | 示例 | 用途 |
|------|---------|------|------|
| **公共频道** | C | C0ABSK92X4G | 公开讨论 |
| **私有频道** | G | G0123456789 | 私有群组 |
| **私聊 DM** | **D** | **D0123456789** | **一对一私聊** ✅ |

---

## 🚀 快速配置（5 分钟）

### 步骤 1: 在 Slack 中给 Bot 发消息

1. 打开你的 Slack
2. 在搜索框输入你的 Bot 名称
3. 点击"**发送消息**"
4. 随便发一条消息（如 "hello" 或 "test"）
5. ✅ 私聊窗口已创建！

### 步骤 2: 获取 DM Channel ID

**方法 A - 查看浏览器 URL（推荐）**

```
1. 打开和 Bot 的私聊窗口
2. 查看浏览器地址栏
3. URL 格式: https://your-workspace.slack.com/archives/D0123456789
4. 复制: D0123456789（D 开头的部分）
```

**方法 B - 使用浏览器 Console**

```
1. 在 Slack 私聊窗口按 F12
2. 切换到 "Console" 标签
3. 粘贴并回车:
```

```javascript
const channelId = window.location.pathname.split('/').pop();
if (channelId.startsWith('D')) {
  console.log('✅ DM Channel ID:', channelId);
  navigator.clipboard.writeText(channelId);
  console.log('✅ 已复制到剪贴板！');
} else {
  console.log('❌ 当前不是 DM 窗口');
}
```

### 步骤 3: 告诉我你的 DM Channel ID

将格式为 `D0123456789` 的 Channel ID 发送给我。

我会自动：
1. 验证格式
2. 配置到 clawdbot.json
3. 重启服务
4. 测试发送

---

## ⚙️ 配置文件格式

你的 `~/.clawdbot/clawdbot.json` 会被修改为：

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "mode": "socket",
      "requireMention": false,
      "groupPolicy": "allowlist",
      "channels": {
        "D0123456789": {
          "allow": true,
          "description": "个人私聊"
        }
      }
    }
  }
}
```

---

## 📝 配置完成后的使用

### 发送消息到私聊

```bash
# 使用 clawdbot 命令
clawdbot message send --channel slack --target D0123456789 --message "私聊消息"

# 使用脚本
python3 /root/clawd/scripts/test-slack.py
```

### 脚本中的使用

```javascript
// 在脚本中
const SLACK_DM_ID = "D0123456789";

clawdbot.message.send({
  channel: "slack",
  target: SLACK_DM_ID,
  message: "这是一条私聊消息"
});
```

---

## 💡 推荐配置方案

### 方案 1: 仅私聊（推荐用于个人使用）

```json
{
  "channels": {
    "slack": {
      "channels": {
        "D0123456789": {
          "allow": true
        }
      }
    }
  }
}
```

**优点**:
- ✅ 只有你能看到消息
- ✅ 不打扰他人
- ✅ 可以发送敏感信息

### 方案 2: 私聊 + 公共频道（推荐用于团队）

```json
{
  "channels": {
    "slack": {
      "channels": {
        "D0123456789": {
          "allow": true,
          "description": "个人私聊"
        },
        "C0ABSK92X4G": {
          "allow": true,
          "description": "团队频道"
        }
      }
    }
  }
}
```

**使用建议**:
- 私聊：任务进度、错误警告、敏感信息
- 频道：成功通知、公共报告、团队更新

---

## 🔧 实际使用示例

### 1. 定时任务发送到私聊

```bash
# 修改 cron 任务
clawdbot cron add \
  --name "daily-report" \
  --cron "0 9 * * *" \
  --session main \
  --system-event "运行 /root/clawd/scripts/quick-report.py 并发送到私聊"

# 脚本中指定发送目标
# 修改 /root/clawd/scripts/quick-report.py
# 将 SLACK_CHANNEL_ID 改为你的 DM ID
```

### 2. 脚本中发送进度报告

```javascript
// 在任何 Node.js 脚本中
const { execSync } = require('child_process');

function sendToSlackDM(message) {
  const SLACK_DM_ID = "D0123456789";
  execSync(`clawdbot message send --channel slack --target ${SLACK_DM_ID} --message "${message}"`);
}

// 使用
sendToSlackDM("任务完成！生成了 5 个新 Skill");
```

### 3. Bash 脚本中发送通知

```bash
#!/bin/bash
# 在任何 Bash 脚本中

SLACK_DM_ID="D0123456789"
MESSAGE="脚本执行完成！"

clawdbot message send \
  --channel slack \
  --target "$SLACK_DM_ID" \
  --message "$MESSAGE"
```

---

## 🧪 测试验证

### 配置完成后自动测试

```bash
# 我会自动运行测试
clawdbot message send --channel slack --target D0123456789 --message "✅ Slack 私聊配置成功！"

# 或使用测试脚本
python3 /root/clawd/scripts/test-slack.py
```

### 手动测试

1. 在 Slack 中查看 Bot 私聊窗口
2. 等待消息到达（通常 < 10 秒）
3. 确认收到测试消息

---

## 🔍 故障排查

### 问题 1: 收不到消息

**检查清单**:
- [ ] DM Channel ID 格式正确（D 开头）
- [ ] 已在 Slack 中给 Bot 发过消息
- [ ] Clawdbot 已重启
- [ ] Bot 没有被拉黑或静音

**解决方法**:
```bash
# 查看日志
clawdbot logs | grep slack

# 测试连接
clawdbot message send --channel slack --target D0123456789 --message "测试"
```

### 问题 2: 找不到 DM Channel ID

**解决方法**:
1. 确保已在 Slack 中和 Bot 对话过
2. 直接在 Slack 私聊窗口查看 URL
3. 如果 URL 中没有 D，尝试刷新页面

### 问题 3: 配置后没有生效

**解决方法**:
```bash
# 重启 Clawdbot
clawdbot gateway restart

# 等待 5-10 秒后测试
python3 /root/clawd/scripts/test-slack.py
```

---

## 📊 对比：私聊 vs 频道

| 特性 | 私聊 DM | 公共频道 |
|------|---------|----------|
| 隐私性 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 实时性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 干扰度 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| 适合内容 | 个人任务、敏感信息、错误警告 | 公共通知、成功消息 |
| 消息历史 | 仅自己可见 | 所有人可见 |

---

## 🎯 推荐使用场景

### ✅ 适合私聊发送:

- 🔍 任务进度报告
- ⚠️ 错误和警告
- 📊 统计和分析报告
- 💬 日常对话
- 🔐 敏感信息

### ❌ 不适合私聊发送:

- 📢 需要团队知道的通知
- 🎉 庆祝成功消息
- 🤖 自动化报告摘要（如果需要团队看到）

---

## 📚 相关文档

- Slack 主动消息指南: `/root/clawd/docs/slack-guide.md`
- Slack 卡顿问题解决: `/root/clawd/docs/slack-lag-solution.md`
- Slack 测试脚本: `/root/clawd/scripts/test-slack.py`

---

## ✅ 总结

1. ✅ 在 Slack 中给 Bot 发消息
2. ✅ 查看浏览器 URL 获取 DM Channel ID（D 开头）
3. ✅ 将 Channel ID 发给我
4. ✅ 我自动配置并测试
5. ✅ 开始使用私聊！

---

**准备好了吗？告诉我你的 DM Channel ID！**

格式：`D0123456789`（D 开头）

我马上帮你配置！🚀
