# Chrome DevTools 真实浏览器配置

## 📌 核心配置

**调试端口:** `9222`
**WebSocket:** `ws://127.0.0.1:9222/devtools/browser/...`
**HTTP API:** `http://127.0.0.1:9222/json/list`
**用户数据:** `C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data`

---

## ✅ 已登录平台

| 平台 | 账号 | 状态 | Cookie 持久化 |
|------|------|------|--------------|
| **知乎** | 财职创新玩家 (Lv3) | ✅ 已登录 (67 封私信) | ✅ 是 |
| **微博** | 已登录 | ✅ 已登录 | ✅ 是 |
| **Product Hunt** | 无需登录 | ✅ 可访问 | - |
| **百度** | 无需登录 | ✅ 可访问 | - |

---

## 🚀 启动方式

### 方式 1：开机自动启动（推荐）
- **快捷方式:** `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Chrome-Debug-9222.lnk`
- **说明:** 开机后自动以调试模式启动 Chrome

### 方式 2：PowerShell 脚本
```powershell
cd C:\Users\Lenovo\AppData\Local\nvm\v22.22.0\node_modules\openclaw\skills\chrome-devtools
.\start-chrome-debug.ps1
```

### 方式 3：命令行
```powershell
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data"
```

---

## 🛠️ 可用工具

### 1. Chrome DevTools MCP（技能）
**路径:** `C:\Users\Lenovo\AppData\Local\nvm\v22.22.0\node_modules\openclaw\skills\chrome-devtools\`

**核心工具:**
- `navigate_page` - 导航到 URL
- `take_snapshot` - 获取页面结构
- `take_screenshot` - 截图
- `click` / `fill` - 元素交互
- `evaluate_script` - 执行 JavaScript

**使用示例:**
```javascript
// 导航到知乎热榜
navigate_page(url="https://www.zhihu.com/hot")

// 获取页面结构
take_snapshot()

// 提取热榜数据
evaluate_script(`
  Array.from(document.querySelectorAll('[data-zop-hot]')).slice(0,15).map((el,i) => ({
    rank: i+1,
    title: el.innerText,
    hot: el.closest('section')?.querySelector('[data-zop-hot]')?.innerText
  }))
`)
```

### 2. CDP 直接连接（PowerShell）
**示例代码:**
```powershell
# 连接到 Chrome
$ws = New-Object System.Net.WebSockets.ClientWebSocket
$ws.ConnectAsync("ws://127.0.0.1:9222/devtools/page/TARGET_ID", [System.Threading.CancellationToken]::None).Wait()

# 导航到页面
$json = @{
    id = 1
    method = "Page.navigate"
    params = @{ url = "https://www.zhihu.com/hot" }
} | ConvertTo-Json -Compress
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
$ws.SendAsync($bytes, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None).Wait()

# 执行 JavaScript
$json = @{
    id = 2
    method = "Runtime.evaluate"
    params = @{ expression = "document.title" }
} | ConvertTo-Json -Compress
# ... 发送并接收结果
```

### 3. browser 工具（OpenClaw 内置）
**注意:** 默认使用 18800 端口（独立浏览器），需要修改为使用 9222 端口

---

## 📊 数据写入

### 飞书多维表格
**App Token:** `DTt9bx9gka7UW6s52ndcdnLCnDe`
**链接:** https://scn2qvzy6171.feishu.cn/base/DTt9bx9gka7UW6s52ndcdnLCnDe

**表结构:**
- **表 1:** 热门内容素材 (tblyIetlgprLVs0V) - 54 条记录
- **表 2:** 提炼情报 (tblnnynER4WjrMQV) - 14 条记录
- **表 3:** 原始情报 (tbl97RKEz1h5uHJX) - 19 条记录
- **表 4:** 清洗情报 (tblnpKvIOTZ6sZNt) - 11 条记录

**写入示例:**
```javascript
// 知乎热榜 Top5
feishu_bitable_app_table_record(
  action="batch_create",
  app_token="DTt9bx9gka7UW6s52ndcdnLCnDe",
  table_id="tblyIetlgprLVs0V",
  records=[...]
)
```

---

## 🔐 登录维护

### Cookie 持久化
- **位置:** `C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data\Default\Cookies`
- **说明:** Chrome 自动保存，无需手动管理
- **有效期:** 取决于平台（通常 30 天 - 永久）

### 登录检查
```powershell
# 检查知乎登录状态
$ws.ConnectAsync("ws://127.0.0.1:9222/devtools/page/ZHIHU_PAGE_ID", ...).Wait()
$json = @{
    id = 1
    method = "Runtime.evaluate"
    params = @{ expression = "document.cookie.includes('z_c0')" }
} | ConvertTo-Json -Compress
# 返回 true = 已登录

# 检查微博登录状态
$json = @{
    id = 2
    method = "Runtime.evaluate"
    params = @{ expression = "document.cookie.includes('SUBP') || document.cookie.includes('_T_WM')" }
} | ConvertTo-Json -Compress
```

### 重新登录
如果 Cookie 过期：
1. 导航到登录页面
2. 用户手动扫码/输入账号密码
3. Cookie 自动保存

---

## ⚠️ 注意事项

### 必须使用真实浏览器
- ❌ **禁止使用** OpenClaw 独立浏览器（18800 端口）
- ✅ **必须使用** 真实 Chrome（9222 端口）
- **原因:**
  - Cookie 持久化（无需重复登录）
  - 真实浏览器指纹（避免风控）
  - 无头模式支持（不打开窗口）

### 避免风控
- ✅ 使用已登录 Cookie
- ✅ 真实 User-Agent
- ✅ 请求间隔至少 5 秒
- ⚠️ 遇到验证码时手动处理

### 错误处理
| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Connection refused` | Chrome 未启动 | 运行 `start-chrome-debug.ps1` |
| `Tab not found` | 标签页已关闭 | 重新导航到目标 URL |
| `Cookie expired` | Cookie 过期 | 用户重新登录 |
| `Feishu auth failed` | 飞书授权失败 | 用户完成授权 |

---

## 📋 快速命令

**检查 Chrome 状态:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version"
```

**查看已打开标签页:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/list" | Select-Object title, url
```

**测试抓取知乎热榜:**
```powershell
$ws = New-Object System.Net.WebSockets.ClientWebSocket
$ws.ConnectAsync("ws://127.0.0.1:9222/devtools/page/TARGET_ID", [System.Threading.CancellationToken]::None).Wait()
$json = @{
    id = 1
    method = "Runtime.evaluate"
    params = @{ expression = "document.title" }
} | ConvertTo-Json -Compress
# ... 发送并接收结果
```

---

## 📚 相关文档

- **TOOLS.md** - 完整工具配置
- **HEARTBEAT.md** - 心跳任务配置
- **MEMORY.md** - 长期记忆
- **skill.json** - Chrome DevTools 技能配置

---

**最后更新:** 2026-03-15 21:31
**维护:** intel-officer
