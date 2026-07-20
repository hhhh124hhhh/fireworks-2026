#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seedance 2.0 提示词生成器
根据用户输入生成符合万能公式的完整提示词
支持联网搜索功能
"""

import sys
import random
import logging
from pathlib import Path
from typing import Dict, List, Optional
from template_library import TemplateLibrary

# 导入在线搜索模块
try:
    # 添加脚本路径
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))

    from search_online import search_prompts as search_online_prompts
    ONLINE_SEARCH_AVAILABLE = True
except ImportError:
    ONLINE_SEARCH_AVAILABLE = False
    logging.warning("在线搜索模块不可用")

# 导入智能扩展模块
try:
    from smart_expansion import (
        SceneTemplateLibrary,
        auto_expand_template,
        detect_emotion,
        detect_environment
    )
    SMART_EXPANSION_AVAILABLE = True
except ImportError:
    SMART_EXPANSION_AVAILABLE = False
    logging.warning("智能扩展模块不可用")

# 配置日志
LOG_DIR = Path("/root/clawd/skills/seedance-2-prompt/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'prompt_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class PromptGenerator:
    """提示词生成器"""

    # 万能公式的 8 个元素
    FORMULA_ELEMENTS = [
        "subject",      # 主体
        "action",       # 动作
        "scene",        # 场景
        "lighting",     # 光影
        "camera",       # 镜头语言
        "style",        # 风格
        "quality",      # 画质
        "constraints"   # 约束
    ]

    # 情感变化关键词
    EMOTION_KEYWORDS = {
        "combat": {
            "base": "冷静对峙",
            "rising": "眼神犀利",
            "peak": "激烈对战",
            "soothing": "胜负已分"
        },
        "happy": {
            "base": "微笑",
            "rising": "开怀大笑",
            "peak": "充满喜悦",
            "soothing": "满足的微笑"
        },
        "sad": {
            "base": "忧郁",
            "rising": "眼中含泪",
            "peak": "悲伤涌上心头",
            "soothing": "平静接受"
        },
        "surprise": {
            "base": "好奇",
            "rising": "惊讶",
            "peak": "难以置信",
            "soothing": "逐渐理解"
        },
        "romantic": {
            "base": "温柔注视",
            "rising": "眼神炙热",
            "peak": "充满爱意",
            "soothing": "满足的微笑"
        },
        "mysterious": {
            "base": "神秘表情",
            "rising": "目光深邃",
            "peak": "充满谜团",
            "soothing": "若有所思"
        },
        "action": {
            "base": "专注表情",
            "rising": "全力以赴",
            "peak": "激烈对抗",
            "soothing": "胜利满足"
        }
    }

    # 环境互动关键词
    ENVIRONMENT_INTERACTION = {
        "rain": "雨水从天空滴落，在地面上溅起水花",
        "sunshine": "温暖的阳光透过窗户洒下斑驳的光影",
        "wind": "微风轻拂，树叶沙沙作响",
        "night": "霓虹灯在湿润的地面反射出绚丽的光芒",
        "snow": "雪花飘落，覆盖一切，世界变得洁白纯净",
        "fire": "火焰跳跃，照亮周围，热浪涌动",
        "ocean": "海浪拍打岸边，溅起白色泡沫",
        "forest": "翠绿的竹林在微风中摇曳，竹叶沙沙作响，空气中弥漫着清新的草木香",
        "garden": "花草摇曳，蝴蝶飞舞，鸟鸣声在林间回荡，空气中弥漫着花香",
        "cafe": "咖啡香气弥漫，温暖的光线透过大玻璃窗洒进来，周围是温馨的装饰和精致的桌椅",
        "cyberpunk": "霓虹闪烁，电子广告牌显示着流动的信息",
        "urban": "城市喧嚣，车流穿梭，建筑耸立",
        "forest_combat": "剑气划过竹林，竹叶纷纷飘落。脚下的落叶被劲风卷起，四周竹子在激烈的对决中微微颤抖。",
        "rain_combat": "雨水在激烈的打斗中飞溅，每一剑划过都带起水珠。地面被脚步踩得泥水四溅。",
        "urban_combat": "街头烟尘四起，路边的物体被劲波撞飞。混凝土碎屑在空中飞舞，周围的建筑物在激烈的战斗中微微震动。",
        "night_combat": "霓虹灯光在战斗中破碎闪烁，光效四溢。黑暗中的剪影快速移动，光影交错如电光火石。"
    }

    # 风格关键词库
    STYLE_KEYWORDS = {
        "科幻": ["未来科技", "机械", "金属", "电子", "全息", "人工智能"],
        "写实": ["真实", "细节丰富", "自然光线", "逼真", "质感"],
        "童话": ["梦幻", "魔法", "色彩鲜艳", "可爱", "奇幻"],
        "武侠": ["古装", "飘逸", "水墨风格", "侠客", "气场"],
        "浪漫": ["柔和光线", "温馨", "精致", "优雅", "诗意"]
    }

    # 视频类型映射
    VIDEO_TYPES = {
        "photo-realistic": "超逼真视频生成",
        "character-consistency": "角色与场景一致性",
        "camera-movement": "高级运镜动作",
        "creative-effects": "创意视觉特效",
        "storytelling": "剧情发展与延伸",
        "audio-sync": "音频与语音合成",
        "one-shot": "一镜到底",
        "emotion-performance": "情绪演绎"
    }

    # 难度级别映射
    DIFFICULTY_LEVELS = {
        "BEGINNER": "初学者",
        "INTERMEDIATE": "中级",
        "ADVANCED": "高级",
        "EXPERT": "专家"
    }

    # 预设的提示词元素库
    ELEMENT_LIBRARY = {
        "lighting": [
            "自然光",
            "柔和光线",
            "戏剧性光影",
            "高对比度",
            "电影打光",
            "晨曦",
            "日落金光",
            "霓虹灯光",
            "烛光",
            "阴影柔和"
        ],
        "camera": [
            "固定镜头",
            "特写镜头",
            "中景",
            "广角镜头",
            "跟拍",
            "摇摄",
            "推镜头",
            "环绕镜头",
            "俯拍",
            "仰拍"
        ],
        "style": [
            "写实",
            "梦幻",
            "艺术",
            "科幻",
            "奇幻",
            "复古",
            "现代",
            "文艺",
            "悬疑惊悚",
            "浪漫温馨"
        ],
        "quality": [
            "高清",
            "超高清",
            "4K",
            "8K",
            "电影级",
            "HDR",
            "超精细"
        ],
        "constraints": [
            "自然流畅",
            "物理真实性",
            "细节清晰",
            "运镜稳定",
            "无剪辑",
            "情感自然",
            "节奏协调"
        ],
        "sound_effects": [
            "自然的音效，如风声、雨声、鸟鸣声",
            "环境音效，如城市噪音、机器运转声",
            "动作音效，如脚步声、碰撞声、武器声",
            "氛围音效，如心跳声、呼吸声",
            "特殊音效，如魔法声、能量声",
            "静谧环境，只有轻微的自然音"
        ],
        "background_music": [
            "激昂的背景音乐，节奏强烈",
            "宁静的背景音乐，旋律优美",
            "悬疑的背景音乐，氛围紧张",
            "浪漫的背景音乐，温馨甜蜜",
            "史诗的背景音乐，气势磅礴",
            "环境背景音，如海浪声、雨声",
            "无背景音乐，只有环境音"
        ],
        "narration": [
            "第一人称旁白，讲述自己的故事",
            "第三人称旁白，客观描述场景",
            "内心独白，展示角色内心",
            "诗意旁白，用优美语言描述",
            "简洁旁白，点到为止",
            "无旁白"
        ],
        "dialogue": [
            "自然对话，日常交流",
            "激烈对话，情绪激动",
            "诗意对话，如诗如画",
            "沉默对话，眼神交流",
            "内心对话，自我思考",
            "无对话，只有动作"
        ]
    }

    # 参考风格模板库
    REFERENCE_TEMPLATES = {
        'movie_trailer': {
            'name': '电影预告片风格',
            'style': '电影风格',
            'lighting': '戏剧性光影',
            'camera': '电影镜头语言',
            'quality': '电影级',
            'background_music': '史诗的背景音乐，气势磅礴',
            'narration': '电影旁白，史诗风格'
        },
        'commercial': {
            'name': '广告风格',
            'style': '商业风格',
            'lighting': '柔和光线',
            'camera': '产品特写镜头',
            'quality': '超高清',
            'background_music': '背景音乐，温馨甜蜜',
            'narration': '广告旁白，专业风格'
        },
        'social_media': {
            'name': '社交媒体风格',
            'style': '现代风格',
            'lighting': '自然光',
            'camera': '手持镜头',
            'quality': '高清',
            'background_music': '背景音乐，轻快',
            'narration': '社交媒体旁白，轻松风格'
        },
        'documentary': {
            'name': '纪录片风格',
            'style': '写实风格',
            'lighting': '自然光线',
            'camera': '纪录片镜头',
            'quality': '超高清',
            'background_music': '环境背景音，如海浪声',
            'narration': '纪录片旁白，客观描述'
        },
        'anime': {
            'name': '动画风格',
            'style': '动漫风格',
            'lighting': '动漫光影',
            'camera': '动漫镜头',
            'quality': '高清',
            'background_music': '动画背景音乐，轻松愉快',
            'narration': '动漫旁白，可爱风格'
        }
    }

    # 场景模板库
    SCENE_TEMPLATES = {
        # 电商场景
        'ecommerce_product': {
            'name': '电商商品展示',
            'style': '商业风格',
            'lighting': '产品打光',
            'camera': '产品特写镜头',
            'quality': '超高清',
            'dialogue': '产品介绍对话',
            'background_music': '商业背景音乐，轻快'
        },
        'ecommerce_tutorial': {
            'name': '电商使用教程',
            'style': '教育风格',
            'lighting': '清晰光线',
            'camera': '教学镜头',
            'quality': '高清',
            'dialogue': '教学对话',
            'narration': '教学旁白，清晰明了'
        },
        # 好莱坞场景
        'hollywood_trailer': {
            'name': '好莱坞预告片',
            'style': '电影风格',
            'lighting': '戏剧性光影',
            'camera': '电影镜头语言',
            'quality': '电影级',
            'background_music': '史诗的背景音乐，气势磅礴',
            'narration': '电影旁白，史诗风格'
        },
        'hollywood_short': {
            'name': '好莱坞短片',
            'style': '艺术风格',
            'lighting': '电影打光',
            'camera': '电影运镜',
            'quality': '电影级',
            'background_music': '艺术背景音乐，优美动听',
            'narration': '电影旁白，诗意风格'
        },
        # 游戏场景
        'game_trailer': {
            'name': '游戏预告片',
            'style': '科幻风格',
            'lighting': '游戏光影',
            'camera': '游戏镜头',
            'quality': '超高清',
            'background_music': '激昂的背景音乐，节奏强烈',
            'narration': '游戏旁白，激动人心'
        },
        'game_character': {
            'name': '游戏角色介绍',
            'style': '奇幻风格',
            'lighting': '角色打光',
            'camera': '角色特写镜头',
            'quality': '超高清',
            'background_music': '游戏背景音乐，史诗',
            'narration': '角色旁白，详细介绍'
        }
    }

    # 打戏动作模板
    ACTION_TEMPLATES = {
        "combat": {
            "sword": "剑锋闪烁，一招劈砍直取对手要害，对手侧身闪避，反手一剑刺来。两人在竹林中快速移动，剑气四溢，每一剑都带着破风声。",
            "fist": "拳风凌厉，一记重拳破空而来。对手格挡反攻，两人近身肉搏，拳影交错。拳头碰撞发出闷响，汗水四溅。",
            "weapon": "兵器相撞，火花四溅。兵器快速挥舞，每一击都带着破风声。双方在空间中快速移动，刀光剑影交错。",
            "general": "动作迅猛有力，招招致命。双方在场景中快速移动，攻防转换如行云流水。每一次交锋都带着强烈的冲击力，周围环境被动作所影响。"
        }
    }

    # 温和的打戏情感路径
    MILD_EMOTION_KEYWORDS = {
        "combat": {
            "base": "专注认真",
            "rising": "沉浸其中",
            "peak": "精彩切磋",
            "soothing": "切磋结束"
        }
    }

    # 温和的打戏环境互动
    MILD_ENVIRONMENT_INTERACTION = {
        "forest_combat": "剑气与竹叶共舞，营造出充满美感的武术竞技场面。",
        "rain_combat": "雨水在精妙的武术招式中飞溅，每一剑都带着优美的弧度。",
        "urban_combat": "武术大师在街头展示精湛的剑术，吸引路人驻足观看。",
        "night_combat": "霓虹灯光在武术动作中闪烁，光影交错如梦如幻。"
    }

    # 温和的打戏动作模板
    MILD_ACTION_TEMPLATES = {
        "combat": {
            "sword": "两位大师在竹林中精彩切磋，展示出精妙的招式和深厚的内力。动作飘逸而有力，每一个招式都展现着中华武术的博大精深。",
            "fist": "两位武术大师在竞技中展示精湛的拳法，动作刚柔并济，每一个招式都充满美感。双方你来我往，攻防转换如行云流水。",
            "weapon": "武术大师展示精湛的兵器使用技巧，每一个动作都充满艺术感。兵器在空中划出优美的弧线，展现出中华武术的深厚底蕴。",
            "general": "两位大师在切磋中展示精妙的招式，动作飘逸而有力，展现出中华武术的博大精深。"
        }
    }

    def __init__(self, template_lib: Optional[TemplateLibrary] = None):
        """
        初始化提示词生成器

        Args:
            template_lib: 模板库实例，如果为 None 则创建新实例
        """
        self.template_lib = template_lib or TemplateLibrary()
        self.online_search_enabled = ONLINE_SEARCH_AVAILABLE

        # 初始化智能扩展场景模板库
        if SMART_EXPANSION_AVAILABLE:
            self.scene_template_lib = SceneTemplateLibrary()
            logger.info("智能扩展场景模板库已加载")
        else:
            self.scene_template_lib = None
            logger.warning("智能扩展模块不可用，场景模板库未加载")

    def generate_prompt_with_search(
        self,
        scene: str,
        style: Optional[str] = None,
        duration: Optional[str] = None,
        difficulty: str = "INTERMEDIATE",
        video_type: str = "photo-realistic",
        include_elements: bool = True,
        use_online: bool = True,
        online_search: bool = False,
        max_online_results: int = 5
    ) -> Dict:
        """
        生成提示词（可选在线搜索）

        Args:
            scene: 场景描述
            style: 风格
            duration: 时长
            difficulty: 难度级别
            video_type: 视频类型
            include_elements: 是否包含元素分析
            use_online: 是否使用在线功能（默认启用）
            online_search: 是否先搜索再生成（默认 False）
            max_online_results: 最大在线搜索结果数量

        Returns:
            包含生成结果的字典

        示例:
            >>> # 基本生成（不使用在线搜索）
            >>> result = generator.generate_prompt_with_search("雨天城市街道", online_search=False)
            >>>
            >>> # 使用在线搜索
            >>> result = generator.generate_prompt_with_search("雨天城市街道", online_search=True)
        """
        result = {
            'prompt': '',
            'elements': {},
            'variants': [],
            'video_type': video_type,
            'difficulty': difficulty,
            'recommended_duration': duration or self._suggest_duration(difficulty),
            'online_used': False,
            'online_results': []
        }

        # 如果启用了在线搜索，先搜索相关提示词
        if use_online and online_search and self.online_search_enabled:
            logger.info(f"正在在线搜索: {scene}")

            try:
                online_results = search_online_prompts(
                    query=scene,
                    video_type=video_type,
                    difficulty=difficulty,
                    max_results=max_online_results
                )

                if online_results:
                    result['online_used'] = True
                    result['online_results'] = online_results
                    logger.info(f"成功获取 {len(online_results)} 个在线提示词")

                    # 从在线结果中提取有用的元素
                    self._merge_online_elements(result, online_results)

                else:
                    logger.warning("在线搜索未返回结果，使用本地生成")

            except Exception as e:
                logger.error(f"在线搜索失败: {str(e)}，回退到本地生成")

        # 生成本地提示词
        local_result = self.generate_prompt(
            scene=scene,
            style=style,
            duration=duration,
            difficulty=difficulty,
            video_type=video_type,
            include_elements=include_elements
        )

        # 合并本地和在线结果
        result['prompt'] = local_result['prompt']
        result['elements'] = local_result['elements']
        result['variants'] = local_result['variants']

        if 'reference_template' in local_result:
            result['reference_template'] = local_result['reference_template']

        return result

    def generate_with_reference(
        self,
        scene: str,
        reference_type: str,
        duration: Optional[str] = None,
        difficulty: str = "INTERMEDIATE",
        include_elements: bool = True
    ) -> Dict:
        """
        根据参考风格生成提示词

        Args:
            scene: 场景描述
            reference_type: 参考类型（movie_trailer, commercial, social_media, documentary, anime）
            duration: 时长
            difficulty: 难度级别
            include_elements: 是否包含元素分析

        Returns:
            生成的提示词字典
        """
        # 获取参考模板
        reference = self.REFERENCE_TEMPLATES.get(reference_type)
        
        if not reference:
            raise ValueError(f"不支持的参考类型: {reference_type}")

        # 构建提示词
        result = self.generate_prompt(
            scene=scene,
            style=reference.get('style', '现代'),
            duration=duration,
            difficulty=difficulty,
            include_elements=include_elements
        )

        # 应用参考风格的额外参数
        if include_elements and 'elements' in result:
            result['elements']['lighting'] = reference.get('lighting', '自然光')
            result['elements']['camera'] = reference.get('camera', '中景')
            result['elements']['quality'] = reference.get('quality', '高清')
            result['elements']['background_music'] = reference.get('background_music', '环境背景音')
            result['elements']['narration'] = reference.get('narration', '无旁白')

        # 添加参考信息
        result['reference_type'] = reference_type
        result['reference_name'] = reference.get('name', '未知')

        return result

    def generate_with_scene_template(
        self,
        scene: str,
        template_type: str,
        duration: Optional[str] = None,
        difficulty: str = "INTERMEDIATE",
        include_elements: bool = True
    ) -> Dict:
        """
        根据场景模板生成提示词

        Args:
            scene: 场景描述
            template_type: 模板类型（ecommerce_product, ecommerce_tutorial, hollywood_trailer, hollywood_short, game_trailer, game_character）
            duration: 时长
            difficulty: 难度级别
            include_elements: 是否包含元素分析

        Returns:
            生成的提示词字典
        """
        # 获取场景模板
        template = self.SCENE_TEMPLATES.get(template_type)
        
        if not template:
            raise ValueError(f"不支持的模板类型: {template_type}")

        # 构建提示词
        result = self.generate_prompt(
            scene=scene,
            style=template.get('style', '现代'),
            duration=duration,
            difficulty=difficulty,
            include_elements=include_elements
        )

        # 应用场景模板的额外参数
        if include_elements and 'elements' in result:
            result['elements']['lighting'] = template.get('lighting', '自然光')
            result['elements']['camera'] = template.get('camera', '中景')
            result['elements']['quality'] = template.get('quality', '高清')
            result['elements']['background_music'] = template.get('background_music', '环境背景音')
            
            if 'narration' in template:
                result['elements']['narration'] = template.get('narration', '无旁白')
            if 'dialogue' in template:
                result['elements']['dialogue'] = template.get('dialogue', '无对话')

        # 添加模板信息
        result['template_type'] = template_type
        result['template_name'] = template.get('name', '未知')

        return result

    def _merge_online_elements(self, result: Dict, online_results: List[Dict]):
        """
        将在线搜索结果中的元素合并到结果中

        Args:
            result: 结果字典
            online_results: 在线搜索结果列表
        """
        # 简单的合并策略：使用第一个在线结果的元素
        if online_results and len(online_results) > 0:
            first_result = online_results[0]

            # 尝试提取提示词
            if 'prompt' in first_result and first_result['prompt']:
                result['online_suggestion'] = first_result['prompt']

            # 提取其他有用信息
            if 'tags' in first_result:
                result['online_tags'] = first_result['tags']

            if 'url' in first_result:
                result['online_source'] = first_result['url']

    def generate_prompt(
        self,
        scene: str,
        style: Optional[str] = None,
        duration: Optional[str] = None,
        difficulty: str = "INTERMEDIATE",
        video_type: str = "photo-realistic",
        include_elements: bool = True
    ) -> Dict:
        """
        根据用户输入生成完整提示词

        Args:
            scene: 场景描述
            style: 风格
            duration: 时长
            difficulty: 难度级别
            video_type: 视频类型
            include_elements: 是否包含元素分析

        Returns:
            包含生成结果的字典
        """
        # 尝试从模板库获取基础模板
        templates = self.template_lib.get_templates_by_type_and_difficulty(video_type, difficulty)

        # 提取场景描述中的关键信息
        elements = self._parse_scene(scene)

        # 补充元素（如果未提供）
        if style:
            elements['style'] = style

        elements = self._complete_elements(elements, difficulty)

        # 生成完整提示词
        prompt = self._construct_prompt(elements, difficulty)

        # 如果指定了时长，添加到元素中
        if duration:
            elements['duration'] = duration

        # 生成变体
        variants = self._generate_variants(elements, difficulty)

        result = {
            'prompt': prompt,
            'elements': elements,
            'variants': variants,
            'video_type': video_type,
            'difficulty': difficulty,
            'recommended_duration': duration or self._suggest_duration(difficulty)
        }

        # 如果有相关模板，也提供参考
        if templates:
            result['reference_template'] = templates[0]['id']

        return result

    def _parse_scene(self, scene: str) -> Dict:
        """
        解析场景描述，提取元素

        Args:
            scene: 场景描述文本

        Returns:
            提取的元素字典
        """
        elements = {}

        # 将场景描述作为主体
        elements['subject'] = scene

        # 尝试提取动作关键词
        action_keywords = ['正在', '进行', '正在做', '开始', '结束', '跑', '走', '跳', '飞', '游']
        for keyword in action_keywords:
            if keyword in scene:
                elements['action'] = f"{keyword}中"
                break

        # 尝试提取场景关键词
        scene_keywords = ['在', '于', '里', '外', '室内', '室外', '花园', '街道', '森林', '海边']
        for keyword in scene_keywords:
            if keyword in scene:
                # 修复"在在场景"重复问题：如果 keyword 是"在"，直接使用场景描述，不再添加"场景"
                if keyword == '在':
                    elements['scene'] = "场景"
                else:
                    elements['scene'] = f"{keyword}场景"
                break

        return elements

    def _complete_elements(self, elements: Dict, difficulty: str) -> Dict:
        """
        根据难度补充缺失的元素

        Args:
            elements: 已有的元素字典
            difficulty: 难度级别

        Returns:
            补充后的元素字典
        """
        # 确保主体存在
        if 'subject' not in elements:
            elements['subject'] = "一个主体"

        # 根据难度补充元素
        if difficulty in ['BEGINNER']:
            # 初学者：只补充基本元素
            if 'action' not in elements:
                elements['action'] = "进行动作"
            if 'scene' not in elements:
                elements['scene'] = "场景中"
            if 'style' not in elements:
                elements['style'] = random.choice(self.ELEMENT_LIBRARY['style'])
            if 'quality' not in elements:
                elements['quality'] = "高清"

        elif difficulty in ['INTERMEDIATE']:
            # 中级：补充更多元素
            if 'action' not in elements:
                elements['action'] = "自然地进行动作"
            if 'scene' not in elements:
                elements['scene'] = "场景中"
            if 'lighting' not in elements:
                elements['lighting'] = random.choice(self.ELEMENT_LIBRARY['lighting'])
            if 'camera' not in elements:
                elements['camera'] = random.choice(self.ELEMENT_LIBRARY['camera'])
            if 'style' not in elements:
                elements['style'] = random.choice(self.ELEMENT_LIBRARY['style'])
            if 'quality' not in elements:
                elements['quality'] = random.choice(self.ELEMENT_LIBRARY['quality'])

        elif difficulty in ['ADVANCED', 'EXPERT']:
            # 高级和专家：补充所有元素（包含音效、音乐、旁白、对话）
            if 'action' not in elements:
                elements['action'] = "流畅地进行复杂动作"
            if 'scene' not in elements:
                elements['scene'] = "精心设计的场景中"
            if 'lighting' not in elements:
                elements['lighting'] = random.choice(self.ELEMENT_LIBRARY['lighting'])
            if 'camera' not in elements:
                elements['camera'] = random.choice(self.ELEMENT_LIBRARY['camera'])
            if 'style' not in elements:
                elements['style'] = random.choice(self.ELEMENT_LIBRARY['style'])
            if 'quality' not in elements:
                elements['quality'] = random.choice(self.ELEMENT_LIBRARY['quality'])
            if 'sound_effects' not in elements:
                elements['sound_effects'] = random.choice(self.ELEMENT_LIBRARY.get('sound_effects', ['自然音效']))
            if 'background_music' not in elements:
                elements['background_music'] = random.choice(self.ELEMENT_LIBRARY.get('background_music', ['背景音乐']))
            if 'narration' not in elements:
                elements['narration'] = random.choice(self.ELEMENT_LIBRARY.get('narration', ['旁白']))
            if 'dialogue' not in elements:
                elements['dialogue'] = random.choice(self.ELEMENT_LIBRARY.get('dialogue', ['对话']))
            if 'constraints' not in elements:
                elements['constraints'] = random.choice(self.ELEMENT_LIBRARY['constraints'])

        return elements

    def _construct_prompt(self, elements: Dict, difficulty: str) -> str:
        """
        根据元素构建完整提示词

        Args:
            elements: 元素字典
            difficulty: 难度级别

        Returns:
            完整提示词文本
        """
        if difficulty == 'BEGINNER':
            # 初学者：简单的主体 + 动作 + 风格
            prompt = f"{elements.get('subject', '')}，{elements.get('action', '')}。{elements.get('style', '')}风格。"
        elif difficulty == 'INTERMEDIATE':
            # 中级：主体 + 动作 + 场景 + 光影 + 镜头 + 风格
            prompt = (
                f"{elements.get('subject', '')}在{elements.get('scene', '')}"
                f"{elements.get('action', '')}，"
                f"{elements.get('lighting', '')}，"
                f"{elements.get('camera', '')}，"
                f"{elements.get('style', '')}风格。"
            )
        else:
            # 高级和专家：完整的万能公式（包含音效、音乐、旁白、对话）
            prompt = (
                f"{elements.get('subject', '')}在{elements.get('scene', '')}"
                f"{elements.get('action', '')}，"
                f"{elements.get('lighting', '')}，"
                f"{elements.get('camera', '')}，"
                f"{elements.get('style', '')}风格，"
                f"{elements.get('quality', '')}，"
                f"{elements.get('sound_effects', '')}，"
                f"{elements.get('background_music', '')}，"
                f"{elements.get('narration', '')}，"
                f"{elements.get('dialogue', '')}，"
                f"{elements.get('constraints', '')}。"
            )

        return prompt

    def _generate_variants(self, elements: Dict, difficulty: str, count: int = 3) -> List[str]:
        """
        生成提示词变体

        Args:
            elements: 基础元素字典
            difficulty: 难度级别
            count: 生成的变体数量

        Returns:
            变体提示词列表
        """
        variants = []

        for i in range(count):
            variant_elements = elements.copy()

            # 随机修改某些元素
            if difficulty in ['INTERMEDIATE', 'ADVANCED', 'EXPERT']:
                if 'lighting' in variant_elements:
                    variant_elements['lighting'] = random.choice(self.ELEMENT_LIBRARY['lighting'])
                if 'camera' in variant_elements:
                    variant_elements['camera'] = random.choice(self.ELEMENT_LIBRARY['camera'])
                if 'style' in variant_elements:
                    variant_elements['style'] = random.choice(self.ELEMENT_LIBRARY['style'])

            # 生成变体提示词
            variant = self._construct_prompt(variant_elements, difficulty)
            variants.append(variant)

        return variants

    def _suggest_duration(self, difficulty: str) -> str:
        """
        根据难度建议时长

        Args:
            difficulty: 难度级别

        Returns:
            建议的时长
        """
        duration_map = {
            'BEGINNER': '5-10s',
            'INTERMEDIATE': '6-12s',
            'ADVANCED': '8-15s',
            'EXPERT': '10-20s'
        }
        return duration_map.get(difficulty, '5-10s')

    def generate_prompt_with_timing(
        self,
        scene: str,
        style: str = "写实",
        duration: str = "15s",
        difficulty: str = "ADVANCED",
        video_type: str = "photo-realistic",
        use_template: bool = True,
        auto_save: bool = True,
        mild_mode: bool = False,
        image_mode: str = "text"
    ) -> Dict:
        """
        按照时间分段标准生成15秒提示词

        Args:
            scene: 场景描述
            style: 风格
            duration: 时长
            difficulty: 难度级别
            video_type: 视频类型
            use_template: 是否使用场景模板库（默认启用）
            auto_save: 是否自动保存新生成的模板（默认启用）
            mild_mode: 是否使用温和模式（默认为False，打戏场景时使用激烈词汇；为True时使用温和词汇）
            image_mode: 图片模式（默认为'text'，纯文字模式；可选'image_9grid'，九宫格图片模式）

        Returns:
            包含时间分段提示词的字典
        """
        # 1. 检查场景模板库
        used_template = False
        template_source = None

        if use_template and SMART_EXPANSION_AVAILABLE and self.scene_template_lib:
            # 尝试从模板库获取
            template = self.scene_template_lib.get_template(scene)

            if template:
                # 使用模板库中的模板
                logger.info(f"使用场景模板库中的模板: {scene}")
                intro = template.get('intro', '')
                main_action = template.get('main_action', '')
                emotion_rise = template.get('emotion_rise', '')
                conclusion = template.get('conclusion', '')
                used_template = True
                template_source = "template_library"
            else:
                logger.info(f"场景 '{scene}' 未在模板库中找到，使用自动生成")
        else:
            logger.info("未使用场景模板库，使用自动生成")

        # 2. 如果没有模板，自动生成
        if not used_template:
            # 0-3秒：引入场景
            intro = self._generate_intro(scene, style, mild_mode=mild_mode)

            # 3-7秒：主要动作
            main_action = self._generate_main_action(scene, style, mild_mode=mild_mode)

            # 7-12秒：情感升级
            emotion_rise = self._generate_emotion_rise(scene, style, mild_mode=mild_mode)

            # 12-15秒：情感收尾
            conclusion = self._generate_conclusion(scene, style, mild_mode=mild_mode)

        # 检测情感类型，决定是否使用时间分段标记
        emotion = self._detect_emotion(scene)
        
        # 打戏场景（combat, action）不使用时间标记，其他场景保留时间标记
        if emotion in ['combat', 'action']:
            # 打戏场景：使用纯文本格式，不使用时间标记
            full_prompt = f"{intro} {main_action} {emotion_rise} {conclusion}"
        else:
            # 其他场景：保留时间分段标记
            full_prompt = f"""【0-3秒】引入场景
{intro}
【3-7秒】主要动作
{main_action}
【7-12秒】情感升级
{emotion_rise}
【12-15秒】情感收尾
{conclusion}"""

        result = {
            "prompt": full_prompt,
            "emotion": emotion,
            "segments": {
                "intro_0-3s": intro,
                "main_action_3-7s": main_action,
                "emotion_rise_7-12s": emotion_rise,
                "conclusion_12-15s": conclusion
            },
            "duration": duration,
            "difficulty": difficulty,
            "video_type": video_type,
            "word_count": len(full_prompt),
            "used_template": used_template,
            "template_source": template_source
        }

        # 3. 自动保存新模板（如果未使用模板且启用了自动保存）
        if not used_template and auto_save and SMART_EXPANSION_AVAILABLE:
            try:
                auto_expand_template(scene, result)
                result['auto_saved'] = True
            except Exception as e:
                logger.error(f"自动保存模板失败: {e}")
                result['auto_saved'] = False

        return result

    def _detect_environment(self, scene: str) -> str:
        """
        检测场景中的环境类型

        Args:
            scene: 场景描述

        Returns:
            环境类型键名
        """
        scene_lower = scene.lower()

        # 先检测是否是打戏场景
        combat_keywords = ["决战", "打戏", "对决", "激战", "交锋", "对峙", "战斗", "对打", "搏斗", "厮杀", "刀剑", "切磋", "武术", "竞技", "比武", "剑术"]
        is_combat = any(keyword in scene_lower for keyword in combat_keywords)

        # 检测关键词（按优先级顺序，更具体的关键词放在前面）
        env_keywords = {
            "snow": ["雪", "雪花", "飘雪", "冰", "雪山", "冰雪"],
            "rain": ["雨夜", "雨天", "雨", "下雨", "降雨"],
            "night": ["霓虹", "夜晚", "黑暗", "夜", "月光", "夜景"],
            "fire": ["火", "火焰", "燃烧"],
            "ocean": ["海", "海边", "海洋", "浪", "沙滩"],
            "cyberpunk": ["赛博", "霓虹灯", "科技", "电子", "未来", "机器人", "赛博朋克"],
            "wind": ["风", "微风", "大风", "风声"],
            "cafe": ["咖啡馆", "咖啡", "咖啡厅"],
            "garden": ["花园", "花", "童话", "魔法", "植物"],
            "forest": ["竹林", "竹", "森林", "树林", "林", "山"],
            "urban": ["城市", "街道", "建筑", "巴黎", "商店", "市集"],
            "sunshine": ["阳光", "晴天", "明媚", "早晨", "日出", "窗户"]
        }

        for env, keywords in env_keywords.items():
            if any(keyword in scene_lower for keyword in keywords):
                # 如果是打戏场景，返回对应的打戏环境类型
                if is_combat:
                    if env in ["forest", "garden"]:
                        return "forest_combat"
                    elif env == "rain":
                        return "rain_combat"
                    elif env == "night":
                        return "night_combat"
                    else:
                        return "urban_combat"
                return env

        return "urban_combat" if is_combat else "urban"  # 默认返回城市打戏或城市

    def _detect_emotion(self, scene: str) -> str:
        """
        检测场景中的情感类型

        Args:
            scene: 场景描述

        Returns:
            情感类型键名
        """
        scene_lower = scene.lower()

        # 检测情感关键词（按优先级顺序）
        emotion_keywords = {
            "combat": ["决战", "打戏", "对决", "激战", "交锋", "对峙", "武术", "战斗", "对打", "搏斗", "厮杀", "刀剑"],
            "action": ["动作", "攻击", "对抗", "飘逸动作"],
            "happy": ["童话", "快乐", "喜悦", "幸福", "开心", "欢乐", "庆祝", "魔法"],
            "romantic": ["浪漫", "爱情", "约会", "情侣", "温馨", "咖啡馆", "巴黎"],
            "mysterious": ["神秘", "未知", "谜团", "探索", "黑暗"],
            "surprise": ["惊讶", "震惊", "奇怪", "好奇", "发现"],
            "sad": ["悲伤", "难过", "忧郁", "眼泪", "失落"]
        }

        for emotion, keywords in emotion_keywords.items():
            if any(keyword in scene_lower for keyword in keywords):
                return emotion

        return "romantic"  # 默认返回浪漫

    def _generate_intro(self, scene: str, style: str, mild_mode: bool = False) -> str:
        """
        生成0-3秒的引入场景

        Args:
            scene: 场景描述
            style: 风格
            mild_mode: 是否使用温和模式

        Returns:
            引入场景描述
        """
        env = self._detect_environment(scene)
        emotion = self._detect_emotion(scene)

        # 根据是否是温和模式选择环境描述
        if emotion == "combat" and mild_mode:
            env_desc = self.MILD_ENVIRONMENT_INTERACTION.get(env, self.MILD_ENVIRONMENT_INTERACTION.get("urban_combat", ""))
        else:
            env_desc = self.ENVIRONMENT_INTERACTION.get(env, self.ENVIRONMENT_INTERACTION["urban"])

        style_keys = self.STYLE_KEYWORDS.get(style, self.STYLE_KEYWORDS["写实"])
        style_word = style_keys[0] if style_keys else "写实"

        # 如果是打戏场景，生成打戏风格的引入
        if emotion == "combat" and mild_mode:
            # 温和版本的引入
            intro = f"镜头缓缓展开，{env_desc}。剑气四溢，展现出中华武术的深厚底蕴。两位武术大师出现在画面两端，形成对峙之势。空气中弥漫着武术竞技的氛围，双方专注认真，一触即发。"
        elif emotion == "combat":
            # 激烈版本的引入
            intro = f"镜头快速展开，{env_desc}。{style_word}风格的环境中，两位主角出现在画面两端，形成对峙之势。空气中弥漫着紧张的气氛，双方眼神犀利，一触即发。"
        else:
            intro = f"镜头缓慢展开，{env_desc}。{style_word}风格的环境中，主角出现在画面中央，周围景色清晰可见。光线柔和，氛围{style_word}。"

        return intro

    def _generate_main_action(self, scene: str, style: str, mild_mode: bool = False) -> str:
        """
        生成3-7秒的主要动作

        Args:
            scene: 场景描述
            style: 风格
            mild_mode: 是否使用温和模式

        Returns:
            主要动作描述
        """
        env = self._detect_environment(scene)
        emotion = self._detect_emotion(scene)

        # 如果是打戏场景，使用打戏动作模板
        if emotion == "combat":
            # 根据是否是温和模式选择模板
            if mild_mode:
                combat_templates = self.MILD_ACTION_TEMPLATES.get("combat", {})
            else:
                combat_templates = self.ACTION_TEMPLATES.get("combat", {})

            # 根据场景关键词选择合适的打戏动作
            if any(keyword in scene.lower() for keyword in ["剑", "刀", "剑客", "剑法"]):
                main_action = combat_templates.get("sword", combat_templates.get("general", ""))
            elif any(keyword in scene.lower() for keyword in ["拳", "拳手", "拳法"]):
                main_action = combat_templates.get("fist", combat_templates.get("general", ""))
            else:
                main_action = combat_templates.get("general", "")
            return main_action

        # 根据环境生成不同的主要动作
        action_templates = {
            "cafe": "主角在咖啡馆内落座，轻抿一口热咖啡。目光投向窗外的街景，表情放松而惬意。手指轻轻敲击桌面，享受着这片刻的宁静。",
            "garden": "主角在花园中漫步，伸手轻触盛开的花朵。蝴蝶在周围飞舞，主角驻足观赏，脸上露出欣喜的表情。步伐轻盈，与自然和谐共处。",
            "forest": "主角在竹林中穿行，衣摆随风飘动。时而伸手轻触竹叶，时而抬头望向天空，动作飘逸而优雅，与竹林的静谧融为一体。",
            "rain": "主角在雨中缓缓行走，雨水打在身上，水珠沿着发丝滑落。身体微微前倾，踏水而行，每一步都激起小小的水花。",
            "sunshine": "主角在阳光下伸展双臂，感受温暖。身体自然摆动，脚步轻盈，沿着小径前行，与周围环境和谐互动。",
            "wind": "主角迎风而立，长发随风飘扬。衣角翻飞，身体微微摆动，与风的节奏融为一体。",
            "night": "主角在霓虹灯光下走过，脚步稳健。目光扫过周围的建筑和灯光，表情专注而从容。",
            "snow": "主角在雪地上缓慢行走，留下一串脚印。伸手接住飘落的雪花，动作温柔而优雅。",
            "fire": "主角靠近火焰，感受温暖。面部被火光映照，动作谨慎而好奇，伸手试探温度。",
            "ocean": "主角站在海边，面对海浪。海风吹拂，衣衫飘动，目光投向远方，感受大海的浩瀚。",
            "cyberpunk": "主角在科技感十足的环境中穿行，电子设备闪烁。动作流畅，与全息投影互动，展现未来感。",
            "urban": "主角在城市中漫步，观察周围的人和事。步伐从容，与城市节奏保持一致，融入环境。",
            "forest_combat": "两位侠客在竹林中对峙，剑光闪烁。竹叶在剑气中纷纷飘落，脚步快速移动，落叶被劲风卷起。",
            "rain_combat": "雨水在激烈的交锋中飞溅，每一剑都带起水珠。两位剑客在雨中快速移动，剑气四溢，地面被踩得泥水四溅。",
            "urban_combat": "两位拳手在街头对决，拳风凌厉。路边的物体被劲波撞飞，混凝土碎屑在空中飞舞，每一击都带着强烈的冲击力。",
            "night_combat": "霓虹灯光在战斗中破碎闪烁，黑暗中的剪影快速移动。光影交错如电光火石，每一次交锋都带着毁灭性的力量。"
        }

        main_action = action_templates.get(env, action_templates["urban"])

        return main_action

    def _generate_emotion_rise(self, scene: str, style: str, mild_mode: bool = False) -> str:
        """
        生成7-12秒的情感升级

        Args:
            scene: 场景描述
            style: 风格
            mild_mode: 是否使用温和模式

        Returns:
            情感升级描述
        """
        emotion = self._detect_emotion(scene)

        # 根据是否是温和模式选择情感关键词
        if emotion == "combat" and mild_mode:
            emotion_words = self.MILD_EMOTION_KEYWORDS.get(emotion, self.MILD_EMOTION_KEYWORDS.get("combat", {}))
        else:
            emotion_words = self.EMOTION_KEYWORDS.get(emotion, self.EMOTION_KEYWORDS["romantic"])

        # 情感从基础到强烈
        if emotion == "combat" and mild_mode:
            # 温和版本的情感升级
            emotion_rise = (
                f"表情从{emotion_words['base']}逐渐转为{emotion_words['rising']}。"
                f"眼神变得深邃有力，全身散发出强烈的武术气场。"
                f"双方你来我往，攻防转换如行云流水，"
                f"将中华武术的魅力展现得淋漓尽致。"
            )
        else:
            emotion_rise = (
                f"表情从{emotion_words['base']}逐渐转为{emotion_words['rising']}。"
                f"眼神变得深邃有力，嘴角微微上扬。"
                f"情感在胸中涌动，达到{emotion_words['peak']}的状态，"
                f"全身散发出强烈的情感气场。"
            )

        return emotion_rise

    def _generate_conclusion(self, scene: str, style: str, mild_mode: bool = False) -> str:
        """
        生成12-15秒的情感收尾

        Args:
            scene: 场景描述
            style: 风格
            mild_mode: 是否使用温和模式

        Returns:
            情感收尾描述
        """
        emotion = self._detect_emotion(scene)

        # 根据是否是温和模式选择情感关键词
        if emotion == "combat" and mild_mode:
            emotion_words = self.MILD_EMOTION_KEYWORDS.get(emotion, self.MILD_EMOTION_KEYWORDS.get("combat", {}))
        else:
            emotion_words = self.EMOTION_KEYWORDS.get(emotion, self.EMOTION_KEYWORDS["romantic"])

        # 情感舒缓或达到高潮
        if emotion == "combat" and mild_mode:
            # 温和版本的收尾
            conclusion = (
                f"最终，{emotion_words['soothing']}。"
                f"双方收招立定，相互行礼。"
                f"镜头缓缓后退，留下一个精彩的武术表演画面，"
                f"整个切磋在这一刻达到了艺术的境界。"
            )
        elif emotion == "combat":
            # 激烈版本的收尾
            conclusion = (
                f"最终，{emotion_words['soothing']}。"
                f"胜负已定，双方停止攻击，相对而立。"
                f"镜头缓缓后退，留下一个激烈的画面，"
                f"整个战斗在这一刻达到了完美的收尾。"
            )
        else:
            conclusion = (
                f"最终，情感渐渐{emotion_words['soothing']}。"
                f"主角脸上露出满足的表情，内心获得了平静与感悟。"
                f"镜头缓缓后退，留下一个美好的画面，"
                f"整个故事在这一刻达到了完美的收尾。"
            )

        return conclusion

    def get_template_by_type(self, video_type: str, difficulty: str) -> Optional[Dict]:
        """
        根据视频类型和难度获取模板

        Args:
            video_type: 视频类型
            difficulty: 难度级别

        Returns:
            模板字典，如果未找到则返回 None
        """
        templates = self.template_lib.get_templates_by_type_and_difficulty(video_type, difficulty)
        if templates:
            return templates[0]
        return None

    def interactive_prompt_generator(self):
        """交互式提示词生成器"""
        print("\n" + "=" * 80)
        print("🎬 Seedance 2.0 交互式提示词生成器")
        print("=" * 80 + "\n")

        # 选择视频类型
        print("请选择视频类型:")
        types = list(self.VIDEO_TYPES.keys())
        for i, (key, name) in enumerate(self.VIDEO_TYPES.items(), 1):
            print(f"  {i}. {name} ({key})")

        type_choice = input("\n请输入编号 (1-8, 默认1): ").strip() or "1"
        try:
            type_index = int(type_choice) - 1
            if 0 <= type_index < len(types):
                video_type = types[type_index]
            else:
                video_type = types[0]
        except ValueError:
            video_type = types[0]

        print(f"\n✓ 已选择: {self.VIDEO_TYPES.get(video_type, video_type)}")

        # 选择难度级别
        print("\n请选择难度级别:")
        levels = list(self.DIFFICULTY_LEVELS.keys())
        for i, (key, name) in enumerate(self.DIFFICULTY_LEVELS.items(), 1):
            print(f"  {i}. {name} ({key})")

        level_choice = input("\n请输入编号 (1-4, 默认2): ").strip() or "2"
        try:
            level_index = int(level_choice) - 1
            if 0 <= level_index < len(levels):
                difficulty = levels[level_index]
            else:
                difficulty = levels[1]
        except ValueError:
            difficulty = levels[1]

        print(f"\n✓ 已选择: {self.DIFFICULTY_LEVELS.get(difficulty, difficulty)}")

        # 输入场景描述
        print("\n请描述你想要的场景:")
        scene = input("> ").strip()
        if not scene:
            print("❌ 场景描述不能为空")
            return

        # 可选：输入风格
        style = input("\n请输入风格 (可选，按 Enter 跳过): ").strip() or None

        # 可选：输入时长
        duration = input("\n请输入时长 (可选，如 5-10s，按 Enter 跳过): ").strip() or None

        # 询问是否使用在线搜索
        online_search = False
        if self.online_search_enabled:
            print(f"\n是否使用在线搜索查找相关提示词? (需要网络连接)")
            online_choice = input("y/N: ").strip().lower()
            online_search = (online_choice == 'y')

        # 生成提示词
        print("\n" + "-" * 80)
        print("🚀 正在生成提示词...")
        if online_search:
            print("   (同时搜索在线提示词...)")
        print("-" * 80 + "\n")

        result = self.generate_prompt_with_search(
            scene=scene,
            style=style,
            duration=duration,
            difficulty=difficulty,
            video_type=video_type,
            online_search=online_search
        )

        # 显示结果
        self._display_result(result)

    def _display_result(self, result: Dict):
        """显示生成结果"""
        print("\n" + "=" * 80)
        print("📝 生成的提示词")
        print("=" * 80 + "\n")

        print(f"视频类型: {self.VIDEO_TYPES.get(result['video_type'], result['video_type'])}")
        print(f"难度级别: {self.DIFFICULTY_LEVELS.get(result['difficulty'], result['difficulty'])}")
        print(f"推荐时长: {result.get('recommended_duration', 'N/A')}")

        # 显示在线搜索状态
        if result.get('online_used'):
            print(f"在线搜索: ✓ 已使用 (找到 {len(result.get('online_results', []))} 个相关提示词)")
        else:
            print(f"在线搜索: ✗ 未使用")

        print()

        # 显示在线搜索建议
        if result.get('online_used') and result.get('online_results'):
            print("-" * 80)
            print("🌐 在线搜索结果:")
            print("-" * 80)
            for i, online_prompt in enumerate(result.get('online_results', [])[:2], 1):
                print(f"\n[{i}] {online_prompt.get('name', '未命名')}")
                print(f"    类型: {online_prompt.get('video_type', 'N/A')}")
                print(f"    难度: {online_prompt.get('difficulty', 'N/A')}")
                if online_prompt.get('prompt'):
                    print(f"    提示词: {online_prompt.get('prompt', '')[:100]}...")
            if len(result.get('online_results', [])) > 2:
                print(f"\n还有 {len(result.get('online_results', [])) - 2} 个结果未显示")
            print()

        print("-" * 80)
        print("完整提示词:")
        print("-" * 80)
        print(result['prompt'])
        print()

        if result.get('elements'):
            print("-" * 80)
            print("元素组成:")
            print("-" * 80)
            for key, value in result['elements'].items():
                if value and key != 'subject':  # 跳过主体，因为已经在场景中
                    print(f"  {key}: {value}")
            print()

        if result.get('variants'):
            print("-" * 80)
            print("提示词变体:")
            print("-" * 80)
            for i, variant in enumerate(result['variants'], 1):
                print(f"\n变体 {i}:")
                print(variant)
            print()

        if result.get('reference_template'):
            print("-" * 80)
            print(f"参考模板 ID: {result['reference_template']}")
            print("-" * 80 + "\n")

    def generate_high_quality_prompt(
        self,
        scene: str,
        reference_work: str = None,
        style_keywords: list = None,
        outfit_before: str = None,
        belt_design: str = None,
        final_costume: str = None,
        scene_setting: str = None,
        camera_movement: str = None,
        action_sequence: str = None,
        transformation_type: str = None,
        effects: str = None,
        ending: str = None,
        duration: str = "15s",
        include_timing: bool = True
    ) -> Dict:
        """
        生成高质量提示词（参考《假面骑士BLACK SUN》风格）

        核心特点：
        1. 风格定位极其精准（参考作品、风格关键词）
        2. 细节极其丰富（每个元素都有明确要求）
        3. 镜头语言极其专业（全程不切镜头）
        4. 变身过程极具科技感（暗红微光＋黑雾黑粒子）
        5. 氛围营造极佳（场景、天气、声音）
        6. 动作设计简洁有力
        7. 声音设计增强沉浸感

        Args:
            scene: 场景描述
            reference_work: 参考作品（如：《假面骑士BLACK SUN》）
            style_keywords: 风格关键词（如：写实暗黑、生物科技与外星科技感、压抑沉重）
            outfit_before: 变身前造型
            belt_design: 腰带设计
            final_costume: 最终战衣
            scene_setting: 场景设定
            camera_movement: 镜头运动
            action_sequence: 动作序列
            transformation_type: 变身类型
            effects: 特效
            ending: 结尾
            duration: 时长
            include_timing: 是否包含分秒设计

        Returns:
            包含生成结果的字典
        """
        result = {
            'prompt': '',
            'elements': {},
            'reference_work': reference_work or '未指定',
            'style_keywords': style_keywords or [],
            'timing_prompts': [],
            'duration': duration,
            'quality_level': 'HIGH_QUALITY'
        }

        # 构建完整的提示词
        prompt_parts = []

        # 1. 使用上传照片作为人物面部参考
        prompt_parts.append("使用上传照片作为人物面部参考，保持脸部完全一致，不改变五官和脸型，不美化。")

        # 2. 服装要求
        prompt_parts.append("服装不要原服装，需要符合视频要求的服装。")

        # 3. 风格参考
        if reference_work:
            prompt_parts.append(f"风格参考{reference_work}，")
        if style_keywords:
            prompt_parts.append(f"{', '.join(style_keywords)}。")

        # 4. 变身前造型
        if outfit_before:
            prompt_parts.append(f"变身前造型：{outfit_before}。")

        # 5. 腰带设计
        if belt_design:
            prompt_parts.append(f"腰带：{belt_design}。")

        # 6. 场景设定
        if scene_setting:
            prompt_parts.append(f"场景：{scene_setting}。")

        # 7. 镜头运动
        if camera_movement:
            prompt_parts.append(f"镜头：{camera_movement}。")

        # 8. 动作序列
        if action_sequence:
            prompt_parts.append(f"动作：{action_sequence}。")

        # 9. 变身类型
        if transformation_type:
            prompt_parts.append(f"变身：{transformation_type}。")

        # 10. 特效
        if effects:
            prompt_parts.append(f"特效：{effects}。")

        # 11. 最终战衣
        if final_costume:
            prompt_parts.append(f"最终战衣：{final_costume}。")

        # 12. 结尾
        if ending:
            prompt_parts.append(f"结尾：{ending}。")

        # 组合完整提示词
        result['prompt'] = ' '.join(prompt_parts)

        # 保存元素
        result['elements'] = {
            'reference_work': reference_work or '未指定',
            'style_keywords': style_keywords or [],
            'outfit_before': outfit_before or '未指定',
            'belt_design': belt_design or '未指定',
            'final_costume': final_costume or '未指定',
            'scene_setting': scene_setting or '未指定',
            'camera_movement': camera_movement or '未指定',
            'action_sequence': action_sequence or '未指定',
            'transformation_type': transformation_type or '未指定',
            'effects': effects or '未指定',
            'ending': ending or '未指定'
        }

        # 如果需要分秒设计，生成15秒的分秒提示词
        if include_timing and duration == "15s":
            result['timing_prompts'] = self._generate_high_quality_timing_prompts(result['elements'])

        return result

    def _generate_high_quality_timing_prompts(self, elements: Dict) -> list:
        """
        生成高质量的分秒提示词（15秒）

        Args:
            elements: 元素字典

        Returns:
            分秒提示词列表
        """
        timing_prompts = []

        # 0-2秒：开场（变身前状态）
        timing_prompts.append({
            'time': '0-2s',
            'camera': '中景定机位，约30度侧面开场，缓慢转正并轻推',
            'action': '低头',
            'scene': elements.get('scene_setting', '阴天户外空地'),
            'lighting': '灰蓝天空，有风'
        })

        # 2-5秒：能量聚集
        timing_prompts.append({
            'time': '2-5s',
            'camera': '中景到特写，缓慢推进',
            'action': '抬头',
            'scene': '场景中央',
            'lighting': '暗红微光开始出现'
        })

        # 5-8秒：变身开始
        timing_prompts.append({
            'time': '5-8s',
            'camera': '特写到环绕，缓慢环绕',
            'action': '右手放腰带',
            'scene': '能量聚集',
            'lighting': '暗红微光＋黑雾黑粒子环绕'
        })

        # 8-12秒：变身过程
        timing_prompts.append({
            'time': '8-12s',
            'camera': '环绕到广角，缓慢拉开',
            'action': '低声说咒语（如：KAMEN RIDER）',
            'scene': '身体微转定格',
            'lighting': '暗红微光＋黑雾黑粒子，身体微转定格，无拼装，无秒变'
        })

        # 12-15秒：变身完成
        timing_prompts.append({
            'time': '12-15s',
            'camera': '广角到远景，缓慢拉远',
            'action': '展示最终战衣',
            'scene': '变身完成',
            'lighting': '低角度正面定格3秒，风声，冷峻压抑'
        })

        return timing_prompts

    def display_high_quality_result(self, result: Dict):
        """显示高质量提示词生成结果"""
        print("\n" + "=" * 80)
        print("📝 高质量提示词（参考《假面骑士BLACK SUN》风格）")
        print("=" * 80 + "\n")

        print(f"参考作品: {result['reference_work']}")
        print(f"风格关键词: {', '.join(result['style_keywords'])}")
        print(f"时长: {result['duration']}")
        print(f"质量级别: {result['quality_level']}")

        print()
        print("-" * 80)
        print("完整提示词:")
        print("-" * 80)
        print(result['prompt'])
        print()

        if result.get('elements'):
            print("-" * 80)
            print("元素组成:")
            print("-" * 80)
            for key, value in result['elements'].items():
                print(f"  {key}: {value}")
            print()

        if result.get('timing_prompts'):
            print("-" * 80)
            print("分秒设计（15秒）:")
            print("-" * 80)
            for timing in result['timing_prompts']:
                print(f"\n【{timing['time']}】")
                print(f"  镜头: {timing['camera']}")
                print(f"  动作: {timing['action']}")
                print(f"  场景: {timing['scene']}")
                print(f"  光影: {timing['lighting']}")
            print()

        print("-" * 80)
        print("核心特点:")
        print("-" * 80)
        print("  1. 风格定位极其精准（参考作品、风格关键词）")
        print("  2. 细节极其丰富（每个元素都有明确要求）")
        print("  3. 镜头语言极其专业（全程不切镜头）")
        print("  4. 变身过程极具科技感（暗红微光＋黑雾黑粒子）")
        print("  5. 氛围营造极佳（场景、天气、声音）")
        print("  6. 动作设计简洁有力")
        print("  7. 声音设计增强沉浸感")
        print("-" * 80 + "\n")


# 便捷函数
def generate_prompt(
    scene: str,
    style: Optional[str] = None,
    duration: Optional[str] = None,
    difficulty: str = "INTERMEDIATE",
    video_type: str = "photo-realistic"
) -> Dict:
    """生成提示词的便捷函数"""
    generator = PromptGenerator()
    return generator.generate_prompt(
        scene=scene,
        style=style,
        duration=duration,
        difficulty=difficulty,
        video_type=video_type
    )


def get_template_by_type(video_type: str, difficulty: str) -> Optional[Dict]:
    """获取模板的便捷函数"""
    generator = PromptGenerator()
    return generator.get_template_by_type(video_type, difficulty)


if __name__ == "__main__":
    # 测试代码
    print("=== Seedance 2.0 提示词生成器 ===\n")

    # 示例1：生成提示词
    print("示例1: 生成提示词")
    print("-" * 80)
    result = generate_prompt(
        scene="一位年轻女性在花园里散步",
        style="梦幻",
        difficulty="INTERMEDIATE",
        video_type="photo-realistic"
    )
    generator = PromptGenerator()
    generator._display_result(result)

    # 示例2：交互式生成
    print("\n" + "=" * 80)
    print("是否启动交互式生成器? (y/N): ")
    choice = input().strip().lower()
    if choice == 'y':
        generator.interactive_prompt_generator()
