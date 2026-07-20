#!/bin/bash

# System Monitoring Script
# Uses monitoring-expert skill as reference for best practices

set -e

# ============================================
# Configuration
# ============================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="/root/clawd/logs/monitoring"
LOG_FILE="$LOG_DIR/system-monitor-$(date +%Y%m%d-%H%M%S).log"
STATE_FILE="$LOG_DIR/monitoring-state.json"
ALERT_THRESHOLD_CPU=80
ALERT_THRESHOLD_MEM=80
ALERT_THRESHOLD_DISK=85
SLACK_CHANNEL="C0ABSK92X4G"

# Create log directory if not exists
mkdir -p "$LOG_DIR"

# ============================================
# Helper Functions (Structured Logging - monitoring-expert best practice)
# ============================================

log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE" >&2
}

# ============================================
# Metrics Collection (Counter, Gauge, Histogram - monitoring-expert pattern)
# ============================================

collect_metrics() {
    log "INFO" "Starting metrics collection"

    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    local mem_usage=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
    local disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    local running_containers=$(docker ps --format '{{.Names}}' | wc -l)

    # Get SearXNG status - try docker inspect first
    local searxng_status
    searxng_status=$(docker inspect searxng --format='{{.State.Status}}' 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$searxng_status" ]; then
        log "WARN" "docker inspect failed, using docker ps fallback"
        searxng_status=$(docker ps --format '{{.Names}}:{{.State}}' | grep "^searxng:" | cut -d':' -f2 || echo "not_found")
    fi

    local openclaw_status=$(pgrep -f "openclaw" > /dev/null 2>&1 && echo "running" || echo "stopped")

    # Ensure status is not empty
    [ -z "$searxng_status" ] && searxng_status="unknown"

    # Build JSON properly - use proper quoting to avoid variable expansion issues
    local metrics_json='{"timestamp":"'$(date -Iseconds)'","containers_running":'$running_containers',"cpu_usage":'$cpu_usage',"memory_usage":'$mem_usage',"disk_usage":'$disk_usage',"searxng_status":"'"$searxng_status"'","openclaw_status":"'"$openclaw_status"'"}'

    echo "$metrics_json" > "$STATE_FILE"
    log "INFO" "Metrics collected: CPU: ${cpu_usage}%, Mem: ${mem_usage}%, Disk: ${disk_usage}%, SearXNG: ${searxng_status}"

    # Return metrics for alerting check
    echo "$metrics_json"
}

# ============================================
# Alerting (monitoring-expert: Alert on meaningful events, avoid alert fatigue)
# ============================================

check_alerts() {
    local metrics_json="$1"

    local cpu_usage=$(echo "$metrics_json" | jq -r '.cpu_usage')
    local mem_usage=$(echo "$metrics_json" | jq -r '.memory_usage')
    local disk_usage=$(echo "$metrics_json" | jq -r '.disk_usage')
    local searxng_status=$(echo "$metrics_json" | jq -r '.searxng_status')
    local openclaw_status=$(echo "$metrics_json" | jq -r '.openclaw_status')

    local alerts=()

    # CPU alert
    if (( $(echo "$cpu_usage > $ALERT_THRESHOLD_CPU" | bc -l 2>/dev/null || echo "0") )); then
        alerts+=("⚠️ CPU usage high: ${cpu_usage}%")
        log "WARN" "CPU usage high: ${cpu_usage}%"
    fi

    # Memory alert
    if (( $(echo "$mem_usage > $ALERT_THRESHOLD_MEM" | bc -l 2>/dev/null || echo "0") )); then
        alerts+=("⚠️ Memory usage high: ${mem_usage}%")
        log "WARN" "Memory usage high: ${mem_usage}%"
    fi

    # Disk alert
    if [ "$disk_usage" -gt "$ALERT_THRESHOLD_DISK" ]; then
        alerts+=("⚠️ Disk usage high: ${disk_usage}%")
        log "WARN" "Disk usage high: ${disk_usage}%"
    fi

    # SearXNG container alert
    if [ "$searxng_status" != "running" ]; then
        alerts+=("🔴 SearXNG container not running: $searxng_status")
        log "ERROR" "SearXNG container not running: $searxng_status"
    fi

    # OpenClaw Gateway alert
    if [ "$openclaw_status" != "running" ]; then
        alerts+=("🔴 OpenClaw Gateway not running")
        log "ERROR" "OpenClaw Gateway not running"
    fi

    # Send alerts if any
    if [ ${#alerts[@]} -gt 0 ]; then
        send_alert "${alerts[@]}"
    fi
}

# ============================================
# Alert Notification
# ============================================

send_alert() {
    local alerts=("$@")

    local alert_message="🚨 **System Alert**\n\n"
    for alert in "${alerts[@]}"; do
        alert_message+="$alert\n"
    done
    alert_message+="\nTimestamp: $(date -Iseconds)"

    # Send to Slack (escape newlines for command line)
    local escaped_message=$(echo -e "$alert_message" | sed ':a;N;$!ba;s/\n/\\n/g')
    /usr/bin/openclaw message send --channel slack --target "$SLACK_CHANNEL" --message "$escaped_message"
}

# ============================================
# Docker Container Monitoring
# ============================================

monitor_containers() {
    log "INFO" "Monitoring Docker containers"

    # Get all containers
    local containers=$(docker ps -a --format "{{.Names}}:{{.State}}")

    for container in $containers; do
        local name=$(echo "$container" | cut -d':' -f1)
        local state=$(echo "$container" | cut -d':' -f2)

        log "INFO" "Container $name: $state"

        # Restart if exited (auto-recovery)
        if [[ "$state" =~ "Exited" ]]; then
            log "WARN" "Container $name is stopped, attempting restart"
            docker start "$name" 2>&1 | tee -a "$LOG_FILE"
        fi
    done
}

# ============================================
# Cron Task Monitoring
# ============================================

monitor_cron() {
    log "INFO" "Monitoring cron tasks"

    # Check recent cron logs
    if [ -f /root/clawd/logs/ai-research-cron.log ]; then
        local last_run=$(tail -1 /root/clawd/logs/ai-research-cron.log 2>/dev/null | head -1)
        log "INFO" "Last AI Research cron run: ${last_run:-No data}"
    fi

    # Check content hotspot collector logs
    if [ -f /root/clawd/logs/content-hotspot-collector.log ]; then
        local last_run=$(tail -1 /root/clawd/logs/content-hotspot-collector.log 2>/dev/null | head -1)
        log "INFO" "Last Content Discovery cron run: ${last_run:-No data}"
    fi
}

# ============================================
# Health Check Endpoints (monitoring-expert: Implement health check endpoints)
# ============================================

check_health() {
    log "INFO" "Checking service health"

    # Check SearXNG endpoint
    if curl -s -f http://localhost:8080 > /dev/null 2>&1; then
        log "INFO" "SearXNG health check: OK"
    else
        log "WARN" "SearXNG health check: FAILED"
    fi

    # Check OpenClaw Gateway (if API available)
    if openclaw status > /dev/null 2>&1; then
        log "INFO" "OpenClaw Gateway health check: OK"
    else
        log "WARN" "OpenClaw Gateway health check: FAILED"
    fi
}

# ============================================
# Dashboard Report (monitoring-expert: Create dashboards with RED/USE method)
# ============================================

generate_report() {
    log "INFO" "Generating monitoring report"

    local metrics_json=$(cat "$STATE_FILE")

    local cpu_usage=$(echo "$metrics_json" | jq -r '.cpu_usage')
    local mem_usage=$(echo "$metrics_json" | jq -r '.memory_usage')
    local disk_usage=$(echo "$metrics_json" | jq -r '.disk_usage')
    local running_containers=$(echo "$metrics_json" | jq -r '.containers_running')
    local searxng_status=$(echo "$metrics_json" | jq -r '.searxng_status')
    local openclaw_status=$(echo "$metrics_json" | jq -r '.openclaw_status')

    local report="📊 **System Monitoring Report**\n\n"
    report+="**Timestamp**: $(date -Iseconds)\n\n"
    report+="**System Resources**:\n"
    report+="• CPU Usage: ${cpu_usage}%\n"
    report+="• Memory Usage: ${mem_usage}%\n"
    report+="• Disk Usage: ${disk_usage}%\n\n"
    report+="**Services**:\n"
    report+="• Running Containers: $running_containers\n"
    report+="• SearXNG: $searxng_status\n"
    report+="• OpenClaw Gateway: $openclaw_status\n\n"
    report+="**Health Checks**: ✅ All critical services monitored\n\n"
    report+="Logs: \`$LOG_FILE\`"

    echo -e "$report"
}

# ============================================
# Main Execution
# ============================================

main() {
    log "INFO" "Starting system monitoring"

    # Collect metrics
    local metrics_json=$(collect_metrics)

    # Check for alerts
    check_alerts "$metrics_json"

    # Monitor containers
    monitor_containers

    # Monitor cron tasks
    monitor_cron

    # Check health
    check_health

    # Generate report
    local report=$(generate_report)

    log "INFO" "Monitoring completed"
    echo -e "$report"
}

# Run main function
main
