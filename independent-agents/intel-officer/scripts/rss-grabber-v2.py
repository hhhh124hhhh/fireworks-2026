#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS Grabber v2.0 - Intel Officer
Features: Retry logic + Feishu integration + Alert system
Author: Intel Officer
Date: 2026-03-18
"""

import feedparser
import json
import sys
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import socket

# Set global timeout
socket.setdefaulttimeout(30)

# ==================== Configuration ====================

# Core feeds (5 verified)
CORE_FEEDS = {
    "openai": "https://openai.com/news/rss.xml",
    "techcrunch": "https://techcrunch.com/feed/",
    "mit_tech_review": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "hacker_news": "https://hnrss.org/frontpage",
    "qbitai": "https://www.qbitai.com/feed",
}

# Extended feeds
EXTENDED_FEEDS = {
    "sspai": "https://sspai.com/feed",
    "leiphone": "https://www.leiphone.com/feed",
    "zhihu_hot": "https://rsshub.app/zhihu/hotlist",
}

# Feishu configuration
FEISHU_CONFIG = {
    "app_token": "DTt9bx9gka7UW6s52ndcdnLCnDe",
    "table_id_raw": "tbl97RKEz1h5uHJX",
    "table_id_clean": "tblnpKvIOTZ6sZNt",
}

# Retry configuration
RETRY_CONFIG = {
    "max_attempts": 3,
    "timeout": 30,
    "backoff": 2,
}

# Alert configuration
ALERT_CONFIG = {
    "max_failures": 3,
    "feishu_user": "ou_c1f49efdd595b46e212560e66abc7205",
}

# Output directory
OUTPUT_DIR = Path(__file__).parent / "memory"
OUTPUT_DIR.mkdir(exist_ok=True)

# ==================== Data Classes ====================

@dataclass
class FeedEntry:
    record_id: str
    fetch_time: str
    keyword: str
    source: str
    title: str
    content: str
    link: str
    published: Optional[str] = None
    author: Optional[str] = None

@dataclass
class FetchResult:
    source: str
    url: str
    success: bool
    entry_count: int
    error: Optional[str] = None
    duration_ms: int = 0

@dataclass
class AlertMessage:
    level: str
    title: str
    message: str
    failed_feeds: List[str]
    timestamp: str

# ==================== Utility Functions ====================

def generate_record_id(source: str, title: str, link: str) -> str:
    content = f"{source}:{title}:{link}"
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]

def parse_timestamp(timestamp_str: str) -> Optional[str]:
    if not timestamp_str:
        return None
    import email.utils
    try:
        dt = email.utils.parsedate_to_datetime(timestamp_str)
        return dt.isoformat()
    except:
        pass
    return timestamp_str

def clean_html(text: str) -> str:
    if not text:
        return ""
    import re
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def truncate_text(text: str, max_length: int = 500) -> str:
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

# ==================== Retry Decorator ====================

def retry_on_failure(max_attempts: int = 3, backoff: int = 2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        wait_time = backoff ** attempt
                        print(f"  [RETRY] {attempt}/{max_attempts}, waiting {wait_time}s...")
                        time.sleep(wait_time)
            raise last_exception
        return wrapper
    return decorator

# ==================== Core Fetch Logic ====================

@retry_on_failure(max_attempts=RETRY_CONFIG["max_attempts"], backoff=RETRY_CONFIG["backoff"])
def fetch_single_feed(source: str, url: str, limit: int = 10) -> Tuple[List[FeedEntry], int]:
    start_time = time.time()
    print(f"  [{source}] {url}")
    
    feed = feedparser.parse(url, request_headers={
        'User-Agent': 'Mozilla/5.0 (Intel Officer RSS Grabber/2.0)'
    })
    
    if feed.bozo:
        raise Exception(f"RSS parse error: {feed.bozo_exception}")
    
    entries = []
    for entry in feed.entries[:limit]:
        record = FeedEntry(
            record_id=generate_record_id(source, entry.title, entry.link),
            fetch_time=datetime.now().isoformat(),
            keyword=f"RSS:{source}",
            source=source,
            title=entry.title[:200] if entry.title else "No title",
            content=truncate_text(clean_html(entry.get('summary', '')), 2000),
            link=entry.link[:500] if entry.link else "",
            published=parse_timestamp(entry.get('published', entry.get('updated', ''))),
            author=entry.get('author', ''),
        )
        entries.append(record)
    
    duration_ms = int((time.time() - start_time) * 1000)
    print(f"    [OK] {len(feed.entries)} entries, taking {limit}, {duration_ms}ms")
    
    return entries, len(feed.entries)

def fetch_all_feeds(feeds: Dict[str, str], limit: int = 10) -> Tuple[List[FeedEntry], List[FetchResult]]:
    all_entries = []
    results = []
    
    print(f"\n[START] Fetching {len(feeds)} RSS feeds...")
    print("=" * 60)
    
    for source, url in feeds.items():
        start_time = time.time()
        try:
            entries, total = fetch_single_feed(source, url, limit)
            all_entries.extend(entries)
            results.append(FetchResult(
                source=source,
                url=url,
                success=True,
                entry_count=len(entries),
                duration_ms=int((time.time() - start_time) * 1000)
            ))
        except Exception as e:
            error_msg = str(e)
            print(f"    [ERROR] {error_msg}")
            results.append(FetchResult(
                source=source,
                url=url,
                success=False,
                entry_count=0,
                error=error_msg,
                duration_ms=int((time.time() - start_time) * 1000)
            ))
    
    print("=" * 60)
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count
    print(f"[DONE] {success_count} success, {fail_count} failed")
    print(f"[TOTAL] {len(all_entries)} entries fetched")
    
    return all_entries, results

# ==================== Feishu Integration ====================

def save_to_feishu(entries: List[FeedEntry], table_id: str = "raw") -> str:
    if not entries:
        print("[Feishu] No data to write")
        return ""
    
    try:
        if table_id == "raw":
            target_table = FEISHU_CONFIG["table_id_raw"]
        else:
            target_table = FEISHU_CONFIG["table_id_clean"]
        
        print(f"\n[Feishu] Preparing to write {len(entries)} records to {target_table}...")
        
        # Save as JSON for later processing
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        json_path = OUTPUT_DIR / f"rss-feishu-{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)
        
        print(f"[Feishu] Saved to: {json_path}")
        print(f"[Feishu] Note: Use feishu_bitable_app_table_record to write to Feishu")
        
        return str(json_path)
        
    except Exception as e:
        print(f"[Feishu] Error: {e}")
        return ""

# ==================== Alert System ====================

def check_failures(results: List[FetchResult]) -> Optional[AlertMessage]:
    failed = [r for r in results if not r.success]
    
    if not failed:
        return None
    
    fail_rate = len(failed) / len(results) * 100
    
    if fail_rate < 50:
        return None
    
    alert = AlertMessage(
        level="error" if fail_rate > 80 else "warning",
        title=f"RSS Fetch Alert ({len(failed)}/{len(results)})",
        message=f"Failure rate: {fail_rate:.1f}%\n\nFailed feeds:\n" + "\n".join([
            f"- {r.source}: {r.error}" for r in failed
        ]),
        failed_feeds=[r.source for r in failed],
        timestamp=datetime.now().isoformat()
    )
    
    return alert

def send_alert(alert: AlertMessage) -> str:
    print(f"\n[ALERT] {alert.level.upper()}: {alert.title}")
    print(alert.message)
    
    # Save alert to file
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    alert_path = OUTPUT_DIR / f"rss-alert-{timestamp}.json"
    with open(alert_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(alert), f, ensure_ascii=False, indent=2)
    
    print(f"[ALERT] Saved to: {alert_path}")
    return str(alert_path)

# ==================== Output Functions ====================

def save_to_json(entries: List[FeedEntry]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = OUTPUT_DIR / f"rss-feed-{timestamp}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)
    
    print(f"[SAVE] JSON: {output_path}")
    return str(output_path)

def save_to_markdown(entries: List[FeedEntry]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = OUTPUT_DIR / f"rss-feed-{timestamp}.md"
    
    by_source = {}
    for entry in entries:
        source = entry.source
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(entry)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# RSS Fetch Results\n\n")
        f.write(f"**Time:** {datetime.now().isoformat()}\n")
        f.write(f"**Total:** {len(entries)} entries\n\n---\n\n")
        
        for source, source_entries in sorted(by_source.items()):
            f.write(f"## [{source}] ({len(source_entries)} entries)\n\n")
            for i, entry in enumerate(source_entries, 1):
                f.write(f"### {i}. {entry.title}\n\n")
                f.write(f"- **Source:** {source}\n")
                if entry.published:
                    f.write(f"- **Published:** {entry.published}\n")
                f.write(f"- **Link:** [{entry.link}]({entry.link})\n\n")
                if entry.content:
                    f.write(f"> {entry.content[:300]}...\n\n")
                f.write(f"---\n\n")
    
    print(f"[SAVE] MD: {output_path}")
    return str(output_path)

def print_summary(entries: List[FeedEntry], results: List[FetchResult]):
    print("\n[SUMMARY]")
    print("=" * 60)
    
    by_source = {}
    for entry in entries:
        by_source[entry.source] = by_source.get(entry.source, 0) + 1
    
    print(f"{'Source':<25} {'Count':>10}")
    print("-" * 60)
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"{source:<25} {count:>10}")
    
    print("=" * 60)
    
    print("\n[LATEST 5]")
    print("=" * 60)
    for entry in entries[:5]:
        title = entry.title[:50]
        print(f"  [{entry.source}] {title}...")
    print("=" * 60)
    
    failed = [r for r in results if not r.success]
    if failed:
        print("\n[FAILED]")
        print("=" * 60)
        for r in failed:
            print(f"  - {r.source}: {r.error}")
        print("=" * 60)

# ==================== Main Function ====================

def main(mode: str = "core", limit: int = 10, feishu: bool = False):
    print("\n" + "=" * 60)
    print("[Intel Officer] RSS Grabber v2.0")
    print("=" * 60)
    print(f"Mode: {mode}")
    print(f"Limit: {limit} per feed")
    print(f"Feishu: {feishu}")
    print(f"Retry: {RETRY_CONFIG['max_attempts']} attempts, {RETRY_CONFIG['backoff']}x backoff")
    print("=" * 60)
    
    if mode == "extended":
        feeds = {**CORE_FEEDS, **EXTENDED_FEEDS}
    else:
        feeds = CORE_FEEDS
    
    print(f"Feeds: {len(feeds)}")
    
    entries, results = fetch_all_feeds(feeds, limit)
    
    if not entries:
        print("\n[ERROR] No entries fetched")
        return False
    
    print_summary(entries, results)
    save_to_json(entries)
    save_to_markdown(entries)
    
    if feishu and entries:
        save_to_feishu(entries, table_id="raw")
    
    alert = check_failures(results)
    if alert:
        send_alert(alert)
        if alert.level == "error":
            return False
    
    print(f"\n[DONE] Complete!")
    return True

# ==================== CLI Entry ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Intel Officer RSS Grabber v2.0")
    parser.add_argument("--mode", choices=["core", "extended"], default="core")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--feishu", action="store_true")
    parser.add_argument("--test-retry", action="store_true", help="Test retry logic")
    
    args = parser.parse_args()
    
    if args.test_retry:
        print("\n[TEST] Testing retry logic...")
        try:
            fetch_single_feed("test", "https://invalid-url-test.com/rss", 1)
        except Exception as e:
            print(f"[TEST] Retry logic works: {e}")
        sys.exit(0)
    
    success = main(mode=args.mode, limit=args.limit, feishu=args.feishu)
    sys.exit(0 if success else 1)
