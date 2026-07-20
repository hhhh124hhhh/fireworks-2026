# MEMORY.md - 核心记忆

*这是精简版核心记忆，只包含最重要的信息。详细内容已拆分到独立的 memory skills。*

## 关于用户
- **姓名**: jack
- **称呼**: jack
- **Pronouns**: (未指定)
- **Timezone**: (未指定)
- **备注**: 关注 Clawdbot 技能开发，对自动化流程感兴趣，正在探索商业变现路径

## 重要项目

### 🎯 AI 提示词转 Skill 商业计划
**目标**: 自动化抓取 Twitter/X 上的热门 AI 提示词，评估质量，转换为 Clawdbot Skill，并打包售卖

**状态**: 
- ✅ Twitter API key 已配置
- ✅ 测试抓取功能
- ✅ 手动评估推文
- ✅ 转换第一个提示词为 Skill (tiktok-ai-model-generator)
- ⏳ 发布到 ClawdHub

**详细内容**: 使用 `memory-projects` skill 查看

## 技术基础设施

### SearXNG 自建搜索服务
- Docker 镜像: `searxng/searxng:latest`
- 运行端口: 8080
- 状态: ✅ 运行中
- 使用策略: 优先使用 SearXNG，避免 Brave API
- 配置位置: ~/.env.d/

**详细配置**: 使用 `memory-tech-infra` skill 查看

## 设置和偏好

### 📝 记忆策略偏好
用户要求更积极的记忆策略，在关键时点自动写入：
1. 重要决策
2. 用户偏好
3. 项目进度
4. 问题解决

### 🔄 子代理结果上传规则
每个子代理运行成功后，把结果上传到私有仓库：
- 仓库: https://github.com/hhhh124hhhh/Clawdbot-Skills-Converter.git
- 流程: git add . → git commit → git push

### 工作偏好
- 关注 Clawdbot 技能开发
- 对自动化流程感兴趣
- 正在探索商业变现路径
- 希望主动记录，避免重复询问

### 🗂️ 项目仓库
**私有仓库**: https://github.com/hhhh124hhhh/Clawdbot-Skills-Converter.git
**用途**: 存储项目文档、策略文件、工作成果

## 重要配置

### API Keys
- **Twitter/X API**: 已配置 (~/.bashrc)
- **ClawdHub Token**: clh_Ki_M1Xiws5Qzi83gqdZhYG3jXSuZOnEfQOxhaRsjHcw
- **Registry**: https://www.clawhub.ai/api

### Coding Agent
- **认知**: coding-agent 就是使用 Claude
- **用途**: 编程任务、代码编写、调试
- **调用方式**: coding-agent skill 或直接使用 claude 命令

## 最近状态（2026-02-02）

### 已解决问题
- ✅ Slack Bot 不回复 - 增加上下文限制到 100k
- ✅ Gateway 日志问题 - 重启解决
- ✅ QQ Bot URL 限制 - 配置完成（待重启）

### 待处理问题
- QQ Bot URL 限制问题（需要重启 Gateway）
- auto-publish-skills: 'SKILL.md required' error
- full-prompt-workflow: 2 skills failed to publish
- clawdhub-tracking: Found 0 out of 4 tracked skills
- searxng skill missing
- achievement-system-dev sub-agent not found
- achievement-system: 尚未开始
- twitter-search: Script ran but may not have saved new data

### 系统配置
- **Gateway**: 运行中 (PID 539567)
- **模型**: zai/glm-4.7 (131k context)
- **上下文限制**: 100k
- **Slack**: ✅ 正常工作
- **Feishu**: ✅ 正常工作
- **QQ**: ⏸️ 待配置

## Memory Skills 索引

- `memory-projects` - AI 提示词商业计划、成就系统
- `memory-tech-infra` - 技术基础设施（SearXNG、Gateway 配置）
- `memory-debugging` - 调试经验记录
- `memory-moltbot` - Moltbot 研究分析
- `memory-workflows` - 自动化工作流、Cron Jobs
- `memory-best-practices` - Python 命名规范、环境变量
- `memory-personal` - jack 的个人主页信息
- `memory-solutions` - 问题解决方案（上下文溢出等）
