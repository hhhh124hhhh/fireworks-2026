---
name: multimedia-scraper
description: 根据关键词抓取抖音、小红书、微信视频号的热门内容。使用当用户需要：(1) 搜索特定关键词的内容，(2) 抓取多平台热门笔记/视频，(3) 分析关键词的热门内容，(4) 获取抖音/小红书/视频号的爆款内容。
dependency:
  python:
    - requests>=2.25.0
---

# 多媒体抓取工具

一键抓取抖音、小红书、微信视频号的热门内容。

## AI 执行步骤

当用户说 "帮我搜索 XX 关键词" 时：

### 1. 提醒用户配置 API Key

⚠️ **重要提示**：本 Skill 需要第三方 API 支持，请先完成以下配置：

1. **获取 API Key**
   - 访问 TikHub.io 注册账号
   - 在控制台获取 API Key

2. **配置 API Key**
   - 将 API Key 填入 `encrypted_keys.json` 文件（位于 Skill 根目录）
   - 文件格式：
     ```json
     {
       "api_key": "你的API_KEY"
     }
     ```

### 2. 检测 Python 环境

```bash
python --version
```

- 未安装 → 引导安装 Python 3.8+
- 已安装 → 继续

### 3. 执行抓取

```bash
cd scripts && python scrape.py -k "关键词"
```

脚本会自动安装依赖（requests）。

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-k, --keyword` | 搜索关键词（必填） | `-k "AI工具"` |
| `--json` | 输出原始 JSON | `--json` |

## 支持平台

| 平台 | 图标 |
|------|------|
| 抖音 | 🎵 |
| 小红书 | 🔴 |
| 微信视频号 | 📱 |

## 输出格式

```markdown
# 🔥 AI工具 热门内容排行

## 🎵 抖音
🥇 第1名：5.8万赞 🔥🔥🔥
**AI工具推荐：10个必备神器**
👤 小胖讲AI
💬 546 | 🔄 1.5万 | ⭐ 9.3万
🔗 https://www.douyin.com/video/xxx

## 🔴 小红书
🥇 第1名：1.2万赞 🔥🔥🔥
**AI工具测评｜真香警告**
💬 856 | ⭐ 3.4k
🔗 https://xiaohongshu.com/explore/xxx

⏰ 抓取时间：2026-02-25 12:00
```