# topics-sync Skill

情报官选题池自动同步工具 - 处理 Git 协作的 pull → write → push 全流程，支持冲突自动解决。

## 功能

1. **同步最新代码** - 从 GitHub pull 最新选题池
2. **写入云端选题** - 生成 `topics-pool-cloud-YYYYMMDD-HHMM.md` 文件
3. **自动提交推送** - commit 并 push 到 GitHub
4. **冲突处理** - 自动解决合并冲突（优先保留本地新内容）
5. **可选读取** - 支持读取选题池供后续使用

## 使用方式

```
@intel-officer 同步选题到云端
@intel-officer 读取今日选题
@intel-officer 同步选题并读取
```

## 路径配置

- **仓库路径**: `/root/clawd/workspace-shared/topics`
- **输出文件**: `topics-pool-cloud-YYYYMMDD-HHMM.md`
- **GitHub**: `https://github.com/hhhh124hhhh/openclaw-topics-sync`

## 冲突解决策略

采用 **ours** 合并策略：
- 远程有更新且本地无改动 → 自动合并
- 远程有更新且本地有改动 → 保留本地版本（云端优先）
- 完全冲突时 → 以日期最新的为准

## 依赖

- git
- 有效的 GitHub token（已配置在 git credential cache 中）
