# camoufox-cli 集成到 bot4

**集成时间**: 2026-03-24  
**状态**: ⚠️ 需要 Python 依赖安装

---

## 📦 当前状态

| 项目 | 状态 | 说明 |
|------|------|------|
| **Skill 复制** | ✅ 已完成 | `skills/camoufox-cli/` |
| **CLI 安装** | ✅ 已完成 | `npm install -g camoufox-cli` |
| **浏览器下载** | ✅ 已完成 | Camoufox 530MB |
| **Python 依赖** | ❌ 待安装 | 需要 `pip install camoufox playwright Pillow` |
| **功能测试** | ⚠️ 阻塞中 | 等待 Python 依赖 |

---

## 🐛 已知问题

### Daemon 启动超时

**错误**:
```
Error: Daemon did not start within 5 seconds
```

**原因**: Python 依赖未安装

**解决**:
```bash
# 安装 Python 依赖
pip install camoufox playwright Pillow

# 验证
python -c "import camoufox; print('OK')"
```

---

## 🎯 bot4 使用场景

### 场景 1: 反爬网站情报采集

```bash
# 打开目标网站
camoufox-cli open https://protected-site.com/intel

# 获取快照
camoufox-cli snapshot -i

# 提取数据
camoufox-cli text @e1
camoufox-cli screenshot intel.png

# 保存数据
camoufox-cli text body > intel.txt
```

### 场景 2: 需要登录的情报系统

```bash
# 首次登录
camoufox-cli open https://intel-system.com/login
camoufox-cli snapshot -i
camoufox-cli fill @e1 "username"
camoufox-cli fill @e2 "password"
camoufox-cli click @e3

# 导出 Cookie
camoufox-cli cookies export bot4-intel.json

# 后续使用
camoufox-cli open https://intel-system.com
camoufox-cli cookies import bot4-intel.json
camoufox-cli reload
```

### 场景 3: 多会话并行采集

```bash
# 会话 1 - 网站 A
camoufox-cli --session site-a open https://site-a.com

# 会话 2 - 网站 B
camoufox-cli --session site-b open https://site-b.com

# 采集数据
camoufox-cli --session site-a snapshot -i
camoufox-cli --session site-b snapshot -i
```

---

## 📋 集成步骤

### Step 1: 安装 Python 依赖

```bash
# 找到 Python
where python

# 安装依赖
pip install camoufox playwright Pillow

# 验证
python -c "import camoufox; print('OK')"
```

### Step 2: 测试基本功能

```bash
# 打开网页
camoufox-cli open https://example.com

# 获取快照
camoufox-cli snapshot -i

# 关闭
camoufox-cli close
```

### Step 3: 集成到 bot4 工作流

编辑 `workspace-intel-officer/skills/opencli-hotspot-grabber/README.md`，添加 camoufox-cli 作为备用抓取源。

---

## 🔄 与 opencli 配合使用

| 场景 | 推荐工具 | 原因 |
|------|---------|------|
| 常规网站 | opencli | 更快，有登录态 |
| 反爬网站 | camoufox-cli | C++ 级指纹伪造 |
| 需要 CAPTCHA | camoufox-cli | 真实浏览器 |
| Cookie 持久化 | 两者均可 | 都支持导入导出 |

**工作流**:
```
1. 先尝试 opencli (快速)
2. 遇到反爬 → 切换到 camoufox-cli
3. 采集完成 → 关闭会话
```

---

## ✅ 待办事项

### P0 (立即)

- [ ] 安装 Python 依赖 (`pip install camoufox playwright Pillow`)
- [ ] 测试基本功能
- [ ] 测试 Cookie 管理

### P1 (本周)

- [ ] 集成到 bot4 热点采集
- [ ] 创建 bot4 专用脚本
- [ ] 添加使用示例

### P2 (下周)

- [ ] 改造成 MCP Server (可选)
- [ ] 优化配置
- [ ] 添加更多使用场景

---

## 📚 相关文档

- **Skill 文档**: `skills/camoufox-cli/SKILL.md`
- **技术报告**: `D:\camoufox-cli\TECH-ANALYSIS.md`
- **集成指南**: `D:\camoufox-cli\INTEGRATION-GUIDE.md`
- **bot4 技能**: `workspace-intel-officer/skills/opencli-hotspot-grabber/`

---

**维护者**: bot3 (zhuazhua-agent)  
**最后更新**: 2026-03-24 11:25
