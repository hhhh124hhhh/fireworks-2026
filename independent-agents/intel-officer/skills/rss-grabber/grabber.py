#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS Grabber Skill - Intel Officer
Auto-fetch RSS feeds with retry, Feishu integration, and alerts
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import feedparser
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import socket

socket.setdefaulttimeout(30)

# ==================== Configuration ====================

CORE_FEEDS = {
    "openai": "https://openai.com/news/rss.xml",
    "techcrunch": "https://techcrunch.com/feed/",
    "mit_tech_review": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "hacker_news": "https://hnrss.org/frontpage",
    "qbitai": "https://www.qbitai.com/feed",
}

EXTENDED_FEEDS = {
    "sspai": "https://sspai.com/feed",
    "leiphone": "https://www.leiphone.com/feed",
    "zhihu_hot": "https://rsshub.app/zhihu/hotlist",
}

FEISHU_CONFIG = {
    "app_token": "DTt9bx9gka7UW6s52ndcdnLCnDe",
    "table_id_raw": "tbl97RKEz1h5uHJX",
    "table_id_clean": "tblnpKvIOTZ6sZNt",
}

RETRY_CONFIG = {
    "max_attempts": 3,
    "backoff": 2,
}

ALERT_CONFIG = {
    "max_failures": 3,
    "feishu_user": "ou_c1f49efdd595b46e212560e66abc7205",
}

OUTPUT_DIR = Path(__file__).parent / "output"
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
    title_en: Optional[str] = None  # 英文原标题
    content_en: Optional[str] = None  # 英文原内容
    published: Optional[str] = None
    author: Optional[str] = None
    is_translated: bool = False  # 是否已翻译

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
    return text[:max_length] + "..." if len(text) > max_length else text

# ==================== Translation Function ====================

def translate_to_chinese(text: str, source_lang: str = "en") -> str:
    """
    Translate English text to Chinese
    
    Args:
        text: Text to translate
        source_lang: Source language (default: en)
    
    Returns:
        Translated text or original if translation fails
    """
    if not text or len(text.strip()) < 10:
        return text
    
    # Simple heuristic: if text contains mostly Chinese characters, skip translation
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    if chinese_chars / len(text) > 0.3:
        return text
    
    try:
        # Use a simple translation approach
        # In production, integrate with translation API (Google Translate, DeepL, etc.)
        # For now, return original with note
        return text  # 保留原文，后续集成真实翻译
    except Exception as e:
        print(f"  [TRANSLATE] Warning: {e}")
        return text

def is_english_text(text: str) -> bool:
    """Check if text is primarily English"""
    if not text:
        return False
    
    # Count English letters vs Chinese characters
    english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    
    # If more English than Chinese, consider it English
    return english_chars > chinese_chars

def format_bilingual_text(chinese: str, english: str) -> str:
    """
    Format bilingual text for display
    
    Args:
        chinese: Chinese translation (or empty if not translated)
        english: English original
    
    Returns:
        Formatted bilingual text
    """
    if not chinese or chinese == english:
        # No translation, show English only
        return english
    else:
        # Show both Chinese and English
        return f"{chinese}\n\n---\n{english}"

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

# ==================== RSS Grabber Class ====================

class RSSGrabber:
    """RSS Grabber with retry, Feishu integration, and alerts"""
    
    def __init__(self):
        self.feeds = {}
        self.results = []
    
    @retry_on_failure(max_attempts=RETRY_CONFIG["max_attempts"], backoff=RETRY_CONFIG["backoff"])
    def fetch_single_feed(self, source: str, url: str, limit: int = 10) -> Tuple[List[FeedEntry], int]:
        start_time = time.time()
        print(f"  [{source}] {url}")
        
        feed = feedparser.parse(url, request_headers={
            'User-Agent': 'Mozilla/5.0 (Intel Officer RSS Grabber/1.0)'
        })
        
        if feed.bozo:
            raise Exception(f"RSS parse error: {feed.bozo_exception}")
        
        entries = []
        for entry in feed.entries[:limit]:
            title_en = entry.title[:200] if entry.title else "No title"
            content_en = truncate_text(clean_html(entry.get('summary', '')), 2000)
            
            # Check if translation needed
            needs_translation = is_english_text(title_en) or is_english_text(content_en)
            
            if needs_translation:
                # For now, keep English as placeholder for Chinese
                # Will integrate real translation API later
                title_cn = title_en  # TODO: Replace with actual translation
                content_cn = content_en  # TODO: Replace with actual translation
                
                # Format bilingual: Chinese + English
                title = format_bilingual_text(title_cn, title_en)
                content = format_bilingual_text(content_cn, content_en)
                is_translated = True
            else:
                # Chinese content, no translation needed
                title = title_en
                content = content_en
                is_translated = False
            
            record = FeedEntry(
                record_id=generate_record_id(source, title_en, entry.link),
                fetch_time=datetime.now().isoformat(),
                keyword=f"RSS:{source}",
                source=source,
                title=title,
                title_en=title_en if is_translated else None,
                content=content,
                content_en=content_en if is_translated else None,
                link=entry.link[:500] if entry.link else "",
                published=parse_timestamp(entry.get('published', entry.get('updated', ''))),
                author=entry.get('author', ''),
                is_translated=is_translated,
            )
            entries.append(record)
        
        duration_ms = int((time.time() - start_time) * 1000)
        print(f"    [OK] {len(feed.entries)} entries, taking {limit}, {duration_ms}ms")
        
        return entries, len(feed.entries)
    
    def fetch_all(self, mode: str = "core", limit: int = 10) -> Tuple[List[FeedEntry], List[FetchResult]]:
        """Fetch all RSS feeds"""
        
        if mode == "extended":
            self.feeds = {**CORE_FEEDS, **EXTENDED_FEEDS}
        else:
            self.feeds = CORE_FEEDS
        
        all_entries = []
        self.results = []
        
        print(f"\n[START] Fetching {len(self.feeds)} RSS feeds...")
        print("=" * 60)
        
        for source, url in self.feeds.items():
            start_time = time.time()
            try:
                entries, total = self.fetch_single_feed(source, url, limit)
                all_entries.extend(entries)
                self.results.append(FetchResult(
                    source=source,
                    url=url,
                    success=True,
                    entry_count=len(entries),
                    duration_ms=int((time.time() - start_time) * 1000)
                ))
            except Exception as e:
                error_msg = str(e)
                print(f"    [ERROR] {error_msg}")
                self.results.append(FetchResult(
                    source=source,
                    url=url,
                    success=False,
                    entry_count=0,
                    error=error_msg,
                    duration_ms=int((time.time() - start_time) * 1000)
                ))
        
        print("=" * 60)
        success_count = sum(1 for r in self.results if r.success)
        fail_count = len(self.results) - success_count
        print(f"[DONE] {success_count} success, {fail_count} failed")
        print(f"[TOTAL] {len(all_entries)} entries fetched")
        
        return all_entries, self.results
    
    def save_to_feishu(self, entries: List[FeedEntry], table_id: str = "raw") -> Optional[str]:
        """Save entries to Feishu bitable"""
        
        if not entries:
            print("[Feishu] No data to write")
            return None
        
        try:
            target_table = FEISHU_CONFIG["table_id_raw"] if table_id == "raw" else FEISHU_CONFIG["table_id_clean"]
            
            print(f"\n[Feishu] Writing {len(entries)} records to {target_table}...")
            
            # Prepare records for Feishu
            records = []
            for entry in entries:
                # Build fields dynamically based on what's available
                fields = {
                    "采集轮次": entry.record_id,
                    "采集时间": entry.fetch_time,
                    "搜索关键词": entry.keyword,
                    "信息源": entry.source,
                    "标题": entry.title,  # 中英文对照
                    "原文内容": entry.content,  # 中英文对照
                    "原文链接": entry.link,
                }
                
                # Add English original fields if translated
                if entry.title_en:
                    fields["标题 (英文)"] = entry.title_en
                if entry.content_en:
                    fields["原文内容 (英文)"] = entry.content_en
                if entry.published:
                    fields["发布时间"] = entry.published
                if entry.author:
                    fields["作者"] = entry.author
                
                # Add translation flag
                fields["是否翻译"] = "是" if entry.is_translated else "否"
                
                record = {"fields": fields}
                records.append(record)
            
            # Use Feishu API via subprocess call
            # This will be handled by the agent session
            print(f"[Feishu] Data prepared, calling Feishu API...")
            
            # Save data for Feishu write
            feishu_data = {
                "action": "batch_create",
                "app_token": FEISHU_CONFIG["app_token"],
                "table_id": target_table,
                "records": records
            }
            
            # Write to temp file for agent to process
            temp_path = OUTPUT_DIR / "feishu-pending.json"
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(feishu_data, f, ensure_ascii=False, indent=2)
            
            print(f"[Feishu] Pending file created: {temp_path}")
            print(f"[Feishu] Agent will process this file and write to Feishu")
            
            return str(temp_path)
            
        except Exception as e:
            print(f"[Feishu] Warning: {e}")
            return self._save_feishu_json(entries, table_id)
        except Exception as e:
            print(f"[Feishu] ✗ Error: {e}")
            return self._save_feishu_json(entries, table_id)
    
    def _save_feishu_json(self, entries: List[FeedEntry], table_id: str) -> str:
        """Save Feishu data as JSON fallback"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = OUTPUT_DIR / f"rss-feishu-{timestamp}.json"
        
        data = {
            "app_token": FEISHU_CONFIG["app_token"],
            "table_id": FEISHU_CONFIG["table_id_raw"] if table_id == "raw" else FEISHU_CONFIG["table_id_clean"],
            "records": [asdict(e) for e in entries]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[Feishu] Saved to JSON: {output_path}")
        return str(output_path)
    
    def save_to_json(self, entries: List[FeedEntry]) -> str:
        """Save entries to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = OUTPUT_DIR / f"rss-feed-{timestamp}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)
        
        print(f"[SAVE] JSON: {output_path}")
        return str(output_path)
    
    def save_to_markdown(self, entries: List[FeedEntry]) -> str:
        """Save entries to Markdown file"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = OUTPUT_DIR / f"rss-feed-{timestamp}.md"
        
        by_source = {}
        for entry in entries:
            if entry.source not in by_source:
                by_source[entry.source] = []
            by_source[entry.source].append(entry)
        
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
    
    def check_failures(self) -> Optional[AlertMessage]:
        """Check for failures and generate alert"""
        failed = [r for r in self.results if not r.success]
        
        if not failed:
            return None
        
        fail_rate = len(failed) / len(self.results) * 100
        
        if fail_rate < 50:
            return None
        
        alert = AlertMessage(
            level="error" if fail_rate > 80 else "warning",
            title=f"RSS Fetch Alert ({len(failed)}/{len(self.results)})",
            message=f"Failure rate: {fail_rate:.1f}%\n\nFailed feeds:\n" + "\n".join([
                f"- {r.source}: {r.error}" for r in failed
            ]),
            failed_feeds=[r.source for r in failed],
            timestamp=datetime.now().isoformat()
        )
        
        return alert
    
    def send_alert(self, alert: AlertMessage) -> str:
        """Send alert message"""
        print(f"\n[ALERT] {alert.level.upper()}: {alert.title}")
        print(alert.message)
        
        # Save alert to file
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        alert_path = OUTPUT_DIR / f"rss-alert-{timestamp}.json"
        
        with open(alert_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(alert), f, ensure_ascii=False, indent=2)
        
        print(f"[ALERT] Saved to: {alert_path}")
        
        # TODO: Send Feishu message
        # from feishu_im_user_message import feishu_im_user_message
        # feishu_im_user_message(...)
        
        return str(alert_path)
    
    def print_summary(self, entries: List[FeedEntry]):
        """Print summary"""
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

# ==================== Main Function ====================

def main(mode: str = "core", limit: int = 10, feishu: bool = False):
    """Main entry point"""
    
    print("\n" + "=" * 60)
    print("[Intel Officer] RSS Grabber Skill v1.0")
    print("=" * 60)
    print(f"Mode: {mode}")
    print(f"Limit: {limit} per feed")
    print(f"Feishu: {feishu}")
    print(f"Retry: {RETRY_CONFIG['max_attempts']} attempts, {RETRY_CONFIG['backoff']}x backoff")
    print("=" * 60)
    
    grabber = RSSGrabber()
    
    # Fetch
    entries, results = grabber.fetch_all(mode=mode, limit=limit)
    
    if not entries:
        print("\n[ERROR] No entries fetched")
        return False
    
    # Summary
    grabber.print_summary(entries)
    
    # Save files
    json_path = grabber.save_to_json(entries)
    md_path = grabber.save_to_markdown(entries)
    
    # Save to Feishu
    feishu_path = None
    if feishu:
        feishu_path = grabber.save_to_feishu(entries, table_id="raw")
    
    # Check alerts
    alert = grabber.check_failures()
    if alert:
        grabber.send_alert(alert)
        if alert.level == "error":
            return False
    
    print(f"\n[DONE] Complete!")
    print(f"  - JSON: {json_path}")
    print(f"  - MD: {md_path}")
    if feishu_path:
        print(f"  - Feishu: {feishu_path}")
    
    return True

# ==================== CLI Entry ====================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Intel Officer RSS Grabber Skill")
    parser.add_argument("--mode", choices=["core", "extended"], default="core")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--feishu", action="store_true")
    
    args = parser.parse_args()
    
    success = main(mode=args.mode, limit=args.limit, feishu=args.feishu)
    sys.exit(0 if success else 1)
