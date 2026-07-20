#!/bin/bash
# AI Content Creator 演示脚本
# 通过串联多个百度千帆技能实现内容创作

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 打印标题
print_header() {
    echo ""
    echo -e "${PURPLE}========================================${NC}"
    echo -e "${BLUE}      AI Content Creator 演示${NC}"
    echo -e "${PURPLE}========================================${NC}"
    echo ""
}

# 打印菜单
print_menu() {
    echo -e "${GREEN}AI Content Creator - 技能串联演示${NC}"
    echo ""
    echo "通过串联多个百度千帆技能实现内容创作："
    echo ""
    echo -e "${YELLOW}可用技能：${NC}"
    echo "  1. AI PPT 生成 - 创建演示文稿"
    echo "  2. AI 绘本生成 - 创建配图绘本"
    echo ""
    echo -e "${YELLOW}选择内容类型：${NC}"
    echo "  1) 生成 PPT"
    echo "  2) 生成绘本"
    echo "  3) 批量生成（PPT + 绘本）"
    echo "  4) 查看技能详情"
    echo "  5) 退出"
    echo ""
}

# 演示 PPT 生成
demo_ppt() {
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${GREEN}演示：AI PPT 生成${NC}"
    echo -e "${BLUE}----------------------------------------${NC}"
    echo ""
    echo -e "${YELLOW}技能：${NC}ai-ppt-generate"
    echo -e "${YELLOW}功能：${NC}根据主题自动生成 PPT 演示文稿"
    echo ""
    echo -e "${YELLOW}使用方法：${NC}"
    echo ""
    echo "方法 1: 通过 OpenClaw 直接调用"
    echo "  $ openclaw -m ai-ppt-generate"
    echo ""
    echo "方法 2: 在对话中直接使用"
    echo "  请帮我生成一个关于 'AI 技术发展' 的 PPT"
    echo ""
    echo -e "${YELLOW}示例输入：${NC}"
    echo "  主题：AI 技术发展趋势"
    echo "  页数：10 页"
    echo "  风格：简洁专业"
    echo ""
    echo -e "${GREEN}✓ PPT 生成技能已准备就绪！${NC}"
    echo ""
    read -p "按回车继续..." dummy
}

# 演示绘本生成
demo_picture_book() {
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${GREEN}演示：AI 绘本生成${NC}"
    echo -e "${BLUE}----------------------------------------${NC}"
    echo ""
    echo -e "${YELLOW}技能：${NC}ai-picture-book"
    echo -e "${YELLOW}功能：${NC}根据故事主题自动生成配图绘本"
    echo ""
    echo -e "${YELLOW}使用方法：${NC}"
    echo ""
    echo "方法 1: 通过 OpenClaw 直接调用"
    echo "  $ openclaw -m ai-picture-book"
    echo ""
    echo "方法 2: 在对话中直接使用"
    echo "  请帮我生成一个关于 '小兔子探险' 的绘本"
    echo ""
    echo -e "${YELLOW}示例输入：${NC}"
    echo "  故事：小兔子的第一次冒险"
    echo "  风格：温馨可爱"
    echo "  页数：8 页"
    echo ""
    echo -e "${GREEN}✓ 绘本生成技能已准备就绪！${NC}"
    echo ""
    read -p "按回车继续..." dummy
}

# 演示批量生成
demo_batch() {
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${GREEN}演示：批量生成工作流${NC}"
    echo -e "${BLUE}----------------------------------------${NC}"
    echo ""
    echo -e "${YELLOW}工作流说明：${NC}"
    echo "通过串联多个技能，实现批量内容创作"
    echo ""
    echo "步骤 1: 生成 PPT"
    echo "  技能：ai-ppt-generate"
    echo "  主题：产品发布会演示"
    echo ""
    echo "步骤 2: 生成绘本"
    echo "  技能：ai-picture-book"
    echo "  主题：产品故事绘本"
    echo ""
    echo -e "${YELLOW}工作流代码示例：${NC}"
    cat << 'WORKFLOW'
# ai-content-creation-workflow.sh
#!/bin/bash

echo "开始 AI 内容创作工作流..."

# 步骤 1: 生成 PPT
echo "步骤 1: 生成 PPT..."
openclaw -m ai-ppt-generate "产品发布会演示"

# 步骤 2: 生成绘本
echo "步骤 2: 生成绘本..."
openclaw -m ai-picture-book "产品故事绘本"

echo "工作流完成！"
WORKFLOW
    echo ""
    echo -e "${GREEN}✓ 工作流演示完成！${NC}"
    echo ""
    read -p "按回车继续..." dummy
}

# 显示技能详情
show_skills() {
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${GREEN}技能详情${NC}"
    echo -e "${BLUE}----------------------------------------${NC}"
    echo ""
    
    echo -e "${YELLOW}技能 1: AI PPT 生成${NC}"
    echo "  名称: ai-ppt-generate"
    echo "  功能: 自动生成演示文稿"
    echo "  用途: 商务汇报、技术分享、产品发布"
    echo "  版本: v1.0.0"
    echo "  来源: 百度千帆"
    echo ""
    
    echo -e "${YELLOW}技能 2: AI 绘本生成${NC}"
    echo "  名称: ai-picture-book"
    echo "  功能: 自动生成配图绘本"
    echo "  用途: 儿童绘本、故事书、插画"
    echo "  版本: v1.0.5"
    echo "  来源: 百度千帆"
    echo ""
    
    echo -e "${GREEN}✓ 已安装 2 个百度千帆技能${NC}"
    echo ""
    read -p "按回车继续..." dummy
}

# 主循环
main() {
    while true; do
        clear
        print_header
        print_menu
        read -p "请选择 (1-5): " choice
        
        case $choice in
            1)
                clear
                print_header
                demo_ppt
                ;;
            2)
                clear
                print_header
                demo_picture_book
                ;;
            3)
                clear
                print_header
                demo_batch
                ;;
            4)
                clear
                print_header
                show_skills
                ;;
            5)
                echo ""
                echo -e "${GREEN}感谢使用 AI Content Creator！${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo ""
                echo -e "${RED}无效选择，请重试...${NC}"
                echo ""
                sleep 2
                ;;
        esac
    done
}

# 启动
main
