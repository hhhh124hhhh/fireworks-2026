# Cloudflare Pages 自动部署配置指南

## ✅ 自动部署已启用！

我已经启用了 Cloudflare Pages 的自动部署功能。现在每次推送到 `main` 分支时，GitHub Actions 会自动将代码部署到 Cloudflare Pages。

---

## 🔧 配置步骤（一次性操作）

### 步骤 1：打开 GitHub 仓库设置

1. 访问 https://github.com/hhhh124hhhh/jack-portfolio
2. 点击 **"Settings"** 标签
3. 在左侧菜单中，找到 **"Secrets and variables"**
4. 点击 **"Actions"**

---

### 步骤 2：添加 Cloudflare API Token

1. 点击 **"New repository secret"** 按钮
2. **Name** 输入: `CLOUDFLARE_API_TOKEN`
3. **Value** 输入: `Sd0vKvLKAVaKIScuBEEsPb1d3tAmL8aR-wh4M6sf`
4. 点击 **"Add secret"** 保存

---

### 步骤 3：添加 Cloudflare Account ID

1. 再次点击 **"New repository secret"** 按钮
2. **Name** 输入: `CLOUDFLARE_ACCOUNT_ID`
3. **Value** 输入: `944fa484617a666c2f04aa2cc308285c`
4. 点击 **"Add secret"** 保存

---

### 步骤 4：验证配置

1. 配置完成后，GitHub Actions 会自动触发部署
2. 访问 https://github.com/hhhh124hhhh/jack-portfolio/actions
3. 查看最新的 workflow 运行状态
4. 等待部署完成（通常 1-3 分钟）

---

## 🚀 自动部署工作流程

### 触发条件

**自动触发**（推荐）:
- 每次推送到 `main` 分支时自动部署
- 无需手动操作

**手动触发**:
1. 访问 https://github.com/hhhh124hhhh/jack-portfolio/actions
2. 找到 **"Deploy to Cloudflare Pages"** workflow
3. 点击 **"Run workflow"**
4. 选择 `main` 分支
5. 点击 **"Run workflow"** 按钮

---

## 📊 部署状态检查

### 查看 GitHub Actions

1. 访问 https://github.com/hhhh124hhhh/jack-portfolio/actions
2. 查看最新的 workflow 运行记录
3. 点击运行记录查看详细日志
4. 确认状态是 **"✅ Success"**

### 查看 Cloudflare Pages

1. 访问 https://dash.cloudflare.com/
2. 找到 `jack-portfolio` 或 `jack-portfolio-5un` 项目
3. 进入项目页面
4. 点击 **"Deployments"** 标签
5. 查看最新的部署记录

### 验证部署结果

1. 访问 https://jack-portfolio-5un.pages.dev/
2. 确认显示最新的 12 个项目
3. 确认是 Luxury 风格
4. 确认所有功能正常

---

## 🔍 故障排查

### 问题 1：GitHub Actions 失败

**可能原因**:
- Secrets 配置错误
- Cloudflare API Token 无效
- Cloudflare Account ID 错误

**解决方法**:
1. 检查 GitHub Secrets 是否正确配置
2. 确认 Secrets 的名称和值完全匹配
3. 查看 GitHub Actions 的详细日志
4. 检查 Cloudflare API Token 是否有效

---

### 问题 2：Cloudflare Pages 部署失败

**可能原因**:
- Cloudflare 项目名称不匹配
- Cloudflare 项目配置错误
- Cloudflare 账户权限问题

**解决方法**:
1. 确认 Cloudflare Pages 项目名称是 `jack-portfolio`
2. 如果项目名称是 `jack-portfolio-5un`，需要修改 workflow 配置
3. 检查 Cloudflare 账户是否有 Pages 权限

---

### 问题 3：部署成功但显示旧内容

**可能原因**:
- 浏览器缓存
- Cloudflare CDN 缓存

**解决方法**:
1. 使用 Ctrl+Shift+R（Windows）或 Cmd+Shift+R（Mac）强制刷新
2. 等待 1-2 分钟让 CDN 缓存更新
3. 访问 https://jack-portfolio-5un.pages.dev/?refresh=true

---

## 📝 Workflow 配置文件

### 文件位置

`.github/workflows/deploy-cloudflare.yml`

### 配置内容

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
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy . --project-name=jack-portfolio
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```

---

## 🎯 重要提示

### Cloudflare 项目名称

如果 Cloudflare Pages 项目名称不是 `jack-portfolio`，需要修改 workflow 配置：

**示例**: 如果项目名称是 `jack-portfolio-5un`

```yaml
command: pages deploy . --project-name=jack-portfolio-5un
```

然后提交并推送更改。

---

### Secrets 安全性

- ✅ Secrets 存储在 GitHub 仓库设置中，不会暴露在代码中
- ✅ 只有仓库管理员可以查看和修改 Secrets
- ✅ GitHub Actions 运行时自动读取 Secrets
- ⚠️ 请勿在代码中硬编码 API Token 或 Account ID

---

## 🔄 未来工作流程

### 正常开发流程

1. 修改代码
2. 提交更改: `git add . && git commit -m "feat: 新功能"`
3. 推送到 GitHub: `git push origin main`
4. GitHub Actions 自动触发部署
5. 等待 1-3 分钟
6. 访问 Cloudflare Pages 查看结果

### 快速验证

每次推送后，可以：
1. 查看 GitHub Actions 状态: https://github.com/hhhh124hhhh/jack-portfolio/actions
2. 访问 Cloudflare Pages: https://jack-portfolio-5un.pages.dev/
3. 确认显示最新内容

---

## 📚 相关链接

- **GitHub 仓库**: https://github.com/hhhh124hhhh/jack-portfolio
- **GitHub Actions**: https://github.com/hhhh124hhhh/jack-portfolio/actions
- **Cloudflare Dashboard**: https://dash.cloudflare.com/
- **Cloudflare Pages**: https://jack-portfolio-5un.pages.dev/
- **GitHub Pages**: https://hhhh124hhhh.github.io/jack-portfolio/

---

## 🆘 需要帮助？

如果配置过程中遇到问题：

1. 查看 GitHub Actions 详细日志
2. 确认 Secrets 配置正确
3. 检查 Cloudflare 账户权限
4. 查看本文档的"故障排查"部分

---

**文档创建时间**: 2026-02-07 21:12  
**自动部署状态**: ✅ 已启用（需要配置 Secrets）
