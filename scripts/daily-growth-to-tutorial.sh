#!/bin/bash

# Daily Growth to Tutorial Generator
# Converts daily growth records into structured tutorials

set -e

# ============================================
# Configuration
# ============================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_DIR="/root/clawd/memory"
TUTORIALS_DIR="/root/clawd/tutorials/daily-growth"
LOG_DIR="/root/clawd/logs/daily-growth"
LOG_FILE="$LOG_DIR/daily-growth-$(date +%Y%m%d-%H%M%S).log"
INDEX_FILE="/root/clawd/tutorials/daily-growth-index.md"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

# Create directories if not exists
mkdir -p "$TUTORIALS_DIR"
mkdir -p "$LOG_DIR"
mkdir -p "$(dirname "$INDEX_FILE")"

# ============================================
# Helper Functions
# ============================================

log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# ============================================
# Extract Key Growth Points from Memory
# ============================================

extract_key_growth() {
    local memory_file="$1"
    local growth_points=()
    
    log "INFO" "Reading memory file: $memory_file"
    
    # Read file line by line
    local in_section=0
    local section_name=""
    local section_content=""
    
    while IFS= read -r line; do
        # Check for major sections (## time - title)
        if [[ "$line" =~ ^##[[:space:]]+[0-9]+:[0-9]+-[[:alpha:]]+ ]]; then
            # Save previous section if valid
            if [ -n "$section_name" ] && [ ${#section_content} -gt 50 ]; then
                growth_points+=("$section_name: $section_content")
            fi
            
            # Start new section
            section_name=$(echo "$line" | sed 's/^##[[:space:]]*//')
            section_content=""
            in_section=1
        elif [ $in_section -eq 1 ]; then
            # Collect section content (limit to 300 chars)
            if [ ${#section_content} -lt 300 ]; then
                section_content+="$line "
            fi
        fi
    done < "$memory_file"
    
    # Don't forget last section
    if [ -n "$section_name" ] && [ ${#section_content} -gt 50 ]; then
        growth_points+=("$section_name: $section_content")
    fi
    
    log "INFO" "Found ${#growth_points[@]} key growth points"
    echo "${growth_points[@]}"
}

# ============================================
# Categorize Growth Point
# ============================================

categorize_growth() {
    local growth_point="$1"
    
    # Keywords for each category
    if [[ "$growth_point" =~ (修复|解决|bug|错误|失败|调试|JSON|Bash|Python|脚本|代码) ]]; then
        echo "技术成长"
    elif [[ "$growth_point" =~ (项目|用户|需求|反馈|沟通|更新|部署|主页) ]]; then
        echo "项目管理"
    elif [[ "$growth_point" =~ (技能|学习|最佳实践|经验教训|成长|健壮|诊断) ]]; then
        echo "最佳实践"
    elif [[ "$growth_point" =~ (创建|开发|设计|实现|自动化) ]]; then
        echo "开发经验"
    elif [[ "$growth_point" =~ (监控|定时任务|Docker|系统) ]]; then
        echo "系统运维"
    else
        echo "其他"
    fi
}

# ============================================
# Generate Tutorial from Growth Point
# ============================================

generate_tutorial() {
    local growth_point="$1"
    local date=$(date +%Y-%m-%d)
    local category=$(categorize_growth "$growth_point")
    local safe_name=$(echo "$category" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
    local filename="${date}-${safe_name}.md"
    
    # Create tutorial content
    local tutorial_content="# [$date] $category\n\n"
    tutorial_content+="## 📋 成长主题\n\n$growth_point\n\n"
    tutorial_content+="## 📅 日期\n\n$date\n\n"
    tutorial_content+="## 🏷️ 分类\n\n$category\n\n"
    
    # Add sections based on content analysis
    tutorial_content+="## 📚 教程内容\n\n"
    
    # Context section
    tutorial_content+="### 背景\n\n"
    tutorial_content+="这个成长点来自日常工作和问题解决过程。\n\n"
    
    # Analysis section
    tutorial_content+="### 分析\n\n"
    tutorial_content+="通过这个经历，我们学到了以下关键点：\n\n"
    
    # Extract keywords
    if [[ "$growth_point" =~ (修复|解决) ]]; then
        tutorial_content+="- 问题诊断能力\n"
        tutorial_content+="- 调试技巧和方法\n"
        tutorial_content+="- 解决方案验证\n"
    elif [[ "$growth_point" =~ (项目|用户) ]]; then
        tutorial_content+="- 项目管理方法\n"
        tutorial_content+="- 用户需求理解\n"
        tutorial_content+="- 反馈处理技巧\n"
    elif [[ "$growth_point" =~ (技能|学习) ]]; then
        tutorial_content+="- 新技能学习\n"
        tutorial_content+="- 经验总结\n"
        tutorial_content+="- 最佳实践应用\n"
    elif [[ "$growth_point" =~ (监控|定时任务) ]]; then
        tutorial_content+="- 系统监控\n"
        tutorial_content+="- 自动化脚本\n"
        tutorial_content+="- Cron 任务配置\n"
    fi
    
    tutorial_content+="\n## 🔑 关键步骤\n\n"
    tutorial_content+="1. 识别问题或需求\n"
    tutorial_content+="2. 分析和诊断\n"
    tutorial_content+="3. 尝试和验证解决方案\n"
    tutorial_content+="4. 总结和记录经验\n"
    
    tutorial_content+="## 💡 经验教训\n\n"
    tutorial_content+="从这次经历中学到的关键经验：\n\n"
    tutorial_content+="- 快速定位问题的重要性\n"
    tutorial_content+="- 分步验证的有效性\n"
    tutorial_content+="- 保持清晰的记录和文档\n"
    
    tutorial_content+="## 🔗 相关资源\n\n"
    tutorial_content+="- **技能**: tutorial-engineer, monitoring-expert\n"
    tutorial_content+="- **相关文档**: /root/clawd/docs/\n"
    tutorial_content+="- **系统记忆**: /root/clawd/memory/\n"
    tutorial_content+="- **工具**: Bash, Python, Docker, Cron\n"
    
    # Echo filename for index update
    echo "$filename"
}

# ============================================
# Update Tutorial Index
# ============================================

update_index() {
    local title="$1"
    local filename="$2"
    local date=$(date +%Y-%m-%d)
    
    # Create index header if not exists
    if [ ! -f "$INDEX_FILE" ]; then
        echo "# 每日成长教程索引\n\n" > "$INDEX_FILE"
        echo "> 自动生成的每日成长教程索引\n\n" >> "$INDEX_FILE"
        echo "| 日期 | 分类 | 主题 | 教程 |\n" >> "$INDEX_FILE"
        echo "|------|------|------|------|\n" >> "$INDEX_FILE"
    fi
    
    # Add entry
    local category=$(categorize_growth "$title")
    local index_entry="| $date | $category | $title | [$filename](daily-growth/$filename) |\n"
    echo -e "$index_entry" >> "$INDEX_FILE"
    
    log "INFO" "Updated index with: $title"
}

# ============================================
# Main Execution
# ============================================

main() {
    log "INFO" "Starting daily growth to tutorial generation"
    
    # Check if yesterday's memory exists
    local yesterday_memory="$MEMORY_DIR/$YESTERDAY.md"
    
    if [ ! -f "$yesterday_memory" ]; then
        log "WARN" "Yesterday's memory not found: $yesterday_memory"
        
        # Try today's memory instead
        local today_memory="$MEMORY_DIR/$TODAY.md"
        
        if [ -f "$today_memory" ]; then
            yesterday_memory="$today_memory"
            log "INFO" "Using today's memory instead"
        else
            log "ERROR" "No memory file found for $TODAY or $YESTERDAY"
            return 1
        fi
    fi
    
    # Extract key growth points
    log "INFO" "Extracting key growth points from memory"
    local growth_points=($(extract_key_growth "$yesterday_memory"))
    
    if [ ${#growth_points[@]} -eq 0 ]; then
        log "WARN" "No growth points found in memory"
        return 0
    fi
    
    log "INFO" "Found ${#growth_points[@]} growth points"
    
    # Generate tutorial for each growth point (limit to top 5 to avoid noise)
    local tutorial_count=0
    local max_tutorials=5
    
    for point in "${growth_points[@]}"; do
        if [ $tutorial_count -ge $max_tutorials ]; then
            log "INFO" "Reached max tutorials limit ($max_tutorials)"
            break
        fi
        
        local filename=$(generate_tutorial "$point")
        
        # Save tutorial
        local tutorial_file="$TUTORIALS_DIR/$filename"
        
        # Need to regenerate content to save
        local content=$(generate_tutorial "$point")
        # Remove filename line (first line) and save
        echo "$content" | tail -n +2 > "$tutorial_file"
        
        # Update index
        update_index "$point" "$filename"
        
        tutorial_count=$((tutorial_count + 1))
        log "INFO" "Generated tutorial: $filename"
    done
    
    log "INFO" "Generated $tutorial_count tutorials"
    
    # Summary
    local summary="📚 **Daily Growth Tutorial Generation Summary**\n\n"
    summary+="**Date**: $date\n\n"
    summary+="**Source Memory**: $yesterday_memory\n\n"
    summary+="**Growth Points Found**: ${#growth_points[@]}\n"
    summary+="**Tutorials Generated**: $tutorial_count\n\n"
    summary+="**Tutorial Directory**: $TUTORIALS_DIR\n"
    summary+="**Index File**: $INDEX_FILE\n\n"
    
    summary+="**Next Steps**:\n"
    summary+="1. Review generated tutorials\n"
    summary+="2. Organize by category\n"
    summary+="3. Create curated collections\n"
    
    summary+="**Tutorial Categories**:\n"
    summary+="- 技术成长\n"
    summary+="- 项目管理\n"
    summary+="- 最佳实践\n"
    summary+="- 系统运维\n"
    summary+="- 开发经验\n"
    
    log "INFO" "Tutorial generation completed"
    echo -e "$summary"
}

# Run main function
main
