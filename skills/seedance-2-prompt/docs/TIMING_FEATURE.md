# 时间分段提示词生成功能

## 功能概述

Seedance 2.0 提示词生成器现在支持按照时间分段标准生成15秒提示词。

## 时间分段结构

### 0-3秒：引入场景
- 描述环境和初始状态
- 展示主角和背景

### 3-7秒：主要动作
- 展示核心动作和互动
- 环境对动作的反应

### 7-12秒：情感升级
- 情感从基础升级到强烈
- 人物表情和眼神变化

### 12-15秒：情感收尾
- 情感舒缓或达到高潮
- 最终的感悟或满足

## 新增方法

### `generate_prompt_with_timing()`

按照时间分段标准生成15秒提示词。

**参数：**
- `scene`: 场景描述
- `style`: 风格（默认："写实"）
- `duration`: 时长（默认："15s"）
- `difficulty`: 难度级别（默认："ADVANCED"）
- `video_type`: 视频类型（默认："photo-realistic"）

**返回值：**
```python
{
    "prompt": "完整提示词",
    "segments": {
        "intro_0-3s": "引入场景描述",
        "main_action_3-7s": "主要动作描述",
        "emotion_rise_7-12s": "情感升级描述",
        "conclusion_12-15s": "情感收尾描述"
    },
    "duration": "15s",
    "difficulty": "ADVANCED",
    "video_type": "photo-realistic",
    "word_count": 提示词字数
}
```

## 新增常量

### 情感变化关键词

`EMOTION_KEYWORDS` 字典定义了不同情感类型的基础、升级、高潮和舒缓状态：

- `happy`: 微笑 → 开怀大笑 → 充满喜悦 → 满足的微笑
- `sad`: 忧郁 → 眼中含泪 → 悲伤涌上心头 → 平静接受
- `surprise`: 好奇 → 惊讶 → 难以置信 → 逐渐理解
- `romantic`: 温柔注视 → 眼神炙热 → 充满爱意 → 满足的微笑
- `mysterious`: 神秘表情 → 目光深邃 → 充满谜团 → 若有所思
- `action`: 专注表情 → 全力以赴 → 激烈对抗 → 胜利满足

### 环境互动关键词

`ENVIRONMENT_INTERACTION` 字典定义了不同环境的互动描述：

- `rain`: 雨水从天空滴落，在地面上溅起水花
- `sunshine`: 温暖的阳光透过窗户洒下斑驳的光影
- `wind`: 微风轻拂，树叶沙沙作响
- `night`: 霓虹灯在湿润的地面反射出绚丽的光芒
- `snow`: 雪花飘落，覆盖一切，世界变得洁白纯净
- `fire`: 火焰跳跃，照亮周围，热浪涌动
- `ocean`: 海浪拍打岸边，溅起白色泡沫
- `forest`: 翠绿的竹林在微风中摇曳，竹叶沙沙作响，空气中弥漫着清新的草木香
- `garden`: 花草摇曳，蝴蝶飞舞，鸟鸣声在林间回荡，空气中弥漫着花香
- `cafe`: 咖啡香气弥漫，温暖的光线透过大玻璃窗洒进来，周围是温馨的装饰和精致的桌椅
- `cyberpunk`: 霓虹闪烁，电子广告牌显示着流动的信息
- `urban`: 城市喧嚣，车流穿梭，建筑耸立

### 风格关键词库

`STYLE_KEYWORDS` 字典定义了不同风格的关键词：

- `科幻`: 未来科技, 机械, 金属, 电子, 全息, 人工智能
- `写实`: 真实, 细节丰富, 自然光线, 逼真, 质感
- `童话`: 梦幻, 魔法, 色彩鲜艳, 可爱, 奇幻
- `武侠`: 古装, 飘逸, 水墨风格, 侠客, 气场
- `浪漫`: 柔和光线, 温馨, 精致, 优雅, 诗意

## 新增辅助方法

### `_detect_environment(scene)`

检测场景中的环境类型。

**支持的环境类型：**
- `cafe`: 咖啡馆
- `garden`: 花园
- `forest`: 竹林/森林
- `rain`: 雨天
- `cyberpunk`: 赛博朋克
- `sunshine`: 阳光
- `night`: 夜晚
- `snow`: 雪天
- `fire`: 火焰
- `ocean`: 海洋
- `wind`: 风天
- `urban`: 城市

### `_detect_emotion(scene)`

检测场景中的情感类型。

**支持的情感类型：**
- `action`: 武术/动作
- `happy`: 快乐/童话
- `romantic`: 浪漫/咖啡馆
- `mysterious`: 神秘
- `surprise`: 惊讶
- `sad`: 悲伤

### `_generate_intro(scene, style)`

生成0-3秒的引入场景描述。

### `_generate_main_action(scene, style)`

生成3-7秒的主要动作描述。

### `_generate_emotion_rise(scene, style)`

生成7-12秒的情感升级描述。

### `_generate_conclusion(scene, style)`

生成12-15秒的情感收尾描述。

## 使用示例

```python
from prompt_generator import PromptGenerator

generator = PromptGenerator()

# 生成时间分段提示词
result = generator.generate_prompt_with_timing(
    scene="赛博朋克雨夜，霓虹灯闪烁，未来城市",
    style="科幻",
    duration="15s",
    difficulty="ADVANCED",
    video_type="photo-realistic"
)

# 查看结果
print("完整提示词：", result["prompt"])
print("\n时间分段：")
for segment_name, segment_content in result["segments"].items():
    print(f"{segment_name}: {segment_content}")

print(f"\n字数：{result['word_count']}")
```

## 测试

运行测试脚本验证功能：

```bash
python3 /root/clawd/skills/seedance-2-prompt/scripts/test_timing_prompts.py
```

测试用例包括：
1. 赛博朋克雨夜（科幻风格）
2. 童话花园（童话风格）
3. 武术竹林（武侠风格）
4. 巴黎咖啡馆（浪漫风格）

## 验证要求

每个生成的提示词都需要满足：
- ✅ 提示词长度 > 100 字
- ✅ 包含4个时间分段
- ✅ 每个分段有明确的情感变化
- ✅ 包含环境互动描述

## 输出示例

### 赛博朋克雨夜

```
镜头缓慢展开，雨水从天空滴落，在地面上溅起水花。未来科技风格的环境中，主角出现在画面中央，周围景色清晰可见。光线柔和，氛围未来科技。

主角在雨中缓缓行走，雨水打在身上，水珠沿着发丝滑落。身体微微前倾，踏水而行，每一步都激起小小的水花。

表情从温柔注视逐渐转为眼神炙热。眼神变得深邃有力，嘴角微微上扬。情感在胸中涌动，达到充满爱意的状态，全身散发出强烈的情感气场。

最终，情感渐渐满足的微笑。主角脸上露出满足的表情，内心获得了平静与感悟。镜头缓缓后退，留下一个美好的画面，整个故事在这一刻达到了完美的收尾。

字数：252
```

## 注意事项

1. 环境检测优先级：更具体的关键词优先匹配
2. 情感检测优先级：动作类型 > 快乐 > 浪漫 > 其他
3. 默认环境：城市
4. 默认情感：浪漫
