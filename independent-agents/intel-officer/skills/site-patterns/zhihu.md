---
domain: zhihu.com
aliases: [知乎，Zhihu]
updated: 2026-03-23
tested_by: bot3, bot12
---

## 平台特征

- **登录态**: 部分内容需要登录才能查看（尤其是评论）
- **内容结构**: 问题页 + 回答列表，回答可折叠/展开
- **反爬策略**: 中等，高频访问会触发验证码
- **内容加载**: 滚动加载更多回答
- **富文本**: 回答使用富文本编辑器，包含图片、视频、引用等

## 有效模式

### 问题页 URL
```
https://www.zhihu.com/question/{question_id}
```

### 回答详情
```
https://www.zhihu.com/question/{question_id}/answer/{answer_id}
```

### 热搜榜
```
https://www.zhihu.com/hot
```

### 操作策略

1. **展开长回答**: 点击"展开"按钮查看全文
2. **滚动加载**: 滚动到底部触发"更多回答"加载
3. **评论查看**: 需要点击评论按钮展开评论列表
4. **图片提取**: 回答中的图片在 `img` 标签，`data-original` 属性为高清 URL

### eval 提取示例

```javascript
// 提取问题页的回答列表
Array.from(document.querySelectorAll('.AnswerItem')).map(item => ({
  author: item.querySelector('.UserLink-link')?.innerText || '匿名用户',
  content: item.querySelector('.RichContent-inner')?.innerText || '',
  upvotes: item.querySelector('.VoteButton--up')?.getAttribute('aria-label') || '0',
  comments: item.querySelector('.ContentItem-action--comment')?.innerText || '0'
}))

// 提取问题信息
{
  title: document.querySelector('h1.QuestionHeader-title')?.innerText,
  description: document.querySelector('.QuestionHeader-detail')?.innerText,
  followerCount: document.querySelector('.QuestionHeader-followers')?.innerText
}
```

## 已知陷阱

### 2026-03-15: 折叠回答
- **现象**: 部分回答只显示摘要
- **原因**: 长回答默认折叠
- **解决**: 点击"展开"或"继续浏览"按钮

### 2026-03-18: 评论需要登录
- **现象**: 未登录时评论区域显示"登录后查看"
- **原因**: 平台限制
- **解决**: 使用已登录的 Chrome，或忽略评论数据

### 2026-03-20: 验证码
- **现象**: 高频访问后触发滑块验证
- **原因**: 风控检测
- **解决**: 降低访问频率，手动完成验证

### 2026-03-22: 图片延迟加载
- **现象**: 图片 URL 为空或低清
- **原因**: 懒加载
- **解决**: 滚动页面触发加载，等待后提取 `data-original` 属性

## 推荐命令

```bash
# 获取热搜榜
opencli zhihu hot -f json

# 搜索问题
opencli zhihu search --keyword "大模型" -f json

# 获取问题详情
opencli zhihu question --id "123456" -f json

# 获取回答
opencli zhihu answer --id "789" -f json
```

## 浏览器操作建议

```bash
# 1. 打开问题页
bb-browser open "https://www.zhihu.com/question/123456"

# 2. 展开所有回答
bb-browser eval "document.querySelectorAll('.ContentItem-expandButton').forEach(b => b.click())"

# 3. 滚动加载
bb-browser scroll down

# 4. 提取回答
bb-browser eval "Array.from(document.querySelectorAll('.AnswerItem'))..."

# 5. 查看评论（需要登录）
bb-browser click ".ContentItem-action--comment"
bb-browser wait 2000
bb-browser eval "Array.from(document.querySelectorAll('.CommentItem'))..."
```
