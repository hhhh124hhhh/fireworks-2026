"""
Grok Imagine API - AI 图像和视频生成

集成 xAI Grok Imagine API 用于图像生成、编辑和视频生成。
"""

import os
import base64
import asyncio
import httpx
from pathlib import Path
from typing import Optional, Literal

# 默认配置
XAI_API_KEY = os.getenv('XAI_API_KEY', '')
IMAGE_API_BASE = "https://api.x.ai/v1/images/generations"
VIDEO_API_BASE = "https://api.x.ai/v1/video/generate"


class GrokImagineClient:
    """Grok Imagine API 客户端"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端

        Args:
            api_key: xAI API Key（默认从环境变量 XAI_API_KEY 获取）
        """
        self.api_key = api_key or XAI_API_KEY
        if not self.api_key:
            raise ValueError("需要提供 XAI_API_KEY")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    # ====== 图像生成 ======

    async def generate_image(
        self,
        prompt: str,
        model: str = "grok-imagine-image",
        image_format: Literal["url", "base64"] = "url",
        aspect_ratio: Optional[str] = None,
        n: int = 1
    ) -> dict:
        """
        生成图像

        Args:
            prompt: 图像描述
            model: 模型名称（默认：grok-imagine-image）
            image_format: 输出格式（url 或 base64）
            aspect_ratio: 宽高比（例如：4:3）
            n: 生成图像数量（最多 10）

        Returns:
            API 响应
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "response_format": image_format
        }

        if aspect_ratio:
            payload["aspect_ratio"] = aspect_ratio

        if n > 1:
            payload["n"] = min(n, 10)

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                IMAGE_API_BASE,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def edit_image(
        self,
        prompt: str,
        image_bytes: bytes,
        model: str = "grok-imagine-image",
        image_format: Literal["url", "base64"] = "url"
    ) -> dict:
        """
        编辑图像

        Args:
            prompt: 编辑提示
            image_bytes: 原始图像字节数据
            model: 模型名称
            image_format: 输出格式

        Returns:
            API 响应
        """
        # 转换为 base64
        base64_string = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/jpeg;base64,{base64_string}"

        payload = {
            "model": model,
            "image_url": image_url,
            "prompt": prompt,
            "response_format": image_format
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                IMAGE_API_BASE,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    # ====== 视频生成 ======

    async def generate_video(
        self,
        prompt: str,
        model: str = "grok-imagine-video",
        duration: int = 5,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        auto_poll: bool = True
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

        Returns:
            API 响应（包含视频 URL）
        """
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
                VIDEO_API_BASE,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()

            result = response.json()

            # 如果启用自动轮询，等待视频生成完成
            if auto_poll and "request_id" in result:
                request_id = result["request_id"]
                video_result = await self.poll_video_result(request_id)
                return video_result

            return result

    async def generate_video_from_image(
        self,
        prompt: str,
        image_url: str,
        model: str = "grok-imagine-video",
        duration: int = 5,
        aspect_ratio: str = "16:9",
        resolution: str = "720p",
        auto_poll: bool = True
    ) -> dict:
        """
        从图像生成视频

        Args:
            prompt: 视频描述
            image_url: 图像 URL
            model: 模型名称
            duration: 视频时长
            aspect_ratio: 宽高比
            resolution: 分辨率
            auto_poll: 是否自动轮询结果

        Returns:
            API 响应
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "image_url": image_url,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                VIDEO_API_BASE,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()

            result = response.json()

            # 如果启用自动轮询，等待视频生成完成
            if auto_poll and "request_id" in result:
                request_id = result["request_id"]
                video_result = await self.poll_video_result(request_id)
                return video_result

            return result

    async def edit_video(
        self,
        prompt: str,
        video_url: str,
        model: str = "grok-imagine-video",
        auto_poll: bool = True
    ) -> dict:
        """
        编辑视频

        Args:
            prompt: 编辑提示
            video_url: 原始视频 URL
            model: 模型名称
            auto_poll: 是否自动轮询结果

        Returns:
            API 响应
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "video_url": video_url
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                VIDEO_API_BASE,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()

            result = response.json()

            # 如果启用自动轮询，等待视频编辑完成
            if auto_poll and "request_id" in result:
                request_id = result["request_id"]
                video_result = await self.poll_video_result(request_id)
                return video_result

            return result

    async def start_video_generation(
        self,
        prompt: str,
        model: str = "grok-imagine-video",
        duration: int = 5,
        aspect_ratio: str = "16:9",
        resolution: str = "720p"
    ) -> dict:
        """
        开始视频生成（返回 request_id）

        Args:
            prompt: 视频描述
            model: 模型名称
            duration: 视频时长
            aspect_ratio: 宽高比
            resolution: 分辨率

        Returns:
            包含 request_id 的响应
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                VIDEO_API_BASE,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_video_result(self, request_id: str) -> dict:
        """
        获取视频生成结果

        Args:
            request_id: 请求 ID

        Returns:
            视频生成结果
        """
        url = f"{VIDEO_API_BASE}/{request_id}"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def poll_video_result(self, request_id: str, max_attempts: int = 60, poll_interval: float = 5.0) -> dict:
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
                if result.get("status") == "succeeded":
                    return result
                elif result.get("status") == "failed":
                    return result
                elif result.get("status") in ["pending", "in_progress"]:
                    print(f"视频生成中... ({attempt + 1}/{max_attempts})")
                    await asyncio.sleep(poll_interval)
                    continue

            except Exception as e:
                print(f"轮询错误: {e}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(poll_interval)
                    continue
                else:
                    raise

        raise TimeoutError(f"视频生成超时（{max_attempts * poll_interval} 秒）")


# ====== 同步 API ======

def generate_image_sync(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "grok-imagine-image",
    image_format: Literal["url", "base64"] = "url",
    aspect_ratio: Optional[str] = None,
    n: int = 1
) -> dict:
    """
    同步生成图像
    """
    client = GrokImagineClient(api_key)
    return asyncio.run(client.generate_image(
        prompt=prompt,
        model=model,
        image_format=image_format,
        aspect_ratio=aspect_ratio,
        n=n
    ))


def generate_video_sync(
    prompt: str,
    api_key: Optional[str] = None,
    model: str = "grok-imagine-video",
    duration: int = 5,
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
    auto_poll: bool = True
) -> dict:
    """
    同步生成视频
    """
    client = GrokImagineClient(api_key)
    return asyncio.run(client.generate_video(
        prompt=prompt,
        model=model,
        duration=duration,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        auto_poll=auto_poll
    ))


# ====== CLI 接口 ======

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Grok Imagine API - AI 图像和视频生成")
    parser.add_argument("--api-key", help="xAI API Key（默认从环境变量 XAI_API_KEY 读取）")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 生成图像命令
    gen_image_parser = subparsers.add_parser("image", help="生成图像")
    gen_image_parser.add_argument("prompt", help="图像描述")
    gen_image_parser.add_argument("--model", default="grok-imagine-image", help="模型名称")
    gen_image_parser.add_argument("--format", choices=["url", "base64"], default="url", help="输出格式")
    gen_image_parser.add_argument("--aspect-ratio", help="宽高比（例如：4:3）")
    gen_image_parser.add_argument("-n", type=int, default=1, help="生成数量（最多 10）")

    # 生成视频命令
    gen_video_parser = subparsers.add_parser("video", help="生成视频")
    gen_video_parser.add_argument("prompt", help="视频描述")
    gen_video_parser.add_argument("--model", default="grok-imagine-video", help="模型名称")
    gen_video_parser.add_argument("--duration", type=int, default=5, help="视频时长（1-15 秒）")
    gen_video_parser.add_argument("--aspect-ratio", default="16:9", help="宽高比（默认：16:9）")
    gen_video_parser.add_argument("--resolution", choices=["720p", "480p"], default="720p", help="分辨率")
    gen_video_parser.add_argument("--no-poll", action="store_true", help="不自动轮询结果")

    args = parser.parse_args()

    if args.command == "image":
        result = generate_image_sync(
            prompt=args.prompt,
            api_key=args.api_key,
            model=args.model,
            image_format=args.format,
            aspect_ratio=args.aspect_ratio,
            n=args.n
        )
        print("图像生成成功！")
        if args.format == "url" and "url" in result:
            print(f"图像 URL: {result['url']}")
        else:
            print(f"结果: {result}")

    elif args.command == "video":
        print("开始生成视频...")
        result = generate_video_sync(
            prompt=args.prompt,
            api_key=args.api_key,
            model=args.model,
            duration=args.duration,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            auto_poll=not args.no_poll
        )

        print("视频生成成功！")
        if "url" in result:
            print(f"视频 URL: {result['url']}")
        else:
            print(f"结果: {result}")

    else:
        parser.print_help()
