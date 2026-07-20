#!/bin/bash

# Clawdbot Server Backup & Migration Script
# 用于备份和迁移 Clawdbot 到新服务器

set -e

# ============================================
# Configuration
# ============================================

BACKUP_DIR="/root/clawd-backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="clawdbot-backup-$TIMESTAMP"
BACKUP_FILE="$BACKUP_DIR/$BACKUP_NAME.tar.gz"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================
# Helper Functions
# ============================================

log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date -Iseconds)
    echo "[$timestamp] [$level] $message"
}

error() {
    echo -e "${RED}ERROR: $1${NC}"
    exit 1
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

show_progress() {
    local current=$1
    local total=$2
    local percent=$((current * 100 / total))
    echo -ne "\r[$current/$total] ${percent}%"
}

# ============================================
# Backup Functions
# ============================================

backup_essential() {
    log "INFO" "Starting essential backup..."

    local items=(
        "~/.openclaw/:OpenClaw配置"
        "~/.agents/skills/:技能库"
        "/root/clawd/memory/:记忆系统"
        "/root/clawd/MEMORY.md:核心记忆"
    )

    local count=0
    local total=${#items[@]}
    local backup_list=""

    for item in "${items[@]}"; do
        local path=${item%%:*}
        local desc=${item##*:}

        count=$((count + 1))
        show_progress $count $total
        log "INFO" "Backing up: $desc ($path)"

        # Expand ~ to /root
        path="${path/#\~/$HOME}"

        if [ -e "$path" ]; then
            backup_list="$backup_list $path"
        else
            warning "Path not found: $path"
        fi
    done

    echo ""

    if [ -n "$backup_list" ]; then
        log "INFO" "Creating essential backup..."
        tar -czf "$BACKUP_FILE-essential.tar.gz" $backup_list 2>/dev/null
        success "Essential backup created: $BACKUP_FILE-essential.tar.gz"
    else
        error "No files to backup"
    fi
}

backup_important() {
    log "INFO" "Starting important backup..."

    local items=(
        "/root/clawd/:个人项目"
        "/root/clawd/.config/:配置文件"
        "/root/.bashrc:Bash配置"
        "/root/.gitconfig:Git配置"
    )

    local count=0
    local total=${#items[@]}
    local backup_list=""

    for item in "${items[@]}"; do
        local path=${item%%:*}
        local desc=${item##*:}

        count=$((count + 1))
        show_progress $count $total
        log "INFO" "Backing up: $desc ($path)"

        if [ -e "$path" ]; then
            backup_list="$backup_list $path"
        else
            warning "Path not found: $path"
        fi
    done

    echo ""

    if [ -n "$backup_list" ]; then
        log "INFO" "Creating important backup..."
        tar -czf "$BACKUP_FILE-important.tar.gz" $backup_list 2>/dev/null
        success "Important backup created: $BACKUP_FILE-important.tar.gz"
    else
        error "No files to backup"
    fi
}

backup_complete() {
    log "INFO" "Starting complete backup..."

    local items=(
        "~/.openclaw/:OpenClaw配置"
        "~/.agents/skills/:技能库"
        "/root/clawd/memory/:记忆系统"
        "/root/clawd/MEMORY.md:核心记忆"
        "/root/clawd/:个人项目"
        "/root/clawd/.config/:配置文件"
        "/root/.bashrc:Bash配置"
        "/root/.gitconfig:Git配置"
    )

    local count=0
    local total=${#items[@]}
    local backup_list=""

    for item in "${items[@]}"; do
        local path=${item%%:*}
        local desc=${item##*:}

        count=$((count + 1))
        show_progress $count $total
        log "INFO" "Backing up: $desc ($path)"

        # Expand ~ to /root
        path="${path/#\~/$HOME}"

        if [ -e "$path" ]; then
            backup_list="$backup_list $path"
        else
            warning "Path not found: $path"
        fi
    done

    echo ""

    if [ -n "$backup_list" ]; then
        log "INFO" "Creating complete backup..."
        tar -czf "$BACKUP_FILE-complete.tar.gz" $backup_list 2>/dev/null
        success "Complete backup created: $BACKUP_FILE-complete.tar.gz"
    else
        error "No files to backup"
    fi
}

backup_crontab() {
    log "INFO" "Backing up crontab..."

    crontab -l > "$BACKUP_DIR/crontab-backup-$TIMESTAMP.txt" 2>/dev/null || true

    if [ -f "$BACKUP_DIR/crontab-backup-$TIMESTAMP.txt" ]; then
        success "Crontab backup created: $BACKUP_DIR/crontab-backup-$TIMESTAMP.txt"
    else
        warning "No crontab to backup"
    fi
}

backup_docker_compose() {
    log "INFO" "Backing up Docker compose files..."

    local docker_files=""
    for file in /root/*/docker-compose.yml /root/*/docker-compose.yaml; do
        if [ -f "$file" ]; then
            docker_files="$docker_files $file"
        fi
    done

    if [ -n "$docker_files" ]; then
        tar -czf "$BACKUP_DIR/docker-compose-backup-$TIMESTAMP.tar.gz" $docker_files 2>/dev/null
        success "Docker compose backup created: $BACKUP_DIR/docker-compose-backup-$TIMESTAMP.tar.gz"
    else
        warning "No docker-compose files found"
    fi
}

generate_restore_script() {
    log "INFO" "Generating restore script..."

    cat > "$BACKUP_DIR/restore-$TIMESTAMP.sh" << 'RESTORE_SCRIPT'
#!/bin/bash

# Clawdbot Restore Script
# 用于在新服务器上恢复 Clawdbot

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_NC='\033[0m'

error() {
    echo -e "${COLOR_RED}ERROR: $1${COLOR_NC}"
    exit 1
}

success() {
    echo -e "${COLOR_GREEN}✓ $1${COLOR_NC}"
}

info() {
    echo -e "${COLOR_BLUE}ℹ $1${COLOR_NC}"
}

warning() {
    echo -e "${COLOR_YELLOW}⚠ $1${COLOR_NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    error "This script must be run as root"
fi

info "Clawdbot Restore Script"
info "======================"
echo ""

# Parse command line arguments
RESTORE_TYPE="$1"
BACKUP_FILE="$2"

if [ -z "$RESTORE_TYPE" ] || [ -z "$BACKUP_FILE" ]; then
    error "Usage: $0 <essential|important|complete> <backup_file>"
fi

if [ ! -f "$BACKUP_FILE" ]; then
    error "Backup file not found: $BACKUP_FILE"
fi

info "Restore type: $RESTORE_TYPE"
info "Backup file: $BACKUP_FILE"
echo ""

# Extract backup
info "Extracting backup..."
tar -xzf "$BACKUP_FILE" -C /
success "Backup extracted"

# Fix permissions
info "Fixing file permissions..."
chown -R root:root /root
chmod 755 /root
chmod -R 755 /root/.openclaw
chmod -R 755 /root/.agents
success "Permissions fixed"

# Restore crontab if exists
if [ -f "$(dirname "$BACKUP_FILE")/crontab-backup-"*.txt" ]; then
    info "Restoring crontab..."
    crontab "$(dirname "$BACKUP_FILE")/crontab-backup-"*.txt"
    success "Crontab restored"
fi

# Verify OpenClaw installation
if [ -d "/root/.openclaw" ]; then
    info "OpenClaw directory found"
else
    error "OpenClaw directory not found"
fi

# Verify skills directory
if [ -d "/root/.agents/skills" ]; then
    info "Skills directory found"
else
    error "Skills directory not found"
fi

echo ""
success "Restore completed!"
echo ""
info "Next steps:"
info "1. Restart OpenClaw Gateway"
info "2. Verify all skills are loaded"
info "3. Test memory system"
info "4. Verify cron jobs"
echo ""
info "Commands:"
info "  openclaw gateway restart"
info "  crontab -l  # Check cron jobs"
info "  ls ~/.agents/skills/  # Check skills"
echo ""

RESTORE_SCRIPT

    chmod +x "$BACKUP_DIR/restore-$TIMESTAMP.sh"
    success "Restore script created: $BACKUP_DIR/restore-$TIMESTAMP.sh"
}

generate_manifest() {
    log "INFO" "Generating manifest..."

    cat > "$BACKUP_DIR/MANIFEST-$TIMESTAMP.txt" << MANIFEST
==========================================
Clawdbot Backup Manifest
==========================================

Backup Date: $(date -Iseconds)
Backup Name: $BACKUP_NAME
Backup Directory: $BACKUP_DIR

Backup Files:
- Essential: $BACKUP_FILE-essential.tar.gz
- Important: $BACKUP_FILE-important.tar.gz
- Complete: $BACKUP_FILE-complete.tar.gz
- Crontab: $BACKUP_DIR/crontab-backup-$TIMESTAMP.txt
- Docker Compose: $BACKUP_DIR/docker-compose-backup-$TIMESTAMP.tar.gz
- Restore Script: $BACKUP_DIR/restore-$TIMESTAMP.sh

Backup Contents:
- OpenClaw Configuration: ~/.openclaw/
- Skills Library: ~/.agents/skills/ (70+ skills)
- Memory System: /root/clawd/memory/, /root/clawd/MEMORY.md
- Personal Projects: /root/clawd/
- Configuration Files: /root/clawd/.config/
- Bash Configuration: ~/.bashrc
- Git Configuration: ~/.gitconfig
- Crontab: crontab -l
- Docker Compose: docker-compose files

Restore Instructions:
1. Copy backup files to new server
2. Run restore script: ./restore-$TIMESTAMP.sh <essential|important|complete> <backup_file>
3. Restart OpenClaw Gateway
4. Verify all systems

Verification Checklist:
[ ] OpenClaw Gateway starts successfully
[ ] All skills are loaded
[ ] Memory system is accessible
[ ] Cron jobs are scheduled
[ ] Personal projects are present
[ ] Configuration files are correct

==========================================
MANIFEST

    success "Manifest created: $BACKUP_DIR/MANIFEST-$TIMESTAMP.txt"
}

# ============================================
# Main Execution
# ============================================

main() {
    echo "=========================================="
    echo "Clawdbot Backup & Migration Script"
    echo "=========================================="
    echo ""

    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    success "Backup directory created: $BACKUP_DIR"
    echo ""

    # Parse command line arguments
    BACKUP_TYPE="${1:-complete}"

    case "$BACKUP_TYPE" in
        essential)
            info "Starting ESSENTIAL backup (~700MB)"
            info "Includes: OpenClaw, Skills, Memory"
            echo ""
            backup_essential
            ;;
        important)
            info "Starting IMPORTANT backup (~1.7GB)"
            info "Includes: Essential + Projects + Config + Cron"
            echo ""
            backup_essential
            backup_important
            ;;
        complete)
            info "Starting COMPLETE backup (~4.2GB)"
            info "Includes: All backups + Docker configs"
            echo ""
            backup_essential
            backup_important
            backup_crontab
            backup_docker_compose
            ;;
        *)
            error "Usage: $0 <essential|important|complete>"
            ;;
    esac

    echo ""
    generate_restore_script
    echo ""
    generate_manifest
    echo ""

    echo "=========================================="
    success "Backup completed!"
    echo "=========================================="
    echo ""
    info "Backup location: $BACKUP_DIR"
    echo ""
    info "Next steps:"
    info "1. Transfer backup files to new server:"
    echo "   scp $BACKUP_DIR/* user@new-server:/root/clawd-backups/"
    echo ""
    info "2. On new server, restore backup:"
    echo "   cd /root/clawd-backups"
    echo "   ./restore-$TIMESTAMP.sh $BACKUP_TYPE $BACKUP_FILE-$BACKUP_TYPE.tar.gz"
    echo ""
    info "3. Restart OpenClaw Gateway:"
    echo "   openclaw gateway restart"
    echo ""
    info "4. Verify all systems:"
    echo "   openclaw gateway status"
    echo "   ls ~/.agents/skills/"
    echo "   crontab -l"
    echo ""
}

# Run main function
main "$@"
