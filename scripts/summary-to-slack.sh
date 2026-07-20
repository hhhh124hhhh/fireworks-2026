#!/bin/bash

# 摘要推送到 Slack
# 自动推送任务清单、进度总结、明日计划

set -e

# 配置
SLACK_CHANNEL="${SLACK_CHANNEL:-C0ABSK92X4G}"
FEISHU_WEBHOOK="${FEISHU_WEBHOOK:-}"

# 时间
NOW=$(date '+%Y-%m-%d %H:%M:%S')
DATE=$(date '+%Y-%m-%d')
TIME_HOUR=$(date '+%H')

# 输出函数
send_to_slack() {
    local message="$1"
    
    # 直接推送到 Slack（通过环境变量）
    # 注意：这里只是打印，实际推送需要调用 message 工具
    echo "$message"
    
    # 可以在这里添加实际的 Slack API 调用
}

# 推送任务清单
push_task_list() {
    echo "📋 任务清单 ($DATE)"
    echo "推送时间: $NOW"
    echo ""
    
    # 读取今日的记忆文件
    local today_memory="/root/clawd/memory/$DATE.md"
    
    if [ ! -f "$today_memory" ]; then
        echo "❌ 今日记忆文件不存在: $today_memory"
        return 1
    fi
    
    # 提取任务清单部分
    local tasks=$(awk "/^## 任务清单/,/^## / {print}" "$today_memory" | head -n -1)
    
    if [ -z "$tasks" ]; then
        echo "📝 今日暂无任务清单"
        echo ""
        echo "💡 想要添加任务清单，请使用以下格式："
        echo "```"
        echo "## 任务清单"
        echo ""
        echo "### 优先级 1（高）"
        echo "- [ ] 任务 1"
        echo "- [ ] 任务 2"
        echo "```"
        return 0
    fi
    
    # 转换并推送
    echo "$tasks"
}

# 推送进度总结
push_progress_summary() {
    echo "📊 进度总结 ($DATE)"
    echo "推送时间: $NOW"
    echo ""
    
    # 读取今日的记忆文件
    local today_memory="/root/clawd/memory/$DATE.md"
    
    if [ ! -f "$today_memory" ]; then
        echo "❌ 今日记忆文件不存在: $today_memory"
        return 1
    fi
    
    # 提取所有完成的部分
    echo "✅ 已完成任务"
    
    # 查找所有包含 "✅" 或 "完成" 的部分
    awk '/✅|完成|Completed/,/^## |^---$/ {print; if (/^## |^---$/) exit}' "$today_memory" | grep -v "^## \|^---$" | head -20
    
    echo ""
    echo "📂 产出物"
    
    # 查找产出物
    awk '/产出物|Results|Output/,/^## |^---$/ {print; if (/^## |^---$/) exit}' "$today_memory" | grep -v "^## \|^---$" | head -20
    
    echo ""
    echo "⚠️ 遇到的问题"
    
    # 查找问题
    awk '/问题|Issue|Problem/,/^## |^---$/ {print; if (/^## |^---$/) exit}' "$today_memory" | grep -v "^## \|^---$" | head -10
}

# 推送明日计划
push_tomorrow_plan() {
    echo "🎯 明日计划 ($(date -d 'tomorrow' '+%Y-%m-%d'))"
    echo "推送时间: $NOW"
    echo ""
    
    # 读取今日的记忆文件
    local today_memory="/root/clawd/memory/$DATE.md"
    
    if [ ! -f "$today_memory" ]; then
        echo "❌ 今日记忆文件不存在: $today_memory"
        return 1
    fi
    
    # 提取未完成的任务
    echo "📋 待完成任务"
    
    # 查找所有未完成的任务（标记为 "- [ ]" 或 "待处理"）
    grep -E "\- \[ \]|待处理|Pending|To Do" "$today_memory" | head -20
    
    echo ""
    echo "💡 建议优先级"
    
    # 查找优先级标记
    grep -i "优先级|priority" "$today_memory" | head -10
}

# 主逻辑
case "$1" in
    morning)
        # 早上 9:00 推送任务清单
        push_task_list
        ;;
    
    evening)
        # 晚上 18:00 推送进度总结
        push_progress_summary
        ;;
    
    night)
        # 晚上 22:00 推送明日计划
        push_tomorrow_plan
        ;;
    
    all)
        # 推送所有
        echo "========================================"
        push_task_list
        echo ""
        echo "========================================"
        push_progress_summary
        echo ""
        echo "========================================"
        push_tomorrow_plan
        ;;
    
    *)
        echo "用法: bash summary-to-slack.sh [mode]"
        echo ""
        echo "模式:"
        echo "  morning  - 推送任务清单（早上 9:00）"
        echo "  evening  - 推送进度总结（晚上 18:00）"
        echo "  night    - 推送明日计划（晚上 22:00）"
        echo "  all      - 推送所有"
        echo ""
        echo "示例:"
        echo "  bash summary-to-slack.sh morning"
        echo "  bash summary-to-slack.sh all"
        exit 1
        ;;
esac
