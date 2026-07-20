---
domain: bilibili.com
aliases: [B 站，哔哩哔哩，Bilibili]
updated: 2026-03-23
tested_by: bot3
---

## 平台特征

- **登录态**: 部分内容需要登录（如评论、弹幕）
- **内容结构**: 视频 + 分区，支持弹幕
- **反爬策略**: 中等，视频播放需要登录
- **内容加载**: 滚动加载推荐视频
- **特色功能**: 弹幕、投币、收藏、充电

## 有效模式

### 热门视频
```
https://www.bilibili.com/v/popular/rank/all
```

### 搜索结果
```
https://search.bilibili.com/all?keyword={keyword}
```

### 视频详情
```
https://www.bilibili.com/video/{bvid}
```

### 用户主页
```
https://space.bilibili.com/{uid}
```

### 操作策略

1. **热门榜单**: 直接抓取，无需登录
2. **搜索**: 无需登录，但评论需要
3. **视频信息**: 标题、UP 主、播放量、弹幕数
4. **评论提取**: 需要登录，滚动加载

### eval 提取示例

```javascript
// 提取热门视频列表
Array.from(document.querySelectorAll('.rank-list li')).map(item => ({
  rank: item.querySelector('.num')?.innerText || '',
  title: item.querySelector('.title')?.innerText || '',
  up: item.querySelector('.upname')?.innerText || '',
  plays: item.querySelector('.play-icon')?.nextSibling?.nodeValue || '',
  danmaku: item.querySelector('.danmaku-icon')?.nextSibling?.nodeValue || '',
  link: item.querySelector('a')?.href || ''
}))

// 提取视频信息
{
  title: document.querySelector('.video-title')?.innerText,
  up: document.querySelector('.up-name')?.innerText,
  plays: document.querySelector('.view-count')?.innerText,
  danmaku: document.querySelector('.danmaku-count')?.innerText,
  time: document.querySelector('.publish-time')?.innerText
}
```

## 已知陷阱

### 2026-03-10: 视频需要登录
- **现象**: 部分视频提示"登录后观看"
- **原因**: 版权限制
- **解决**: 使用已登录的 Chrome，或选择其他视频

### 2026-03-15: 评论分页
- **现象**: 只能获取第一页评论
- **原因**: 评论需要滚动加载
- **解决**: 滚动到评论区域底部

### 2026-03-18: 弹幕需要登录
- **现象**: 未登录时弹幕不显示
- **原因**: 平台限制
- **解决**: 使用已登录的 Chrome

### 2026-03-20: BV 号转换
- **现象**: 视频 URL 使用 BV 号，不是 av 号
- **解决**: 直接用 BV 号访问，无需转换

## 推荐命令

```bash
# 获取热门视频
opencli bilibili hot --limit 50 -f json

# 搜索视频
opencli bilibili search --keyword "AI 教程" -f json

# 获取用户视频
opencli bilibili user --uid "xxx" -f json

# 获取视频评论（需要登录）
opencli bilibili comments --bvid "BV1xx" -f json
```

## 浏览器操作建议

```bash
# 1. 打开热门页
bb-browser open "https://www.bilibili.com/v/popular/rank/all"

# 2. 提取热门列表
bb-browser eval "Array.from(document.querySelectorAll('.rank-list li'))..."

# 3. 打开视频详情
bb-browser click ".rank-list li:nth-child(1)"

# 4. 等待加载
bb-browser wait 3000

# 5. 提取视频信息
bb-browser eval "{title: document.querySelector('.video-title')?.innerText, ...}"

# 6. 查看评论（需要登录）
bb-browser scroll down
bb-browser eval "Array.from(document.querySelectorAll('.comment-item'))..."
```
