# Clawdbot 自动更新脚本

## 🚀 功能

- ✅ 自动检查更新（每天凌晨 2 点）
- ✅ 自动安装新版本
- ✅ 自动重启服务
- ✅ 发送通知（Feishu + Slack）
- ✅ 日志记录

---

## 📁 文件列表

| 文件 | 说明 |
|------|------|
| `auto-update-clawdbot.sh` | 主脚本 |
| `auto-update-config.sh` | 配置文件 |
| `test-auto-update.sh` | 测试脚本 |

---

## ⚙️ 配置

### 1. 编辑配置文件

```bash
nano /root/clawd/scripts/auto-update-config.sh
```

### 2. 配置选项

```bash
# Feishu 用户 ID（私聊）
export FEISHU_USER_ID="ou_3bc5290afc1a94f38e23dc17c35f26d6"

# Slack DM Channel ID
export SLACK_DM_ID="D0AB0J4QLAH"
```

---

## 🔧 使用方法

### 手动运行

```bash
# 检查并更新（如果有新版本）
/root/clawd/scripts/auto-update-clawdbot.sh

# 强制更新（无论是否有新版本）
/root/clawd/scripts/auto-update-clawdbot.sh --force

# 查看帮助
/root/clawd/scripts/auto-update-clawdbot.sh --help
```

### 运行测试

```bash
/root/clawd/scripts/test-auto-update.sh
```

---

## ⏰ 定时任务

已配置为每天凌晨 2 点自动检查更新：

```cron
0 2 * * *  # 每天凌晨 2 点
```

### 查看定时任务

```bash
clawdbot cron list | grep auto-update
```

### 修改更新时间

```bash
# 删除旧任务
clawdbot cron remove 9d8297af-4e05-48a6-bcb7-75054639477d

# 添加新任务（例如改为每天 9:00）
clawdbot cron add \
  --name "auto-update-clawdbot" \
  --cron "0 9 * * *" \
  --session main \
  --wake next-heartbeat \
  --system-event "运行 Clawdbot 自动更新脚本"
```

---

## 📊 通知

更新后会自动发送通知到：

**Feishu**:
- 用户 ID: `ou_3bc5290afc1a94f38e23dc17c35f26d6`

**Slack**:
- Channel ID: `D0AB0J4QLAH`

### 通知示例

```
✅ Clawdbot 已自动更新到最新版本！

❌ Clawdbot 自动更新失败，请手动检查！
```

---

## 📝 日志

日志文件: `/tmp/clawdbot-auto-update.log`

### 查看日志

```bash
# 查看最近 50 行
tail -50 /tmp/clawdbot-auto-update.log

# 实时监控日志
tail -f /tmp/clawdbot-auto-update.log
```

---

## 🔍 故障排查

### 问题 1: 脚本没有权限

```bash
chmod +x /root/clawd/scripts/auto-update-clawdbot.sh
```

### 问题 2: 定时任务没有运行

```bash
# 查看定时任务状态
clawdbot cron list

# 查看任务日志
tail -100 /tmp/clawdbot-auto-update.log
```

### 问题 3: 更新失败

```bash
# 手动运行并查看详细日志
/root/clawd/scripts/auto-update-clawdbot.sh --force
```

### 问题 4: 没有收到通知

检查配置文件中的用户 ID 是否正确：

```bash
cat /root/clawd/scripts/auto-update-config.sh
```

---

## 💡 最佳实践

1. **定期检查日志** - 每周查看一次更新日志
2. **监控服务状态** - 更新后确认服务正常运行
3. **备份重要数据** - 更新前备份数据（脚本已自动停止服务）
4. **调整更新时间** - 建议在低峰期运行（如凌晨）

---

## 📚 相关文档

- Clawdbot 官方文档: https://docs.clawd.bot
- Cron 任务管理: `clawdbot cron --help`

---

*最后更新: 2026-01-30*
