# Seedance 15秒视频展示和数字分身圆梦 Skill

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/hhhh124hhhh/seedance-2-prompt)

## 简介

Seedance 15秒视频展示和数字分身圆梦 Skill 是一个强大的 AI 视频提示词生成工具，专门为字节跳动 Seedance 2.0 视频模型设计，专注于两大核心功能：15秒视频展示和数字分身圆梦。

## 功能特性

### 核心功能

#### 🎬 15秒视频展示
- ✅ **高质量提示词生成** - 参考优秀作品（如《假面骑士BLACK SUN》、《仙侠小说经典场景》）
- ✅ **风格定位极其精准** - 参考作品、风格关键词
- ✅ **细节极其丰富** - 每个元素都有明确要求
- ✅ **镜头语言极其专业** - 全程不切镜头，或精确的分秒镜头变化
- ✅ **氛围营造极佳** - 场景、天气、声音
- ✅ **动作设计简洁有力**
- ✅ **特效设计增强震撼感**
- ✅ **分秒设计** - 15秒标准分秒设计，每个时段都有明确的镜头、动作、场景、光影
- ✅ **悬念设计** - 支持悬念结尾设计，增强吸引力

#### 🎭 数字分身圆梦
- ✅ **数字分身场景设计** - 结合用户上传的数字分身，设计圆梦场景
- ✅ **使用上传照片作为人物面部参考** - 保持脸部完全一致，不改变五官和脸型，不美化
- ✅ **服装符合视频要求**
- ✅ **专注于动作场景设计** - 分秒设计
- ✅ **圆梦场景** - 仙法万剑归宗、机械变身、历史事件演绎、极限运动、动画变身、其他梦想场景

### 辅助功能
- ✅ **交互式提示词生成** - 通过交互式对话引导用户生成完整的视频提示词
- ✅ **提示词优化** - 优化用户输入的提示词，根据万能公式补充缺失元素
- ✅ **模板库管理** - 存储和管理 24 个预设模板，按类型和难度分类
- ✅ **高质量示例展示** - 展示高质量提示词示例，包含结构分析
- ✅ **提示词变体生成** - 为同一场景生成多个优化版本
- ✅ **在线搜索** - 搜索最新的 Seedance 2.0 提示词，获取灵感和参考
- ✅ **模板更新** - 从网络获取最新模板，更新本地模板库

## 适用场景

### 最适合（⭐⭐⭐⭐⭐）
- **15秒视频展示**：
  - 仙法万剑归宗（仙侠玄幻）
  - 机械变身（科技感）
  - 历史事件（马嵬坡兵变、玄武门之变、赤壁之战等）
  - 极限运动（冲浪、跳伞、水上漂）
  - 动画变身（元素变身、英雄变身）
  - 其他15秒视频场景

- **数字分身圆梦**：
  - 仙法万剑归宗（仙侠玄幻）
  - 机械变身（科技感）
  - 历史事件演绎（参与历史）
  - 极限运动（冲浪、跳伞、水上漂）
  - 动画变身（元素变身、英雄变身）
  - 其他梦想场景

### 工作流程
1. 用户上传数字分身图片（人物图片）
2. 专注设计动作场景（分秒设计）
3. 用户使用数字分身 + 我的动作设计 = 完整视频
4. 简化工作流程，提高效率

## 安装

### 使用 ClawdHub 安装（推荐）

```bash
clawdhub install hhhh124hhhh/seedance-2-prompt
```

### 手动安装

1. 克隆仓库：
```bash
git clone https://github.com/hhhh124hhhh/seedance-2-prompt.git
cd seedance-2-prompt
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 快速开始

### 高质量提示词生成（15秒视频展示）

```python
from scripts.prompt_generator import PromptGenerator

# 创建生成器
generator = PromptGenerator()

# 生成高质量提示词（仙法万剑归宗）
result = generator.generate_high_quality_prompt(
    scene='仙法万剑归宗',
    reference_work='仙侠小说经典场景',
    style_keywords=['仙侠玄幻', '仙气弥漫', '震撼壮观', '仙术特效'],
    outfit_before='白色道袍，飘逸长发，手持古剑，仙风道骨',
    belt_design='古朴素雅，灵气流转，仙家气息',
    final_costume='仙法护体，剑气环绕，仙气弥漫，仙法战衣',
    scene_setting='山顶云雾缭绕，仙气弥漫，苍松翠柏，云海翻腾',
    camera_movement='全景到特写，环绕镜头，展现万剑归宗的震撼效果',
    action_sequence='聚气→施法→万剑归宗→剑气爆发→收功',
    transformation_type='仙气聚集→剑气成形→万剑归宗→剑气爆发',
    effects='仙气缭绕，剑气纵横，光芒四射，仙法特效震撼',
    ending='山顶云雾，剑气消散，收功凝神，仙气依旧',
    duration='15s',
    include_timing=True
)

# 显示结果
generator.display_high_quality_result(result)
```

### 基本使用（辅助功能）

```python
from scripts.prompt_generator import PromptGenerator

# 创建生成器
generator = PromptGenerator()

# 生成提示词
result = generator.generate_prompt(
    scene='一只可爱的小猫在花园里玩耍',
    style='动漫风格',
    duration='10s',
    difficulty='INTERMEDIATE'
)

print(result['prompt'])
```

### 逐秒分镜格式（辅助功能）

```python
result = generator.generate_prompt_with_timing(
    scene='一位年轻女孩走在科幻雨夜中',
    style='科幻',
    duration='15s',
    difficulty='ADVANCED'
)
```

## 文档

- [SKILL.md](SKILL.md) - 技能文档
- [DELIVERY-REPORT.md](DELIVERY-REPORT.md) - 交付报告
- [QUICK-REF.md](QUICK-REF.md) - 快速参考
- [CHANGES_TIMING.md](CHANGES_TIMING.md) - 时间分段更新日志
- [COMBAT_OPTIMIZATION.md](COMBAT_OPTIMIZATION.md) - 战斗优化文档
- [SMART_EXPANSION.md](SMART_EXPANSION.md) - 智能扩展功能
- [SMART_EXPANSION_REPORT.md](SMART_EXPANSION_REPORT.md) - 智能扩展报告

## 脚本

- `scripts/prompt_generator.py` - 提示词生成器
- `scripts/prompt_optimizer.py` - 提示词优化器
- `scripts/template_library.py` - 模板库
- `scripts/examples.py` - 示例展示
- `scripts/search_online.py` - 在线搜索
- `scripts/smart_expansion.py` - 智能扩展
- `scripts/test_*.py` - 测试套件

## 测试

运行所有测试：

```bash
cd scripts
python test_comprehensive.py
```

运行特定测试：

```bash
cd scripts
python test_timing_prompts.py      # 时间分段测试
python test_mild_mode.py            # 轻微模式测试
python test_online_features.py       # 在线功能测试
python test_smart_expansion.py       # 智能扩展测试
```

## 版本历史

### v2.0.0 (2026-02-19)

重大升级 - 15秒视频展示和数字分身圆梦：

- ✅ **改名**：seedance-2-prompt → seedance-15s-avatar
- ✅ **15秒视频展示**：
  - 高质量提示词生成（参考优秀作品）
  - 分秒设计（15秒标准）
  - 悬念设计（增强吸引力）
  - 场景类型（仙法万剑归宗、机械变身、历史事件、极限运动等）
- ✅ **数字分身圆梦**：
  - 数字分身场景设计
  - 圆梦场景（仙法万剑归宗、机械变身、历史事件演绎、极限运动、动画变身、其他梦想场景）
  - 工作流程：数字分身 + 动作设计 = 完整视频
- ✅ **高质量提示词生成功能**：
  - 新增 `generate_high_quality_prompt` 方法
  - 新增 `_generate_high_quality_timing_prompts` 方法
  - 新增 `display_high_quality_result` 方法
- ✅ **辅助功能**（保留）：
  - 交互式提示词生成
  - 提示词优化
  - 模板库管理
  - 高质量示例展示
  - 提示词变体生成
  - 在线搜索
  - 模板更新
- ✅ 添加 .gitignore

### v1.0.0 (2026-02-16)

初始版本发布：
- ✅ 支持 22 种玩法
- ✅ 17 个模板库
- ✅ 逐秒分镜格式
- ✅ 九宫格图片模式
- ✅ 音频元素支持
- ✅ 智能情感和环境检测
- ✅ 轻微模式（mild_mode）
- ✅ 参考风格和场景模板生成
- ✅ 完整的测试套件

## 许可证

MIT License

## 作者

Clawdbot AI Assistant

## 贡献

欢迎提交 Issue 和 Pull Request！

## 支持

如果你觉得这个技能有用，请给它一个 Star！⭐
