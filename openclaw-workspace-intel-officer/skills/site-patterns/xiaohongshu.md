---
domain: xiaohongshu.com
aliases: [小红书，RED，XHS]
updated: 2026-03-23
tested_by: bot3, bot9
---

## 平台特征

- **强反爬**: 必须登录态，未登录只能看少量内容
- **内容动态加载**: 瀑布流布局，需滚动触发懒加载
- **搜索需要处理验证码**: 高频搜索会触发滑块验证
- **笔记详情页**: 需要登录才能查看全文和评论
- **API 特点**: 大量使用 GraphQL，参数复杂

## 有效模式

### 搜索 URL 模式
```
https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes
```

### 首页推荐
```
https://www.xiaohongshu.com/explore
```

### 用户主页
```
https://www.xiaohongshu.com/user/profile/{user_id}
```

### 笔记详情
```
https://www.xiaohongshu.com/explore/{note_id}
```

### 操作策略

1. **触发懒加载**: 使用 `/scroll direction=bottom` 滚动到底部
2. **提取笔记卡片**: 用 `/eval` 提取 DOM 中的数据
3. **进入详情**: 从搜索结果页点击进入，不要直接访问详情页 URL
4. **图片提取**: 笔记图片在 DOM 中，用 `/eval` 提取 `data-original` 属性

### eval 提取示例

```javascript
// 提取搜索结果页的笔记列表
Array.from(document.querySelectorAll('.note-item')).map(item => ({
  title: item.querySelector('.title')?.innerText || '',
  author: item.querySelector('.author')?.innerText || '',
  likes: item.querySelector('.like-count')?.innerText || '0',
  link: item.querySelector('a.cover')?.href || ''
}))
```

## 已知陷阱

### 2026-03-20: 详情页 403
- **现象**: 直接访问笔记详情页 URL 会返回 403
- **原因**: 平台检测直接访问，需要从搜索结果页或首页点击进入
- **解决**: 先用 opencli 搜索，从结果中提取链接，然后用浏览器点击打开

### 2026-03-21: 滑块验证码
- **现象**: 高频搜索后触发滑块验证
- **原因**: 平台风控检测到异常请求频率
- **解决**: 降低搜索频率，或手动完成验证后继续

### 2026-03-22: 图片懒加载
- **现象**: 提取图片 URL 时部分图片为空
- **原因**: 图片未进入视口，懒加载未触发
- **解决**: 先用 `/scroll direction=bottom` 滚动到底部，等待 2 秒再提取

### 2026-03-23: 评论分页
- **现象**: 只能获取第一页评论
- **原因**: 评论需要滚动加载
- **解决**: 滚动到评论区域底部，触发加载后再提取

## 推荐命令

```bash
# 搜索笔记
opencli xiaohongshu search --keyword "AI 工具" -f json

# 获取热门笔记
opencli xiaohongshu hot --limit 20 -f json

# 获取用户笔记
opencli xiaohongshu user --user_id "xxx" -f json
```

## 浏览器操作建议

当 opencli 命令不满足需求时，使用 bb-browser 或 web-access：

```bash
# 1. 打开搜索页
bb-browser open "https://www.xiaohongshu.com/search_result?keyword=AI 工具"

# 2. 滚动触发懒加载
bb-browser scroll down

# 3. 提取笔记列表
bb-browser eval "Array.from(document.querySelectorAll('.note-item'))..."

# 4. 点击笔记详情
bb-browser click @5

# 5. 提取正文
bb-browser eval "document.querySelector('.note-content').innerText"
```
