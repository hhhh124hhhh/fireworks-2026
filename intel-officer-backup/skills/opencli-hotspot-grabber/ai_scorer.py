#!/usr/bin/env python
# encoding: utf-8
"""
AI 相关性评分模块
自动识别 AI 相关内容并评分
"""

# AI 关键词库（按类别分组）
AI_KEYWORDS = {
    # 核心 AI 术语
    'core': [
        'AI', '人工智能', 'LLM', '大模型', 'GPT', 'Claude', 'Gemini',
        'Agent', '智能体', '多模态', 'AIGC', '生成式 AI',
        'Machine Learning', 'Deep Learning', 'NLP', 'CV', '强化学习',
        'Transformer', 'Diffusion', 'MoE', 'RAG'
    ],
    # 公司和产品
    'products': [
        'OpenAI', 'Anthropic', 'Google DeepMind', 'Meta AI', 'Microsoft AI',
        'ChatGPT', 'Copilot', 'Midjourney', 'Stable Diffusion', 'DALL-E',
        'Sora', 'Runway', 'Character.ai', 'Hugging Face',
        '文心一言', '通义千问', 'Kimi', '智谱 AI', '月之暗面', 'MiniMax'
    ],
    # 技术和应用
    'tech': [
        '对话', '问答', '写作', '绘图', '视频生成', '代码生成',
        '自动驾驶', '机器人', '智能助手', '语音识别', '图像识别',
        '推荐系统', '搜索', '翻译', '摘要', '分类'
    ],
    # 热门话题
    'trending': [
        'AGI', '通用人工智能', '奇点', 'AI 安全', 'AI 监管',
        '失业', '替代', '赋能', '提效', 'AI 编程', 'AI 写作'
    ]
}

# 关键词权重
KEYWORD_WEIGHTS = {
    'core': 1.0,
    'products': 0.8,
    'tech': 0.6,
    'trending': 0.7
}


def score_ai_relevance(item):
    """
    计算 AI 相关性评分 (0-1)
    
    Args:
        item: 热点数据，包含 'title' 和可选的 'description'
    
    Returns:
        float: AI 相关性评分 (0-1)
    """
    text = (item.get('title', '') + ' ' + item.get('description', '')).lower()
    
    if not text.strip():
        return 0.0
    
    # 关键词匹配得分
    match_score = 0.0
    matched_keywords = []
    
    for category, keywords in AI_KEYWORDS.items():
        weight = KEYWORD_WEIGHTS.get(category, 0.5)
        
        for keyword in keywords:
            if keyword.lower() in text:
                match_score += weight
                matched_keywords.append(keyword)
    
    # 归一化（最多 5 个关键词）
    normalized_score = min(match_score / 5, 1.0)
    
    # 标题中包含 AI 关键词的额外加分
    title = item.get('title', '').lower()
    if any(kw.lower() in title for kw in AI_KEYWORDS['core']):
        normalized_score = min(normalized_score + 0.2, 1.0)
    
    # 记录匹配的关键词
    item['_ai_keywords'] = list(set(matched_keywords))
    item['_ai_score'] = normalized_score
    
    return normalized_score


def is_ai_related(item, threshold=0.3):
    """
    判断是否为 AI 相关内容
    
    Args:
        item: 热点数据
        threshold: 评分阈值
    
    Returns:
        bool: 是否为 AI 相关
    """
    return score_ai_relevance(item) >= threshold


def enhance_with_ai_score(items):
    """
    为热点列表添加 AI 评分和标签
    
    Args:
        items: 热点列表
    
    Returns:
        增强后的热点列表
    """
    enhanced = []
    
    for item in items:
        score = score_ai_relevance(item)
        item['ai_score'] = score
        item['is_ai_related'] = score >= 0.3
        
        # 根据 AI 评分调整优先级
        if score >= 0.7:
            # 强 AI 相关，提升优先级
            if item.get('priority') == 'P1':
                item['priority'] = 'P0'
            elif item.get('priority') == 'P2':
                item['priority'] = 'P1'
        
        enhanced.append(item)
    
    return enhanced


def filter_ai_related(items, min_score=0.3):
    """
    筛选 AI 相关内容
    
    Args:
        items: 热点列表
        min_score: 最低 AI 评分
    
    Returns:
        AI 相关的热点列表
    """
    return [item for item in items if score_ai_relevance(item) >= min_score]


def get_ai_summary(items):
    """
    获取 AI 相关内容摘要
    
    Args:
        items: 热点列表
    
    Returns:
        dict: AI 相关统计
    """
    ai_items = [item for item in items if item.get('is_ai_related', False)]
    
    # 按类别统计
    category_stats = {}
    for item in ai_items:
        for kw in item.get('_ai_keywords', []):
            # 判断关键词类别
            for category, keywords in AI_KEYWORDS.items():
                if kw in keywords:
                    category_stats[category] = category_stats.get(category, 0) + 1
                    break
    
    return {
        'total': len(items),
        'ai_related': len(ai_items),
        'ai_percentage': round(len(ai_items) / len(items) * 100, 1) if items else 0,
        'avg_ai_score': round(sum(i.get('_ai_score', 0) for i in ai_items) / len(ai_items), 2) if ai_items else 0,
        'category_distribution': category_stats,
        'top_keywords': get_top_keywords(ai_items)
    }


def get_top_keywords(items, top_n=10):
    """
    获取最常见的 AI 关键词
    
    Args:
        items: AI 相关的热点列表
        top_n: 返回前 N 个
    
    Returns:
        list: 关键词列表
    """
    keyword_count = {}
    
    for item in items:
        for kw in item.get('_ai_keywords', []):
            keyword_count[kw] = keyword_count.get(kw, 0) + 1
    
    # 排序
    sorted_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)
    
    return [{'keyword': kw, 'count': count} for kw, count in sorted_keywords[:top_n]]


if __name__ == '__main__':
    # 测试
    test_items = [
        {'title': 'GPT-5 即将发布，性能提升 10 倍', 'description': 'OpenAI 新一代模型'},
        {'title': 'Python 3.13 正式发布', 'description': '新增多个特性'},
        {'title': 'Sora 竞品分析：10 款 AI 视频生成工具对比', 'description': ''},
        {'title': '小红书 AI 工具推荐', 'description': '提升效率的 10 个工具'},
        {'title': '今天天气不错', 'description': ''},
    ]
    
    print('AI 相关性评分测试:\n')
    
    for item in test_items:
        score = score_ai_relevance(item)
        is_ai = is_ai_related(item)
        keywords = item.get('_ai_keywords', [])
        
        print(f"标题：{item['title']}")
        print(f"  AI 评分：{score:.2f}")
        print(f"  AI 相关：{'是' if is_ai else '否'}")
        print(f"  匹配关键词：{', '.join(keywords) if keywords else '无'}")
        print()
