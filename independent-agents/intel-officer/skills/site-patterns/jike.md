---
domain: jike.com
aliases: [即刻，Jike]
updated: 2026-03-23
tested_by: bot3, bot8
---

## 平台特征

- **登录态**: 必须登录才能查看内容
- **内容结构**: 圈子 + 动态，类似微博的短内容平台
- **反爬策略**: 中等，需要登录态
- **内容加载**: 滚动加载，无限瀑布流
- **互动功能**: 点赞、评论、转发

## 有效模式

### 首页推荐
```
https://web.okjike.com
```

### 圈子页
```
https://web.okjike.com/topic/{topic_id}
```

### 用户主页
```
https://web.okjike.com/u/{user_id}
```

### 操作策略

1. **滚动加载**: 滚动到底部自动加载下一条动态
2. **图片提取**: 动态图片在 `img` 标签，直接提取 `src` 属性
3. **链接提取**: 动态中的外链在 `a` 标签，`href` 属性

### eval 提取示例

```javascript
// 提取首页动态列表
Array.from(document.querySelectorAll('.post')).map(item => ({
  author: item.querySelector('.username')?.innerText || '',
  content: item.querySelector('.content')?.innerText || '',
  images: Array.from(item.querySelectorAll('img')).map(img => img.src),
  likes: item.querySelector('.like-count')?.innerText || '0',
  comments: item.querySelector('.comment-count')?.innerText || '0',
  time: item.querySelector('.time')?.innerText || ''
}))
```

## 已知陷阱

### 2026-03-10: 登录验证
- **现象**: 未登录时重定向到登录页
- **原因**: 平台强制登录
- **解决**: 使用已登录的 Chrome，确保 Cookie 有效

### 2026-03-15: 图片懒加载
- **现象**: 图片 URL 为占位图
- **原因**: 懒加载
- **解决**: 滚动页面触发加载，等待后提取

### 2026-03-20: 评论嵌套
- **现象**: 评论有多层嵌套
- **原因**: 即刻支持回复评论
- **解决**: 用递归方式提取评论树

## 推荐命令

```bash
# 获取首页推荐
opencli jike feed -f json

# 获取圈子动态
opencli jike topic --id "xxx" -f json

# 获取用户动态
opencli jike user --user_id "xxx" -f json

# 发布动态（需要确认）
opencli jike post --text "内容"
```

## 浏览器操作建议

```bash
# 1. 打开首页
bb-browser open "https://web.okjike.com"

# 2. 滚动加载
bb-browser scroll down

# 3. 提取动态
bb-browser eval "Array.from(document.querySelectorAll('.post'))..."

# 4. 点赞
bb-browser click ".like-button"

# 5. 评论
bb-browser click ".comment-button"
bb-browser fill ".comment-input" "评论内容"
bb-browser press Enter
```
