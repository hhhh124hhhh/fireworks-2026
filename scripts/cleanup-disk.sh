#!/bin/bash
# 磁盘清理脚本
# 日期: 2026-02-10

set -e

echo "=== 磁盘清理脚本 ==="
echo "开始时间: $(date)"
echo ""

# 当前磁盘使用情况
echo "=== 当前磁盘使用情况 ==="
df -h /
echo ""

# 检查占用空间最大的目录
echo "=== 占用空间最大的目录 ==="
du -sh /root/clawd/* 2>/dev/null | sort -rh | head -10
echo ""

# 清理建议
echo "=== 清理建议 ==="
echo ""
echo "1. /root/clawd/venv (7.1G)"
echo "   - 包含: nvidia (4.3G), torch (1.7G), triton (639M)"
echo "   - 用途: 深度学习相关的 Python 虚拟环境"
echo "   - 清理风险: 如果有项目使用这个 venv，需要重新安装"
echo "   - 建议: 如果当前不使用深度学习，可以删除"
echo ""
echo "2. /root/clawd/skills/x-prompt-hunter/venv (3.3G)"
echo "   - 用途: x-prompt-hunter 技能的虚拟环境"
echo "   - 清理风险: x-prompt-hunter 可能无法正常工作"
echo "   - 建议: 如果不使用 x-prompt-hunter，可以删除"
echo ""
echo "3. /root/clawd/interactive-demo (104M)"
echo "   - 用途: 交互式演示项目"
echo "   - 清理风险: 可能丢失演示代码"
echo "   - 建议: 如果不再需要，可以删除"
echo ""
echo "4. /root/clawd/ai-prompt-marketplace (104M)"
echo "   - 用途: AI 提示词市场项目"
echo "   - 清理风险: 可能丢失项目代码"
echo "   - 建议: 如果不再需要，可以删除"
echo ""

# 询问用户是否继续
echo "=== 清理选项 ==="
echo ""
echo "A) 清理 /root/clawd/venv (7.1G) - 深度学习虚拟环境"
echo "B) 清理 /root/clawd/skills/x-prompt-hunter/venv (3.3G) - x-prompt-hunter 虚拟环境"
echo "C) 清理 /root/clawd/interactive-demo (104M) - 交互式演示"
echo "D) 清理 /root/clawd/ai-prompt-marketplace (104M) - AI 提示词市场"
echo "E) 清理全部 (10.4G)"
echo "X) 退出"
echo ""
read -p "请选择 (A/B/C/D/E/X): " choice

case $choice in
    [Aa])
        echo "清理 /root/clawd/venv..."
        rm -rf /root/clawd/venv
        echo "完成！已清理 7.1G"
        ;;
    [Bb])
        echo "清理 /root/clawd/skills/x-prompt-hunter/venv..."
        rm -rf /root/clawd/skills/x-prompt-hunter/venv
        echo "完成！已清理 3.3G"
        ;;
    [Cc])
        echo "清理 /root/clawd/interactive-demo..."
        rm -rf /root/clawd/interactive-demo
        echo "完成！已清理 104M"
        ;;
    [Dd])
        echo "清理 /root/clawd/ai-prompt-marketplace..."
        rm -rf /root/clawd/ai-prompt-marketplace
        echo "完成！已清理 104M"
        ;;
    [Ee])
        echo "清理全部..."
        rm -rf /root/clawd/venv
        rm -rf /root/clawd/skills/x-prompt-hunter/venv
        rm -rf /root/clawd/interactive-demo
        rm -rf /root/clawd/ai-prompt-marketplace
        echo "完成！已清理 10.4G"
        ;;
    [Xx])
        echo "退出清理脚本"
        exit 0
        ;;
    *)
        echo "无效的选择: $choice"
        exit 1
        ;;
esac

# 清理后的磁盘使用情况
echo ""
echo "=== 清理后的磁盘使用情况 ==="
df -h /
echo ""

# 清理 Docker 系统
echo "=== 清理 Docker 系统 ==="
docker system prune -f 2>/dev/null || echo "Docker 清理失败或未安装"
echo ""

echo "=== 清理完成 ==="
echo "结束时间: $(date)"
