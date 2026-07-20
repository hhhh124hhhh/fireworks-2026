# Video Prompt Generator - Installation & Usage Guide
# 视频提示词生成器 - 安装与使用指南

## 📋 Overview / 概述

Video Prompt Generator is a powerful tool for generating high-quality video prompts with style templates and automatic enhancement. It integrates with XAI Grok Imagine API for direct video generation.
视频提示词生成器是一个强大的工具，用于生成高质量视频提示词，具有风格模板和自动增强功能。它集成 XAI Grok Imagine API 支持直接生成视频。

## ✅ Features / 功能特性

- 🎬 **High-Quality Prompts** - Generate professional video prompts automatically / 自动生成专业视频提示词
- 🎨 **10+ Style Templates** - Landscape, product, tech, emotional, and more / 10+ 种风格模板
- ⚡ **Grok Imagine API** - One-click video generation / 一键生成视频
- 🔄 **Auto Enhancement** - Automatically add lighting, composition, and atmosphere / 自动添加光影、构图和氛围
- 📊 **Batch Generation** - Generate multiple prompt variants at once / 批量生成多个提示词变体
- 💾 **Multiple Formats** - Output in readable, JSON, or Markdown / 多种输出格式

## 📦 Installation / 安装

### Prerequisites / 前置要求

- Python 3.8 or higher
- XAI API Key (for video generation)

### Install Dependencies / 安装依赖

```bash
cd /root/clawd/skills/video-prompt-generator
pip install -r requirements.txt
```

## 🚀 Quick Start / 快速开始

### 1. List Available Styles / 列出可用风格

```bash
python3 main.py --list
```

### 2. Generate Prompts from Topic / 从主题生成提示词

```bash
python3 main.py --topic "一只可爱的猫咪在花园里玩耍" --style "landscape"
```

### 3. Generate Multiple Variants / 生成多个变体

```bash
python3 main.py --topic "产品展示" --style "product" --variants 5
```

### 4. Generate from Keywords / 从关键词生成

```bash
python3 main.py --keywords "可爱,温暖,阳光" --style "emotional"
```

### 5. Output in Different Formats / 不同格式输出

```bash
# JSON format
python3 main.py --topic "测试" --style "landscape" --output json

# Markdown format
python3 main.py --topic "测试" --style "landscape" --output markdown
```

### 6. Save to File / 保存到文件

```bash
python3 main.py --topic "产品展示" --style "product" --output json --file prompts.json
```

## 🎬 Video Generation / 视频生成

### Setup API Key / 设置 API 密钥

```bash
# Method 1: Environment variable (recommended)
export XAI_API_KEY="your-api-key-here"

# Method 2: Command line parameter
python3 main.py --topic "..." --generate-video --api-key "your-api-key"
```

### Generate Video / 生成视频

```bash
python3 main.py \
  --topic "美丽的山景" \
  --style "landscape" \
  --generate-video \
  --duration 5 \
  --aspect-ratio 16:9
```

### Video Parameters / 视频参数

| Parameter / 参数 | Description / 描述 | Range / 范围 |
|----------------|-------------------|---------------|
| `--duration` | Video duration / 视频时长 | 1-15 seconds |
| `--aspect-ratio` | Aspect ratio / 宽高比 | 16:9, 9:16, 4:3, 1:1 |

## 📚 Available Styles / 可用风格

| Style Key / 风格键 | Name / 名称 | Description / 描述 |
|-------------------|-------------|-------------------|
| `landscape` | 风景风光 | 自然风景、城市风光、季节变化 |
| `product` | 产品展示 | 产品特写、使用场景、电商广告 |
| `tech` | 科技未来 | 赛博朋克、未来城市、AI 主题 |
| `emotional` | 情感故事 | 浪漫、怀旧、励志、感人 |
| `urban` | 都市生活 | 街头、办公、咖啡店、都市夜景 |
| `food` | 美食烹饪 | 食物拍摄、烹饪过程、美食特写 |
| `sports` | 运动健身 | 运动场景、健身日常、体育赛事 |
| `traditional` | 古风传统 | 中国风、汉服、古装、古建筑 |
| `anime` | 动漫二次 | 动漫风格、Q版、二次元 |
| `abstract` | 抽象艺术 | 抽象、艺术、创意、实验性 |

## 📖 Usage Examples / 使用示例

### Example 1: Product Video / 示例1: 产品视频

```bash
python3 main.py \
  --topic "新款智能手机产品展示" \
  --style "product" \
  --variants 3 \
  --output json \
  --file product_prompts.json
```

### Example 2: Travel Content / 示例2: 旅游内容

```bash
python3 main.py \
  --topic "美丽的海滩日落" \
  --style "landscape" \
  --variants 5 \
  --output markdown \
  --file travel_prompts.md
```

### Example 3: Tech Video / 示例3: 科技视频

```bash
export XAI_API_KEY="your-api-key"

python3 main.py \
  --topic "AI 机器人与人类协作" \
  --style "tech" \
  --generate-video \
  --duration 10 \
  --aspect-ratio 16:9
```

### Example 4: Food Content / 示例4: 美食内容

```bash
python3 main.py \
  --keywords "美味意大利面,新鲜食材,烹饪过程" \
  --style "food" \
  --variants 5
```

### Example 5: Traditional Style / 示例5: 古风风格

```bash
python3 main.py \
  --topic "汉服美女在古建筑前" \
  --style "traditional" \
  --generate-video \
  --duration 8 \
  --aspect-ratio 9:16
```

## 🧪 Testing / 测试

### Run Test Suite / 运行测试套件

```bash
bash test.sh
```

### Run Example Scripts / 运行示例脚本

```bash
bash examples.sh
```

## 📂 Project Structure / 项目结构

```
video-prompt-generator/
├── SKILL.md           # Skill documentation / 技能文档
├── README.md          # User guide / 用户指南
├── INSTALLATION.md    # This file / 本文件
├── main.py           # Main CLI program / 主程序
├── templates.py       # Style templates / 风格模板
├── grok_client.py    # Grok Imagine API client / API 客户端
├── requirements.txt   # Dependencies / 依赖项
├── test.sh           # Test suite / 测试套件
└── examples.sh       # Example scripts / 示例脚本
```

## 🛠️ Command-Line Reference / 命令行参考

### Input Parameters / 输入参数

```bash
--topic, -t      Video topic / 视频主题
--keywords, -k    Keywords (comma-separated) / 关键词（逗号分隔）
--style, -s       Video style / 视频风格（默认: landscape）
--variants, -v    Number of variants / 变体数量（默认: 1）
```

### Output Parameters / 输出参数

```bash
--output, -o      Format: readable, json, markdown / 格式（默认: readable）
--file, -f        Output to file / 输出到文件
--no-enhance      Disable enhancement / 禁用增强
```

### Video Generation Parameters / 视频生成参数

```bash
--generate-video  Generate video with API / 使用 API 生成视频
--duration, -d    Duration 1-15s / 时长 1-15 秒（默认: 5）
--aspect-ratio, -a Ratio: 16:9, 9:16, 4:3, 1:1 / 宽高比（默认: 16:9）
--api-key         XAI API Key / XAI API 密钥
```

### Tool Parameters / 工具参数

```bash
--list, -l        List all styles / 列出所有风格
--version         Show version / 显示版本
```

## 🎯 Best Practices / 最佳实践

1. **Choose the Right Style** - Match style to your content type / 选择合适的风格，匹配内容类型
2. **Be Specific with Topics** - Provide detailed, descriptive topics / 提供具体、详细的主题
3. **Batch Generate** - Create multiple variants to choose from / 生成多个变体以供选择
4. **Test with Short Videos** - Start with shorter durations (3-5s) for testing / 用较短时长（3-5秒）测试
5. **Use Appropriate Keywords** - Combine keywords with style for best results / 结合关键词和风格获得最佳效果

## 🔍 Troubleshooting / 故障排除

### Issue: API Key Not Found / 问题：找不到 API Key

```bash
# Set environment variable
export XAI_API_KEY="your-api-key-here"
```

### Issue: Style Not Found / 问题：找不到风格

```bash
# List all available styles
python3 main.py --list
```

### Issue: Invalid Duration / 问题：无效时长

```bash
# Duration must be between 1-15 seconds
python3 main.py --topic "..." --generate-video --duration 5
```

## 📖 Documentation / 文档

- **SKILL.md** - Detailed skill documentation with all features / 详细技能文档，包含所有功能
- **README.md** - User guide and usage examples / 用户指南和使用示例

## 🤝 Support / 支持

For detailed documentation, examples, and advanced usage, see `SKILL.md`.
详细文档、示例和高级用法请参见 `SKILL.md`。

## ✨ Tips / 提示

- Use `--list` to see all available styles / 使用 `--list` 查看所有可用风格
- Use `--variants` to generate multiple options / 使用 `--variants` 生成多个选项
- Save prompts to files for later use / 保存提示词到文件以备后用
- Test with short durations before long videos / 在长视频前用短时长测试
- Combine topic and keywords for best results / 结合主题和关键词获得最佳效果

---

**Created with ❤️ for video creators**
**为视频创作者而制作**
