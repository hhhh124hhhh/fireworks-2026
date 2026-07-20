#!/bin/bash
# 数据源管理脚本
# 用于统一管理 AI 信息收集项目的数据源配置和健康检查

set -e

# 配置目录
CONFIG_DIR="/root/clawd/.config/data-sources"

# 日志设置
LOG_FILE="/root/clawd/logs/data-source-manager.log"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    local level=$1
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

# 显示帮助信息
show_help() {
    cat << EOF
数据源管理脚本 - 使用说明

用法: bash data-source-manager.sh [命令] [参数]

命令:
  help                    显示帮助信息

  test [数据源]          测试指定数据源
  check [数据源]          检查指定数据源的健康状态
  list                    列出所有数据源

  load [数据源]           加载指定数据源配置（输出到 stdout）
  config [数据源]         显示指定数据源的配置

  clean-cache [数据源]    清理指定数据源的缓存
  clean-logs [数据源]     清理指定数据源的日志

数据源:
  searxng                 SearXNG 隐私搜索引擎
  tavily                  Tavily Search API
  twitter                 Twitter/X API

示例:
  bash data-source-manager.sh test searxng
  bash data-source-manager.sh check tavily
  bash data-source-manager.sh list
  bash data-source-manager.sh clean-cache searxng

EOF
}

# 检查数据源配置是否存在
check_config_exists() {
    local source=$1
    local config_file="$CONFIG_DIR/${source}.conf"

    if [ ! -f "$config_file" ]; then
        log "ERROR" "配置文件不存在: $config_file"
        return 1
    fi

    return 0
}

# 加载数据源配置
load_config() {
    local source=$1
    local config_file="$CONFIG_DIR/${source}.conf"

    check_config_exists "$source" || return 1

    # 输出配置内容
    cat "$config_file"
}

# 测试 SearXNG
test_searxng() {
    log "INFO" "测试 SearXNG 数据源..."

    source "$CONFIG_DIR/searxng.conf"

    # 检查 SearXNG 是否可访问
    if ! curl -s -f --max-time "$TIMEOUT" "$SEARXNG_URL" > /dev/null 2>&1; then
        log "ERROR" "SearXNG 无法访问: $SEARXNG_URL"
        return 1
    fi

    # 检查首页是否可访问
    homepage=$(curl -s -f --max-time "$TIMEOUT" "$SEARXNG_URL/" 2>&1 || echo "")

    if echo "$homepage" | grep -q "SearXNG"; then
        log "INFO" "SearXNG 测试成功"
        return 0
    else
        log "ERROR" "SearXNG 首页测试失败"
        return 1
    fi
}

# 测试 Tavily
test_tavily() {
    log "INFO" "测试 Tavily 数据源..."

    source "$CONFIG_DIR/tavily.conf"

    # 检查 API Key
    if [ -z "$TAVILY_API_KEY" ]; then
        log "ERROR" "Tavily API Key 未配置"
        return 1
    fi

    # 测试 API
    local test_result=$(curl -s -X POST "$API_BASE/search" \
        -H "Content-Type: application/json" \
        -d "{\"api_key\": \"$TAVILY_API_KEY\", \"query\": \"test\", \"max_results\": 1}" \
        --max-time "$TIMEOUT" 2>&1 || echo "")

    if echo "$test_result" | jq -e '.answer' > /dev/null 2>&1; then
        log "INFO" "Tavily 测试成功"
        return 0
    else
        log "ERROR" "Tavily API 测试失败"
        return 1
    fi
}

# 测试 Twitter API
test_twitter() {
    log "INFO" "测试 Twitter API 数据源..."

    source "$CONFIG_DIR/twitter.conf"

    # 检查 API Key
    if [ -z "$TWITTER_API_KEY" ]; then
        log "ERROR" "Twitter API Key 未配置"
        return 1
    fi

    # 测试 API（这里只是示例，实际 API 可能需要更多配置）
    log "INFO" "Twitter API 配置已加载"
    log "INFO" "注意：实际 API 测试可能需要额外的认证配置"

    return 0
}

# 测试数据源
test_source() {
    local source=$1

    check_config_exists "$source" || return 1

    case $source in
        searxng)
            test_searxng
            ;;
        tavily)
            test_tavily
            ;;
        twitter)
            test_twitter
            ;;
        *)
            log "ERROR" "未知的数据源: $source"
            return 1
            ;;
    esac
}

# 检查数据源健康状态
check_source() {
    local source=$1

    check_config_exists "$source" || return 1

    log "INFO" "检查 $source 健康状态..."

    case $source in
        searxng)
            source "$CONFIG_DIR/searxng.conf"

            # 检查缓存目录
            if [ ! -d "$CACHE_DIR" ]; then
                log "WARN" "缓存目录不存在: $CACHE_DIR"
            else
                local cache_size=$(du -sh "$CACHE_DIR" 2>/dev/null | cut -f1)
                log "INFO" "缓存大小: $cache_size"
            fi

            # 检查日志目录
            if [ ! -d "$LOG_DIR" ]; then
                log "WARN" "日志目录不存在: $LOG_DIR"
            else
                local log_count=$(find "$LOG_DIR" -type f 2>/dev/null | wc -l)
                log "INFO" "日志文件数量: $log_count"
            fi

            test_searxng
            ;;
        tavily)
            source "$CONFIG_DIR/tavily.conf"
            test_tavily
            ;;
        twitter)
            source "$CONFIG_DIR/twitter.conf"
            test_twitter
            ;;
        *)
            log "ERROR" "未知的数据源: $source"
            return 1
            ;;
    esac
}

# 列出所有数据源
list_sources() {
    log "INFO" "可用的数据源:"

    for config_file in "$CONFIG_DIR"/*.conf; do
        if [ -f "$config_file" ]; then
            local source_name=$(basename "$config_file" .conf)
            echo "  - $source_name"
        fi
    done
}

# 清理缓存
clean_cache() {
    local source=$1

    check_config_exists "$source" || return 1

    source "$CONFIG_DIR/${source}.conf"

    if [ -n "$CACHE_DIR" ] && [ -d "$CACHE_DIR" ]; then
        log "INFO" "清理 $source 缓存: $CACHE_DIR"
        rm -rf "$CACHE_DIR"/*
        log "INFO" "缓存清理完成"
    else
        log "WARN" "缓存目录不存在: $CACHE_DIR"
    fi
}

# 清理日志
clean_logs() {
    local source=$1

    check_config_exists "$source" || return 1

    source "$CONFIG_DIR/${source}.conf"

    if [ -n "$LOG_DIR" ] && [ -d "$LOG_DIR" ]; then
        log "INFO" "清理 $source 日志: $LOG_DIR"
        rm -f "$LOG_DIR"/*.log
        log "INFO" "日志清理完成"
    else
        log "WARN" "日志目录不存在: $LOG_DIR"
    fi
}

# 显示配置
show_config() {
    local source=$1

    check_config_exists "$source" || return 1

    echo "=== $source 配置 ==="
    load_config "$source"
}

# 主函数
main() {
    local command=$1
    shift || true

    case $command in
        help|--help|-h)
            show_help
            ;;
        test)
            test_source "$@"
            ;;
        check)
            check_source "$@"
            ;;
        list)
            list_sources
            ;;
        load)
            load_config "$@"
            ;;
        config)
            show_config "$@"
            ;;
        clean-cache)
            clean_cache "$@"
            ;;
        clean-logs)
            clean_logs "$@"
            ;;
        *)
            log "ERROR" "未知命令: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
