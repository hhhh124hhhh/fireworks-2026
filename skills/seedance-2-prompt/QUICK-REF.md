# Seedance 2.0 联网功能快速参考

## 🚀 快速开始

### 搜索在线提示词

```bash
# 基本搜索
python scripts/search_online.py "雨天城市街道"

# 按类型搜索
python scripts/search_online.py "人物肖像" -t photo-realistic

# 按难度搜索
python scripts/search_online.py "复杂场景" -d ADVANCED
```

### 生成提示词（使用在线搜索）

```python
from scripts.prompt_generator import PromptGenerator

generator = PromptGenerator()
result = generator.generate_prompt_with_search(
    scene="雨天城市街道",
    online_search=True
)
```

### 更新模板库

```bash
# 从搜索更新
python scripts/update_templates.py --search "最新 Seedance 2.0 提示词"
```

---

## 📋 视频类型

| 类型 | 说明 |
|------|------|
| `photo-realistic` | 超逼真视频生成 |
| `character-consistency` | 角色与场景一致性 |
| `camera-movement` | 高级运镜动作 |
| `creative-effects` | 创意视觉特效 |
| `storytelling` | 剧情发展与延伸 |
| `audio-sync` | 音频与语音合成 |
| `one-shot` | 一镜到底 |
| `emotion-performance` | 情绪演绎 |

---

## 📊 难度级别

| 级别 | 说明 |
|------|------|
| `BEGINNER` | 初学者（简单描述，基础元素） |
| `INTERMEDIATE` | 中级（增加光影和镜头） |
| `ADVANCED` | 高级（完整的万能公式） |
| `EXPERT` | 专家（极致细节和专业术语） |

---

## 🔧 Python API

### search_prompts()

```python
from search_online import search_prompts

results = search_prompts(
    query="雨天城市街道",
    video_type="photo-realistic",
    difficulty="INTERMEDIATE",
    max_results=10
)
```

### PromptGenerator.generate_prompt_with_search()

```python
from prompt_generator import PromptGenerator

generator = PromptGenerator()
result = generator.generate_prompt_with_search(
    scene="雨天城市街道",
    style="梦幻",
    difficulty="INTERMEDIATE",
    video_type="photo-realistic",
    online_search=True,
    max_online_results=5
)
```

### TemplateUpdater

```python
from update_templates import TemplateUpdater

updater = TemplateUpdater()

# 获取新模板
templates = updater.fetch_templates_from_search(
    query="Seedance 2.0 提示词",
    max_results=10
)

# 更新本地库
count = updater.update_local_templates(templates)

# 获取统计
stats = updater.get_stats()
```

---

## 📚 文档

| 文档 | 路径 |
|------|------|
| 主文档 | `SKILL.md` |
| 联网功能详细说明 | `references/online-features.md` |
| 交付报告 | `DELIVERY-REPORT.md` |
| 使用示例 | `scripts/usage_examples.py` |

---

## 🧪 测试

```bash
# 运行所有测试
python scripts/test_online_features.py

# 运行使用示例
python scripts/usage_examples.py
```

---

## 📝 日志

| 日志 | 路径 |
|------|------|
| 搜索日志 | `logs/search_online.log` |
| 更新日志 | `logs/update_templates.log` |
| 生成日志 | `logs/prompt_generator.log` |

---

## ⚙️ 配置

搜索源配置: `/root/clawd/.config/data-sources/`

### Tavily (tavily.conf)
```
TAVILY_API_KEY="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"
TIMEOUT=30
```

### SearXNG (searxng.conf)
```
SEARXNG_URL="http://localhost:8080"
TIMEOUT=30
```

---

## 🔍 故障排除

### 在线搜索不可用

1. 检查 `search-wrapper.py` 是否可用
2. 检查搜索源配置文件
3. 检查网络连接
4. 查看日志文件

### 搜索结果为空

1. 尝试不同的关键词
2. 检查搜索源是否正常工作
3. 增加搜索结果数量限制

### 模板更新失败

1. 检查 `data/templates.json` 文件权限
2. 确保目录存在且可写
3. 查看更新日志

---

## 💡 使用技巧

1. **高效搜索** - 使用具体的关键词
2. **精确过滤** - 指定视频类型和难度级别
3. **定期更新** - 定期更新模板库
4. **智能合并** - 结合本地模板和在线提示词
5. **备份管理** - 定期备份本地模板库
