"""
Private Twitter API Server
使用 ntscraper + FastAPI 构建，无需官方 Twitter API Key
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from ntscraper import Nitter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Private Twitter API",
    description="基于 Nitter 的免费 Twitter API 代理服务",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nitter 实例
scraper = Nitter(
    log_level=1,
    skip_instance_check=False
)


class Tweet(BaseModel):
    """推文模型"""
    date: str
    link: str
    text: str
    stats: Dict[str, int]
    pictures: List[str]
    videos: List[str]
    mentions: List[str]
    external_links: List[str]


class UserProfile(BaseModel):
    """用户资料模型"""
    username: str
    name: str
    bio: str
    stats: Dict[str, int]
    avatar: str
    banner: str


@app.get("/")
async def root():
    """API 根路径"""
    return {
        "message": "Private Twitter API Server",
        "endpoints": {
            "search_tweets": "/api/tweets/search",
            "get_user_tweets": "/api/tweets/user/{username}",
            "get_user_profile": "/api/user/{username}"
        }
    }


@app.get("/api/tweets/search", response_model=List[Tweet])
async def search_tweets(
    term: str = Query(..., description="搜索关键词"),
    mode: str = Query("term", description="搜索模式: term 或 hashtag"),
    number: int = Query(10, ge=1, le=100, description="返回数量"),
    since: Optional[str] = Query(None, description="起始日期 YYYY-MM-DD"),
    until: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD")
):
    """
    搜索推文

    参数:
    - term: 搜索关键词
    - mode: term (关键词搜索) 或 hashtag (话题标签)
    - number: 返回推文数量 (1-100)
    - since: 起始日期
    - until: 结束日期
    """
    try:
        logger.info(f"搜索推文: term={term}, mode={mode}, number={number}")

        tweets = scraper.get_tweets(
            term=term,
            mode=mode,
            number=number,
            since=since,
            until=until
        )

        if not tweets or 'tweets' not in tweets:
            raise HTTPException(status_code=404, detail="未找到推文")

        return tweets['tweets']

    except Exception as e:
        logger.error(f"搜索失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@app.get("/api/tweets/user/{username}", response_model=List[Tweet])
async def get_user_tweets(
    username: str,
    number: int = Query(10, ge=1, le=100, description="返回数量"),
    replies: bool = Query(False, description="是否包含回复")
):
    """
    获取用户的推文

    参数:
    - username: Twitter 用户名（不含 @）
    - number: 返回推文数量 (1-100)
    - replies: 是否包含回复
    """
    try:
        logger.info(f"获取用户推文: username={username}, number={number}")

        tweets = scraper.get_tweets(
            username=username,
            number=number,
            replies=replies
        )

        if not tweets or 'tweets' not in tweets:
            raise HTTPException(status_code=404, detail=f"未找到用户 @{username} 的推文")

        return tweets['tweets']

    except Exception as e:
        logger.error(f"获取失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")


@app.get("/api/user/{username}", response_model=UserProfile)
async def get_user_profile(username: str):
    """
    获取用户资料

    参数:
    - username: Twitter 用户名（不含 @）
    """
    try:
        logger.info(f"获取用户资料: username={username}")

        profile = scraper.get_profile(username)

        if not profile:
            raise HTTPException(status_code=404, detail=f"未找到用户 @{username}")

        return {
            "username": profile.get("username"),
            "name": profile.get("name"),
            "bio": profile.get("bio"),
            "stats": profile.get("stats", {}),
            "avatar": profile.get("avatar"),
            "banner": profile.get("banner")
        }

    except Exception as e:
        logger.error(f"获取用户资料失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取用户资料失败: {str(e)}")


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "private-twitter-api"}


if __name__ == "__main__":
    import uvicorn

    # 启动服务器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
