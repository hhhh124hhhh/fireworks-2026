# OpenCLI 站点经验

**位置**: `site-patterns/{domain}.md`

**用途**: 积累特定网站的操作经验，跨 session 复用，避免重复踩坑。

---

## 文件格式

```markdown
---
domain: example.com
aliases: [示例，Example]
updated: 2026-03-23
tested_by: bot3
---

## 平台特征

架构、反爬行为、登录需求、内容加载方式等事实

## 有效模式

已验证的 URL 模式、操作策略、选择器

## 已知陷阱

什么会失败以及为什么
```

---

## 使用规则

1. **确定目标网站后，先读取对应经验文件**
2. 经验标注发现日期，当作"可能有效的提示"而非"保证"
3. 按经验操作失败时，回退通用模式并更新文件
4. CDP 操作成功后，主动写入新发现的经验

---

## 已有经验站点

| 站点 | 域名 | 经验文件 |
|------|------|----------|
| 小红书 | xiaohongshu.com | `xiaohongshu.md` |
| 知乎 | zhihu.com | `zhihu.md` |
| 即刻 | jike.com | `jike.md` |
| 微博 | weibo.com | `weibo.md` |
| B 站 | bilibili.com | `bilibili.md` |

---

## 更新日志

- 2026-03-23: 初始化站点经验机制
