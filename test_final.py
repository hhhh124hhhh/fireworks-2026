#!/usr/bin/env python3
"""最终验证百度 API 调用"""

import os
import sys
sys.path.insert(0, '/root/clawd/skills/ai-insights-generator/scripts')

from ai_insights_generator import MultiSourceSearcher

# 创建搜索器实例
searcher = MultiSourceSearcher('test-tavily-key')

# 测试环境变量
api_key = os.environ.get('BAIDU_API_KEY', '')
print(f"BAIDU_API_KEY 存在: {bool(api_key)}")

if not api_key:
    print("⚠️  未设置 BAIDU_API_KEY，跳过测试")
    exit(0)

# 测试百度搜索
print("\n测试百度搜索...")
results = searcher.search_baidu("AI agent", max_results=3)
print(f"\n返回结果数: {len(results)}")

if results:
    print("\n前3条结果:")
    for i, r in enumerate(results[:3], 1):
        print(f"  {i}. {r.get('title', 'N/A')[:50]}...")
else:
    print("⚠️  未获取到结果")

print("\n✅ 测试完成")
