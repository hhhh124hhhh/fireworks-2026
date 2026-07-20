#!/bin/bash
# OpenClaw 更新前备份脚本

echo "=== OpenClaw 更新前备份 ==="
echo "备份时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 备份目录
BACKUP_DIR="/root/clawd/backup/backup-$(date '+%Y%m%d-%H%M%S')"
mkdir -p "$BACKUP_DIR"

# 备份配置文件
echo "1. 备份配置文件..."
cp -r ~/.openclaw "$BACKUP_DIR/"
cp -r ~/.config/clawd "$BACKUP_DIR/" 2>/dev/null || echo "  clawd config 不存在，跳过"
echo "  ✓ 配置文件备份完成"

# 备份记忆文件
echo "2. 备份记忆文件..."
cp -r /root/clawd/memory "$BACKUP_DIR/"
cp -r /root/clawd/IDENTITY.md "$BACKUP_DIR/"
cp -r /root/clawd/SOUL.md "$BACKUP_DIR/"
cp -r /root/clawd/USER.md "$BACKUP_DIR/"
echo "  ✓ 记忆文件备份完成"

# 备份技能
echo "3. 备份技能..."
cp -r /root/clawd/skills "$BACKUP_DIR/"
echo "  ✓ 技能备份完成"

# 备份文档
echo "4. 备份文档..."
cp -r /root/clawd/docs "$BACKUP_DIR/"
echo "  ✓ 文档备份完成"

# 备份脚本
echo "5. 备份脚本..."
cp -r /root/clawd/scripts "$BACKUP_DIR/"
echo "  ✓ 脚本备份完成"

# 生成备份清单
echo "" > "$BACKUP_DIR/backup-manifest.txt"
echo "=== 备份清单 ===" >> "$BACKUP_DIR/backup-manifest.txt"
echo "备份时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$BACKUP_DIR/backup-manifest.txt"
echo "" >> "$BACKUP_DIR/backup-manifest.txt"
echo "备份内容:" >> "$BACKUP_DIR/backup-manifest.txt"
du -sh "$BACKUP_DIR"/* >> "$BACKUP_DIR/backup-manifest.txt"

echo ""
echo "备份完成！"
echo "备份目录: $BACKUP_DIR"
echo "备份大小: $(du -sh $BACKUP_DIR | cut -f1)"
echo ""
echo "备份清单:"
cat "$BACKUP_DIR/backup-manifest.txt"
