# Seedance 2.0 联网功能文档

本文档详细介绍了 Seedance 2.0 提示词 Skill 的联网功能，包括在线搜索、模板更新等。

## 目录

- [功能概述](#功能概述)
- [在线搜索](#在线搜索)
- [模板更新](#模板更新)
- [API 参考](#api-参考)
- [配置说明](#配置说明)
- [故障排除](#故障排除)

---

## 功能概述

Seedance 2.0 提示词 Skill 支持以下联网功能：

1. **在线搜索** - 搜索最新的 Seedance 2.0 提示词
2. **模板更新** - 从网络获取最新模板，更新本地模板库
3. **智能合并** - 将在线搜索结果与本地模板智能结合

### 优势

- ✅ 获取最新的提示词创意和灵感
- ✅ 扩展本地模板库
- ✅ 学习优秀的提示词写作技巧
- ✅ 自动 Fallback 机制，确保可靠性
- ✅ 多搜索源支持，提高搜索成功率

---

## 在线搜索

### 基本使用

#### 命令行

```bash
# 基本搜索
python scripts/search_online.py "雨天城市街道"

# 按视频类型搜索
python scripts/search_online.py "人物肖像" -t photo-realistic

# 按难度搜索
python scripts/search_online.py "复杂场景" -d ADVANCED

# 组合搜索
python scripts/search_online.py "城市夜景" -t photo-realistic -d INTERMEDIATE -n 10
```

#### Python API

```python
from scripts.search_online import search_prompts

# 基本搜索
results = search_prompts("雨天城市街道")

# 按视频类型搜索
results = search_prompts(
    query="人物肖像",
    video_type="photo-realistic",
    max_results=10
)

# 按难度搜索
results = search_prompts(
    query="复杂场景",
    difficulty="ADVANCED",
    max_results=5
)

# 组合搜索
results = search_prompts(
    query="城市夜景",
    video_type="photo-realistic",
    difficulty="INTERMEDIATE",
    max_results=10
)
```

### 搜索参数

| 参数 | 类型 | 必需 | 说明 | 可选值 |
|------|------|------|------|--------|
| `query` | str | 是 | 搜索关键词 | 任意文本 |
| `video_type` | str | 否 | 视频类型 | `photo-realistic`, `character-consistency`, `camera-movement`, `creative-effects`, `storytelling`, `audio-sync`, `one-shot`, `emotion-performance` |
| `difficulty` | str | 否 | 难度级别 | `BEGINNER`, `INTERMEDIATE`, `ADVANCED`, `EXPERT` |
| `max_results` | int | 否 | 最大结果数量 | 默认 10 |

### 返回格式

```python
[
    {
        "id": "online-a1b2c3d4",
        "name": "提示词标题",
        "title": "完整的提示词标题",
        "prompt": "提示词内容...",
        "video_type": "photo-realistic",
        "difficulty": "INTERMEDIATE",
        "description": "描述内容...",
        "tags": ["Seedance 2.0", "AI", "视频"],
        "duration": "5-10s",
        "source": "online-search",
        "url": "https://example.com/prompt",
        "search_source": "tavily",
        "search_timestamp": "2026-02-14T12:34:56.789123"
    },
    ...
]
```

### 搜索源

在线搜索功能使用 info-search 项目的 `search-wrapper.py`，支持以下搜索源：

1. **Tavily** (优先)
   - 高质量搜索结果
   - API Key 已配置
   - 超时或错误 → Fallback 到百度

2. **百度搜索** (Fallback 1)
   - 百度 AI 搜索 API
   - 支持中文搜索优化
   - 失败 → Fallback 到 SearXNG

3. **SearXNG** (Fallback 2)
   - 本地搜索服务
   - 开源、免费
   - 失败 → Fallback 到 Brave

4. **Brave Search API** (Fallback 3)
   - 免费版无需 API Key
   - 隐私保护
   - 最后的备选方案

### 工作原理

1. **构建搜索查询**
   - 将用户输入的关键词与 "Seedance 2.0"、"提示词" 等关键词组合
   - 如果指定了视频类型或难度级别，也会添加到查询中

2. **执行搜索**
   - 使用 `search-wrapper.py` 执行搜索
   - 自动 Fallback 到下一个搜索源

3. **提取和格式化**
   - 从搜索结果中提取提示词相关信息
   - 尝试识别视频类型和难度级别
   - 标准化返回格式

---

## 模板更新

### 基本使用

#### 命令行

```bash
# 从搜索更新模板
python scripts/update_templates.py --search "最新 Seedance 2.0 提示词"

# 指定结果数量
python scripts/update_templates.py --search "人物肖像" -n 20

# 强制更新（覆盖已存在的模板）
python scripts/update_templates.py --search "城市夜景" -f
```

#### Python API

```python
from scripts.update_templates import TemplateUpdater

updater = TemplateUpdater()

# 从搜索获取模板
templates = updater.fetch_templates_from_search(
    query="最新 Seedance 2.0 提示词",
    max_results=10
)

# 更新本地模板库
count = updater.update_local_templates(templates)

print(f"更新了 {count} 个模板")

# 获取统计信息
stats = updater.get_stats()
print(f"新增: {stats['added']}")
print(f"更新: {stats['updated']}")
print(f"跳过: {stats['skipped']}")
print(f"失败: {stats['failed']}")
```

### 更新策略

#### 智能合并

- **新模板** - 直接添加到本地模板库
- **已存在模板** - 默认跳过，使用 `-f` 强制更新
- **唯一 ID** - 基于提示词内容生成哈希值，避免重复

#### 统计信息

更新完成后会显示以下统计信息：

- **新增** - 新添加的模板数量
- **更新** - 已存在并更新的模板数量
- **跳过** - 因已存在而跳过的模板数量
- **失败** - 处理失败的模板数量

### 模板库位置

本地模板库保存在：
```
/root/clawd/skills/seedance-2-prompt/data/templates.json
```

### 更新日志

模板库包含以下元数据：

- `last_updated` - 最后更新时间
- `templates` - 模板列表

---

## API 参考

### search_prompts()

在线搜索提示词。

**函数签名：**
```python
def search_prompts(
    query: str,
    video_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    max_results: int = 10
) -> List[Dict]
```

**参数：**
- `query` (str): 搜索关键词
- `video_type` (Optional[str]): 视频类型
- `difficulty` (Optional[str]): 难度级别
- `max_results` (int): 最大结果数量

**返回：**
- `List[Dict]`: 提示词结果列表

**示例：**
```python
results = search_prompts("雨天城市街道")
```

### PromptGenerator.generate_prompt_with_search()

生成提示词（可选在线搜索）。

**函数签名：**
```python
def generate_prompt_with_search(
    self,
    scene: str,
    style: Optional[str] = None,
    duration: Optional[str] = None,
    difficulty: str = "INTERMEDIATE",
    video_type: str = "photo-realistic",
    include_elements: bool = True,
    use_online: bool = True,
    online_search: bool = False,
    max_online_results: int = 5
) -> Dict
```

**参数：**
- `scene` (str): 场景描述
- `style` (Optional[str]): 风格
- `duration` (Optional[str]): 时长
- `difficulty` (str): 难度级别
- `video_type` (str): 视频类型
- `include_elements` (bool): 是否包含元素分析
- `use_online` (bool): 是否使用在线功能（默认启用）
- `online_search` (bool): 是否先搜索再生成（默认 False）
- `max_online_results` (int): 最大在线搜索结果数量

**返回：**
- `Dict`: 包含生成结果的字典

**示例：**
```python
from scripts.prompt_generator import PromptGenerator

generator = PromptGenerator()
result = generator.generate_prompt_with_search(
    scene="一位年轻女性在花园里散步",
    online_search=True
)
```

### TemplateUpdater

模板更新器类。

**方法：**

#### fetch_templates_from_search()

```python
def fetch_templates_from_search(
    self,
    query: str,
    max_results: int = 10
) -> List[Dict]
```

从搜索结果获取模板。

#### update_local_templates()

```python
def update_local_templates(
    self,
    new_templates: List[Dict],
    force: bool = False
) -> int
```

更新本地模板库。

#### get_stats()

```python
def get_stats(self) -> Dict
```

获取更新统计信息。

**示例：**
```python
from scripts.update_templates import TemplateUpdater

updater = TemplateUpdater()
templates = updater.fetch_templates_from_search("Seedance 2.0", max_results=10)
count = updater.update_local_templates(templates)
stats = updater.get_stats()
```

---

## 配置说明

### 搜索源配置

搜索源配置由 `search-wrapper.py` 管理，配置文件位置：

```
/root/clawd/.config/data-sources/
```

#### Tavily 配置 (tavily.conf)
```
TAVILY_API_KEY="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"
TIMEOUT=30
```

#### SearXNG 配置 (searxng.conf)
```
SEARXNG_URL="http://localhost:8080"
TIMEOUT=30
```

### 日志配置

日志文件位置：

```
/root/clawd/skills/seedance-2-prompt/logs/
```

- `search_online.log` - 在线搜索日志
- `update_templates.log` - 模板更新日志
- `prompt_generator.log` - 提示词生成日志

---

## 故障排除

### 在线搜索失败

**问题：** 搜索提示 "在线搜索功能不可用"

**解决方案：**

1. 检查 `search-wrapper.py` 是否可用：
   ```bash
   python3 /root/clawd/projects/info-search/scripts/search-wrapper.py "test"
   ```

2. 检查搜索源配置：
   ```bash
   cat /root/clawd/.config/data-sources/tavily.conf
   cat /root/clawd/.config/data-sources/searxng.conf
   ```

3. 检查网络连接：
   ```bash
   ping -c 3 api.tavily.com
   ```

4. 查看日志：
   ```bash
   tail -f /root/clawd/skills/seedance-2-prompt/logs/search_online.log
   ```

### 模板更新失败

**问题：** 更新模板时出错

**解决方案：**

1. 检查模板库目录是否存在：
   ```bash
   ls -la /root/clawd/skills/seedance-2-prompt/data/
   ```

2. 检查文件权限：
   ```bash
   chmod 755 /root/clawd/skills/seedance-2-prompt/data/
   chmod 644 /root/clawd/skills/seedance-2-prompt/data/templates.json
   ```

3. 查看日志：
   ```bash
   tail -f /root/clawd/skills/seedance-2-prompt/logs/update_templates.log
   ```

### 搜索结果质量不佳

**问题：** 搜索结果不相关或质量低

**解决方案：**

1. 尝试更具体的关键词
2. 指定视频类型和难度级别进行过滤
3. 尝试不同的搜索源（通过配置）
4. 增加搜索结果数量

### 导入错误

**问题：** `ImportError: No module named 'search_wrapper'`

**解决方案：**

1. 确保 `info-search` 项目路径正确
2. 确保 `search-wrapper.py` 存在且可执行
3. 检查 Python 路径设置

---

## 使用技巧

### 1. 高效搜索

- 使用具体的关键词，而不是泛泛的描述
- 指定视频类型和难度级别以获得更精确的结果
- 定期更新模板库以获取最新内容

### 2. 提示词优化

- 使用在线搜索结果作为灵感
- 结合本地模板和在线提示词
- 提取优秀提示词的结构和元素

### 3. 模板管理

- 定期备份本地模板库
- 使用 `-f` 强制更新时要小心
- 根据需要清理不使用的模板

---

## 更新日志

### 2026-02-14
- ✅ 添加在线搜索功能
- ✅ 添加模板更新功能
- ✅ 集成 info-search 的 search-wrapper
- ✅ 添加完整的文档和示例

---

## 相关文档

- [SKILL.md](../SKILL.md) - 主要文档
- [references/templates.md](templates.md) - 模板库文档
- [references/video-types.md](video-types.md) - 视频类型文档
- [references/difficulty-levels.md](difficulty-levels.md) - 难度级别文档

---

## 技术支持

如有问题，请查看：

1. 日志文件
2. 故障排除部分
3. 相关文档

或提交 Issue 到项目仓库。
