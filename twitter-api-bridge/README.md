# Twitter API Bridge

**使用 Nitter 镜像站的免费 Twitter/X API 替代方案**

无需官方 Twitter API Key，完全免费！

## ✨ 特性

- 🚀 **无需 API Key** - 使用公开的 Nitter 镜像站
- 🔄 **自动重试** - 自动切换不同的 Nitter 实例
- ✅ **自我检查** - 自动检测和修复抓取问题
- 🔄 **自循环** - 定期检查确保持续可用
- 📊 **健康监控** - 完整的统计和监控信息
- 🛡️ **错误处理** - 优雅的错误处理和恢复

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /root/clawd
python3 -m venv venv
source venv/bin/activate
pip install ntscraper flask flask-cors
```

### 2. 启动服务

```bash
cd /root/clawd/twitter-api-bridge
chmod +x start.sh
./start.sh
```

服务将在 `http://0.0.0.0:5000` 启动。

### 3. 测试 API

```bash
cd /root/clawd/twitter-api-bridge
python3 test_api.py
```

## 📡 API 端点

### 1. 健康检查

```bash
GET /health
```

响应示例:
```json
{
  "status": "healthy",
  "uptime": "0:05:23.123456",
  "statistics": {
    "total_requests": 15,
    "successful_requests": 12,
    "failed_requests": 3,
    "success_rate": "80.00%"
  },
  "instances": {
    "working": ["https://nitter.net", "https://nitter.poast.org"],
    "failed": []
  }
}
```

### 2. 获取用户推文

```bash
GET /api/user/<username>?mode=user&num=20
```

参数:
- `mode`: 抓取模式
  - `user` - 用户推文（默认）
  - `faves` - 用户点赞
  - `media` - 媒体推文
  - `replies` - 回复
- `num`: 获取数量（默认 20）

示例:
```bash
# 获取 @elonmusk 的推文
curl http://localhost:5000/api/user/elonmusk?num=10

# 获取 @OpenAI 的媒体推文
curl http://localhost:5000/api/user/OpenAI?mode=media&num=5
```

响应示例:
```json
{
  "success": true,
  "username": "elonmusk",
  "count": 10,
  "data": {
    "tweets": [
      {
        "date": "2026-01-30",
        "text": "Hello world!",
        "stats": {
          "comments": 100,
          "retweets": 500,
          "likes": 2000
        },
        "user": {
          "name": "Elon Musk",
          "username": "elonmusk"
        }
      }
    ]
  },
  "instance": "https://nitter.net"
}
```

### 3. 搜索推文

```bash
GET /api/search?q=关键词&mode=term&num=20
```

参数:
- `q`: 搜索关键词（必需）
- `mode`: 搜索模式
  - `term` - 关键词搜索（默认）
  - `hashtag` - 标签搜索
  - `user` - 用户搜索
- `num`: 获取数量（默认 20）

示例:
```bash
# 搜索 "AI"
curl http://localhost:5000/api/search?q=AI&num=10

# 搜索标签 "#AI"
curl http://localhost:5000/api/search?q=AI&mode=hashtag&num=5
```

### 4. 自我检查

```bash
POST /api/self-check
```

测试抓取功能是否正常工作。

响应示例:
```json
{
  "check_time": "2026-01-30T11:30:00",
  "status": "healthy",
  "summary": {
    "total": 3,
    "passed": 3,
    "failed": 0
  },
  "tests": [
    {
      "name": "Test: OpenAI",
      "status": "passed",
      "instance": "https://nitter.net"
    }
  ]
}
```

## 🔁 自循环功能

### 启动自动检查守护进程

```bash
cd /root/clawd/twitter-api-bridge
source ../venv/bin/activate
python3 auto_check.py
```

这个守护进程会:
- 每 5 分钟检查一次服务健康状态
- 定期执行自我检查
- 自动记录问题
- 确保抓取功能持续可用

### 使用 Cron 定期检查

将以下行添加到 crontab (`crontab -e`):

```bash
*/5 * * * * cd /root/clawd/twitter-api-bridge && source ../venv/bin/activate && python3 -c "import requests; requests.post('http://localhost:5000/api/self-check')"
```

这会每 5 分钟自动执行一次自我检查。

## 🧪 测试

运行完整测试套件:

```bash
cd /root/clawd/twitter-api-bridge
python3 test_api.py
```

测试内容:
1. ✓ 健康检查
2. ✓ 获取用户推文
3. ✓ 搜索推文
4. ✓ 自我检查

## 🐛 故障排除

### 问题: 所有实例都失败

**原因**: Nitter 镜像站可能不稳定或被封锁

**解决方案**:
1. 等待几分钟再试
2. 检查网络连接
3. 查看日志了解详细错误
4. 在 `NITTER_INSTANCES` 列表中添加新的镜像站

### 问题: 抓取速度慢

**原因**: 某些 Nitter 实例较慢

**解决方案**: 系统会自动切换到更快的实例，无需手动干预。

### 问题: 部分推文无法获取

**原因**: Nitter 镜像站的数据可能不完整

**解决方案**: 这是正常现象，尝试使用不同的 Nitter 实例。

## 📝 使用示例

### Python 示例

```python
import requests

# 获取用户推文
response = requests.get('http://localhost:5000/api/user/elonmusk?num=5')
data = response.json()

if data['success']:
    for tweet in data['data']['tweets']:
        print(f"{tweet['date']}: {tweet['text']}")
else:
    print(f"错误: {data['error']}")

# 搜索推文
response = requests.get('http://localhost:5000/api/search?q=AI&num=10')
data = response.json()

if data['success']:
    for tweet in data['data']['tweets']:
        print(f"@{tweet['user']['username']}: {tweet['text']}")
```

### Bash 示例

```bash
# 获取用户推文
curl -s http://localhost:5000/api/user/OpenAI | jq '.data.tweets[] | .text'

# 搜索并统计
curl -s http://localhost:5000/api/search?q=AI | jq '.count'

# 检查健康状态
curl -s http://localhost:5000/health | jq '.statistics'
```

## 📊 监控

查看实时统计:

```bash
curl http://localhost:5000/health | jq
```

关键指标:
- `total_requests` - 总请求数
- `successful_requests` - 成功请求数
- `failed_requests` - 失败请求数
- `success_rate` - 成功率
- `working_instances` - 可用的 Nitter 实例
- `failed_instances` - 失败的 Nitter 实例

## 🔒 安全性

- 此服务仅访问公开的 Twitter/X 数据
- 不需要任何 API Key 或认证
- 可以通过防火墙限制访问端口 5000

## 📜 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

---

**提示**: Twitter/X 官方 API 需要付费，这个方案使用公开的 Nitter 镜像站作为替代，完全免费！
