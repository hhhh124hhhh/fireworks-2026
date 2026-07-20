#!/usr/bin/env python3
import re
import json
from datetime import datetime

# 更新统计数据
stats = {
  "skills": 100,
  "automation_flows": 50,
  "community_participation": "30K+",
  "curiosity": "∞",
  "last_updated": datetime.now().isoformat()
}

# 更新 HTML
with open('index.html', 'r', encoding='utf-8') as f:
  content = f.read()

# 更新技能数
content = re.sub(
  r'<div class="stat-number">\d+</div>\s*<div class="stat-label">AI 技能开发</div>',
  f'<div class="stat-number">{stats["skills"]}</div>\n                  <div class="stat-label">AI 技能开发</div>',
  content
)

# 更新自动化流程数
content = re.sub(
  r'<div class="stat-number">\d+</div>\s*<div class="stat-label">自动化流程</div>',
  f'<div class="stat-number">{stats["automation_flows"]}</div>\n                  <div class="stat-label">自动化流程</div>',
  content
)

# 保存
with open('index.html', 'w', encoding='utf-8') as f:
  f.write(content)

print(f"Updated stats: {stats}")
