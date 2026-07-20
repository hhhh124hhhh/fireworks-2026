#!/bin/bash
# 启动 OpenCV MCP Server

# 激活虚拟环境
source /opt/opencv-mcp-venv/bin/activate

# 启动 MCP server
python3 -m opencv_mcp_server "$@"

deactivate
