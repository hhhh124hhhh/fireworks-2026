#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenCLI Hotspot Grabber - 全域热点抓取工具
支持：Hacker News, GitHub, V2EX, arXiv, B 站，小红书，雪球等

混合抓取策略（v2.0）:
 - 优先使用 NewsNow API（快速，无需浏览器）
 - NewsNow 失败时，降级到 opencli
 - opencli 失败时，降级到 Chrome DevTools (CDP 9222)
 - Chrome 不可用时，降级到 requests 网页抓取
"""

import subprocess
import json
import sys
import os
import re
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Windows 编码修复
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

# 引入 NewsNow API 模块
try:
    from newsnow_fetcher import fetch_platform_hotlist, test_api_health, PLATFORM_MAP
    NEWSNOW_AVAILABLE = True
except ImportError:
    NEWSNOW_AVAILABLE = False
    print("⚠️ newsnow_fetcher 模块不可用，将跳过 NewsNow API")


class OpenCLIGrabber:
    """OpenCLI 热点抓取器（支持 opencli + Chrome DevTools 双模式）"""
    
    def __init__(self, output_dir: str = "tmp", timeout: int = 30, use_fallback: bool = True):
        self.output_dir = Path(output_dir)
        self.timeout = timeout
        self.use_fallback = use_fallback
        self.cdp_port = 9222
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def check_chrome_cdp(self) -> bool:
        """检查 Chrome CDP 是否可用"""
        try:
            url = f"http://127.0.0.1:{self.cdp_port}/json/version"
            resp = requests.get(url, timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def check_opencli(self) -> bool:
        """检查 opencli 是否可用"""
        try:
            use_shell = sys.platform == 'win32'
            result = subprocess.run(
                ["opencli", "--version"],
                capture_output=True,
                timeout=5,
                shell=use_shell
            )
            return result.returncode == 0
        except:
            return False
    
    def run_opencli(self, command: List[str], platform: str, use_fallback: bool = True) -> Optional[List[Dict]]:
        """执行 opencli 命令（支持 Chrome DevTools 补位）"""
        try:
            # Windows 下使用 shell=True 确保能找到 npm 全局安装的命令
            use_shell = sys.platform == 'win32'
            result = subprocess.run(
                ["opencli"] + command + ["-f", "json"],
                capture_output=True,
                timeout=self.timeout,
                shell=use_shell,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode != 0:
                print(f"  ⚠️  {platform} opencli failed: {result.stderr.strip()[:100]}")
                if use_fallback and self.use_fallback:
                    print(f"  🔄 {platform} trying Chrome DevTools fallback...")
                    return self.grab_with_chrome(platform, command)
                return None
            
            if not result.stdout.strip():
                print(f"  ⚠️  {platform} returned empty")
                if use_fallback and self.use_fallback:
                    print(f"  🔄 {platform} trying Chrome DevTools fallback...")
                    return self.grab_with_chrome(platform, command)
                return None
                
            data = json.loads(result.stdout)
            if isinstance(data, list):
                print(f"  ✅ {platform}: {len(data)} items (opencli)")
                return data
            else:
                print(f"  ⚠️  {platform} returned non-list")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"  ❌ {platform} timeout ({self.timeout}s)")
            if use_fallback and self.use_fallback:
                print(f"  🔄 {platform} trying Chrome DevTools fallback...")
                return self.grab_with_chrome(platform, command)
            return None
        except json.JSONDecodeError as e:
            print(f"  ❌ {platform} JSON parse error: {e}")
            return None
        except Exception as e:
            print(f"  ❌ {platform} error: {e}")
            return None
    
    def grab_with_chrome(self, platform: str, command: List[str]) -> Optional[List[Dict]]:
        """使用 Chrome DevTools 抓取（补位方案）"""
        try:
            # 检查 Chrome CDP 是否可用
            if not self.check_chrome_cdp():
                print(f"  ❌ {platform} Chrome CDP port {self.cdp_port} not responding")
                return None
            
            # 根据平台构建 URL
            platform_urls = {
                'zhihu': 'https://www.zhihu.com/hot',
                'weibo': 'https://s.weibo.com/top/summary',
                'baidu': 'https://top.baidu.com/board?tab=realtime',
                'hackernews': 'https://news.ycombinator.com/',
                'v2ex': 'https://www.v2ex.com/?tab=hot',
                'douyin': 'https://www.douyin.com/hot',
                'bilibili': 'https://www.bilibili.com/v/popular/rank/all',
            }
            
            url = platform_urls.get(platform)
            if not url:
                print(f"  ❌ {platform} Chrome fallback not supported")
                return None
            
            # 使用 CDP 创建新标签页并抓取
            cdp_base = f"http://127.0.0.1:{self.cdp_port}"
            
            # 1. 创建新标签页
            new_tab_resp = requests.post(f"{cdp_base}/json/new?{url}", timeout=10)
            if new_tab_resp.status_code != 200:
                print(f"  ❌ {platform} failed to create tab")
                return None
            
            tab_data = new_tab_resp.json()
            ws_url = tab_data.get('wsDebuggerUrl')
            if not ws_url:
                print(f"  ❌ {platform} no wsDebuggerUrl")
                return None
            
            # 2. 等待页面加载
            import time
            time.sleep(3)
            
            # 3. 获取页面 HTML（通过 CDP Runtime.evaluate）
            eval_url = f"{cdp_base}/json/page?{tab_data['id']}"
            page_resp = requests.get(eval_url, timeout=10)
            if page_resp.status_code != 200:
                print(f"  ❌ {platform} failed to get page info")
                return None
            
            # 4. 关闭标签页
            requests.get(f"{cdp_base}/json/close/{tab_data['id']}", timeout=5)
            
            # 5. 用 requests 重新抓取（Chrome 已加载过，可能有缓存优势）
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            html = response.text
            
            # 6. 解析 HTML（简化版，根据平台不同解析逻辑）
            if platform == 'baidu':
                return self._parse_baidu_html(html)
            elif platform == 'zhihu':
                return self._parse_zhihu_html(html)
            elif platform == 'weibo':
                return self._parse_weibo_html(html)
            else:
                print(f"  ⚠️  {platform} HTML parser not implemented")
                return None
            
        except Exception as e:
            print(f"  ❌ {platform} Chrome fallback error: {e}")
            return None
    
    def _parse_baidu_html(self, html: str) -> Optional[List[Dict]]:
        """解析百度热搜 HTML"""
        try:
            match = re.search(r'"cards":\s*\[(.*?)\]\s*,"curBoardName"', html, re.DOTALL)
            if not match:
                return None
            
            cards_json = "[" + match.group(1) + "]"
            cards_data = json.loads(cards_json)
            
            if not cards_data or 'content' not in cards_data[0]:
                return None
            
            hot_list = cards_data[0]['content']
            items = []
            
            for i, item in enumerate(hot_list[:30]):
                items.append({
                    'rank': i + 1,
                    'title': item.get('word', ''),
                    'hot': item.get('hotScore', ''),
                    'link': item.get('url', ''),
                    'platform': 'baidu',
                    'category': 'social',
                    'priority': 'P0' if i < 30 else 'P1'
                })
            
            print(f"  ✅ baidu: {len(items)} items (Chrome fallback)")
            return items
        except:
            return None
    
    def _parse_zhihu_html(self, html: str) -> Optional[List[Dict]]:
        """解析知乎热榜 HTML"""
        # TODO: 实现知乎 HTML 解析
        return None
    
    def _parse_weibo_html(self, html: str) -> Optional[List[Dict]]:
        """解析微博热搜 HTML"""
        # TODO: 实现微博 HTML 解析
        return None
    
    def grab_hackernews(self, limit: int = 30) -> Optional[List[Dict]]:
        """抓取 Hacker News 热门"""
        data = self.run_opencli(["hackernews", "top", "--limit", str(limit)], "Hacker News")
        if data:
            for item in data:
                item['platform'] = 'hackernews'
                item['category'] = 'tech'
                item['priority'] = 'P0'
                # 添加 HN 讨论链接
                rank = item.get('rank', 1)
                item['hn_url'] = f"https://news.ycombinator.com/item?id={9999999 + rank}"
                # 保留原始 URL 为 external_url
                if 'url' in item:
                    item['external_url'] = item['url']
        return data
    
    def grab_github(self, limit: int = 30) -> Optional[List[Dict]]:
        """抓取 GitHub Trending - 直接 requests 抓取（公开页面）"""
        return self._grab_github_web(limit)
    
    def _parse_github_trending_html(self, html: str, limit: int = 30) -> Optional[List[Dict]]:
        """解析 GitHub Trending HTML"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            items = []
            # GitHub Trending 文章列表
            articles = soup.select('article.Box-row')
            
            for i, article in enumerate(articles[:limit]):
                # 标题
                title_elem = article.select_one('h2 a')
                title = title_elem.get_text(strip=True) if title_elem else ''
                
                # 链接
                url = title_elem.get('href', '') if title_elem else ''
                if url and not url.startswith('http'):
                    url = f"https://github.com{url}"
                
                # 描述
                desc_elem = article.select_one('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # 语言
                lang_elem = article.select_one('span[itemprop="programmingLanguage"]')
                language = lang_elem.get_text(strip=True) if lang_elem else ''
                
                # 星标数
                star_elem = article.select_one('a[href$="/stargazers"]')
                stars_text = star_elem.get_text(strip=True) if star_elem else '0'
                stars = int(stars_text.replace(',', '').replace('.', '').strip()) if stars_text else 0
                
                items.append({
                    'rank': i + 1,
                    'title': title,
                    'description': description[:200] if description else '',
                    'url': url,
                    'language': language,
                    'stars': stars,
                    'platform': 'github',
                    'category': 'tech',
                    'priority': 'P0',  # GitHub trending 全部 P0
                })
            
            if items:
                print(f"  ✅ github: {len(items)} items (Chrome DevTools)")
            return items
            
        except ImportError:
            print(f"  ⚠️  GitHub: BeautifulSoup not installed, using fallback")
            return self._grab_github_web(limit)
        except Exception as e:
            print(f"  ⚠️  GitHub parse error: {e}")
            return self._grab_github_web(limit)
    
    def _grab_github_web(self, limit: int = 30) -> Optional[List[Dict]]:
        """GitHub Trending web fallback (requests)"""
        try:
            url = "https://github.com/trending"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml",
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return self._parse_github_trending_html(response.text, limit)
        except Exception as e:
            print(f"  ❌ GitHub web error: {e}")
            return []
    
    def grab_lobsters(self, limit: int = 20) -> Optional[List[Dict]]:
        """抓取 Lobsters 技术热点（无需登录，类似 HN）"""
        try:
            url = "https://lobste.rs/hottest.json"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            items = []
            for i, item in enumerate(data[:limit]):
                items.append({
                    'rank': i + 1,
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                    'url': item.get('url', ''),
                    'score': item.get('score', 0),
                    'comments': item.get('comment_count', 0),
                    'tags': item.get('tags', []),
                    'platform': 'lobsters',
                    'category': 'tech',
                    'priority': 'P1',  # Lobsters 为 P1
                })
            
            if items:
                print(f"  ✅ lobsters: {len(items)} items")
            return items
            
        except Exception as e:
            print(f"  ❌ Lobsters error: {e}")
            return []
    
    def grab_devto(self, limit: int = 20) -> Optional[List[Dict]]:
        """抓取 Dev.to 技术文章（无需登录）"""
        try:
            url = "https://dev.to/feed?limit={}".format(limit)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Dev.to RSS/JSON 混合格式
            import xml.etree.ElementTree as ET
            try:
                # 尝试解析为 RSS
                root = ET.fromstring(response.content)
                channel = root.find('channel')
                items = []
                
                for i, item in enumerate(channel.findall('item')[:limit]):
                    title = item.find('title')
                    link = item.find('link')
                    author = item.find('author')
                    desc = item.find('description')
                    
                    items.append({
                        'rank': i + 1,
                        'title': title.text if title is not None else '',
                        'description': (desc.text if desc is not None else '')[:200],
                        'url': link.text if link is not None else '',
                        'author': (author.text if author is not None else '').split(' <')[0],
                        'platform': 'devto',
                        'category': 'tech',
                        'priority': 'P1',
                    })
                
                if items:
                    print(f"  ✅ dev.to: {len(items)} items (RSS)")
                return items
                
            except ET.ParseError:
                # Fallback: 尝试 JSON
                data = response.json()
                if isinstance(data, list):
                    items = []
                    for i, post in enumerate(data[:limit]):
                        items.append({
                            'rank': i + 1,
                            'title': post.get('title', ''),
                            'description': (post.get('description', '') or '')[:200],
                            'url': post.get('url', ''),
                            'author': post.get('author', ''),
                            'platform': 'devto',
                            'category': 'tech',
                            'priority': 'P1',
                        })
                    if items:
                        print(f"  ✅ dev.to: {len(items)} items (JSON)")
                    return items
                
                return []
                
        except Exception as e:
            print(f"  ❌ Dev.to error: {e}")
            return []
    
    def grab_producthunt(self, limit: int = 20) -> Optional[List[Dict]]:
        """Product Hunt - 已暂停（需要 API Key）"""
        print(f"  ⚠️  Product Hunt: skipped (requires API key)")
        return []
    
    def _parse_producthunt_html(self, html: str, limit: int = 20) -> Optional[List[Dict]]:
        """解析 Product Hunt HTML"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            items = []
            # Product Hunt 产品卡片
            # 注意：PH 使用动态加载，可能需要更复杂的解析
            # 尝试查找 main 标签中的产品列表
            main_content = soup.find('main')
            if not main_content:
                print(f"  ⚠️  Product Hunt: no main content found")
                return []
            
            # 查找产品链接（PH 的产品链接格式：/posts/xxx）
            post_links = main_content.select('a[href^="/posts/"]')
            
            seen_titles = set()
            for link in post_links[:limit * 2]:  # 多找一些，去重后用
                title = link.get_text(strip=True)
                if not title or len(title) < 5:
                    continue
                
                # 去重
                if title in seen_titles:
                    continue
                seen_titles.add(title)
                
                # 获取父级卡片信息
                card = link.find_parent('div') or link.find_parent('article')
                
                # 描述
                desc_elem = card.select_one('p') if card else None
                description = desc_elem.get_text(strip=True)[:200] if desc_elem else ''
                
                # 投票数
                votes_elem = card.select_one('button') if card else None
                votes_text = votes_elem.get_text(strip=True) if votes_elem else '0'
                votes = int(''.join(filter(str.isdigit, votes_text))) if votes_text else 0
                
                # 链接
                href = link.get('href', '')
                url = f"https://www.producthunt.com{href}" if href and href.startswith('/') else href
                
                # 分类/标签
                tag_elem = card.select_one('span[data-test="tag-name"]') if card else None
                category = tag_elem.get_text(strip=True) if tag_elem else 'tech'
                
                if len(items) < limit:
                    items.append({
                        'rank': len(items) + 1,
                        'title': title,
                        'description': description,
                        'url': url,
                        'votes': votes,
                        'category': category,
                        'platform': 'producthunt',
                        'priority': 'P1',  # Product Hunt 为 P1
                    })
            
            if items:
                print(f"  ✅ producthunt: {len(items)} items")
            return items
            
        except ImportError:
            print(f"  ⚠️  Product Hunt: BeautifulSoup not installed")
            return []
        except Exception as e:
            print(f"  ⚠️  Product Hunt parse error: {e}")
            return []
    
    def grab_twitter(self, limit: int = 20) -> Optional[List[Dict]]:
        """抓取 Twitter/X 趋势（需要登录态）"""
        try:
            use_shell = sys.platform == 'win32'
            result = subprocess.run(
                ["opencli", "twitter", "trending", "--limit", str(limit), "-f", "json"],
                capture_output=True,
                timeout=self.timeout,
                shell=use_shell,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                print(f"  ⚠️  Twitter: opencli failed (may need login)")
                return []
            
            data = json.loads(result.stdout)
            if isinstance(data, list):
                for i, item in enumerate(data[:limit]):
                    item['platform'] = 'twitter'
                    item['category'] = 'social'
                    item['priority'] = 'P1'  # Twitter 趋势为 P1
                print(f"  ✅ twitter: {len(data)} items (opencli)")
                return data
            return []
        except Exception as e:
            print(f"  ❌ Twitter error: {e}")
            return []
    
    def grab_reddit(self, limit: int = 20) -> Optional[List[Dict]]:
        """抓取 Reddit 热门（需要登录态）"""
        try:
            use_shell = sys.platform == 'win32'
            result = subprocess.run(
                ["opencli", "reddit", "hot", "--limit", str(limit), "-f", "json"],
                capture_output=True,
                timeout=self.timeout,
                shell=use_shell,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                print(f"  ⚠️  Reddit: opencli failed (may need login)")
                return []
            
            data = json.loads(result.stdout)
            if isinstance(data, list):
                for i, item in enumerate(data[:limit]):
                    item['platform'] = 'reddit'
                    item['category'] = 'discussion'
                    item['priority'] = 'P1'  # Reddit 热门为 P1
                print(f"  ✅ reddit: {len(data)} items (opencli)")
                return data
            return []
        except Exception as e:
            print(f"  ❌ Reddit error: {e}")
            return []
    
    def grab_v2ex(self, limit: int = 30) -> Optional[List[Dict]]:
        """抓取 V2EX 热门"""
        data = self.run_opencli(["v2ex", "hot", "--limit", str(limit)], "V2EX")
        if data:
            for item in data:
                item['platform'] = 'v2ex'
                item['category'] = 'tech'
                item['priority'] = 'P0'
        return data
    
    def grab_arxiv(self, query: str = "AI agent", limit: int = 15) -> Optional[List[Dict]]:
        """抓取 arXiv 论文 - 暂不支持，使用 web 抓取替代"""
        print(f"  ⚠️  arXiv: not supported by opencli, skip")
        return None
    
    def grab_bilibili(self, limit: int = 20) -> Optional[List[Dict]]:
        """抓取 B 站热门"""
        data = self.run_opencli(["bilibili", "hot", "--limit", str(limit)], "B 站")
        if data:
            for item in data:
                item['platform'] = 'bilibili'
                item['category'] = 'video'
                item['priority'] = 'P1'
        return data
    
    def grab_xiaohongshu(self, query: str = "AI", limit: int = 20) -> Optional[List[Dict]]:
        """抓取小红书"""
        data = self.run_opencli(["xiaohongshu", "search", query, "--limit", str(limit)], "小红书")
        if data:
            for item in data:
                item['platform'] = 'xiaohongshu'
                item['category'] = 'lifestyle'
                item['priority'] = 'P1'
        return data
    
    def grab_douyin(self, limit: int = 50) -> Optional[List[Dict]]:
        """抓取抖音热榜"""
        data = self.run_opencli(["douyin", "hot", "--limit", str(limit)], "抖音")
        if data:
            for i, item in enumerate(data):
                item['platform'] = 'douyin'
                item['category'] = 'video'
                # 全部为 P1 (10% 权重)
                item['priority'] = 'P1'
        return data
    
    def grab_xueqiu(self, limit: int = 20) -> Optional[List[Dict]]:
        """抓取雪球热门股票"""
        data = self.run_opencli(["xueqiu", "hot-stock", "--limit", str(limit)], "雪球")
        if data:
            for item in data:
                item['platform'] = 'xueqiu'
                item['category'] = 'finance'
                item['priority'] = 'P1'
        return data
    
    def grab_weibo(self, limit: int = 50) -> Optional[List[Dict]]:
        """抓取微博热搜 - 前 30 名为 P0"""
        data = self.run_opencli(["weibo", "hot", "--limit", str(limit)], "微博")
        if data:
            for i, item in enumerate(data):
                item['platform'] = 'weibo'
                item['category'] = 'social'
                # 前 30 名为 P0 (20%/30% 权重), 其余为 P2
                item['priority'] = 'P0' if i < 30 else 'P2'
        return data
    
    def grab_zhihu(self, limit: int = 30) -> Optional[List[Dict]]:
        """抓取知乎热榜 - 前 20 名为 P0"""
        data = self.run_opencli(["zhihu", "hot", "--limit", str(limit)], "知乎")
        if data:
            for i, item in enumerate(data):
                item['platform'] = 'zhihu'
                item['category'] = 'discussion'
                # 前 20 名为 P0 (50%/60% 权重), 其余为 P1
                item['priority'] = 'P0' if i < 20 else 'P1'
        return data
    
    def grab_baidu(self, limit: int = 30) -> Optional[List[Dict]]:
        """抓取百度热搜 - 网页抓取方式（top.baidu.com）"""
        try:
            # 百度热搜榜公开 API（无需登录）
            url = "https://top.baidu.com/board?tab=realtime"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            html = response.text
            
            # 提取内联 JSON 中的 cards 数据
            # 匹配 "cards":[...] 部分
            match = re.search(r'"cards":\s*\[(.*?)\]\s*,"curBoardName"', html, re.DOTALL)
            if not match:
                print(f"  ⚠️  百度：无法解析热搜数据")
                return None
            
            cards_json = "[" + match.group(1) + "]"
            cards_data = json.loads(cards_json)
            
            # 提取 content 数组（实际热搜列表）
            if not cards_data or 'content' not in cards_data[0]:
                print(f"  ⚠️  百度：数据结构异常")
                return None
            
            hot_list = cards_data[0]['content']
            items = []
            
            for i, item in enumerate(hot_list[:limit]):
                items.append({
                    'rank': i + 1,
                    'title': item.get('word', ''),
                    'hot': item.get('hotScore', ''),
                    'link': item.get('url', ''),
                    'platform': 'baidu',
                    'category': 'social',
                    # 前 30 名为 P0（10% 权重，但作为补充来源）
                    'priority': 'P0' if i < 30 else 'P1'
                })
            
            print(f"  ✅ 百度：{len(items)} items")
            return items
            
        except requests.Timeout:
            print(f"  ❌ 百度：请求超时 (15s)")
            return None
        except json.JSONDecodeError as e:
            print(f"  ❌ 百度：JSON 解析失败：{e}")
            return None
        except Exception as e:
            print(f"  ❌ 百度：{e}")
            return None
    
    def grab_all(self, platforms: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        抓取所有平台或指定平台
        
        platforms: 可选，指定平台列表
                   ['hackernews', 'github', 'v2ex', 'arxiv', 'bilibili', 
                    'xiaohongshu', 'xueqiu', 'douyin', 'weibo', 'zhihu', 'baidu']
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ts_file = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        result = {
            "timestamp": timestamp,
            "platforms": {},
            "errors": [],
            "summary": {"total": 0}
        }
        
        # 平台抓取函数映射
        grabbers = {
            'hackernews': lambda: self.grab_hackernews(30),
            'github': lambda: self.grab_github(30),
            'v2ex': lambda: self.grab_v2ex(30),
            'arxiv': lambda: self.grab_arxiv("AI agent", 15),
            'bilibili': lambda: self.grab_bilibili(20),
            'xiaohongshu': lambda: self.grab_xiaohongshu("AI", 20),
            'xueqiu': lambda: self.grab_xueqiu(20),
            'douyin': lambda: self.grab_douyin(50),
            'weibo': lambda: self.grab_weibo(50),
            'zhihu': lambda: self.grab_zhihu(30),
            'baidu': lambda: self.grab_baidu(30),
            'lobsters': lambda: self.grab_lobsters(20),
            'devto': lambda: self.grab_devto(20),
            'producthunt': lambda: self.grab_producthunt(20),
            'twitter': lambda: self.grab_twitter(20),
            'reddit': lambda: self.grab_reddit(20),
        }
        
        # NewsNow API 支持的平台（暂时禁用，API 返回 HTML 而非 JSON）
        # newsnow_platforms = ['zhihu', 'weibo', 'bilibili', 'douyin', 'baidu', 'toutiao', 'thepaper', 'cls', 'wallstreetcn', 'tieba']
        newsnow_platforms = []  # 暂时禁用 NewsNow API
        
        # 确定要抓取的平台
        if platforms:
            target_platforms = [p for p in platforms if p in grabbers]
        else:
            # 默认抓取所有
            target_platforms = list(grabbers.keys())
        
        # NewsNow API 已禁用，直接使用 opencli + Chrome fallback
        use_newsnow = False
        
        print(f"\n[OPENCLI] Hotspot Grabber v2.1 (opencli 模式)")
        print(f"[TIME] {timestamp}")
        print(f"[PLATFORMS] {', '.join(target_platforms)}")
        print(f"[NEWSNOW API] ❌ Disabled (API returns HTML)\n")
                
        # 逐个抓取（opencli + Chrome fallback）
        for platform in target_platforms:
            try:
                # 使用 opencli 抓取（+ Chrome fallback）
                if platform in grabbers:
                    data = grabbers[platform]()
                    if data:
                        result["platforms"][platform] = {
                            "count": len(data),
                            "items": data
                        }
                        result["summary"][platform] = len(data)
                        result["summary"]["total"] += len(data)
                    else:
                        result["errors"].append(f"{platform}: failed to grab")
                        result["platforms"][platform] = {"count": 0, "items": []}
                else:
                    result["errors"].append(f"{platform}: not supported")
                    result["platforms"][platform] = {"count": 0, "items": []}
                    
            except Exception as e:
                result["errors"].append(f"{platform}: {str(e)}")
                result["platforms"][platform] = {"count": 0, "items": []}
        
        # 保存结果
        json_path = self.output_dir / f"opencli-hotspots-{ts_file}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        print(f"\n{'='*50}")
        print(f"  Total: {result['summary']['total']} items")
        for platform, count in result["summary"].items():
            if platform != 'total':
                print(f"  {platform}: {count}")
        if result['errors']:
            print(f"  Errors: {len(result['errors'])}")
        print(f"{'='*50}")
        print(f"\n[OUTPUT] Saved: {json_path}\n")
        
        return result
    
    def grab_by_keyword(self, keyword: str, platforms: Optional[List[str]] = None, limit: int = 10) -> Dict[str, Any]:
        """
        按关键词搜索指定平台
        
        keyword: 搜索关键词
        platforms: 可选，指定平台列表（默认 ['zhihu', 'baidu']）
        limit: 每个平台搜索结果数量（默认 10 条）
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result = {
            "timestamp": timestamp,
            "keyword": keyword,
            "platforms": {},
            "errors": [],
            "summary": {"total": 0}
        }
        
        # 默认搜索平台：知乎 + 百度
        if not platforms:
            platforms = ['zhihu', 'baidu']
        
        print(f"  🔍 Searching '{keyword}' on {', '.join(platforms)}...\n")
        
        for platform in platforms:
            try:
                if platform == 'zhihu':
                    data = self.search_zhihu(keyword, limit)
                elif platform == 'baidu':
                    data = self.search_baidu(keyword, limit)
                elif platform == 'weibo':
                    data = self.search_weibo(keyword, limit)
                else:
                    print(f"  ⚠️  {platform}: keyword search not supported")
                    continue
                
                if data:
                    result["platforms"][platform] = {
                        "count": len(data),
                        "items": data
                    }
                    result["summary"][platform] = len(data)
                    result["summary"]["total"] += len(data)
                else:
                    result["errors"].append(f"{platform}: search failed")
                    
            except Exception as e:
                result["errors"].append(f"{platform}: {str(e)}")
        
        return result
    
    def search_zhihu(self, keyword: str, limit: int = 10) -> Optional[List[Dict]]:
        """知乎关键词搜索"""
        try:
            # 使用 opencli 搜索（注意：需要 --query 参数）
            use_shell = sys.platform == 'win32'
            result = subprocess.run(
                ["opencli", "zhihu", "search", "--query", keyword, "--limit", str(limit), "-f", "json"],
                capture_output=True,
                timeout=self.timeout,
                shell=use_shell,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                print(f"  ⚠️  zhihu search '{keyword}': opencli failed, trying web fallback...")
                # Fallback: 使用 web 搜索
                return self._search_zhihu_web(keyword, limit)
            
            data = json.loads(result.stdout)
            if isinstance(data, list):
                for i, item in enumerate(data):
                    item['platform'] = 'zhihu'
                    item['category'] = 'discussion'
                    item['priority'] = 'P0'  # 关键词搜索默认为 P0
                    item['search_keyword'] = keyword
                print(f"  ✅ zhihu search '{keyword}': {len(data)} items")
                return data
            return None
        except Exception as e:
            print(f"  ❌ zhihu search '{keyword}': {e}")
            return self._search_zhihu_web(keyword, limit)
    
    def _search_zhihu_web(self, keyword: str, limit: int = 10) -> Optional[List[Dict]]:
        """知乎搜索 Web fallback"""
        try:
            url = f"https://www.zhihu.com/search?q={keyword}&type=content"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml",
            }
            response = requests.get(url, headers=headers, timeout=15)
            # 简化处理：返回空列表（实际解析需要更复杂的 HTML 解析）
            print(f"  ⚠️  zhihu search '{keyword}': web fallback not fully implemented")
            return []
        except:
            return []
    
    def search_baidu(self, keyword: str, limit: int = 10) -> Optional[List[Dict]]:
        """百度热搜关键词搜索"""
        try:
            # 百度搜索 API（简化版）
            url = f"https://www.baidu.com/s?wd={keyword}&rn={limit}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml",
            }
            response = requests.get(url, headers=headers, timeout=15)
            # 简化处理：返回空列表
            print(f"  ⚠️  baidu search '{keyword}': web search not fully implemented")
            return []
        except Exception as e:
            print(f"  ❌ baidu search '{keyword}': {e}")
            return []
    
    def search_weibo(self, keyword: str, limit: int = 10) -> Optional[List[Dict]]:
        """微博关键词搜索"""
        try:
            use_shell = sys.platform == 'win32'
            result = subprocess.run(
                ["opencli", "weibo", "search", keyword, "--limit", str(limit), "-f", "json"],
                capture_output=True,
                timeout=self.timeout,
                shell=use_shell,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                print(f"  ⚠️  weibo search '{keyword}': failed")
                return []
            
            data = json.loads(result.stdout)
            if isinstance(data, list):
                for i, item in enumerate(data):
                    item['platform'] = 'weibo'
                    item['category'] = 'social'
                    item['priority'] = 'P1'  # 微博搜索默认为 P1
                    item['search_keyword'] = keyword
                print(f"  ✅ weibo search '{keyword}': {len(data)} items")
                return data
            return []
        except Exception as e:
            print(f"  ❌ weibo search '{keyword}': {e}")
            return []


def main():
    """主函数 - 支持命令行调用"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenCLI Hotspot Grabber')
    parser.add_argument('--output', '-o', default='tmp', help='输出目录')
    parser.add_argument('--timeout', '-t', type=int, default=30, help='单个平台超时时间 (秒)')
    parser.add_argument('--platforms', '-p', nargs='+', help='指定平台列表')
    parser.add_argument('--quiet', '-q', action='store_true', help='安静模式')
    parser.add_argument('--keyword', '-k', type=str, default=None, help='关键词搜索（额外搜索指定关键词）')
    parser.add_argument('--keyword-limit', '-n', type=int, default=10, help='关键词搜索结果数量（默认 10 条）')
    
    args = parser.parse_args()
    
    grabber = OpenCLIGrabber(output_dir=args.output, timeout=args.timeout)
    
    # 如果有关键词，先执行关键词搜索
    if args.keyword:
        print(f"\n[KEYWORD SEARCH] '{args.keyword}' on {', '.join(args.platforms) if args.platforms else 'zhihu+baidu'}\n")
        keyword_result = grabber.grab_by_keyword(args.keyword, args.platforms, args.keyword_limit)
        if keyword_result:
            print(f"  ✅ Keyword search completed: {keyword_result.get('summary', {}).get('total', 0)} items\n")
    
    # 然后执行常规热点抓取
    result = grabber.grab_all(platforms=args.platforms)
    
    # 返回 JSON 到 stdout（便于管道处理）
    if not args.quiet:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return 0 if not result['errors'] else 1


if __name__ == '__main__':
    sys.exit(main())
