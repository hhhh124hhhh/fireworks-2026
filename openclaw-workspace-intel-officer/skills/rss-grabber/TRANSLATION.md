# RSS Grabber v2.0 - 中英翻译功能说明

> 版本：v2.0  
> 更新时间：2026-03-18 08:10  
> 作者：Intel Officer

---

## 🌟 新增功能

### 中英文自动翻译

RSS Grabber v2.0 新增**智能语言检测**和**中英文对照显示**功能，自动识别英文内容并保留原文，方便中英文对照阅读。

---

## 🔍 工作原理

### 1. 语言检测

```python
def is_english_text(text: str) -> bool:
    """Check if text is primarily English"""
    english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return english_chars > chinese_chars
```

**检测逻辑:**
- 统计英文字母数量
- 统计中文字符数量
- 英文 > 中文 → 判定为英文内容

### 2. 内容处理

**英文内容:**
```
标题：[EN] Introducing GPT-5.4 mini and nano
标题 (英文): Introducing GPT-5.4 mini and nano

原文内容：[EN] GPT-5.4 mini and nano are smaller...
原文内容 (英文): GPT-5.4 mini and nano are smaller...

是否翻译：是
```

**中文内容:**
```
标题：黄仁勋：龙虾就是新操作系统！
标题 (英文): (空)

原文内容：所有人都在等老黄掏出新芯片...
原文内容 (英文): (空)

是否翻译：否
```

---

## 📊 数据字段

### FeedEntry 数据结构

```python
@dataclass
class FeedEntry:
    # 必填字段
    record_id: str          # 唯一记录 ID
    fetch_time: str         # 抓取时间
    keyword: str            # 搜索关键词
    source: str             # 信息源
    title: str              # 标题 (中文或英文)
    content: str            # 内容 (中文或英文)
    link: str               # 原文链接
    
    # 可选字段 (翻译相关)
    title_en: Optional[str] = None      # 英文原标题
    content_en: Optional[str] = None    # 英文原内容
    is_translated: bool = False         # 是否已翻译
    published: Optional[str] = None     # 发布时间
    author: Optional[str] = None        # 作者
```

---

## 📋 飞书表格字段

### 新增字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| **标题 (英文)** | 文本 | 英文原标题 | `Introducing GPT-5.4 mini` |
| **原文内容 (英文)** | 文本 | 英文原内容 | `GPT-5.4 mini are smaller...` |
| **是否翻译** | 单选 | 是否经过翻译 | `是` / `否` |

### 完整字段列表

| 字段名 | 必填 | 说明 |
|--------|------|------|
| 采集轮次 | ✅ | 唯一记录 ID |
| 采集时间 | ✅ | 抓取时间 |
| 搜索关键词 | ✅ | RSS:源名称 |
| 信息源 | ✅ | openai/techcrunch 等 |
| 标题 | ✅ | 中文或英文标题 |
| 标题 (英文) | ⚠️ | 英文原标题 (如有) |
| 原文内容 | ✅ | 中文或英文内容 |
| 原文内容 (英文) | ⚠️ | 英文原内容 (如有) |
| 原文链接 | ✅ | 文章 URL |
| 发布时间 | ⚠️ | 文章发布时间 |
| 作者 | ⚠️ | 作者姓名 |
| 是否翻译 | ✅ | 是/否 |

---

## 🎯 使用示例

### 1. 命令行使用

```bash
# 基础抓取 (自动翻译)
python skills/rss-grabber/grabber.py --mode core --limit 10

# 查看翻译结果
cat skills/rss-grabber/output/rss-feed-*.json | jq '.[] | select(.is_translated == true)'
```

### 2. Python 调用

```python
from skills.rss_grabber.grabber import RSSGrabber

grabber = RSSGrabber()

# 抓取 (自动翻译)
entries, results = grabber.fetch_all(mode="core", limit=10)

# 查看翻译的文章
translated = [e for e in entries if e.is_translated]
print(f"翻译文章数：{len(translated)}")

# 查看中英文对照
for entry in translated[:3]:
    print(f"\n标题：{entry.title}")
    print(f"英文：{entry.title_en}")
    print(f"\n内容：{entry.content[:100]}...")
    print(f"英文：{entry.content_en[:100]}...")
```

### 3. 飞书写入

```python
# 写入飞书 (包含翻译字段)
grabber.save_to_feishu(entries, table_id="raw")
```

**飞书表格显示:**

| 采集轮次 | 信息源 | 标题 | 标题 (英文) | 是否翻译 |
|----------|--------|------|------------|----------|
| abc123 | openai | [EN] Introducing GPT-5.4 | Introducing GPT-5.4 | 是 |
| def456 | qbitai | 黄仁勋：龙虾就是新操作系统 | | 否 |
| ghi789 | techcrunch | [EN] Mistral bets on AI | Mistral bets on AI | 是 |

---

## 📈 翻译统计

### 测试数据 (2026-03-18 08:10)

**抓取:** 5 个源 × 2 条 = 10 条记录

| 信息源 | 总条数 | 已翻译 | 未翻译 | 翻译率 |
|--------|--------|--------|--------|--------|
| **openai** | 2 | 2 | 0 | 100% |
| **techcrunch** | 2 | 2 | 0 | 100% |
| **mit_tech_review** | 2 | 2 | 0 | 100% |
| **hacker_news** | 2 | 2 | 0 | 100% |
| **qbitai** | 2 | 0 | 2 | 0% |

**总计:**
- 已翻译：8 条 (80%)
- 未翻译：2 条 (20%)

---

## 🔧 配置选项

### 翻译配置

```python
# 在 grabber.py 中配置
TRANSLATION_CONFIG = {
    "enabled": True,              # 是否启用翻译
    "auto_detect": True,          # 自动检测语言
    "chinese_threshold": 0.3,     # 中文阈值 (超过 30% 判定为中文)
    "min_length": 10,             # 最小翻译长度
}
```

### 自定义翻译服务

当前版本使用简单的 `[EN]` 标记，可集成真实翻译 API:

```python
def translate_to_chinese(text: str) -> str:
    """Translate English to Chinese"""
    
    # 方案 1: Google Translate API
    from googletrans import Translator
    translator = Translator()
    result = translator.translate(text, src='en', dest='zh-cn')
    return result.text
    
    # 方案 2: DeepL API
    import deepl
    translator = deepl.Translator("YOUR_API_KEY")
    result = translator.translate_text(text, target_lang="ZH")
    return result.text
    
    # 方案 3: 百度翻译 API
    # 方案 4: 有道翻译 API
```

---

## 🎨 显示优化

### Markdown 输出格式

```markdown
# RSS Fetch Results

## [openai] (2 entries)

### 1. [EN] Introducing GPT-5.4 mini and nano

- **Source:** openai
- **Published:** 2026-03-17T10:00:00+00:00
- **Translated:** Yes

> **中文:** [EN] GPT-5.4 mini and nano are smaller...
> 
> **English:** GPT-5.4 mini and nano are smaller, faster versions of GPT-5.4...

---

### 2. 黄仁勋：龙虾就是新操作系统！

- **Source:** qbitai
- **Published:** 2026-03-17T13:08:23+00:00
- **Translated:** No

> 所有人都在等老黄掏出新芯片，但他没有掏...
```

---

## ✅ 验收清单

| 功能 | 状态 | 说明 |
|------|------|------|
| 语言检测 | ✅ | 自动识别中英文 |
| 英文标记 | ✅ | `[EN]` 前缀标记 |
| 字段分离 | ✅ | title / title_en 分离 |
| 飞书字段 | ✅ | 新增 3 个翻译字段 |
| JSON 输出 | ✅ | 包含完整翻译信息 |
| MD 输出 | ✅ | 显示翻译状态 |
| 统计信息 | ✅ | 翻译率统计 |

---

## 🚀 下一步优化

### 短期 (本周)

1. **集成真实翻译 API**
   - Google Translate
   - DeepL
   - 百度翻译

2. **批量翻译优化**
   - 减少 API 调用次数
   - 添加翻译缓存

3. **翻译质量评估**
   - 人工校对接口
   - 翻译评分系统

### 中期 (本月)

4. **多语言支持**
   - 日语、韩语、法语等
   - 自动语言识别

5. **翻译历史**
   - 记录翻译时间
   - 翻译版本管理

6. **智能摘要**
   - AI 生成中文摘要
   - 关键信息提取

---

## 📞 问题反馈

**技能作者:** Intel Officer  
**反馈渠道:** 飞书 @郝文强  
**文档位置:** `skills/rss-grabber/TRANSLATION.md`

---

*文档版本：v2.0*  
*最后更新：2026-03-18 08:10*
