# Cron 任务总结

## 更新时间
2026-02-10 08:06

## Cron 任务列表

### 现有任务

| 时间 | 任务 | 日志文件 |
|------|------|----------|
| 0 0 * * * | Daily Auto Update | `/root/clawd/logs/clawdbot-update-cron.log` |
| 0 9 * * * | ClawdHub Stats Tracking | `/root/clawd/memory/clawdhub-stats/cron.log` |
| 0 8 * * * | AI Research Extended | `/root/clawd/logs/ai-research-cron.log` |
| */30 * * * * | System Monitor (每 30 分钟) | `/root/clawd/logs/monitoring-cron.log` |
| 0 2 * * * | Daily Growth Tutorial Generation | `/root/clawd/logs/daily-growth-cron.log` |
| 30 8 * * * | Content Discovery Assistant | `/root/clawd/logs/content-hotspot-cron.log` |
| 0 9 * * * | Daily Research Push | `/root/clawd/logs/daily-research-push-cron.log` |

### 新增任务 (2026-02-10)

| 时间 | 任务 | 日志文件 |
|------|------|----------|
| 0 * * * * | openclaw-gateway CPU Monitor (每小时) | `/root/clawd/logs/gateway-monitor-cron.log` |
| 0 3 * * * | openclaw-gateway Auto Restart (凌晨 3 点) | `/root/clawd/logs/gateway-restart-cron.log` |

## 监控脚本

### monitor-gateway-cron.sh
- 位置：`/root/clawd/scripts/monitor-gateway-cron.sh`
- 频率：每小时执行一次（0 * * * *）
- 功能：
  - 记录 CPU 使用率
  - 记录内存使用率
  - 记录运行时间
  - 记录线程数
  - 判断状态（OK/WARNING/HIGH_CPU）
  - 超过阈值时记录告警

### 监控数据存储

```
/root/clawd/memory/gateway-monitoring/
├── cpu-history-2026-02-10.log   # 历史记录（表格式）
├── cpu-detail-2026-02-10.log     # 详细日志
├── alerts.log                     # 告警日志
└── cpu-monitor.log                # 实时监控日志
```

## 监控阈值

- **OK**: CPU < 50%
- **WARNING**: 50% ≤ CPU < 80%
- **HIGH_CPU**: CPU ≥ 80%

## 历史数据格式

```csv
# Timestamp | PID | CPU% | MEM% | Elapsed | Threads | Status
1770681118 | 700810 | 2.0% | 19.8% | 2-16:51:25 | 15 | OK
1770681999 | 700810 | 2.0% | 20.6% | 2-17:06:06 | 15 | OK
```

## 自动重启

- **时间**: 凌晨 3:00 (0 3 * * *)
- **命令**: `/usr/bin/openclaw gateway restart`
- **日志**: `/root/clawd/logs/gateway-restart-cron.log`
- **目的**: 在睡觉时间重启 gateway，清理资源

## 管理命令

### 查看 crontab
```bash
crontab -l
```

### 编辑 crontab
```bash
crontab -e
```

### 测试监控脚本
```bash
bash /root/clawd/scripts/monitor-gateway-cron.sh
```

### 查看监控日志
```bash
# 查看历史记录
cat /root/clawd/memory/gateway-monitoring/cpu-history-2026-02-10.log

# 查看详细日志
cat /root/clawd/memory/gateway-monitoring/cpu-detail-2026-02-10.log

# 查看告警
cat /root/clawd/memory/gateway-monitoring/alerts.log
```

### 查看运行状态
```bash
# 查看进程
ps aux | grep openclaw-gateway

# 查看 CPU/内存
ps -p $(pgrep openclaw-gateway) -o %cpu,%mem,etime,thcount

# 查看日志
tail -f /root/clawd/logs/gateway-monitor-cron.log
```

## 故障排查

### 如果监控没有运行
1. 检查 crontab 是否正确：`crontab -l`
2. 检查脚本权限：`ls -l /root/clawd/scripts/monitor-gateway-cron.sh`
3. 检查 cron 日志：`grep CRON /var/log/syslog`

### 如果自动重启失败
1. 检查 openclaw 命令路径：`which openclaw`
2. 查看重启日志：`cat /root/clawd/logs/gateway-restart-cron.log`
3. 手动测试重启：`openclaw gateway restart`

### 如果 CPU 仍然很高
1. 查看历史数据，找出高峰时间
2. 检查是否有长时间运行的任务
3. 查看告警日志：`cat /root/clawd/memory/gateway-monitoring/alerts.log`
4. 考虑增加重启频率或调整阈值

## 注意事项

1. **监控数据保留**: 历史日志会按日期分割，建议定期清理旧日志
2. **告警级别**: 高 CPU 持续超过 80% 时，可能需要人工干预
3. **重启时机**: 凌晨 3 点通常不会有重要任务，适合重启
4. **日志位置**: 所有日志都保存在 `/root/clawd/logs/` 下，便于集中管理
