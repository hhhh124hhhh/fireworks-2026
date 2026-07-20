# 🔍 知乎热榜抓取方案（最终版）

## 问题诊断

**现象:**
- ✅ Chrome 9222 端口正常运行
- ✅ 知乎已登录（67 封私信）
- ✅ 能导航到 https://www.zhihu.com/hot
- ✅ 截图显示页面正常
- ❌ 但 JavaScript 选择器提取不到数据

**原因:**
知乎热榜页面是 React 单页应用，动态加载内容，CDP 执行 JavaScript 时页面可能还没完全渲染。

---

## 解决方案（3 选 1）

### 方案 1：等待更长时间 +  MutationObserver（推荐）

```javascript
await Page.navigate({ url: 'https://www.zhihu.com/hot' });

// 等待动态内容加载
await Runtime.evaluate({
  expression: `
    new Promise((resolve) => {
      const observer = new MutationObserver(() => {
        const items = document.querySelectorAll('.HotItem, [data-zop-question]');
        if (items.length >= 20) {
          observer.disconnect();
          resolve(items.length);
        }
      });
      observer.observe(document.body, { childList: true, subtree: true });
      // 超时 15 秒
      setTimeout(() => {
        observer.disconnect();
        resolve(document.querySelectorAll('.HotItem').length);
      }, 15000);
    })
  `
});
```

### 方案 2：用知乎公开 API（最简单）⭐

知乎热榜有公开 API，不需要登录：

```javascript
const response = await fetch('https://www.zhihu.com/api/v3/feed/topstory/hot-list?limit=20&reverse_order=0');
const data = await response.json();
const hotList = data.data.map((item, i) => ({
  rank: i + 1,
  title: item.target.title,
  hot: item.children[0]?.text || '未知',
  link: `https://www.zhihu.com/question/${item.target.id}`
}));
```

### 方案 3：用 web_search 搜索知乎热榜（备选）

```python
web_search(query="知乎热榜 2026-03-16", freshness="day")
```

---

## 明日执行方案（2026-03-16 08:00）

**优先级：**
1. **方案 2（知乎 API）** - 最简单，不需要浏览器
2. **方案 1（CDP+MutationObserver）** - 如果 API 失效
3. **方案 3（web_search）** - 作为备选

**晨间轮抓取流程：**
```
08:00 启动抓取
08:01 尝试知乎 API
08:02 如果失败，用 CDP+MutationObserver
08:05 如果还失败，用 web_search
08:06 写入飞书多维表格
08:07 生成晨报
```

---

## 配置更新

**文件:** `HEARTBEAT.md`

已更新晨间轮配置：
- ✅ 知乎必须用 Chrome CDP 或 API
- ✅ 禁止用 web_fetch（会 403）
- ✅ 备选方案：知乎 API → CDP → web_search

---

**测试状态:** ⚠️ 测试中
**预计完成:** 2026-03-16 今晚
**明日执行:** ✅ 确保正常
