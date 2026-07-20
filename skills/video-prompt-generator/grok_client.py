"""
Grok Imagine Client - 视频生成客户端

集成 XAI Grok Imagine API 用于视频生成
"""

import os
import asyncio
import httpx
from typing import Optional, Literal


class GrokImagineClient:
    """Grok Imagine API 客户端 - 视频生成专用"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端

        Args:
            api_key: xAI API Key（默认从环境变量 XAI_API_KEY 获取）
        """
        self.api_key = api_key or os.getenv('XAI_API_KEY', '')
        if not self.api_key:
            raise ValueError("需要提供 XAI_API_KEY，可通过环境变量或参数设置")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # API 端点
        self.video_api_base = "https://api.x.ai/v1/video/generate"

    async def generate_video(
        self,
        prompt: str,
        model: str = "grok-imagine-video",
        duration: int = 5,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        auto_poll: bool = True,
        poll_interval: float = 5.0,
        max_attempts: int = 60
    ) -> dict:
        """
        生成视频

        Args:
            prompt: 视频描述
            model: 模型名称（默认：grok-imagine-video）
            duration: 视频时长（秒，1-15）
            aspect_ratio: 宽高比（默认：16:9）
            resolution: 分辨率（720p 或 480p）
            auto_poll: 是否自动轮询结果
            poll_interval: 轮询间隔（秒）
            max_attempts: 最大轮询次数

        Returns:
            API 响应（包含视频 URL）
        """
        # 验证参数
        if not 1 <= duration <= 15:
            raise ValueError("视频时长必须在 1-15 秒之间")

        if resolution not in ["720p", "480p"]:
            raise ValueError("分辨率必须是 720p 或 480p")

        # 构建请求 payload
        payload = {
            "model": model,
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            # 发送生成请求
            response = await client.post(
                self.video_api_base,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()

            result = response.json()

            # 如果启用自动轮询，等待视频生成完成
            if auto_poll and "request_id" in result:
                request_id = result["request_id"]
                print(f"📹 视频生成请求已提交，Request ID: {request_id}")

                try:
                    video_result = await self.poll_video_result(
                        request_id,
                        max_attempts=max_attempts,
                        poll_interval=poll_interval
                    )
                    return video_result
                except TimeoutError as e:
                    return {
                        "status": "timeout",
                        "request_id": request_id,
                        "error": str(e),
                        "poll_url": f"{self.video_api_base}/{request_id}"
                    }

            return result

    async def get_video_result(self, request_id: str) -> dict:
        """
        获取视频生成结果

        Args:
            request_id: 请求 ID

        Returns:
            视频生成结果
        """
        url = f"{self.video_api_base}/{request_id}"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def poll_video_result(
        self,
        request_id: str,
        max_attempts: int = 60,
        poll_interval: float = 5.0
    ) -> dict:
        """
        轮询视频生成结果

        Args:
            request_id: 请求 ID
            max_attempts: 最大尝试次数
            poll_interval: 轮询间隔（秒）

        Returns:
            最终的视频结果
        """
        for attempt in range(max_attempts):
            try:
                result = await self.get_video_result(request_id)

                # 检查状态
                status = result.get("status", "unknown")

                if status == "succeeded":
                    print(f"✅ 视频生成成功！")
                    return result
                elif status == "failed":
                    error = result.get("error", "未知错误")
                    print(f"❌ 视频生成失败: {error}")
                    return result
                elif status in ["pending", "in_progress", "processing"]:
                    progress_percent = int((attempt + 1) / max_attempts * 100)
                    print(f"⏳ 视频生成中... ({status}) ({progress_percent}%)")
                    await asyncio.sleep(poll_interval)
                    continue
                else:
                    # 未知状态，继续等待
                    print(f"⏳ 等待中... 状态: {status}")
                    await asyncio.sleep(poll_interval)
                    continue

            except httpx.HTTPStatusError as e:
                print(f"⚠️  轮询错误: HTTP {e.response.status_code}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(poll_interval)
                    continue
                else:
                    raise

            except Exception as e:
                print(f"⚠️  轮询错误: {e}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(poll_interval)
                    continue
                else:
                    raise

        raise TimeoutError(
            f"视频生成超时（{max_attempts * poll_interval} 秒）\n"
            f"Request ID: {request_id}\n"
            f"可以稍后使用 GET {self.video_api_base}/{request_id} 查询结果"
        )


# ====== 同步 API ======

def generate_video_sync(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "grok-imagine-video",
    duration: int = 5,
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
    auto_poll: bool = True,
    poll_interval: float = 5.0,
    max_attempts: int = 60
) -> dict:
    """
    同步生成视频

    Args:
        prompt: 视频描述
        api_key: xAI API Key
        model: 模型名称
        duration: 视频时长
        aspect_ratio: 宽高比
        resolution: 分辨率
        auto_poll: 是否自动轮询
        poll_interval: 轮询间隔
        max_attempts: 最大轮询次数

    Returns:
        视频生成结果
    """
    client = GrokImagineClient(api_key)
    return asyncio.run(client.generate_video(
        prompt=prompt,
        model=model,
        duration=duration,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        auto_poll=auto_poll,
        poll_interval=poll_interval,
        max_attempts=max_attempts
    ))


def get_video_result_sync(
    request_id: str,
    api_key: Optional[str] = None
) -> dict:
    """
    同步获取视频结果

    Args:
        request_id: 请求 ID
        api_key: xAI API Key

    Returns:
        视频生成结果
    """
    client = GrokImagineClient(api_key)
    return asyncio.run(client.get_video_result(request_id))


# ====== 测试函数 ======

if __name__ == "__main__":
    # 测试视频生成
    import sys

    if len(sys.argv) < 2:
        print("用法: python grok_client.py <prompt> [duration] [aspect_ratio]")
        print("示例: python grok_client.py '一只可爱的猫咪在花园里玩耍' 5 16:9")
        sys.exit(1)

    prompt = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    aspect_ratio = sys.argv[3] if len(sys.argv) > 3 else "16:9"

    print(f"🎬 开始生成视频...")
    print(f"📝 提示词: {prompt}")
    print(f"⏱️  时长: {duration}秒")
    print(f"📐 宽高比: {aspect_ratio}")
    print()

    result = generate_video_sync(
        prompt=prompt,
        duration=duration,
        aspect_ratio=aspect_ratio
    )

    print()
    print("="*60)
    if result.get("status") == "succeeded":
        print("✅ 视频生成成功！")
        if "url" in result:
            print(f"📹 视频 URL: {result['url']}")
    elif result.get("status") == "timeout":
        print("⏱️  视频生成超时，但请求已提交")
        if "poll_url" in result:
            print(f"🔗 查询地址: {result['poll_url']}")
    else:
        print(f"❌ 视频生成失败")
        if "error" in result:
            print(f"错误信息: {result['error']}")

    print("="*60)
