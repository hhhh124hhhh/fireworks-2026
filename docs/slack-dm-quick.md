# 🚀 Slack 私聊配置 - 3 步搞定

## 第 1 步：在 Slack 给 Bot 发消息

1. 打开你的 Slack
2. 搜索你的 Bot 名称
3. 点击"**发送消息**"
4. 随便发一条消息（如 "hello"）

---

## 第 2 步：获取 DM Channel ID

**看浏览器地址栏：**

```
https://your-workspace.slack.com/archives/D0123456789
                                         ↑
                              复制这部分（D 开头）
```

**如果看不到，试试这个：**

1. 按 **F12** 打开开发者工具
2. 切换到 **Console** 标签
3. 粘贴并回车：

```javascript
const id = window.location.pathname.split('/').pop();
console.log('你的 DM Channel ID:', id);
```

4. 复制显示的 ID（D 开头）

---

## 第 3 步：发给我

把你的 **DM Channel ID** 发给我！

格式：`D0123456789`（D 开头的字符串）

---

## ⚡ 配置后就能：

✅ 私聊接收任务进度
✅ 私聊查看统计报告
✅ 私聊接收错误警告
✅ 避免群聊干扰

---

**准备好了吗？把你的 DM Channel ID 发给我！**

格式：`D0123456789` 🚀
