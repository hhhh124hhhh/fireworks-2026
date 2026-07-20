# 备份系统配置文档

## 概述

为了确保轻量云环境的数据安全，建立了完整的自动备份系统。

## 备份策略

### 1. 每日备份 ⭐⭐⭐

**脚本**: `/root/clawd/scripts/daily-backup.sh`

**执行时间**: 每天凌晨 1:00

**备份内容**:
- `/root/clawd/memory/` - 记忆文件
- `/root/clawd/docs/` - 文档和知识库
- `/root/clawd/data/` - 数据清单
- `/root/clawd/IDENTITY.md` - 身份配置
- `/root/clawd/USER.md` - 用户信息
- `/root/clawd/SOUL.md` - 灵魂配置
- `/root/clawd/AGENTS.md` - 配置文件
- `/root/clawd/HEARTBEAT.md` - 心跳配置
- `/root/clawd/TOOLS.md` - 工具配置

**备份位置**: `/root/clawd/backups/daily/`

**保留期**: 7 天

**压缩格式**: tar.gz

**状态**: ✅ 已测试

---

### 2. Git 同步 ⭐⭐⭐

**脚本**: `/root/clawd/scripts/git-sync.sh`

**执行时间**: 每天凌晨 1:30

**同步内容**:
- memory/
- docs/
- scripts/
- IDENTITY.md
- USER.md
- SOUL.md
- AGENTS.md
- HEARTBEAT.md
- TOOLS.md

**仓库**: https://github.com/hhhh124hhhh/jack-portfolio.git

**分支**: main

**提交信息**: "Daily backup - YYYY-MM-DD HHMM"

**状态**: ✅ 已配置，需要首次推送

---

### 3. 备份状态检查 ⭐⭐

**脚本**: `/root/clawd/scripts/backup-status.sh`

**执行时间**: 每小时

**检查内容**:
- 每日备份状态
- Git 同步状态
- 记忆文件状态
- 建议操作

**报告位置**: `/root/clawd/logs/backup/backup-status-*.md`

**保留期**: 7 天

**状态**: ✅ 已配置

---

## Cron 任务

### 备份相关

| 时间 | 任务 | 脚本 | 状态 |
|------|------|------|------|
| 每天 1:00 | 每日备份 | daily-backup.sh | ✅ |
| 每天 1:30 | Git 同步 | git-sync.sh | ✅ |
| 每小时 | 状态检查 | backup-status.sh | ✅ |

### 其他任务

| 时间 | 任务 | 脚本 | 状态 |
|------|------|------|------|
| 每天 2:00 | 百度云同步 | sync-to-baidu-cloud-v2.sh | ✅ |
| 每天 2:00 | 自动归档（周日） | auto-archive.sh | ✅ |
| 每天 3:00 | 清理旧文件 | cleanup-old-files.sh | ✅ |
| 每天 3:00 | Gateway 重启 | openclaw gateway restart | ✅ |
| 每天 4:00 | Rclone 备份 | rclone-backup.sh | ✅ |
| 每天 9:00 | AI 研究推送 | daily-research-push.sh | ✅ |
| 每小时 | CPU 监控 | monitor-gateway-cron.sh | ✅ |

---

## 备份文件管理

### 备份目录结构

```
/root/clawd/backups/
├── daily/
│   ├── daily-backup-2026-02-10-0100.tar.gz
│   ├── daily-backup-2026-02-11-0100.tar.gz
│   └── daily-backup-summary.md
└── archive/
    └── (归档文件)
```

### 日志目录结构

```
/root/clawd/logs/
├── backup/
│   ├── daily-backup-*.log
│   ├── git-sync-*.log
│   └── backup-status-*.md
├── git/
│   └── git-sync-*.log
└── (其他日志)
```

---

## 备份恢复流程

### 场景 1: 恢复记忆文件

```bash
# 1. 查找备份
ls -lh /root/clawd/backups/daily/

# 2. 解压备份
cd /root/clawd
tar -xzf /root/clawd/backups/daily/daily-backup-YYYY-MM-DD-HHMM.tar.gz

# 3. 恢复文件
# 文件会自动解压到正确的位置
```

### 场景 2: 从 Git 恢复

```bash
# 1. 克隆仓库
git clone https://github.com/hhhh124hhhh/jack-portfolio.git /tmp/restore

# 2. 查看历史
cd /tmp/restore
git log --oneline

# 3. 恢复到特定版本
git checkout <commit-hash>

# 4. 复制文件
cp -r memory/ /root/clawd/
cp -r docs/ /root/clawd/
cp *.md /root/clawd/
```

---

## 备份配置文件

### 配置文件

| 文件 | 说明 |
|------|------|
| `/root/clawd/memory/MEMORY.md` | 长期记忆 |
| `/root/clawd/IDENTITY.md` | 身份配置 |
| `/root/clawd/USER.md` | 用户信息 |
| `/root/clawd/SOUL.md` | 灵魂配置 |
| `/root/clawd/AGENTS.md` | 配置文件 |

### 脚本文件

| 脚本 | 功能 |
|------|------|
| `daily-backup.sh` | 每日备份 |
| `git-sync.sh` | Git 同步 |
| `backup-status.sh` | 状态检查 |
| `setup-backup-cron.sh` | 配置 Cron |

---

## 监控和告警

### 备份检查

每小时自动运行 `backup-status.sh`，检查：
- 最近 24 小时是否有备份
- Git 是否有未提交的更改
- 关键文件是否存在

### 手动检查

```bash
# 运行状态检查
bash /root/clawd/scripts/backup-status.sh

# 查看备份日志
tail -f /root/clawd/logs/backup/daily-backup-*.log

# 查看 Git 同步日志
tail -f /root/clawd/logs/git/git-sync-*.log
```

---

## 未来改进

### 短期（1-2 周）

1. ⏳ 配置百度云 BOS 上传
2. ⏳ 首次 Git 推送
3. ⏳ 配置告警通知

### 中期（1-2 个月）

1. ⏳ 多云备份（阿里云 OSS、腾讯云 COS）
2. ⏳ 自动恢复脚本
3. ⏳ 备份验证脚本

### 长期（3 个月以上）

1. ⏳ 备份加密
2. ⏳ 异地备份
3. ⏳ 备份性能优化

---

## 联系方式

如有问题，请查看：
- 备份日志: `/root/clawd/logs/backup/`
- Cron 任务: `crontab -l`
- Git 仓库: https://github.com/hhhh124hhhh/jack-portfolio.git

---

**文档更新**: 2026-02-10
**状态**: ✅ 已配置并测试
