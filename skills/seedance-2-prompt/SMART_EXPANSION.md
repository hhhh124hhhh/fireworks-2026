# Seedance 2.0 智能扩展系统使用指南

## 📋 目录

1. [系统概述](#系统概述)
2. [快速开始](#快速开始)
3. [核心功能](#核心功能)
4. [API 参考](#api-参考)
5. [使用示例](#使用示例)
6. [最佳实践](#最佳实践)

---

## 系统概述

Seedance 2.0 智能扩展系统提供以下核心功能：

- **场景模板库管理**：存储和检索场景化的提示词模板
- **自动扩展机制**：自动将生成的提示词保存到模板库
- **联网学习机制**：从官方文档和网络搜索学习新的提示词模式
- **用户自定义**：允许用户添加自定义模板

### 文件结构

```
seedance-2-prompt/
├── scripts/
│   ├── smart_expansion.py        # 核心智能扩展系统
│   ├── learn_from_official.py    # 从官方学习
│   ├── learn_from_search.py      # 从网络搜索学习
│   ├── test_smart_expansion.py   # 综合测试
│   └── data/
│       └── template_library.json # 场景模板库存储
└── SMART_EXPANSION.md            # 本文档
```

---

## 快速开始

### 1. 基本使用

```python
from prompt_generator import PromptGenerator

# 创建生成器实例
generator = PromptGenerator()

# 生成提示词（会自动使用模板库）
result = generator.generate_prompt_with_timing(
    scene="竹林决战",
    style="写实",
    duration="15s",
    difficulty="ADVANCED"
)

# 查看结果
print(result['prompt'])
print(f"是否使用模板: {result['used_template']}")
```

### 2. 添加自定义模板

```python
from smart_expansion import add_custom_template

# 添加自定义模板
success = add_custom_template(
    scene_name="雪山对决",
    intro="镜头从雪山之巅开始，寒风呼啸，雪花纷飞。两位高手在白雪皑皑的山顶对峙。",
    main_action="动作迅猛有力，剑气激起的雪尘在空中飞舞。每一次交锋都带着破冰的气势。",
    emotion_rise="表情从冷静对峙转为激烈对抗，眼神中燃烧着战斗的火焰。",
    conclusion="最终，胜负已分。胜者站在雪山之巅，雪花落在他的剑上。",
    tags=["雪山", "对决", "剑术"]
)
```

### 3. 从网络学习

```python
from learn_from_search import search_and_learn

# 搜索并学习新模板
result = search_and_learn(
    query="浪漫约会场景",
    max_results=5,
    auto_save=True
)

print(f"找到 {result['results_count']} 个结果")
print(f"学习了 {result['templates_learned']} 个模板")
```

---

## 核心功能

### 1. 场景模板库管理

#### 加载模板库

```python
from smart_expansion import SceneTemplateLibrary

# 加载模板库
library = SceneTemplateLibrary()

# 获取统计信息
stats = library.get_stats()
print(f"总模板数: {stats['total_templates']}")
print(f"情感类型: {stats['emotion_types']}")
```

#### 检索模板

```python
# 根据场景名称获取模板
template = library.get_template("竹林决战")

# 列出所有模板
all_templates = library.list_templates()

# 搜索模板
results = library.search_templates("竹")
for emotion_type, scene_name, template in results:
    print(f"{emotion_type}: {scene_name}")
```

#### 添加模板

```python
template = {
    "emotion": "combat",
    "environment": "forest_combat",
    "intro": "镜头快速展开...",
    "main_action": "动作迅猛有力...",
    "emotion_rise": "表情从冷静对峙...",
    "conclusion": "最终，胜负已分...",
    "tags": ["竹林", "决战"]
}

library.add_template("新场景", template, "combat")
```

### 2. 自动扩展机制

```python
from prompt_generator import PromptGenerator

generator = PromptGenerator()

# 生成新场景（会自动保存到模板库）
result = generator.generate_prompt_with_timing(
    scene="沙漠追逐",
    style="写实",
    auto_save=True  # 启用自动保存
)

# 查看是否自动保存
print(f"自动保存: {result.get('auto_saved', False)}")

# 下次生成同一场景会使用模板
result2 = generator.generate_prompt_with_timing(
    scene="沙漠追逐",
    style="写实"
)

print(f"使用模板: {result2.get('used_template', False)}")
```

### 3. 情感和环境检测

```python
from smart_expansion import detect_emotion, detect_environment

# 检测情感
emotion = detect_emotion("竹林决战")
print(emotion)  # 输出: combat

# 检测环境
environment = detect_environment("竹林决战")
print(environment)  # 输出: forest_combat
```

### 4. 联网学习

#### 从官方学习

```python
from learn_from_official import update_from_official

# 从官方文档更新模板
result = update_from_official(
    force_fetch=True,
    auto_save=True
)

print(f"找到 {result['templates_found']} 个官方模板")
print(f"添加了 {result['templates_added']} 个模板")
```

#### 从网络搜索学习

```python
from learn_from_search import search_and_learn, batch_learn_from_search

# 单次搜索学习
result = search_and_learn(
    query="浪漫约会",
    max_results=10,
    auto_save=True
)

# 批量搜索学习
queries = ["浪漫约会", "城市夜景", "武侠打斗"]
batch_result = batch_learn_from_search(
    queries=queries,
    max_results=5,
    auto_save=True
)

print(f"总查询数: {batch_result['total_queries']}")
print(f"成功查询数: {batch_result['successful_queries']}")
print(f"总学习模板数: {batch_result['total_templates_learned']}")
```

---

## API 参考

### SceneTemplateLibrary

#### 方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `get_template(scene_key, emotion_type=None)` | 获取指定模板 | Dict 或 None |
| `add_template(name, template, emotion_type=None)` | 添加新模板 | bool |
| `list_templates(emotion_type=None)` | 列出模板 | Dict |
| `search_templates(keyword)` | 搜索模板 | List[Tuple] |
| `get_stats()` | 获取统计信息 | Dict |

### PromptGenerator

#### 新增参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `use_template` | bool | True | 是否使用场景模板库 |
| `auto_save` | bool | True | 是否自动保存新模板 |

#### 返回值

新增字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `used_template` | bool | 是否使用了模板库中的模板 |
| `template_source` | str | 模板来源（"template_library" 或 None） |
| `auto_saved` | bool | 是否自动保存了新模板 |

### 便捷函数

| 函数 | 说明 |
|------|------|
| `add_custom_template(...)` | 添加自定义模板 |
| `auto_expand_template(scene, generated_prompt)` | 自动扩展模板 |
| `detect_emotion(scene)` | 检测情感类型 |
| `detect_environment(scene)` | 检测环境类型 |

---

## 使用示例

### 示例 1：创建完整的打戏场景

```python
from prompt_generator import PromptGenerator
from smart_expansion import add_custom_template

# 方法 1：使用生成器自动生成
generator = PromptGenerator()

result = generator.generate_prompt_with_timing(
    scene="竹林决战",
    style="写实",
    duration="15s",
    difficulty="ADVANCED"
)

print("生成的提示词:")
print(result['prompt'])
print("\n分段:")
for segment_name, segment_text in result['segments'].items():
    print(f"{segment_name}: {segment_text}")

# 方法 2：添加自定义模板
add_custom_template(
    scene_name="雪山对决",
    intro="镜头从雪山之巅开始...",
    main_action="动作迅猛有力...",
    emotion_rise="表情从冷静对峙...",
    conclusion="最终，胜负已分...",
    tags=["雪山", "对决"]
)
```

### 示例 2：批量学习并生成

```python
from learn_from_search import batch_learn_from_search
from prompt_generator import PromptGenerator

# 1. 批量学习
queries = ["浪漫约会", "城市夜景", "武侠打斗"]
batch_result = batch_learn_from_search(queries, max_results=3, auto_save=True)

print(f"学习了 {batch_result['total_templates_learned']} 个模板")

# 2. 使用学习到的模板生成
generator = PromptGenerator()

for query in queries:
    result = generator.generate_prompt_with_timing(
        scene=query,
        style="写实"
    )

    print(f"\n{query}:")
    print(f"  使用模板: {result.get('used_template', False)}")
    print(f"  字数: {result.get('word_count', 0)}")
```

### 示例 3：模板管理和搜索

```python
from smart_expansion import SceneTemplateLibrary

library = SceneTemplateLibrary()

# 获取统计信息
stats = library.get_stats()
print(f"模板库统计:")
print(f"  总数: {stats['total_templates']}")
print(f"  情感类型: {', '.join(stats['emotion_types'])}")

# 列出所有 combat 类型的模板
combat_templates = library.list_templates("combat")
print(f"\nCombat 模板:")
for scene_name, template in combat_templates.items():
    print(f"  - {scene_name}")

# 搜索包含"竹"的模板
results = library.search_templates("竹")
print(f"\n搜索 '竹':")
for emotion_type, scene_name, template in results:
    print(f"  {emotion_type}: {scene_name}")
```

---

## 最佳实践

### 1. 模板命名规范

- 使用清晰的场景名称，如 "竹林决战"、"雪山对决"
- 避免使用过于简短的名称
- 保持命名一致性

### 2. 标签使用

- 使用有意义的标签，如 ["竹林", "决战", "剑术"]
- 标签应该反映场景的核心要素
- 避免使用过多或过少的标签

### 3. 自动保存策略

- 在开发和测试阶段启用自动保存（`auto_save=True`）
- 在生产环境根据需求决定是否启用
- 定期清理自动生成的低质量模板

### 4. 模板质量

- 定期审查和更新模板库
- 删除重复或低质量的模板
- 保留高质量的官方和学习到的模板

### 5. 性能优化

- 对于常用场景，优先使用模板库（`use_template=True`）
- 对于新场景，可以禁用模板库以加速生成
- 定期备份模板库数据

---

## 常见问题

### Q1: 如何重置模板库？

```python
from pathlib import Path
import json

# 备份当前模板库
template_path = Path("/root/clawd/skills/seedance-2-prompt/scripts/data/template_library.json")
template_path.replace(template_path.with_suffix('.json.bak'))

# 重新加载会创建新的模板库
```

### Q2: 如何导出模板库？

```python
from learn_from_search import export_learned_templates

# 导出所有模板
export_learned_templates("output/templates.json")
```

### Q3: 为什么某些场景没有使用模板？

可能的原因：
- 场景名称不完全匹配
- 模板库中没有该场景
- `use_template` 参数设置为 `False`

### Q4: 如何提高情感检测的准确性？

在场景描述中包含明确的情感关键词：
- Combat: "决战", "打戏", "对决", "激战"
- Happy: "开心", "快乐", "喜悦"
- Romantic: "浪漫", "爱情", "约会"

---

## 更新日志

### v2.0 (2026-02-15)

- ✅ 实现场景模板库管理
- ✅ 实现自动扩展机制
- ✅ 实现联网学习功能
- ✅ 实现用户自定义模板
- ✅ 集成到 PromptGenerator
- ✅ 完成所有测试用例

---

## 联系支持

如有问题或建议，请查阅：
- Seedance 2.0 官方文档
- 项目 GitHub 仓库
- 技术支持邮箱
