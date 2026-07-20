#!/bin/bash
#
# 改进版提示词收集和转换工作流 v2
# 简化版本，避免依赖外部复杂脚本
#

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="/root/clawd/data/prompts"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
OUTPUT_DIR="${DATA_DIR}/workflow-${TIMESTAMP}"

# 创建输出目录
mkdir -p "${OUTPUT_DIR}"

# 日志文件
LOG_FILE="${OUTPUT_DIR}/workflow.log"

# 简单的日志函数
log_info() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1" | tee -a "${LOG_FILE}"
}

log_success() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [SUCCESS] $1" | tee -a "${LOG_FILE}"
}

log_warning() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [WARNING] $1" | tee -a "${LOG_FILE}"
}

log_error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1" | tee -a "${LOG_FILE}"
}

echo "=========================================="
echo "🚀 提示词工作流 v2"
echo "开始时间: $(date)"
echo "=========================================="

log_info "工作流启动"
log_info "输出目录: ${OUTPUT_DIR}"

# 阶段 1: 检查 awesome-chatgpt-prompts 数据源
log_info "阶段 1: 检查数据源..."

AWESOME_PROMPTS_DIR="/root/clawd/data/awesome-chatgpt-prompts"
if [ -d "${AWESOME_PROMPTS_DIR}" ]; then
    PROMPT_COUNT=$(find "${AWESOME_PROMPTS_DIR}" -name "*.md" | wc -l)
    log_success "找到 ${PROMPT_COUNT} 个提示词文件"
else
    log_warning "awesome-chatgpt-prompts 目录不存在，将使用简化数据源"
fi

# 阶段 2: 使用 Python 脚本进行数据提取和转换
log_info "阶段 2: 执行 Python 转换脚本..."

PYTHON_SCRIPT="${SCRIPT_DIR}/prompt-extractor-v2.py"

if [ ! -f "${PYTHON_SCRIPT}" ]; then
    log_warning "Python 脚本不存在: ${PYTHON_SCRIPT}"
    log_info "创建简化版本的提取脚本..."
    
    cat > "${PYTHON_SCRIPT}" << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
简化版提示词提取器 v2
从 awesome-chatgpt-prompts 提取并转换为技能格式
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

def extract_prompts_from_markdown(file_path):
    """从 markdown 文件提取提示词"""
    prompts = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 尝试提取 "Act as" 格式的提示词
        # 匹配 ## Act as XXX 或 ### Act as XXX
        pattern = r'#{2,3}\s+Act as ([^\n]+)\n+([^#]+)'
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        for role, prompt_text in matches:
            prompts.append({
                'role': role.strip(),
                'prompt': prompt_text.strip(),
                'source': str(file_path)
            })
        
        # 如果没有匹配到，尝试其他格式
        if not prompts:
            # 尝试匹配简单的标题格式
            lines = content.split('\n')
            current_role = None
            current_prompt = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('#') and 'Act as' in line:
                    if current_role and current_prompt:
                        prompts.append({
                            'role': current_role,
                            'prompt': '\n'.join(current_prompt).strip(),
                            'source': str(file_path)
                        })
                    current_role = line.replace('#', '').replace('Act as', '').strip()
                    current_prompt = []
                elif current_role is not None:
                    current_prompt.append(line)
            
            # 添加最后一个
            if current_role and current_prompt:
                prompts.append({
                    'role': current_role,
                    'prompt': '\n'.join(current_prompt).strip(),
                    'source': str(file_path)
                })
        
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
    
    return prompts

def convert_to_skill_format(prompts):
    """将提取的提示词转换为技能格式"""
    skills = []
    
    for i, p in enumerate(prompts):
        # 生成技能名称
        role_slug = re.sub(r'[^a-zA-Z0-9]+', '-', p['role'].lower()).strip('-')
        skill_name = f"{role_slug}-assistant"
        
        skill = {
            "name": skill_name,
            "description": f"Act as {p['role']}",
            "version": "1.0.0",
            "author": "awesome-chatgpt-prompts",
            "prompt": p['prompt'],
            "metadata": {
                "source": p['source'],
                "role": p['role'],
                "extracted_at": datetime.now().isoformat(),
                "index": i
            }
        }
        
        skills.append(skill)
    
    return skills

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: prompt-extractor-v2.py <output_dir>", file=sys.stderr)
        sys.exit(1)
    
    output_dir = Path(sys.argv[1])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 数据源目录
    data_dirs = [
        Path("/root/clawd/data/awesome-chatgpt-prompts"),
        Path("/root/clawd/data/prompts"),
    ]
    
    all_prompts = []
    
    print("🔍 扫描数据源...", file=sys.stderr)
    
    for data_dir in data_dirs:
        if not data_dir.exists():
            print(f"  ⚠️  跳过: {data_dir}", file=sys.stderr)
            continue
        
        print(f"  📂 扫描: {data_dir}", file=sys.stderr)
        
        # 查找所有 markdown 文件
        md_files = list(data_dir.rglob("*.md"))
        print(f"     找到 {len(md_files)} 个 markdown 文件", file=sys.stderr)
        
        for md_file in md_files:
            prompts = extract_prompts_from_markdown(md_file)
            all_prompts.extend(prompts)
            if prompts:
                print(f"     ✓ {md_file.name}: {len(prompts)} 个提示词", file=sys.stderr)
    
    print(f"\n📊 提取统计:", file=sys.stderr)
    print(f"   总计: {len(all_prompts)} 个提示词", file=sys.stderr)
    
    # 转换为技能格式
    print(f"\n🔄 转换为技能格式...", file=sys.stderr)
    skills = convert_to_skill_format(all_prompts)
    
    # 保存提取的提示词
    prompts_file = output_dir / "extracted_prompts.json"
    with open(prompts_file, 'w', encoding='utf-8') as f:
        json.dump(all_prompts, f, indent=2, ensure_ascii=False)
    print(f"   ✓ 保存: {prompts_file}", file=sys.stderr)
    
    # 保存转换后的技能
    skills_file = output_dir / "converted_skills.json"
    with open(skills_file, 'w', encoding='utf-8') as f:
        json.dump(skills, f, indent=2, ensure_ascii=False)
    print(f"   ✓ 保存: {skills_file}", file=sys.stderr)
    
    # 生成摘要报告
    report_file = output_dir / "extraction_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("提示词提取和转换报告\n")
        f.write("="*60 + "\n\n")
        f.write(f"执行时间: {datetime.now().isoformat()}\n")
        f.write(f"输出目录: {output_dir}\n\n")
        
        f.write("提取统计:\n")
        f.write(f"  - 原始提示词: {len(all_prompts)}\n")
        f.write(f"  - 转换技能: {len(skills)}\n\n")
        
        f.write("输出文件:\n")
        f.write(f"  - 提取的提示词: {prompts_file}\n")
        f.write(f"  - 转换的技能: {skills_file}\n")
        f.write(f"  - 本报告: {report_file}\n\n")
        
        f.write("="*60 + "\n")
    
    print(f"   ✓ 保存: {report_file}", file=sys.stderr)
    
    print(f"\n✅ 完成!", file=sys.stderr)
    print(f"   输出目录: {output_dir}", file=sys.stderr)
    
    # 输出 JSON 摘要到 stdout
    summary = {
        "status": "success",
        "total_prompts": len(all_prompts),
        "total_skills": len(skills),
        "output_dir": str(output_dir),
        "files": {
            "prompts": str(prompts_file),
            "skills": str(skills_file),
            "report": str(report_file)
        }
    }
    
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
PYTHON_EOF
    
    chmod +x "${PYTHON_SCRIPT}"
    log_success "创建 Python 脚本: ${PYTHON_SCRIPT}"
fi

# 运行 Python 脚本
log_info "运行 Python 提取脚本..."

if python3 "${PYTHON_SCRIPT}" "${OUTPUT_DIR}"; then
    log_success "Python 脚本执行成功"
else
    log_error "Python 脚本执行失败"
    exit 1
fi

# 阶段 3: 质量评估报告
log_info "阶段 3: 生成质量评估报告..."

REPORT_FILE="${OUTPUT_DIR}/quality_report.txt"

cat > "${REPORT_FILE}" << EOF
========================================
提示词质量评估报告
========================================

生成时间: $(date)
工作流版本: v2

----------------------------------------
执行摘要
----------------------------------------

输出目录: ${OUTPUT_DIR}
日志文件: ${LOG_FILE}

----------------------------------------
阶段完成情况
----------------------------------------

✓ 阶段 1: 数据源检查
✓ 阶段 2: Python 提取和转换
✓ 阶段 3: 质量评估报告

----------------------------------------
下一步操作
----------------------------------------

1. 查看提取结果:
   ls -la ${OUTPUT_DIR}

2. 检查转换的技能:
   cat ${OUTPUT_DIR}/converted_skills.json | jq '.[:5]'

3. 手动验证技能质量

4. 发布到 ClawdHub (可选):
   clawdhub publish <skill-file>

========================================
EOF

log_success "质量报告生成完成: ${REPORT_FILE}"

# 最终摘要
echo ""
echo "========================================"
echo "✅ 提示词工作流 v2 完成"
echo "========================================"
echo ""
echo "📁 输出目录: ${OUTPUT_DIR}"
echo "📄 日志文件: ${LOG_FILE}"
echo "📊 质量报告: ${REPORT_FILE}"
echo ""
echo "生成文件:"
ls -lh "${OUTPUT_DIR}"
echo ""
echo "========================================"

log_success "工作流执行完成！"

exit 0
