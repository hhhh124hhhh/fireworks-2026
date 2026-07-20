# Hotspot Grabber v3.0 - 热点采集器

**bot4 (intel-officer) 热点采集模块**

---

## 🚀 快速开始

```bash
cd workspace-intel-officer/skills/opencli-hotspot-grabber

# 测试单个平台
python -c "from router import fetch_platform; items = fetch_platform('zhihu', limit=5); print(f'{len(items)} items')"

# 测试多平台
python -c "from router import fetch_all_platforms; results = fetch_all_platforms(['zhihu', 'weibo', 'bilibili'], limit=5)"

# 清除缓存
python -c "from cache import clear_cache; clear_cache()"
```

---

## 📋 架构设计

### 三层架构

```
用户请求
  ↓
Router (智能路由)
  ├─ 优先级 1: NewsNow MCP
  └─ 优先级 2: opencli (Chrome 登录态)
  ↓
Cache (缓存层)
  ↓
结果返回
```

### 核心模块

| 模块 | 文件 | 职责 |
|------|------|------|
| **Router** | `router.py` | 智能路由，优先级调度 |
| **Cache** | `cache.py` | 磁盘缓存，减少重复抓取 |
| **Fetchers** | `fetcher/*.py` | 平台专用抓取器 |
| **Config** | `config/mcporter.json` | MCP Server 配置 |

---

## 🔧 配置

### 1. MCP Server 配置

**文件**: `workspace-intel-officer/config/mcporter.json`

```json
{
  "mcpServers": {
    "newsnow": {
      "command": "npx",
      "args": ["-y", "newsnow-mcp@latest"],
      "description": "NewsNow MCP Server - 全网热点抓取"
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest", "--browser-url=http://127.0.0.1:9222", "--slim"]
    }
  }
}
```

### 2. opencli 配置

**自动启动 Chrome**: 已配置到 `C:\nvm4w\nodejs\opencli.ps1`

**验证**:
```bash
opencli doctor
opencli bilibili hot --limit 5
```

---

## 📊 支持的平台

### 双源支持（NewsNow + opencli）

| 平台 | NewsNow | opencli | 实际使用 |
|------|---------|---------|---------|
| 知乎 | ✅ | ✅ | opencli |
| 微博 | ✅ | ✅ | opencli |
| B 站 | ✅ | ✅ | opencli |
| 抖音 | ✅ | ⚠️ | opencli |
| 今日头条 | ✅ | ⚠️ | opencli |
| 百度 | ✅ | ✅ | opencli |
| V2EX | ✅ | ✅ | opencli |
| Hacker News | ✅ | ✅ | opencli |

### 仅 opencli 支持

| 平台 | 命令 |
|------|------|
| Reddit | `opencli reddit hot` |
| Twitter | `opencli twitter trending` |
| YouTube | `opencli youtube search` |
| 小红书 | `opencli xiaohongshu feed` |

---

## 🧪 测试

### 单元测试

```bash
# 测试缓存模块
python cache.py

# 测试知乎抓取器
python fetcher/zhihu.py

# 测试微博抓取器
python fetcher/weibo.py

# 测试 B 站抓取器
python fetcher/bilibili.py

# 测试 NewsNow 抓取器
python fetcher/newsnow.py

# 测试路由器
python router.py
```

### 集成测试

```bash
# 测试单平台
python -c "from router import fetch_platform; print(fetch_platform('zhihu', limit=5))"

# 测试多平台
python -c "from router import fetch_all_platforms; print(fetch_all_platforms(['zhihu', 'weibo', 'bilibili']))"

# 测试缓存统计
python -c "from cache import get_cache_stats; print(get_cache_stats())"
```

---

## 📈 性能指标

| 指标 | 目标 | 实际 |
|------|------|------|
| **单平台抓取时间** | <10s | ~3-6s (opencli) |
| **缓存命中率** | >80% | 取决于调用频率 |
| **缓存 TTL** | 5-60 分钟 | 可配置 |
| **支持平台数** | 20+ | 44+ (opencli) |

---

## 🔍 故障排查

### 1. opencli 不可用

```bash
# 检查 opencli 是否安装
where opencli

# 检查 Chrome 调试模式
opencli doctor

# 启动 Chrome 调试模式
opencli bilibili hot  # 会自动启动
```

### 2. NewsNow API 不可用

**状态**: 已废弃（2026-03-24）

**原因**: API 返回 HTML 而非 JSON

**解决**: 自动降级到 opencli

### 3. 缓存问题

```bash
# 查看缓存统计
python -c "from cache import get_cache_stats; print(get_cache_stats())"

# 清除缓存
python -c "from cache import clear_cache; clear_cache()"
```

### 4. 编码问题

所有打印语句已改为 ASCII，避免 Windows GBK 编码问题。

---

## 📝 更新日志

### v3.0.0 (2026-03-24)

- ✅ 配置 NewsNow MCP Server
- ✅ NewsNow API 废弃，降级到 opencli
- ✅ 修复 Windows 编码问题
- ✅ 添加自动降级逻辑
- ✅ 优化缓存机制
- ✅ 添加迁移报告

### v2.0.0 (2026-03-23)

- ✅ 集成 NewsNow API
- ✅ 混合抓取策略
- ✅ 添加缓存层

### v1.0.0 (2026-03-22)

- ✅ 初始版本
- ✅ opencli 集成

---

## 📚 相关文档

- [NewsNow 迁移报告](NEWSNOW-MIGRATION.md)
- [opencli 技能文档](../../opencli/SKILL.md)
- [MCP 配置](../../config/mcporter.json)

---

**维护者**: bot4 (intel-officer) + bot3 (zhuazhua-agent)  
**最后更新**: 2026-03-24
