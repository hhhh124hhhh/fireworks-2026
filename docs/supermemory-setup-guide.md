# Supermemory 插件配置指南

**安装时间**: 2026-01-30 17:35

---

## ✅ 安装状态

**插件**: `@supermemory/clawdbot-supermemory`

**状态**: ✅ 安装成功

**详细信息**:
```
✅ 下载完成
✅ 提取完成
✅ 安装到: /root/.clawdbot/extensions/clawdbot-supermemory
✅ 安装依赖: 完成
✅ 内存 slot 切换: 从 memory-core 切换到 clawdbot-supermemory
✅ Gateway 重启: 完成
```

---

## ⚠️ 需要配置

**错误信息**:
```
supermemory: apiKey is required (set in plugin config or SUPERMEMORY_CLAWDBOT_API_KEY env var)
```

**影响**:
- 插件已安装，但无法使用
- 需要配置 Supermemory API Key

---

## 🔧 配置步骤

### 步骤 1: 获取 Supermemory API Key

1. 访问 https://supermemory.ai
2. 注册或登录
3. 进入 Settings 或 API Keys 页面
4. 创建新的 API Key
5. 复制 API Key（格式：`sm_xxxxxxxxx`）

---

### 步骤 2: 配置 API Key

#### 方法 A: 使用环境变量（推荐）✨

**临时配置**（当前会话有效）:
```bash
export SUPERMEMORY_CLAWDBOT_API_KEY=<你的_API_KEY>

# 验证
clawdbot plugins list
```

**永久配置**（重启后仍然有效）:
```bash
# 添加到 ~/.bashrc
echo 'export SUPERMEMORY_CLAWDBOT_API_KEY=<你的_API_KEY>' >> ~/.bashrc

# 重新加载
source ~/.bashrc

# 重启 Clawdbot
pkill -f clawdbot-gateway
nohup clawdbot gateway start > /tmp/clawdbot-gateway.log 2>&1 &
```

---

#### 方法 B: 使用插件配置文件

**创建配置文件**:
```bash
# 创建配置目录
mkdir -p ~/.clawdbot/extensions/clawdbot-supermemory

# 创建配置文件
cat > ~/.clawdbot/extensions/clawdbot-supermemory/.supermemory.json << 'EOF'
{
  "apiKey": "<你的_API_KEY>"
}
EOF
```

**重启 Gateway**:
```bash
pkill -f clawdbot-gateway
nohup clawdbot gateway start > /tmp/clawdbot-gateway.log 2>&1 &
```

---

#### 方法 C: 使用 clawdbot config

```bash
# 设置 API Key
clawdbot config set plugins.clawdbot-supermemory.apiKey <你的_API_KEY>

# 重启 Gateway
clawdbot gateway restart
```

---

### 步骤 3: 验证配置

**检查插件状态**:
```bash
clawdbot plugins list
```

**预期输出**:
```
[plugins]
clawdbot-supermemory    ✅ enabled
  @clawdbot/supermemory  v0.1.0
  Supermemory integration for Clawdbot
  Memory enabled: true
```

**查看日志**:
```bash
tail -20 /tmp/clawdbot-gateway.log | grep -i supermemory
```

---

### 步骤 4: 测试记忆功能

**发送测试消息**:
```bash
clawdbot message send \
  --channel slack \
  --target D0AB0J4QLAH \
  --message "测试 Supermemory 记忆功能"
```

**测试对话**:
1. 在 Slack 私聊中发送一些重要信息
2. 稍后询问："记得我刚才说了什么吗？"
3. 如果记住了，说明配置成功！

---

## 📋 配置检查清单

- [ ] 步骤 1: 获取 Supermemory API Key
- [ ] 步骤 2: 配置 API Key（方法 A/B/C）
- [ ] 步骤 3: 验证插件状态
- [ ] 步骤 4: 测试记忆功能

---

## 💡 推荐配置方法

**方法 A: 环境变量（最简单）**
- ✅ 最快
- ✅ 容易修改
- ⚠️ 需要重新加载 shell

**方法 C: clawdbot config（最可靠）**
- ✅ 持久化
- ✅ 与 Clawdbot 集成
- ✅ 重启后仍然有效

---

## 🎯 配置完成后

Supermemory 将自动：

1. ✅ **保存重要对话**
   - 自动识别关键信息
   - 分类和标记
   - 持久化存储

2. ✅ **智能检索**
   - 语义搜索
   - 上下文相关
   - 时间排序

3. ✅ **跨会话记忆**
   - 长期存储
   - 自动清理过期内容
   - 隐私保护

4. ✅ **提供上下文**
   - 为新对话提供历史信息
   - 提高对话连贯性
   - 减少重复说明

---

## 🔍 故障排查

### 问题 1: 插件仍然提示需要 API Key

**检查**:
```bash
# 检查环境变量
echo $SUPERMEMORY_CLAWDBOT_API_KEY

# 检查配置文件
cat ~/.clawdbot/extensions/clawdbot-supermemory/.supermemory.json

# 查看 Gateway 日志
tail -50 /tmp/clawdbot-gateway.log | grep -i "api.*key"
```

**解决方法**:
1. 确认 API Key 格式（应该是 `sm_xxxxxxxxx`）
2. 重新设置环境变量
3. 重启 Gateway
4. 检查日志中的错误信息

---

### 问题 2: 插件已启用但无法保存记忆

**检查**:
```bash
# 查看插件日志
tail -100 /tmp/clawdbot-gateway.log | grep -i "supermemory"

# 测试连接
curl -H "Authorization: Bearer <你的_API_KEY>" \
  https://api.supermemory.ai/v1/memories
```

**解决方法**:
1. 检查 API Key 是否正确
2. 检查网络连接
3. 查看错误日志
4. 联系 Supermemory 技术支持

---

## 📊 预期效果

**配置成功后，你将看到**:

1. **自动保存**
   - 重要对话自动保存到 Supermemory
   - 无需手动操作
   - 实时同步

2. **智能检索**
   - 问"记得什么"时能准确回答
   - 提供相关的历史信息
   - 支持语义搜索

3. **长期记忆**
   - 跨会话保持记忆
   - 重要信息不会丢失
   - 智能清理和分类

4. **无缝集成**
   - 与 Slack/Feishu 无缝集成
   - 不改变使用方式
   - 完全自动化

---

## 🚀 下一步

1. ✅ **获取 API Key** - 访问 https://supermemory.ai
2. ✅ **选择配置方法** - 推荐方法 C（clawdbot config）
3. ✅ **配置并重启** - 按照"步骤 2"操作
4. ✅ **验证配置** - 按照"步骤 3"验证
5. ✅ **测试功能** - 按照"步骤 4"测试

---

**准备好配置了吗？把你的 Supermemory API Key 告诉我，我帮你配置！** 🚀

或者你想用哪个配置方法（A/B/C）？
