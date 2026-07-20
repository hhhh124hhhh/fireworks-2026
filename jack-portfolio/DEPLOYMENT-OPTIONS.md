# Jack Portfolio - 部署选项

## 问题说明

GitHub Pages 在某些网络环境下无法访问（ERR_CONNECTION_RESET），这是由于网络限制或防火墙拦截造成的。

---

## ✅ 可用的部署方案

### 方案 1：本地预览（立即可用）

#### 使用方法

1. **启动本地服务器**:
```bash
cd /root/clawd/jack-portfolio
chmod +x start-server.sh
./start-server.sh
```

2. **访问地址**:
- http://localhost:8000
- http://127.0.0.1:8000

#### 优点
- ✅ 无需网络
- ✅ 立即可用
- ✅ 完全控制

#### 缺点
- ❌ 无法分享给他人
- ❌ 需要本地运行

---

### 方案 2：Vercel（推荐）

#### 部署步骤

**方法 A：Vercel CLI（推荐）**

1. **安装 Vercel CLI**:
```bash
npm install -g vercel
```

2. **部署**:
```bash
cd /root/clawd/jack-portfolio
vercel --prod
```

**方法 B：Vercel Dashboard**

1. 访问 https://vercel.com/new
2. 导入 GitHub 仓库
3. 自动部署

#### 访问地址
- https://jack-portfolio.vercel.app

#### 优点
- ✅ 全球 CDN
- ✅ 访问稳定
- ✅ 免费额度充足
- ✅ 自动部署

#### 缺点
- ❌ 需要注册账号
- ❌ 首次部署需要几分钟

---

### 方案 3：Gitee Pages（国内推荐）

#### 部署步骤

1. **创建 Gitee 仓库**:
   - 访问 https://gitee.com
   - 注册账号
   - 创建新仓库 `jack-portfolio`

2. **推送代码到 Gitee**:
```bash
cd /root/clawd/jack-portfolio
git remote add gitee https://gitee.com/YOUR_USERNAME/jack-portfolio.git
git push -u gitee main
```

3. **启用 Gitee Pages**:
   - 进入仓库设置
   - 选择 "Pages"
   - 启用 Pages 服务
   - 选择 `index.html` 作为主页

#### 访问地址
- https://YOUR_USERNAME.gitee.io/jack-portfolio

#### 优点
- ✅ 国内访问速度快
- ✅ 免费
- ✅ 自动部署

#### 缺点
- ❌ 需要注册 Gitee 账号
- ❌ 海外访问较慢

---

### 方案 4：Netlify

#### 部署步骤

**方法 A：Netlify CLI**

1. **安装 Netlify CLI**:
```bash
npm install -g netlify-cli
```

2. **部署**:
```bash
cd /root/clawd/jack-portfolio
netlify deploy --prod
```

**方法 B：Netlify Dashboard**

1. 访问 https://app.netlify.com/drop
2. 拖拽整个文件夹到浏览器
3. 自动部署

#### 访问地址
- https://随机名字.netlify.app

#### 优点
- ✅ 免费托管
- ✅ 拖拽部署
- ✅ 访问稳定

#### 缺点
- ❌ URL 包含随机字符
- ❌ 海外服务器

---

## 🎯 推荐方案

### 立即查看效果
**选择方案 1（本地预览）**

### 长期部署
- **国内访问**: 方案 3（Gitee Pages）
- **全球访问**: 方案 2（Vercel）

---

## 📋 快速对比

| 方案 | 访问速度 | 部署难度 | 免费额度 | 推荐度 |
|------|---------|---------|---------|--------|
| 本地预览 | ⭐⭐⭐⭐⭐ | ⭐ | N/A | ⭐⭐⭐⭐⭐ |
| Vercel | ⭐⭐⭐⭐ | ⭐⭐⭐ | 100GB/月 | ⭐⭐⭐⭐⭐ |
| Gitee Pages | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 1GB | ⭐⭐⭐⭐ |
| Netlify | ⭐⭐⭐ | ⭐⭐ | 100GB/月 | ⭐⭐⭐⭐ |

---

## 🚀 下一步

**请告诉我你选择哪个方案，我会帮你完成部署！**

1. **方案 1**: 本地预览（立即可用）
2. **方案 2**: Vercel（访问稳定）
3. **方案 3**: Gitee Pages（国内快）
4. **方案 4**: Netlify（简单）

---

## 📝 注意事项

### GitHub Pages 问题

- GitHub Pages 在某些网络环境下被拦截
- 这是网络限制，不是网站问题
- 服务器端可以正常访问

### 建议使用 Vercel

- Vercel 使用全球 CDN
- 访问更稳定
- 支持 Git 自动部署
- 免费额度充足
