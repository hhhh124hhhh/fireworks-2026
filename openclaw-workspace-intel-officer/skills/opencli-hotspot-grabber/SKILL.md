# OpenCLI Hotspot Grabber - 全域热点抓取 Skill

## 描述

基于 OpenCLI 的全域热点抓取工具，支持 9 个平台的技术趋势、内容素材和社会热点采集。

**版本**: 1.0.0  
**依赖**: `opencli` (npm), `python3`  
**GitHub**: https://github.com/jackwener/opencli

---

## 🎯 核心能力

### 技术趋势 (P0 优先级)
- **Hacker News** - 科技热门（30 条）
- **GitHub Trending** - 开源项目（20 条）
- **V2EX** - 开发者话题（30 条）
- **arXiv** - AI 论文（15 条）

### 内容素材 (P1 优先级)
- **B 站** - 热门视频（20 条）
- **小红书** - AI 种草（20 条）
- **雪球** - 热门股票（20 条）
- **知乎** - 深度讨论（30 条）

### 社会热点 (P2 优先级)
- **微博** - 热搜榜单（50 条）

**总计**: 235 条全域热点

---

## 🔧 使用方法

### ✅ 推荐：Python 脚本（主入口）
```bash
# 抓取所有平台
python skills/opencli-hotspot-grabber/hotspot_grabber.py

# 指定平台
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p hackernews v2ex arxiv

# 指定输出目录
python skills/opencli-hotspot-grabber/hotspot_grabber.py -o tmp/hotspots

# 安静模式（适合定时任务）
python skills/opencli-hotspot-grabber/hotspot_grabber.py -q

# 组合使用
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p hackernews v2ex -o tmp/tech -q
```

### ⚠️ 可选：PowerShell 封装（不推荐，可能有编码问题）
```powershell
# 完整抓取
powershell -File skills/opencli-hotspot-grabber/run-grabber.ps1

# 指定平台
powershell -File skills/opencli-hotspot-grabber/run-grabber.ps1 -Platforms hackernews,v2ex
```

### ✅ 定时任务配置示例
```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "python skills/opencli-hotspot-grabber/hotspot_grabber.py -o tmp -q"
  }
}
```

---

## 📤 输出格式

```json
{
  "timestamp": "2026-03-21 18:00:00",
  "platforms": {
    "hackernews": {
      "count": 30,
      "items": [
        {
          "rank": 1,
          "title": "Show HN: ...",
          "url": "https://...",
          "score": 123,
          "comments": 45,
          "platform": "hackernews",
          "category": "tech",
          "priority": "P0"
        }
      ]
    }
  },
  "summary": {
    "total": 235,
    "hackernews": 30,
    "github": 20,
    ...
  },
  "errors": []
}
```

---

## 🤖 Bot 使用场景

### bot4 (情报官 - intel-officer)
```python
# 每日全域热点采集
python skills/opencli-hotspot-grabber/hotspot_grabber.py -o tmp -q

# 输出：tmp/opencli-hotspots-YYYYMMDD-HHMMSS.json
# 用途：写入飞书多维表格「热门内容素材」表
```

### bot2 (内容创作 - content-lite)
```python
# 技术类选题素材
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p hackernews github v2ex -o tmp/tech

# 用途：公众号文章选题
```

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| **抓取平台** | 8 个 |
| **总数据量** | 215 条 |
| **总耗时** | ~60-90 秒 |
| **技术内容占比** | 40%+ |
| **P0 选题产出** | 5-8 个/天 |

**平台数据量明细:**
- Hacker News: 30 条 (P0)
- V2EX: 30 条 (P0)
- arXiv: 15 条 (P0)
- B 站：20 条 (P1)
- 小红书：20 条 (P1)
- 雪球：20 条 (P1)
- 知乎：30 条 (P1)
- 微博：50 条 (P2)

---

## ⚠️ 注意事项

1. **依赖安装**:
   ```bash
   # 1. 安装 OpenCLI (npm)
   npm install -g @jackwener/opencli
   
   # 2. Python 无需额外依赖（仅使用标准库）
   # 要求：Python 3.8+
   ```

2. **浏览器桥接**: OpenCLI 需要 Chrome 扩展支持
   ```bash
   opencli doctor  # 诊断连接
   ```

3. **超时设置**: 默认 30 秒/平台，可通过 `-t` 调整
   ```bash
   python skills/opencli-hotspot-grabber/hotspot_grabber.py -t 60
   ```

4. **错误处理**: 单个平台失败不影响其他平台

5. **编码问题**: 
   - ✅ Python 脚本已处理 Windows 编码问题
   - ⚠️ PowerShell 脚本可能有编码问题，不推荐使用

---

## 🚀 快速测试

```bash
# 测试单个平台
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p hackernews -q

# 验证输出
cat tmp/opencli-hotspots-*.json | jq '.summary'
```

---

## 📝 更新日志

- **v1.0.0** (2026-03-21) - 初始版本，支持 9 个平台

---

**创建日期**: 2026-03-21  
**维护者**: intel-officer
