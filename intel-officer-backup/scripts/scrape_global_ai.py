#!/usr/bin/env python3
"""
Evening Global AI Intelligence Scraper
Scrapes Product Hunt, HackerNews, Reddit, Twitter for AI news
"""

import requests
import json
from datetime import datetime
from skills.chrome_devtools import navigate, evaluate, screenshot

def scrape_product_hunt():
    """Scrape Product Hunt AI/ML products"""
    print("📍 Product Hunt: AI/ML products...")
    navigate("https://www.producthunt.com/topics/artificial-intelligence")
    
    # Wait for page load
    import time
    time.sleep(3)
    
    # Extract top products
    products = evaluate("""
    () => {
        const items = document.querySelectorAll('[data-test="post-item"]');
        return Array.from(items.slice(0, 10)).map(item => {
            const title = item.querySelector('[data-test="post-title"]')?.textContent?.trim();
            const desc = item.querySelector('[data-test="post-tagline"]')?.textContent?.trim();
            const votes = item.querySelector('[aria-label="votes"]')?.textContent?.trim();
            const link = item.querySelector('a[href^="/posts/"]')?.href;
            return { title, desc, votes, link };
        }).filter(x => x.title);
    }
    """)
    return products

def scrape_hackernews():
    """Scrape Hacker News AI posts"""
    print("📍 Hacker News: AI posts...")
    navigate("https://news.ycombinator.com/front")
    
    import time
    time.sleep(2)
    
    # Extract AI-related posts
    posts = evaluate("""
    () => {
        const rows = document.querySelectorAll('.athing');
        return Array.from(rows.slice(0, 30)).map(row => {
            const titleElem = row.querySelector('.titleline > a');
            const title = titleElem?.textContent?.trim();
            const link = titleElem?.href;
            const score = document.querySelector(`#score_${row.id}`)?.textContent?.trim();
            // Check if AI-related
            const aiKeywords = ['AI', 'LLM', 'GPT', 'Claude', 'model', 'neural', 'machine learning', 'transformer'];
            const isAI = aiKeywords.some(k => title?.toLowerCase().includes(k.toLowerCase()));
            return { title, link, score, isAI };
        }).filter(x => x.title && x.isAI);
    }
    """)
    return posts

def scrape_reddit_ml():
    """Scrape Reddit r/MachineLearning"""
    print("📍 Reddit: r/MachineLearning...")
    navigate("https://www.reddit.com/r/MachineLearning/hot/")
    
    import time
    time.sleep(3)
    
    # Extract posts
    posts = evaluate("""
    () => {
        const posts = document.querySelectorAll('[data-adclicklocation="post_title"]');
        return Array.from(posts.slice(0, 15)).map(post => {
            const title = post.textContent?.trim();
            const link = post.href;
            const score = post.closest('shreddit-post')?.querySelector('[slot="vote-count"]')?.textContent?.trim();
            return { title, link, score };
        }).filter(x => x.title);
    }
    """)
    return posts

def main():
    results = {
        'timestamp': datetime.now().isoformat(),
        'product_hunt': [],
        'hackernews': [],
        'reddit': []
    }
    
    try:
        results['product_hunt'] = scrape_product_hunt()
    except Exception as e:
        print(f"Product Hunt error: {e}")
    
    import time
    time.sleep(2)
    
    try:
        results['hackernews'] = scrape_hackernews()
    except Exception as e:
        print(f"Hacker News error: {e}")
    
    time.sleep(2)
    
    try:
        results['reddit'] = scrape_reddit_ml()
    except Exception as e:
        print(f"Reddit error: {e}")
    
    # Save results
    with open('./memory/evening-global.md', 'w', encoding='utf-8') as f:
        f.write(f"# 🌍 Evening Global AI Intelligence\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')} (Asia/Shanghai)\n\n")
        f.write(f"---\n\n")
        
        f.write(f"## 🚀 Product Hunt - AI/ML\n\n")
        if results['product_hunt']:
            for i, p in enumerate(results['product_hunt'][:10], 1):
                f.write(f"{i}. **{p['title']}**\n")
                if p.get('desc'): f.write(f"   {p['desc']}\n")
                if p.get('votes'): f.write(f"   👍 {p['votes']}\n")
                if p.get('link'): f.write(f"   🔗 https://www.producthunt.com{p['link']}\n\n")
        else:
            f.write("*No data available*\n\n")
        
        f.write(f"---\n\n")
        
        f.write(f"## 📰 Hacker News - AI Posts\n\n")
        if results['hackernews']:
            for i, p in enumerate(results['hackernews'][:10], 1):
                f.write(f"{i}. **{p['title']}**\n")
                if p.get('score'): f.write(f"   ⬆️ {p['score']}\n")
                if p.get('link'): f.write(f"   🔗 {p['link']}\n\n")
        else:
            f.write("*No AI-related posts found*\n\n")
        
        f.write(f"---\n\n")
        
        f.write(f"## 🤖 Reddit r/MachineLearning\n\n")
        if results['reddit']:
            for i, p in enumerate(results['reddit'][:10], 1):
                f.write(f"{i}. **{p['title']}**\n")
                if p.get('score'): f.write(f"   ⬆️ {p['score']}\n")
                if p.get('link'): f.write(f"   🔗 {p['link']}\n\n")
        else:
            f.write("*No data available*\n\n")
    
    print(f"\n✅ Saved to ./memory/evening-global.md")
    print(f"📊 Product Hunt: {len(results['product_hunt'])} products")
    print(f"📊 Hacker News: {len(results['hackernews'])} AI posts")
    print(f"📊 Reddit: {len(results['reddit'])} posts")

if __name__ == '__main__':
    main()
