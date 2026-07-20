#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API Key 加载器 - 多层混淆保护"""

import base64

# 混淆的 Key 片段
_KEY_PARTS = [
    'NQ92FQ4JMXc8Fy8EMhA/aQRwLy0=',
    'HHN/ZHBfBHxWRQJuTXN7VlxlQmQ=',
    'NwAvKFQTNykrPFYIKAkdSyoTWVk='
]

_XOR_KEYS = [0x46, 0x37, 0x64]

def _decode_part(encoded: str, xor_key: int) -> str:
    """解码单个片段"""
    decoded = base64.b64decode(encoded)
    return bytes([b ^ xor_key for b in decoded]).decode()

def load_api_key() -> str:
    """加载并组装 API Key"""
    parts = []
    for i, part in enumerate(_KEY_PARTS):
        parts.append(_decode_part(part, _XOR_KEYS[i]))
    return ''.join(parts)


if __name__ == '__main__':
    # 测试解码
    key = load_api_key()
    print(f"API Key 长度: {len(key)}")
    print(f"API Key 前缀: {key[:10]}...")
