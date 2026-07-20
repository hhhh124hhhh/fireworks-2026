"""
Fetcher Package - 热点抓取模块
每个平台一个独立模块，便于维护和扩展
"""

from .zhihu import fetch_zhihu
from .weibo import fetch_weibo
from .bilibili import fetch_bilibili
from .newsnow import fetch_from_newsnow_mcp

__all__ = [
    'fetch_zhihu',
    'fetch_weibo',
    'fetch_bilibili',
    'fetch_from_newsnow_mcp',
]
