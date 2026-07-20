#!/bin/bash
# GLM-5 接入状态检查脚本

echo "=== GLM-5 接入状态检查 ==="
echo "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 记录位置
LOG_DIR="/root/clawd/memory/glm5-monitor"
LOG_FILE="$LOG_DIR/check-log.txt"

# 创建目录
mkdir -p "$LOG_DIR"

# 检查日志
check_glm5() {
    echo "检查 GLM-5 模型接入状态..." | tee -a "$LOG_FILE"

    # 尝试设置模型
    echo "尝试: openclaw session-status model=zai/glm-5" | tee -a "$LOG_FILE"

    # 记录结果
    echo "---" | tee -a "$LOG_FILE"
}

# 主函数
main() {
    check_glm5

    echo ""
    echo "检查完成。日志已保存到: $LOG_FILE"
    echo ""
}

# 执行
main
