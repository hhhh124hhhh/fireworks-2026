# 生图/生视频 Prompts 转 Skills 子代理 - 完整配置

**创建时间**: 2026-01-30 20:35
**任务 ID**: `prompt-to-skill-converter`

---

## 🎯 任务目标

收集 AI 生图和生视频 Prompts，并将其转换为可发布的 Skills。

---

## 📱 任务描述

这个子代理将：

1. **搜索 Prompts**
   - 使用 SearXNG 搜索生图关键词（Midjourney, DALL-E, Stable Diffusion 等）
   - 使用 SearXNG 搜索生视频关键词（Kling, Runway, Pika Labs, Sora 等）
   - 从多个数据源收集高质量 Prompts

2. **提取和清理**
   - 从搜索结果中提取 Prompt 内容
   - 清理和格式化 Prompt
   - 识别 Prompt 类型（生图/生视频）
   - 计算质量分数

3. **转换为 Skills**
   - 为每个高质量 Prompt 创建 SKILL.md 文件
   - 使用标准格式（标题、描述、Prompt、标签）
   - 添加元数据（来源、类型、质量分数）

4. **打包和发布**
   - 将 Skills 打包成 .skill 文件
   - 批量上传到 ClawdHub（使用正确的 registry）
   - 验证上传结果

5. **生成报告**
   - 生成详细的收集和发布报告
   - 包含统计数据和链接

---

## 🔄 执行流程

### 阶段 1: 数据收集（5-10 分钟）

```bash
python3 /root/clawd/scripts/collect-image-video-prompts.py
```

**输出**:
- `/root/clawd/data/prompts/image-prompts.jsonl`
- `/root/clawd/data/prompts/video-prompts.jsonl`
- `/root/clawd/data/prompts/prompt-collection-report.json`

---

### 阶段 2: 转换为 Skills（3-5 分钟）

```bash
python3 /root/clawd/scripts/convert-prompts-to-skills.py
```

**输出**:
- `/root/clawd/generated-skills/skill-[name]/SKILL.md` (多个）
- `/root/clawd/generated-skills/metadata.json` (汇总)

**过滤条件**:
- 只保留质量分数 >= 60 的 Prompts
- 避免重复内容
- 确保有效的 Prompt 格式

---

### 阶段 3: 打包和去重（2-3 分钟）

```bash
# 转换脚本会自动打包
# 使用去重系统检查已发布的 Skills
```

**输出**:
- `/root/clawd/dist/skill-[name].skill` (多个)
- 去重日志

---

### 阶段 4: 上传到 ClawdHub（3-5 分钟）

```bash
clawdhub \
  --registry https://www.clawhub.ai/api \
  --workdir /root/clawd/generated-skills \
  publish \
  --version 1.0.0 \
  skill-[name]
```

**输出**:
- 所有 Skills 上传到 ClawdHub
- 上传日志
- 验证报告

---

### 阶段 5: 生成报告（1 分钟）

```bash
python3 /root/clawd/scripts/generate-prompt-report.py
```

**输出**:
- Markdown 报告（Top 20 Prompts）
- JSON 报告（完整统计数据）
- ClawdHub 链接

---

## 📊 预期产出

### 数据收集
- **生图 Prompts**: 50-100 个高质量
- **生视频 Prompts**: 30-50 个高质量
- **总 Prompts**: 80-150 个

### Skill 转换
- **生图 Skills**: 30-50 个（过滤后）
- **生视频 Skills**: 20-30 个（过滤后）
- **总 Skills**: 50-80 个

### ClawdHub 发布
- **成功发布**: 40-60 个
- **发布率**: 预计 80%+
- **可搜索**: 所有 Skills 都可搜索

---

## 🎯 数据源

### 搜索关键词

**生图**:
- `midjourney prompt template`
- `dalle prompt generator`
- `stable diffusion prompt`
- `AI 绘图提示词`
- `AI image generation`

**生视频**:
- `kling ai prompt`
- `runway video prompt`
- `pika labs prompt`
- `sora prompt`
- `AI 视频生成`

### 平台覆盖

**SearXNG**:
- Google 搜索
- Bing 搜索
- DuckDuckGo 搜索
- GitHub 搜索

**社区平台**:
- Reddit (r/StableDiffusion, r/Midjourney)
- Dev.to
- Medium（通过搜索）

---

## 🔍 质量评估

### 评分标准（0-100 分）

**内容质量** (40 分):
- Prompt 完整性 (0-20)
- Prompt 结构 (0-20)

**可用性** (30 分):
- 易于使用 (0-15)
- 灵活性 (0-15)

**相关性** (20 分):
- 是否为生图/生视频专用 (0-10)
- 是否符合最新技术 (0-10)

**流行度** (10 分):
- 来自知名来源 (0-10)

### 过滤条件

- 最低质量分数: **60 分**
- 最大 Prompt 长度: **2000 字符**
- 最短 Prompt 长度: **50 字符**
- 重复检查: **启用**

---

## 💡 使用建议

### 技能学习

**生图 Prompts**:
- 学习 Midjourney 特定参数
- 掌握 Stable Diffusion LoRA
- 了解 DALL-E 3 提示词结构

**生视频 Prompts**:
- 学习 Kling AI 参数
- 掌握 RunwayML 特点
- 了解 Pika Labs 风格

### 实用技巧

- 从高质量 Prompts 中提取模式
- 创建自己的 Prompt 模板
- 建立工作流程

---

## 📋 任务依赖

### 已满足
- ✅ SearXNG 服务可用
- ✅ ClawdHub Token 已配置
- ✅ GitHub API 访问
- ✅ 输出目录已创建

### 待配置
- ⏸️ 定时任务（执行时间）
- ⏸️ 通知渠道（报告发送）

---

## 🚀 执行命令

### 手动执行（立即）

```bash
# 1. 收集 Prompts
python3 /root/clawd/scripts/collect-image-video-prompts.py

# 2. 转换为 Skills
python3 /root/clawd/scripts/convert-prompts-to-skills.py

# 3. 上传到 ClawdHub
clawdhub \
  --registry https://www.clawhub.ai/api \
  --workdir /root/clawd/generated-skills \
  publish \
  --version 1.0.0 \
  skill-*
```

### 自动执行（定时任务）

**推荐时间**: 每天凌晨 3:00
**任务名称**: `prompt-to-skill-converter`

---

## 📊 监控指标

### 收集阶段
- 搜索查询数
- 找到的结果数
- 去重后的 Prompts 数
- 高质量 Prompts 数

### 转换阶段
- 创建的 Skills 数
- 跳过的 Prompts 数
- 平均质量分数

### 发布阶段
- 打包的 Skills 数
- 上传成功的 Skills 数
- 上传失败的 Skills 数
- 总耗时

---

## ✅ 成功标准

### 最小目标
- [ ] 收集至少 50 个高质量 Prompts
- [ ] 转换为至少 30 个 Skills
- [ ] 成功发布至少 20 个 Skills
- [ ] 生成完整报告

### 理想目标
- [ ] 收集 100 个高质量 Prompts
- [ ] 转换为 60 个 Skills
- [ ] 成功发布 50 个 Skills
- [ ] 建立持续更新流程

---

## 🔄 后续优化

### 短期（1-2 周）
1. **优化搜索查询**
   - 测试不同关键词组合
   - 调整质量评分阈值
   - 添加更多数据源

2. **提升转换质量**
   - 优化 Prompt 格式化
   - 改进标签生成
   - 增强描述质量

### 中期（1 个月）
1. **自动化定时任务**
   - 每天自动收集新 Prompts
   - 自动转换和上传
   - 自动生成报告

2. **建立反馈机制**
   - 跟踪 Skill 下载量
   - 收集用户反馈
   - 优化推荐算法

3. **扩展功能**
   - 添加更多 Prompt 类型
   - 支持自定义搜索
   - 提供 Prompt 编辑器

### 长期（3 个月）
1. **建立 Prompt 数据库**
   - 持久化存储所有 Prompts
   - 实现语义搜索
   - 提供高级筛选

2. **开发 Prompt 管理工具**
   - Web 界面管理 Skills
   - 批量操作和编辑
   - 性能监控和分析

3. **社区集成**
   - 开放用户提交 Prompts
   - 投票和评论功能
   - 顶级 Prompts 排行榜

---

## 🎯 最终目标

建立一个持续更新的 **AI Prompt 转换系统**，为开发者提供高质量的生成工具。

**关键特性**:
- 自动收集高质量 Prompts
- 智能转换和分类
- 批量发布到 ClawdHub
- 详细的统计和报告

---

**任务准备完成！** 🚀

准备好执行子代理了！
