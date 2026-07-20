#!/bin/bash

# 定期监控 openclaw-gateway 的 CPU 使用率
# 通过 cron 每小时运行一次

LOG_DIR="/root/clawd/memory/gateway-monitoring"
TODAY=$(date '+%Y-%m-%d')
LOG_FILE="${LOG_DIR}/cpu-history-${TODAY}.log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 添加头部（如果文件不存在）
if [ ! -f "$LOG_FILE" ]; then
    echo "# Timestamp | PID | CPU% | MEM% | Elapsed | Threads | Status" > "$LOG_FILE"
fi

# 获取当前时间
NOW=$(date '+%Y-%m-%d %H:%M:%S')
TIMESTAMP=$(date '+%s')

# 检查 openclaw-gateway 进程是否存在
PID=$(pgrep -f "openclaw-gateway")

if [ -z "$PID" ]; then
    echo "${TIMESTAMP} | N/A  | N/A | N/A | N/A | N/A | NOT_RUNNING" >> "$LOG_FILE"
    # 发送告警
    echo "[${NOW}] CRITICAL: openclaw-gateway process is NOT running!" >> "${LOG_DIR}/alerts.log"
    exit 1
fi

# 获取 CPU 使用率
CPU_USAGE=$(ps -p $PID -o %cpu --no-headers | tr -d ' ')
MEM_USAGE=$(ps -p $PID -o %mem --no-headers | tr -d ' ')
ELAPSED=$(ps -p $PID -o etime --no-headers | tr -d ' ')
THREADS=$(ps -p $PID -o thcount --no-headers | tr -d ' ')

# 判断状态
STATUS="OK"
CPU_FLOAT=$(echo "$CPU_USAGE" | bc -l)
THRESHOLD_HIGH=80.0
THRESHOLD_MEDIUM=50.0

if (( $(echo "$CPU_FLOAT > $THRESHOLD_HIGH" | bc -l) )); then
    STATUS="HIGH_CPU"
    echo "[${NOW}] ALERT: CPU usage ${CPU_USAGE}% exceeds ${THRESHOLD_HIGH}%" >> "${LOG_DIR}/alerts.log"
elif (( $(echo "$CPU_FLOAT > $THRESHOLD_MEDIUM" | bc -l) )); then
    STATUS="WARNING"
    echo "[${NOW}] WARNING: CPU usage ${CPU_USAGE}% exceeds ${THRESHOLD_MEDIUM}%" >> "${LOG_DIR}/alerts.log"
fi

# 记录到历史日志
echo "${TIMESTAMP} | ${PID} | ${CPU_USAGE}% | ${MEM_USAGE}% | ${ELAPSED} | ${THREADS} | ${STATUS}" >> "$LOG_FILE"

# 也记录到详细日志
DETAIL_LOG="${LOG_DIR}/cpu-detail-${TODAY}.log"
echo "[${NOW}] PID=${PID} CPU=${CPU_USAGE}% MEM=${MEM_USAGE}% TIME=${ELAPSED} THREADS=${THREADS} STATUS=${STATUS}" >> "$DETAIL_LOG"

# 如果是告警状态，检查负载平均值
if [ "$STATUS" != "OK" ]; then
    LOAD_AVG=$(cat /proc/loadavg | awk '{print $1,$2,$3}')
    echo "[${NOW}] Load average: ${LOAD_AVG}" >> "${LOG_DIR}/alerts.log"
fi
