# Grok Imagine 视频演示页面

集成 Grok Imagine API 生成视频并在网页上播放。

## 快速开始

### 1. 安装依赖

```bash
cd /root/clawd/skills/grok-imagine
pip install httpx
```

### 2. 配置 API Key

```bash
export XAI_API_KEY="your_api_key_here"
```

### 3. 生成视频

```bash
# 生成 10 秒视频（16:9, 720p）
python3 grok-imagine.py video "A cat playing with a ball in a sunny garden" --duration 10

# 生成 15 秒视频（4:3, 720p）
python3 grok-imagine.py video "Beautiful sunset over ocean with seagulls flying" --duration 15 --aspect-ratio 4:3
```

### 4. 在网页上播放

将生成的视频 URL 复制到 `grok-imagine.html` 的视频源中即可播放。

## 视频参数

- **duration**: 视频时长（秒，1-15）
- **aspect_ratio**: 宽高比
  - `16:9` - 全高清（默认）
  - `4:3` - 标准宽屏
  - `1:1` - 正方形
  - `9:16` - 竖屏
  - `3:4` - 竖向标准
- **resolution**: 分辨率
  - `720p` - 高清（默认）
  - `480p` - 标准

## 使用示例

### 示例 1：风景视频

```bash
python3 grok-imagine.py video "A serene mountain lake at sunrise with mist rolling over the water" --duration 10
```

### 示例 2：动物视频

```bash
python3 grok-imagine.py video "A golden retriever puppy playing in autumn leaves" --duration 8
```

### 示例 3：科技视频

```bash
python3 grok-imagine.py video "Futuristic city with flying cars and holographic billboards" --duration 12
```

### 示例 4：产品展示

```bash
python3 grok-imagine.py video "Professional product video of a sleek smartphone on a marble surface" --duration 15 --aspect-ratio 1:1
```

## API 文档

- [xAI API 文档](https://docs.x.ai/docs/guides/video-generation)
- [模型和定价](https://docs.x.ai/docs/models)

## 相关技能

- [vap-media](../vap-multimedia-generation/) - 多媒体生成工具
- [ai-video-gen](../ai-video-gen/) - AI 视频生成
- [nano-banana-pro](../nano-banana-pro/) - 图像生成

---

**Made with ❤️ by Momo**
