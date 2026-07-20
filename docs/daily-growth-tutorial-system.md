# 每日成长教程系统 - 使用 tutorial-engineer

## 系统概述

这个系统使用 `tutorial-engineer` 技能的最佳实践，将每日的成长记录转换为结构化的教程。

## 核心组件

### 1. tutorial-engineer 技能

已安装技能：`tutorial-engineer`
- 位置：`~/.agents/skills/tutorial-engineer/`
- 功能：创建分步教程和教育内容
- 特点：
  - 渐进式披露（Progressive Disclosure）
  - 动手学习（Hands-On Learning）
  - 错误预测（Error Anticipation）
  - 多种学习风格支持

### 2. Python 教程生成脚本

**文件**: `/root/clawd/scripts/daily-growth-tutorial-engineer.py`

**功能**:
- 读取昨天的 memory 文件
- 解析并提取关键成长点
- 使用 tutorial-engineer 最佳实践生成教程
- 更新教程索引

**教程结构**（遵循 tutorial-engineer 规范）:
1. What You'll Learn - 学习目标
2. Prerequisites - 前置条件
3. Context & Background - 上下文和背景
4. Problem Analysis - 问题分析
5. Solution Steps - 解决步骤
6. Lessons Learned - 经验教训
7. Resources - 相关资源

### 3. 定时任务

**执行时间**: 每天 02:00（用户睡觉时）

**Cron 任务**:
```bash
0 2 * * * python3 /root/clawd/scripts/daily-growth-tutorial-engineer.py >> /root/clawd/logs/daily-growth-cron.log 2>&1
```

## 文件结构

```
/root/clawd/
├── tutorials/
│   ├── daily-growth/
│   │   ├── 2026-02-09-技术成长.md
│   │   ├── 2026-02-09-项目管理.md
│   │   └── ...
│   └── daily-growth-index.md
├── scripts/
│   └── daily-growth-tutorial-engineer.py
├── memory/
│   ├── 2026-02-08.md
│   └── ...
└── logs/
    ├── daily-growth-cron.log
    └── daily-growth/
```

## 分类系统

教程自动分类到以下类别：

1. **技术成长** - 修复、解决、bug、调试、JSON、Bash、Python
2. **项目管理** - 项目、用户、需求、反馈、沟通、更新、部署
3. **最佳实践** - 技能、学习、最佳实践、经验教训、成长
4. **开发经验** - 创建、开发、设计、实现、自动化
5. **系统运维** - 监控、定时任务、Docker、系统
6. **其他** - 其他类型

## 使用方式

### 手动执行

```bash
# 生成今天的教程（基于昨天的 memory）
python3 /root/clawd/scripts/daily-growth-tutorial-engineer.py

# 查看日志
tail -f /root/clawd/logs/daily-growth-cron.log
```

### 自动执行

系统会在每天凌晨 02:00 自动执行。

### 查看教程

```bash
# 列出所有教程
ls -la /root/clawd/tutorials/daily-growth/

# 查看教程索引
cat /root/clawd/tutorials/daily-growth-index.md

# 查看特定教程
cat /root/clawd/tutorials/daily-growth/2026-02-09-技术成长.md
```

## 生成的教程质量

每个教程包含：

✅ **学习目标** - 明确的学习成果
✅ **前置条件** - 需要的背景知识
✅ **上下文** - 问题的背景和重要性
✅ **问题分析** - 识别和诊断问题
✅ **解决步骤** - 详细的步骤和代码示例
✅ **经验教训** - 关键经验和最佳实践
✅ **相关资源** - 技能、文档、工具的链接

## 当前状态

- ✅ tutorial-engineer 技能已安装
- ✅ Python 教程生成脚本已创建
- ✅ 定时任务已设置（02:00 执行）
- ✅ 首次测试成功（5 个教程已生成）
- ✅ 教程索引已创建

## 下一步

1. **等待第一次自动执行**（明天 02:00）
2. **查看生成的教程质量**
3. **根据需要优化生成逻辑**
4. **创建教程精选合集**

---

**最后更新**: 2026-02-09
**版本**: v1.0
**状态**: ✅ 已完成并运行
