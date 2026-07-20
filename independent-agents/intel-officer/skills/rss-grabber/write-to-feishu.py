#!/usr/bin/env python3
"""Write RSS data to Feishu bitable"""

import json
from pathlib import Path

# Read pending file
pending_file = Path("skills/rss-grabber/output/feishu-pending.json")
with open(pending_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Records to write: {len(data['records'])}")
print(f"Table ID: {data['table_id']}")
print(f"App Token: {data['app_token']}")

# Output for tool call
print("\n=== Tool Call Arguments ===")
print(f"action: {data['action']}")
print(f"app_token: {data['app_token']}")
print(f"table_id: {data['table_id']}")
print(f"records: {json.dumps(data['records'], ensure_ascii=False)}")
