#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情报官 - 热点抓取脚本
抓取微博热搜、知乎热榜、百度热搜
"""

import sys
import os
sys.path.insert(0, r'C:\Users\Lenovo\AppData\Local\nvm\v22.22.0\node_modules\openclaw\skills\chrome-devtools')

from skills.chrome_devtools import navigate, evaluate, screenshot
import time
import json
from datetime import datetime

def crawl_weibo():
    """抓取微博热搜"""
    print("🔍 正在抓取微博热搜...")
    navigate('https://s.weibo.com/top/summary')
    time.sleep(4)
    
    result = evaluate('''
        Array.from(document.querySelectorAll('.hot-list li')).slice(0, 20).map(item => {
            const rank = item.querySelector('.txt-top')?.innerText?.trim() || '';
            const title = item.querySelector('a')?.innerText?.trim() || '';
            const hot = item.querySelector('.ico1')?.innerText?.trim() || '';
            return { rank, title, hot };
        }).filter(x => x.title)
    ''')
    
    print(f"✅ 微博热搜抓取完成：{len(result)} 条")
    return result

def crawl_zhihu():
    """抓取知乎热榜"""
    print("🔍 正在抓取知乎热榜...")
    navigate('https://www.zhihu.com/hot')
    time.sleep(4)
    
    result = evaluate('''
        Array.from(document.querySelectorAll('.HotList-list .HotItem')).slice(0, 20).map(item => {
            const rank = item.querySelector('.HotItem-rank')?.innerText?.trim() || '';
            const title = item.querySelector('.HotItem-title')?.innerText?.trim() || '';
            const hot = item.querySelector('.HotItem-metrics')?.innerText?.trim() || '';
            return { rank, title, hot };
        }).filter(x => x.title)
    ''')
    
    print(f"✅ 知乎热榜抓取完成：{len(result)} 条")
    return result

def crawl_baidu():
    """抓取百度热搜"""
    print("🔍 正在抓取百度热搜...")
    navigate('https://top.baidu.com/board?tab=realtime')
    time.sleep(4)
    
    result = evaluate('''
        Array.from(document.querySelectorAll('.category-wrap')).slice(0, 20).map(item => {
            const rank = item.querySelector('.index_2E9s4')?.innerText?.trim() || '';
            const title = item.querySelector('.title_dpy35')?.innerText?.trim() || '';
            const hot = item.querySelector('.hot_39MBT')?.innerText?.trim() || '';
            return { rank, title, hot };
        }).filter(x => x.title)
    ''')
    
    print(f"✅ 百度热搜抓取完成：{len(result)} 条")
    return result

def main():
    print("=" * 60)
    print("🔍 情报官 - 热点抓取任务")
    print(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 抓取三大平台
    weibo_data = crawl_weibo()
    time.sleep(2)
    zhihu_data = crawl_zhihu()
    time.sleep(2)
    baidu_data = crawl_baidu()
    
    # 输出结果
    output = {
        'timestamp': datetime.now().isoformat(),
        'weibo': weibo_data,
        'zhihu': zhihu_data,
        'baidu': baidu_data
    }
    
    # 保存到文件
    output_dir = r'D:\openclaw-data\.openclaw\workspace-intel-officer\memory'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f'trending-{datetime.now().strftime("%Y%m%d-%H%M")}.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 数据已保存：{output_file}")
    print("=" * 60)
    
    # 打印摘要
    print("\n📊 抓取摘要:")
    print(f"  微博热搜：{len(weibo_data)} 条")
    print(f"  知乎热榜：{len(zhihu_data)} 条")
    print(f"  百度热搜：{len(baidu_data)} 条")
    
    return output

if __name__ == '__main__':
    main()
