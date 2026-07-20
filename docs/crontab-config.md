# Cron Jobs Configuration

## 当前定时任务

### 1. Clawdbot 自动更新
```bash
0 0 * * * /root/clawd/scripts/auto_update_clawdbot.sh >> /root/clawd/logs/clawdbot-update-cron.log 2>&1
```
**时间**: 每天 00:00
**日志**: `/root/clawd/logs/clawdbot-update-cron.log`

### 2. ClawdHub 统计追踪
```bash
0 9 * * * /root/clawd/scripts/track-clawdhub-stats.sh >> /root/clawd/memory/clawdhub-stats/cron.log 2>&1
```
**时间**: 每天 09:00
**日志**: `/root/clawd/memory/clawdhub-stats/cron.log`

### 3. AI Research Hub
```bash
0 8 * * * /root/clawd/projects/info-search/workflows/ai-research-extended.sh >> /root/clawd/logs/ai-research-cron.log 2>&1
```
**时间**: 每天 08:00
**日志**: `/root/clawd/logs/ai-research-cron.log`

### 4. 系统监控（新增）
```bash
*/30 * * * * /root/clawd/scripts/system-monitor.sh >> /root/clawd/logs/monitoring-cron.log 2>&1
```
**时间**: 每 30 分钟
**日志**: `/root/clawd/logs/monitoring-cron.log`

---

## 查看和编辑

### 查看当前定时任务
```bash
crontab -l
```

### 编辑定时任务
```bash
crontab -e
```

### 重启 Cron 服务
```bash
systemctl restart cron
```

### 检查 Cron 服务状态
```bash
systemctl status cron
```

---

## 日志位置

- Clawdbot 更新: `/root/clawd/logs/clawdbot-update-cron.log`
- ClawdHub 统计: `/root/clawd/memory/clawdhub-stats/cron.log`
- AI Research: `/root/clawd/logs/ai-research-cron.log`
- 系统监控: `/root/clawd/logs/monitoring-cron.log`
- 监控日志: `/root/clawd/logs/monitoring/`

---

## 添加定时任务

### 方法 1：使用 crontab 命令
```bash
# 创建临时文件
cat > /tmp/new-crontab.txt << EOF
* * * * * /path/to/script.sh >> /path/to/log.log 2>&1
EOF

# 安装新的 crontab
crontab /tmp/new-crontab.txt

# 验证
crontab -l
```

### 方法 2：使用编辑器
```bash
crontab -e
# 在编辑器中添加新行
# 保存后自动安装
```

---

## Cron 表达式说明

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-6, 0 = 星期日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

### 常用示例

| 表达式 | 说明 |
|--------|------|
| `0 0 * * *` | 每天 00:00 |
| `0 8 * * *` | 每天 08:00 |
| `*/30 * * * *` | 每 30 分钟 |
| `0 */2 * * *` | 每 2 小时 |
| `0 9 * * 1-5` | 周一到周五 09:00 |

---

## 备份和恢复

### 备份
```bash
crontab -l > /root/clawd/backups/crontab-backup-$(date +%Y%m%d-%H%M%S).txt
```

### 恢复
```bash
crontab /path/to/crontab-backup.txt
```

---

**最后更新**: 2026-02-08 22:41
**状态**: ✅ 正常运行
**Cron 服务**: Active
