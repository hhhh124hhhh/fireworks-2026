#!/bin/bash
# 使用 Twitter API 收集 AI 提示词

set -e

# 配置
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M)
OUTPUT_FILE="/root/clawd/data/prompts/twitter-prompts.jsonl"

# Twitter API Key (从环境变量加载)
export TWITTER_API_KEY="${TWITTER_API_KEY:-new1_1f191206d7234ac883f47640b933792a}"

# 搜索查询（中英文）
QUERIES=(
    # 英文查询
    "AI prompt engineering"
    "ChatGPT prompts"
    "Claude prompts"
    "midjourney prompts"
    "AI art prompts"
    "prompt engineering tips"
    "best AI prompts"
    "prompt templates"
    # 中文查询
    "AI 提示词"
    "ChatGPT 指令"
    "AI 绘画提示词"
    "提示词工程"
)

# 临时文件
TMP_DIR="/tmp/twitter-prompt-collect-${DATE}-${TIME}"
mkdir -p "$TMP_DIR"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 bird CLI 是否安装
if ! command -v bird &> /dev/null; then
    log_error "bird CLI 未安装"
    log_info "请运行: npm install -g @sugarcube/cli"
    exit 1
fi

log "=========================================="
log "Twitter AI 提示词收集"
log "=========================================="

# 统计
TOTAL_TWEETS=0
TOTAL_PROMPTS=0

# 确保 Python 可用
if ! command -v python3 &> /dev/null; then
    log_error "python3 未安装"
    exit 1
fi

# 创建 Python 脚本来处理数据
cat > "$TMP_DIR/process-tweets.py" << 'PYTHON_SCRIPT'
#!/usr/bin/env python3
import json
import re
from datetime import datetime
import sys

def extract_prompts_from_tweet(text):
    """从推文中提取可能的提示词"""
    prompts = []

    # 查找代码块
    code_blocks = re.findall(r'```(?:python|javascript|json)?\n(.*?)```', text, re.DOTALL)
    for block in code_blocks:
        block = block.strip()
        if len(block) > 20:
            prompts.append(block)

    # 查找引用文本
    quoted = re.findall(r'"([^"]{30,300})"', text)
    for quote in quoted:
        if any(word in quote.lower() for word in ['prompt', 'act as', 'please', '帮我', '扮演']):
            prompts.append(quote)

    # 查找以冒号开头的指令
    instructions = re.findall(r'([A-Z][^.!?]{20,150})', text)
    for instr in instructions[:2]:
        prompts.append(instr)

    return list(set(prompts))[:3]  # 最多返回 3 个

def process_tweet_data(raw_data, query):
    """处理原始推文数据"""
    try:
        data = json.loads(raw_data)

        if isinstance(data, dict):
            # 单个推文
            data = [data]
        elif isinstance(data, list):
            pass  # 已经是列表
        else:
            return []

        processed = []

        for item in data:
            # 尝试不同的数据结构
            if isinstance(item, dict):
                tweet = item.get('data', item) if 'data' in item else item

                # 获取推文内容
                text = ""
                if 'text' in tweet:
                    text = tweet['text']
                elif 'full_text' in tweet:
                    text = tweet['full_text']
                elif 'body' in tweet:
                    text = tweet['body']

                if not text:
                    continue

                # 提取提示词
                prompts = extract_prompts_from_tweet(text)

                author_info = tweet.get('user', tweet.get('author', {}))
                author_name = author_info.get('name', author_info.get('username', 'Unknown'))
                author_handle = author_info.get('screen_name', author_info.get('username', ''))

                # 获取 URL
                tweet_id = tweet.get('id', tweet.get('id_str', ''))
                tweet_url = f"https://twitter.com/{author_handle}/status/{tweet_id}" if tweet_id else ""

                processed.append({
                    "timestamp": datetime.now().isoformat(),
                    "source": "twitter",
                    "search_query": query,
                    "tweet_id": tweet_id,
                    "tweet_url": tweet_url,
                    "author_name": author_name,
                    "author_handle": author_handle,
                    "text": text[:500],  # 限制长度
                    "prompts_found": len(prompts),
                    "prompts": prompts,
                    "likes": tweet.get('favorite_count', 0),
                    "retweets": tweet.get('retweet_count', 0),
                    "replies": tweet.get('reply_count', 0)
                })

        return processed

    except Exception as e:
        print(f"Error processing data: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: process-tweets.py <query> <raw_data_file>")
        sys.exit(1)

    query = sys.argv[1]
    data_file = sys.argv[2]

    with open(data_file, 'r') as f:
        raw_data = f.read()

    processed = process_tweet_data(raw_data, query)

    for item in processed:
        print(json.dumps(item, ensure_ascii=False))
PYTHON_SCRIPT

chmod +x "$TMP_DIR/process-tweets.py"

# 对每个查询进行搜索
log ""
log "开始搜索 Twitter..."
log ""

QUERY_INDEX=0
for query in "${QUERIES[@]}"; do
    QUERY_INDEX=$((QUERY_INDEX + 1))
    log "[$QUERY_INDEX/${#QUERIES[@]}] 搜索: $query"

    # 使用 bird CLI 搜索
    SEARCH_FILE="$TMP_DIR/search-${QUERY_INDEX}.json"

    if bird search -c 10 -f json "$query" > "$SEARCH_FILE" 2>&1; then
        log_info "  ✅ 搜索成功"

        # 处理数据
        PROMPT_COUNT=$(python3 "$TMP_DIR/process-tweets.py" "$query" "$SEARCH_FILE" | tee -a "$TMP_DIR/processed.jsonl" | wc -l)

        TOTAL_TWEETS=$((TOTAL_TWEETS + PROMPT_COUNT))

        if [ "$PROMPT_COUNT" -gt 0 ]; then
            log_info "  📝 处理了 $PROMPT_COUNT 条推文"
        fi
    else
        log_warn "  ⚠️  搜索失败或无结果"
    fi

    sleep 1
done

log ""
log "=========================================="
log "合并数据..."
log "=========================================="

# 读取现有数据
if [ -f "$OUTPUT_FILE" ]; then
    cp "$OUTPUT_FILE" "$TMP_DIR/existing.jsonl"
else
    touch "$TMP_DIR/existing.jsonl"
fi

# 合并所有处理的数据
cat "$TMP_DIR/processed.jsonl" "$TMP_DIR/existing.jsonl" | sort -u > "$OUTPUT_FILE"

# 统计最终结果
FINAL_COUNT=$(wc -l < "$OUTPUT_FILE")
NEW_COUNT=$(wc -l < "$TMP_DIR/processed.jsonl")

# 计算提取的提示词总数
TOTAL_PROMPTS=$(python3 -c "
import json
count = 0
with open('$OUTPUT_FILE', 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            count += data.get('prompts_found', 0)
        except:
            pass
print(count)
" 2>/dev/null || echo "0")

log ""
log "=========================================="
log "✅ 收集完成！"
log "=========================================="
log ""
log "📊 统计:"
log "  • 处理的推文: $TOTAL_TWEETS 条"
log "  • 新增数据: $NEW_COUNT 条"
log "  • 总数据量: $FINAL_COUNT 条"
log "  • 提取的提示词: $TOTAL_PROMPTS 个"
log ""
log "📁 文件: $OUTPUT_FILE"

# 清理临时文件
# rm -rf "$TMP_DIR"

exit 0
