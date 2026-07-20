#!/bin/bash

# openclaw-gateway CPU 监控脚本
# 记录 CPU 使用率到日志文件

LOG_DIR="/root/clawd/memory/gateway-monitoring"
LOG_FILE="${LOG_DIR}/cpu-monitor.log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 获取当前时间
NOW=$(date '+%Y-%m-%d %H:%M:%S')

# 检查 openclaw-gateway 进程是否存在
PID=$(pgrep -f "openclaw-gateway")

if [ -z "$PID" ]; then
    echo "[${NOW}] ERROR: openclaw-gateway process not found" >> "$LOG_FILE"
    exit 1
fi

# 获取 CPU 使用率
CPU_USAGE=$(ps -p $PID -o %cpu --no-headers | tr -d ' ')
MEM_USAGE=$(ps -p $PID -o %mem --no-headers | tr -d ' ')

# 获取进程运行时间
ELAPSED=$(ps -p $PID -o etime --no-headers | tr -d ' ')

# 获取线程数
THREADS=$(ps -p $PID -o thcount --no-headers | tr -d ' ')

# 记录到日志
echo "[${NOW}] PID=${PID} CPU=${CPU_USAGE}% MEM=${MEM_USAGE}% TIME=${ELAPSED} THREADS=${THREADS}" >> "$LOG_FILE"

# 如果 CPU 使用率超过 50%，记录警告
CPU_FLOAT=$(echo "$CPU_USAGE" | bc -l)
THRESHOLD=50.0

if (( $(echo "$CPU_FLOAT > $THRESHOLD" | bc -l) )); then
    echo "[${NOW}] WARNING: CPU usage ${CPU_USAGE}% exceeds ${THRESHOLD}%" >> "${LOG_DIR}/alerts.log"
    # 同时发送到当前 session 的日志（如果是 heartbeat 触发）
    echo "⚠️ ALERT: openclaw-gateway CPU usage is ${CPU_USAGE}%"
fi

# 输出当前状态（便于脚本调用时直接看到）
echo "PID=${PID} CPU=${CPU_USAGE}% MEM=${MEM_USAGE}% TIME=${ELAPSED} THREADS=${THREADS}"
