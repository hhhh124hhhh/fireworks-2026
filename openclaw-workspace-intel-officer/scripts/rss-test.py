#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 抓取脚本 - 快速测试版
只测试可访问的源
"""

import feedparser
import json
from datetime import datetime
from pathlib import Path

# 已验证可访问的源 (2026-03-18 测试)
TESTED_FEEDS = {
    "openai": "https://openai.com/news/rss.xml",
    "techcrunch": "https://techcrunch.com/feed/",
    "mit_tech_review": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "hacker_news": "https://hnrss.org/frontpage",
    "qbitai": "https://www.qbitai.com/feed",
}

OUTPUT_DIR = Path(__file__).parent / "memory"
OUTPUT_DIR.mkdir(exist_ok=True)

def fetch_and_save():
    all_entries = []
    
    print("=" * 60)
    print("RSS 抓取测试 - 已验证源")
    print("=" * 60)
    
    for source, url in TESTED_FEEDS.items():
        print(f"\n[{source}] {url}")
        try:
            feed = feedparser.parse(url, request_headers={
                'User-Agent': 'Mozilla/5.0 (Intel Officer RSS Grabber/1.0)'
            })
            
            if feed.bozo:
                print(f"  [WARN] {feed.bozo_exception}")
            
            print(f"  [OK] {len(feed.entries)} 条")
            
            for entry in feed.entries[:3]:
                record = {
                    "source": source,
                    "title": entry.title[:100] if entry.title else "N/A",
                    "link": entry.link[:200] if entry.link else "",
                    "published": entry.get('published', ''),
                    "summary": entry.get('summary', '')[:200],
                }
                all_entries.append(record)
                print(f"    - {record['title'][:60]}...")
                
        except Exception as e:
            print(f"  [ERROR] {e}")
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # JSON
    json_path = OUTPUT_DIR / f"rss-test-{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"\n[SAVE] {json_path}")
    
    # 摘要
    print(f"\n总计：{len(all_entries)} 条")
    by_source = {}
    for e in all_entries:
        by_source[e['source']] = by_source.get(e['source'], 0) + 1
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"  {source}: {count} 条")
    
    return all_entries

if __name__ == "__main__":
    fetch_and_save()
