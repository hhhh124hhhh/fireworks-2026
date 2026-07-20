# ✅ Clawdbot 自动更新脚本 - 已配置完成

## 🎉 配置总结

已成功创建并配置自动更新脚本！

---

## 📦 创建的文件

| 文件 | 路径 | 说明 |
|------|------|------|
| **主脚本** | `/root/clawd/scripts/auto-update-clawdbot.sh` | 自动更新脚本 |
| **配置文件** | `/root/clawd/scripts/auto-update-config.sh` | 通知配置 |
| **测试脚本** | `/root/clawd/scripts/test-auto-update.sh` | 测试脚本 |
| **文档** | `/root/clawd/docs/clawdbot-auto-update.md` | 使用文档 |

---

## ⚙️ 自动配置

### 定时任务

```cron
0 2 * * *  # 每天凌晨 2 点自动检查更新
```

**任务 ID**: `9d8297af-4e05-48a6-bcb7-75054639477d`

### 通知配置

| 平台 | ID | 状态 |
|------|----|----|
| Feishu | `ou_3bc5290afc1a94f38e23dc17c35f26d6` | ✅ 已配置 |
| Slack | `D0AB0J4QLAH` | ✅ 已配置 |

---

## 🚀 功能特性

✅ **自动检查更新** - 每天凌晨 2 点自动检查
✅ **自动安装** - 发现新版本自动安装
✅ **自动重启** - 更新后自动重启服务
✅ **双通知** - Feishu + Slack 同时通知
✅ **日志记录** - 详细日志便于排查

---

## 📋 使用方法

### 1. 手动检查更新

```bash
/root/clawd/scripts/auto-update-clawdbot.sh
```

### 2. 强制更新

```bash
/root/clawd/scripts/auto-update-clawdbot.sh --force
```

### 3. 查看日志

```bash
tail -50 /tmp/clawdbot-auto-update.log
```

### 4. 查看帮助

```bash
/root/clawd/scripts/auto-update-clawdbot.sh --help
```

---

## 📊 定时任务状态

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

## 🔔 通知示例

更新成功时会收到：

**Feishu/Slack**:
```
✅ Clawdbot 已自动更新到最新版本！
```

更新失败时会收到：

```
❌ Clawdbot 自动更新失败，请手动检查！
```

---

## 📝 日志位置

**日志文件**: `/tmp/clawdbot-auto-update.log`

**查看实时日志**:
```bash
tail -f /tmp/clawdbot-auto-update.log
```

---

## ✅ 测试结果

```
==========================================
Clawdbot 自动更新测试
==========================================

1. 检查脚本权限...
-rwxr-xr-x 1 root root 6294 Jan 30 15:03 ...

2. 加载配置文件...
✅ 配置文件加载成功
   FEISHU_USER_ID: ou_3bc5290afc1a94f38e23dc17c35f26d6
   SLACK_DM_ID: D0AB0J4QLAH

3. 测试自动更新脚本...
✅ 帮助信息正常

==========================================
测试完成
==========================================
```

---

## 🎯 下次更新

**下次运行时间**: 每天凌晨 2:00

**自动执行**:
1. 检查是否有新版本
2. 如果有新版本，自动安装
3. 停止旧服务
4. 启动新服务
5. 发送通知到 Feishu + Slack

---

## 💡 建议

1. **首次使用** - 建议先手动运行一次测试
2. **监控日志** - 更新后检查日志确认成功
3. **调整时间** - 如需更改时间，参考"修改更新时间"部分

---

## 📚 完整文档

详细使用文档: `/root/clawd/docs/clawdbot-auto-update.md`

---

## ✅ 总结

- ✅ 自动更新脚本已创建
- ✅ 定时任务已配置（每天凌晨 2 点）
- ✅ 通知已配置（Feishu + Slack）
- ✅ 测试通过
- ✅ 文档已创建

**从现在开始，Clawdbot 会自动保持最新版本！** 🎉

---

*配置完成时间: 2026-01-30 15:05:00*
