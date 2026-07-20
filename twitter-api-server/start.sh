#!/bin/bash

echo "🚀 启动私有 Twitter API 服务器..."

# 进入项目目录
cd "$(dirname "$0")"

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3.8+"
    exit 1
fi

# 检查是否需要安装依赖
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境并安装依赖..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "✅ 虚拟环境已存在，激活中..."
    source venv/bin/activate
fi

# 启动服务器
echo "🌐 启动 FastAPI 服务器 (http://0.0.0.0:8000)..."
python3 main.py
