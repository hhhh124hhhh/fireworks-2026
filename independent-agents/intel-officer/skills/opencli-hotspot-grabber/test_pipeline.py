#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""管道模块快速测试"""

import sys
sys.path.insert(0, 'skills/opencli-hotspot-grabber')

from pipeline import AIFilter, QualityScorer

# 测试 AI 筛选
filter = AIFilter()
test_titles = [
    'GPT-5 即将发布，性能提升 10 倍',
    '油价临时调控 13 年来首次',
    'Cursor 用户破 100 万',
    '郑钦文迈阿密站止步',
    '5 个步骤学会 AI 编程',
    'AI Agent 实战：3 个技巧提升效率',
    '中国 AI 产业发展报告 2026',
    '新手用 AI 最常见的 5 个坑'
]

print('🔍 AI 筛选测试:\n')
for title in test_titles:
    is_ai, matched = filter.is_ai_related(title)
    status = '✅' if is_ai else '❌'
    print(f'{status} {title}')
    if matched:
        print(f'   匹配关键词：{matched}')
    print()

# 测试质量评分
scorer = QualityScorer()
print('\n📊 质量评分测试:\n')
for title in test_titles:
    score, pos, neg = scorer.score(title)
    if pos or neg:
        print(f'{title}')
        print(f'   评分：{score}')
        if pos:
            print(f'   正面：{pos}')
        if neg:
            print(f'   负面：{neg}')
        print()

print('\n✅ 测试完成!')
