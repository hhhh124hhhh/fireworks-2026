# Clawdbot 服务器备份和迁移指南

## 📋 概述

这套脚本用于备份和迁移 Clawdbot 到新服务器，支持三种备份类型：

- **Essential**（~700MB）- 核心系统
- **Important**（~1.7GB）- 核心系统 + 项目和配置
- **Complete**（~4.2GB）- 所有内容

---

## 🚀 快速开始

### 1. 在当前服务器创建备份

```bash
# 方式 1: Essential 备份（推荐快速迁移）
bash /root/clawd/scripts/backup-and-migrate.sh essential

# 方式 2: Important 备份（推荐完整迁移）
bash /root/clawd/scripts/backup-and-migrate.sh important

# 方式 3: Complete 备份（包含所有内容）
bash /root/clawd/scripts/backup-and-migrate.sh complete
```

### 2. 查看备份文件

```bash
ls -lh /root/clawd-backups/
```

### 3. 传输到新服务器

```bash
# 使用 scp 传输所有备份文件
scp /root/clawd-backups/* user@new-server:/root/clawd-backups/
```

### 4. 在新服务器恢复

```bash
# 解压备份文件
cd /root/clawd-backups

# 运行恢复脚本
./restore-YYYYMMDD-HHMMSS.sh essential clawdbot-backup-YYYYMMDD-HHMMSS.tar.gz-essential.tar.gz
```

### 5. 重启 OpenClaw Gateway

```bash
openclaw gateway restart

# 验证状态
openclaw gateway status
```

---

## 📦 备份类型详解

### Essential 备份（~700MB）

**包含内容**:
- `~/.openclaw/` - OpenClaw 配置
- `~/.agents/skills/` - 技能库（70+ 技能）
- `/root/clawd/memory/` - 记忆系统
- `/root/clawd/MEMORY.md` - 核心记忆

**优点**:
- 快速备份（约 5-10 分钟）
- 小文件，传输快速
- 包含所有核心功能

**缺点**:
- 不包含个人项目
- 不包含配置文件
- 需要手动重建定时任务

**适用场景**:
- 快速迁移到新服务器
- 只需要核心功能
- 时间紧迫

---

### Important 备份（~1.7GB）

**包含内容**:
- Essential 备份的所有内容
- `/root/clawd/` - 个人项目
- `/root/clawd/.config/` - 配置文件
- `~/.bashrc` - Bash 配置
- `~/.gitconfig` - Git 配置

**优点**:
- 包含所有个人项目
- 完整的环境配置
- 保持环境一致性

**缺点**:
- 备份时间较长（约 15-30 分钟）
- 文件较大，传输较慢
- 不包含 Docker 配置

**适用场景**:
- 推荐的迁移方式
- 完整环境迁移
- 需要保持所有项目

---

### Complete 备份（~4.2GB）

**包含内容**:
- Important 备份的所有内容
- Crontab 定时任务
- Docker Compose 配置

**优点**:
- 包含所有内容
- 可以立即使用
- 完全保持环境

**缺点**:
- 备份时间很长（约 30-60 分钟）
- 文件很大，传输很慢
- 包含大量不需要的日志

**适用场景**:
- 完整的备份
- 需要保留所有历史数据
- 有足够的传输带宽

---

## 🔄 迁移步骤详解

### 第 1 步：在当前服务器创建备份

```bash
# 选择备份类型
BACKUP_TYPE="essential"  # 或 "important", "complete"

# 运行备份脚本
bash /root/clawd/scripts/backup-and-migrate.sh $BACKUP_TYPE
```

**输出示例**:
```
==========================================
Clawdbot Backup & Migration Script
==========================================

✓ Backup directory created: /root/clawd-backups

ℹ Starting ESSENTIAL backup (~700MB)
ℹ Includes: OpenClaw, Skills, Memory

[INFO] Starting essential backup...
[1/4] 25% Backing up: OpenClaw配置 (~/.openclaw/)
[2/4] 50% Backing up: 技能库 (~/.agents/skills/)
[3/4] 75% Backing up: 记忆系统 (/root/clawd/memory/)
[4/4] 100% Backing up: 核心记忆 (/root/clawd/MEMORY.md)

[INFO] Creating essential backup...
✓ Essential backup created: /root/clawd-backups/clawdbot-backup-20260209-184917.tar.gz-essential.tar.gz

✓ Restore script created: /root/clawd-backups/restore-20260209-184917.sh
✓ Manifest created: /root/clawd-backups/MANIFEST-20260209-184917.txt

==========================================
✓ Backup completed!
==========================================
```

### 第 2 步：验证备份文件

```bash
# 查看备份文件
ls -lh /root/clawd-backups/

# 查看备份清单
cat /root/clawd-backups/MANIFEST-*.txt
```

### 第 3 步：传输到新服务器

```bash
# 方式 1: 使用 scp（推荐）
scp /root/clawd-backups/* user@new-server:/root/clawd-backups/

# 方式 2: 使用 rsync（适合大文件）
rsync -avz --progress /root/clawd-backups/ user@new-server:/root/clawd-backups/

# 方式 3: 使用 tar + ssh（管道传输）
tar -czf - /root/clawd-backups/ | ssh user@new-server "tar -xzf - -C /root/"
```

### 第 4 步：在新服务器恢复

```bash
# 进入备份目录
cd /root/clawd-backups

# 列出可用的恢复脚本
ls restore-*.sh

# 运行恢复脚本
./restore-YYYYMMDD-HHMMSS.sh essential clawdbot-backup-YYYYMMDD-HHMMSS.tar.gz-essential.tar.gz
```

**输出示例**:
```
Clawdbot Restore Script
======================

ℹ Restore type: essential
ℹ Backup file: clawdbot-backup-20260209-184917.tar.gz-essential.tar.gz

ℹ Extracting backup...
✓ Backup extracted

ℹ Fixing file permissions...
✓ Permissions fixed

✓ OpenClaw directory found
✓ Skills directory found
ℹ Skills found: 70

✓ Restore completed!

ℹ Next steps:
ℹ 1. Restart OpenClaw Gateway
ℹ 2. Verify all skills are loaded
ℹ 3. Test memory system
ℹ 4. Verify cron jobs (if restoring important/complete)

ℹ Commands:
  openclaw gateway restart
  openclaw gateway status
  ls ~/.agents/skills/
  crontab -l
```

### 第 5 步：重启 OpenClaw Gateway

```bash
# 重启 OpenClaw Gateway
openclaw gateway restart

# 等待几秒钟
sleep 5

# 检查状态
openclaw gateway status
```

### 第 6 步：验证所有系统

```bash
# 验证技能库
ls ~/.agents/skills/
echo "Skill count: $(ls ~/.agents/skills/ | wc -l)"

# 验证记忆系统
cat /root/clawd/MEMORY.md

# 验证 OpenClaw 配置
ls ~/.openclaw/

# 验证个人项目（如果恢复了 important 或 complete）
ls /root/clawd/

# 验证定时任务（如果恢复了 important 或 complete）
crontab -l

# 验证 Docker 容器（如果恢复了 complete）
docker ps
```

---

## 📊 备份对比

| 特性 | Essential | Important | Complete |
|-----|-----------|-----------|-----------|
| OpenClaw 配置 | ✅ | ✅ | ✅ |
| 技能库 | ✅ | ✅ | ✅ |
| 记忆系统 | ✅ | ✅ | ✅ |
| 个人项目 | ❌ | ✅ | ✅ |
| 配置文件 | ❌ | ✅ | ✅ |
| 定时任务 | ❌ | ❌ | ✅ |
| Docker 配置 | ❌ | ❌ | ✅ |
| 大小 | ~700MB | ~1.7GB | ~4.2GB |
| 备份时间 | 5-10 分钟 | 15-30 分钟 | 30-60 分钟 |
| 推荐度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

---

## ⚠️ 注意事项

### 安全注意事项

1. **API keys 安全**
   - 备份文件包含敏感的 API keys
   - 不要通过邮件或即时通讯发送
   - 使用安全的传输方式（scp, rsync）
   - 恢复后立即删除临时备份文件

2. **权限问题**
   - 确保新服务器的文件权限正确
   - 检查 `.openclaw/` 的权限
   - 确保 OpenClaw Gateway 可以访问配置文件

3. **磁盘空间**
   - 确保新服务器有足够的磁盘空间
   - Essential: 至少 2GB
   - Important: 至少 5GB
   - Complete: 至少 10GB

### 常见问题

**Q: 备份文件太大，传输太慢怎么办？**

A: 使用 `rsync` 的增量同步功能，可以断点续传：
```bash
rsync -avz --partial --progress /root/clawd-backups/ user@new-server:/root/clawd-backups/
```

**Q: 恢复后 OpenClaw Gateway 无法启动？**

A: 检查文件权限：
```bash
chmod -R 755 /root/.openclaw
chmod -R 755 /root/.agents
openclaw gateway restart
```

**Q: 技能没有正确加载？**

A: 检查 OpenClaw 配置：
```bash
cat ~/.openclaw/openclaw.json | grep skills.load.extraDirs
```

**Q: 定时任务没有恢复？**

A: 如果使用的是 Essential 或 Important 备份，需要手动重建定时任务。查看旧服务器的 crontab：
```bash
crontab -l > /tmp/crontab-backup.txt
# 然后在新服务器导入
crontab /tmp/crontab-backup.txt
```

---

## 🎯 推荐方案

### 快速迁移（Essential）

**适用场景**:
- 快速迁移到新服务器
- 只需要核心功能
- 时间紧迫

**步骤**:
1. 创建 Essential 备份
2. 传输到新服务器
3. 恢复备份
4. 重建个人项目和定时任务

**时间**: 约 30-60 分钟

---

### 完整迁移（Important）✅ 推荐

**适用场景**:
- 推荐的迁移方式
- 完整环境迁移
- 需要保持所有项目

**步骤**:
1. 创建 Important 备份
2. 传输到新服务器
3. 恢复备份
4. 重启 OpenClaw Gateway
5. 验证所有系统

**时间**: 约 60-120 分钟

---

### 完整备份（Complete）

**适用场景**:
- 完整的备份和归档
- 需要保留所有历史数据
- 有足够的传输带宽

**步骤**:
1. 创建 Complete 备份
2. 传输到新服务器
3. 恢复备份
4. 重启 OpenClaw Gateway
5. 验证所有系统

**时间**: 约 120-240 分钟

---

## 📚 相关文件

### 备份和迁移脚本

- **备份脚本**: `/root/clawd/scripts/backup-and-migrate.sh`
- **备份目录**: `/root/clawd-backups/`
- **恢复脚本**: `/root/clawd-backups/restore-YYYYMMDD-HHMMSS.sh`
- **备份清单**: `/root/clawd-backups/MANIFEST-YYYYMMDD-HHMMSS.txt`

### 配置文件

- **OpenClaw 配置**: `~/.openclaw/openclaw.json`
- **技能库**: `~/.agents/skills/`
- **记忆系统**: `/root/clawd/memory/`, `/root/clawd/MEMORY.md`
- **个人项目**: `/root/clawd/`

---

## ✅ 总结

**三种备份类型**:
- Essential（~700MB）- 核心系统
- Important（~1.7GB）- 核心系统 + 项目和配置 ✅ 推荐
- Complete（~4.2GB）- 所有内容

**推荐方案**: Important 备份 + 恢复

**优点**:
- 完整的环境
- 可以立即使用
- 迁移时间适中

**下一步**: 运行备份脚本，开始迁移！

---

*最后更新: 2026-02-09*
*版本: v1.0*
