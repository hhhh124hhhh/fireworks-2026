#!/bin/bash
# Intel Officer - 独立启动脚本

WORKSPACE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🚀 启动 Intel Officer (独立工作区)"
echo "📁 工作目录: $WORKSPACE_DIR"
echo ""

cd "$WORKSPACE_DIR"

# 检查 openclaw 是否可用
if ! command -v openclaw &> /dev/null; then
    echo "❌ openclaw 命令未找到"
    exit 1
fi

# 检查配置
if [ ! -f ".openclaw/workspace-state.json" ]; then
    echo "⚠️  未检测到 OpenClaw 配置，首次设置..."
    openclaw configure
fi

echo "✅ 配置检查通过"
echo ""
echo "📋 启动选项:"
echo "  1) openclaw tui (交互模式)"
echo "  2) openclaw run --headless (无头模式)"
echo "  3) 仅检查状态"
echo ""

read -p "请选择 [1-3]: " choice

case $choice in
    1)
        exec openclaw tui
        ;;
    2)
        exec openclaw run --headless
        ;;
    3)
        openclaw status
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac
