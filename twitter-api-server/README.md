# 私有 Twitter API 服务器

使用 `ntscraper` + FastAPI 构建的免费 Twitter API 代理服务，无需官方 Twitter API Key。

## ✨ 特性

- 🆓 **完全免费** - 通过 Nitter 镜像获取数据，无需付费 API
- 🔍 **搜索推文** - 支持关键词搜索和话题标签搜索
- 👤 **获取用户推文** - 获取指定用户的推文
- 📋 **用户资料** - 获取用户的详细信息
- 🚀 **快速响应** - 基于 FastAPI 高性能框架
- 📚 **自动文档** - 提供 Swagger UI 和 ReDoc 文档

## 📦 安装

### 方法 1: 使用启动脚本（推荐）

```bash
cd /root/clawd/twitter-api-server
chmod +x start.sh
./start.sh
```

### 方法 2: 手动安装

```bash
# 创建虚拟环境
cd /root/clawd/twitter-api-server
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务器
python3 main.py
```

### 方法 3: 使用 systemd（生产环境）

```bash
# 复制服务文件
sudo cp twitter-api.service /etc/systemd/system/

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable twitter-api
sudo systemctl start twitter-api

# 查看状态
sudo systemctl status twitter-api

# 查看日志
sudo journalctl -u twitter-api -f
```

## 🚀 启动后

服务器启动后，访问：

- **API 基础地址**: `http://YOUR_SERVER_IP:8000`
- **API 文档**: `http://YOUR_SERVER_IP:8000/docs`
- **ReDoc 文档**: `http://YOUR_SERVER_IP:8000/redoc`

## 🔌 API 接口

### 1. 搜索推文

```
GET /api/tweets/search
```

参数:
- `term` (必填): 搜索关键词
- `mode` (可选): 搜索模式，`term` 或 `hashtag`，默认 `term`
- `number` (可选): 返回数量 (1-100)，默认 10
- `since` (可选): 起始日期 `YYYY-MM-DD`
- `until` (可选): 结束日期 `YYYY-MM-DD`

示例:
```bash
curl "http://localhost:8000/api/tweets/search?term=AI+prompt&number=5"
```

### 2. 获取用户推文

```
GET /api/tweets/user/{username}
```

参数:
- `username` (路径参数): Twitter 用户名（不含 @）
- `number` (可选): 返回数量 (1-100)，默认 10
- `replies` (可选): 是否包含回复，默认 false

示例:
```bash
curl "http://localhost:8000/api/tweets/user/openai?number=5"
```

### 3. 获取用户资料

```
GET /api/user/{username}
```

参数:
- `username` (路径参数): Twitter 用户名（不含 @）

示例:
```bash
curl "http://localhost:8000/api/user/openai"
```

### 4. 健康检查

```
GET /api/health
```

## 🧪 测试

运行测试脚本：

```bash
python3 test_api.py
```

**注意**: 测试前需要先启动服务器。

## 🔧 配置

### 修改端口号

编辑 `main.py` 最后一行：

```python
uvicorn.run(app, host="0.0.0.0", port=YOUR_PORT)
```

### CORS 配置

在 `main.py` 中修改 CORS 中间件配置：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # 限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 使用示例

### Python 示例

```python
import requests

# 搜索推文
response = requests.get(
    "http://localhost:8000/api/tweets/search",
    params={"term": "AI prompt", "number": 10}
)
tweets = response.json()

for tweet in tweets:
    print(f"{tweet['date']}: {tweet['text']}")
    print(f"链接: {tweet['link']}")
    print(f"点赞: {tweet['stats']['likes']}\n")
```

### JavaScript/Node.js 示例

```javascript
const axios = require('axios');

async function searchTweets(term) {
    const response = await axios.get('http://localhost:8000/api/tweets/search', {
        params: { term, number: 10 }
    });

    response.data.forEach(tweet => {
        console.log(`${tweet.date}: ${tweet.text}`);
        console.log(`链接: ${tweet.link}\n`);
    });
}

searchTweets('AI prompt');
```

## ⚠️ 限制

由于使用 Nitter 镜像，可能存在以下限制：

1. **速度限制** - Nitter 实例可能有速率限制
2. **实例可用性** - 部分镜像可能不稳定或离线
3. **数据延迟** - 与官方 API 相比，数据可能有延迟
4. **功能限制** - 某些高级功能可能不可用

## 🔄 替换 Nitter 实例

如果默认 Nitter 实例不可用，可以修改 `main.py` 中的实例列表：

```python
scraper = Nitter(
    log_level=1,
    skip_instance_check=False
)
```

`ntscraper` 会自动尝试不同的 Nitter 实例。

## 🛠 故障排除

### 问题: 请求超时或失败

**解决方案**:
- 检查 Nitter 实例是否可用
- 尝试减少 `number` 参数
- 等待一段时间后重试

### 问题: 端口被占用

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

### 问题: 依赖安装失败

**解决方案**:
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 📦 项目结构

```
twitter-api-server/
├── main.py                 # 主应用文件
├── requirements.txt        # 依赖列表
├── start.sh               # 启动脚本
├── test_api.py            # 测试脚本
├── twitter-api.service    # systemd 服务文件
└── README.md              # 本文档
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [ntscraper](https://github.com/balibouse/ntscraper) - Nitter 抓取库
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Web 框架
- [Nitter](https://github.com/zedeus/nitter) - Twitter 的开源前端
