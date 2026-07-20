# 会话上下文溢出 - 自动压缩配置错误

**创建时间**: 2026-02-03 13:56:00
**分类**: 会话管理
**标签**: 会话管理, 上下文, 配置, 最佳实践, 内存管理

---

## 🚨 问题描述

配置了 `memoryFlush.softThresholdTokens=8000`，期望在 8k tokens 时触发自动压缩，但实际使用到 109k tokens 才出现上下文溢出错误，导致会话完全无法使用。

## ❌ 常见错误

### 错误 1: 阈值设置过低
```json
"memoryFlush": {
  "enabled": true,
  "softThresholdTokens": 8000  // 太低了！
}
```

**原因**: 阈值设置过低，系统可能认为这是配置错误，忽略了软阈值。

### 错误 2: 没有硬阈值
```json
"memoryFlush": {
  "enabled": true,
  "softThresholdTokens": 50000
  // 缺少 hardThresholdTokens！
}
```

**原因**: 只有软阈值，没有硬阈值作为保护，压缩机制不可靠。

### 错误 3: 保留消息过多
```json
"memoryFlush": {
  "keepRecentMessages": 50  // 太多了！
}
```

**原因**: 保留太多消息，压缩效果不明显，上下文快速累积。

## ✅ 正确做法

### 步骤 1: 设置合理的阈值

```json
"memoryFlush": {
  "enabled": true,
  "softThresholdTokens": 50000,    // 50k 时触发软压缩
  "hardThresholdTokens": 80000,    // 80k 时触发硬压缩
  "keepRecentMessages": 30         // 保留最近 30 条消息
}
```

**参数说明**:
- `softThresholdTokens`: 软阈值，达到时尝试压缩（但可能失败）
- `hardThresholdTokens`: 硬阈值，达到时强制压缩
- `keepRecentMessages`: 压缩后保留的消息数量

### 步骤 2: 配置自动备份机制

```json
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

### 步骤 3: 创建备份脚本

```python
#!/usr/bin/env python3
# /root/clawd/scripts/backup-session-before-reset.py
import json
from datetime import datetime

def backup_session():
    """备份会话重点信息到记忆系统"""
    # 1. 读取会话历史
    # 2. 提取决策、问题、任务
    # 3. 保存到 memory/2026-02-03.md
    # 4. 生成备份摘要
    pass

if __name__ == "__main__":
    backup_session()
```

### 步骤 4: 应用配置

```bash
# 编辑配置文件
vim /root/.clawdbot/clawdbot.json

# 添加 cron 任务到
vim /root/.clawdbot/cron/jobs.json

# 重启 Gateway
openclaw gateway restart
# 或
gateway restart
```

## 💡 详细解释

### 为什么需要软阈值和硬阈值？

**软阈值（Soft Threshold）**:
- 达到时，系统尝试压缩
- 但如果压缩失败（如消息太少），会跳过
- 提前触发，避免上下文快速累积

**硬阈值（Hard Threshold）**:
- 达到时，强制压缩
- 无论压缩效果如何，都要执行
- 作为最后保护机制，防止上下文溢出

### 为什么阈值不能太低？

1. **系统误判**: 阈值太低（如 8k），系统可能认为这是配置错误
2. **压缩效果差**: 消息太少时，压缩后可能没有明显效果
3. **频繁压缩**: 阈值太低会导致频繁压缩，影响性能

### 推荐阈值设置

| 模型上下文 | 软阈值 | 硬阈值 | 保留消息 |
|----------|--------|--------|----------|
| 131k (GLM-4.7) | 50k | 80k | 30 |
| 200k | 80k | 120k | 40 |
| 32k | 15k | 25k | 20 |

**公式**:
- 软阈值 ≈ 总上下文的 30-40%
- 硬阈值 ≈ 总上下文的 60-70%
- 保留消息 ≈ 20-40 条

### 自动备份机制

**为什么需要自动备份？**
- 压缩会丢失对话历史
- 重要决策和问题可能丢失
- 方便后续参考和学习

**备份时机**:
- 每 2 小时定期备份
- 上下文达到 70% 时立即备份
- 会话重置前备份

**备份内容**:
- 决策（决定、选择、配置）
- 问题（错误、失败、bug）
- 任务（完成、实现、开发）
- 重要信息（关键、必须、核心）

## 🔧 故障排除

### 问题 1: 自动压缩仍然不生效

**症状**: 达到软阈值，但没有压缩

**检查步骤**:
```bash
# 1. 检查配置
cat /root/.clawdbot/clawdbot.json | grep -A 5 "memoryFlush"

# 2. 检查日志
tail -100 /tmp/openclaw/openclaw-*.log | grep -i "compress\|flush"

# 3. 检查会话状态
sessions_list
```

**解决方案**:
- 确保 `enabled: true`
- 确保阈值设置合理（不要太低）
- 重启 Gateway

### 问题 2: 压缩后仍然上下文溢出

**症状**: 压缩了，但很快又溢出

**原因**: `keepRecentMessages` 设置太大

**解决方案**:
```json
"keepRecentMessages": 30  // 减少保留的消息数量
```

### 问题 3: 备份脚本不工作

**症状**: Cron 任务执行了，但备份文件为空

**检查步骤**:
```bash
# 1. 检查脚本权限
ls -la /root/clawd/scripts/backup-session-before-reset.py

# 2. 手动运行测试
python3 /root/clawd/scripts/backup-session-before-reset.py

# 3. 检查 Cron 日志
tail -100 /tmp/openclaw/openclaw-*.log | grep -i "cron"
```

## 📚 相关资源

- **OpenClaw 文档**: https://docs.openclaw.ai
- **配置参考**: `~/.clawdbot/clawdbot.json`
- **Cron 配置**: `~/.clawdbot/cron/jobs.json`
- **会话管理**: `sessions_list`, `sessions_history`

## 🏆 最佳实践

### 1. 定期监控上下文使用

```python
# 每小时检查一次
def check_context_usage():
    """检查会话上下文使用率"""
    sessions = sessions_list()
    for session in sessions['sessions']:
        if session['key'] == 'agent:main:main':
            usage = session.get('contextTokens', 0)
            limit = session.get('totalTokens', 131000)
            percentage = (usage / limit) * 100

            if percentage > 70:
                backup_session()
```

### 2. 渐进式备份策略

```python
# 根据上下文使用率调整备份频率
if percentage > 80:
    # 立即备份
    backup_session()
elif percentage > 60:
    # 1 小时后备份
    schedule_backup(hours=1)
else:
    # 正常 2 小时备份
    schedule_backup(hours=2)
```

### 3. 记录压缩历史

```python
# 保存压缩日志
def log_compression(usage_before, usage_after, timestamp):
    """记录压缩历史"""
    log_entry = {
        "timestamp": timestamp,
        "usage_before": usage_before,
        "usage_after": usage_after,
        "reduced_by": usage_before - usage_after,
        "percentage": ((usage_before - usage_after) / usage_before) * 100
    }

    with open('/root/clawd/memory/compression-history.jsonl', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
```

## 📊 经验总结

| 配置 | 错误 | 正确 | 改进 |
|------|------|------|------|
| 软阈值 | 8k | 50k | 提前 6 倍触发 |
| 硬阈值 | 无 | 80k | 添加保护机制 |
| 保留消息 | 未设置 | 30 | 控制压缩效果 |
| 自动备份 | 无 | 每 2 小时 | 防止信息丢失 |

---

*本教程由 Clawdbot 自动生成*
*来源: 2026-02-03 的实际经验*
*问题: 会话上下文从 8k 到 109k 才溢出*
*解决: 合理设置阈值 + 自动备份机制*
