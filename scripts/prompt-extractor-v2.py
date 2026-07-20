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
