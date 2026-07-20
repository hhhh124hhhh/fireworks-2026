# 🚨 核心规则 - 热点抓取标准流程

**固化日期:** 2026-03-21  
**优先级:** ⭐⭐⭐⭐⭐ (最高)  
**P0 标准:** 已按最新要求调整

---

## 📌 P0 选题标准（最新）

### 早上 08:30
| 来源 | 权重 | 筛选标准 | 优先级 | 状态 |
|------|------|---------|--------|------|
| **知乎热榜** | 50% | TOP20 | P0 | ✅ |
| **微博热搜** | 20% | TOP30 | P0 | ✅ |
| **Hacker News** | 15% | Top30 | P0 | ✅ |
| **GitHub Trends** | 15% | Trending | P0 | ⚠️ 待补充 |

### 下午 15:05
| 来源 | 权重 | 筛选标准 | 优先级 | 状态 |
|------|------|---------|--------|------|
| **知乎热榜** | 60% | TOP20 | P0 | ✅ |
| **微博热搜** | 30% | TOP30 | P0 | ✅ |
| **抖音热榜** | 10% | Top50 | P1 | ✅ |

### 晚上 21:00
- **深度研究** - 保持现状

---

## 🔧 标准命令

```bash
# 晨间抓取 (08:15)
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo hackernews -o tmp -q

# 下午抓取 (14:55)
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p zhihu weibo douyin -o tmp -q

# 夜间抓取 (02:00)
python skills/opencli-hotspot-grabber/hotspot_grabber.py -p hackernews v2ex -o tmp -q
```

---

## 📊 优先级标记规则

### 知乎
```python
zhihu[0:20] → P0  # 前 20 名 (50%/60% 权重)
zhihu[21:30] → P1
```

### 微博
```python
weibo[0:30] → P0  # 前 30 名 (20%/30% 权重)
weibo[31:50] → P2
```

### 抖音
```python
douyin[0:50] → P1  # 全部 P1 (10% 权重)
```

### Hacker News
```python
hackernews[0:30] → P0  # 全部 P0 (15% 权重)
```

---

## 📁 输出位置

```
tmp/opencli-hotspots-YYYYMMDD-HHMMSS.json
```

**示例:**
```
tmp/opencli-hotspots-20260322-0815.json  # 晨间
tmp/opencli-hotspots-20260322-1455.json  # 下午
tmp/opencli-hotspots-20260322-0200.json  # 夜间
```

---

## 🔄 数据流向

```
08:15 抓取 → 知乎 (30) + 微博 (50) + HN (30)
   ↓
P0 筛选 → 知乎前 20 + 微博前 30 + HN 全部
   ↓
08:30 分析 + 写入选题池 → 推送到咨讯群
   ↓
14:55 抓取 → 知乎 (30) + 微博 (50) + 抖音 (50)
   ↓
P0 筛选 → 知乎前 20 + 微博前 30
   ↓
15:05 分析 + 更新选题池 → 推送到咨讯群
```

---

## ⏰ 定时任务

| 时间 | 任务 | 平台 | P0 产出 |
|------|------|------|--------|
| **02:00** | 夜间海外技术 | Hacker News + V2EX | ~40 条 |
| **08:15** | 晨间热点 | 知乎 + 微博 + HN | ~80 条 |
| **08:30** | 晨间分析 | 写入选题池 + 推送 | - |
| **14:55** | 下午热点 | 知乎 + 微博 + 抖音 | ~70 条 |
| **15:05** | 下午分析 | 更新选题池 + 推送 | - |
| **21:00** | 心跳检查 | - | - |

**每日 P0 总计:** ~190 条

---

## ⚠️ 注意事项

1. **依赖检查**
   ```bash
   opencli --version  # 应返回 1.1.1+
   python --version   # 应返回 3.8+
   ```

2. **诊断命令**
   ```bash
   opencli doctor  # 检查浏览器桥接
   ```

3. **错误处理**
   - 单个平台失败不影响其他平台
   - 查看 `tmp/opencli-hotspots-*.json` 中的 `errors` 字段

4. **编码问题**
   - ✅ Python 脚本已处理 Windows 编码
   - ⚠️ 避免使用 PowerShell 直接调用

---

## ✅ 验证清单

- [ ] `opencli` 已安装 (`opencli --version`)
- [ ] Python 3.8+ 已安装
- [ ] Skill 已注册 (`.openclaw/skills/.skills_store_lock.json`)
- [ ] 知乎前 20 名标记 P0
- [ ] 微博前 30 名标记 P0
- [ ] 抖音热榜已添加
- [ ] 定时任务已更新

---

**最后更新:** 2026-03-21 19:58  
**维护者:** intel-officer
