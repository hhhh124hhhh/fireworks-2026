"""
Video Prompt Templates - 风格模板系统

提供多种视频风格的提示词模板和增强技巧
"""

import random
from typing import Dict, List, Optional

# ====== 视频风格模板 ======

VIDEO_STYLES: Dict[str, Dict] = {
    "landscape": {
        "name": "风景风光",
        "name_en": "Landscape & Scenery",
        "description": "自然风景、城市风光、季节变化",
        "keywords": [
            "natural scenery", "mountains", "ocean", "forest", "sunset", "skyline",
            "urban cityscape", "countryside", "waterfall", "snow landscape",
            "自然风景", "山川", "海洋", "森林", "日落", "城市天际线",
            "田园风光", "瀑布", "雪景", "季节变化"
        ],
        "enhancements": {
            "lighting": ["golden hour", "sunrise", "sunset", "diffused light", "natural light"],
            "composition": ["wide angle", "panoramic", "aerial view", "landscape orientation"],
            "mood": ["serene", "majestic", "peaceful", "breathtaking", "epic"],
            "technical": ["4K", "8K", "hyper-detailed", "slow motion", "time-lapse"]
        }
    },
    "product": {
        "name": "产品展示",
        "name_en": "Product Showcase",
        "description": "产品特写、使用场景、电商广告",
        "keywords": [
            "product close-up", "360 degree rotation", "product demonstration",
            "lifestyle shot", "e-commerce", "commercial",
            "产品特写", "360度展示", "产品演示", "生活场景", "电商广告", "商业"
        ],
        "enhancements": {
            "lighting": ["studio lighting", "soft box lighting", "ring light", "professional lighting"],
            "composition": ["close-up", "macro shot", "isometric view", "white background"],
            "mood": ["professional", "clean", "elegant", "trustworthy", "premium"],
            "technical": ["4K", "sharp focus", "depth of field", "smooth camera movement"]
        }
    },
    "tech": {
        "name": "科技未来",
        "name_en": "Tech & Future",
        "description": "赛博朋克、未来城市、AI 主题",
        "keywords": [
            "cyberpunk", "futuristic city", "AI technology", "neon lights",
            "hologram", "digital interface", "tech innovation", "robotics",
            "赛博朋克", "未来城市", "AI技术", "霓虹灯", "全息投影",
            "数字界面", "科技创新", "机器人"
        ],
        "enhancements": {
            "lighting": ["neon lights", "cyberpunk colors", "blue and purple", "glowing", "dynamic lighting"],
            "composition": ["dynamic camera", "futuristic perspective", "digital overlay", "HUD elements"],
            "mood": ["futuristic", "innovative", "cutting-edge", "sleek", "high-tech"],
            "technical": ["4K", "digital effects", "particle effects", "motion graphics"]
        }
    },
    "emotional": {
        "name": "情感故事",
        "name_en": "Emotional Story",
        "description": "浪漫、怀旧、励志、感人",
        "keywords": [
            "romantic", "nostalgic", "inspirational", "heartwarming",
            "love story", "memory", "hope", "touching moments",
            "浪漫", "怀旧", "励志", "感人", "爱情故事", "回忆",
            "希望", "感人瞬间"
        ],
        "enhancements": {
            "lighting": ["warm lighting", "soft candlelight", "dramatic shadows", "cinematic lighting"],
            "composition": ["close-up emotions", "eye-level shot", "intimate framing", "shallow depth of field"],
            "mood": ["emotional", "touching", "nostalgic", "heartwarming", "inspiring"],
            "technical": ["cinematic", "slow motion", "film grain", "color grading"]
        }
    },
    "urban": {
        "name": "都市生活",
        "name_en": "Urban Life",
        "description": "街头、办公、咖啡店、都市夜景",
        "keywords": [
            "street photography", "office life", "cafe scene", "city night",
            "urban lifestyle", "modern architecture", "busy streets",
            "街头摄影", "办公生活", "咖啡店场景", "城市夜景",
            "都市生活", "现代建筑", "繁忙街道"
        ],
        "enhancements": {
            "lighting": ["city lights", "neon signs", "street lamps", "indoor lighting", "natural daylight"],
            "composition": ["street level view", "candid moments", "urban architecture", "lifestyle framing"],
            "mood": ["modern", "dynamic", "energetic", "authentic", "urban"],
            "technical": ["4K", "handheld camera", "natural movement", "documentary style"]
        }
    },
    "food": {
        "name": "美食烹饪",
        "name_en": "Food & Cooking",
        "description": "食物拍摄、烹饪过程、美食特写",
        "keywords": [
            "food photography", "cooking process", "delicious dish",
            "ingredients", "steaming food", "gourmet meal", "appetizing",
            "美食摄影", "烹饪过程", "美味佳肴", "食材", "热气腾腾",
            "美食", "诱人"
        ],
        "enhancements": {
            "lighting": ["appetizing lighting", "backlight for steam", "soft diffuse light", "warm food lighting"],
            "composition": ["close-up details", "overhead view", "45-degree angle", "plating showcase"],
            "mood": ["appetizing", "delicious", "mouth-watering", "cozy", "gourmet"],
            "technical": ["4K", "macro shots", "slow motion cooking", "steam effects"]
        }
    },
    "sports": {
        "name": "运动健身",
        "name_en": "Sports & Fitness",
        "description": "运动场景、健身日常、体育赛事",
        "keywords": [
            "sports action", "fitness training", "gym workout",
            "outdoor activities", "team sports", "athlete", "exercise",
            "运动动作", "健身训练", "健身房锻炼", "户外活动",
            "团队运动", "运动员", "运动"
        ],
        "enhancements": {
            "lighting": ["dynamic lighting", "stadium lights", "outdoor natural light", "action lighting"],
            "composition": ["action shots", "wide angle", "freeze frame", "motion blur"],
            "mood": ["energetic", "powerful", "dynamic", "inspiring", "competitive"],
            "technical": ["4K", "slow motion", "fast shutter", "action camera"]
        }
    },
    "traditional": {
        "name": "古风传统",
        "name_en": "Traditional Chinese",
        "description": "中国风、汉服、古装、古建筑",
        "keywords": [
            "Chinese traditional", "Hanfu", "ancient architecture",
            "classical scenery", "cultural heritage", "Chinese art",
            "中国风", "汉服", "古装", "古建筑", "古典风景",
            "文化遗产", "中国画风格"
        ],
        "enhancements": {
            "lighting": ["soft natural light", "candlelight", "lantern light", "golden hour"],
            "composition": ["classical framing", "symmetrical composition", "traditional perspective", "negative space"],
            "mood": ["elegant", "timeless", "cultured", "poetic", "graceful"],
            "technical": ["4K", "soft colors", "traditional aesthetics", "film-like quality"]
        }
    },
    "anime": {
        "name": "动漫二次",
        "name_en": "Anime & 2D Style",
        "description": "动漫风格、Q版、二次元",
        "keywords": [
            "anime style", "2D animation", "chibi", "manga",
            "Japanese animation", "colorful", "cute characters",
            "动漫风格", "二次元", "Q版", "漫画风格", "日式动画",
            "色彩丰富", "可爱角色"
        ],
        "enhancements": {
            "lighting": ["vibrant colors", "soft anime lighting", "glowing effects", "pastel tones"],
            "composition": ["dynamic poses", "character close-ups", "expressive angles", "anime framing"],
            "mood": ["energetic", "cute", "playful", "dreamy", "expressive"],
            "technical": ["2D style", "cel-shaded", "vibrant colors", "animated quality"]
        }
    },
    "abstract": {
        "name": "抽象艺术",
        "name_en": "Abstract Art",
        "description": "抽象、艺术、创意、实验性",
        "keywords": [
            "abstract art", "creative visuals", "experimental",
            "artistic expression", "unique perspectives", "surreal",
            "抽象艺术", "创意视觉", "实验性", "艺术表达",
            "独特视角", "超现实主义"
        ],
        "enhancements": {
            "lighting": ["dramatic lighting", "colored lighting", "silhouette", "experimental light"],
            "composition": ["abstract composition", "unconventional angles", "negative space", "geometric patterns"],
            "mood": ["artistic", "creative", "mysterious", "thought-provoking", "experimental"],
            "technical": ["4K", "color manipulation", "texture effects", "visual experiments"]
        }
    }
}

# ====== 提示词增强词库 ======

ENHANCEMENTS = {
    "lighting": {
        "golden hour": "黄金时刻的温暖光线",
        "soft lighting": "柔和的散射光",
        "dramatic shadows": "戏剧性的阴影",
        "neon lights": "霓虹灯光",
        "studio lighting": "专业影棚灯光",
        "natural light": "自然光",
        "sunrise": "日出",
        "sunset": "日落",
        "diffused light": "漫射光",
        "backlighting": "逆光",
        "rim light": "轮廓光",
        "ambient light": "环境光"
    },
    "composition": {
        "wide angle": "广角镜头",
        "close-up": "特写镜头",
        "aerial view": "鸟瞰视角",
        "rule of thirds": "三分法构图",
        "low angle": "低角度",
        "high angle": "高角度",
        "dutch angle": "荷兰角",
        "pan shot": "摇镜头",
        "tilt shot": "俯仰镜头",
        "tracking shot": "跟拍镜头",
        "360 degree": "360度全景",
        "macro shot": "微距拍摄"
    },
    "atmosphere": {
        "cinematic": "电影质感",
        "dreamy": "梦幻",
        "energetic": "充满活力",
        "mysterious": "神秘",
        "romantic": "浪漫",
        "nostalgic": "怀旧",
        "peaceful": "宁静",
        "dramatic": "戏剧性",
        "ethereal": "空灵",
        "urban": "都市感",
        "cozy": "温馨",
        "intense": "激烈"
    },
    "technical": {
        "4K": "4K超高清",
        "8K": "8K超高清",
        "slow motion": "慢动作",
        "time-lapse": "延时摄影",
        "hyper-detailed": "超精细细节",
        "film grain": "胶片颗粒",
        "shallow DOF": "浅景深",
        "bokeh": "背景虚化",
        "motion blur": "运动模糊",
        "color grading": "色彩分级"
    }
}

# ====== 工具函数 ======

def get_style(style_name: str) -> Optional[Dict]:
    """
    获取风格配置

    Args:
        style_name: 风格名称或标识

    Returns:
        风格配置字典，不存在则返回 None
    """
    # 模糊匹配
    for key, style in VIDEO_STYLES.items():
        if style_name.lower() in [key.lower(), style["name"].lower(), style["name_en"].lower()]:
            return style

    # 如果找不到，返回默认风格
    return VIDEO_STYLES.get(style_name.lower())

def get_all_styles() -> List[str]:
    """
    获取所有风格标识

    Returns:
        风格标识列表
    """
    return list(VIDEO_STYLES.keys())

def get_random_enhancement(category: str, count: int = 2) -> List[str]:
    """
    随机选择增强元素

    Args:
        category: 增强类别 (lighting, composition, atmosphere, technical)
        count: 选择数量

    Returns:
        选择的增强元素列表
    """
    if category not in ENHANCEMENTS:
        return []

    options = list(ENHANCEMENTS[category].keys())
    count = min(count, len(options))
    return random.sample(options, count)

def generate_prompt_enhancement(
    base_prompt: str,
    style: Dict,
    enhance: bool = True,
    language: str = "auto"
) -> str:
    """
    生成增强的提示词

    Args:
        base_prompt: 基础提示词
        style: 风格配置
        enhance: 是否增强提示词
        language: 语言 (en, zh, auto)

    Returns:
        增强后的提示词
    """
    if not enhance:
        return base_prompt

    # 获取风格特定的增强词
    style_enhancements = style.get("enhancements", {})

    # 随机选择各类增强词
    lighting = random.sample(style_enhancements.get("lighting", ["soft lighting"]), 1)[0]
    composition = random.sample(style_enhancements.get("composition", ["wide angle"]), 1)[0]
    mood = random.sample(style_enhancements.get("mood", ["cinematic"]), 1)[0]
    technical = random.sample(style_enhancements.get("technical", ["4K"]), 1)[0]

    # 构建增强提示词
    enhanced = f"{base_prompt}, {lighting}, {composition}, {mood}, {technical}"

    return enhanced

def generate_prompt_from_keywords(
    keywords: List[str],
    style: Optional[Dict] = None,
    enhance: bool = True
) -> str:
    """
    从关键词生成提示词

    Args:
        keywords: 关键词列表
        style: 风格配置（可选）
        enhance: 是否增强

    Returns:
        生成的提示词
    """
    base = ", ".join(keywords)

    if style:
        return generate_prompt_enhancement(base, style, enhance)

    return base

def generate_prompt_variants(
    topic: str,
    style: Dict,
    count: int = 3,
    enhance: bool = True
) -> List[str]:
    """
    生成多个提示词变体

    Args:
        topic: 主题
        style: 风格配置
        count: 生成数量
        enhance: 是否增强

    Returns:
        提示词列表
    """
    variants = []

    for _ in range(count):
        # 随机选择一些关键词
        style_keywords = style["keywords"]
        selected_keywords = random.sample(style_keywords, min(3, len(style_keywords)))

        # 构建基础提示词
        base_parts = [topic] + selected_keywords
        base_prompt = ", ".join(base_parts)

        # 增强提示词
        if enhance:
            enhanced_prompt = generate_prompt_enhancement(base_prompt, style, enhance)
            variants.append(enhanced_prompt)
        else:
            variants.append(base_prompt)

    return variants

def format_prompt_output(
    prompts: List[str],
    style: Dict,
    format_type: str = "readable"
) -> str:
    """
    格式化输出提示词

    Args:
        prompts: 提示词列表
        style: 风格配置
        format_type: 输出格式 (readable, json, markdown)

    Returns:
        格式化后的字符串
    """
    if format_type == "json":
        import json
        return json.dumps({
            "style": style["name"],
            "style_en": style["name_en"],
            "prompts": prompts
        }, ensure_ascii=False, indent=2)

    elif format_type == "markdown":
        output = f"# {style['name']} ({style['name_en']})\n\n"
        output += f"**描述**: {style['description']}\n\n"
        output += "## 生成的提示词\n\n"

        for i, prompt in enumerate(prompts, 1):
            output += f"### 提示词 {i}\n\n"
            output += f"```\n{prompt}\n```\n\n"

        return output

    else:  # readable
        output = f"\n🎨 风格: {style['name']} ({style['name_en']})\n"
        output += f"📝 描述: {style['description']}\n"
        output += f"{'='*60}\n\n"

        for i, prompt in enumerate(prompts, 1):
            output += f"✨ 提示词 {i}:\n"
            output += f"   {prompt}\n\n"

        return output
