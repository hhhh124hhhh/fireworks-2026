#!/bin/bash
# 启动 Twitter API Bridge

cd "$(dirname "$0")"

# 激活虚拟环境
source ../venv/bin/activate

echo "================================"
echo "Twitter API Bridge 启动中..."
echo "================================"

# 启动应用
python3 app.py
