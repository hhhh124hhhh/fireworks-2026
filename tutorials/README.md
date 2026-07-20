# Clawdbot/Momo 沟通教程

## 📚 简介

这个目录记录了与 Clawdbot/Momo 沟通过程中的易错点、优化点和最佳实践。

每个教程都是基于实际经验生成，帮助你：
- 避免常见错误
- 理解最佳实践
- 提高沟通效率
- 快速解决问题

## 🔍 如何使用教程

### 查找教程
```bash
# 列出所有教程
python3 /root/clawd/scripts/tutorial-generator.py

# 搜索特定主题
python3 /root/clawd/scripts/tutorial-generator.py search "关键词"
```

### 阅读教程
直接在 `/root/clawd/tutorials/` 目录下找到对应的 Markdown 文件。

### 贡献教程
当发现新的易错点或优化点时：
1. 记录问题
2. 记录错误做法
3. 记录正确做法
4. 运行 tutorial-generator.py 生成教程

## 📖 教程索引

所有教程的信息保存在 `index.json` 中，包含：
- 教程 ID
- 标题
- 分类
- 标签
- 创建日期
- 文件路径

## 🏷️ 标签系统

教程使用标签进行分类：
- `会话管理` - 会话、上下文、记忆相关
- `配置` - 配置文件、环境变量
- `最佳实践` - 推荐的做法
- `API` - API 调用相关
- `Python` - Python 脚本相关
- `工具使用` - OpenClaw 工具使用

## 🤝 自动生成

教程由子代理自动生成：
1. 记录易错点和优化点
2. 调用 coding-agent (Claude) 生成详细内容
3. 保存到教程目录
4. 更新索引

## 📝 贡献

发现新的问题或优化点？请：
1. 在 daily memory 中记录
2. 运行 tutorial-generator.py
3. 子代理会自动生成教程

---

*维护者: Momo*
*最后更新: 2026-02-03*
