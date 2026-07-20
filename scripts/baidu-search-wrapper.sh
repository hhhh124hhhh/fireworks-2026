#!/bin/bash
# 百度搜索包装脚本
# 简化百度搜索 API 调用

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查参数
if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage:${NC} bash baidu-search-wrapper.sh \"<query>\""
    echo ""
    echo "Example:"
    echo "  bash baidu-search-wrapper.sh \"AI技术发展趋势2026\""
    exit 1
fi

QUERY="$1"

# 构造 JSON 参数
REQUEST_BODY="{
  \"query\": \"$QUERY\",
  \"resource_type_filter\": [
    {
      \"type\": \"web\",
      \"top_k\": 20
    }
  ],
  \"search_recency_filter\": \"year\"
}"

# 调用百度搜索
echo -e "${BLUE}=== 百度搜索 ===${NC}"
echo -e "${BLUE}查询:${NC} $QUERY"
echo ""

cd /root/clawd/skills/baidu-search/scripts
export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"
python3 search.py "$REQUEST_BODY"
