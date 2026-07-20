#!/usr/bin/env python3
"""
评估提示词质量
"""

import json
import os
import re
from datetime import datetime

# 配置
INPUT_DIR = "/root/clawd/data/prompts"
OUTPUT_DIR = "/root/clawd/data/prompts/evaluated"
MIN_QUALITY_SCORE = 60

# 质量评估标准
QUALITY_CRITERIA = {
    "length": {
        "min": 50,
        "max": 2000,
        "weight": 0.2
    },
    "specificity": {
        "keywords": [
            "specific", "detailed", "precise", "clear", "exactly",
            "specifically", "explicitly", "determine", "specify"
        ],
        "weight": 0.2
    },
    "structure": {
        "patterns": [
            r'(act|role|persona):\s*\w+',
            r'(context|background|scenario):',
            r'(task|instruction|action):',
            r'(format|output|result):'
        ],
        "weight": 0.25
    },
    "clarity": {
        "indicators": [
            "step by step",
            "in detail",
            "comprehensive",
            "thorough",
            "systematic"
        ],
        "weight": 0.2
    },
    "creativity": {
        "indicators": [
            "creative", "innovative", "unique", "original",
            "novel", "inspiring", "imaginative"
        ],
        "weight": 0.15
    }
}

def evaluate_length(prompt_text):
    """评估长度"""
    length = len(prompt_text)

    if QUALITY_CRITERIA["length"]["min"] <= length <= QUALITY_CRITERIA["length"]["max"]:
        return 100
    elif length < QUALITY_CRITERIA["length"]["min"]:
        return (length / QUALITY_CRITERIA["length"]["min"]) * 100
    else:
        return max(0, 100 - ((length - QUALITY_CRITERIA["length"]["max"]) / 100) * 10)

def evaluate_specificity(prompt_text):
    """评估具体性"""
    score = 0
    keywords = QUALITY_CRITERIA["specificity"]["keywords"]

    prompt_lower = prompt_text.lower()

    for keyword in keywords:
        if keyword in prompt_lower:
            score += 100 / len(keywords)

    return min(100, score)

def evaluate_structure(prompt_text):
    """评估结构"""
    score = 0
    patterns = QUALITY_CRITERIA["structure"]["patterns"]

    for pattern in patterns:
        if re.search(pattern, prompt_text, re.IGNORECASE):
            score += 100 / len(patterns)

    return min(100, score)

def evaluate_clarity(prompt_text):
    """评估清晰度"""
    score = 0
    indicators = QUALITY_CRITERIA["clarity"]["indicators"]

    prompt_lower = prompt_text.lower()

    for indicator in indicators:
        if indicator in prompt_lower:
            score += 100 / len(indicators)

    return min(100, score)

def evaluate_creativity(prompt_text):
    """评估创意性"""
    score = 0
    indicators = QUALITY_CRITERIA["creativity"]["indicators"]

    prompt_lower = prompt_text.lower()

    for indicator in indicators:
        if indicator in prompt_lower:
            score += 100 / len(indicators)

    return min(100, score)

def calculate_overall_score(prompt_text):
    """计算总体质量分数"""
    length_score = evaluate_length(prompt_text)
    specificity_score = evaluate_specificity(prompt_text)
    structure_score = evaluate_structure(prompt_text)
    clarity_score = evaluate_clarity(prompt_text)
    creativity_score = evaluate_creativity(prompt_text)

    overall_score = (
        length_score * QUALITY_CRITERIA["length"]["weight"] +
        specificity_score * QUALITY_CRITERIA["specificity"]["weight"] +
        structure_score * QUALITY_CRITERIA["structure"]["weight"] +
        clarity_score * QUALITY_CRITERIA["clarity"]["weight"] +
        creativity_score * QUALITY_CRITERIA["creativity"]["weight"]
    )

    return {
        "overall": round(overall_score, 2),
        "length": round(length_score, 2),
        "specificity": round(specificity_score, 2),
        "structure": round(structure_score, 2),
        "clarity": round(clarity_score, 2),
        "creativity": round(creativity_score, 2)
    }

def classify_prompt(prompt_text, score_data):
    """分类提示词类型"""
    length = len(prompt_text)

    if score_data["structure"] > 70:
        return "structured"
    elif length > 500:
        return "detailed"
    elif score_data["creativity"] > 60:
        return "creative"
    elif "image" in prompt_text.lower() or "art" in prompt_text.lower():
        return "image-generation"
    elif "video" in prompt_text.lower():
        return "video-generation"
    elif "code" in prompt_text.lower() or "programming" in prompt_text.lower():
        return "coding"
    else:
        return "general"

def main():
    print("=" * 80)
    print("📊 评估提示词质量")
    print("=" * 80)
    print()

    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 查找输入文件
    input_files = []
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".jsonl") and "prompts" in filename:
            input_files.append(os.path.join(INPUT_DIR, filename))

    if not input_files:
        print("❌ 未找到输入文件")
        print(f"请在 {INPUT_DIR} 中放置 *.jsonl 文件")
        return

    print(f"📁 找到 {len(input_files)} 个输入文件")
    print()

    # 处理每个文件
    all_evaluated = []
    total_evaluated = 0
    high_quality = 0
    medium_quality = 0
    low_quality = 0

    for input_file in input_files:
        print(f"📖 处理: {os.path.basename(input_file)}")

        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    prompt_data = json.loads(line)
                    
                    # 支持多个字段名，按优先级顺序查找
                    prompt_text = (
                        prompt_data.get("prompt") or
                        prompt_data.get("content") or
                        prompt_data.get("full_text") or
                        ""
                    )

                    # 跳过空提示词或太短的提示词
                    if not prompt_text or len(prompt_text.strip()) < 10:
                        continue

                    # 评估质量
                    scores = calculate_overall_score(prompt_text)

                    # 添加评估结果
                    evaluated_data = {
                        **prompt_data,
                        "quality_scores": scores,
                        "quality_category": classify_prompt(prompt_text, scores),
                        "quality_level": "high" if scores["overall"] >= 80 else "medium" if scores["overall"] >= 60 else "low",
                        "evaluated_at": datetime.now().isoformat()
                    }

                    all_evaluated.append(evaluated_data)
                    total_evaluated += 1

                    # 统计
                    if scores["overall"] >= 80:
                        high_quality += 1
                    elif scores["overall"] >= 60:
                        medium_quality += 1
                    else:
                        low_quality += 1

                except Exception as e:
                    print(f"  ⚠️  跳过: {e}")

        print(f"  ✓ 评估完成")

    # 保存评估结果
    print()
    print(f"💾 保存评估结果...")

    output_file = os.path.join(OUTPUT_DIR, f"evaluated-prompts-{datetime.now().strftime('%Y%m%d-%H%M%S')}.jsonl")

    with open(output_file, 'w', encoding='utf-8') as f:
        for evaluated in all_evaluated:
            f.write(json.dumps(evaluated, ensure_ascii=False) + '\n')

    # 生成报告
    report_file = os.path.join(OUTPUT_DIR, f"evaluation-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_evaluated": total_evaluated,
        "quality_distribution": {
            "high": high_quality,
            "medium": medium_quality,
            "low": low_quality
        },
        "average_score": sum(e["quality_scores"]["overall"] for e in all_evaluated) / total_evaluated if total_evaluated > 0 else 0,
        "output_file": output_file
    }

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(report, indent=2, ensure_ascii=False))

    print()
    print("=" * 80)
    print("✅ 评估完成！")
    print("=" * 80)
    print()
    print(f"📊 统计:")
    print(f"  总评估: {total_evaluated} 个")
    print(f"  高质量 (≥80): {high_quality} 个")
    print(f"  中等质量 (60-79): {medium_quality} 个")
    print(f"  低质量 (<60): {low_quality} 个")
    print(f"  平均分数: {report['average_score']:.2f}")
    print()
    print(f"📁 输出文件:")
    print(f"  评估结果: {output_file}")
    print(f"  评估报告: {report_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏸️  用户中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
