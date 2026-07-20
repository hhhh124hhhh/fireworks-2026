#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晨间深度情报扫描脚本
抓取百度热搜、微博热搜、知乎热榜
"""

import requests
import json
from datetime import datetime

# Chrome DevTools CDP 配置
CDP_BASE = "http://127.0.0.1:9222"

def get_tabs():
    """获取当前 Chrome 标签页"""
    try:
        resp = requests.get(f"{CDP_BASE}/json/list", timeout=5)
        return resp.json()
    except Exception as e:
        print(f"获取标签页失败：{e}")
        return []

def navigate_to(url):
    """导航到 URL"""
    tabs = get_tabs()
    if not tabs:
        print("没有可用的标签页")
        return None
    
    tab_id = tabs[0]['id']
    
    # 使用 CDP Runtime.evaluate 导航
    ws_url = tabs[0]['webSocketDebuggerUrl']
    
    # 简单 HTTP 方式导航（通过评估 JavaScript）
    navigate_script = f"""
    (async () => {{
        window.location.href = '{url}';
        return 'navigating';
    }})()
    """
    
    try:
        resp = requests.post(
            f"{CDP_BASE}/json/execute/{tab_id}",
            json={'script': navigate_script},
            timeout=10
        )
        return resp.json()
    except Exception as e:
        print(f"导航失败：{e}")
        return None

def fetch_baidu_hotsearch():
    """抓取百度热搜（通过搜索结果页）"""
    print("\n=== 抓取百度热搜 ===")
    
    # 直接访问百度热搜榜
    url = "https://top.baidu.com/board?tab=realtime"
    
    try:
        # 使用 requests 直接抓取（备用方案）
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        resp = requests.get(url, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            print(f"✓ 百度热搜页面抓取成功 ({len(resp.text)} bytes)")
            # 简单提取标题（实际需要更复杂的解析）
            return {'status': 'success', 'length': len(resp.text)}
        else:
            print(f"✗ 百度热搜抓取失败：HTTP {resp.status_code}")
            return {'status': 'failed', 'code': resp.status_code}
            
    except Exception as e:
        print(f"✗ 百度热搜抓取异常：{e}")
        return {'status': 'error', 'error': str(e)}

def fetch_weibo_hotsearch():
    """抓取微博热搜"""
    print("\n=== 抓取微博热搜 ===")
    
    url = "https://s.weibo.com/top/summary"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        resp = requests.get(url, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            print(f"✓ 微博热搜页面抓取成功 ({len(resp.text)} bytes)")
            return {'status': 'success', 'length': len(resp.text)}
        else:
            print(f"✗ 微博热搜抓取失败：HTTP {resp.status_code}")
            return {'status': 'failed', 'code': resp.status_code}
            
    except Exception as e:
        print(f"✗ 微博热搜抓取异常：{e}")
        return {'status': 'error', 'error': str(e)}

def fetch_zhihu_hotlist():
    """抓取知乎热榜"""
    print("\n=== 抓取知乎热榜 ===")
    
    url = "https://www.zhihu.com/hot"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': 'z_c0=dummy_cookie_for_demo',  # 实际应从 Chrome 获取真实 Cookie
        }
        resp = requests.get(url, headers=headers, timeout=15)
        
        if resp.status_code == 200:
            print(f"✓ 知乎热榜页面抓取成功 ({len(resp.text)} bytes)")
            return {'status': 'success', 'length': len(resp.text)}
        else:
            print(f"✗ 知乎热榜抓取失败：HTTP {resp.status_code}")
            return {'status': 'failed', 'code': resp.status_code}
            
    except Exception as e:
        print(f"✗ 知乎热榜抓取异常：{e}")
        return {'status': 'error', 'error': str(e)}

def main():
    print("=" * 60)
    print("[INTEL] 晨间深度情报扫描")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 检查 Chrome 连接
    print("\n[1/4] Checking Chrome connection...")
    try:
        version = requests.get(f"{CDP_BASE}/json/version", timeout=5).json()
        print(f"✓ Chrome 已连接：{version.get('Browser', 'Unknown')}")
    except Exception as e:
        print(f"✗ Chrome 连接失败：{e}")
        return
    
    # 抓取各平台热点
    print("\n[2/4] Fetching Baidu HotSearch...")
    baidu_result = fetch_baidu_hotsearch()
    
    print("\n[3/4] Fetching Weibo HotSearch...")
    weibo_result = fetch_weibo_hotsearch()
    
    print("\n[4/4] Fetching Zhihu HotList...")
    zhihu_result = fetch_zhihu_hotlist()
    
    # 输出结果汇总
    print("\n" + "=" * 60)
    print("[SUMMARY] Scan Results")
    print("=" * 60)
    print(f"Baidu:  {baidu_result['status']}")
    print(f"Weibo:  {weibo_result['status']}")
    print(f"Zhihu:  {zhihu_result['status']}")
    print("=" * 60)
    
    # 返回结果供后续处理
    return {
        'baidu': baidu_result,
        'weibo': weibo_result,
        'zhihu': zhihu_result,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    result = main()
    print(f"\n[COMPLETE] Deep scan finished")
    
    # 保存结果到 JSON 文件
    with open('./memory/deep-scan-result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[SAVED] Results saved to ./memory/deep-scan-result.json")
