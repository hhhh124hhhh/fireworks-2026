# Chrome 调试模式配置指南（真实浏览器）

## 🎯 核心问题

**错误做法：**
```powershell
# ❌ 错误：使用独立用户数据目录
chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\openclaw-data\browser\user-data"
```

**问题：**
- 使用独立的用户数据目录
- 每次启动都是全新的浏览器
- Cookie 不持久化，关闭后丢失
- 没有用户的扩展/书签/历史记录
- 每次都要重新登录所有网站

**正确做法：**
```powershell
# ✅ 正确：使用用户的日常 Chrome 数据目录
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data"
```

**优势：**
- 使用用户的日常 Chrome 数据目录
- 所有 Cookie/扩展/书签都在
- 关闭后登录状态保留
- 不需要重复登录
- 真实的浏览器指纹（避免风控）

---

## 📋 配置步骤

### 1️⃣ 关闭现有 Chrome

```powershell
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3
```

### 2️⃣ 启动调试模式 Chrome（真实浏览器）

```powershell
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$userDataDir = "$env:LOCALAPPDATA\Google\Chrome\User Data"
$debugPort = 9222

Start-Process -FilePath $chromePath `
  -ArgumentList "--remote-debugging-port=$debugPort", `
                "--user-data-dir=$userDataDir"

Start-Sleep -Seconds 5
```

### 3️⃣ 验证连接

```powershell
# 检查 Chrome 是否启动成功
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version" | Select-Object Browser, webSocketDebuggerUrl

# 查看已打开的标签页
Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/list" | Where-Object { $_.type -eq "page" } | Select-Object title, url
```

---

## 🔧 CDP 连接示例

### 方法 1：PowerShell WebSocket

```powershell
# 获取 browser ID
$browserId = (Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl -replace '^.*/devtools/browser/', ''

# 创建 WebSocket 连接
$ws = New-Object System.Net.WebSockets.ClientWebSocket
$ws.ConnectAsync("ws://127.0.0.1:9222/devtools/browser/$browserId", [System.Threading.CancellationToken]::None).Wait()

# 打开新标签页
$json = @{
    id = 1
    method = "Target.createTarget"
    params = @{ url = "https://paperswithcode.com/" }
} | ConvertTo-Json -Compress

$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
$ws.SendAsync($bytes, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None).Wait()

# 等待并读取响应
Start-Sleep -Seconds 2
$buffer = New-Object byte[] 10240
$result = $ws.ReceiveAsync($buffer, [System.Threading.CancellationToken]::None).Result
[System.Text.Encoding]::UTF8.GetString($buffer, 0, $result.Count)
```

### 方法 2：使用 browser 工具（OpenClaw）

```powershell
# 注意：browser 工具默认使用 18800 端口，需要修改配置
# 推荐直接使用 CDP WebSocket 连接
```

---

## 🚀 开机自动启动配置

### 创建快捷方式

```powershell
# 创建开机启动快捷方式
$WScript = New-Object -ComObject WScript.Shell
$shortcut = $WScript.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\Chrome-Debug-9222.lnk")
$shortcut.TargetPath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$shortcut.Arguments = '--remote-debugging-port=9222 --user-data-dir="C:\Users\Lenovo\AppData\Local\Google\Chrome\User Data"'
$shortcut.Description = "Chrome 调试模式（真实浏览器）"
$shortcut.Save()
```

### 验证脚本

创建 `start-chrome-debug.ps1`：

```powershell
# start-chrome-debug.ps1
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$debugPort = 9222
$userDataDir = "$env:LOCALAPPDATA\Google\Chrome\User Data"

Write-Host "正在启动 Chrome 调试模式..." -ForegroundColor Green
Write-Host "用户数据：$userDataDir" -ForegroundColor Cyan

# 关闭现有 Chrome
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 3

# 启动调试模式 Chrome
Start-Process -FilePath $chromePath `
  -ArgumentList "--remote-debugging-port=$debugPort", `
                "--user-data-dir=$userDataDir"

Start-Sleep -Seconds 5

# 验证连接
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:$debugPort/json/version" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Chrome 调试模式启动成功！" -ForegroundColor Green
    Write-Host "浏览器版本：$($response.Browser)" -ForegroundColor White
} catch {
    Write-Host "❌ 启动失败" -ForegroundColor Red
}
```

---

## 📊 平台抓取示例

### 抓取 Papers With Code

```powershell
# 打开 Papers With Code
$browserId = (Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/version").webSocketDebuggerUrl -replace '^.*/devtools/browser/', ''
$ws = New-Object System.Net.WebSockets.ClientWebSocket
$ws.ConnectAsync("ws://127.0.0.1:9222/devtools/browser/$browserId", [System.Threading.CancellationToken]::None).Wait()

$json = @{
    id = 1
    method = "Target.createTarget"
    params = @{ url = "https://paperswithcode.com/" }
} | ConvertTo-Json -Compress

$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
$ws.SendAsync($bytes, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None).Wait()
Start-Sleep -Seconds 5

# 获取页面标题
$pageId = (Invoke-RestMethod -Uri "http://127.0.0.1:9222/json/list" | Where-Object { $_.url -like "*paperswithcode*" }).id
$ws2 = New-Object System.Net.WebSockets.ClientWebSocket
$ws2.ConnectAsync("ws://127.0.0.1:9222/devtools/page/$pageId", [System.Threading.CancellationToken]::None).Wait()

$json = @{
    id = 2
    method = "Runtime.evaluate"
    params = @{ expression = "document.title" }
} | ConvertTo-Json -Compress

$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
$ws2.SendAsync($bytes, [System.Net.WebSockets.WebSocketMessageType]::Text, $true, [System.Threading.CancellationToken]::None).Wait()
Start-Sleep -Seconds 1

$buffer = New-Object byte[] 10240
$result = $ws2.ReceiveAsync($buffer, [System.Threading.CancellationToken]::None).Result
Write-Host "页面标题：$([System.Text.Encoding]::UTF8.GetString($buffer, 0, $result.Count))"
```

### 抓取 The Rundown AI

```powershell
# 同上，修改 URL 为 https://www.therundown.ai/
```

---

## ⚠️ 注意事项

### 1. 不要使用独立用户数据目录

```powershell
# ❌ 错误
--user-data-dir="D:\openclaw-data\browser\user-data"

# ✅ 正确
--user-data-dir="C:\Users\%USERNAME%\AppData\Local\Google\Chrome\User Data"
```

### 2. 关闭 Chrome 时的处理

```powershell
# 关闭所有 Chrome 前，先保存数据
# 建议：不要完全关闭 Chrome，保持后台运行
Get-Process chrome | Where-Object { $_.MainWindowHandle -eq [IntPtr]::Zero } | Stop-Process -Force
```

### 3. 多个 Agent 共享同一个 Chrome

如果多个 Agent 需要共享同一个 Chrome：
- 使用相同的调试端口（9222）
- 使用相同的用户数据目录
- 避免同时操作同一个标签页

### 4. Cookie 持久化

- 使用真实用户数据目录后，Cookie 自动持久化
- 关闭 Chrome 不会丢失登录状态
- 只需要在第一次登录各平台

---

## 🎯 最佳实践

### 1. 启动脚本标准化

创建统一的启动脚本 `start-chrome-debug.ps1`，所有 Agent 都使用这个脚本启动 Chrome。

### 2. 端口配置化

```powershell
# 在配置文件中定义端口
$debugPort = 9222  # 可配置
```

### 3. 错误处理

```powershell
try {
    # 启动 Chrome
    # 验证连接
} catch {
    Write-Host "启动失败：$($_.Exception.Message)" -ForegroundColor Red
    # 重试逻辑或报错
}
```

### 4. 日志记录

```powershell
# 记录启动日志
$logFile = "C:\logs\chrome-debug-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
Start-Transcript -Path $logFile
# ... 启动代码 ...
Stop-Transcript
```

---

## 📚 参考文档

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Remote Debugging](https://developer.chrome.com/docs/devtools/remote-debugging/)
- [CDP WebSocket 连接示例](https://github.com/cyrus-and/chrome-remote-interface)

---

## 🔑 关键总结

**核心要点：**
1. ✅ 使用用户的日常 Chrome 数据目录
2. ✅ 不要使用独立的用户数据目录
3. ✅ Cookie 自动持久化，无需重复登录
4. ✅ 真实的浏览器指纹，避免风控
5. ✅ 所有扩展/书签/历史记录都在

**一句话总结：**
> 用用户的日常 Chrome 启动调试模式，而不是创建一个全新的 Chrome 实例。

---

**最后更新:** 2026-03-15 23:25
**维护:** intel-officer
**适用场景:** 所有需要长期登录状态、避免风控的爬虫场景
