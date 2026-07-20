# Intel Officer - 独立工作区设置指南

## 🎯 目标
将 intel-officer 作为独立 OpenClaw 实例运行，不污染主 agent 上下文。

---

## 📁 目录结构
```
/path/to/intel-officer/     ← 独立工作区
├── AGENTS.md
├── SOUL.md
├── IDENTITY.md
├── USER.md
├── HEARTBEAT.md
├── skills/                  ← 热点抓取工具
├── memory/                  ← 情报报告
├── scripts/                 ← 定时任务脚本
└── data/                    ← 热点数据
```

---

## 🚀 启动方式

### 方式 1：openclaw tui（本地）
```bash
cd /path/to/intel-officer
openclaw tui
```

### 方式 2：openclaw run（无头模式）
```bash
cd /path/to/intel-officer
openclaw run --headless
```

### 方式 3：systemd 服务
```bash
sudo systemctl enable openclaw@intel-officer
sudo systemctl start openclaw@intel-officer
```

---

## 🔧 配置飞书 Bot

intel-officer 原有的飞书 bot 配置在 `config/` 目录下。
启动后确认：
1. 飞书 Bot token 有效
2. 飞书 Webhook 可用
3. 接收者 ID 正确（ou_c1f49efdd595b46e212560e66abc7205）

---

## 📡 协作机制

### 共享存储（推荐）
intel-officer 写数据到飞书文档，Momo 读取：

| Agent | 职责 | 输出 |
|-------|------|------|
| intel-officer | 热点挖掘 | 飞书文档 |
| Momo | 内容创作 | 直接回复/文档 |

### 直接通信
```bash
# Momo 发消息给 intel-officer
clawdbot sessions send agent:intel-officer:xxx "任务指令"

# 查看 intel-officer 状态
clawdbot sessions list | grep intel
```

---

## ⏰ 定时任务

intel-officer 原有定时任务（保留）：
- 06:00 / 12:00 / 18:00 / 23:00 - 情报推送
- 01:00-05:00 - 深度挖掘

---

## 🗑️ 清理（如果需要）
```bash
rm -rf /path/to/intel-officer
```

---

**最后更新**: 2026-04-01
