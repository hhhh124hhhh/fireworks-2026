#!/bin/bash

# 下载绘本视频脚本

# 静态绘本
STATIC_URL="http://image0.bj.bcebos.com/picture_book/2026-02-10/ba3636c0-0bbe-4489-b7ef-13089c7682d5.mp4"
STATIC_FILE="/root/clawd/downloads/小AI的冒险故事.mp4"

# 动态绘本
DYNAMIC_URL="http://image0.bj.bcebos.com/picture_book/2026-02-10/c05df768-80e6-4b4a-94e5-8d15f342077e.mp4"
DYNAMIC_FILE="/root/clawd/downloads/智能机器人小酷.mp4"

# 创建下载目录
mkdir -p /root/clawd/downloads

echo "开始下载绘本视频..."
echo ""

# 下载静态绘本
echo "下载静态绘本：小AI的冒险故事"
curl -o "$STATIC_FILE" "$STATIC_URL"

if [ $? -eq 0 ]; then
    echo "✅ 静态绘本下载成功"
    ls -lh "$STATIC_FILE"
else
    echo "❌ 静态绘本下载失败"
fi

echo ""

# 下载动态绘本
echo "下载动态绘本：智能机器人小酷"
curl -o "$DYNAMIC_FILE" "$DYNAMIC_URL"

if [ $? -eq 0 ]; then
    echo "✅ 动态绘本下载成功"
    ls -lh "$DYNAMIC_FILE"
else
    echo "❌ 动态绘本下载失败"
fi

echo ""
echo "下载完成！"
echo "文件位置："
echo "  - 静态绘本：$STATIC_FILE"
echo "  - 动态绘本：$DYNAMIC_FILE"
