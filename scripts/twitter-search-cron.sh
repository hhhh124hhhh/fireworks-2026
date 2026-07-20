#!/bin/bash

# Twitter 自动搜索脚本 (Cron 版本）
# 功能：搜索 Twitter AI 提示词并生成报告
# 频率：每 6 小时执行一次（通过 cron）

set -e

# 配置变量
SEARCH_QUERY="#AIPrompts OR #promptengineering OR \"AI prompt engineering\" OR \"ChatGPT prompts\" OR \"Claude prompts\""
MAX_RESULTS=50
REPORT_DIR="/root/clawd/ai-prompt-marketplace/reports"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M)
REPORT_FILE="$REPORT_DIR/twitter-report-${DATE}-${TIME}.json"
SUMMARY_FILE="$REPORT_DIR/twitter-summary-${DATE}-${TIME}.md"
LOG_FILE="$REPORT_DIR/execution.log"

# 创建目录
mkdir -p "$REPORT_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "Starting Twitter search automation"
log "=========================================="

# 加载 Twitter API key
if [ -f ~/.bashrc ]; then
    # 直接获取 API key 而不是 source 整个文件
    # 使用双引号作为分隔符（.bashrc 中使用的是双引号）
    export TWITTER_API_KEY=$(grep "^export TWITTER_API_KEY=" ~/.bashrc | sed 's/export TWITTER_API_KEY="\(.*\)"/\1/')
fi

if [ -z "$TWITTER_API_KEY" ]; then
    log "ERROR: TWITTER_API_KEY not found in environment"
    exit 1
fi

log "Twitter API key loaded"

# 执行搜索
log "Searching Twitter for: $SEARCH_QUERY"
log "Max results: $MAX_RESULTS"

# 使用正确的脚本路径
TWITTER_SCRIPT="/root/clawd/skills/twitter-search-skill/scripts/twitter_search_improved.py"

if [ ! -f "$TWITTER_SCRIPT" ]; then
    log "ERROR: Twitter search script not found: $TWITTER_SCRIPT"
    exit 1
fi

log "Using Twitter search script: $TWITTER_SCRIPT"

# 执行搜索
if python3 "$TWITTER_SCRIPT" \
    "$TWITTER_API_KEY" \
    "$SEARCH_QUERY" \
    --max-results "$MAX_RESULTS" \
    --query-type Top \
    --lang en \
    --min-likes 10 \
    --format json > "$REPORT_FILE" 2>> "$LOG_FILE"; then

    # 检查结果文件是否存在且非空
    if [ -f "$REPORT_FILE" ] && [ -s "$REPORT_FILE" ]; then
        # 提取统计数据
        if command -v jq &> /dev/null; then
            TOTAL_TWEETS=$(jq -r '.total_tweets // 0' "$REPORT_FILE" 2>/dev/null || echo "0")
        else
            TOTAL_TWEETS=$(python3 -c "import json; data=json.load(open('$REPORT_FILE')); print(data.get('total_tweets', 0))" 2>/dev/null || echo "0")
        fi

        log "Search completed successfully: $TOTAL_TWEETS tweets found"

        # 生成 Markdown 摘要
        if [ "$TOTAL_TWEETS" -gt 0 ]; then
            log "Generating markdown summary..."

            DATE="$DATE" TIME="$TIME" python3 <<'PYTHON_SCRIPT'
import json
import sys
import os

try:
    # 从环境变量获取文件名
    date = os.environ.get('DATE', '2026-02-10')
    time = os.environ.get('TIME', '1143')

    report_file = f"/root/clawd/ai-prompt-marketplace/reports/twitter-report-{date}-{time}.json"

    with open(report_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_tweets = data.get('total_tweets', 0)
    tweets = data.get('tweets', [])

    # 生成摘要
    summary = f"""# Twitter 搜索报告

**搜索时间**: {data.get('search_time', 'N/A')}
**查询**: {data.get('query', 'N/A')}
**结果数量**: {total_tweets}

## 统计信息

- 总推文数: {total_tweets}
- 语言: {data.get('language', 'N/A')}
- 查询类型: {data.get('query_type', 'N/A')}

"""

    if total_tweets > 0:
        summary += "## 热门推文\n\n"
        count = 0
        for tweet in tweets[:10]:  # 只显示前 10 条
            count += 1
            summary += f"""
### {count}. {tweet.get('author', 'N/A')}

**发布时间**: {tweet.get('created_at', 'N/A')}
**点赞数**: {tweet.get('like_count', 0)}
**转发数**: {tweet.get('retweet_count', 0)}

**内容**:
> {tweet.get('text', 'N/A')}

---
"""
    else:
        summary += "\n未找到符合条件的推文。\n"

    summary += f"\n\n完整报告: `twitter-report-{date}-{time}.json`\n"

    # 保存摘要
    summary_file = f"/root/clawd/ai-prompt-marketplace/reports/twitter-summary-{date}-{time}.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"Summary generated: {summary_file}")

except FileNotFoundError:
    print("ERROR: Report file not found", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"ERROR: Failed to parse JSON: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Failed to generate summary: {e}", file=sys.stderr)
    sys.exit(1)

PYTHON_SCRIPT

            log "Twitter search automation completed successfully"
        else
            log "No tweets found, skipping summary generation"
        fi
    else
        log "ERROR: Report file is empty"
        exit 1
    fi
else
    log "ERROR: Twitter search failed with exit code $?"
    exit 1
fi

log "=========================================="
log "End of Twitter search automation"
log "=========================================="
