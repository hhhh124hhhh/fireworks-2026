#!/bin/bash

# Jack Portfolio - Local Server Script
# 快速启动本地服务器预览 Cyberpunk 风格主页

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印欢迎信息
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}           Jack Portfolio - 本地服务器启动器              ${GREEN}║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查 Python 版本
echo -e "${BLUE}[1/4]${NC} 检查 Python 环境..."

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}✓${NC} Python 已安装: ${PYTHON_VERSION}"
else
    echo -e "${YELLOW}⚠${NC}  未找到 Python3，尝试使用 Python..."
    if command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1)
        echo -e "${GREEN}✓${NC} Python 已安装: ${PYTHON_VERSION}"
        PYTHON_CMD="python"
    else
        echo -e "${RED}✗${NC} 错误: 未找到 Python，请先安装 Python"
        exit 1
    fi
fi
PYTHON_CMD="python3"

# 检查文件
echo -e "${BLUE}[2/4]${NC} 检查文件..."

if [ ! -f "index.html" ]; then
    echo -e "${RED}✗${NC} 错误: 未找到 index.html"
    exit 1
fi

if [ ! -f "css/cyberpunk.css" ]; then
    echo -e "${RED}✗${NC} 错误: 未找到 css/cyberpunk.css"
    exit 1
fi

if [ ! -f "js/cyberpunk.js" ]; then
    echo -e "${RED}✗${NC} 错误: 未找到 js/cyberpunk.js"
    exit 1
fi

echo -e "${GREEN}✓${NC} 所有必要文件已找到"

# 选择端口
PORT=8000
while [ true ]; do
    if ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        break
    fi
    PORT=$((PORT + 1))
done

# 启动服务器
echo -e "${BLUE}[3/4]${NC} 启动服务器..."

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓${NC} 服务器已启动！"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}访问地址:${NC} ${YELLOW}http://localhost:$PORT${NC}"
echo -e "${BLUE}访问地址:${NC} ${YELLOW}http://127.0.0.1:$PORT${NC}"
echo ""
echo -e "${BLUE}按 Ctrl+C 停止服务器${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 尝试自动打开浏览器
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "http://localhost:$PORT"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:$PORT" 2>/dev/null || true
    fi
fi

# 启动服务器
cd "$(dirname "$0")"
$PYTHON_CMD -m http.server $PORT
