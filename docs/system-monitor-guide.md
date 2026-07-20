# System Monitoring Script - 使用说明

## 📖 简介

基于 `monitoring-expert` 技能的最佳实践创建的自动化系统监控脚本。

**核心功能**：
- Docker 容器监控
- 系统资源监控（CPU、内存、磁盘）
- 定时任务监控
- 服务状态监控
- 自动报警（Slack 通知）

---

## 🎯 监控功能

### 1. 系统资源监控

**监控指标**（monitoring-expert：使用正确的指标类型）:
- **Counter**: 运行的容器数量
- **Gauge**: CPU 使用率
- **Gauge**: 内存使用率
- **Gauge**: 磁盘使用率

**报警阈值**:
- CPU 使用率 > 80%
- 内存使用率 > 80%
- 磁盘使用率 > 85%

### 2. Docker 容器监控

**监控内容**:
- 所有容器状态（运行中、停止、退出）
- 自动重启失败的容器
- SearXNG 容器状态

### 3. 服务状态监控

**监控服务**:
- SearXNG（localhost:8080）
- OpenClaw Gateway

**健康检查**:
- SearXNG HTTP 端点检查
- OpenClaw 状态检查

### 4. 定时任务监控

**监控内容**:
- AI Research Hub 定时任务日志
- Content Discovery Assistant 定时任务日志
- 最后执行时间

### 5. 自动报警

**报警条件**:
- CPU 使用率过高
- 内存使用率过高
- 磁盘空间不足
- 容器停止运行
- 服务不可用

**报警方式**:
- Slack 通知（#clawdbot）
- 结构化日志记录

---

## 🚀 快速开始

### 1. 手动执行监控

```bash
# 执行监控脚本
bash /root/clawd/scripts/system-monitor.sh

# 查看日志
tail -f /root/clawd/logs/monitoring/system-monitor-*.log
```

### 2. 设置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每 30 分钟执行一次）
*/30 * * * * /root/clawd/scripts/system-monitor.sh >> /root/clawd/logs/monitoring-cron.log 2>&1
```

### 3. 配置报警阈值（可选）

编辑脚本中的配置变量：

```bash
ALERT_THRESHOLD_CPU=80      # CPU 报警阈值（%）
ALERT_THRESHOLD_MEM=80      # 内存报警阈值（%）
ALERT_THRESHOLD_DISK=85     # 磁盘报警阈值（%）
SLACK_CHANNEL="C0ABSK92X4G"  # Slack 频道 ID
```

---

## 📊 监控报告

### 报告内容

执行脚本后会生成以下报告：

```
📊 **System Monitoring Report**

**Timestamp**: 2026-02-08T22:15:00+08:00

**System Resources**:
• CPU Usage: 15.2%
• Memory Usage: 45.3%
• Disk Usage: 62.1%

**Services**:
• Running Containers: 3
• SearXNG: running
• OpenClaw Gateway: running

**Health Checks**: ✅ All critical services monitored

Logs: `/root/clawd/logs/monitoring/system-monitor-20260208-221500.log`
```

### 状态文件

监控状态保存在：
```
/root/clawd/logs/monitoring/monitoring-state.json
```

内容示例：
```json
{
  "timestamp": "2026-02-08T22:15:00+08:00",
  "containers_running": 3,
  "cpu_usage": 15.2,
  "memory_usage": 45.3,
  "disk_usage": 62.1,
  "searxng_status": "running",
  "openclaw_status": "running"
}
```

---

## 🔧 最佳实践（monitoring-expert 指导）

### 1. 结构化日志

**使用结构化日志记录**（monitoring-expert 最佳实践）:

```bash
# 格式：[timestamp] [level] message
[2026-02-08T22:15:00+08:00] [INFO] Starting metrics collection
[2026-02-08T22:15:00+08:00] [WARN] CPU usage high: 85.2%
```

### 2. 指标类型选择

**使用正确的指标类型**（monitoring-expert）:

| 类型 | 用途 | 示例 |
|------|------|------|
| Counter | 累计数值 | 容器运行次数 |
| Gauge | 当前状态值 | CPU 使用率 |
| Histogram | 分布统计 | 响应时间分布 |

### 3. 避免报警疲劳

**只在有意义的时刻报警**（monitoring-expert 约束）:

✅ **应该报警**:
- CPU 使用率 > 80% 持续 5 分钟
- 内存使用率 > 80% 持续 5 分钟
- 关键容器停止运行

❌ **不应该报警**:
- 瞬间 CPU 峰值（< 1 秒）
- 短暂的网络波动
- 非关键容器的临时停止

### 4. 业务指标监控

**监控业务指标，不仅仅是技术指标**（monitoring-expert）:

- 定时任务执行状态
- 数据收集成功率
- 服务可用性（uptime）
- 关键功能可用性

### 5. 健康检查端点

**实现健康检查端点**（monitoring-expert）:

- SearXNG: `http://localhost:8080/health`
- OpenClaw Gateway: `openclaw status`
- API 服务: `/api/health`

---

## 📁 文件结构

```
/root/clawd/
├── scripts/
│   └── system-monitor.sh          # 监控脚本（主文件）
└── logs/
    └── monitoring/
        ├── system-monitor-*.log   # 监控日志
        ├── monitoring-state.json   # 监控状态
        └── monitoring-cron.log    # Cron 任务日志
```

---

## 🔍 故障排除

### 问题 1：Slack 通知不发送

**原因**: OpenClaw message tool 配置问题

**解决**:
```bash
# 检查 OpenClaw 配置
openclaw config

# 手动测试 Slack 通知
echo "Test message" | openclaw message send --channel slack --target C0ABSK92X4G --message-from-stdin
```

### 问题 2：Docker 容器监控失败

**原因**: Docker daemon 未运行

**解决**:
```bash
# 检查 Docker 状态
systemctl status docker

# 启动 Docker
systemctl start docker
```

### 问题 3：CPU/内存数据不准确

**原因**: 系统负载计算方法问题

**解决**:
- 脚本使用 `top` 和 `free` 命令获取数据
- 确保脚本在轻负载时执行以获取准确基线

---

## 📈 扩展建议

### 1. 添加更多监控指标

```bash
# 网络流量监控
network_in=$(cat /proc/net/dev | grep eth0 | awk '{print $2}')
network_out=$(cat /proc/net/dev | grep eth0 | awk '{print $10}')

# 磁盘 I/O 监控
disk_read=$(iostat -x | grep sda | awk '{print $4}')
disk_write=$(iostat -x | grep sda | awk '{print $5}')
```

### 2. 集成 Prometheus/Grafana

```bash
# 导出指标到 Prometheus
curl -X POST -d @"$STATE_FILE" http://localhost:9091/metrics/job/monitoring
```

### 3. 添加历史数据保存

```bash
# 保存历史状态
cp "$STATE_FILE" "$LOG_DIR/histories/monitoring-$(date +%Y%m%d-%H%M%S).json"
```

### 4. 添加趋势分析

```bash
# 对比当前和历史数据
if [ "$cpu_usage" -gt "$prev_cpu_usage" ]; then
    echo "CPU usage increased"
fi
```

---

## 📚 参考资料

**基于 monitoring-expert 技能的最佳实践**:
- 观察性三大支柱：日志、指标、追踪
- 结构化日志记录
- 使用正确的指标类型（Counter/Gauge/Histogram）
- 避免报警疲劳
- 监控业务指标
- 实现健康检查端点

---

**创建时间**: 2026-02-08 22:15
**基于技能**: monitoring-expert
**版本**: 1.0
**作者**: Momo 🔧
