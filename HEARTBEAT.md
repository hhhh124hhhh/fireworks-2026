# HEARTBEAT.md - 心跳检查配置

## 上下文清理策略（优先级最高）
- **定时清理**: 每天 2 次（2:00, 14:00） - 通过 cron 自动执行
- **阈值清理**: 超过 50% 时自动触发 - 在 heartbeat 中执行
- **清理脚本**: `/root/clawd/scripts/backup-and-flush-memory.sh`
- **检查脚本**: `/root/clawd/scripts/check-context-usage.sh`
- **状态跟踪**: `/root/clawd/memory/heartbeat-state.json`

### 清理触发时机
1. **定时清理**（自动）：
   - 每天 2:00 和 14:00
   - 无条件执行

2. **阈值清理**（智能）：
   - 每次 heartbeat 时检查
   - 估算使用率超过 50% 时触发
   - 避免一天内清理太频繁

3. **手动清理**（可选）：
   - 随时可以手动运行清理脚本
   - `bash /root/clawd/scripts/backup-and-flush-memory.sh`

## 心跳检查流程

### 第 1 步：上下文使用率检查（优先）
```bash
# 检查当前上下文使用率
bash /root/clawd/scripts/check-context-usage.sh

# 这个脚本会：
# 1. 估算上下文使用率
# 2. 如果超过 50%，自动触发清理
# 3. 记录到日志
```

### 第 2 步：深夜模式检查
- **安静时段**: 23:00 - 07:00 (Asia/Shanghai)
- **通知渠道**: 飞书和 Slack
- **当前时间检查**: 在执行任何通知任务前，先检查当前时间

## 时间判断逻辑
```python
import datetime
from datetime import timezone

def is_night_mode():
    """判断当前是否在深夜模式（23:00-07:00）"""
    now = datetime.datetime.now(timezone.utc).astimezone(
        datetime.timezone(datetime.timedelta(hours=8))
    )
    hour = now.hour
    return hour >= 23 or hour < 7

def should_notify():
    """判断当前时间是否可以发送通知"""
    return not is_night_mode()
```

## 深夜模式检查流程

### 心跳接收时的处理
1. **先运行上下文使用率检查**（优先级最高）
2. 如果超过 50%，触发清理
3. 然后运行深夜模式检查
4. 如果返回非零码（深夜模式），则：
   - 记录到日志："[时间] 深夜模式，跳过通知"
   - 回复：HEARTBEAT_OK
   - 不执行任何通知相关的检查
5. 如果返回零码（白天），则：
   - 继续执行以下检查

## 心跳检查任务（仅在白天执行）
- Email 检查
- Calendar 事件提醒（<2h）
- Twitter/social 通知
- Weather 更新
- ClawdHub Token 状态检查（每 24 小时一次）
- 成就系统进度检查（每 4 小时一次）
- AI 提示词自动化流程（每天早上 9 点，通过 cron 自动执行）

## 深夜监工任务（23:00-07:00）
- **审查代理检查**: 使用 `/root/clawd/scripts/check-review-agent.sh` 检查 review-agent 和 achievement-system-dev 的状态
- **AI 信息搜索**: 使用 searXNG 搜索 AI 相关信息，分析并保存到 `/root/clawd/memory/ai-research/`
- **子代理监工**: 确保 achievement-system-dev 正常工作，工具可用
- **进度记录**: 将发现的问题和进展记录到 daily memory

## 深夜模式例外
- 紧急事件
- 安全警报
- 用户明确要求的通知
- **AI 研究任务**（jack 授权，使用 searXNG 搜索 AI 相关信息）
- **审查代理监督**（检查子代理开发进度）

## 📊 白天检查任务详细说明

### 成就系统进度检查（每 4 小时）
```bash
# 检查脚本
/root/clawd/scripts/check-achievement-progress.sh

# 检查内容
1. 子代理状态（achievement-system-dev）
2. 终端工具开发进度
3. 成就数据收集状态
4. 发送进度报告到 Slack/Feishu
```

### ClawdHub Token 状态检查（每 24 小时）
```bash
# 检查脚本
/root/clawd/scripts/check-clawdhub-token-auto.sh

# 检查内容
1. Token 是否有效（通过 clawdhub search 测试）
2. 记录到 memory/clawdhub-token-check.log
3. 如果无效，记录告警到 memory/clawdhub-token-alerts.txt
4. Token 有效则静默，无效则通知用户更新
```

### AI 信息搜索（每天晚上 9 点）
```bash
# 执行脚本
/root/clawd/projects/info-search/workflows/ai-research-extended.sh

# 流程内容
1. 搜索 15 个核心 AI 主题
2. 包含：AI 模型更新、AI 技术、AI 商业化、AI 产品
3. 生成报告并保存到 /root/clawd/memory/ai-research/
4. 自动推送摘要报告到 Slack/Feishu

# 搜索主题（15 个核心主题）
- AI 模型和平台更新：Claude、OpenAI、Google Gemini、Meta Llama
- AI 技术和应用：Agents、Multimodal、Coding、Automation
- AI 商业化和产品：Startup trends、Business ideas、Monetization
```

### 工具和技能使用记录（持续）
```bash
# 记录脚本
/root/clawd/scripts/record-tool-usage.sh

# 记录内容
1. 使用了哪些工具（coding-agent, searXNG 等）
2. 使用了哪些技能
3. 任务类型和结果
4. 保存到 memory/tool-usage/
```

## 状态跟踪
- 记录最后检查时间到 `memory/heartbeat-state.json`
- 避免重复通知同一事件
