#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 抓取脚本 - Intel Officer 情报收集
用途：抓取 AI/科技领域 RSS 订阅源，写入飞书多维表格
作者：Intel Officer
更新：2026-03-18
"""

import feedparser
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

# ==================== 配置区 ====================

# 核心订阅源 (已验证可用 - 2026-03-18 测试)
# 测试状态：✅ 成功 (100% 可用)
CORE_FEEDS = {
    # 官方实验室 (1 个)
    "openai": "https://openai.com/news/rss.xml",  # ✅ 888 条
    
    # 科技媒体 (3 个)
    "techcrunch": "https://techcrunch.com/feed/",  # ✅ 20 条
    "mit_tech_review": "https://www.technologyreview.com/topic/artificial-intelligence/feed",  # ✅ 10 条
    "hacker_news": "https://hnrss.org/frontpage",  # ✅ 20 条
    
    # 中文媒体 (1 个)
    "qbitai": "https://www.qbitai.com/feed",  # ✅ 10 条
}

# 扩展订阅源 (可选)
EXTENDED_FEEDS = {
    # 中文媒体 (2 个)
    "sspai": "https://sspai.com/feed",  # ✅ 可用
    "leiphone": "https://www.leiphone.com/feed",  # ✅ 可用
    
    # RSSHub (社交媒体)
    "zhihu_hot": "https://rsshub.app/zhihu/hotlist",  # 知乎热榜
}

# 问题源 (需要重试/代理)
PROBLEM_FEEDS = {
    # 超时源 (国内访问慢)
    "google_ai": "https://research.google/blog/rss/",  # ⚠️ 超时
    "huggingface": "https://huggingface.co/blog/feed.xml",  # ⚠️ 超时
    
    # 失效源 (需要替换)
    # "jiqizhixin": "https://www.jiqizhixin.com/rss",  # ❌ 返回 HTML
    # "36kr": "http://feeds.feedburner.com/36kr/motie",  # ❌ feedburner 被墙
}

# 扩展订阅源 (20+ 个，阶段 2 使用)
EXTENDED_FEEDS = {
    # 更多官方实验室
    "deepmind": "https://deepmind.google/discover/blog/feed/",
    "bair": "https://bair.berkeley.edu/blog/feed.xml",
    
    # 更多科技媒体
    "the_verge": "https://www.theverge.com/rss/index.xml",
    "ars_technica": "https://feeds.arstechnica.com/arstechnica/index",
    "wired_ai": "https://www.wired.com/feed/tag-ai/rss",
    "infoq_ai": "https://www.infoq.com/ai/feed/",
    
    # 学术论文
    "arxiv_cs_ai": "http://arxiv.org/rss/cs.AI",
    "arxiv_cs_ml": "http://arxiv.org/rss/cs.LG",
    
    # 中文媒体
    "leiphone": "https://www.leiphone.com/feed",
    "ithome": "https://www.ithome.com/rss/",
    
    # 开发者社区
    "github_blog": "https://github.blog/feed/",
    "stackoverflow": "https://stackoverflow.blog/feed/",
    "meituan_tech": "https://tech.meituan.com/feed/",
    "juejin": "https://juejin.cn/feed",
}

# 飞书多维表格配置
FEISHU_CONFIG = {
    "app_token": "DTt9bx9gka7UW6s52ndcdnLCnDe",
    "table_id": "tbl97RKEz1h5uHJX",  # 原始情报表
}

# 输出配置
OUTPUT_DIR = Path(__file__).parent / "memory"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==================== 工具函数 ====================

def generate_record_id(source: str, title: str, link: str) -> str:
    """生成唯一记录 ID (用于去重)"""
    content = f"{source}:{title}:{link}"
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]

def parse_timestamp(timestamp_str: str) -> Optional[str]:
    """解析 RSS 时间戳为 ISO 格式"""
    if not timestamp_str:
        return None
    
    # 尝试多种格式
    formats = [
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(timestamp_str.strip(), fmt)
            return dt.isoformat()
        except ValueError:
            continue
    
    return timestamp_str

def clean_html(text: str) -> str:
    """清理 HTML 标签"""
    if not text:
        return ""
    
    # 简单清理：移除 HTML 标签
    import re
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def truncate_text(text: str, max_length: int = 500) -> str:
    """截断文本到指定长度"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

# ==================== 核心抓取逻辑 ====================

def fetch_single_feed(source: str, url: str, limit: int = 10) -> List[Dict]:
    """抓取单个 RSS 源"""
    entries = []
    
    try:
        # 使用 UTF-8 安全打印
        print(f"  [{source}] {url}")
        feed = feedparser.parse(url, request_headers={
            'User-Agent': 'Mozilla/5.0 (Intel Officer RSS Grabber/1.0)'
        })
        
        if feed.bozo:
            print(f"    [WARN] RSS 解析问题 - {feed.bozo_exception}")
        
        print(f"    [OK] 成功，共 {len(feed.entries)} 条，取前 {limit} 条")
        
        for i, entry in enumerate(feed.entries[:limit]):
            record = {
                "采集轮次": generate_record_id(source, entry.title, entry.link),
                "采集时间": datetime.now().isoformat(),
                "搜索关键词": f"RSS:{source}",
                "信息源": source,
                "标题": entry.title[:200] if entry.title else "无标题",
                "原文内容": truncate_text(clean_html(entry.get('summary', entry.get('description', ''))), 2000),
                "原文链接": entry.link[:500] if entry.link else "",
                "发布时间": parse_timestamp(entry.get('published', entry.get('updated', ''))),
                "作者": entry.get('author', ''),
            }
            entries.append(record)
            
    except Exception as e:
        print(f"    [ERROR] {e}")
    
    return entries

def fetch_all_feeds(feeds: Dict[str, str], limit: int = 10) -> List[Dict]:
    """抓取所有 RSS 源"""
    all_entries = []
    
    print(f"\n[START] 开始抓取 {len(feeds)} 个 RSS 源...")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    for source, url in feeds.items():
        entries = fetch_single_feed(source, url, limit)
        if entries:
            all_entries.extend(entries)
            success_count += 1
        else:
            fail_count += 1
    
    print("=" * 60)
    print(f"[DONE] {success_count} 成功，{fail_count} 失败")
    print(f"[TOTAL] 共抓取 {len(all_entries)} 条内容")
    
    return all_entries

# ==================== 输出处置 ====================

def save_to_json(entries: List[Dict], filename: Optional[str] = None) -> str:
    """保存为 JSON 文件"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"rss-feed-{timestamp}.json"
    
    output_path = OUTPUT_DIR / filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    
    print(f"[SAVE] JSON: {output_path}")
    return str(output_path)

def save_to_markdown(entries: List[Dict], filename: Optional[str] = None) -> str:
    """保存为 Markdown 文件"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"rss-feed-{timestamp}.md"
    
    output_path = OUTPUT_DIR / filename
    
    # 按来源分组
    by_source = {}
    for entry in entries:
        source = entry.get("信息源", "unknown")
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(entry)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# RSS 抓取结果\n\n")
        f.write(f"**抓取时间:** {datetime.now().isoformat()}\n")
        f.write(f"**总计:** {len(entries)} 条内容\n\n")
        f.write(f"---\n\n")
        
        for source, source_entries in sorted(by_source.items()):
            f.write(f"## [{source}] ({len(source_entries)} 条)\n\n")
            
            for i, entry in enumerate(source_entries, 1):
                title = entry['标题'].replace('\n', ' ')
                f.write(f"### {i}. {title}\n\n")
                f.write(f"- **来源:** {source}\n")
                if entry.get('发布时间'):
                    f.write(f"- **发布:** {entry['发布时间']}\n")
                if entry.get('作者'):
                    f.write(f"- **作者:** {entry['作者']}\n")
                f.write(f"- **链接:** [{entry['原文链接']}]({entry['原文链接']})\n\n")
                
                if entry.get('原文内容'):
                    content = entry['原文内容'][:300].replace('\n', ' ')
                    f.write(f"> {content}...\n\n")
                
                f.write(f"---\n\n")
    
    print(f"[SAVE] MD: {output_path}")
    return str(output_path)

def print_summary(entries: List[Dict]):
    """打印摘要统计"""
    print("\n[SUMMARY] 抓取摘要统计")
    print("=" * 60)
    
    # 按来源统计
    by_source = {}
    for entry in entries:
        source = entry.get("信息源", "unknown")
        by_source[source] = by_source.get(source, 0) + 1
    
    print(f"{'来源':<20} {'数量':>10}")
    print("-" * 60)
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"{source:<20} {count:>10}")
    
    print("=" * 60)
    
    # 显示最新 5 条
    print("\n[LATEST] 最新 5 条内容")
    print("=" * 60)
    for entry in entries[:5]:
        title = entry['标题'][:50].replace('\n', ' ')
        print(f"  [{entry['信息源']}] {title}...")
    print("=" * 60)

# ==================== 飞书集成 (可选) ====================

def save_to_feishu(entries: List[Dict]) -> bool:
    """保存到飞书多维表格 (需要飞书 API)"""
    print("\n[WARN] 飞书写入功能需要配置 API 凭证")
    print("       当前跳过，仅保存到本地文件")
    # TODO: 集成 feishu_bitable_app_table_record
    return False

# ==================== 主函数 ====================

def main(mode: str = "core", limit: int = 10, output_format: str = "both"):
    """
    主函数
    
    Args:
        mode: "core" (核心 10 个) 或 "extended" (扩展 30+ 个)
        limit: 每个源抓取条数
        output_format: "json", "markdown", "both"
    """
    print("\n" + "=" * 60)
    print("[Intel Officer] RSS 抓取脚本")
    print("=" * 60)
    print(f"模式：{mode}")
    print(f"每源限制：{limit} 条")
    print(f"输出格式：{output_format}")
    print("=" * 60)
    
    # 选择订阅源
    if mode == "extended":
        feeds = {**CORE_FEEDS, **EXTENDED_FEEDS}
    else:
        feeds = CORE_FEEDS
    
    print(f"订阅源：{len(feeds)} 个")
    
    # 执行抓取
    entries = fetch_all_feeds(feeds, limit)
    
    if not entries:
        print("\n[ERROR] 未抓取到任何内容，请检查网络连接或 RSS 源")
        return False
    
    # 输出结果
    print_summary(entries)

    # 修复4: 空数据不写文件
    if not entries:
        print("\n[WARN] No entries fetched, skipping file write")
        return True

    output_files = []
    if output_format in ["json", "both"]:
        output_files.append(save_to_json(entries))

    if output_format in ["markdown", "both"]:
        output_files.append(save_to_markdown(entries))
    
    # 尝试写入飞书
    # save_to_feishu(entries)
    
    print(f"\n[DONE] 完成！共生成 {len(output_files)} 个文件")
    return True

# ==================== 命令行入口 ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Intel Officer RSS 抓取脚本")
    parser.add_argument("--mode", choices=["core", "extended"], default="core",
                       help="抓取模式：core(10 个核心源) 或 extended(30+ 扩展源)")
    parser.add_argument("--limit", type=int, default=10,
                       help="每个源抓取条数 (默认 10)")
    parser.add_argument("--format", choices=["json", "markdown", "both"], default="both",
                       help="输出格式 (默认 both)")
    
    args = parser.parse_args()
    
    success = main(
        mode=args.mode,
        limit=args.limit,
        output_format=args.format
    )
    
    sys.exit(0 if success else 1)
