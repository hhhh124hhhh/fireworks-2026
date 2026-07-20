# Clawdbot 命令参考

## 核心命令速查

### Gateway 管理
```bash
clawdbot gateway status     # 查看 Gateway 状态
clawdbot gateway start      # 启动 Gateway 服务
clawdbot gateway stop       # 停止 Gateway 服务
clawdbot gateway restart    # 重启 Gateway 服务
clawdbot gateway health     # 获取 Gateway 健康信息
```

### 系统状态
```bash
clawdbot status             # 显示频道健康和会话摘要
clawdbot status --all       # 完整诊断（只读）
clawdbot status --json      # 机器可读输出
clawdbot status --deep      # 运行频道探测
```

### 日志查看
```bash
clawdbot logs               # 查看日志
clawdbot logs --follow      # 实时跟踪日志
clawdbot logs --limit 100   # 限制行数
```

### Agent 执行
```bash
clawdbot agent --to <number> --message "消息"    # 向特定号码发送消息
clawdbot agent --agent <id> --message "消息"     # 使用特定 agent
clawdbot agent --session-id <id> --message "msg" # 向特定会话发送
clawdbot agent --local                           # 本地运行 embedded agent
```

### 消息发送
```bash
clawdbot message send --target <target> --message "消息" --channel <channel>
```

### 内存管理
```bash
clawdbot memory search "关键词"     # 搜索内存
```

### 技能管理
```bash
clawdbot skills list         # 列出所有技能
clawdbot skills add <path>   # 添加技能
```

### Cron 任务
```bash
clawdbot cron list           # 列出 cron 任务
clawdbot cron add            # 添加 cron 任务
clawdbot cron run <id>       # 运行 cron 任务
```

## 当前系统信息

### Gateway
- **地址**: ws://127.0.0.1:18789
- **状态**: 本地运行，可访问
- **认证**: 使用 token
- **机器**: i-6978a0478084e255a79deb58 (10.198.0.131)

### 配置的频道
- **Slack**: ON (OK) - tokens ok
- **Feishu**: ON (OK) - configured

### 会话统计
- 总会话数: 9
- 活跃会话: 9
- 默认模型: glm-4.7 (205k context)

### 安全注意事项
- Reverse proxy headers 未受信任
- Extensions 存在但 plugins.allow 未设置

## 常用模式

### 查看 Gateway 日志
```bash
clawdbot logs --follow
```

### 测试频道连接
```bash
clawdbot status --deep
```

### 发送消息到 Slack
```bash
clawdbot message send --channel slack --target "#channel" --message "消息"
```

### 获取使用统计
```bash
clawdbot gateway usage-cost
```

## 错误排查

### 如果 Gateway 未运行
```bash
clawdbot gateway start
```

### 如果无法连接
```bash
clawdbot gateway probe
```

### 如果需要完整诊断
```bash
clawdbot status --all
```
