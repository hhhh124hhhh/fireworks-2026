# Nano Banana Pro (Gemini API) 代理中转指南

## 问题背景

Google Gemini API 在中国大陆无法直接访问，需要使用代理中转服务。本文档提供多个可行方案，包括免费和付费选项。

## 方案一：Cloudflare Workers 中转（推荐，免费）

### 优势
- ✅ 完全免费
- ✅ 全球 CDN 加速，国内外都快速
- ✅ 无需维护服务器
- ✅ 支持自定义域名

### 实施步骤

1. **注册 Cloudflare 账号**
   - 访问 https://dash.cloudflare.com/sign-up
   - 完成邮箱验证

2. **创建 Worker**
   - 进入 Workers & Pages
   - 点击 Create Application
   - 选择 Create Worker
   - 命名为 `gemini-proxy`（或自定义）

3. **部署 Worker 代码**

创建以下 Worker 代码：

```javascript
// gemini-proxy-worker.js
export default {
  async fetch(request, env, ctx) {
    // 处理 CORS 预检请求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-goog-api-key',
          'Access-Control-Max-Age': '86400',
        }
      });
    }

    try {
      const url = new URL(request.url);
      const originalHost = 'generativelanguage.googleapis.com';
      
      // 构建目标 URL
      const targetUrl = new URL(url.pathname + url.search, `https://${originalHost}`);
      
      // 创建新请求，转发所有头信息
      const headers = new Headers();
      for (const [key, value] of request.headers.entries()) {
        if (key.toLowerCase() !== 'host') {
          headers.set(key, value);
        }
      }
      
      const newRequest = new Request(targetUrl.toString(), {
        method: request.method,
        headers: headers,
        body: request.body,
        redirect: 'follow'
      });

      // 转发请求到 Google API
      const response = await fetch(newRequest);

      // 处理响应头，添加 CORS
      const responseHeaders = new Headers();
      for (const [key, value] of response.headers.entries()) {
        if (!['access-control-allow-origin', 'access-control-allow-methods', 'access-control-allow-headers'].includes(key.toLowerCase())) {
          responseHeaders.set(key, value);
        }
      }
      responseHeaders.set('Access-Control-Allow-Origin', '*');

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: responseHeaders
      });

    } catch (error) {
      return new Response(JSON.stringify({
        error: 'Proxy error',
        message: error.message
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }
  }
}
```

4. **部署并获取 URL**
   - 点击 Deploy
   - 部署成功后会得到类似 `https://gemini-proxy.YOUR_USERNAME.workers.dev` 的 URL

5. **使用代理 URL**

使用新脚本调用：

```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image_with_proxy.py \
  --prompt "a beautiful landscape" \
  --filename "test.png" \
  --api-endpoint "https://gemini-proxy.YOUR_USERNAME.workers.dev" \
  --api-key "YOUR_GEMINI_API_KEY"
```

### 可选：绑定自定义域名

1. 在 Workers 设置中添加自定义域名（如 `gemini.yourdomain.com`）
2. 将域名 DNS 指向 Cloudflare
3. 使用自定义域名替代 `.workers.dev` 域名

---

## 方案二：第三方 API 代理服务（快速上手）

### 1. API2D（推荐）

**官网**: https://api2d.com

**优势**:
- ✅ 支持 Gemini API 代理
- ✅ 国内直连，速度快
- ✅ 按量付费，无月费
- ✅ 完善的文档和 SDK

**定价**:
- Gemini Pro: ¥0.002 / 1K tokens
- Gemini Pro Vision: ¥0.004 / 图像

**使用方法**:

1. 注册账号并获取 API Key
2. 调用方式：

```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image_with_proxy.py \
  --prompt "your prompt" \
  --filename "output.png" \
  --api-endpoint "https://oa.api2d.net" \
  --api-key "API2D_API_KEY"
```

**文档**: https://api2d.com/docs

---

### 2. OpenAI-SB

**官网**: https://openai-sb.com

**优势**:
- ✅ 支持 Gemini 代理
- ✅ 免费额度（需关注公众号）
- ✅ 国内访问

**使用方法**:
- 注册获取 Token
- API Endpoint: `https://api.openai-sb.com/v1`

---

### 3. New API

**GitHub**: https://github.com/Calcium-Ion/new-api

**优势**:
- ✅ 开源免费，可自部署
- ✅ 支持多种 AI API
- ✅ 可接入国内渠道

**自部署步骤**:

```bash
# 使用 Docker 部署
docker run -d --name new-api \
  -p 3000:3000 \
  -v /path/to/data:/data \
  calciumion/new-api:latest
```

然后在 VPS 上运行，国内可直连。

---

### 4. OneAPI

**GitHub**: https://github.com/songquanpeng/one-api

**优势**:
- ✅ 开源免费
- ✅ 多渠道聚合
- ✅ 支持密钥管理
- ✅ 可自部署

**部署**:

```bash
docker run -d --name one-api \
  -p 3000:3000 \
  -v /path/to/data:/data \
  ghcr.io/songquanpeng/one-api:latest
```

---

## 方案三：VPS 自建 Nginx 反向代理（最灵活）

### 优势
- ✅ 完全控制
- ✅ 可添加缓存、限流等功能
- ✅ 成本低（$5-10/月 VPS）

### 实施步骤

1. **购买境外 VPS**
   - 推荐: DigitalOcean, Vultr, Linode, BandwagonHost
   - 选择: 美国/日本/新加坡节点

2. **安装 Nginx**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y

# CentOS/Rocky
sudo yum install nginx -y
```

3. **配置反向代理**

编辑 `/etc/nginx/conf.d/gemini-proxy.conf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 转发 Gemini API 请求
    location /v1beta/ {
        proxy_pass https://generativelanguage.googleapis.com/v1beta/;
        proxy_ssl_server_name on;
        proxy_set_header Host generativelanguage.googleapis.com;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置（图像生成需要较长时间）
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # 健康检查端点
    location /health {
        return 200 'OK';
        add_header Content-Type text/plain;
    }
}
```

4. **重启 Nginx**

```bash
sudo nginx -t  # 测试配置
sudo systemctl restart nginx
```

5. **（可选）配置 SSL 证书**

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

6. **使用代理**

```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image_with_proxy.py \
  --prompt "your prompt" \
  --filename "output.png" \
  --api-endpoint "https://your-domain.com" \
  --api-key "YOUR_GEMINI_API_KEY"
```

---

## 方案四：VPN / 代理软件（临时方案）

如果你的网络环境已经有可用的代理，可以配置环境变量：

### 使用 HTTP 代理

```bash
export HTTP_PROXY="http://proxy-server:port"
export HTTPS_PROXY="http://proxy-server:port"

# 然后使用原脚本
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "your prompt" \
  --filename "output.png"
```

### 使用 SOCKS5 代理

```bash
# 需要安装 proxychains
sudo apt install proxychains -y

# 编辑 /etc/proxychains4.conf
# 将代理配置改为:
# socks5 127.0.0.1 1080

# 使用 proxychains 运行脚本
proxychains uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "your prompt" \
  --filename "output.png"
```

---

## 推荐方案对比

| 方案 | 成本 | 难度 | 稳定性 | 速度 | 推荐度 |
|------|------|------|--------|------|--------|
| Cloudflare Workers | 免费 | 中 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| API2D | 低费用 | 低 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| New API 自部署 | $5/月 VPS | 中 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| VPS Nginx | $5-10/月 | 中 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| VPN 代理 | 已有方案 | 低 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

---

## 快速测试

获取 Gemini API Key: https://aistudio.google.com/app/apikey

使用 Cloudflare Workers 代理测试：

```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image_with_proxy.py \
  --prompt "a cute cat in a garden" \
  --filename "test-cat.png" \
  --resolution 1K \
  --api-endpoint "https://your-worker.workers.dev" \
  --api-key "YOUR_GEMINI_API_KEY"
```

---

## 故障排查

### 问题：连接超时
**解决方案**：
- 检查代理服务是否正常运行
- 确认防火墙规则
- 尝试不同的代理端点

### 问题：403 Forbidden
**解决方案**：
- 检查 API Key 是否正确
- 确认 API Key 配额未用完
- 检查代理是否正确转发认证头

### 问题：图像生成失败
**解决方案**：
- 增加 timeout 时间
- 检查网络连接
- 尝试降低分辨率（1K → 2K）

---

## 注意事项

1. **API Key 安全**：
   - 不要在公开代码中硬编码 API Key
   - 使用环境变量存储敏感信息

2. **配额管理**：
   - Gemini API 有调用限制
   - 监控使用量避免超额

3. **国内使用**：
   - 确保代理服务在国内可访问
   - 测试延迟选择最佳节点

4. **成本控制**：
   - 4K 分辨率消耗更多配额
   - 生成前先用 1K 测试

---

## 相关资源

- Gemini API 官方文档: https://ai.google.dev/docs
- Cloudflare Workers 文档: https://developers.cloudflare.com/workers/
- Nano Banana Pro 技能文档: `/root/clawd/skills/nano-banana-pro/SKILL.md`

---

如有问题，请查看各服务的官方文档或联系技术支持。
