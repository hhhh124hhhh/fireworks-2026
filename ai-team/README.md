# AI 自媒体情报系统 🤖

基于 OpenClaw 的 AI 团队自动化系统，专注服务 AI 自媒体从业者，每天自动收集、分析 AI 工具/实战/资讯情报。

---

## 系统架构

```
AI 自媒体情报系统
│
├── 情报收集层
│   └── 老刘 (Researcher) → intel/raw/ + intel/data/
│
├── 分析处理层
│   └── 阿强 (Analyst) → intel/DAILY-INTEL.md
│
├── 内容创作层
│   ├── 小凯 (X/Twitter Writer) → deliverables/kelly-drafts/
│   └── 小美 (LinkedIn Writer) → deliverables/rachel-drafts/
│
└── 协调控制层
    └── Monica (Orchestrator) → HEARTBEAT.md
```

---

## 核心设计原则

### 1. Agent = SOUL.md
每个 Agent 的核心定义都在一个文件里：**`SOUL.md`**

- 身份定义（Who）
- 岗位职责（What）
- 行为准则（How）
- 协作关系（With whom）

### 2. 文件即通信
Agent 之间**不直接对话**，通过**文件系统**协作：

```
老刘写 → intel/raw/YYYY-MM-DD-raw-intel.md
            ↓
阿强读 → 分析 → 写 → intel/DAILY-INTEL.md
                          ↓
小凯/小美读 → 创作 → deliverables/
```

**好处：**
- 简单可靠（文件不会崩溃）
- 可追溯（每个文件都有时间戳）
- 解耦（Agent 可以独立运行）

### 3. 两层记忆系统

**每日日志:** `memory/YYYY-MM-DD.md`
- 当天干了什么
- 遇到的坑
- 学到的经验

**长期记忆:** `MEMORY.md`
- 提炼后的精华
- 发现的模式
- 积累的经验

---

## 目录结构

```
~/clawd/ai-team/
│
├── SOUL.md                    # Monica (CEO) 的定义
├── AGENTS.md                  # 全局行为规则
├── HEARTBEAT.md               # 系统状态监控
├── README.md                  # 本文件
│
├── agents/                    # Agent 定义目录
│   ├── dwight/               # 研究员 (可复用)
│   │   ├── SOUL.md
│   │   └── memory/
│   │
│   ├── liu-researcher/       # 老刘 (AI 情报收集)
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── memory/
│   │
│   ├── xiao-analyst/         # 阿强 (情报分析)
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── memory/
│   │
│   ├── kelly/                # 小凯 (X/Twitter 内容)
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── memory/
│   │
│   └── rachel/               # 小美 (LinkedIn 内容)
│       ├── SOUL.md
│       ├── AGENTS.md
│       └── memory/
│
├── intel/                     # 情报共享区
│   ├── DAILY-INTEL.md        # 每日核心情报 (阿强产出)
│   ├── raw/                  # 老刘的原始情报
│   ├── data/                 # 结构化 JSON 数据
│   └── analysis/             # 阿强的深度分析
│
├── deliverables/              # 内容产出
│   ├── kelly-drafts/          # 小凯的 X/Twitter 草稿
│   └── rachel-drafts/         # 小美的 LinkedIn 草稿
│
└── memory/                     # 团队共享记忆 (可选)
```

---

## 使用流程

### 1. 初始化系统

```bash
cd ~/clawd/ai-team

# 检查目录结构
ls -la

# 查看系统状态
cat HEARTBEAT.md
```

### 2. 启动情报收集 (老刘)

```bash
# 让老刘开始收集情报
openclaw sessions_spawn \
  --task "你是老刘，AI 情报侦察兵。请阅读你的 SOUL.md 文件: ~/clawd/ai-team/agents/liu-researcher/SOUL.md，然后按照你的职责开始收集今天的 AI 情报（工具、案例、资讯）。将输出写入指定位置。" \
  --mode run \
  --label "liu-researcher" \
  --timeout 1800
```

### 3. 启动情报分析 (阿强)

```bash
# 让阿强分析情报（需要等老刘完成）
openclaw sessions_spawn \
  --task "你是阿强，AI 情报分析师。请阅读你的 SOUL.md: ~/clawd/ai-team/agents/xiao-analyst/SOUL.md，然后阅读老刘的情报文件: ~/clawd/ai-team/intel/raw/$(date +%Y-%m-%d)-raw-intel.md，分析后产出每日核心情报报告。" \
  --mode run \
  --label "xiao-analyst" \
  --timeout 1800
```

### 4. 启动内容创作 (小凯、小美)

```bash
# 小凯写 X/Twitter 内容
openclaw sessions_spawn \
  --task "你是小凯，X/Twitter 内容创作者。阅读你的 SOUL.md: ~/clawd/ai-team/agents/kelly/SOUL.md，然后阅读阿强的情报报告: ~/clawd/ai-team/intel/DAILY-INTEL.md，创作 3-5 条推文草稿。" \
  --mode run \
  --label "kelly-writer" \
  --timeout 1200

# 小美写 LinkedIn 内容
openclaw sessions_spawn \
  --task "你是小美，LinkedIn 内容创作者。阅读你的 SOUL.md: ~/clawd/ai-team/agents/rachel/SOUL.md，然后阅读阿强的情报报告: ~/clawd/ai-team/intel/DAILY-INTEL.md，创作 2-3 条 LinkedIn 帖子草稿。" \
  --mode run \
  --label "rachel-writer" \
  --timeout 1200
```

### 5. 检查系统状态

```bash
# 查看 HEARTBEAT 状态
cat ~/clawd/ai-team/HEARTBEAT.md

# 查看各 Agent 的记忆文件
ls -la ~/clawd/ai-team/agents/*/memory/

# 查看产出文件
ls -la ~/clawd/ai-team/intel/
ls -la ~/clawd/ai-team/deliverables/
```

---

## 自动化设置 (Cron)

建议的定时任务：

```bash
# 编辑 crontab
crontab -e

# 添加以下定时任务

# 每天 00:00 — 老刘收集情报
0 0 * * * cd ~/clawd/ai-team && openclaw sessions_spawn --task "阅读 agents/liu-researcher/SOUL.md 并执行情报收集任务" --mode run --label "liu-researcher-daily" --timeout 1800 >> logs/liu-researcher.log 2>&1

# 每天 03:00 — 阿强分析情报 (在老刘完成后)
0 3 * * * cd ~/clawd/ai-team && openclaw sessions_spawn --task "阅读 agents/xiao-analyst/SOUL.md 和 intel/raw/\$(date +\%Y-\%m-\%d)-raw-intel.md，产出 DAILY-INTEL.md" --mode run --label "xiao-analyst-daily" --timeout 1800 >> logs/xiao-analyst.log 2>&1

# 每天 06:00 — 小凯写 X 内容
0 6 * * * cd ~/clawd/ai-team && openclaw sessions_spawn --task "阅读 agents/kelly/SOUL.md 和 intel/DAILY-INTEL.md，创作 X/Twitter 内容" --mode run --label "kelly-daily" --timeout 1200 >> logs/kelly.log 2>&1

# 每天 06:30 — 小美写 LinkedIn 内容
30 6 * * * cd ~/clawd/ai-team && openclaw sessions_spawn --task "阅读 agents/rachel/SOUL.md 和 intel/DAILY-INTEL.md，创作 LinkedIn 内容" --mode run --label "rachel-daily" --timeout 1200 >> logs/rachel.log 2>&1

# 每小时 — Monica 检查系统状态
0 * * * * cd ~/clawd/ai-team && cat HEARTBEAT.md | head -50 > /tmp/heartbeat-check.txt
```

---

## 故障排除

### 问题 1: Agent 没有产出

**检查清单:**
1. 检查 Agent 的 SOUL.md 是否存在且可读
2. 检查输入文件是否存在（如 `intel/raw/...`）
3. 检查 `openclaw sessions_spawn` 命令是否正确执行
4. 查看 Agent 的 memory 文件是否有错误记录

### 问题 2: 文件权限错误

**解决方案:**
```bash
# 确保所有目录可写
chmod -R 755 ~/clawd/ai-team

# 确保 Agent 可以写入各自目录
chmod -R 755 ~/clawd/ai-team/agents/*/memory/
chmod -R 755 ~/clawd/ai-team/intel/
chmod -R 755 ~/clawd/ai-team/deliverables/
```

### 问题 3: 循环依赖或等待超时

**症状:** Agent 一直在等待输入文件

**检查:**
```bash
# 检查文件时间戳
ls -la ~/clawd/ai-team/intel/raw/
ls -la ~/clawd/ai-team/intel/DAILY-INTEL.md

# 如果文件太旧，手动触发前置 Agent
```

---

## 扩展与定制

### 添加新 Agent

1. 创建目录: `mkdir -p ~/clawd/ai-team/agents/new-agent/{memory,output}`
2. 创建 SOUL.md: 定义新 Agent 的身份、职责、输入输出
3. 创建 AGENTS.md (可选): 如果有特殊规则
4. 更新 HEARTBEAT.md: 添加新 Agent 的执行时序
5. 添加 cron 任务: 自动化新 Agent 的执行

### 修改执行时序

编辑 `HEARTBEAT.md` 中的 "Daily Execution Cycle" 部分，调整：
- 各 Phase 的执行时间
- Agent 的启动顺序
- 检查点和依赖关系

### 添加新的输出格式

在 `intel/` 或 `deliverables/` 下创建新的子目录，然后在相关 Agent 的 SOUL.md 中：
1. 定义新的输出格式
2. 指定输出路径
3. 提供模板和示例

---

## 系统理念

### 为什么用文件系统？

- **简单可靠** — 文件不会崩溃，不需要维护
- **完全可审计** — 每个中间状态都有记录
- **松耦合** — Agent 可以独立开发、测试、部署
- **人类可读** — Markdown 文件，随时可以用编辑器查看

### 为什么用 SOUL.md？

- **单一真相源** — 每个 Agent 的定义在一个文件里
- **版本可控** — 可以用 git 管理 Agent 的变更
- **可迁移** — 换个环境，复制 SOUL.md 就能复现

### 为什么分离收集/分析/创作？

- **专业化** — 每个 Agent 只做一件事，做到极致
- **可替换** — 不满意某个 Agent？换掉 SOUL.md 就行
- **可扩展** — 需要新类型的内容？加一个新 Agent

---

## 贡献与反馈

这个系统是 jack 的 AI 自媒体工作流。如果你有兴趣：

1. **克隆使用** — 复制这套系统，改成你自己的领域
2. **改进反馈** — 发现问题或有建议，告诉 jack
3. **扩展分享** — 开发了新的 Agent 类型，分享给社区

---

## License

MIT — Use, modify, share freely. Just keep attribution.

---

*System Version: 1.0.0*  
*Last Updated: 2026-03-04*  
*Author: jack's AI Team*