#!/bin/bash
# 修复 SearXNG - 禁用 DuckDuckGo 引擎

set -e

echo "========================================="
echo "🔧 修复 SearXNG 配置"
echo "========================================="

# 检查 Docker 容器
CONTAINER_ID=$(docker ps -q -f name=searxng)

if [ -z "$CONTAINER_ID" ]; then
    echo "❌ SearXNG 容器未运行"
    exit 1
fi

echo "✅ 找到 SearXNG 容器: $CONTAINER_ID"

# 直接使用 Python 修改配置
echo "🔧 禁用 DuckDuckGo 引擎..."

docker exec searxng python3 << 'PYEOF'
import yaml

# 读取配置
with open('/etc/searxng/settings.yml', 'r') as f:
    config = yaml.safe_load(f)

# 禁用所有 DuckDuckGo 引擎
disabled_count = 0
for engine in config['engines']:
    name = engine.get('name', '')
    if name and 'duckduckgo' in name.lower():
        engine['disabled'] = True
        disabled_count += 1

# 写回配置
with open('/etc/searxng/settings.yml', 'w') as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

print(f'✅ 已禁用 {disabled_count} 个 DuckDuckGo 引擎')
PYEOF

# 重启 SearXNG
echo "🔄 重启 SearXNG..."
docker restart searxng

# 等待启动
echo "⏳ 等待 SearXNG 启动..."
sleep 10

# 测试搜索
echo "🧪 测试搜索..."
for i in {1..3}; do
    TEST_RESULT=$(curl -s --max-time 10 "http://localhost:8080/search?format=json&q=test" 2>&1)

    if echo "$TEST_RESULT" | grep -q '"results"'; then
        RESULT_COUNT=$(echo "$TEST_RESULT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('results', [])))" 2>/dev/null || echo "0")
        echo "✅ SearXNG 修复成功！找到 $RESULT_COUNT 个结果"
        echo ""
        echo "========================================="
        echo "✅ SearXNG 修复完成"
        echo "========================================="
        echo ""
        echo "下一步：运行优化版的提示词收集"
        echo "  python3 /root/clawd/scripts/collect_prompts_optimized.py"
        exit 0
    fi

    echo "⏳ 第 $i 次尝试失败，等待后重试..."
    sleep 5
done

echo "❌ SearXNG 仍有问题"
echo "📋 查看日志："
echo "  docker logs searxng --tail 50"
exit 1
