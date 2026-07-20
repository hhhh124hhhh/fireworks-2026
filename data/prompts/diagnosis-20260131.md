# AI 提示词转 Skill 项目 - 执行情况诊断

**日期**: 2026-01-31 15:45
**评估人**: Clawdbot

---

## 📊 当前状态

### 脚本状态
| 脚本 | 状态 | 问题 |
|------|------|------|
| `collect-prompts-via-searxng.py` | ✅ 已创建 | ❌ 提取逻辑存在严重问题 |
| `evaluate-prompts-agent.py` | ✅ 已创建 | ❌ JSON 解析失败 |
| `convert-prompts-to-skills.py` | ✅ 已创建 | - |

### 数据质量（测试运行）
- **收集数量**: 25 条
- **平均分数**: 36.4 / 100
- **质量分布**:
  - 高质量 (≥70): **0%** ❌
  - 中等 (50-69): **12%** ⚠️
  - 低质量 (<50): **88%** ❌

**预期目标**: 高质量 ≥40%，低质量 <10%
**实际结果**: 高质量 0%，低质量 88%

---

## 🔴 核心问题

### 问题 1: 提取逻辑过于宽泛（严重）

**现象**:
- 提取的内容大多是页面标题、导航菜单、课程大纲
- 不是真正的 AI 提示词

**示例（实际提取到的数据）**:
```
"Function Prompt Hub Classification Sentiment Classification"
"Engineering Guide | Prompt Engineering Guide 🚀 Master building AI workflows"
"1. Code readability and maintainability"
"2. Performance optimization"
"- Generate Code Snippet"
"- Generate MySQL Query"
```

**根本原因**:
```python
# 问题代码
list_patterns = [
    r'\d+\.\s+([^.!?]{40,800})',   # 匹配任何编号列表项
    r'[-*]\s+([^.!?]{40,800})',    # 匹配任何无序列表项
]
```

这段代码会匹配**所有**列表项，包括：
- ✅ 真正的提示词示例（极少数）
- ❌ 导航菜单
- ❌ 功能列表
- ❌ 课程章节标题
- ❌ 特性介绍

**影响**:
- 垃圾数据比例高达 **88%**
- 无法提取到真正有用的提示词
- 后续评估和转换都基于错误的数据

---

### 问题 2: Agent 评估脚本失败（严重）

**现象**:
```
JSON 解析失败: Expecting value: line 1 column 1 (char 0)
```

**根本原因**:
`sessions_spawn` 返回的内容不是预期的 JSON 格式，可能是：
- 返回了纯文本确认消息
- 返回格式与脚本期望的不匹配
- 需要特殊处理返回的响应

**影响**:
- 无法使用系统级 Agent 进行语义评估
- 只能依赖基于关键词的规则评分（不准确）
- 质量评估系统完全失效

---

### 问题 3: 来源选择不当（中等）

**现象**:
- 大部分搜索结果来自教程网站、文档网站
- 这些网站的结构不适合用通用正则表达式提取

**不合适的来源**:
- Prompt Engineering Guide（教程网站）
- LearnPrompting（教程网站）
- 文档网站（OpenAI、Midjourney 官网）

**问题**:
- 教程网站的内容是"教你怎么写提示词"，不是"提示词本身"
- 文档网站主要是 API 说明，不是提示词示例
- 用通用规则从这些网站提取，成功率极低

**影响**:
- 浪费大量资源爬取不合适的网站
- 提取成功率低，垃圾数据多

---

## ✅ 部分成功的改进

### 1. 系统架构设计
- 使用 `sessions_spawn` 避免外部 API 依赖（概念正确）
- SearXNG 多源搜索（方向正确）
- 批量处理和自动化流程（设计合理）

### 2. 质量过滤框架
- 多层过滤机制（方向正确）
- 类型分类系统（思路正确）
- 质量评分框架（结构合理）

### 3. 基础设施
- SearXNG 实例可访问
- 脚本文件已创建
- 数据目录结构合理

**问题在于实现细节，而非整体架构。**

---

## 🔧 改进方案

### 方案 1: 修复提取逻辑（优先级：高）

#### 1.1 使用专门的提示词格式模式

```python
# 只匹配真正的提示词格式
prompt_patterns = [
    # Role-based: "You are a..."
    r'(?:You are|Act as|I want you to act as)[^.!?]{30,500}',

    # Task-based: "Please generate..."
    r'(?:Please|Generate|Create|Write)[^.!?]{30,500}\s+(?:an?|the)\s+\w+',

    # Explicit prompt markers
    r'Prompt:\s*["\']?([^.!?]{30,500})["\']?',
    r'Example\s*(?:prompt|example)?[:\s]+["\']?([^.!?]{30,500})',

    # Code/technical prompts
    r'(?:Code|Script|Program):\s*["\']?([^.!?]{30,500})',
]
```

#### 1.2 添加语义验证

```python
def is_valid_prompt(text: str) -> bool:
    """验证是否是真正的提示词"""
    # 必须包含指令性词汇
    instruction_words = [
        'generate', 'create', 'write', 'design', 'build',
        'analyze', 'explain', 'translate', 'summarize',
        'help me', 'show me', 'tell me'
    ]
    has_instruction = any(word in text.lower() for word in instruction_words)

    # 不能只是列表或标题
    if text.startswith(('1.', '2.', '-', '*', '•')):
        return False

    # 必须有足够的上下文
    if len(text.split()) < 5:
        return False

    return has_instruction
```

#### 1.3 针对性来源选择

```python
# 专注于专门的提示词数据库
TARGETED_SOURCES = {
    'promptbase.com': '专业的提示词市场',
    'prompts.chat': 'AI 提示词社区',
    'github.com/f/awesome-chatgpt-prompts': '精选提示词仓库',
    'github.com/dair-ai/Prompt-Engineering-Guide': '提示词指南示例',
}
```

---

### 方案 2: 修复 Agent 评估（优先级：高）

#### 2.1 调试返回值格式

```python
# 修改评估脚本，先打印原始返回值
response = sessions_spawn(
    task=eval_prompt,
    agentId="main",
    timeoutSeconds=30
)

# 调试：打印原始响应
logger.info(f"Raw response type: {type(response)}")
logger.info(f"Raw response: {response}")

# 如果是字符串，尝试解析
if isinstance(response, str):
    # 处理可能的格式
    pass
```

#### 2.2 添加降级机制

```python
# 如果 Agent 评估失败，使用改进的规则评分
if agent_evaluation_failed:
    logger.warning("Agent 评估失败，使用改进的规则评分")
    return enhanced_rule_based_score(prompt)
```

---

### 方案 3: 改进数据收集策略（优先级：中）

#### 3.1 分类收集

```python
# 针对不同类型使用不同的提取策略
COLLECTION_STRATEGIES = {
    'promptbase': {
        'url_patterns': ['promptbase.com'],
        'extraction': 'api_or_structured'
    },
    'github': {
        'url_patterns': ['github.com'],
        'extraction': 'code_block_or_list'
    },
    'tutorial': {
        'url_patterns': ['promptingguide.ai', 'learnprompting.org'],
        'extraction': 'example_blocks'
    }
}
```

#### 3.2 增加验证步骤

```python
# 收集后验证
def validate_prompt_batch(prompts: List[str]) -> List[str]:
    """批量验证提示词质量"""
    # 先用规则过滤
    filtered = [p for p in prompts if is_valid_prompt(p)]

    # 再用 Agent 评估（如果可用）
    evaluated = evaluate_with_agent(filtered)

    # 只保留高质量的
    return [p for p in evaluated if p['score'] >= 60]
```

---

## 📋 立即行动项

### 今天（1-2小时）

1. **修复提取逻辑** (`collect-prompts-via-searxng.py`)
   - ✅ 移除通用的列表匹配模式
   - ✅ 添加专门的提示词格式模式
   - ✅ 添加语义验证函数
   - ✅ 重新测试并验证结果

2. **修复 Agent 评估** (`evaluate-prompts-agent.py`)
   - ✅ 调试 `sessions_spawn` 返回值格式
   - ✅ 添加错误处理和降级机制
   - ✅ 测试评估功能

### 本周（3-4小时）

3. **改进来源选择**
   - ✅ 添加专门的提示词数据库（PromptBase API？）
   - ✅ 针对性提取 GitHub 仓库的示例
   - ✅ 跳过教程网站的通用内容

4. **建立质量监控**
   - ✅ 添加数据质量报告
   - ✅ 建立质量阈值（低于阈值自动丢弃）
   - ✅ 定期评估和调整参数

---

## 🎯 预期改进效果

修复后的目标：

| 指标 | 当前 | 目标 | 提升 |
|------|------|------|------|
| 高质量比例 | 0% | 40% | +40% |
| 低质量比例 | 88% | <10% | -78% |
| 平均分数 | 36.4 | 65+ | +28.6 |
| 提取成功率 | 低 | 高 | 3x |

---

## 💡 建议

### 短期（本周）
1. **立即修复提取逻辑** - 这是最关键的问题
2. **测试 Agent 评估** - 确保评估系统可用
3. **小规模测试** - 收集 50-100 条，验证质量

### 中期（2-4周）
1. **建立专用提取器** - 针对不同来源定制
2. **引入人工审核** - 初期样本人工验证
3. **持续优化** - 根据结果调整参数

### 长期（1-2个月）
1. **多源聚合** - PromptBase API + GitHub + 社区
2. **质量闭环** - 反馈机制持续改进
3. **自动化运营** - 全流程自动化

---

## 📝 总结

**当前问题**:
- 提取逻辑过于宽泛，导致 88% 垃圾数据
- Agent 评估脚本 JSON 解析失败
- 来源选择不当，大量爬取不适合的网站

**核心改进方向**:
1. 使用专门的提示词格式模式，而非通用列表匹配
2. 添加语义验证，确保提取的是真正的提示词
3. 修复 Agent 评估脚本，使其可用
4. 针对性选择数据源，避免教程网站的通用内容

**下一步行动**:
1. 修复 `collect-prompts-via-searxng.py` 的提取逻辑（优先级：高）
2. 修复 `evaluate-prompts-agent.py` 的 JSON 解析问题（优先级：高）
3. 重新测试并验证数据质量

---

*诊断完成。建议立即开始修复提取逻辑。*
