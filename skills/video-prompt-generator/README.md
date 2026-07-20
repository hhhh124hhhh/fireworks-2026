# 视频提示词生成器 | Video Prompt Generator

AI 驱动的高质量视频提示词生成工具，集成 Grok Imagine API 直接生成视频。

## ✨ 特性 Features

- 🎬 **10+ 视频风格** - 风景、产品、科技、情感、都市、美食、运动、古风、动漫、抽象
- ⚡ **Grok Imagine API** - 一键生成视频
- 📚 **历史记录管理** - 自动保存到 localStorage
- 🔍 **实时搜索过滤** - 按关键词和分类筛选
- 📄 **多种导出格式** - JSON 和 Markdown 格式
- 🌐 **完整的 Web UI** - 浏览器界面直接操作
- ⚙️ **视频参数配置** - 时长、宽高比、分辨率自定义

## 🚀 快速开始 Quick Start

### 1. 环境配置 Setup

```bash
# 安装 Grok Imagine 依赖
cd /root/clawd/skills/grok-imagine
pip install -r requirements.txt

# 设置 API Key
export XAI_API_KEY="your_xai_api_key"
```

### 2. 启动 API 服务器 Start API Server

```bash
cd /root/clawd/skills/video-prompt-generator
node generate.js --server --port 3000
```

### 3. 打开 Web UI Open Web Interface

在浏览器中打开：
```
file:///tmp/hhhh124hhhh.github.io/video-prompt-generator.html
```

### 4. 开始使用 Start Creating

1. 输入主题（如："猫咪玩耍"）
2. 选择分类（可多选）
3. 点击"生成提示词"
4. 点击"生成视频"创建视频
5. 查看结果或导出

## 📖 使用指南 Usage Guide

### Web UI 功能 Web UI Features

#### 生成提示词 Generate Prompts
- 在主题输入框中输入您的视频主题
- 选择一个或多个分类
- 可选：添加增强效果（灯光、镜头、情绪、技术参数）
- 点击"生成提示词"按钮

#### 历史记录 History
- 所有生成的提示词自动保存到浏览器
- 点击历史记录项可重新加载
- 使用搜索框搜索历史
- 使用分类标签过滤
- 点击垃圾桶图标清除历史

#### 生成视频 Generate Video
- 在提示词卡片上点击"生成视频"按钮
- 配置视频参数：
  - **时长**: 3、5、10、15 秒
  - **宽高比**: 16:9（横屏）、4:3（标准）、1:1（方形）、9:16（竖屏）
  - **分辨率**: 720p（高清）或 480p（标清）
- 点击"开始生成"
- 等待生成完成，查看视频链接

#### 导出功能 Export

**导出当前提示词:**
- **JSON**: 结构化数据，便于程序使用
- **Markdown**: 人类可读格式，包含格式化

**导出历史记录:**
- **JSON**: 所有历史记录
- **Markdown**: 完整历史，包含所有提示词

#### 复制功能 Copy
- 复制单个提示词：点击提示词卡片的"复制"按钮
- 复制全部提示词：点击"复制全部"按钮

### 命令行模式 CLI Mode

#### 交互模式 Interactive
```bash
node generate.js --interactive
```

#### 命令行模式 Command Line
```bash
# 生成所有分类的提示词
node generate.js --topic "cat playing" --all

# 生成特定分类
node generate.js --topic "sunset" --categories "landscape,emotional"

# 添加增强效果
node generate.js --topic "product" \
  --lighting "golden hour" \
  --camera "slow zoom" \
  --mood "cinematic"

# 直接生成视频
node generate.js --topic "cat" \
  --style "Serene Mountain Sunrise" \
  --generate-video \
  --duration 10 \
  --aspect-ratio 16:9
```

## 🎨 视频分类 Categories

### 🌄 风景 Landscape
宁静山岳日出、海上落日无人机拍摄、森林树冠漫步、城市延时摄影、樱花季节

### 📦 产品 Product
电影级产品展示、生活方式产品使用、电商平面拍摄、爆炸视图动画、开箱体验

### 🤖 科技 Tech
赛博朋克霓虹城市、AI 数字界面、太空站视角、数字故障艺术、未来实验室

### 💖 情感 Emotional
浪漫月光场景、怀旧胶片、鼓舞人心的旅程、苦乐参半的告别、庆祝和欢乐

### 🏙 都市 Urban
街边咖啡厅清晨、现代办公室工作空间、夜城漫步、地铁通勤、屋顶城市景观

### 🍜 美食 Food
食品准备特写、烹饪过程、摆盘展示、从农场到餐桌、美食美学

### 🏃 运动 Sports
动态体育动作、健身房锻炼日常、户外冒险、瑜伽和冥想、团队精神

### 🏛️ 古风 Ancient
中国传统园林、汉服服装展示、水墨画风格、古建筑、武侠武术

### 🎨 动漫 Anime
动漫开场风格、卡哇伊角色、奇幻校园生活、机甲机器人战斗、魔法少女变身

### 🎭 抽象 Abstract
液体抽象艺术、几何图案、粒子爆炸、水墨入水、分形缩放

## 💡 提示词增强 Enhancements

### 灯光 Lighting
- **Golden Hour** - 温暖柔和的阳光
- **Soft Lighting** - 柔和漫射光
- **Dramatic Shadows** - 高对比度光线
- **Neon Lights** - 彩色人造光

### 镜头 Camera
- **Slow Zoom** - 缓慢变焦
- **Pan Left/Right** - 水平移动
- **Drone Shot** - 航拍视角
- **Tracking Shot** - 跟随拍摄

### 情绪 Mood
- **Cinematic** - 电影质感
- **Dreamy** - 梦幻空灵
- **Energetic** - 动感活力
- **Mysterious** - 神秘诱人

### 技术 Technical
- **4K Quality** - 超高清
- **8K Quality** - 极高分辨率
- **Slow Motion** - 慢动作
- **Hyper-detailed** - 超精细纹理

## 🎯 使用示例 Examples

### 社交媒体内容 Social Media
```bash
# Instagram Reel (9:16 竖屏)
# 使用 Web UI 或命令行
node generate.js --topic "服装展示" \
  --style "Lifestyle Product Usage" \
  --lighting "golden hour" \
  --camera "slow zoom" \
  --generate-video \
  --aspect-ratio 9:16 \
  --duration 15
```

### 产品广告 Product Ad
```bash
# 电商产品视频
node generate.js --topic "智能手机" \
  --style "Cinematic Product Reveal" \
  --mood "premium" \
  --technical "4K quality" \
  --generate-video \
  --aspect-ratio 16:9 \
  --duration 10
```

### 故事视频 Storytelling
```bash
# 情感叙事
node generate.js --topic "成长" \
  --style "Inspiring Journey" \
  --lighting "warm soft" \
  --mood "cinematic" \
  --generate-video \
  --duration 15
```

### 艺术项目 Art Project
```bash
# 抽象艺术视频
node generate.js --topic "液体艺术" \
  --style "Liquid Abstract Art" \
  --technical "slow motion" \
  --mood "dreamy" \
  --generate-video
```

## 🛠️ API 服务器 API Server

### 启动服务器 Start Server
```bash
node generate.js --server --port 3000
```

### 端点 Endpoints

#### POST /api/generate-video
生成视频

**请求:**
```json
{
  "prompt": "您的视频提示词",
  "duration": 5,
  "aspectRatio": "16:9",
  "resolution": "720p"
}
```

**响应:**
```json
{
  "success": true,
  "url": "https://video-url-here",
  "prompt": "...",
  "duration": 5,
  "aspectRatio": "16:9",
  "resolution": "720p"
}
```

#### GET /api/status
检查服务状态

**响应:**
```json
{
  "status": "running",
  "service": "Video Prompt Generator API",
  "version": "2.0.0",
  "features": ["prompt-generation", "video-generation", "history", "search", "export"]
}
```

## 📋 输出格式 Output Formats

### JSON 导出
结构化 JSON 数据：
```json
{
  "topic": "sunset",
  "categories": ["landscape"],
  "generatedAt": "2026-02-04T00:00:00.000Z",
  "promptCount": 5,
  "prompts": [
    {
      "category": "landscape",
      "style": "Serene Mountain Sunrise",
      "prompt": "Cinematic video of sunset..."
    }
  ]
}
```

### Markdown 导出
格式化的 Markdown 文档，包含：
- 主题和生成信息
- 每个提示词的代码块
- 正确的标题层级
- 提示词之间的分隔符

## 🐛 故障排除 Troubleshooting

### Grok Imagine API 不工作
- 检查 `XAI_API_KEY` 是否正确设置
- 确认 Grok Imagine 依赖已安装
- 检查网络连接到 x.ai
- API 服务器是否正在运行

### 提示词生成问题
- 主题太泛泛 → 更具体一些
- 风格不匹配 → 选择合适的分类
- 增强效果过多 → 保持简单

### 视频生成失败
- API 速率限制 → 等待重试
- 无效提示词 → 检查格式
- 余额不足 → 检查 x.ai 账户
- 服务器未运行 → 启动 API 服务器

### Web UI 视频生成
- 确保 API 服务器正在运行
- 检查浏览器控制台错误
- 验证与 localhost:3000 的网络连接

### 历史记录未保存
- 检查浏览器是否支持 localStorage
- 确认未阻止 cookies/localStorage
- 尝试清除浏览器缓存

## 💡 最佳实践 Best Practices

1. **具体化** - 使用详细的主题（如："带红球玩耍的猫" vs "猫"）
2. **匹配风格** - 为主题选择合适的分类
3. **适度增强** - 最多添加 2-3 个增强效果
4. **测试变体** - 生成多个版本并选择最佳
5. **审查提示词** - 生成视频前阅读提示词
6. **使用历史** - 保存和重用成功的提示词
7. **定期导出** - 导出历史记录作为备份

## 📊 API 成本 API Costs

Grok Imagine API 定价（截至 2026）：
- **视频生成**: ~$0.04-0.08 每秒
- **分辨率**: 720p 基础，1080p 高级
- **音频**: 包含（与视频同步）

查看最新定价：https://x.ai/docs/models

## 🔗 集成 Integration

此技能集成了：
- **Grok Imagine** - `/root/clawd/skills/grok-imagine` - 视频生成 API
- **ad-creative-generator** - `/root/clawd/skills/ad-creative-generator` - 原始广告提示词
- **prompt-craft** - `/root/clawd/skills/prompt-craft` - 提示词优化

## 📄 许可证 License

MIT License

## 📝 版本历史 Version History

### v2.0.0 (2026-02-04)
- ✅ 历史记录管理（localStorage）
- ✅ 实时搜索和过滤
- ✅ 导出为 JSON 和 Markdown
- ✅ 完整的 Web UI
- ✅ 从 Web UI 直接生成视频
- ✅ API 服务器用于后端集成
- ✅ 视频参数配置
- ✅ 复制单个和全部提示词

### v1.0.0 (2026-02-04)
- ✅ 初始版本
- ✅ 10 个视频分类，每类 5 种风格
- ✅ Grok Imagine API 集成
- ✅ 交互和命令行模式
- ✅ 提示词增强系统
- ✅ JSON 导出支持
- ✅ 批量生成

## 📞 联系与支持 Contact & Support

如有问题或疑问：
- 查看本文档
- 测试 Grok Imagine API
- 检查浏览器控制台（Web UI 问题）
- 审查生成的提示词

---

**Made with ❤️ by Momo**
