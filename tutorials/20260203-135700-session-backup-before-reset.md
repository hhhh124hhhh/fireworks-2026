# 会话重置前备份 - 防止信息丢失

**创建时间**: 2026-02-03 13:57:00
**分类**: 会话管理
**标签**: 会话管理, 备份, 记忆系统, 数据保护

---

## 🚨 问题描述

直接重置会话会丢失所有对话历史和重要信息，包括：
- 重要的决策
- 未解决的问题
- 正在进行的任务
- 有价值的讨论

## ❌ 常见错误

### 错误 1: 直接重置会话

```bash
# 错误做法！
curl -X POST http://127.0.0.1:18789/api/sessions/agent:main:main/reset
# 或
openclaw session reset
```

**原因**: 会话重置会清空所有对话历史，没有任何备份。

### 错误 2: 手动复制粘贴

```bash
# 错误做法！手动复制整个对话历史到文件
```

**原因**:
- 耗时且容易遗漏
- 没有结构化
- 不易检索和管理

### 错误 3: 依赖自动压缩

```json
// 错误做法！
"memoryFlush": {
  "enabled": true
}
// 认为自动压缩就够了
```

**原因**: 自动压缩会删除旧消息，但不会提取重点信息。

## ✅ 正确做法

### 步骤 1: 创建备份脚本

```python
#!/usr/bin/env python3
"""
会话备份工具 - 重置前提取重点到记忆系统
"""
import json
import sys
import os
from datetime import datetime

# 配置
SESSION_KEY = "agent:main:main"
MEMORY_DIR = "/root/clawd/memory"
DATE = datetime.now().strftime("%Y-%m-%d")
MEMORY_FILE = f"{MEMORY_DIR}/{DATE}.md"

def extract_keywords(text):
    """提取关键词内容"""
    # 决策关键词
    decision_keywords = ['决定', '选择', '配置', '设置', '部署', '创建', '修改', '更新']
    # 问题关键词
    problem_keywords = ['问题', '错误', '失败', 'bug', '修复', '解决', '异常']
    # 任务关键词
    task_keywords = ['任务', '完成', '实现', '开发', '创建', '生成']
    # 重要关键词
    important_keywords = ['重要', '关键', '必须', '核心', '主要']

    decisions = []
    problems = []
    tasks = []
    important = []

    for kw in decision_keywords:
        if kw in text.lower():
            decisions.append(kw)

    for kw in problem_keywords:
        if kw in text.lower():
            problems.append(kw)

    for kw in task_keywords:
        if kw in text.lower():
            tasks.append(kw)

    for kw in important_keywords:
        if kw in text.lower():
            important.append(kw)

    return {
        'decisions': decisions,
        'problems': problems,
        'tasks': tasks,
        'important': important
    }

def backup_session():
    """备份会话重点信息"""
    # 1. 获取会话历史
    # 使用 sessions_history API
    # 或读取会话文件

    # 2. 提取重点信息
    messages = [...]  # 从 API 或文件读取

    # 3. 分类和提取
    for msg in messages:
        content = msg.get('content', '')
        keywords = extract_keywords(content)

        # 4. 生成备份摘要
        # ...

    # 5. 保存到记忆系统
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(backup_content)

    print(f"✅ 备份完成: {MEMORY_FILE}")

if __name__ == "__main__":
    backup_session()
```

**保存位置**: `/root/clawd/scripts/backup-session-before-reset.py`

### 步骤 2: 运行备份脚本

```bash
# 方法 1: 手动运行
python3 /root/clawd/scripts/backup-session-before-reset.py

# 方法 2: 通过 cron 自动运行
# 添加到 ~/.clawdbot/cron/jobs.json
{
  "id": "session-backup-2h",
  "name": "会话自动备份（每2小时）",
  "schedule": {
    "kind": "cron",
    "expr": "0 */2 * * *",
    "timezone": "Asia/Shanghai"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "运行会话备份脚本"
  },
  "enabled": true
}
```

### 步骤 3: 验证备份

```bash
# 查看备份文件
tail -50 /root/clawd/memory/2026-02-03.md

# 查看备份日志
tail -20 /root/clawd/memory/backup-2026-02-03.log
```

### 步骤 4: 重置会话

```bash
# 确认备份成功后，重置会话
gateway restart
```

## 💡 详细解释

### 为什么需要备份？

1. **防止信息丢失**
   - 对话历史包含重要决策
   - 未解决的问题和 bug
   - 正在进行的任务
   - 有价值的讨论和见解

2. **便于后续参考**
   - 快速查找之前的决策
   - 了解问题解决过程
   - 学习最佳实践

3. **知识积累**
   - 构建个人知识库
   - 记录学习路径
   - 形成系统记忆

### 备份什么？

#### 重点分类

1. **决策** (🎯)
   - 重要的决定
   - 技术选择
   - 配置变更
   - 部署决策

2. **问题** (🔧)
   - 遇到的错误
   - 失败的尝试
   - 未解决的 bug
   - 需要修复的问题

3. **任务** (✅)
   - 完成的任务
   - 进行中的工作
   - 待办事项
   - 实现的功能

4. **重要信息** (⭐)
   - 关键发现
   - 重要提醒
   - 核心概念
   - 主要要点

#### 备份格式

```markdown
## 🔄 会话备份 (13:51:09)

**备份时间**: 2026-02-03 13:51:09
**会话**: agent:main:main

### ⭐ 重要信息 (1 项)
1. 确保下次不会溢出并且还能记忆

### 🎯 决策 (2 项)
1. 自己配置自动备份和压缩机制
2. 创建会话备份脚本

### 🔧 问题 (2 项)
1. 会话上下文溢出问题需要解决
2. zai 模型冷却状态

### ✅ 任务 (3 项)
1. 配置自动备份和压缩机制
2. 创建会话备份脚本
3. 备份后重启 Gateway

### 📊 统计
- 总消息数: 100
- 决策数: 15
- 问题数: 8
- 任务数: 22
```

### 何时备份？

#### 定期备份
- 每 2 小时一次
- 防止信息丢失

#### 触发式备份
- 上下文使用率超过 70%
- 检测到重要讨论
- 完成重要任务

#### 手动备份
- 会话重置前
- 完成重要工作后
- 学习新知识后

### 如何检索备份？

#### 查看单个日期
```bash
cat /root/clawd/memory/2026-02-03.md
```

#### 搜索特定主题
```bash
grep -n "会话上下文" /root/clawd/memory/*.md
```

#### 使用 Memory Manager
```bash
python3 /root/clawd/scripts/memory-manager.py search "关键词"
```

## 🔧 故障排除

### 问题 1: 备份文件为空

**症状**: 运行脚本成功，但文件为空

**检查步骤**:
```bash
# 1. 检查脚本权限
ls -la /root/clawd/scripts/backup-session-before-reset.py

# 2. 手动运行并查看错误
python3 /root/clawd/scripts/backup-session-before-reset.py

# 3. 检查日志
tail -50 /root/clawd/memory/backup-*.log
```

**解决方案**:
- 确保 Python 3 可用
- 确保有读取会话的权限
- 检查 API 连接

### 问题 2: 备份内容不完整

**症状**: 只备份了部分信息

**原因**: 关键词匹配不完善

**解决方案**:
- 扩充关键词列表
- 使用 LLM 智能提取（如果可用）
- 调整匹配逻辑

### 问题 3: 备份文件过大

**症状**: 备份文件增长太快

**解决方案**:
- 限制备份的条目数量
- 定期清理旧备份
- 使用增量备份

## 📚 相关资源

- **Memory Manager**: `/root/clawd/scripts/memory-manager.py`
- **会话管理**: `sessions_list`, `sessions_history`
- **记忆系统**: `/root/clawd/memory/`
- **Cron 配置**: `~/.clawdbot/cron/jobs.json`

## 🏆 最佳实践

### 1. 备份验证清单

- [ ] 备份文件已创建
- [ ] 包含重要决策
- [ ] 包含未解决的问题
- [ ] 包含进行的任务
- [ ] 文件大小合理（几 KB 到几十 KB）
- [ ] 可以正常读取

### 2. 备份命名规范

```
/root/clawd/memory/YYYY-MM-DD.md
/root/clawd/memory/backup-YYYY-MM-DD.log
/root/clawd/memory/compression-history.jsonl
```

### 3. 备份频率策略

```python
# 根据上下文使用率动态调整
def get_backup_interval(usage_percentage):
    """根据上下文使用率获取备份间隔"""
    if usage_percentage > 80:
        return "immediate"  # 立即备份
    elif usage_percentage > 60:
        return 3600        # 1 小时
    else:
        return 7200        # 2 小时
```

### 4. 备份保留策略

```python
# 保留最近 7 天的备份
def cleanup_old_backups():
    """清理旧备份"""
    from datetime import timedelta

    cutoff_date = datetime.now() - timedelta(days=7)

    for file in os.listdir(MEMORY_DIR):
        if file.endswith('.md'):
            file_date = datetime.strptime(file[:10], '%Y-%m-%d')
            if file_date < cutoff_date:
                os.remove(os.path.join(MEMORY_DIR, file))
```

## 📊 经验总结

| 场景 | 错误做法 | 正确做法 | 改进 |
|------|----------|----------|------|
| 会话重置 | 直接重置 | 先备份再重置 | 防止信息丢失 |
| 手动备份 | 复制粘贴 | 使用脚本 | 自动化、结构化 |
| 备份内容 | 所有消息 | 只备份重点 | 减少冗余 |
| 备份频率 | 不定期 | 每 2 小时 | 及时性 |
| 备份检索 | 手动搜索 | 使用工具 | 高效便捷 |

---

*本教程由 Clawdbot 自动生成*
*来源: 2026-02-03 的实际经验*
*问题: 重置会话丢失重要信息*
*解决: 创建备份脚本 + 自动化机制*
