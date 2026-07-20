#!/usr/bin/env python3
"""
使用已有数据测试推送流程
"""
import json
import sys
from pathlib import Path

# 读取已有的X数据
x_data_file = Path("/root/clawd/data/x-scraping/prompts-20260129.jsonl")

if not x_data_file.exists():
    print("错误：找不到X数据文件")
    sys.exit(1)

try:
    with open(x_data_file, 'r') as f:
        data = json.load(f)
    
    print(f"✓ 成功加载X数据")
    print(f"  查询: {data.get('query', 'N/A')}")
    print(f"  推文总数: {data.get('total_tweets', 0)}")
    
    tweets = data.get('tweets', [])
    print(f"  推文列表长度: {len(tweets)}")
    
    # 找出高价值推文（点赞>10 或有特定关键词）
    high_value_tweets = []
    keywords = ['AI', 'prompt', 'slide', 'PowerPoint', '生成', '自动化']
    
    for tweet in tweets:
        text = tweet.get('text', '')
        metrics = tweet.get('metrics', {})
        likes = metrics.get('likes', 0)
        
        # 高价值判断：高互动 或 包含关键词
        if likes > 10 or any(keyword.lower() in text.lower() for keyword in keywords):
            high_value_tweets.append(tweet)
    
    print(f"\n✓ 找到 {len(high_value_tweets)} 条高价值推文")
    
    # 保存为harvester可用的格式
    output_file = Path("/root/clawd/automation/x-prompts-harvester/existing_prompts.jsonl")
    with open(output_file, 'w', encoding='utf-8') as f:
        for tweet in high_value_tweets:
            prompt_data = {
                "text": tweet.get('text', ''),
                "url": tweet.get('url', ''),
                "author": tweet.get('author', {}).get('username', ''),
                "metrics": tweet.get('metrics', {}),
                "created_at": tweet.get('created_at', '')
            }
            f.write(json.dumps(prompt_data, ensure_ascii=False) + '\n')
    
    print(f"\n✓ 已保存到: {output_file}")
    print(f"  可以用这些数据测试评估→转换→发布流程")
    
except json.JSONDecodeError as e:
    print(f"错误：JSON解析失败 - {e}")
    print("尝试只读取前部分数据...")
    with open(x_data_file, 'r') as f:
        content = f.read()
        print(f"文件大小: {len(content)} 字符")
        # 看看是不是多个JSON对象
        if content.strip().startswith('{') and content.count('{"query":') > 1:
            print("检测到多个JSON对象，尝试分割...")
except Exception as e:
    print(f"错误：{e}")
    import traceback
    traceback.print_exc()
