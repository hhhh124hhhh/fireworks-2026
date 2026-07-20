# 会话上下文溢出教程

## 1. 问题描述

在使用 Clawdbot/Momo 系统时，配置了 `memoryFlush.softThresholdTokens=8000`，但实际使用时直到达到 109k tokens 才发生溢出。自动压缩机制没有按预期生效，导致会话完全溢出后才触发处理。

**典型症状：**
- 配置的软阈值（8k tokens）被忽略
- 会话增长到超过 100k tokens
- 自动压缩未触发
- 性能显著下降
- 最终触发硬性限制导致错误

## 2. 常见错误及原因

### 错误 1：软阈值设置过低
**现象：** 设置 `softThresholdTokens=8000`，但实际使用时完全被忽略

**原因：**
1. 软阈值低于系统最小生效阈值（通常需要 10k+）
2. 硬阈值未设置或设置过高
3. 系统优先使用硬阈值，软阈值仅为建议值
4. 内存压缩算法需要足够的历史记录才能工作

### 错误 2：只配置软阈值，未配置硬阈值
**现象：** 会话持续增长直到达到模型最大限制

**原因：**
- 系统在没有硬阈值的情况下，不会触发任何压缩
- 软阈值只是一个"建议"，没有强制执行机制
- 只有达到硬阈值时才会执行压缩或重置

### 错误 3：未启用自动备份机制
**现象：** 会话重置后丢失重要信息

**原因：**
- 系统默认不启用自动备份
- 配置中缺少备份相关的设置
- 没有配置备份存储路径

### 错误 4：混淆 token 估算方法
**现象：** 实际使用量远超预期

**原因：**
- 使用字符数而非 token 数来估算
- 不同模型的 token 计算方式不同
- 忽略了系统提示词和工具调用占用的 token

## 3. 正确做法（详细步骤）

### 步骤 1：检查当前配置

```bash
# 查看当前内存管理配置
cat ~/.clawd/config.json | grep -A 10 memoryFlush

# 或查看环境变量
env | grep MEMORY_
```

### 步骤 2：设置合理的阈值

编辑配置文件（`~/.clawd/config.json` 或相关配置文件）：

```json
{
  "memoryFlush": {
    "softThresholdTokens": 50000,
    "hardThresholdTokens": 80000,
    "compressionRatio": 0.6,
    "autoBackup": true,
    "backupPath": "~/.clawd/memory/backups/"
  }
}
```

**阈值选择原则：**
- **软阈值**：建议设置为硬阈值的 60-70%（50k tokens）
- **硬阈值**：建议设置为模型最大限制的 60-70%（80k tokens）
- **留有余地**：为系统提示词、工具调用留出 20-30% 空间

### 步骤 3：启用自动备份

确保配置中包含备份设置：

```json
{
  "memoryFlush": {
    "autoBackup": true,
    "backupPath": "/root/clawd/memory/backups/",
    "backupFormat": "json",
    "keepBackups": 10,
    "backupOnFlush": true
  }
}
```

### 步骤 4：创建备份目录

```bash
# 创建备份目录
mkdir -p /root/clawd/memory/backups/

# 设置权限
chmod 755 /root/clawd/memory/backups/
```

### 步骤 5：验证配置

```bash
# 重启服务以应用新配置
openclaw gateway restart

# 检查服务状态
openclaw gateway status

# 查看日志确认配置生效
tail -f /var/log/clawd/gateway.log | grep -i memory
```

### 步骤 6：测试阈值机制

```bash
# 使用测试会话验证阈值是否生效
# 可以通过长时间对话来触发软阈值
# 观察日志中是否有压缩相关的消息
```

### 步骤 7：监控 token 使用量

```bash
# 定期检查 token 使用情况
# 可以通过 API 或日志查看当前会话大小
tail -f /var/log/clawd/gateway.log | grep -i token
```

## 4. 详细解释（为什么这样做）

### 为什么软阈值需要设置得足够高？

**Token 计算的复杂性：**
1. **不同模型的 token 计算方式不同**
   - GPT-4: 约 1 token ≈ 4 个字符（英文）
   - GLM-4: 约 1 token ≈ 2-3 个字符（中文）
   - 实际使用中，中英文混合会变化

2. **系统开销**
   - 系统提示词：通常占用 1k-5k tokens
   - 工具调用：每次调用增加 500-2k tokens
   - 上下文管理：额外的元数据占用

3. **压缩算法的需要**
   - 压缩算法需要足够的历史记录才能有效工作
   - 太低的阈值会导致压缩后的上下文质量下降
   - 建议 50k+ tokens 才有足够的上下文进行有效压缩

### 为什么硬阈值要设置为 80k？

**模型限制考虑：**
1. **GLM-4.7 最大上下文：131k tokens**
   - 硬阈值 80k 留有 51k 余量（39%）
   - 为长任务和复杂查询留出空间

2. **性能考虑**
   - 上下文越长，响应速度越慢
   - 80k tokens 是性能和容量的平衡点
   - 避免超过 100k 后响应时间急剧增加

3. **稳定性考虑**
   - 避免 100k+ tokens 的边界情况
   - 预留空间处理突发性长请求

### 为什么需要自动备份？

**数据安全：**
1. **信息丢失风险**
   - 会话压缩可能丢失重要信息
   - 决策、任务、问题等关键信息需要保留
   - 历史对话用于分析和改进

2. **恢复能力**
   - 出错时可以从备份恢复
   - 可以回溯之前的决策
   - 支持会话重建

### 压缩比 0.6 的含义

**压缩策略：**
- 0.6 表示压缩后保留 60% 的内容
- 智能保留：优先保留重要信息（决策、任务、关键对话）
- 丢弃：重复内容、闲聊、低价值信息

## 5. 故障排除

### 问题 1：配置修改后未生效

**症状：** 修改配置后，会话仍然溢出到 100k+ tokens

**排查步骤：**
```bash
# 1. 确认配置文件语法正确
cat ~/.clawd/config.json | python3 -m json.tool

# 2. 检查服务是否重启
openclaw gateway restart

# 3. 查看日志确认配置加载
grep -i "memoryFlush\|threshold" /var/log/clawd/gateway.log

# 4. 检查环境变量是否覆盖配置
env | grep -i memory
```

**解决方案：**
- 确保 JSON 格式正确
- 重启服务以加载新配置
- 检查是否有环境变量覆盖了配置文件
- 清除缓存：`rm -rf ~/.cache/clawd/`

### 问题 2：压缩后的会话质量下降

**症状：** 压缩后，机器人忘记之前的重要信息

**排查步骤：**
```bash
# 1. 检查压缩日志
grep -i "compress\|flush" /var/log/clawd/gateway.log

# 2. 查看备份文件
ls -la /root/clawd/memory/backups/

# 3. 检查压缩比设置
cat ~/.clawd/config.json | grep compressionRatio
```

**解决方案：**
- 增加 `compressionRatio` 到 0.7 或 0.8
- 调高软阈值，减少压缩频率
- 确保启用备份机制
- 手动标记重要信息（如果系统支持）

### 问题 3：备份文件未生成

**症状：** `autoBackup` 设置为 true，但备份目录为空

**排查步骤：**
```bash
# 1. 检查备份目录权限
ls -la /root/clawd/memory/backups/

# 2. 检查磁盘空间
df -h /root/clawd/memory/backups/

# 3. 查看备份相关错误日志
grep -i "backup\|error" /var/log/clawd/gateway.log
```

**解决方案：**
- 确保备份目录有写权限
- 检查磁盘空间是否充足
- 修正备份路径配置
- 手动测试备份功能

### 问题 4：Token 计数不准确

**症状：** 显示的 token 数与实际不符

**排查步骤：**
```bash
# 1. 使用 tokenizer 工具验证
# 需要安装对应的 tokenizer 工具

# 2. 对比不同会话的 token 使用
# 通过 API 获取实际的 token 计数

# 3. 检查日志中的 token 统计
grep -i "tokens\|usage" /var/log/clawd/gateway.log
```

**解决方案：**
- 使用官方 tokenizer 工具验证
- 考虑不同模型之间的差异
- 使用保守估计（宁可多算）
- 定期校准 token 计数

## 6. 相关资源

### 官方文档
- OpenClaw 配置文档（如果存在）
- GLM-4.7 模型文档
- Token 计算工具

### 工具和脚本
- Token 计算器：https://platform.openai.com/tokenizer（用于参考）
- JSON 配置验证：`python3 -m json.tool`
- 日志查看：`tail -f`, `grep`, `journalctl`

### 配置文件位置
- 主配置：`~/.clawd/config.json`
- 环境变量：`~/.bashrc`, `~/.env.d/`
- 日志文件：`/var/log/clawd/gateway.log`
- 备份目录：`/root/clawd/memory/backups/`

### 相关技能
- `memory-management`（如果存在）
- `clawd-config`（如果存在）

## 7. 最佳实践

### 配置管理

**1. 版本控制配置文件**
```bash
# 使用 git 管理配置
cd ~/.clawd
git init
git add config.json
git commit -m "Initial memory flush config"
```

**2. 配置文件分离**
```
~/.clawd/
├── config.json              # 基础配置
├── config.memory.json       # 内存管理配置
├── config.backup.json       # 备份配置
└── env/                     # 环境特定配置
    ├── development.json
    └── production.json
```

**3. 使用环境变量覆盖敏感配置**
```bash
# 在 ~/.env.d/clawd 中设置
export CLAWD_MEMORY_HARD_THRESHOLD=80000
export CLAWD_MEMORY_SOFT_THRESHOLD=50000
export CLAWD_BACKUP_PATH=/root/clawd/memory/backups/
```

### 监控和告警

**1. 定期检查会话大小**
```bash
# 创建监控脚本
cat > /root/clawd/scripts/check-session-size.sh << 'EOF'
#!/bin/bash
MAX_TOKENS=70000
CURRENT=$(curl -s http://localhost:3000/api/session/size | jq '.tokens')

if [ $CURRENT -gt $MAX_TOKENS ]; then
    echo "WARNING: Session size $CURRENT tokens exceeds threshold $MAX_TOKENS"
    # 发送通知（通过您偏好的方式）
fi
EOF

chmod +x /root/clawd/scripts/check-session-size.sh
```

**2. 定期清理备份**
```bash
# 保留最近 10 个备份，删除旧的
find /root/clawd/memory/backups/ -name "*.json" -type f -printf '%T+ %p\n' | sort -r | tail -n +11 | cut -d' ' -f2- | xargs rm -f
```

**3. 日志轮转**
```bash
# 配置 logrotate
cat > /etc/logrotate.d/clawd << 'EOF'
/var/log/clawd/gateway.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
EOF
```

### 使用建议

**1. 定期备份关键对话**
```bash
# 手动备份当前会话
curl -s http://localhost:3000/api/session/export > /root/clawd/memory/manual-backup-$(date +%Y%m%d-%H%M%S).json
```

**2. 重要信息标记**
- 在对话中使用特殊标记重要信息
- 例如：`[重要]`, `[决策]`, `[待办]`
- 配置压缩算法优先保留这些标记

**3. 定期检查和调整**
- 每月审查 token 使用情况
- 根据实际使用调整阈值
- 监控压缩后的会话质量

**4. 性能优化**
- 对于频繁使用的场景，考虑使用更激进的压缩
- 对于长任务，临时提高阈值
- 使用不同的会话处理不同类型的任务

**5. 文档记录**
```bash
# 在配置文件中添加注释
cat >> ~/.clawd/config.memory.json << 'EOF'
{
  "_comment": "Memory flush configuration - updated 2026-02-03",
  "memoryFlush": {
    "softThresholdTokens": 50000,
    "softThresholdReason": "60% of hard threshold, ensures enough context for compression",
    "hardThresholdTokens": 80000,
    "hardThresholdReason": "60% of GLM-4.7 max (131k), leaves room for long queries"
  }
}
EOF
```

### 避免的陷阱

**1. 不要设置过低的软阈值**
- ❌ `softThresholdTokens: 5000`
- ✅ `softThresholdTokens: 50000`

**2. 不要忽视硬阈值**
- ❌ 只设置软阈值，不设置硬阈值
- ✅ 同时设置软阈值和硬阈值

**3. 不要关闭自动备份**
- ❌ `autoBackup: false`
- ✅ `autoBackup: true` + 定期手动备份

**4. 不要依赖默认配置**
- ❌ 使用系统默认值
- ✅ 根据实际使用场景配置

**5. 不要忽略日志**
- ❌ 从不查看日志
- ✅ 定期检查日志，监控会话状态

---

**总结：**
合理配置内存管理参数是确保 Clawdbot/Momo 稳定运行的关键。设置 50k 软阈值和 80k 硬阈值，启用自动备份，并定期监控会话状态，可以有效避免会话溢出问题，同时保持良好的对话质量和系统性能。

**最后更新：** 2026-02-03
**作者：** Clawdbot Tutorial Generator
**版本：** 1.0
