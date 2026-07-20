#!/bin/bash

# 私有 Twitter API 服务器 - 一键部署脚本

set -e

echo "🚀 开始部署私有 Twitter API 服务器..."

# 检查系统
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ 此脚本仅支持 Linux 系统"
    exit 1
fi

# 检查是否为 root
if [[ $EUID -ne 0 ]]; then
   echo "❌ 请使用 root 用户运行此脚本"
   exit 1
fi

# 检查 Python 3
echo "📦 检查 Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python 3 未安装，正在安装..."
    apt-get update
    apt-get install -y python3 python3-pip python3-venv
else
    echo "✅ Python 3 已安装: $(python3 --version)"
fi

# 检查 git
if ! command -v git &> /dev/null; then
    echo "⚠️  Git 未安装，正在安装..."
    apt-get install -y git
fi

# 创建虚拟环境
echo "📦 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 安装 uvicorn
pip install uvicorn

# 测试启动
echo "🧪 测试启动服务器..."
timeout 5 python3 -c "
from ntscraper import Nitter
from fastapi import FastAPI
print('✅ 依赖安装成功！')
" || {
    echo "❌ 依赖安装失败"
    exit 1
}

echo ""
echo "✅ 部署完成！"
echo ""
echo "📝 使用方法:"
echo "   1. 启动服务器: ./start.sh"
echo "   2. 测试 API: python3 test_api.py"
echo "   3. 查看文档: http://localhost:8000/docs"
echo ""
echo "🔧 生产环境部署（可选）:"
echo "   1. 安装为 systemd 服务:"
echo "      sudo cp twitter-api.service /etc/systemd/system/"
echo "      sudo systemctl daemon-reload"
echo "      sudo systemctl enable twitter-api"
echo "      sudo systemctl start twitter-api"
echo "   2. 查看服务状态:"
echo "      sudo systemctl status twitter-api"
echo "   3. 查看日志:"
echo "      sudo journalctl -u twitter-api -f"
echo ""
echo "🌐 访问 API:"
echo "   本地: http://localhost:8000"
echo "   外部: http://YOUR_SERVER_IP:8000"
echo ""
echo "⚠️  如果服务器有防火墙，请开放 8000 端口:"
echo "   sudo ufw allow 8000"
echo "   或"
echo "   sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT"
echo ""
