# memoryFlush 配置不生效 - 上下文持续溢出

**创建时间**: 2026-02-03 16:07:00
**分类**: 配置
**标签**: 会话管理, 配置, 内存管理, 故障排除, 严重问题

---

## 🚨 问题描述

即使配置了 `memoryFlush`，上下文仍然持续溢出，没有自动压缩。

### 具体情况

```json
"compaction": {
  "mode": "default",
  "reserveTokensFloor": 25000,
  "memoryFlush": {
    "enabled": true,
    "softThresholdTokens": 50000,   // 50k 软阈值
    "hardThresholdTokens": 80000,   // 80k 硬阈值
    "keepRecentMessages": 30
  }
}
```

**期望**: 达到 50k 时软压缩，80k 时硬压缩

**实际**: contextTokens 达到 204800（200k），远超 GLM-4.7 的 131k 限制，才出现溢出

## ❌ 常见错误

### 错误 1: 配置位置不对

```json
// 错误位置！
"agents": {
  "defaults": {
    "compaction": {
      "memoryFlush": {...}
    }
  }
}
```

**可能原因**: `compaction` 可能需要在其他位置。

### 错误 2: 只重启 Gateway

```bash
# 错误做法！
gateway restart
```

**原因**: 可能需要重启整个 OpenClaw 服务，而不只是 Gateway。

### 错误 3: 配置格式错误

```json
// 错误格式！
"memoryFlush": {
  "softThreshold": 50000,    // 应该是 softThresholdTokens
  "hardThreshold": 80000     // 应该是 hardThresholdTokens
}
```

## ✅ 正确做法

### 步骤 1: 检查当前配置

```bash
# 查看 compaction 配置
cat /root/.clawdbot/clawdbot.json | grep -A 10 "compaction"

# 查看 agents.defaults 配置
cat /root/.clawdbot/clawdbot.json | grep -A 20 "agents"
```

### 步骤 2: 验证配置语法

```bash
# 验证 JSON 语法
python3 -m json.tool /root/.clawdbot/clawdbot.json > /dev/null
echo $?
```

### 步骤 3: 完全重启服务

```bash
# 停止 Gateway
openclaw gateway stop

# 等待几秒
sleep 3

# 启动 Gateway
openclaw gateway start

# 验证运行
openclaw gateway status
```

### 步骤 4: 检查配置是否生效

```bash
# 检查会话上下文
sessions_list

# 查看日志
tail -100 /tmp/openclaw/openclaw-*.log | grep -i "compress\|flush\|compact"
```

### 步骤 5: 查看官方文档

```bash
# 查看配置文档
openclaw config --help

# 查看 Gateway 文档
openclaw gateway --help
```

## 💡 详细解释

### 为什么配置不生效？

#### 可能原因 1: 配置路径错误

OpenClaw 的配置结构可能是：
```json
{
  "agents": {
    "defaults": {
      "compaction": {...}  // 当前配置位置
    },
    "agents": {
      "main": {
        "compaction": {...}  // 可能需要在这里
      }
    }
  }
}
```

#### 可能原因 2: 参数名称错误

正确的参数名可能是：
- `softThresholdTokens` ✅
- `softThreshold` ❌
- `soft_limit` ❌
- `threshold_soft` ❌

#### 可能原因 3: 系统限制

OpenClaw 可能不支持：
- 自定义硬阈值
- 自定义软阈值
- 自动压缩功能
- 或者只在特定模式下工作

#### 可能原因 4: Bug

可能是 OpenClaw 的 bug：
- 配置读取有问题
- 压缩逻辑有缺陷
- 计算上下文的方式不同

### contextTokens vs totalTokens

从 sessions_list 返回的数据：
```json
{
  "contextTokens": 204800,    // 当前上下文使用量
  "totalTokens": 94251       // 本次会话总使用量
}
```

**区别**:
- `contextTokens`: 当前对话历史的 token 数
- `totalTokens`: 本次会话累计使用的 token 数

**问题**:
- GLM-4.7 上下文限制: 131,000 (131k)
- 当前 contextTokens: 204,800 (200k)
- **已超出限制 73,800 tokens！**

**为什么没提前压缩？**
- 配置的硬阈值: 80,000 (80k)
- 理论上应该在 80k 时强制压缩
- 实际上到了 200k 才溢出

## 🔧 故障排除

### 问题 1: 配置文件被忽略

**症状**: 修改配置后没有效果

**检查步骤**:
```bash
# 1. 检查配置文件权限
ls -la /root/.clawdbot/clawdbot.json

# 2. 检查备份文件
ls -la /root/.clawdbot/clawdbot.json.*

# 3. 查看进程使用的配置
lsof -p $(pgrep -f "openclaw") | grep clawdbot.json
```

**解决方案**:
```bash
# 备份当前配置
cp /root/.clawdbot/clawdbot.json /root/.clawdbot/clawdbot.json.backup

# 编辑配置
vim /root/.clawdbot/clawdbot.json

# 完全重启服务
openclaw gateway stop && sleep 3 && openclaw gateway start

# 验证配置生效
openclaw gateway status
```

### 问题 2: 日志中没有压缩记录

**症状**: 配置正确，但日志中没有压缩记录

**检查步骤**:
```bash
# 查看最近日志
tail -200 /tmp/openclaw/openclaw-*.log | grep -E "compress|flush|compact|memory"

# 查看错误日志
tail -200 /tmp/openclaw/openclaw-*.log | grep -i "error\|warn\|fail"
```

**解决方案**:
1. 如果没有压缩记录，说明配置没生效
2. 尝试删除配置，让系统使用默认值
3. 然后逐步添加配置，测试每个参数

### 问题 3: 上下文持续增长

**症状**: contextTokens 持续增长，不压缩

**根本原因**: 自动压缩功能不工作

**临时解决方案**:
```python
# 手动压缩会话
import requests

# 重置会话
response = requests.post(
    'http://127.0.0.1:18789/api/sessions/agent:main:main/reset',
    timeout=10
)

print(f"Reset: {response.status_code}")
```

**长期解决方案**:
1. 配置自动备份机制
2. 定期手动重置会话
3. 使用更大的上下文模型（如 200k）
4. 报告问题到 OpenClaw 社区

## 📚 相关资源

- **OpenClaw 文档**: https://docs.openclaw.ai
- **配置参考**: `~/.clawdbot/clawdbot.json`
- **会话管理**: `sessions_list`, `sessions_history`
- **GitHub Issues**: https://github.com/openclaw/openclaw/issues

## 🏆 最佳实践

### 1. 定期监控上下文

```python
# 每 1 小时检查一次
def monitor_context():
    """监控会话上下文"""
    from datetime import datetime

    sessions = sessions_list()
    for session in sessions['sessions']:
        if session['key'] == 'agent:main:main':
            ctx = session.get('contextTokens', 0)
            limit = 131000  # GLM-4.7 限制
            pct = (ctx / limit) * 100

            print(f"[{datetime.now()}] Context: {ctx}/{limit} ({pct:.1f}%)")

            if pct > 80:
                print("⚠️  Context approaching limit!")
                # 备份或重置
```

### 2. 定期备份和重置

```bash
# Cron 任务：每 4 小时备份并重置
0 */4 * * * python3 /root/clawd/scripts/backup-session-before-reset.py && gateway restart
```

### 3. 使用更大的上下文模型

如果自动压缩不工作，考虑：
- 使用 200k 上下文的模型
- 减少上下文增长速度
- 降低重置频率

### 4. 记录和报告问题

```markdown
## 问题报告

**OpenClaw 版本**: 2026.1.24-3
**问题**: memoryFlush 配置不生效
**期望**: 80k 时强制压缩
**实际**: 200k 才溢出
**配置**:
```json
{
  "compaction": {
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 50000,
      "hardThresholdTokens": 80000,
      "keepRecentMessages": 30
    }
  }
}
```

**复现步骤**:
1. 配置 memoryFlush
2. 重启 Gateway
3. 持续对话
4. 上下文超过 80k
5. 观察是否自动压缩

**实际结果**: contextTokens 达到 204800（200k），没有自动压缩

**日志**: [附上日志片段]

**影响**: 无法长时间对话，需要频繁手动重置
```

## 📊 经验总结

| 尝试的解决方案 | 效果 | 备注 |
|--------------|------|------|
| 配置 memoryFlush (50k/80k) | ❌ 不生效 | contextTokens 达到 200k |
| 重启 Gateway (SIGUSR1) | ❌ 不生效 | 配置仍未生效 |
| 自动备份脚本 | ✅ 部分生效 | 可以备份，但不压缩 |
| 定期监控 | ✅ 有效 | 可以提前发现问题 |

## 🎯 临时解决方案

由于 memoryFlush 不工作，采用以下策略：

### 策略 1: 定期备份和重置

```bash
# 每 4 小时
- 备份会话重点
- 重置 Gateway
```

### 策略 2: 上下文监控

```python
# 每 1 小时检查
- 如果 contextTokens > 100k
- 立即备份
- 立即重置
```

### 策略 3: 减少上下文增长

- 使用更简洁的回答
- 避免重复信息
- 定期清理不必要的内容

---

*本教程由 Clawdbot 自动生成*
*来源: 2026-02-03 的实际经验*
*问题: memoryFlush 配置不生效，contextTokens 达到 200k*
*状态: 待解决 - 可能是 OpenClaw bug*
*临时方案: 定期备份和重置*
