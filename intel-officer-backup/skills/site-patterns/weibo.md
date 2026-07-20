---
domain: weibo.com
aliases: [微博，Weibo，新浪微博]
updated: 2026-03-23
tested_by: bot3
---

## 平台特征

- **登录态**: 部分内容需要登录，评论必须登录
- **内容结构**: 微博列表 + 详情页，支持图文/视频
- **反爬策略**: 较强，高频访问会触发验证
- **内容加载**: 滚动加载，无限瀑布流
- **热搜榜**: 实时热点，每 5 分钟更新

## 有效模式

### 热搜榜
```
https://s.weibo.com/top/summary
```

### 搜索结果
```
https://s.weibo.com/weibo?q={keyword}
```

### 用户主页
```
https://weibo.com/u/{user_id}
```

### 微博详情
```
https://weibo.com/{user_id}/{status_id}
```

### 操作策略

1. **热搜榜**: 直接抓取，无需登录
2. **搜索**: 需要处理可能的验证码
3. **滚动加载**: 滚动到底部自动加载
4. **图片提取**: 微博图片在 `img` 标签，`src` 属性

### eval 提取示例

```javascript
// 提取热搜榜
Array.from(document.querySelectorAll('.top-list li')).map((item, i) => ({
  rank: i + 1,
  title: item.querySelector('.title')?.innerText || '',
  hot: item.querySelector('.hot')?.innerText || '',
  link: item.querySelector('a')?.href || ''
}))

// 提取搜索结果
Array.from(document.querySelectorAll('.card-wrap')).map(item => ({
  author: item.querySelector('.name')?.innerText || '',
  content: item.querySelector('.txt')?.innerText || '',
  time: item.querySelector('.from')?.innerText || '',
  reposts: item.querySelector('.card-act li:nth-child(1)')?.innerText || '0',
  comments: item.querySelector('.card-act li:nth-child(2)')?.innerText || '0',
  likes: item.querySelector('.card-act li:nth-child(3)')?.innerText || '0'
}))
```

## 已知陷阱

### 2026-03-12: 验证码
- **现象**: 搜索时触发滑块验证
- **原因**: 高频搜索
- **解决**: 降低频率，手动完成验证

### 2026-03-15: 评论需要登录
- **现象**: 未登录时评论区域不显示
- **原因**: 平台限制
- **解决**: 使用已登录的 Chrome

### 2026-03-18: 内容折叠
- **现象**: 长微博显示"全文"按钮
- **原因**: 默认折叠
- **解决**: 点击"全文"展开

### 2026-03-20: 图片反爬
- **现象**: 图片 URL 有防盗链
- **解决**: 在浏览器内截图，或添加 Referer 头

## 推荐命令

```bash
# 获取热搜榜
opencli weibo hot -f json

# 搜索微博
opencli weibo search --keyword "AI" -f json

# 获取用户微博
opencli weibo user --user_id "xxx" -f json
```

## 浏览器操作建议

```bash
# 1. 打开热搜榜
bb-browser open "https://s.weibo.com/top/summary"

# 2. 提取热搜
bb-browser eval "Array.from(document.querySelectorAll('.top-list li'))..."

# 3. 搜索
bb-browser open "https://s.weibo.com/weibo?q=AI"
bb-browser scroll down
bb-browser eval "Array.from(document.querySelectorAll('.card-wrap'))..."

# 4. 查看全文
bb-browser click ".expand"
bb-browser get text ".txt"
```
