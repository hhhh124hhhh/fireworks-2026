# NewsNow API 集成报告

**完成时间**: 2026-03-23 12:26
**API 来源**: https://newsnow.busiyi.world/
**状态**: ⚠️ API 格式已变更，需要调整

---

## 已完成工作

### 1. 创建 newsnow_fetcher.py 模块 ✅

**文件**: `D:\openclaw-data\.openclaw\workspace-intel-officer\skills\opencli-hotspot-grabber\newsnow_fetcher.py`

**功能**:
- 支持 10 个平台抓取（知乎、微博、B 站、抖音、今日头条、百度、澎湃新闻、财联社、华尔街见闻、贴吧）
- 标准化输出格式
- 自动重试机制（3 次）
- 健康检查接口

**代码量**: 260 行

---

### 2. 集成到主脚本 ✅

**修改**: `hotspot_grabber.py`

**增强**:
- 引入 newsnow_fetcher 模块
- 混合抓取策略（NewsNow → opencli → Chrome fallback）
- 版本升级为 v2.0
- 自动检测 NewsNow API 可用性

**抓取流程**:
```
用户请求
  ↓
NewsNow API 可用？
  ├─ 是 → 优先使用 NewsNow（快速）
  └─ 否 → 降级到 opencli
           ↓
        opencli 失败？
          ├─ 是 → 降级到 Chrome CDP
          └─ 否 → 完成
```

---

## API 问题分析

### 当前状态

| 检查项 | 状态 | 说明 |
|--------|------|------|
| **API 可达性** | ✅ 可用 | 健康检查通过 |
| **返回格式** | ❌ HTML | 期望 JSON，实际返回 HTML |
| **平台支持** | ⚠️ 待确认 | 需要确认最新 API 格式 |

### 问题详情

**预期 API 格式**:
```
GET https://newsnow.busiyi.world/api/hotlist?platform=zhihu
Response: {"code": 0, "msg": "success", "data": [...]}
```

**实际返回**:
```html
<!doctype html>
<html lang="zh-CN" class="dark">
<head>
  <meta charset="UTF-8" />
  ...
```

**可能原因**:
1. API 格式已变更（从 query parameter 改为 path parameter）
2. 需要认证（API Key）
3. 需要特定的请求头
4. API 服务已停止

---

## 解决方案

### 方案 A：修复 NewsNow API 调用（推荐）

**步骤**:
1. 访问 https://newsnow.busiyi.world/ 查看最新 API 文档
2. 测试正确的 API 格式
3. 更新 newsnow_fetcher.py

**预期时间**: 30 分钟

---

### 方案 B：直接使用 hotspot-monitor-skill 的抓取逻辑

**步骤**:
1. 从 GitHub 下载 hotspot-monitor-skill 项目
2. 提取其 fetcher.py 模块
3. 集成到 bot4

**预期时间**: 1 小时

**优点**: 已验证可用
**缺点**: 需要解决 GitHub 连接问题

---

### 方案 C：保持现有 opencli 方案

**当前 bot4 方案**:
```
opencli → Chrome CDP → requests 网页抓取
```

**优点**:
- ✅ 已验证可用
- ✅ 有登录态优势
- ✅ 不依赖第三方 API

**缺点**:
- ❌ 速度较慢
- ❌ 需要浏览器
- ❌ 平台覆盖有限（8 个）

---

## 平台对比

| 平台 | NewsNow API | opencli | 推荐方案 |
|------|-----------|---------|---------|
| 知乎 | ⚠️ 待修复 | ✅ 可用 | opencli |
| 微博 | ⚠️ 待修复 | ✅ 可用 | opencli |
| B 站 | ⚠️ 待修复 | ✅ 可用 | opencli |
| 抖音 | ⚠️ 待修复 | ❌ 不支持 | NewsNow（修复后） |
| 今日头条 | ⚠️ 待修复 | ❌ 不支持 | NewsNow（修复后） |
| 百度 | ⚠️ 待修复 | ✅ 自有逻辑 | opencli |
| 澎湃新闻 | ⚠️ 待修复 | ❌ 不支持 | NewsNow（修复后） |
| 财联社 | ⚠️ 待修复 | ❌ 不支持 | NewsNow（修复后） |
| 华尔街见闻 | ⚠️ 待修复 | ❌ 不支持 | NewsNow（修复后） |
| 贴吧 | ⚠️ 待修复 | ❌ 不支持 | NewsNow（修复后） |

---

## 建议行动

### 立即行动（P0）

1. ✅ **保持现有 opencli 方案**
   - bot4 热点采集照常运行
   - 不受 NewsNow API 影响

2. ⏸️ **验证 API 最新格式**
   - 访问 https://newsnow.busiyi.world/
   - 查看 API 文档或示例
   - 测试正确的调用方式

---

### 短期行动（P1，本周）

1. ⏸️ **修复 NewsNow API 模块**
   - 根据最新 API 格式调整
   - 重新测试

2. ⏸️ **混合抓取测试**
   - NewsNow API（优先）
   - opencli（兜底）

---

### 中期行动（P2，下周）

1. ⏸️ **引入 hotspot-monitor-skill 的抓取逻辑**
   - 如果 NewsNow API 不可用
   - 使用其自研的抓取模块

2. ⏸️ **关键词筛选功能**
   - 从 hotspot-monitor-skill 借鉴
   - 普通词 + 必须词 + 排除词

---

## 代码保留价值

虽然 NewsNow API 暂时不可用，但 **newsnow_fetcher.py 模块仍有保留价值**:

1. **架构设计**: 模块化、可重试、健康检查
2. **平台映射**: 10 个平台的 ID 映射
3. **标准化输出**: 统一的数据格式
4. **混合抓取框架**: 已集成到主脚本

**建议**: 保留模块，等待 API 修复后重新启用。

---

## 总结

| 项目 | 状态 |
|------|------|
| **newsnow_fetcher.py** | ✅ 已完成 |
| **主脚本集成** | ✅ 已完成 |
| **NewsNow API 调用** | ❌ 格式待确认 |
| **bot4 现有功能** | ✅ 不受影响 |
| **下一步** | 验证 API 最新格式 |

---

**创建者**: bot3 (zhuazhua-agent)
**时间**: 2026-03-23 12:26
