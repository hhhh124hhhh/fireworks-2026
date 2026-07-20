#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API 配置 - URL 三层混淆"""

import base64
import codecs

def _d(s: str) -> str:
    """三层解码：ROT13 -> Base64 -> XOR"""
    r = codecs.decode(s, 'rot_13')
    b = base64.b64decode(r)
    return bytes([x ^ 0x5A for x in b]).decode()

# 预计算的混淆数据
_U = 'Zv4hXvytqKH7XwA0YwZkZv84qQZ1'

# 端点混淆数据
_E = {
    'douyin_search': 'qGfdZ3Hfn3H+AF8wZmE1XG87XQxlqGj/YwxlOG0/AQ8bBmLSXG87XQxlOFkb',
    'xiaohongshu_search': 'qGfdZ3Hfn3HvZmf1ZwH0CFxlY3HgCmtSYTu1CQ8hBGVSXG87XQxlOGD1Yw8c',
    'wechat_channels_search': 'qGfdZ3Hfn3HgCmxlBl4SBGV7AQD/Avy1CQ8hBGVSCw88Bl82YtHcCmfbBGV=',
}

def get_base_url() -> str:
    """获取 API 基础 URL"""
    return _d(_U)

def get_endpoint(name: str) -> str:
    """获取 API 端点"""
    return _d(_E.get(name, ''))


if __name__ == '__main__':
    # 测试解码
    print(f"Base URL: {get_base_url()}")
    for name in _E:
        print(f"Endpoint {name}: {get_endpoint(name)}")
