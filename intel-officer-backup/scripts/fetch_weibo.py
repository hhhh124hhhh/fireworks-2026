#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""微博热搜采集脚本"""
import sys
import os
sys.path.insert(0, r'C:\Users\Lenovo\AppData\Local\nvm\v22.22.0\node_modules\openclaw\skills\chrome-devtools')

from chrome_devtools import navigate, evaluate, screenshot
import time
import json

def fetch_weibo_hot_search():
    """采集微博热搜前 20 条"""
    try:
        # 导航到微博热搜
        navigate(url='https://s.weibo.com/top/summary')
        time.sleep(3)
        
        # 提取热搜列表
        result = evaluate(script='''
            const items = document.querySelectorAll("td.td-02");
            const hotSearch = [];
            items.forEach((item, index) => {
                const a = item.querySelector("a");
                if (a) {
                    hotSearch.push({
                        rank: index + 1,
                        title: a.textContent.trim(),
                        hot: item.nextElementSibling?.textContent?.trim() || ""
                    });
                }
            });
            return JSON.stringify(hotSearch.slice(0, 20));
        ''')
        
        data = json.loads(result)
        print("=== 微博热搜 Top20 ===")
        for item in data:
            print(f"{item['rank']:2d}. {item['title']} [{item['hot']}]")
        
        return data
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == '__main__':
    fetch_weibo_hot_search()
