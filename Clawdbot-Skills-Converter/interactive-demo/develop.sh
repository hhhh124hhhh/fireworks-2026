#!/bin/bash

# 使用 Claude Code 开发交互式演示项目
# 自动化执行各个技能阶段

PROJECT_DIR="/root/clawd/interactive-demo"
LOG_FILE="$PROJECT_DIR/development.log"
ERROR_LOG="$PROJECT_DIR/errors.log"

# 创建日志文件
touch "$LOG_FILE"
touch "$ERROR_LOG"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    echo "[ERROR $(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$ERROR_LOG"
}

log "=== 开始开发交互式演示项目 ==="

# 阶段 1: 需求讨论（brainstorming）
log "阶段 1: 使用 brainstorming 技能讨论需求..."
cd "$PROJECT_DIR"

echo "请使用 brainstorming 技能帮我规划一个交互式演示网页。

项目目标:
- 展示 Ultimate Skills Bundle 的 70+ 技能
- 交互式浏览技能
- 展示技能效果对比
- 包含实际的代码示例
- 现代化 UI 设计

请帮我:
1. 澄清需求
2. 设计页面结构
3. 规划功能模块
4. 选择技术栈
5. 制定实施计划" | claude --non-interactive 2>&1 | tee -a "$LOG_FILE" || error "brainstorming 阶段失败"

if [ $? -eq 0 ]; then
    log "✅ 阶段 1 完成"
else
    error "阶段 1 失败"
    exit 1
fi

# 等待用户确认
read -p "阶段 1 完成，是否继续？(y/n): " continue
if [ "$continue" != "y" ]; then
    log "用户中断执行"
    exit 0
fi

# 阶段 2: 制定计划（writing-plans）
log "阶段 2: 使用 writing-plans 技能制定计划..."

echo "使用 writing-plans 技能，为交互式演示网页创建详细的实施计划。

基于之前的需求讨论，创建:
- 详细的任务分解
- 每个任务的时间估算
- 技术实施细节
- 测试计划
- 部署方案" | claude --non-interactive 2>&1 | tee -a "$LOG_FILE" || error "writing-plans 阶段失败"

if [ $? -eq 0 ]; then
    log "✅ 阶段 2 完成"
else
    error "阶段 2 失败"
    exit 1
fi

# 继续后续阶段...
# (这里简化了，实际需要逐步执行)

log "=== 开发完成 ==="
log "日志文件: $LOG_FILE"
log "错误日志: $ERROR_LOG"
