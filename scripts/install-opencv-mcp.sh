#!/bin/bash
# 解决 OpenCV MCP 安装问题

echo "=== 解决 OpenCV MCP 安装问题 ==="
echo ""

# 创建虚拟环境
VENV_DIR="/opt/opencv-mcp-venv"

if [ -d "$VENV_DIR" ]; then
    echo "虚拟环境已存在，删除旧的..."
    rm -rf "$VENV_DIR"
fi

echo "创建虚拟环境..."
python3 -m venv "$VENV_DIR"

# 激活虚拟环境并安装
echo "安装 OpenCV MCP Server..."
source "$VENV_DIR/bin/activate"
pip install opencv-mcp-server

# 创建启动脚本
cat > /root/clawd/scripts/start-opencv-mcp.sh << 'EOF'
#!/bin/bash
# 启动 OpenCV MCP Server

# 激活虚拟环境
source /opt/opencv-mcp-venv/bin/activate

# 启动 MCP server
python3 -m opencv_mcp_server "$@"

deactivate
EOF

chmod +x /root/clawd/scripts/start-opencv-mcp.sh

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法："
echo "  启动 MCP server: bash /root/clawd/scripts/start-opencv-mcp.sh"
echo ""
echo "注意："
echo "  - MCP server 需要配置到你的 AI 系统"
echo "  - 虚拟环境位置: /opt/opencv-mcp-venv"
echo ""
echo "=== 完成 ==="
