"""
AI Use Case Collector - Night Intel Round 8
Collects real AI applications from Xiaohongshu, Weibo, Zhihu, and web
"""

from skills.chrome_devtools import navigate, evaluate, screenshot
import json
from datetime import datetime

def collect_xiaohongshu_ai_cases():
    """Collect AI use cases from Xiaohongshu"""
    print("📕 Collecting from Xiaohongshu...")
    
    # Navigate to Xiaohongshu search
    navigate(url="https://www.xiaohongshu.com/search_result?keyword=AI 实际应用&source=web_search_result_notes")
    
    # Extract top posts
    script = """
    Array.from(document.querySelectorAll('.note-item')).slice(0, 10).map(item => ({
        title: item.querySelector('.title')?.innerText?.trim() || '',
        author: item.querySelector('.nickname')?.innerText?.trim() || '',
        likes: item.querySelector('.like-count')?.innerText?.trim() || '0',
        link: item.querySelector('a')?.href || ''
    })).filter(x => x.title && x.title.length > 0)
    """
    
    result = evaluate(script=script)
    return result.get('data', [])

def collect_weibo_ai_topics():
    """Collect AI-related topics from Weibo"""
    print("📱 Collecting from Weibo...")
    
    navigate(url="https://s.weibo.com/top/summary")
    
    script = """
    Array.from(document.querySelectorAll('.hot-list li')).slice(0, 20).map(li => ({
        rank: li.querySelector('.hot-index')?.innerText?.trim() || '',
        title: li.querySelector('.hot-title')?.innerText?.trim() || '',
        hot: li.querySelector('.hot-num')?.innerText?.trim() || '',
        isAI: (li.querySelector('.hot-title')?.innerText || '').toLowerCase().includes('ai') || 
              (li.querySelector('.hot-title')?.innerText || '').includes('人工智能')
    }))
    """
    
    result = evaluate(script=script)
    data = result.get('data', [])
    return [x for x in data if x.get('isAI') or x.get('rank')]

def collect_zhihu_ai_discussions():
    """Collect AI discussions from Zhihu"""
    print("📚 Collecting from Zhihu...")
    
    navigate(url="https://www.zhihu.com/search?q=AI 实际应用案例&type=content")
    
    script = """
    Array.from(document.querySelectorAll('.ContentItem')).slice(0, 10).map(item => ({
        title: item.querySelector('.ContentItem-title')?.innerText?.trim() || '',
        excerpt: item.querySelector('.RichText')?.innerText?.trim() || '',
        votes: item.querySelector('.VoteButton--up')?.innerText?.trim() || '0',
        author: item.querySelector('.UserLink-link')?.innerText?.trim() || ''
    })).filter(x => x.title && x.title.length > 5)
    """
    
    result = evaluate(script=script)
    return result.get('data', [])

def generate_report():
    """Generate comprehensive AI use case report"""
    print("🚀 Starting AI use case collection...\n")
    
    # Collect from all platforms
    xiaohongshu_data = collect_xiaohongshu_ai_cases()
    weibo_data = collect_weibo_ai_topics()
    zhihu_data = collect_zhihu_ai_discussions()
    
    # Take screenshot for evidence
    screenshot()
    
    report = {
        "collection_time": datetime.now().isoformat(),
        "platforms": {
            "xiaohongshu": xiaohongshu_data,
            "weibo": weibo_data,
            "zhihu": zhihu_data
        },
        "summary": {
            "xiaohongshu_count": len(xiaohongshu_data),
            "weibo_count": len(weibo_data),
            "zhihu_count": len(zhihu_data)
        }
    }
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print("\n✅ Collection complete!")
    print(json.dumps(report, ensure_ascii=False, indent=2))
