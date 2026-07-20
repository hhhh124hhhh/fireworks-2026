# Cloudflare Pages 自动部署配置教程

## 📋 概述

本教程将指导你如何配置 Cloudflare Pages 的自动部署，使其在每次推送代码到 GitHub 时自动更新。

---

## 🎯 前提条件

### 必需条件
1. GitHub 账号和仓库
2. Cloudflare 账号
3. Cloudflare Pages 项目已创建

### 准备工作
1. GitHub 仓库的 `main` 分支
2. Cloudflare API Token
3. Cloudflare Account ID
4. Cloudflare Pages 项目名称

---

## 🔧 步骤 1：获取 Cloudflare 凭证

### 1.1 获取 Cloudflare API Token

1. 访问 https://dash.cloudflare.com/profile/api-tokens
2. 点击 **"Create Token"**
3. 选择 **"Custom token"**
4. 配置权限：
   - **Account** → **Cloudflare Pages** → **Edit**
5. 点击 **"Continue to summary"**
6. 点击 **"Create Token"**
7. **复制生成的 Token**（只显示一次！）

### 1.2 获取 Cloudflare Account ID

**方法 1**：
1. 访问 https://dash.cloudflare.com/
2. 选择你的账户
3. 在 URL 中查看：`dash.cloudflare.com/<account-id>/...`
4. `<account-id>` 就是你的 Account ID

**方法 2**：
1. 访问 https://dash.cloudflare.com/profile/api-tokens
2. 在 **"Global API Key"** 部分
3. **Account ID** 一栏显示你的 ID

### 1.3 确认 Cloudflare Pages 项目名称

**重要**：项目名称是 Cloudflare 内部标识，不是自定义域名！

**如何找到正确的项目名称**：
1. 访问 Cloudflare Dashboard
2. 进入 **"Workers & Pages"**
3. 找到你的 Pages 项目
4. 点击进入项目
5. **查看 URL 路径**：`dash.cloudflare.com/.../pages/view/<项目名称>/...`
6. `<项目名称>` 就是正确的项目名称

**示例**：
- **Dashboard URL**: `dash.cloudflare.com/.../pages/view/jack-portfolio/...`
- **项目名称**: `jack-portfolio`
- **自定义域名**: `jack-portfolio-5un.pages.dev`

**注意**：配置文件中使用的是 **项目名称**，不是自定义域名！

---

## 🔧 步骤 2：配置 GitHub Secrets

### 2.1 打开 GitHub 仓库设置

1. 访问你的 GitHub 仓库（例如：https://github.com/hhhh124hhhh/jack-portfolio）
2. 点击 **"Settings"** 标签
3. 在左侧菜单中，找到 **"Secrets and variables"**
4. 点击 **"Actions"**

### 2.2 添加 Cloudflare API Token

1. 点击 **"New repository secret"** 按钮
2. **Name**: `CLOUDFLARE_API_TOKEN`
3. **Value**: 粘贴你刚才复制的 API Token
4. 点击 **"Add secret"** 保存

### 2.3 添加 Cloudflare Account ID

1. 再次点击 **"New repository secret"** 按钮
2. **Name**: `CLOUDFLARE_ACCOUNT_ID`
3. **Value**: 粘贴你的 Account ID
4. 点击 **"Add secret"** 保存

---

## 🔧 步骤 3：创建 GitHub Actions workflow

### 3.1 创建 workflow 文件

在你的 GitHub 仓库中创建文件：

**路径**: `.github/workflows/deploy-cloudflare.yml`

**内容**:

```yaml
name: Deploy to Cloudflare Pages

on:
  # 自动部署：当推送到 main 分支时
  push:
    branches:
      - main
  # 手动触发
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    name: Deploy to Cloudflare Pages
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: <你的项目名称>
          directory: .
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

**注意**：将 `<你的项目名称>` 替换为实际的 Cloudflare Pages 项目名称（例如：`jack-portfolio`）。

### 3.2 提交 workflow 文件

```bash
git add .github/workflows/deploy-cloudflare.yml
git commit -m "feat: 添加 Cloudflare Pages 自动部署"
git push origin main
```

---

## 🔧 步骤 4：验证自动部署

### 4.1 检查 GitHub Actions

1. 访问 https://github.com/<你的用户名>/<你的仓库>/actions
2. 查看最新的 **"Deploy to Cloudflare Pages"** workflow
3. 确认状态是 **"✅ Success"**

### 4.2 检查 Cloudflare Pages 部署记录

1. 访问 Cloudflare Dashboard
2. 进入你的 Pages 项目
3. 点击 **"Deployments"** 标签
4. 查看最新的部署记录
5. 确认最新的部署显示了最新内容

### 4.3 访问 Cloudflare Pages

1. 访问你的 Cloudflare Pages URL
2. 确认显示最新的内容
3. 如果显示旧内容，尝试强制刷新（Ctrl+Shift+R）

---

## 🔍 常见问题

### 问题 1：GitHub Actions 部署失败

**可能原因**:
- Cloudflare API Token 无效
- Cloudflare Account ID 错误
- 项目名称不匹配

**解决方法**:
1. 检查 GitHub Actions 详细日志
2. 确认 Secrets 配置正确
3. 确认项目名称正确（查看 Dashboard URL）
4. 重新配置并提交

---

### 问题 2：部署成功但页面未更新

**可能原因**:
- Cloudflare CDN 缓存
- 浏览器缓存

**解决方法**:
1. 强制刷新浏览器（Ctrl+Shift+R）
2. 等待 5-10 分钟让 CDN 缓存更新
3. 访问预览 URL（最新部署的 URL）

---

### 问题 3：项目名称错误

**症状**: 部署失败或部署到错误的项目

**可能原因**:
- 使用了自定义域名作为项目名称

**解决方法**:
1. 访问 Cloudflare Dashboard
2. 查看 URL 路径：`/pages/view/<项目名称>/...`
3. 使用 `<项目名称>` 配置 workflow
4. 不要使用自定义域名！

**示例**:
- ✅ 正确: `projectName: jack-portfolio`
- ❌ 错误: `projectName: jack-portfolio-5un.pages.dev`

---

### 问题 4：Wrangler Action 失败

**可能原因**:
- Wrangler Action 版本兼容性问题
- 环境配置问题

**解决方法**:
1. 切换到官方 Pages Action: `cloudflare/pages-action@v1`
2. 重新配置 workflow
3. 重新提交

---

## 📊 最佳实践

### 1. 使用官方 Action

**推荐**: `cloudflare/pages-action@v1`
- Cloudflare 官方维护
- 专为 Cloudflare Pages 设计
- 更稳定可靠

**不推荐**: `cloudflare/wrangler-action@v3`
- 通用 Wrangler 工具
- 兼容性问题较多

---

### 2. 正确的项目命名

**项目名称**:
- Cloudflare 内部标识
- 用于 API 调用
- 配置文件中使用

**自定义域名**:
- 访问 URL
- 对外展示
- 不用于配置

---

### 3. 自动触发配置

**推荐配置**:
```yaml
on:
  push:
    branches:
      - main
  workflow_dispatch:
```

**说明**:
- 自动触发：推送到 `main` 分支时
- 手动触发：在 GitHub Actions 页面手动触发

---

### 4. 部署验证

**验证清单**:
- [ ] GitHub Actions 状态是 "Success"
- [ ] Cloudflare Pages 部署记录显示最新内容
- [ ] Cloudflare Pages URL 显示最新内容
- [ ] 所有功能正常

---

## 🚀 未来工作流程

### 正常开发流程

```bash
# 1. 修改代码
vim index.html

# 2. 提交更改
git add .
git commit -m "feat: 新功能或优化"

# 3. 推送到 GitHub
git push origin main

# 4. GitHub Actions 自动部署（无需手动操作）
# 等待 1-3 分钟

# 5. 访问 Cloudflare Pages 查看结果
# https://<你的项目名称>.pages.dev/
```

---

## 📚 相关资源

### 官方文档
- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)
- [Cloudflare Pages Action](https://github.com/cloudflare/pages-action)
- [GitHub Actions 文档](https://docs.github.com/en/actions)

### 工具
- [Cloudflare Dashboard](https://dash.cloudflare.com/)
- [GitHub](https://github.com/)

---

## 🎯 总结

### 配置要点
1. **获取凭证**: API Token、Account ID、项目名称
2. **配置 Secrets**: 在 GitHub 仓库中添加 Secrets
3. **创建 workflow**: 使用 Cloudflare 官方 Pages Action
4. **验证部署**: 检查 GitHub Actions 和 Cloudflare Pages

### 关键要点
1. 使用官方 Action: `cloudflare/pages-action@v1`
2. 项目名称是 Cloudflare 内部标识，不是自定义域名
3. 从 Dashboard URL 路径找到正确的项目名称
4. 推送到 `main` 分支时自动触发部署

### 常见错误
1. 使用自定义域名作为项目名称 ❌
2. 使用非官方 Action ❌
3. 项目名称配置错误 ❌
4. Secrets 配置错误 ❌

---

## 🆘 需要帮助？

如果遇到问题：
1. 查看 GitHub Actions 详细日志
2. 确认 Secrets 配置正确
3. 确认项目名称正确
4. 查看本文档的"常见问题"部分

---

**教程完成时间**: 2026-02-07 22:30  
**适用版本**: Cloudflare Pages 最新版本
