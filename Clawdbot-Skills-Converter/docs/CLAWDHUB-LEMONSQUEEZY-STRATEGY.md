# ClawdHub + Gumroad/Lemon Squeezy 双渠道架构策划

## 📊 项目概述

**目标**：将 AI 提示词自动化转换为 Clawdbot Skills，通过双渠道销售变现

**核心价值**：
- 不卖原始提示词，而是卖**自动化转换后的完整技能包**
- 面向不同用户群体的分层策略

---

## 🎯 双渠道定位

### 1️⃣ ClawdHub - 核心渠道（B2B/技术用户）

**目标用户**：
- Clawdbot 现有用户
- 开发者和自动化爱好者
- 企业用户

**产品形态**：
- 纯 Skill 文件（`.skill` 包）
- 可直接通过 `clawdhub` CLI 安装
- 即插即用

**优势**：
- ✅ 完全自动化发布（无需人工干预）
- ✅ 用户无缝集成到现有工作流
- ✅ 生态内流量天然导入
- ✅ 版本管理和更新便捷

**定价策略**：
- 基础技能：$0.99 - $4.99
- 高级技能：$4.99 - $9.99
- 订阅制：$19.99/月（全库访问）

### 2️⃣ Gumroad/Lemon Squeezy - 扩展渠道（B2C/非技术用户）

**目标用户**：
- 不懂技术的 AI 提示词爱好者
- 内容创作者
- 小企业主
- 希望快速上手的普通用户

**产品形态**：
- **完整包**：Skill + 详细文档 + 视频教程 + 示例
- **新手友好**：从零开始的安装指南
- **增值内容**：使用场景、最佳实践、FAQ

**打包内容示例**：
```
📦 AI 写作助手技能包
├── 📄 ai-writer-assistant.skill (Clawdbot 技能文件)
├── 📖 README.md (使用文档)
├── 🎬 10分钟快速入门.mp4
├── 📋 使用场景清单.md
├── ❓ FAQ.md
└── 🎁 bonus-templates.md (额外模板)
```

**优势**：
- ✅ 接触更广泛受众（非技术用户）
- ✅ 支持更多支付方式
- ✅ 自动化产品交付
- ✅ 灵活的折扣和促销机制
- ✅ 邮件营销集成

**定价策略**：
- 基础包：$9.99 - $14.99（含文档）
- 高级包：$19.99 - $29.99（含视频教程）
- 终极包：$49.99 - $99.99（全套 + 1对1 咨询）

---

## 🔄 自动化流程设计

### 阶段 1：内容获取（自动化）

```
Twitter/X → twitter-search-skill → 提取热门 AI 提示词
     ↓
质量评估 → 5维度评分系统
     ↓
筛选过滤 → 分数 > 80 分的提示词
```

### 阶段 2：Skill 转换（半自动化）

```
提示词 → prompt-optimizer 优化
     ↓
skill-creator 生成 Skill 框架
     ↓
人工审查和调整（关键质量控制点）
     ↓
生成最终 .skill 包
```

### 阶段 3：双渠道发布（完全自动化）

#### ClawdHub 自动化
```bash
# 脚本示例
clawdhub publish \
  --skill ai-writer-assistant \
  --version 1.0.0 \
  --price "$4.99" \
  --category "writing" \
  --description "$(cat descriptions/ai-writer-assistant.md)"
```

#### Gumroad/Lemon Squeezy 自动化
```javascript
// 使用 API 自动创建产品
const product = await gumroad.products.create({
  name: "AI 写作助手技能包",
  price: 14.99,
  files: [
    "ai-writer-assistant.skill",
    "README.md",
    "tutorial.mp4"
  ],
  description: "一键安装，10分钟上手..."
});
```

---

## 💡 差异化策略

| 维度 | PromptBase | 我们 |
|------|------------|------|
| 产品形式 | 原始提示词 | 完整自动化技能 |
| 目标用户 | 提示词工程师 | Clawdbot 用户 |
| 集成度 | 需手动复制粘贴 | 一键安装 |
| 文档 | 简短说明 | 完整教程 + 视频 |
| 更新 | 手动推送 | 自动更新 |
| 支持 | 无 | 邮件 + 社区 |

---

## 📈 收入预测

### 保守场景（第1年）

**ClawdHub**：
- 月售 30 个技能 × $4.99 = $149.70
- 年收入：$1,796

**Gumroad**：
- 月售 15 个打包产品 × $14.99 = $224.85
- 年收入：$2,698

**总计**：$4,494/年

### 乐观场景（第1年）

**ClawdHub**：
- 月售 60 个技能 × $4.99 = $299.40
- 订阅收入：20 用户 × $19.99 = $399.80
- 月收入：$699.20
- 年收入：$8,390

**Gumroad**：
- 月售 40 个打包产品 × $19.99 = $799.60
- 年收入：$9,595

**总计**：$17,985/年

---

## ⚙️ 技术实现

### ClawdHub 集成

**使用 clawdhub CLI 自动化发布**：

```bash
# 安装 clawdhub CLI
npm install -g @clawdhub/cli

# 登录
clawdhub login

# 发布技能
clawdhub publish \
  --path ./skills/ai-writer-assistant \
  --name "AI 写作助手" \
  --price "4.99" \
  --category "writing" \
  --tags "ai,writing,automation" \
  --auto-approve
```

### Gumroad API 集成

**API Key 配置**：
```bash
# 环境变量
export GUMROAD_ACCESS_TOKEN="your_api_key"
export GUMROAD_PRODUCT_ID="your_product_id"
```

**Node.js 脚本示例**：
```javascript
const Gumroad = require('gumroad-api');

const client = new Gumroad(process.env.GUMROAD_ACCESS_TOKEN);

async function createProduct(skillData) {
  const product = await client.products.create({
    name: skillData.name + " 完整版",
    price: skillData.price * 3, // 打包版价格是 Skill 版的 3 倍
    description: generateDescription(skillData),
    tags: skillData.tags,
    file_url: skillData.packageUrl
  });

  return product;
}
```

### Lemon Squeezy API 集成

**配置**：
```bash
export LEMON_SQUEEZY_API_KEY="your_api_key"
export LEMON_SQUEEZY_STORE_ID="your_store_id"
```

**Webhook 处理自动交付**：
```javascript
// 当用户购买时自动发送 Skill 包
app.post('/webhook/lemonsqueezy', async (req, res) => {
  const { event, data } = req.body;

  if (event === 'order_created') {
    const userEmail = data.attributes.first_order_item.customer_email;
    const productId = data.attributes.first_order_item.product_id;

    // 发送邮件（带 Skill 包下载链接）
    await sendDeliveryEmail(userEmail, productId);
  }

  res.status(200).send('OK');
});
```

---

## 🗓️ 实施时间线

### 第 1-2 周：基础设施
- [x] 安装核心技能（已完成）
- [ ] 配置 ClawdHub CLI
- [ ] 注册 Gumroad/Lemon Squeezy 账户
- [ ] 获取 API Keys

### 第 3-4 周：自动化脚本
- [ ] 开发 Twitter 抓取脚本
- [ ] 开发 Skill 自动转换脚本
- [ ] 开发 ClawdHub 自动发布脚本
- [ ] 开发 Gumroad/Lemon Squeezy 自动发布脚本

### 第 5-6 周：产品准备
- [ ] 手动转换 10 个高质量提示词
- [ ] 创建文档模板
- [ ] 录制新手教程视频

### 第 7-8 周：测试和上线
- [ ] 内测发布 5 个 Skill
- [ ] 收集反馈并优化
- [ ] 正式上线到双渠道

---

## 🚀 立即行动

### 本周任务
1. **调研 Gumroad/Lemon Squeezy API**
   - 比较两者的费用、功能、支付方式
   - 选择更适合的平台

2. **配置开发环境**
   - 获取 Gumroad/Lemon Squeezy API Key
   - 配置 ClawdHub CLI

3. **测试手动流程**
   - 手动转换 1 个提示词为 Skill
   - 手动发布到 ClawdHub 测试

4. **编写第一个打包产品**
   - 选择最热门的 AI 提示词
   - 创建完整文档 + 教程

---

## 📌 关键决策点

### Q1：Gumroad 还是 Lemon Squeezy？

**Gumroad**：
- ✅ 市场成熟，用户基数大
- ✅ 支持订阅和付费解锁
- ✅ 费用：10% + 30¢/交易
- ❌ 佣金略高

**Lemon Squeezy**：
- ✅ 费用更低：5% + 50¢/交易
- ✅ 更好的开发者体验
- ✅ 内置税单处理
- ❌ 市场较小

**推荐**：**先上 Gumroad**（流量优势），后期扩展到 Lemon Squeezy（降低成本）

### Q2：定价策略如何优化？

**分层定价**：
- ClawdHub 纯 Skill：技术用户，价格敏感 → 低价策略（$0.99 - $9.99）
- Gumroad 完整包：非技术用户，重视体验 → 高价策略（$9.99 - $49.99）

**动态定价**：
- 新品首发折扣（7 天 8 折）
- 捆绑销售优惠（3 个 Skill 9 折）
- 订阅用户专属折扣

### Q3：自动化程度如何控制？

**风险控制**：
- 质量评分 < 80 分 → 不发布
- 所有发布前必须人工审查
- 建立"黑名单"机制（过滤低质内容）

**人机协作**：
- ✅ 抓取、评分、转换：自动化
- ⚠️ 审查、分类、定价：半自动化
- ❌ 文档、教程、营销：人工

---

## 📚 参考资源

### ClawdHub 相关
- ClawdHub CLI 文档：https://docs.clawdhub.com
- Skill 发布指南：https://docs.clawdhub.com/publishing

### Gumroad API
- API 文档：https://gumroad.com/api
- Webhook 配置：https://gumroad.com/api/webhooks
- 产品创建端点：POST /products

### Lemon Squeezy API
- API 文档：https://docs.lemonsqueezy.com/api
- 产品管理：https://docs.lemonsqueezy.com/api/products

---

## 🎯 成功指标

**第 1 季度目标**：
- 发布 20 个 Skills
- ClawdHub 销售额：$500+
- Gumroad 销售额：$300+

**第 2 季度目标**：
- 发布 50 个 Skills
- ClawdHub 销售额：$2,000+
- Gumroad 销售额：$1,500+
- 订阅用户：10+

**年度目标**：
- 发布 100+ Skills
- 总收入：$10,000+
- 订阅用户：50+

---

*最后更新：2026-01-29*
