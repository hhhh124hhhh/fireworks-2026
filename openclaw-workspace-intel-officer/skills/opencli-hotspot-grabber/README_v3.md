# OpenCLI Hotspot Grabber v3.0 使用指南

**版本**: v3.0.0
**架构**: 混合架构（NewsNow + opencli + 缓存）
**创建时间**: 2026-03-23

---

## 🎯 核心特性

| 特性 | 说明 | 状态 |
|------|------|------|
| **混合抓取** | NewsNow（快速）+ opencli（登录态） | ✅ |
| **缓存机制** | 30 分钟默认缓存，减少重复抓取 | ✅ |
| **模块化** | 每个平台独立模块，易维护 | ✅ |
| **智能路由** | 自动选择最佳抓取源 | ✅ |
| **统计信息** | 缓存/平台/抓取器统计 | ✅ |

---

## 📦 目录结构

```
opencli-hotspot-grabber/
├── hotspot_grabber_v3.py      # 主程序 v3.0
├── router.py                  # 智能路由层
├── cache.py                   # 缓存模块
├── fetcher/                   # 平台抓取模块
│   ├── __init__.py
│   ├── newsnow.py             # NewsNow MCP
│   ├── zhihu.py               # 知乎
│   ├── weibo.py               # 微博
│   └── bilibili.py            # B 站
├── hotspot_grabber.py         # 旧版（保留兼容）
└── README.md                  # 本文档
```

---

## 🚀 快速开始

### 基础用法

```bash
# 抓取默认平台（知乎 + 微博+B 站）
python hotspot_grabber_v3.py

# 抓取指定平台
python hotspot_grabber_v3.py -p zhihu weibo bilibili

# 抓取并限制数量
python hotspot_grabber_v3.py -p zhihu -l 20

# 禁用缓存
python hotspot_grabber_v3.py --no-cache

# 安静模式（只输出 JSON）
python hotspot_grabber_v3.py -q
```

### 高级用法

```bash
# 显示统计信息
python hotspot_grabber_v3.py --stats

# 清除缓存
python hotspot_grabber_v3.py --clear-cache

# 清除指定平台缓存
python hotspot_grabber_v3.py --clear-cache -p zhihu

# 输出到指定目录
python hotspot_grabber_v3.py -o output
```

---

## 📊 支持平台

### 已实现

| 平台 | ID | 抓取源 | 缓存时间 |
|------|----|--------|---------|
| 知乎 | `zhihu` | NewsNow → opencli | 30 分钟 |
| 微博 | `weibo` | NewsNow → opencli | 5 分钟 |
| B 站 | `bilibili` | NewsNow → opencli | 30 分钟 |

### 计划中

| 平台 | ID | 优先级 |
|------|----|--------|
| 抖音 | `douyin` | P1 |
| 今日头条 | `toutiao` | P1 |
| 百度热搜 | `baidu` | P1 |
| Hacker News | `hackernews` | P2 |
| GitHub | `github` | P2 |
| V2EX | `v2ex` | P2 |

---

## 🔧 配置说明

### 路由配置（router.py）

```python
ROUTE_CONFIG = {
    'zhihu': {
        'priority': ['newsnow', 'opencli'],  # 优先级
        'cache_ttl': 1800,  # 缓存时间（秒）
    },
    'weibo': {
        'priority': ['newsnow', 'opencli'],
        'cache_ttl': 300,  # 微博更新快，5 分钟
    },
}
```

### 缓存配置（cache.py）

```python
CACHE_TTL = 1800  # 默认 30 分钟
CACHE_TTL_SHORT = 300  # 5 分钟（快速更新平台）
CACHE_TTL_LONG = 3600  # 1 小时（慢速更新平台）

PLATFORM_CACHE_TTL = {
    'zhihu': CACHE_TTL,
    'weibo': CACHE_TTL_SHORT,
    'bilibili': CACHE_TTL,
    # ...
}
```

---

## 📈 性能对比

### v2.0 vs v3.0

| 指标 | v2.0 | v3.0 | 提升 |
|------|------|------|------|
| **首次抓取** | ~10s/平台 | ~3s/平台（NewsNow） | +233% |
| **缓存命中** | ❌ 无 | ~0.1s/平台 | +∞ |
| **代码维护** | 单文件 | 模块化 | +∞ |
| **扩展性** | 低 | 高 | +∞ |

### 缓存效果

```
首次抓取知乎：
  ✅ zhihu: 30 items (NewsNow)
  ⏱️ zhihu: 2.8s

第二次抓取（缓存命中）：
  ✅ zhihu: 从缓存加载 (180s 前)
  ⏱️ zhihu: 0.1s

速度提升：28 倍
```

---

## 🛠️ 开发指南

### 添加新平台

**步骤**:

1. **创建抓取模块** (`fetcher/new_platform.py`):
```python
"""New Platform Fetcher"""

from typing import List, Dict, Optional

def fetch_new_platform(limit: int = 50) -> Optional[List[Dict]]:
    """抓取新平台热点"""
    # 实现抓取逻辑
    items = [...]
    
    # 标准化格式
    for item in items:
        item['platform'] = 'new_platform'
        item['category'] = 'social'
        item['priority'] = 'P0' if i < 20 else 'P1'
        item['source'] = 'opencli'
    
    return items
```

2. **更新路由配置** (`router.py`):
```python
ROUTE_CONFIG = {
    # ...
    'new_platform': {
        'priority': ['newsnow', 'opencli'],
        'cache_ttl': 1800,
    },
}

FETCHERS = {
    # ...
    'new_platform': fetch_new_platform,
}
```

3. **测试**:
```bash
python hotspot_grabber_v3.py -p new_platform
```

---

### 调试技巧

```bash
# 查看详细日志
python -u hotspot_grabber_v3.py -p zhihu

# 禁用缓存调试
python hotspot_grabber_v3.py -p zhihu --no-cache

# 清除缓存后重试
python hotspot_grabber_v3.py --clear-cache
python hotspot_grabber_v3.py -p zhihu
```

---

## 📝 升级说明

### 从 v2.0 升级

**兼容性**: ✅ 完全向后兼容

**旧版命令**:
```bash
python hotspot_grabber.py -p zhihu weibo -o tmp
```

**新版命令**:
```bash
python hotspot_grabber_v3.py -p zhihu weibo -o tmp
```

**变化**:
- ✅ 命令不变
- ✅ 参数不变
- ✅ 输出格式不变
- ✨ 新增缓存支持
- ✨ 新增 NewsNow 支持
- ✨ 性能提升

---

## 🐛 故障排查

### 问题 1: NewsNow 抓取失败

**现象**:
```
⚠️ zhihu: NewsNow 调用失败 - ...
```

**解决**:
1. 检查网络连接
2. 检查 NewsNow 服务状态
3. 自动降级到 opencli

### 问题 2: 缓存不生效

**现象**:
```
每次都是重新抓取，没有缓存命中
```

**解决**:
1. 检查 `cache/` 目录是否存在
2. 检查文件权限
3. 确认未使用 `--no-cache`

### 问题 3: opencli 命令找不到

**现象**:
```
FileNotFoundError: [WinError 2] 系统找不到指定的文件
```

**解决**:
```bash
# 安装 opencli
npm install -g opencli

# 或检查 PATH 环境变量
echo $PATH
```

---

## 📊 统计信息示例

```bash
$ python hotspot_grabber_v3.py --stats

{
  "cache": {
    "count": 5,
    "size": 125000,
    "size_mb": 0.12,
    "platforms": {
      "zhihu": {"count": 2, "size": 50000},
      "weibo": {"count": 2, "size": 50000},
      "bilibili": {"count": 1, "size": 25000}
    }
  },
  "platforms": ["zhihu", "weibo", "bilibili", "douyin"],
  "fetchers": ["zhihu", "weibo", "bilibili"]
}
```

---

## 🎯 最佳实践

### 1. 定时任务配置

```bash
# 每 30 分钟抓取一次（利用缓存）
*/30 * * * * cd /path/to/grabber && python hotspot_grabber_v3.py -q
```

### 2. 多平台并行

```python
# 使用 router 模块
from router import fetch_all_platforms

platforms = ['zhihu', 'weibo', 'bilibili']
results = fetch_all_platforms(platforms, limit=50)
```

### 3. 缓存管理

```bash
# 每天凌晨清除缓存
0 0 * * * python hotspot_grabber_v3.py --clear-cache
```

---

## 📄 许可证

MIT License

---

**创建者**: bot3 (zhuazhua-agent)
**时间**: 2026-03-23 12:37
