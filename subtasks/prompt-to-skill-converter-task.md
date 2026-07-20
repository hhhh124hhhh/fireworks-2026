# 生图/生视频提示词转 Skill 子代理任务

**创建时间**: 2026-01-30 20:30
**代理 ID**: `prompt-to-skill-converter`

---

## 🎯 任务目标

收集 AI 生图和生视频提示词（Prompt），并转换成可发布的 Skills。

---

## 📱 数据源搜索关键词

### 生图提示词关键词
- `image prompt`
- `midjourney prompt`
- `dalle prompt`
- `stable diffusion prompt`
- `runwayML prompt`
- `leonardo ai prompt`
- `firefly ai prompt`
- `starryai prompt`
- `playgroundai prompt`
- `ai image generator`
- `AI 绘图提示词`
- `AI 画图指令`

### 生视频提示词关键词
- `video prompt`
- `kling ai prompt`
- `runway video prompt`
- `pika labs prompt`
- `sora prompt`
- `ai video generator`
- `AI 视频生成`
- `AI 做视频`

---

## 🔄 工作流程

### 阶段 1: 数据收集
**时间估计**: 5-10 分钟

**执行命令**:
```bash
# 1. 使用 SearXNG 搜索生图提示词
python3 /root/clawd/scripts/collect-prompts-test.py \
  --query "midjourney prompt stable diffusion dalle" \
  --output /root/clawd/data/prompts/image-prompts.jsonl

# 2. 使用 SearXNG 搜索生视频提示词
python3 /root/clawd/scripts/collect-prompts-test.py \
  --query "kling runway pika ai video generator" \
  --output /root/clawd/data/prompts/video-prompts.jsonl

# 3. 使用 Reddit 搜索相关讨论
python3 /root/clawd/scripts/collect-reddit-prompts.py \
  --subreddit "midjourney stable diffusion" \
  --limit 50

# 4. 使用 Hacker News 搜索 AI 工具
python3 /root/clawd/scripts/collect-hackernews.py \
  --query "midjourney dalle kling runway" \
  --limit 30
```

---

### 阶段 2: 提取 Prompt
**时间估计**: 3-5 分钟

**任务**:
- 从收集的数据中提取纯 prompt 内容
- 清理和格式化 prompt
- 识别 prompt 类型（生图/生视频）
- 评分和排序

---

### 阶段 3: 转换成 Skills
**时间估计**: 2-3 分钟

**任务**:
- 为每个 prompt 创建 SKILL.md 文件
- 使用标准格式：
  ```markdown
  # [类型] Prompt: [标题]

  ## 描述
  [简短描述]

  ## Prompt
  ```
  [prompt 内容]
  ```

  ## 标签
  - [相关标签]
  ```

---

### 阶段 4: 打包和去重
**时间估计**: 1-2 分钟

**任务**:
- 将每个 skill 打包成 .skill 文件
- 使用去重系统检查是否已存在
- 只保留新 skills

---

### 阶段 5: 发布到 ClawdHub
**时间估计**: 3-5 分钟

**任务**:
- 使用正确的 registry URL: `https://www.clawhub.ai/api`
- 批量上传所有 skills
- 验证上传结果
- 生成发布报告

---

### 阶段 6: 发送通知
**时间估计**: 1 分钟

**任务**:
- 发送 Slack 通知
- 发送 Feishu 通知
- 包含发布统计和链接

---

## 📊 预期产出

### 生图 Prompts
- **预计数量**: 50-100 个
- **质量**: 高（来自社区和教程）
- **类型**: Midjourney, DALL-E, Stable Diffusion 等

### 生视频 Prompts
- **预计数量**: 30-50 个
- **质量**: 高（来自 AI 工具讨论）
- **类型**: Kling, Runway, Pika Labs, Sora 等

### 总 Skills
- **预计数量**: 80-150 个
- **格式**: .skill 文件
- **状态**: 已发布到 ClawdHub

---

## 🛠️ 技术实现

### 搜索脚本扩展
```python
# collect-image-video-prompts.py
def search_image_prompts():
    """搜索 AI 生图 prompt"""
    queries = [
        "midjourney prompt template",
        "dalle prompt generator",
        "stable diffusion prompt",
        "AI 绘图指令大全",
        "AI image prompt examples"
    ]
    # 实现搜索逻辑

def search_video_prompts():
    """搜索 AI 生视频 prompt"""
    queries = [
        "kling ai prompt template",
        "runway video prompt",
        "pika labs prompt",
        "AI 视频生成 prompt",
        "AI 做视频指令"
    ]
    # 实现搜索逻辑
```

### Prompt 提取和转换
```python
# extract-and-convert-prompts.py
def extract_prompt_from_text(text):
    """从文本中提取 prompt"""
    # 使用正则表达式提取 prompt 内容
    # 清理和格式化
    pass

def convert_to_skill(prompt, prompt_type, source_info):
    """将 prompt 转换成 skill"""
    # 创建 SKILL.md 文件
    # 添加必要的元数据
    pass
```

### 批量上传脚本
```bash
# batch-upload-prompts.sh
# 批量上传所有生成的 skills
# 使用正确的 registry URL
# 验证上传结果
```

---

## ⚠️ 注意事项

1. **API 速率限制**
   - GitHub API 搜索有速率限制
   - 添加适当的延迟（1-2 秒）

2. **去重**
   - 使用去重系统避免重复
   - 基于 prompt 内容哈希

3. **质量过滤**
   - 只转换高质量的 prompt
   - 设置最低分数阈值（>= 60）

4. **Token 管理**
   - 确保 ClawdHub token 有效
   - 使用正确的 registry URL

---

## 📋 验收标准

### 数据收集
- [ ] 至少收集 80 个 unique prompts
- [ ] 生图 prompt: 至少 50 个
- [ ] 生视频 prompt: 至少 30 个
- [ ] 质量评分: 平均 >= 70

### Skill 转换
- [ ] 所有 prompt 都转换成 skills
- [ ] 格式正确（SKILL.md）
- [ ] 包含必要的元数据
- [ ] 标签准确

### 发布
- [ ] 所有 skills 成功打包
- [ ] 至少 90% 成功发布
- [ ] 已去重
- [ ] ClawdHub 可搜索到

---

## 🎯 子代理执行指令

```bash
# 启动子代理
clawdbot subagent start \
  --name prompt-to-skill-converter \
  --session main \
  --tasks \
    "收集生图提示词（关键词：midjourney, dalle, stable diffusion, runwayML）" \
    "收集生视频提示词（关键词：kling, runway, pika, sora）" \
    "提取和清理 prompt" \
    "转换成 skills（生图类型）" \
    "转换成 skills（生视频类型）" \
    "打包成 .skill 文件" \
    "去重检查" \
    "批量上传到 ClawdHub" \
    "生成发布报告" \
    "发送 Slack 通知" \
    "发送 Feishu 通知"
```

---

## 📊 预期时间

| 阶段 | 预计时间 |
|------|---------|
| 数据收集 | 5-10 分钟 |
| Prompt 提取 | 3-5 分钟 |
| Skill 转换 | 2-3 分钟 |
| 打包去重 | 1-2 分钟 |
| 上传发布 | 3-5 分钟 |
| 通知 | 1 分钟 |
| **总计** | **15-26 分钟** |

---

## 🚀 后续优化

1. **自动化定时任务**
   - 每天收集一次新的 prompt
   - 自动转换和上传
   - 持续更新 prompt 库

2. **质量提升**
   - 添加更精细的评分系统
   - 过滤低质量 prompt
   - 突出高质量 prompt

3. **分类系统**
   - 按类型分类（生图/生视频/其他）
   - 按风格分类（Midjourney/DALL-E/等）
   - 按难度分类（简单/中等/复杂）

---

**任务准备完成！准备好执行子代理！** 🚀
