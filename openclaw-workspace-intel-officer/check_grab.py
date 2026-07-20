import json

with open('tmp/opencli-hotspots-20260328-221227.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"总数据：{data['summary']['total']} 条\n")
print("平台分布:")
for platform, count in data['summary'].items():
    if platform != 'total':
        print(f"  {platform}: {count} 条")

print(f"\n错误数：{len(data.get('errors', []))}")

# 查看每个平台的前 3 条数据
print("\n\n数据样例:")
for platform, pdata in data['platforms'].items():
    items = pdata.get('items', [])
    if items:
        print(f"\n{platform.upper()} (前 3 条):")
        for i, item in enumerate(items[:3], 1):
            print(f"  {i}. {item.get('title', 'N/A')[:60]}")
            print(f"     排名：{item.get('rank', 'N/A')}, 热度：{item.get('hot', item.get('score', 'N/A'))}")
