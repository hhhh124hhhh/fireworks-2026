#!/bin/bash
# AI Research Cron - 深夜 AI 信息搜索任务（改进版）
# 功能：使用 SearXNG 搜索 AI 相关信息，分析并保存到 memory/ai-research/
# 改进：添加超时控制、更好的错误处理、重试机制

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
WORKSPACE="/root/clawd"
MEMORY_DIR="$WORKSPACE/memory/ai-research"
LOG_FILE="$MEMORY_DIR/research.log"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
DATE=$(date +%Y-%m-%d)

# 超时配置（秒）
SEARCH_TIMEOUT=30
MAX_RETRIES=2

# 创建目录
mkdir -p "$MEMORY_DIR"

# 函数：输出带时间戳的日志
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}" | tee -a "$LOG_FILE"
}

# 函数：使用 SearXNG 搜索（带超时和重试）
search_searxng() {
    local query="$1"
    local output_file="$2"
    local retry=0

    while [ $retry -le $MAX_RETRIES ]; do
        log "INFO" "搜索: $query (尝试 $((retry + 1))/$((MAX_RETRIES + 1)))"

        # 使用 timeout 命令限制执行时间
        if timeout $SEARCH_TIMEOUT curl -s "http://localhost:8080/search?format=json&q=$(echo "$query" | sed 's/ /%20/g')&category=search" -o "$output_file" 2>/dev/null; then
            # 检查是否成功获取结果
            if [ -f "$output_file" ] && [ -s "$output_file" ]; then
                local count=$(cat "$output_file" | jq '.results | length' 2>/dev/null || echo "0")
                if [ "$count" -gt 0 ]; then
                    log "INFO" "✅ 搜索成功，找到 $count 个结果"
                    return 0
                fi
            fi
            log "WARN" "⚠️ 搜索返回空结果或无效格式"
        else
            log "WARN" "⚠️ 搜索超时或失败 (尝试 $((retry + 1))/$((MAX_RETRIES + 1)))"
        fi

        retry=$((retry + 1))
        if [ $retry -le $MAX_RETRIES ]; then
            log "INFO" "等待 2 秒后重试..."
            sleep 2
        fi
    done

    log "ERROR" "❌ 搜索失败，已达到最大重试次数"
    return 1
}

# 函数：分析搜索结果
analyze_results() {
    local input_file="$1"
    local output_file="$2"
    local topic="$3"

    log "INFO" "分析结果: $topic"

    if [ ! -f "$input_file" ] || [ ! -s "$input_file" ]; then
        log "WARN" "输入文件不存在或为空: $input_file"
        echo "搜索失败，无结果" > "$output_file"
        return 1
    fi

    # 简单统计
    local count=$(cat "$input_file" | jq '.results | length' 2>/dev/null || echo "0")

    if [ "$count" -eq 0 ]; then
        log "WARN" "未找到结果"
        echo "未找到相关结果" > "$output_file"
        return 0
    fi

    # 提取标题和 URL
    cat "$input_file" | jq -r '.results[] | "- \(.title): \(.url)"' 2>/dev/null > "$output_file"

    if [ $? -ne 0 ]; then
        log "WARN" "解析 JSON 失败"
        echo "解析失败" > "$output_file"
        return 1
    fi

    log "INFO" "✅ 找到 $count 个结果，已保存到: $output_file"
    return 0
}

# 主流程
main() {
    log "INFO" "========================================"
    log "INFO" "🔍 AI Research Cron 启动 (改进版)"
    log "INFO" "========================================"
    log "INFO" "开始时间: $(date)"
    log "INFO" "模式: 深夜 AI 研究搜索"
    log "INFO" "搜索超时: ${SEARCH_TIMEOUT}秒"
    log "INFO" "最大重试: ${MAX_RETRIES}次"

    # 搜索主题列表
    declare -A topics=(
        ["AI news"]="AI news 2026 artificial intelligence latest"
        ["AI tools"]="AI tools 2026 best new software"
        ["AI agents"]="AI agents 2026 autonomous workflow"
        ["AI prompt engineering"]="AI prompt engineering 2026 techniques"
        ["Claude AI"]="Claude AI 2026 Anthropic features"
        ["OpenAI"]="OpenAI 2026 GPT updates"
        ["multimodal AI"]="multimodal AI 2026 vision audio"
        ["AI coding"]="AI coding 2026 programming assistants"
    )

    local success_count=0
    local fail_count=0
    declare -a failed_topics

    # 对每个主题进行搜索
    for topic_name in "${!topics[@]}"; do
        local query="${topics[$topic_name]}"
        local json_file="$MEMORY_DIR/${topic_name// /_}_$TIMESTAMP.json"
        local md_file="$MEMORY_DIR/${topic_name// /_}_$TIMESTAMP.md"

        log "INFO" "----------------------------------------"
        log "INFO" "主题: $topic_name"

        # 搜索
        if search_searxng "$query" "$json_file"; then
            # 分析
            if analyze_results "$json_file" "$md_file" "$topic_name"; then
                success_count=$((success_count + 1))
            else
                fail_count=$((fail_count + 1))
                failed_topics+=("$topic_name")
            fi
        else
            fail_count=$((fail_count + 1))
            failed_topics+=("$topic_name")
        fi
    done

    # 生成汇总报告
    local report_file="$MEMORY_DIR/research_summary_$DATE.md"
    log "INFO" "生成汇总报告: $report_file"

    cat > "$report_file" << EOF
# AI Research Summary - $DATE

生成时间: $(date '+%Y-%m-%d %H:%M:%S')
搜索来源: SearXNG (localhost:8080)
搜索超时: ${SEARCH_TIMEOUT}秒
最大重试: ${MAX_RETRIES}次

## 执行统计

- **成功主题数:** $success_count
- **失败主题数:** $fail_count
- **总主题数:** $((${success_count} + ${fail_count}))

EOF

    if [ ${#failed_topics[@]} -gt 0 ]; then
        echo "## 失败的主题" >> "$report_file"
        echo "" >> "$report_file"
        for topic in "${failed_topics[@]}"; do
            echo "- $topic" >> "$report_file"
        done
        echo "" >> "$report_file"
    fi

    echo "## 搜索主题" >> "$report_file"
    echo "" >> "$report_file"

    for topic_name in "${!topics[@]}"; do
        local md_file="$MEMORY_DIR/${topic_name// /_}_$TIMESTAMP.md"
        local json_file="$MEMORY_DIR/${topic_name// /_}_$TIMESTAMP.json"

        echo "### $topic_name" >> "$report_file"
        echo "" >> "$report_file"

        if [ -f "$json_file" ] && [ -s "$json_file" ]; then
            local count=$(cat "$json_file" | jq '.results | length' 2>/dev/null || echo "0")
            echo "**找到结果数:** $count" >> "$report_file"
        else
            echo "**状态:** 搜索失败" >> "$report_file"
        fi
        echo "" >> "$report_file"

        if [ -f "$md_file" ] && [ -s "$md_file" ]; then
            cat "$md_file" >> "$report_file"
        fi
        echo "" >> "$report_file"
    done

    log "INFO" "========================================"
    log "INFO" "✅ AI Research Cron 完成"
    log "INFO" "========================================"
    log "INFO" "完成时间: $(date)"
    log "INFO" "成功: $success_count, 失败: $fail_count"
    log "INFO" "汇总报告: $report_file"
    log "INFO" "详细日志: $LOG_FILE"

    # 返回成功（即使有失败的主题）
    return 0
}

# 执行主流程
main
exit_code=$?

exit $exit_code
