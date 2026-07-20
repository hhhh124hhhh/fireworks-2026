#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多媒体抓取脚本 - 一键抓取多平台热门内容

支持平台：
- 🎵 抖音 - 视频搜索
- 🔴 小红书 - 笔记搜索
- 📱 微信视频号 - 视频搜索

Usage:
    python scrape.py --keyword "AI工具"
    python scrape.py -k "关键词"
"""

import os
import sys
import base64
import argparse
import subprocess
from datetime import datetime

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


def ensure_dependencies():
    """自动安装缺失的依赖"""
    try:
        import requests
    except ImportError:
        print("正在自动安装依赖: requests...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', '-q'])
            print("依赖安装成功！")
        except subprocess.CalledProcessError as e:
            print(f"自动安装失败: {e}")
            print("请手动运行: pip install requests")
            return False
    return True


# API 配置（已编码）
API_BASE_URL = base64.b64decode('aHR0cHM6Ly9hcGkudGlraHViLmlv').decode()
API_ENDPOINTS = {
    'douyin_search': '/api/v1/douyin/search/fetch_general_search_v2',
    'xiaohongshu_search': '/api/v1/xiaohongshu/web_v2/fetch_search_notes',
    'wechat_channels_search': '/api/v1/wechat_channels/fetch_default_search',
}

# 小红书多端点配置（按优先级排序）
XIAOHONGSHU_ENDPOINTS = [
    {
        'name': 'web_v2_fetch_search_notes',
        'path': '/api/v1/xiaohongshu/web_v2/fetch_search_notes',
        'method': 'GET',
        'params_key': 'keywords',  # 注意：复数形式
        'params': {'keywords': 'keyword', 'page': 'page', 'page_size': 'page_size'}
    },
    {
        'name': 'web_search_notes_v3',
        'path': '/api/v1/xiaohongshu/web/search_notes_v3',
        'method': 'GET',
        'params_key': 'keyword',
        'params': {'keyword': 'keyword', 'page': 'page', 'page_size': 'page_size'}
    },
    {
        'name': 'web_search_notes',
        'path': '/api/v1/xiaohongshu/web/search_notes',
        'method': 'GET',
        'params_key': 'keyword',
        'params': {'keyword': 'keyword', 'page': 'page'}
    },
    {
        'name': 'app_v2_search_notes',
        'path': '/api/v1/xiaohongshu/app_v2/search_notes',
        'method': 'GET',
        'params_key': 'keyword',
        'params': {'keyword': 'keyword', 'page': 'page', 'page_size': 'page_size'}
    },
    {
        'name': 'app_search_notes',
        'path': '/api/v1/xiaohongshu/app/search_notes',
        'method': 'POST',
        'params_key': 'keyword',
        'params': {'keyword': 'keyword', 'page': 'page', 'page_size': 'page_size'}
    },
]


def load_config(args) -> dict:
    """
    加载配置 - 仅支持加密文件方式

    从 encrypted_keys.json 加载加密的 API Key
    """
    config = {'api_key': None}

    try:
        from key_loader import load_api_key
        config['api_key'] = load_api_key()
    except FileNotFoundError:
        print("❌ 未找到加密配置文件 (encrypted_keys.json)")
        print("   请确保文件存在于脚本目录中")
    except Exception as e:
        print(f"❌ 加载加密配置失败: {e}")

    return config


def search_xiaohongshu(keyword: str, api_key: str) -> tuple:
    """
    小红书多端点自动重试搜索

    Returns:
        tuple: (success: bool, data: dict or None, error: str or None, endpoint_name: str or None)
    """
    import requests

    for endpoint in XIAOHONGSHU_ENDPOINTS:
        try:
            url = f"{API_BASE_URL}{endpoint['path']}"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "accept": "application/json"
            }

            # 构建参数
            if endpoint['method'] == 'GET':
                params = {'page': 1}
                if 'keyword' in endpoint['params']:
                    params['keyword'] = keyword
                if 'keywords' in endpoint['params']:
                    params['keywords'] = keyword
                if 'page_size' in endpoint['params']:
                    params['page_size'] = 20

                resp = requests.get(url, headers=headers, params=params, timeout=120)
            else:  # POST
                json_data = {"keyword": keyword, "page": 1}
                if 'count' in endpoint['params']:
                    json_data['count'] = 20
                headers["Content-Type"] = "application/json"
                resp = requests.post(url, headers=headers, json=json_data, timeout=120)

            if resp.ok:
                data = resp.json()
                # 验证数据有效性
                if data.get('data') or data.get('items'):
                    print(f"    ✓ 使用端点: {endpoint['name']}")
                    return True, data, None, endpoint['name']
                else:
                    print(f"    ✗ {endpoint['name']}: 响应数据为空")
            else:
                print(f"    ✗ {endpoint['name']}: {resp.status_code}")

        except Exception as e:
            print(f"    ✗ {endpoint['name']}: {str(e)[:50]}")
            continue

    return False, None, "所有端点均失败", None


def scrape_content(keyword: str, api_key: str, platforms: list = None) -> dict:
    """
    调用 API 抓取数据

    Args:
        keyword: 搜索关键词
        api_key: API Key
        platforms: 要搜索的平台列表，默认为 ['douyin', 'xiaohongshu', 'wechat']

    Returns:
        包含各平台搜索结果的字典
    """
    import requests

    if platforms is None:
        platforms = ['douyin', 'xiaohongshu', 'wechat']

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    results = {}
    errors = []

    # 1. 抖音搜索（POST 方法）
    if 'douyin' in platforms:
        try:
            print("  正在搜索抖音...")
            resp = requests.post(
                f"{API_BASE_URL}{API_ENDPOINTS['douyin_search']}",
                headers=headers,
                json={"keyword": keyword, "count": 20},
                timeout=60
            )
            if resp.ok:
                data = resp.json()
                results['douyin'] = parse_douyin(data)
            else:
                errors.append(f"抖音搜索失败: {resp.status_code} - {resp.text[:200]}")
        except Exception as e:
            errors.append(f"抖音搜索异常: {str(e)}")

    # 2. 小红书搜索（多端点重试）
    if 'xiaohongshu' in platforms:
        try:
            print("  正在搜索小红书...")
            success, data, error, endpoint = search_xiaohongshu(keyword, api_key)
            if success:
                results['xiaohongshu'] = parse_xiaohongshu(data)
            else:
                errors.append(f"小红书搜索失败: {error}")
        except Exception as e:
            errors.append(f"小红书搜索异常: {str(e)}")

    # 3. 微信视频号搜索（POST 方法）
    if 'wechat' in platforms:
        try:
            print("  正在搜索微信视频号...")
            resp = requests.post(
                f"{API_BASE_URL}{API_ENDPOINTS['wechat_channels_search']}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={"keywords": keyword, "count": 20, "page": 1},
                timeout=60
            )
            if resp.ok:
                data = resp.json()
                results['wechat'] = parse_wechat(data)
            else:
                errors.append(f"视频号搜索失败: {resp.status_code} - {resp.text[:200]}")
        except Exception as e:
            errors.append(f"视频号搜索异常: {str(e)}")

    return {
        'success': len(results) > 0,
        'data': results,
        'errors': errors if errors else None
    }


def parse_douyin(data: dict) -> list:
    """解析抖音搜索结果"""
    items = []
    try:
        business_data = data.get('data', {}).get('business_data', [])
        if not business_data:
            business_data = data.get('data', {}).get('data', [])

        for item in business_data:
            if isinstance(item, dict) and 'data' in item:
                aweme_info = item.get('data', {}).get('aweme_info', {})
                if aweme_info:
                    statistics = aweme_info.get('statistics', {})
                    items.append({
                        'title': aweme_info.get('desc', '')[:50] or '无标题',
                        'desc': aweme_info.get('desc', ''),
                        'likes': statistics.get('digg_count', 0),
                        'comments': statistics.get('comment_count', 0),
                        'shares': statistics.get('share_count', 0),
                        'collects': statistics.get('collect_count', 0),
                        'url': f"https://www.douyin.com/video/{aweme_info.get('aweme_id', '')}",
                        'author': aweme_info.get('author', {}).get('nickname', ''),
                    })
            elif isinstance(item, dict):
                statistics = item.get('statistics', {})
                items.append({
                    'title': item.get('desc', '')[:50] or item.get('title', ''),
                    'desc': item.get('desc', ''),
                    'likes': statistics.get('digg_count', 0),
                    'comments': statistics.get('comment_count', 0),
                    'shares': statistics.get('share_count', 0),
                    'collects': statistics.get('collect_count', 0),
                    'url': f"https://www.douyin.com/video/{item.get('aweme_id', '')}",
                    'author': item.get('author', {}).get('nickname', ''),
                })
    except Exception as e:
        print(f"解析抖音数据异常: {e}")
    return items


def parse_xiaohongshu(data: dict) -> list:
    """解析小红书搜索结果（App API 格式）"""
    items = []
    try:
        raw_items = data.get('data', {}).get('data', {}).get('items', [])
        if not raw_items:
            raw_items = data.get('data', {}).get('items', []) or data.get('items', [])

        for item in raw_items:
            note = item.get('note', item)
            if isinstance(note, dict):
                interact_info = note.get('interact_info', {})
                user_info = note.get('user', {})
                note_id = note.get('note_id') or note.get('id', '')
                title = note.get('display_title', '') or note.get('title', '')
                author_name = user_info.get('nickname', '') or note.get('nickname', '')

                items.append({
                    'title': title,
                    'desc': note.get('desc', ''),
                    'likes': interact_info.get('liked_count', 0) or note.get('liked_count', 0),
                    'comments': interact_info.get('comment_count', 0) or note.get('comments_count', 0),
                    'collects': interact_info.get('collected_count', 0) or note.get('collected_count', 0),
                    'url': f"https://www.xiaohongshu.com/explore/{note_id}",
                    'author': author_name,
                    'search_hint': f"小红书App搜索: {title[:20]} @{author_name}" if title else '',
                })
    except Exception as e:
        print(f"解析小红书数据异常: {e}")
    return items


def parse_wechat(data: dict) -> list:
    """解析微信视频号搜索结果"""
    items = []
    try:
        media_list = data.get('data', {}).get('media_list', [])
        if not media_list:
            media_list = data.get('data', {}).get('search_result_list', []) or data.get('data', [])

        for item in media_list:
            object_desc = item.get('object_desc', {})
            title = object_desc.get('description', '')[:50].replace('<em class="highlight">', '').replace('</em>', '') or '无标题'
            author_name = item.get('nickname', '') or object_desc.get('nickname', '')

            items.append({
                'title': title,
                'desc': object_desc.get('description', '').replace('<em class="highlight">', '').replace('</em>', ''),
                'likes': item.get('like_count', 0) or object_desc.get('like_count', 0),
                'comments': item.get('comment_count', 0) or object_desc.get('comment_count', 0),
                'shares': item.get('share_count', 0) or object_desc.get('share_count', 0),
                'url': '',  # 视频号没有公开Web链接
                'author': author_name,
                'search_hint': f"微信视频号搜索: {title[:15]} @{author_name}" if author_name else f"微信视频号搜索: {title[:20]}",
            })
    except Exception as e:
        print(f"解析视频号数据异常: {e}")
    return items


def format_output(result: dict, keyword: str) -> str:
    """格式化输出为 Markdown（飞书友好格式，分平台展示）"""
    if not result.get('success'):
        error_msg = result.get('error', '未知错误')
        if result.get('errors'):
            error_msg += '\n' + '\n'.join(result['errors'])
        return f"❌ 抓取失败：{error_msg}"

    lines = [f"# 🔥 {keyword} 热门内容排行\n"]

    data = result.get('data', {})

    # 平台配置（按展示顺序）
    platform_config = {
        'douyin': {'icon': '🎵', 'name': '抖音'},
        'xiaohongshu': {'icon': '🔴', 'name': '小红书'},
        'wechat': {'icon': '📱', 'name': '视频号'},
    }

    def get_rank_emoji(index: int) -> str:
        if index == 1:
            return "🥇 第1名："
        elif index == 2:
            return "🥈 第2名："
        elif index == 3:
            return "🥉 第3名："
        else:
            return f"第{index}名："

    def format_number(num: int) -> str:
        """格式化数字，大于1万显示为 X.X万"""
        if num >= 10000:
            return f"{num / 10000:.1f}万"
        return str(num)

    def format_platform_section(platform_key: str, config: dict, items: list) -> list:
        """格式化单个平台的输出"""
        section_lines = []

        # 平台标题
        section_lines.append(f"## {config['icon']} {config['name']}\n")

        if not items:
            section_lines.append("暂无数据\n")
            return section_lines

        # 按点赞数降序排序
        sorted_items = sorted(items, key=lambda x: x.get('likes', 0), reverse=True)

        for i, item in enumerate(sorted_items, 1):
            title = item.get('title', '') or item.get('desc', '')[:30] or '无标题'
            author = item.get('author', '')
            likes = item.get('likes', 0)
            comments = item.get('comments', 0)
            shares = item.get('shares', 0)
            collects = item.get('collects', 0)
            url = item.get('url', '')
            search_hint = item.get('search_hint', '')

            # 标题行（带奖牌和点赞数）
            likes_str = format_number(likes)
            if i <= 3:
                section_lines.append(f"{get_rank_emoji(i)}{likes_str}赞 {'🔥' * min(i, 3)}")
            else:
                section_lines.append(f"{get_rank_emoji(i)}{likes_str}赞")

            # 内容标题
            section_lines.append(f"**{title}**")

            # 作者
            if author:
                section_lines.append(f"👤 {author}")

            # 互动数据
            stats = []
            if comments:
                stats.append(f"💬 {format_number(comments)}")
            if shares:
                stats.append(f"🔄 {format_number(shares)}")
            if collects:
                stats.append(f"⭐ {format_number(collects)}")
            if stats:
                section_lines.append(f"{' | '.join(stats)}")

            # 链接或搜索提示
            if url:
                section_lines.append(f"🔗 {url}")
            elif search_hint:
                section_lines.append(f"🔍 {search_hint}")

            section_lines.append("")  # 空行分隔

        return section_lines

    # 按平台分开展示
    total_items = 0
    for platform_key, config in platform_config.items():
        items = data.get(platform_key, [])
        if items:
            total_items += len(items)
            section = format_platform_section(platform_key, config, items)
            lines.extend(section)

    if total_items == 0:
        lines.append("未找到相关内容\n")

    errors = result.get('errors', [])
    if errors:
        lines.append("---\n⚠️ 部分错误\n")
        for err in errors:
            lines.append(f"- {err}\n")

    lines.append(f"\n⏰ 抓取时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='多媒体抓取工具 - 抓取抖音、小红书、视频号热门内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --keyword "AI工具"
  %(prog)s -k "关键词"
  %(prog)s -k "关键词" --json

支持平台:
  - 抖音 🎵
  - 小红书 🔴
  - 微信视频号 📱
        """
    )
    parser.add_argument('--keyword', '-k', required=True, help='搜索关键词')
    parser.add_argument('--json', action='store_true', help='输出原始 JSON')

    args = parser.parse_args()

    # 加载配置（仅支持加密文件方式）
    config = load_config(args)

    if not config.get('api_key'):
        print("❌ 无法加载 API Key")
        print("   请确保 encrypted_keys.json 文件存在且有效")
        sys.exit(1)

    # 安装依赖
    if not ensure_dependencies():
        sys.exit(1)

    # 执行抓取
    print(f"正在抓取关键词: {args.keyword}...")
    print("正在搜索各平台...")

    result = scrape_content(args.keyword, config['api_key'])

    # 输出结果
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result, args.keyword))


if __name__ == '__main__':
    main()
