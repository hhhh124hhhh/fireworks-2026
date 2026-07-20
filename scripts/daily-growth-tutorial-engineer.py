#!/usr/bin/env python3
"""
Daily Growth Tutorial Generator using tutorial-engineer skill
Transforms daily memory into structured tutorials following tutorial-engineer best practices
"""

import os
import re
import json
from datetime import datetime, timedelta
from pathlib import Path

# ============================================
# Configuration
# ============================================

MEMORY_DIR = Path("/root/clawd/memory")
TUTORIALS_DIR = Path("/root/clawd/tutorials/daily-growth")
LOG_DIR = Path("/root/clawd/logs/daily-growth")
INDEX_FILE = Path("/root/clawd/tutorials/daily-growth-index.md")

TODAY = datetime.now().strftime("%Y-%m-%d")
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# Create directories
TUTORIALS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

# ============================================
# Tutorial Engineering Patterns
# ============================================

class TutorialEngine:
    """
    Follows tutorial-engineer best practices:
    - Progressive disclosure
    - Hands-on learning
    - Error anticipation
    - Multiple learning styles
    - Show, don't tell
    """

    def __init__(self):
        self.categories = {
            "技术成长": r"(修复|解决|bug|错误|失败|调试|JSON|Bash|Python|脚本|代码)",
            "项目管理": r"(项目|用户|需求|反馈|沟通|更新|部署|主页)",
            "最佳实践": r"(技能|学习|最佳实践|经验教训|成长|健壮|诊断)",
            "开发经验": r"(创建|开发|设计|实现|自动化)",
            "系统运维": r"(监控|定时任务|Docker|系统)"
        }

    def categorize(self, title):
        """Categorize growth point based on keywords"""
        for category, pattern in self.categories.items():
            if re.search(pattern, title, re.IGNORECASE):
                return category
        return "其他"

    def generate_tutorial(self, title, content, category):
        """
        Generate tutorial following tutorial-engineer structure:
        - What You'll Learn
        - Prerequisites
        - Context/Background
        - Problem Analysis
        - Solution Steps
        - Lessons Learned
        - Resources
        """
        safe_name = re.sub(r'[^\w-]', '_', category.lower())
        filename = f"{TODAY}-{safe_name}.md"

        tutorial = f"""# [{TODAY}] {category}

> 本教程来自日常工作和问题解决过程，按照 tutorial-engineer 最佳实践编写。

---

## 📚 What You'll Learn

完成本教程后，你将能够：

- 理解 {category} 的核心概念
- 应用相关的最佳实践
- 避免常见的错误和陷阱

---

## 🎯 Prerequisites

在开始之前，你应该具备：

- 基础的 {category} 知识
- 熟悉相关工作流程

**预计时间**: 10-15 分钟

---

## 📖 Context & Background

### 问题描述

{title}

### 背景

这个成长点来自日常的工作实践，通过实际问题和挑战总结而来。它反映了在 {category} 领域中的真实经验和学习过程。

---

## 🔍 Problem Analysis

### 问题诊断

通过这次经历，我们识别了以下关键问题：

1. **问题识别**: {title[:50]}...
2. **根本原因**: 通过调试和分析找到了根本原因
3. **影响范围**: 影响了相关的工作流程

### 常见错误

在处理类似问题时，容易犯以下错误：

- ❌ 错误 1：没有充分分析就急于动手
- ❌ 错误 2：忽略了错误日志和调试信息
- ❌ 错误 3：没有记录解决方案和经验

---

## 💡 Solution Steps

### Step 1: 识别问题

**目标**: 准确识别问题的本质

```bash
# 示例：检查日志和错误信息
tail -f /path/to/log
```

**要点**:
- 不要匆忙下结论
- 收集足够的证据
- 记录所有相关错误

### Step 2: 分析根本原因

**目标**: 找到问题的根本原因，而不是症状

**方法**:
- 使用调试工具
- 检查配置文件
- 查看相关文档

### Step 3: 尝试解决方案

**目标**: 提出并验证解决方案

**策略**:
- 从简单到复杂
- 每次只改动一个地方
- 验证每次修改

### Step 4: 验证和记录

**目标**: 确保问题解决，并记录经验

**检查清单**:
- [ ] 问题是否完全解决
- [ ] 是否有副作用
- [ ] 记录了解决步骤
- [ ] 更新了相关文档

---

## 📝 Lessons Learned

### 关键经验

从这次经历中，我们学到了：

1. **快速诊断的重要性**
   - 正确的诊断比快速解决更重要
   - 收集充分的信息是成功的关键

2. **分步验证的有效性**
   - 每次只改动一个地方
   - 验证每次修改的效果
   - 避免多个改动同时进行

3. **保持清晰的记录**
   - 记录问题和解决步骤
   - 更新相关文档
   - 方便未来查阅和分享

### Best Practices

- 🎯 **优先诊断**: 先理解问题，再动手解决
- 📝 **详细记录**: 记录每一步和结果
- ✅ **充分测试**: 验证解决方案的完整性和副作用
- 🔄 **持续改进**: 从每次经历中学习，不断优化

---

## 🔗 Resources

### 相关技能

- **tutorial-engineer**: 创建分步教程和教育内容
- **monitoring-expert**: 系统监控最佳实践
- **project-health**: 项目健康检查

### 相关文档

- **系统文档**: `/root/clawd/docs/`
- **脚本说明**: `/root/clawd/scripts/`
- **项目 README**: `/root/clawd/*/README.md`

### 系统记忆

- **日常记录**: `/root/clawd/memory/YYYY-MM-DD.md`
- **长期记忆**: `/root/clawd/MEMORY.md`

### 工具和资源

- **Bash**: 脚本编程和自动化
- **Python**: 数据处理和分析
- **Docker**: 容器化部署
- **Cron**: 定时任务管理

---

## ✅ Summary

本教程涵盖了 {category} 的核心概念和实践经验。通过：

- ✅ 理解问题和背景
- ✅ 学习分析和诊断方法
- ✅ 掌握解决步骤和最佳实践
- ✅ 记录和应用经验教训

你现在应该能够更好地处理类似的 {category} 问题。

---

## 🚀 Next Steps

1. **实践应用**: 将学到的知识应用到实际工作中
2. **深入学习**: 探索相关技能和文档
3. **分享经验**: 将自己的经验记录和分享

---

**最后更新**: {TODAY}  
**教程版本**: v1.0  
**作者**: Momo
"""

        return tutorial, filename

# ============================================
# Memory Parser
# ============================================

class MemoryParser:
    """Parse daily memory files and extract growth points"""

    def __init__(self):
        self.growth_patterns = [
            r'## \d{1,2}:\d{2} - (.+)',  # Time-based sections
            r'### (.+)',  # Subsections
        ]

    def parse_memory_file(self, memory_path):
        """Parse memory file and extract growth points"""
        if not memory_path.exists():
            return []

        content = memory_path.read_text(encoding='utf-8', errors='ignore')
        growth_points = []

        # Find all major sections (## time - title)
        section_pattern = r'^## (\d{1,2}:\d{2} - .+)'
        sections = re.findall(section_pattern, content, re.MULTILINE)

        # For each section, extract content
        for section_title in sections:
            # Extract content after the section header
            match = re.search(
                r'^## ' + re.escape(section_title) + r'\n(.*?)(?=^## |\Z)',
                content,
                re.MULTILINE | re.DOTALL
            )

            if match:
                content_text = match.group(1)[:500]  # First 500 chars

                # Only include meaningful sections
                if len(content_text) > 50 and not any(
                    keyword in section_title.lower()
                    for keyword in ['heartbeat', '上下文检查', '系统状态', '其他信息']
                ):
                    growth_points.append({
                        'title': section_title,
                        'content': content_text
                    })

        return growth_points

# ============================================
# Index Manager
# ============================================

class IndexManager:
    """Manage tutorial index"""

    def __init__(self):
        if not INDEX_FILE.exists():
            self.create_index()

    def create_index(self):
        """Create new index file"""
        index_content = """# 每日成长教程索引

> 自动生成的每日成长教程索引，遵循 tutorial-engineer 最佳实践。

---

| 日期 | 分类 | 主题 | 教程 |
|------|------|------|------|

"""
        INDEX_FILE.write_text(index_content, encoding='utf-8')

    def add_entry(self, date, category, title, filename):
        """Add entry to index"""
        index_content = INDEX_FILE.read_text(encoding='utf-8')
        entry = f"| {date} | {category} | {title} | [教程](daily-growth/{filename}) |\n"

        # Insert before the last newline
        if index_content.endswith('\n'):
            index_content = index_content.rstrip('\n') + '\n' + entry + '\n'
        else:
            index_content += '\n' + entry

        INDEX_FILE.write_text(index_content, encoding='utf-8')

# ============================================
# Main Execution
# ============================================

def main():
    print(f"📚 Daily Growth Tutorial Generator")
    print(f"📅 Date: {TODAY}")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print()

    # Check memory file
    memory_path = MEMORY_DIR / f"{YESTERDAY}.md"
    if not memory_path.exists():
        memory_path = MEMORY_DIR / f"{TODAY}.md"

    if not memory_path.exists():
        print(f"❌ No memory file found for {YESTERDAY} or {TODAY}")
        return 1

    print(f"📖 Reading memory: {memory_path}")

    # Parse memory
    parser = MemoryParser()
    growth_points = parser.parse_memory_file(memory_path)

    if not growth_points:
        print("⚠️  No growth points found in memory")
        return 0

    print(f"✅ Found {len(growth_points)} growth points")
    print()

    # Generate tutorials
    engine = TutorialEngine()
    index_manager = IndexManager()

    tutorial_count = 0
    max_tutorials = 5  # Limit to top 5 to avoid noise

    for i, point in enumerate(growth_points[:max_tutorials]):
        title = point['title']
        content = point['content']
        category = engine.categorize(title)

        print(f"📝 Generating tutorial {i+1}/{max_tutorials}: {category}")

        tutorial, filename = engine.generate_tutorial(title, content, category)

        # Save tutorial
        tutorial_path = TUTORIALS_DIR / filename
        tutorial_path.write_text(tutorial, encoding='utf-8')

        # Update index
        index_manager.add_entry(TODAY, category, title[:30], filename)

        tutorial_count += 1

    print()
    print("=" * 60)
    print("📊 **Tutorial Generation Summary**")
    print("=" * 60)
    print()
    print(f"**Date**: {TODAY}")
    print(f"**Source Memory**: {memory_path.name}")
    print(f"**Growth Points Found**: {len(growth_points)}")
    print(f"**Tutorials Generated**: {tutorial_count}")
    print()
    print(f"**Tutorial Directory**: {TUTORIALS_DIR}")
    print(f"**Index File**: {INDEX_FILE}")
    print()
    print("✅ Tutorial generation completed successfully!")
    print()

    return 0

if __name__ == "__main__":
    exit(main())
