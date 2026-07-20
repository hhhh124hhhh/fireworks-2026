# AI 研究搜索 - 优化版使用说明

**更新日期**: 2026-02-06
**优化内容**: 减少搜索主题数量，提高免费额度利用率

---

## 📊 优化对比

### 优化前
- **搜索主题**: 10 个
- **每天调用**: 50 次（10 × 5）
- **可用天数**: 20 天 ❌

### 优化后（默认）
- **搜索主题**: 5 个
- **每天调用**: 25 次（5 × 5）
- **可用天数**: 40 天 ✅

### 混合模式（备选主题）
- **核心主题**: 5 个
- **备选主题**: 1 个（每周轮换）
- **每天调用**: 30 次（5 × 5 + 1 × 5）
- **可用天数**: 33 天 ✅

---

## 🎯 核心搜索主题（5 个）

1. **Claude AI updates 2026**
   - 跟踪 Claude 最新动态

2. **OpenAI GPT-5 news**
   - 跟踪 GPT-5 最新消息

3. **AI prompt engineering best practices**
   - 提示词工程最佳实践

4. **AI tools for developers 2026**
   - 开发者 AI 工具

5. **machine learning trends 2026**
   - 机器学习趋势

---

## 📅 备选搜索主题（5 个，每周轮换）

1. **Claude coding agent**
   - Claude 编码代理

2. **OpenAI function calling**
   - OpenAI 函数调用

3. **AI automation tools**
   - AI 自动化工具

4. **AI skill development**
   - AI 技能开发

5. **AI workflow automation**
   - AI 工作流自动化

**轮换方式**：根据星期几自动选择（周一到周日）

---

## 🔧 使用方法

### 1. 默认模式（5 个核心主题）

```bash
bash /root/clawd/projects/info-search/workflows/ai-research-extended.sh
```

**每天调用**: 25 次
**可用天数**: 40 天

---

### 2. 混合模式（核心 + 备选主题）

```bash
ENABLE_WEEKLY_TOPICS=true bash /root/clawd/projects/info-search/workflows/ai-research-extended.sh
```

**每天调用**: 30 次
**可用天数**: 33 天

---

### 3. 自定义搜索主题

```bash
SEARCH_TOPICS="主题1,主题2,主题3" bash ai-research-extended.sh
```

**示例**:
```bash
# 自定义主题
SEARCH_TOPICS="Python async tips,Rust memory safety,Go concurrency" bash ai-research-extended.sh

# 组合主题
SEARCH_TOPICS="Claude AI updates 2026,OpenAI GPT-5 news,React performance" bash ai-research-extended.sh
```

**每天调用**: 自定义主题数量 × 5

---

### 4. 启用自动推送

```bash
PUSH_SUMMARY=true bash /root/clawd/projects/info-search/workflows/ai-research-extended.sh
```

---

## ⚙️ Cron 任务

### 默认模式（5 个核心主题）

```cron
0 8 * * * /root/clawd/projects/info-search/workflows/ai-research-extended.sh >> /root/clawd/logs/ai-research-cron.log 2>&1
```

**每天调用**: 25 次
**可用天数**: 40 天

---

### 混合模式（核心 + 备选主题）

更新 Cron 任务：
```bash
# 编辑 crontab
crontab -e

# 添加以下行
0 8 * * * ENABLE_WEEKLY_TOPICS=true /root/clawd/projects/info-search/workflows/ai-research-extended.sh >> /root/clawd/logs/ai-research-cron.log 2>&1
```

**每天调用**: 30 次
**可用天数**: 33 天

---

## 📈 Tavily API 使用情况

### 当前配置

**免费额度**: 1,000 次/月
**API Key**: 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

### 使用量估算

| 模式 | 每天调用 | 每月调用 | 可用天数 | 状态 |
|------|---------|---------|---------|------|
| 默认（5 个主题） | 25 次 | 750 次 | 40 天 | ✅ 推荐 |
| 混合（6 个主题） | 30 次 | 900 次 | 33 天 | ✅ 可用 |
| 自定义（10 个主题） | 50 次 | 1,500 次 | 20 天 | ❌ 不够 |

### 实际使用

**当前使用**: 约 85 次（测试）
**剩余额度**: 约 915 次/月

---

## 📊 搜索结果

### 输出文件

**日志文件**: `/root/clawd/memory/ai-research/ai-research-YYYYMMDD_HHMMSS.log`
- 完整的搜索结果
- 每个主题的详细信息
- 时间戳和 URL

**摘要文件**: `/root/clawd/memory/ai-research/ai-research-summary-YYYYMMDD_HHMMSS.md`
- 统计摘要
- 搜索主题列表
- 结果数量

### 示例输出

```markdown
# AI 研究搜索摘要

**日期**: 2026-02-06
**时间**: 08:53:09
**搜索主题数量**: 5

## 统计摘要

- **总搜索主题**: 5
- **总结果数量**: 25
- **平均结果数量**: 5

## 搜索主题列表

- **Claude AI updates 2026**: 5 条结果
- **OpenAI GPT-5 news**: 5 条结果
- **AI prompt engineering best practices**: 5 条结果
- **AI tools for developers 2026**: 5 条结果
- **machine learning trends 2026**: 5 条结果
```

---

## 🚀 下一步建议

### 短期（1-2 周）

1. **监控使用情况**
   - 每周检查 API 使用量
   - 调整搜索主题数量

2. **评估搜索结果质量**
   - 检查搜索结果的相关性
   - 优化搜索关键词

3. **测试混合模式**
   - 启用备选主题
   - 观察每周轮换效果

### 中期（1-2 月）

4. **注册更多搜索 API**
   - **Brave Search**: 2,000 次/月免费
   - **SerpAPI**: 100 次/月免费
   - **总计**: 3,100 次/月免费

5. **集成到其他工作流**
   - 集成到 `HEARTBEAT.md`
   - 添加到主工作流

6. **自动化分析**
   - 分析搜索结果的趋势
   - 生成周报/月报

### 长期（3-6 月）

7. **实现智能推荐**
   - 根据历史结果推荐搜索主题
   - 自动调整搜索策略

8. **建立知识图谱**
   - 整合搜索结果
   - 建立知识关联

---

## 📄 相关文件

**工作流脚本**:
- `/root/clawd/projects/info-search/workflows/ai-research-extended.sh` - 优化版
- `/root/clawd/projects/info-search/workflows/push-ai-research-summary.sh` - 推送脚本

**配置脚本**:
- `/root/clawd/projects/info-search/workflows/setup-cron.sh` - 初始设置
- `/root/clawd/projects/info-search/workflows/update-cron.sh` - 更新 Cron

**输出目录**:
- `/root/clawd/memory/ai-research/` - 搜索结果和摘要

**项目文档**:
- `/root/clawd/projects/info-search/README.md` - 项目文档
- `/root/clawd/projects/info-search/docs/search-api-list.md` - 搜索 API 清单

---

## 🔍 常见问题

### Q: 如何查看最新的搜索结果？

```bash
cat $(cat /root/clawd/memory/ai-research/latest-summary.txt)
```

### Q: 如何手动测试搜索功能？

```bash
# 默认模式
bash /root/clawd/projects/info-search/workflows/ai-research-extended.sh

# 混合模式
ENABLE_WEEKLY_TOPICS=true bash /root/clawd/projects/info-search/workflows/ai-research-extended.sh

# 自定义主题
SEARCH_TOPICS="主题1,主题2" bash ai-research-extended.sh
```

### Q: 如何查看 Cron 日志？

```bash
tail -f /root/clawd/logs/ai-research-cron.log
```

### Q: 如何更新 Cron 任务？

```bash
# 备份当前 crontab
crontab -l > /tmp/crontab-backup

# 编辑 crontab
crontab -e

# 或使用更新脚本
bash /root/clawd/projects/info-search/workflows/update-cron.sh
```

### Q: 免费额度用完了怎么办？

1. 注册 Brave Search（2,000 次/月免费）
2. 注册 SerpAPI（100 次/月免费）
3. 考虑付费 Tavily API
4. 减少搜索主题或结果数量

---

**更新时间**: 2026-02-06
**版本**: 2.0 (优化版）
