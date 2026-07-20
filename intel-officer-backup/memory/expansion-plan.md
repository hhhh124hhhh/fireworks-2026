# 扩源计划 - Intel Officer

## 🎯 目标

扩展热点来源，解决"连续两天热点已写，今日热点不够"的问题。

---

## 📊 当前状态（2026-03-26）

### 已有平台（稳定运行）
| 平台 | 数量 | 优先级 | 登录态 | 状态 |
|------|------|--------|--------|------|
| 知乎 | 30 | P0 (前 20) | ❌ 无需 | ✅ |
| 微博 | 50 | P0 (前 30) | ❌ 无需 | ✅ |
| 百度 | 30 | P0 | ❌ 无需 | ✅ |
| Hacker News | 30 | P0 | ❌ 无需 | ✅ |
| V2EX | 10 | P0 | ❌ 无需 | ✅ |
| 抖音 | 50 | P1 | ❌ 无需 | ✅ |
| B 站 | 20 | P1 | ❌ 无需 | ✅ |
| 小红书 | 14 | P1 | ❌ 无需 | ✅ |
| 雪球 | 20 | P1 | ❌ 无需 | ✅ |

**总计：** ~260 条/次

---

## 🆕 扩源平台（新增）

### 第一阶段（2026-03-26 ~ 04-01）- 技术向

| 平台 | 预期数量 | 优先级 | 登录态 | 实现方式 | 状态 |
|------|---------|--------|--------|---------|------|
| **GitHub Trending** | 30 | P0 | ❌ 无需 | Chrome DevTools (CDP 9222) | 🔄 进行中 |
| **Product Hunt** | 20 | P1 | ❌ 无需 | Chrome DevTools | 🔄 待实现 |
| **Reddit r/ArtificialIntelligence** | 20 | P1 | ✅ 需要 | opencli (需登录) | ⚠️ 需登录 |

**预期增量：** +70 条/次

### 第二阶段（2026-04-01 ~ 04-07）- 社交向

| 平台 | 预期数量 | 优先级 | 登录态 | 实现方式 | 状态 |
|------|---------|--------|--------|---------|------|
| **Twitter/X Trending** | 20 | P1 | ✅ 需要 | opencli (需登录) | ⚠️ 需登录 |
| **即刻首页** | 20 | P1 | ✅ 需要 | opencli jike feed | 🔄 待测试 |

**预期增量：** +40 条/次

### 第三阶段（2026-04-07 ~ 04-14）- 深度向

| 平台 | 预期数量 | 优先级 | 登录态 | 实现方式 | 状态 |
|------|---------|--------|--------|---------|------|
| **arXiv AI 论文** | 15 | P1 | ❌ 无需 | arXiv API | 🔄 待实现 |
| **微信公众号 AI 垂类** | 20 | P1 | ✅ 需要 | Chrome DevTools | 🔄 待实现 |

**预期增量：** +35 条/次

---

## 🛠️ 实现方案

### GitHub Trending（优先级最高）

**方案：** Chrome DevTools (CDP 9222) 抓取

```python
def grab_github_chrome(self, limit: int = 30):
    """使用 Chrome DevTools 抓取 GitHub Trending"""
    url = "https://github.com/trending"
    # 1. CDP 创建新标签页
    # 2. 等待页面加载
    # 3. 获取页面 HTML
    # 4. 解析 trending repos
    # 5. 关闭标签页
```

**解析逻辑：**
- 标题：repo 名称
- 描述：repo description
- 链接：repo URL
- 星标：star count
- 语言：primary language

**状态：** 🔄 代码已更新，待测试

---

### Product Hunt

**方案：** Chrome DevTools 抓取

```python
def grab_producthunt_chrome(self, limit: int = 20):
    """使用 Chrome DevTools 抓取 Product Hunt 今日产品"""
    url = "https://www.producthunt.com/"
    # 类似 GitHub 流程
```

**状态：** 🔄 待实现

---

### Twitter/X（需要登录态）

**方案：** opencli（依赖 Chrome 已登录 Cookie）

```bash
opencli twitter trending --limit 20 -f json
```

**状态：** ⚠️ 需要验证 Chrome 是否已登录 Twitter

---

### Reddit（需要登录态）

**方案：** opencli（依赖 Chrome 已登录 Cookie）

```bash
opencli reddit hot --limit 20 -f json
```

**状态：** ⚠️ 需要验证 Chrome 是否已登录 Reddit

---

## 📋 定时任务调整

### 当前抓取任务

| 时间 | 任务 | 平台 |
|------|------|------|
| 08:15 | Morning Hotspots | 知乎 + 微博 + 百度 + HN |
| 14:55 | Afternoon Hotspots | 知乎 + 微博 + 百度 + 抖音 |
| 02:00 | Night Tech Tracker | HN + V2EX |

### 扩源后调整（建议）

**方案 A：保持现有任务，新增独立任务**
```
08:00 - GitHub Trending + Product Hunt (技术向)
14:45 - Twitter + Reddit (社交向)
```

**方案 B：扩展现有任务**
```
08:15 - 知乎 + 微博 + 百度 + HN + GitHub + Product Hunt
14:55 - 知乎 + 微博 + 百度 + 抖音 + Twitter + Reddit
```

**推荐：** 方案 A（独立任务，便于监控和调试）

---

## 🔍 心跳检查升级

### 当前检查项
1. Chrome CDP 9222 是否响应
2. tmp/opencli-hotspots-*.json 是否存在
3. 定时任务是否执行
4. 共享选题池是否更新

### 新增检查项（扩源后）

1. **opencli 可用性**
   ```powershell
   opencli --version
   ```

2. **gh CLI 可用性**
   ```powershell
   gh auth status
   ```

3. **Chrome 登录态检查**
   - Twitter: 访问 `twitter.com/home` 检查是否登录
   - Reddit: 访问 `reddit.com` 检查是否登录
   - Product Hunt: 访问 `producthunt.com` 检查是否登录

4. **扩源平台数据 freshness**
   - GitHub: tmp/github-trending-*.json
   - Product Hunt: tmp/producthunt-*.json
   - Twitter: tmp/twitter-trending-*.json

---

## 📈 预期效果

### 热点供给对比

| 阶段 | 每日热点总量 | AI 相关估算 | 可用选题 |
|------|------------|-----------|---------|
| **当前** | ~260 条 | ~80 条 | ~20 条 |
| **第一阶段后** | ~330 条 | ~110 条 | ~30 条 |
| **第三阶段后** | ~405 条 | ~150 条 | ~40 条 |

### 选题多样性提升

- **技术深度：** GitHub + Product Hunt + arXiv
- **社交热度：** Twitter + Reddit + 即刻
- **本土视角：** 知乎 + 微博 + 百度 + 抖音

---

## ✅ 下一步行动

### 本周（2026-03-26 ~ 04-01）
1. ✅ 实现 GitHub Trending 抓取（Chrome DevTools）
2. ✅ 实现 Product Hunt 抓取（Chrome DevTools）
3. ✅ 测试 Twitter/Reddit opencli（验证登录态）
4. ✅ 更新心跳检查规则

### 下周（2026-04-01 ~ 04-07）
1. 新增定时任务（扩源平台）
2. 监控数据质量
3. 调整 AI 筛选规则

---

**最后更新：** 2026-03-26 12:00  
**负责人：** intel-officer
