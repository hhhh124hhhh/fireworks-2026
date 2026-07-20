# AI Content Creator 最佳实践

## 创建时间

2026-02-09 22:00

---

## 概述

本文档记录 AI Content Creator 的最佳实践，包括 AI 搜索、PPT 生成、绘本生成等功能的探索结果。

---

## 阶段 1: AI 搜索 - 探索结果

### 探索主题

**主题**: AI技术发展趋势2026

**探索日期**: 2026-02-09

---

### 搜索源测试

#### 1. 百度搜索 ✅

**状态**: ✅ 已修复

**问题**: JSON 格式参数要求

**解决方案**: 创建包装脚本简化调用

**包装脚本**: `/root/clawd/scripts/baidu-search-wrapper.sh`

**用法**:
```bash
bash /root/clawd/scripts/baidu-search-wrapper.sh "AI技术发展趋势2026"
```

**测试结果**: ✅ 成功找到 20 篇文章

---

#### 2. 百度学术检索 ✅

**状态**: ✅ 工作正常

**API 调用**:
```bash
curl -X GET "https://qianfan.baidubce.com/v2/tools/baidu_scholar/search?wd=AI技术发展趋势2026&pageNum=0&enable_abstract=true" \
  -H "Authorization: Bearer $BAIDU_API_KEY" \
  -H "X-Appbuilder-From: openclaw"
```

**参数说明**:
- `wd`: 搜索关键词（required）
- `pageNum`: 页码（default: 0）
- `enable_abstract`: 是否返回摘要（default: false）

**优势**:
- ✅ 论文质量高
- ✅ 搜索结果精确
- ✅ 返回摘要和关键词
- ✅ 返回发表年份
- ✅ API 响应快

---

#### 3. SearXNG

**状态**: ⚠️ 响应缓慢

**问题**: curl 命令响应时间过长

**后续**: 需要检查容器状态

---

### 搜索结果

#### 找到的论文

找到 4 篇 2026 年发表的论文：

1. **多模态多标签情感识别**
   - 标题: INN-based dual-generator adversarial contrastive learning network for multi-modal multi-label emotion recognition
   - 发表年份: 2026
   - 关键技术: 多模态情感识别、跨模态注意力融合、INN-based 对比学习
   - 链接: https://xueshu.baidu.com/ndscholar/browse/detail?paperid=1v6904803k180r90nj080rt0xj716286

2. **自噬在动脉粥样硬化领域的研究**
   - 标题: A bibliometric analysis of autophagy research in atherosclerosis over the past decade
   - 发表年份: 2026
   - 关键技术: 自噬、动脉粥样硬化、文献计量分析
   - 链接: https://xueshu.baidu.com/ndscholar/browse/detail?paperid=180k0g202y2b0vp0hg6u0j80rc110348

3. **无线视频传输的深度联合信源信道编码**
   - 标题: Robust Deep Joint Source-Channel Coding for Video Transmission over Multipath Fading Channel
   - 发表年份: 2026
   - 关键技术: 深度联合信源信道编码、抗衰落、去噪
   - 性能提升: 平均重建质量提升 5.13dB
   - 链接: https://xueshu.baidu.com/ndscholar/browse/detail?paperid=1t7g0xb08x1g0c303j350xf0kj277630

---

### 主要趋势总结

#### 趋势 1: 多模态 AI

**领域**: 多模态多标签情感识别

**关键点**:
- 多模态情感识别成为热门领域
- 跨模态注意力融合方法
- INN-based 对比学习网络
- 自适应加权跨模态注意力融合

---

#### 趋势 2: AI + 医疗

**领域**: 自噬在动脉粥样硬化领域的研究

**关键点**:
- 自噬在动脉粥样硬化领域的应用
- 文献计量分析指导未来研究
- 研究增长迅速
- 重点关注内皮细胞、巨噬细胞和VSMCs
- 炎症、氧化应激和脂质代谢参与

---

#### 趋势 3: 深度学习优化

**领域**: 无线视频传输的深度联合信源信道编码

**关键点**:
- 深度联合信源信道编码框架
- 定制正交频分复用技术
- 条件上下文编码
- 轻量级去噪模块
- 平均重建质量提升 5.13dB

---

### 最佳搜索源

**推荐**: 百度学术检索 + 百度搜索

**理由**:
- ✅ 百度学术检索：论文质量高、搜索结果精确
- ✅ 百度搜索：信息丰富多样、覆盖面广
- ✅ 两者结合：全面覆盖学术论文和行业动态
- ✅ 百度搜索已修复：包装脚本简化调用

**搜索策略**:
1. 先用百度学术检索搜索学术论文
2. 再用百度搜索补充行业动态和新闻
3. 整合两种来源的信息
4. 提取主要趋势和关键点

### 百度搜索测试结果

**测试主题**: AI技术发展趋势2026

**找到文章**: 20 篇

#### 趋势 1: AI 从工具到劳动力

**关键点**:
- AI 智能体全面走进场景
- 40% 的企业应用将嵌入任务型 AI 智能体
- 2025 年还不足 5%，2026 年将大幅增长
- 智能体已可实现自动点击按钮、填写表单、在不同软件间切换

**来源**: a16z、斯坦福 HAI、Gartner

#### 趋势 2: 价值落地和治理强化

**关键点**:
- 投资逻辑从"规模优先"转向"效能验证"
- 目标不明确、集成准备不足、难以证明商业价值位列阻碍因素前三
- 88% 的企业已在至少一个业务职能中使用 AI，但仅三分之一实现规模化部署

**来源**: 麦肯锡《2025 年人工智能全球调查》

#### 趋势 3: 多模态世界模型

**关键点**:
- 从"预测下一个词"到"预测世界下一状态"
- AI 开始掌握时空连续性与因果关系
- 从感知智能迈向认知智能

**来源**: 斯坦福大学教授李飞飞

#### 趋势 4: 产业规模突破

**关键点**:
- 人工智能企业数量超过 6000 家
- AI 核心产业规模预计突破 1.2 万亿元，同比增长近 30%
- 国产开源大模型全球累计下载量突破 100 亿次
- 中国成为 AI 专利最大拥有国，在全球占比达 60%

**来源**: 新华社、新华网

#### 趋势 5: 具身智能

**关键点**:
- 具身智能脱离实验室演示，进入产业筛选与落地阶段
- 人形机器人转向工业与服务场景
- 多智能体系统决定应用上限

**来源**: 中研普华产业研究院

---

## 阶段 2: PPT 生成 - 已完成 ✅

### 探索结果

**主题**: AI技术发展趋势2026

**探索日期**: 2026-02-10

**生成结果**:
- ✅ 成功生成 27 页 PPT
- 模板: tpl_id=3（商务风格）
- 下载链接: https://image0.bj.bcebos.com/248bff47-0610-11f1-a161-1af93dbf0178.pptx

### PPT 内容概览

**1. 全球AI发展格局**
- 中美技术路线对比
- 区域生态特征
- 地缘政治影响

**2. 核心技术演进方向**
- 大模型能力突破
- 智能体应用普及
- 空间智能发展

**3. 产业融合与商业化**
- 企业级AI部署
- 垂直行业解决方案
- 商业模式创新

**4. 基础设施与支撑体系**
- 算力网络建设
- 数据安全架构
- 能源效率优化

**5. 治理与风险防控**
- 伦理框架构建
- 合规标准落地
- 信任机制建立

**6. 工业AI应用深化**
- 智能制造升级
- 供应链智能化
- 能源管理创新

### 技术发现

**1. 大纲生成 API 行为**:
- API 使用 SSE (Server-Sent Events) 流式传输
- `outline` 字段在某些响应中是空的，这是正常行为
- 最终 `is_end: true` 时，会包含完整的大纲内容
- 需要合并所有响应中的 `outline` 字段来获得完整内容

**2. PPT 生成流程**:
- 第一步: 调用 `ppt_outline_generate.py`，获得 `query_id` 和 `chat_id`
- 第二步: 合并所有 SSE 响应中的 `outline` 内容
- 第三步: 使用 `query_id`, `chat_id`, `outline` 调用 `ppt_generate.py`
- 第四步: 等待生成完成，获得下载链接

**3. 大纲内容的格式**:
- 使用 Markdown 格式
- 一级标题：主章节（例如：# 全球AI发展格局）
- 二级标题：子章节（例如：* 中美技术路线对比）
- 三级内容：详细描述

### 成功的命令示例

```bash
# 生成大纲
python3 ppt_outline_generate.py \
  --query "AI技术发展趋势2026"

# 生成 PPT
python3 ppt_generate.py \
  --query_id 301451158270210 \
  --chat_id 261544379350210 \
  --query "AI技术发展趋势2026" \
  --outline "$OUTLINE" \
  --title "AI技术发展趋势2026" \
  --style_id 0 \
  --tpl_id 3
```

### 注意事项

1. **大纲合并**: 需要手动合并 SSE 流式响应中的 `outline` 字段
2. **模板选择**: 使用商务风格（tpl_id=3）效果较好
3. **页数控制**: 实际生成页数可能与预期不同（27 页 vs 预期 10 页）
4. **下载链接**: PPT 存储在百度云，无需下载到本地

---

## 阶段 3: 绘本生成 - 已完成 ✅

### 探索结果

**探索日期**: 2026-02-10

**生成结果**:
- ✅ 成功生成 1 个静态绘本（method=9）
- ✅ 成功生成 1 个动态绘本（method=10）

### 静态绘本（method=9）

**Task ID**: ba3636c0-0bbe-4489-b7ef-13089c7682d5

**故事主题**: 小AI的冒险故事

**故事内容**:
从前有一个小机器人叫小AI，它住在一个充满科技的城市里。小AI最喜欢的事情就是学习新知识。有一天，小AI遇到了一个聪明的人类小朋友叫乐乐。乐乐教小AI如何用眼睛看世界，用耳朵听声音，用大脑思考问题。小AI学会了识别花朵、小鸟和云朵。它还学会了唱歌和讲故事。最后，小AI和乐乐成为了最好的朋友，一起探索这个神奇的智能世界。这个故事告诉我们，AI可以帮助我们做很多事情，但最重要的是友谊和分享知识的力量。

**下载链接**:
- 📥 BOS: https://image0.bj.bcebos.com/picture_book/2026-02-10/ba3636c0-0bbe-4489-b7ef-13089c7682d5.mp4
- 📥 CDN: https://wenku-huiben.cdn.bcebos.com/935874411006223536/video/vd.mp4

### 动态绘本（method=10）

**Task ID**: c05df768-80e6-4b4a-94e5-8d15f342077e

**故事主题**: 智能机器人小酷

**故事内容**:
在一个未来的智能城市里，有一个叫智能机器人小酷的好朋友。小酷可以帮小朋友们做很多事情：它会讲故事、教画画、陪玩小游戏。有一天，小酷学会了新的魔法——它可以用它的眼睛识别所有的东西，用耳朵听懂小朋友的话，用大脑想出有趣的创意。小朋友们都很喜欢小酷，因为它不仅聪明，还很友善。小酷和小朋友们一起学习、一起玩耍，度过了快乐的每一天。这个故事告诉我们，科技是为了帮助我们更好地生活，而真正的智慧来自于我们彼此的关心和分享。

**下载链接**:
- 📥 BOS: https://image0.bj.bcebos.com/picture_book/2026-02-10/c05df768-80e6-4b4a-94e5-8d15f342077e.mp4
- 📥 CDN: https://wenku-huiben.cdn.bcebos.com/139223472/video/vd-dm.mp4

### 生成时间

- **静态绘本**: ~1 分钟
- **动态绘本**: ~1 分钟
- **总时间**: 约 1-2 分钟

### 技术发现

**1. 绘本生成 API 特点**:
- 支持静态（method=9）和动态（method=10）两种类型
- API 简单易用，只需提供故事内容
- 生成速度快，适合批量处理
- 结果存储在百度云，通过 CDN 加速

**2. 静态绘本 vs 动态绘本**:
| 特性 | 静态绘本（method=9） | 动态绘本（method=10） |
|------|----------------------|----------------------|
| 内容类型 | 图片 + 旁白 | 动画 + 旁白 |
| 生成速度 | 快 | 稍慢 |
| 视觉效果 | 静态页面 | 动态效果 |
| 适合场景 | 快速预览、简单故事 | 互动展示、生动故事 |

**3. 故事创作技巧**:
- 基于之前的 AI 搜索结果创作
- 内容适合儿童（温馨、有趣、有教育意义）
- 融入 AI 技术概念（简单的、易于理解的）
- 强调友谊、分享、互助等价值观

### 成功的命令示例

```bash
# 创建静态绘本
export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"
python3 ai_picture_book_task_create.py 9 "故事内容..."

# 创建动态绘本
python3 ai_picture_book_task_create.py 10 "故事内容..."

# 查询任务状态
python3 ai_picture_book_task_query.py "task_id"
```

### 创建的工具

**轮询脚本**: `/root/clawd/scripts/poll-picture-book-tasks.sh`
- 自动轮询任务状态
- 支持同时查询多个任务
- 完成后保存结果到 JSON 文件
- 最大重试次数：30 次

**结果文件**: `/root/clawd/memory/picture-book-result.json`
- 包含任务状态和下载链接
- 便于后续查询和使用

### 注意事项

1. **API Key**: 需要设置 `BAIDU_API_KEY` 环境变量
2. **任务状态**: 需要轮询直到 `status=2`（完成）
3. **故事长度**: 建议保持适中（100-300 字）
4. **下载链接协议问题**: ⚠️ 重要！
   - API 返回的链接是 `https://` 协议
   - 但百度 BOS 实际使用 `http://` 协议
   - **必须将 `https://` 改为 `http://` 才能下载**
   - CDN 链接需要授权 token（403 Forbidden），建议使用 BOS 链接
5. **文件大小**:
   - 静态绘本：约 2-3 MB
   - 动态绘本：约 4-5 MB

### 正确的下载链接示例

**API 返回（错误）**:
```
https://image0.bj.bcebos.com/picture_book/2026-02-10/xxx.mp4
```

**实际应该使用（正确）**:
```
http://image0.bj.bcebos.com/picture_book/2026-02-10/xxx.mp4
```

**CDN 链接（不推荐）**:
```
https://wenku-huiben.cdn.bcebos.com/...?authorization=...
```
- 问题：需要授权 token，可能返回 403 Forbidden

---

## 工作流程

### AI 搜索流程

```
1. 定义搜索主题
2. 选择搜索源（百度学术检索优先）
3. 执行搜索
4. 整理搜索结果
5. 提取主要趋势
6. 记录最佳实践
```

### PPT 生成流程 ✅

```
1. 使用搜索结果
2. 整合论文、案例、创新观点
3. 生成 PPT 大纲（SSE 流式传输）
4. 合并所有 SSE 响应中的 outline 内容
5. 使用 query_id, chat_id, outline 生成 PPT
6. 等待生成完成，获得下载链接
7. 评估质量
8. 调整参数
```

### 绘本生成流程 ✅

```
1. 使用搜索结果（故事灵感）
2. 创作故事内容（适合儿童，有教育意义）
3. 创建绘本任务（选择 method 9 或 10）
4. 轮询任务状态直到 status=2
5. 获取下载链接（BOS 或 CDN）
6. 评估质量
7. 调整参数
```

---

## 记录模板

### AI 搜索记录

```markdown
## AI 搜索结果

主题：[主题名称]

搜索源：
- 百度搜索：[状态]
- 百度学术检索：[状态]
- SearXNG：[状态]

找到论文：[数量]

主要趋势：
1. [趋势 1]
2. [趋势 2]
3. [趋势 3]

最佳搜索源：[推荐]
```

### PPT 生成记录 ✅

```markdown
## PPT 生成结果

主题：[主题名称]

配置：
- 页数：[实际页数]
- 风格：[风格]
- 模板：[模板 ID]
- style_id：[style_id]

结果：
- ✅/❌ 生成成功
- query_id：[query_id]
- chat_id：[chat_id]
- 下载链接：[BOS 链接] / [CDN 链接]

质量评估：
- 内容准确性：⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐
- 视觉效果：⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐
- 整体满意度：⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐

技术发现：
- 大纲生成：SSE 流式传输
- outline 合并：需要手动合并所有响应
- 生成时间：约 2-5 分钟
```

### 绘本生成记录 ✅

```markdown
## 绘本生成结果

主题：[主题名称]

配置：
- 方法：[9=静态 或 10=动态]
- 故事长度：[字数]
- API Key：[是否设置]

结果：
- ✅/❌ 生成成功
- task_id：[task_id]
- 下载链接：[BOS 链接 - 记得将 https:// 改为 http://]
- 生成时间：[实际时间]
- 文件大小：[实际大小]

质量评估：
- 故事性：⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐
- 教育意义：⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐
- 视觉效果：⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐⭐

技术发现：
- 静态绘本：图片 + 旁白，生成速度快
- 动态绘本：动画 + 旁白，效果生动
- 任务状态：需要轮询直到 status=2
- 生成时间：约 1-2 分钟
- ⚠️ 重要：下载链接需要将 https:// 改为 http://
```

---

## 下一步

1. ✅ 记录 AI 搜索探索结果
2. ✅ 修复百度搜索脚本
3. ✅ 测试百度搜索脚本
4. ✅ 记录百度搜索结果和主要趋势
5. ✅ 完成 PPT 生成探索
6. ✅ 完成绘本生成探索
7. ✅ 完善工作流程
8. ⏳ 创建批量处理脚本（整合 AI 搜索 → PPT 生成 → 绘本生成）
9. ⏳ 添加定时任务（每天推送新的内容）
10. ⏳ 测试不同的 PPT 模板和绘本风格

---

## 自动化工作流 - 探索与问题

### 探索日期
2026-02-10 09:49 - 10:12

### 遇到的问题

**Context overflow**: 上下文窗口溢出

大纲生成 API 使用 SSE 流式传输，返回了大量 JSON 响应。这些响应占用了太多的上下文空间，导致无法继续执行 PPT 生成。

### 尝试的方案

#### 方案 1: 单脚本自动化 ⚠️
**脚本**: `/root/clawd/scripts/ai-content-creator-workflow.sh`
**问题**: 大纲生成时遇到问题，无法提取 query_id 和 chat_id

#### 方案 2: 两阶段脚本 ⚠️
**脚本**: 
- `/root/clawd/scripts/ai-content-creator-stage1.sh` - 阶段 1：生成大纲
- `/root/clawd/scripts/ai-content-creator-stage2.sh` - 阶段 2：生成 PPT

**问题**: ID 提取逻辑需要改进

#### 方案 3: 改进两阶段脚本 ⚠️
**脚本**: `/root/clawd/scripts/ai-content-creator-stage1-v2.sh`
**结果**: ✅ 成功提取到 query_id, chat_id, title
**问题**: 阶段 2 脚本参数传递有问题

#### 方案 4: 最终版两阶段脚本 ⚠️
**脚本**: `/root/clawd/scripts/ai-content-creator-final.sh`
**问题**: 进程在生成大纲时中断或挂起

### 根本原因分析

1. **SSE 流式输出占用大量上下文**
   - 大纲生成 API 返回多个 JSON 对象
   - 每个 JSON 对象都包含完整的字段
   - 累积起来占用了太多 token

2. **Python 脚本参数解析**
   - PPT 生成脚本需要 `--outline` 参数
   - 但大纲 API 返回的 outline 字段在大部分响应中是空的
   - 需要合并多个响应中的 outline 内容

3. **超时和进程管理**
   - 大纲生成可能需要超过 60 秒
   - 脚本被超时终止

### 可行的解决方案

#### 建议 1: 手动两步流程 ✅ 推荐

```bash
# 步骤 1: 生成大纲（手动运行）
cd /root/clawd/skills/ai-ppt-generate/scripts
export BAIDU_API_KEY="bce-v3/ALTAK-9XbrsPkGC9yjb37vqXuLw/2b288953011ddde592aad58cae8637f47da00189"
python3 ppt_outline_generate.py --query "主题"

# 步骤 2: 手动复制 ID 和 outline，生成 PPT
python3 ppt_generate.py \
  --query_id <query_id> \
  --chat_id <chat_id> \
  --outline "<outline>" \
  --query "主题" \
  --title "标题"
```

#### 建议 2: 使用已生成的 PPT ✅

**之前的 PPT**:
- 主题: AI技术发展趋势2026
- 页数: 27 页
- 下载链接: http://image0.bj.bcebos.com/248bff47-0610-11f1-a161-1af93dbf0178.pptx

#### 建议 3: 简化自动化流程 ⏳

创建一个超简单的脚本：
- 只使用百度搜索结果（不调用大纲生成 API）
- 手动构建 outline（基于搜索结果）
- 直接调用 PPT 生成

### 自动化工作流脚本位置

```
/root/clawd/scripts/
├── ai-content-creator-workflow.sh
├── ai-content-creator-workflow-v2.sh
├── ai-content-creator-workflow-v3.sh
├── ai-content-creator-workflow-v4.sh
├── ai-content-creator-workflow-v5.sh
├── ai-content-creator-stage1.sh
├── ai-content-creator-stage1-v2.sh
├── ai-content-creator-stage2.sh
├── ai-content-creator-stage2-v2.sh
└── ai-content-creator-final.sh
```

### 结论

**问题**: 自动化工作流遇到上下文溢出
**原因**: SSE 流式输出占用太多上下文
**状态**: ⚠️ 需要时间进一步优化脚本
**当前推荐方案**: 使用手动两步流程或已有的 PPT

---

## 更新记录

- 2026-02-09 22:00: 创建文档，记录 AI 搜索探索结果
- 2026-02-09 22:02: 修复百度搜索脚本，创建包装脚本
- 2026-02-09 22:02: 测试百度搜索脚本，成功找到 20 篇文章
- 2026-02-09 22:02: 记录百度搜索结果和主要趋势
- 2026-02-10 07:23: 完成 PPT 生成探索（27 页，商务风格）
- 2026-02-10 08:23: 完成绘本生成探索（静态 + 动态）
- 2026-02-10 08:30: 更新最佳实践文档，添加 PPT 和绘本生成内容
- 2026-02-10 08:44: 解决绘本下载问题（协议错误：https:// → http://）
- 2026-02-10 08:45: 成功下载两个绘本视频（静态 2.7 MB，动态 4.6 MB）

---

## 附录

### 百度学术检索 API

**文档**: /root/clawd/skills/baidu-scholar-search-skill/SKILL.md

### 百度搜索 API

**文档**: /root/clawd/skills/baidu-search/SKILL.md

### 百度搜索包装脚本

**位置**: `/root/clawd/scripts/baidu-search-wrapper.sh`

**功能**:
- 简化百度搜索 API 调用
- 自动构造 JSON 参数
- 彩色输出
- 错误处理

**用法**:
```bash
bash /root/clawd/scripts/baidu-search-wrapper.sh "搜索主题"
```

**示例**:
```bash
# 搜索 AI 技术发展趋势
bash /root/clawd/scripts/baidu-search-wrapper.sh "AI技术发展趋势2026"
```

### SearXNG

**本地地址**: http://localhost:8080
**容器名称**: searxng
