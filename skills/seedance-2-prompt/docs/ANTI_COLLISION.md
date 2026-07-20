# Seedance 2.0 防撞脸人物特征生成器

## 📋 简介

Seedance 2.0 AI 视频生成中，人物"撞脸"（不同视频中人物脸部特征过于相似）是一个常见问题。本工具通过生成独特的人物特征描述，帮助防止撞脸，提升视频质量。

---

## 🎭 功能特性

### 1. 独特人物特征生成
- 脸型：9 种（鹅蛋脸、瓜子脸、圆脸、长脸、方脸等）
- 眼睛：9 种（丹凤眼、杏仁眼、圆眼、桃花眼等）
- 眉毛：8 种（剑眉、平眉、柳叶眉等）
- 鼻子：8 种（高鼻梁、小巧鼻、直鼻梁等）
- 嘴唇：7 种（樱桃小嘴、厚唇、薄唇、M字唇等）
- 发型：11 种（长发、短发、中长发、波波头、卷发等）
- 发色：10 种（黑色、棕色、金色、银色、彩色等）
- 肤色：7 种（白皙、小麦色、橄榄色、深褐色等）
- 年龄：6 种（18-20岁少女 到 40-45岁中年）
- 气质：8 种（清纯可爱、成熟优雅、知性气质等）
- 身高：5 种（155cm 到 175cm）
- 体型：5 种（纤细苗条、匀称健康、丰满曲线等）
- 服饰风格：8 种（简约时尚、休闲舒适、职业装等）

### 2. 组合数量
理论组合数量：**1,341,204,480+ 种**（13 个维度的乘积）
- 确保每次生成的人物都是独特的
- 避免重复和撞脸

### 3. 去重机制
- 自动记录已生成的人物 ID
- 避免重复生成相同特征
- 支持排除特定人物

---

## 🚀 使用方法

### 命令行工具

```bash
cd /root/clawd/skills/seedance-2-prompt

# 生成 3 个独特人物
python3 scripts/character_generator.py -n 3

# 生成详细描述
python3 scripts/character_generator.py -n 3 --detailed

# 输出 Seedance 2.0 提示词格式
python3 scripts/character_generator.py -n 3 --prompt-format

# 为特定场景生成人物
python3 scripts/character_generator.py --scene "公园散步" --style realistic

# 显示统计信息
python3 scripts/character_generator.py --stats
```

### Python API

#### 基本使用

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()

# 生成单个人物
char = generator.generate_unique_character()
print(char)

# 生成多个人物
characters = generator.generate_multiple_characters(5)
for char in characters:
    print(char)
```

#### 格式化输出

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()
char = generator.generate_unique_character()

# 格式化为描述
desc = generator.format_character_description(char, detailed=False)
print(desc)
# 输出：一位20-25岁青年，知性气质的女性，瓜子脸，发型，发色，肤色，眼睛

# 格式化为 Seedance 2.0 提示词
prompt = generator.format_character_for_prompt(char)
print(prompt)
# 输出：一位20-25岁青年，知性气质的女性，瓜子脸，肤色，发型，发色，眼睛，眉毛，鼻子，嘴唇，身高，体型
```

#### 为特定场景生成人物

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()

# 写实风格
char = generator.generate_character_for_scene("公园散步", style="realistic")

# 动漫风格
char = generator.generate_character_for_scene("校园日常", style="anime")

# 奇幻风格
char = generator.generate_character_for_scene("魔法世界", style="fantasy")
```

---

## 📚 示例

### 示例 1：单个人物场景

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()
char = generator.generate_unique_character()

prompt = (
    f"{generator.format_character_for_prompt(char)}，"
    "在海边看日落，唯美风格，超高清电影级画质，"
    "黄金时刻光线，浪漫氛围，电影感"
)

print(prompt)
```

**输出**：
```
一位35-40岁青年，阳光活力的女性，椭圆脸，深褐色皮肤，马尾，蓝色，杏仁眼，剑眉，高鼻梁，M字唇，165cm标准，丰满曲线，在海边看日落，唯美风格，超高清电影级画质，黄金时刻光线，浪漫氛围，电影感
```

### 示例 2：多个人物场景

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()
characters = generator.generate_multiple_characters(3)

char_descs = [generator.format_character_for_prompt(c) for c in characters]
prompt = (
    f"{char_descs[0]}和{char_descs[1]}在咖啡馆聊天，"
    f"{char_descs[2]}在旁边看书，"
    "都市风格，超高清电影级画质，室内柔光，温馨氛围"
)

print(prompt)
```

### 示例 3：人物系列（连续剧）

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()

# 固定主角
char = generator.generate_unique_character()

scenes = [
    ("在清晨的公园里慢跑", "清新的晨光"),
    ("在办公室里工作", "明亮的办公室灯光"),
    ("在咖啡馆里休息", "温馨的咖啡厅氛围"),
    ("在夜市里逛街", "霓虹灯点缀的夜市"),
    ("在海边看日落", "黄金时刻的暖光")
]

for i, (action, lighting) in enumerate(scenes, 1):
    prompt = (
        f"{generator.format_character_for_prompt(char)}，{action}，"
        "都市风格，超高清电影级画质，"
        f"{lighting}，自然表情"
    )
    print(f"场景 {i}：{prompt}\n")
```

**关键点**：
- 同一人物，5 个场景
- 人物特征完全一致（防止连续剧撞脸）
- 不同场景展现不同侧面

### 示例 4：不同年龄的人物

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()
characters = generator.generate_multiple_characters(5)

for char in characters:
    prompt = (
        f"{generator.format_character_for_prompt(char)}，"
        "在花园里赏花，唯美风格，"
        "超高清电影级画质，自然光线"
    )
    print(f"{char['年龄']}：{prompt}\n")
```

**效果**：
- 覆盖多个年龄段（18-20岁 到 40-45岁）
- 增加视频多样性
- 避免角色同质化

### 示例 5：一致性人物（角色设定）

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()

# 固定主角设定
fixed_character = {
    '脸型': '瓜子脸',
    '眼睛': '杏仁眼',
    '眉毛': '柳叶眉',
    '鼻子': '高鼻梁',
    '嘴唇': '樱桃小嘴',
    '发型': '中长发',
    '发色': '黑色',
    '肤色': '白皙皮肤',
    '年龄': '20-25岁青年',
    '气质': '知性气质',
    '身高': '165cm标准',
    '体型': '匀称健康',
    '服饰风格': '简约时尚'
}

scenes = [
    "在图书馆里看书",
    "在咖啡馆里写东西",
    "在公园里散步",
    "在海边思考",
    "在教室里上课"
]

for scene in scenes:
    # 格式化固定角色
    char_desc = (
        f"一位{fixed_character['年龄']}，{fixed_character['气质']}的女性，"
        f"{fixed_character['脸型']}，{fixed_character['肤色']}，"
        f"{fixed_character['发型']}，{fixed_character['发色']}，"
        f"{fixed_character['眼睛']}，{fixed_character['眉毛']}，"
        f"{fixed_character['鼻子']}，{fixed_character['嘴唇']}，"
        f"{fixed_character['身高']}，{fixed_character['体型']}"
    )

    prompt = (
        f"{char_desc}，{scene}，"
        "文艺风格，超高清电影级画质，自然光线"
    )

    print(f"{prompt}\n")
```

**关键点**：
- 完全固定的角色设定
- 适合连续剧主角
- 确保角色一致性

---

## 🎯 最佳实践

### 1. 连续剧人物一致性
- **问题**：同一角色在不同视频中外貌不一致
- **解决**：使用固定角色设定（示例 5）
- **方法**：创建一个 `fixed_character` 字典，重复使用

### 2. 多角色区分
- **问题**：多个角色撞脸（外貌相似）
- **解决**：使用 `generate_multiple_characters()`
- **方法**：一次生成多个不同角色，自动去重

### 3. 年龄层次丰富
- **问题**：所有角色都是年轻女性
- **解决**：确保年龄多样性
- **方法**：检查生成角色的年龄分布

### 4. 肤色多样性
- **问题**：所有角色都是同一肤色
- **解决**：覆盖 7 种不同肤色
- **方法**：检查生成角色的肤色分布

### 5. 场景适配
- **问题**：人物特征与场景不匹配
- **解决**：使用 `generate_character_for_scene()`
- **方法**：根据场景自动调整风格

---

## 📊 统计信息

运行以下命令查看统计：

```bash
python3 scripts/character_generator.py --stats
```

**输出**：
```
📊 人物特征库统计
============================================================
脸型：9 种
眼睛：9 种
眉毛：8 种
鼻子：8 种
嘴唇：7 种
发型：11 种
发色：10 种
肤色：7 种
年龄：6 种
气质：8 种
身高：5 种
体型：5 种
服饰风格：8 种

组合数量：1,341,204,480
```

---

## 🔧 高级功能

### 1. 排除已生成人物

```python
generator = CharacterGenerator()

# 第一次生成
char1 = generator.generate_unique_character()
print(f"角色 1：{char1['脸型']}")

# 第二次生成（排除角色 1）
char2 = generator.generate_unique_character(exclude=[char1['脸型']])
print(f"角色 2：{char2['脸型']}")
```

### 2. 自定义人物特征

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()

# 创建自定义人物
custom_char = {
    '脸型': '瓜子脸',
    '眼睛': '杏仁眼',
    '眉毛': '柳叶眉',
    '鼻子': '高鼻梁',
    '嘴唇': '樱桃小嘴',
    '发型': '中长发',
    '发色': '黑色',
    '肤色': '白皙皮肤',
    '年龄': '20-25岁青年',
    '气质': '知性气质',
    '身高': '165cm标准',
    '体型': '匀称健康',
    '服饰风格': '简约时尚'
}

# 格式化为提示词
prompt = generator.format_character_for_prompt(custom_char)
print(prompt)
```

### 3. 不同风格适配

```python
from scripts.character_generator import CharacterGenerator

generator = CharacterGenerator()

# 写实风格（适用于电影、短剧）
char_realistic = generator.generate_character_for_scene("都市生活", style="realistic")

# 动漫风格（适用于漫剧）
char_anime = generator.generate_character_for_scene("校园日常", style="anime")

# 奇幻风格（适用于奇幻题材）
char_fantasy = generator.generate_character_for_scene("魔法世界", style="fantasy")
```

---

## 📝 注意事项

1. **特征唯一性**：每次生成的人物特征都是独特的，避免撞脸
2. **去重机制**：自动记录已生成的人物，防止重复
3. **场景适配**：根据场景自动调整人物风格
4. **角色一致性**：连续剧建议使用固定角色设定
5. **多样性**：确保年龄、肤色、气质等多维度多样性

---

## 🎮 使用场景

### 1. 连续剧制作
- 使用固定角色设定
- 确保同一角色在不同场景中特征一致
- 生成 5-10 个场景的提示词

### 2. 短视频制作
- 使用多个人物生成
- 每个短视频使用不同人物
- 确保人物特征差异性

### 3. 电影预告片
- 使用主角 + 配角
- 主角固定设定，配角随机生成
- 突出主角独特性

### 4. 多角色场景
- 一次生成 3-5 个角色
- 确保每个角色特征不同
- 场景中展现多人物互动

---

## 📦 文件结构

```
seedance-2-prompt/
├── scripts/
│   └── character_generator.py          # 人物特征生成器
├── examples/
│   └── anti_collision_characters.py    # 防撞脸示例
└── docs/
    └── ANTI_COLLISION.md             # 本文档
```

---

## 🔄 版本历史

- **v1.0.0** (2026-02-17)
  - 初始版本
  - 13 个维度的人物特征库
  - 去重机制
  - 5 个使用示例

---

## 📞 联系方式

如有问题或建议，请联系 Seedance Team。

---

**Momo 说**："呐呐，这个工具可以帮你防止人物撞脸！🎭
- 13 个维度的人物特征
- 13 亿+ 种组合
- 自动去重
- 支持固定角色设定

**快去试试吧！** 🎯"
