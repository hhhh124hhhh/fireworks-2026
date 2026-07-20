#!/bin/bash

# Daily Research Push Script
# 统一推送所有搜索结果到 Slack

set -e

# ============================================
# Configuration
# ============================================

AI_RESEARCH_SUMMARY_DIR="/root/clawd/memory/ai-research"
CONTENT_HOTSPOT_DIR="/root/clawd/projects/info-search/data/hotspots"
LOG_DIR="/root/clawd/logs/daily-research-push"
LOG_FILE="$LOG_DIR/daily-research-push-$(date +%Y%m%d-%H%M%S).log"
TODAY=$(date +%Y-%m-%d)
SLACK_CHANNEL="C0ABSK92X4G"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create directories
mkdir -p "$LOG_DIR"

# ============================================
# Helper Functions
# ============================================

log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

get_latest_file() {
    local dir="$1"
    local pattern="$2"
    local latest=$(ls -t "$dir" | grep "$pattern" | head -1)
    if [ -n "$latest" ]; then
        echo "$dir/$latest"
    else
        echo ""
    fi
}

# ============================================
# Main Execution
# ============================================

main() {
    log "INFO" "Starting daily research push"
    log "INFO" "Date: $TODAY"
    
    # Initialize message
    SLACK_MESSAGE="## 📊 **每日搜索报告** - $TODAY\n\n"
    
    # ========================================
    # Section 1: AI Research Hub
    # ========================================
    log "INFO" "Checking AI Research Hub results..."
    
    AI_SUMMARY_FILE=$(get_latest_file "$AI_RESEARCH_SUMMARY_DIR" "ai-research-summary-.*.md")
    
    if [ -n "$AI_SUMMARY_FILE" ]; then
        log "INFO" "Found AI Research Hub summary: $AI_SUMMARY_FILE"
        
        # Extract key info from summary
        AI_DATE=$(echo "$AI_SUMMARY_FILE" | grep -oP "ai-research-summary-\K\d+" | head -1)
        AI_DATE_FORMATTED=$(date -d "$AI_DATE" "+%Y-%m-%d %H:%M" 2>/dev/null || echo "$AI_DATE")
        
        # Extract search topics count
        AI_TOPICS=$(grep -c "搜索:" "$AI_SUMMARY_FILE" 2>/dev/null || echo 0)
        
        # Extract total results
        AI_TOTAL=$(grep "总结果:" "$AI_SUMMARY_FILE" 2>/dev/null | grep -oP '\d+' || echo 0)
        
        SLACK_MESSAGE+="### 🤖 **AI Research Hub**\n\n"
        SLACK_MESSAGE+="**生成时间**: $AI_DATE_FORMATTED\n"
        SLACK_MESSAGE+="**搜索主题**: $AI_TOPICS 个\n"
        SLACK_MESSAGE+="**总结果**: $AI_TOTAL 条\n"
        SLACK_MESSAGE+="**详细报告**: \`$AI_SUMMARY_FILE\`\n\n"
        
        log "INFO" "AI Research Hub: $AI_TOPICS topics, $AI_TOTAL results"
    else
        log "WARN" "No AI Research Hub summary found for today"
        SLACK_MESSAGE+="### 🤖 **AI Research Hub**\n\n"
        SLACK_MESSAGE+="⚠️ 今天还没有生成搜索报告\n\n"
    fi
    
    # ========================================
    # Section 2: Content Discovery Assistant
    # ========================================
    log "INFO" "Checking Content Discovery Assistant results..."
    
    HOTSPOT_FILE=$(get_latest_file "$CONTENT_HOTSPOT_DIR" "hotspot-report-.*.md")
    
    if [ -n "$HOTSPOT_FILE" ]; then
        log "INFO" "Found Content Discovery Assistant report: $HOTSPOT_FILE"
        
        # Extract hotspot count
        HOTSPOT_COUNT=$(grep -c "^###" "$HOTSPOT_FILE" 2>/dev/null || echo 0)
        
        # Extract collection time
        HOTSPOT_TIME=$(echo "$HOTSPOT_FILE" | grep -oP "hotspot-report-\K\d+" | head -1)
        HOTSPOT_TIME_FORMATTED=$(date -d "$HOTSPOT_TIME" "+%Y-%m-%d %H:%M" 2>/dev/null || echo "$HOTSPOT_TIME")
        
        # Extract top 3 hotspots (if available)
        TOP_HOTSPOTS=$(grep "^###" "$HOTSPOT_FILE" 2>/dev/null | head -3 | sed 's/^### //' | sed 's/^ *//')
        
        SLACK_MESSAGE+="### 🔥 **Content Discovery Assistant**\n\n"
        SLACK_MESSAGE+="**收集时间**: $HOTSPOT_TIME_FORMATTED\n"
        SLACK_MESSAGE+="**热点数量**: $HOTSPOT_COUNT 个\n"
        
        if [ -n "$TOP_HOTSPOTS" ]; then
            SLACK_MESSAGE+="**前 3 热点**: [查看完整报告](file://$HOTSPOT_FILE)\n\n"
        fi
        
        SLACK_MESSAGE+="**详细报告**: \`$HOTSPOT_FILE\`\n\n"
        
        log "INFO" "Content Discovery Assistant: $HOTSPOT_COUNT hotspots"
    else
        log "WARN" "No Content Discovery Assistant report found for today"
        SLACK_MESSAGE+="### 🔥 **Content Discovery Assistant**\n\n"
        SLACK_MESSAGE+="⚠️ 今天还没有收集热点\n\n"
    fi
    
    # ========================================
    # Section 3: Summary
    # ========================================
    SLACK_MESSAGE+="---\n\n"
    SLACK_MESSAGE+="### 📈 **今日搜索统计**\n\n"
    
    TOTAL_SEARCHES=0
    if [ -n "$AI_SUMMARY_FILE" ]; then
        TOTAL_SEARCHES=$((TOTAL_SEARCHES + 1))
    fi
    if [ -n "$HOTSPOT_FILE" ]; then
        TOTAL_SEARCHES=$((TOTAL_SEARCHES + 1))
    fi
    
    SLACK_MESSAGE+="**搜索系统运行**: $TOTAL_SEARCHES 个\n"
    SLACK_MESSAGE+="**数据保存位置**:\n"
    SLACK_MESSAGE+="- AI Research: \`/root/clawd/memory/ai-research/\`\n"
    SLACK_MESSAGE+="- Content Hotspots: \`/root/clawd/projects/info-search/data/hotspots/\`\n\n"
    
    SLACK_MESSAGE+="### 🔗 **快速访问**\n\n"
    
    if [ -n "$AI_SUMMARY_FILE" ]; then
        AI_BASENAME=$(basename "$AI_SUMMARY_FILE")
        SLACK_MESSAGE+="- [AI Research Hub 报告](file://$AI_SUMMARY_FILE)\n"
    fi
    
    if [ -n "$HOTSPOT_FILE" ]; then
        HOTSPOT_BASENAME=$(basename "$HOTSPOT_FILE")
        SLACK_MESSAGE+="- [Content Discovery 报告](file://$HOTSPOT_FILE)\n"
    fi
    
    SLACK_MESSAGE+="\n---\n\n"
    SLACK_MESSAGE+="*报告生成时间: $(date "+%Y-%m-%d %H:%M")*"
    
    # ========================================
    # Send to Slack
    # ========================================
    log "INFO" "Sending message to Slack channel: $SLACK_CHANNEL"
    
    echo -e "$SLACK_MESSAGE" | /usr/bin/openclaw message send \
        --channel slack \
        --target "$SLACK_CHANNEL" \
        --message-from-stdin 2>&1 | tee -a "$LOG_FILE"
    
    SLACK_EXIT_CODE=${PIPESTATUS[0]}
    
    if [ $SLACK_EXIT_CODE -eq 0 ]; then
        log "INFO" "✅ Successfully sent to Slack"
        echo -e "${GREEN}✅ 已成功推送到 Slack #clawdbot${NC}"
        echo -e "${BLUE}📊 统计: $TOTAL_SEARCHES 个搜索系统已运行${NC}"
    else
        log "ERROR" "❌ Failed to send to Slack (exit code: $SLACK_EXIT_CODE)"
        echo -e "${RED}❌ Slack 推送失败 (exit code: $SLACK_EXIT_CODE)${NC}"
        echo -e "${YELLOW}可能原因:${NC}"
        echo -e "${YELLOW}- OpenClaw message tool 配置问题${NC}"
        echo -e "${YELLOW}- Slack token 失效${NC}"
        echo -e "${YELLOW}- 网络连接问题${NC}"
    fi
    
    echo ""
    echo "=========================================="
    log "INFO" "Daily research push completed"
    echo "=========================================="
    echo ""
    echo "日志文件: $LOG_FILE"
    echo ""
    
    return $SLACK_EXIT_CODE
}

# Run main function
main
