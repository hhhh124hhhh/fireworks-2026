#!/usr/bin/env python
# encoding: utf-8
"""
热点去重模块
基于 SimHash 算法检测重复内容
"""

import hashlib
import re
from collections import defaultdict

# 中文停用词表（简化版）
STOP_WORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
    '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
    '你', '会', '着', '没有', '看', '好', '自己', '这'
}


def extract_keywords(text, max_keywords=20):
    """
    提取文本关键词
    简单实现：分词 + 去停用词 + 取前 N 个
    """
    # 转小写
    text = text.lower()
    
    # 移除 URL
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # 移除特殊字符
    text = re.sub(r'[^\w\s\u4e00-\u9fa5]', ' ', text)
    
    # 简单分词（按空格和中文标点）
    words = re.split(r'[\s，。！？；：、]+', text)
    
    # 去停用词和短词
    keywords = [w for w in words if w and len(w) > 1 and w not in STOP_WORDS]
    
    # 返回前 N 个
    return keywords[:max_keywords]


def simhash(text, hash_bits=64):
    """
    计算 SimHash 值
    返回 int 类型的 hash 值
    """
    keywords = extract_keywords(text)
    
    # 为每个关键词计算 hash
    hashes = defaultdict(int)
    
    for keyword in keywords:
        # 计算关键词的 hash
        h = int(hashlib.md5(keyword.encode('utf-8')).hexdigest(), 16)
        
        # 加权（关键词位置越靠前权重越高）
        weight = max(1, len(keywords) - keywords.index(keyword))
        
        # 更新每一位
        for i in range(hash_bits):
            bit = (h >> i) & 1
            hashes[i] += weight if bit else -weight
    
    # 生成最终 hash
    result = 0
    for i in range(hash_bits):
        if hashes[i] > 0:
            result |= (1 << i)
    
    return result


def hamming_distance(h1, h2, hash_bits=64):
    """
    计算海明距离
    """
    xor = h1 ^ h2
    distance = 0
    for i in range(hash_bits):
        if (xor >> i) & 1:
            distance += 1
    return distance


def dedup_hotspots(items, threshold=5):
    """
    基于 SimHash 去重
    
    Args:
        items: 热点列表，每项包含 'title' 字段
        threshold: 海明距离阈值，越小越严格（推荐 3-5）
    
    Returns:
        去重后的热点列表
    """
    if not items:
        return []
    
    deduped = []
    hash_map = {}  # hash -> item
    
    for item in items:
        title = item.get('title', '')
        if not title:
            continue
        
        # 计算 SimHash
        h = simhash(title)
        
        # 检查是否重复
        is_dup = False
        dup_of = None
        
        for existing_hash, existing_item in hash_map.items():
            dist = hamming_distance(h, existing_hash)
            
            if dist <= threshold:
                # 发现重复
                is_dup = True
                dup_of = existing_item
                
                # 保留优先级高的（P0 > P1 > P2）
                current_priority = get_priority_value(item.get('priority', 'P2'))
                existing_priority = get_priority_value(existing_item.get('priority', 'P2'))
                
                if current_priority > existing_priority:
                    # 新 item 优先级更高，替换
                    hash_map[existing_hash] = item
                    # 从 deduped 中移除旧的，添加新的
                    deduped = [i for i in deduped if i.get('title') != existing_item.get('title')]
                    deduped.append(item)
                
                break
        
        if not is_dup:
            hash_map[h] = item
            deduped.append(item)
    
    return deduped


def get_priority_value(priority):
    """
    获取优先级的数值（用于比较）
    P0=3, P1=2, P2=1
    """
    priority_map = {'P0': 3, 'P1': 2, 'P2': 1}
    return priority_map.get(priority, 0)


def cross_platform_dedup(platforms_data, threshold=5):
    """
    跨平台去重
    
    Args:
        platforms_data: dict，key 为平台名，value 为热点列表
        threshold: 海明距离阈值
    
    Returns:
        去重后的 platforms_data
    """
    # 收集所有热点
    all_items = []
    for platform, items in platforms_data.items():
        for item in items:
            item['_platform'] = platform
            all_items.append(item)
    
    # 去重
    deduped = dedup_hotspots(all_items, threshold)
    
    # 按平台重组
    result = defaultdict(list)
    for item in deduped:
        platform = item.pop('_platform', 'unknown')
        result[platform].append(item)
    
    return dict(result)


if __name__ == '__main__':
    # 测试
    test_items = [
        {'title': 'GPT-5 即将发布，性能提升 10 倍', 'priority': 'P0'},
        {'title': 'GPT5 即将发布 性能提升 10 倍', 'priority': 'P1'},  # 重复
        {'title': 'OpenAI 发布 GPT-5，性能大幅提升', 'priority': 'P1'},  # 相似
        {'title': 'Python 3.13 正式发布', 'priority': 'P0'},
        {'title': '小红书 AI 工具推荐', 'priority': 'P1'},
    ]
    
    print('原始数据:')
    for item in test_items:
        print(f"  - {item['title']}")
    
    deduped = dedup_hotspots(test_items, threshold=5)
    
    print(f'\n去重后 ({len(test_items)} → {len(deduped)}):')
    for item in deduped:
        print(f"  - {item['title']}")
