#!/usr/bin/env python3
"""
Video Prompt Generator - 视频提示词生成器

自动生成高质量视频提示词，并支持调用 XAI Grok Imagine API 生成视频
"""

import argparse
import sys
import json
from typing import List, Optional
from templates import (
    VIDEO_STYLES,
    get_style,
    get_all_styles,
    generate_prompt_variants,
    generate_prompt_from_keywords,
    format_prompt_output
)
from grok_client import generate_video_sync


# ====== CLI 颜色输出 ======

class Colors:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DIM = '\033[2m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header():
    """打印标题"""
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║       🎬 Video Prompt Generator v1.0                    ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}║       高质量视频提示词生成器                              ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.END}")
    print()


def print_error(message: str):
    """打印错误信息"""
    print(f"{Colors.RED}✗ 错误: {message}{Colors.END}")


def print_success(message: str):
    """打印成功信息"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")


def print_info(message: str):
    """打印信息"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")


def list_styles():
    """列出所有可用风格"""
    print(f"{Colors.BOLD}{Colors.CYAN}可用视频风格:{Colors.END}\n")

    for i, (key, style) in enumerate(VIDEO_STYLES.items(), 1):
        print(f"  {Colors.CYAN}{i}. {Colors.BOLD}{style['name']}{Colors.END} ({style['name_en']})")
        print(f"     {style['description']}")
        print(f"     {Colors.DIM}关键词: {', '.join(style['keywords'][:5])}...{Colors.END}")
        print()

    print(f"总计: {len(VIDEO_STYLES)} 种风格")


def generate_prompts(
    topic: Optional[str],
    keywords: Optional[List[str]],
    style_key: str,
    variants: int = 1,
    enhance: bool = True
) -> tuple:
    """
    生成提示词

    Returns:
        (prompts, style)
    """
    # 获取风格
    style = get_style(style_key)
    if not style:
        print_error(f"未找到风格: {style_key}")
        print_info("使用 --list 查看所有可用风格")
        sys.exit(1)

    # 生成提示词
    prompts = []

    if topic:
        # 从主题生成多个变体
        prompts = generate_prompt_variants(topic, style, variants, enhance)
    elif keywords:
        # 从关键词生成
        prompts.append(generate_prompt_from_keywords(keywords, style, enhance))
        # 生成更多变体
        if variants > 1:
            for i in range(variants - 1):
                prompt = generate_prompt_variants(
                    " ".join(keywords),
                    style,
                    1,
                    enhance
                )[0]
                prompts.append(prompt)
    else:
        print_error("必须提供 --topic 或 --keywords")
        sys.exit(1)

    return prompts, style


def generate_videos(
    prompts: List[str],
    duration: int,
    aspect_ratio: str,
    api_key: Optional[str] = None
) -> List[dict]:
    """
    生成视频

    Returns:
        视频结果列表
    """
    results = []

    for i, prompt in enumerate(prompts, 1):
        print()
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}生成视频 {i}/{len(prompts)}{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"提示词: {prompt}")
        print(f"时长: {duration}秒 | 宽高比: {aspect_ratio}")
        print()

        try:
            result = generate_video_sync(
                prompt=prompt,
                api_key=api_key,
                duration=duration,
                aspect_ratio=aspect_ratio,
                auto_poll=True
            )
            results.append(result)

            # 显示结果
            print()
            if result.get("status") == "succeeded":
                print_success(f"视频 {i} 生成成功！")
                if "url" in result:
                    print(f"{Colors.GREEN}📹 视频 URL: {result['url']}{Colors.END}")
            elif result.get("status") == "timeout":
                print_info(f"视频 {i} 生成超时，请求已提交")
                if "poll_url" in result:
                    print(f"查询地址: {result['poll_url']}")
            else:
                print_error(f"视频 {i} 生成失败: {result.get('error', '未知错误')}")

        except ValueError as e:
            print_error(f"参数错误: {e}")
            break
        except Exception as e:
            print_error(f"生成失败: {e}")
            results.append({
                "status": "error",
                "error": str(e),
                "prompt": prompt
            })

    return results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="视频提示词生成器 - 生成高质量视频提示词并调用 Grok Imagine API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本使用 - 从主题生成提示词
  python3 main.py --topic "猫咪玩耍" --style "风景风光"

  # 生成并调用 Grok Imagine API 生成视频
  python3 main.py --topic "猫咪玩耍" --style "可爱" --generate-video

  # 批量生成多个变体
  python3 main.py --topic "猫咪玩耍" --variants 5

  # 从关键词生成
  python3 main.py --keywords "可爱,温暖,阳光" --style "都市生活"

  # 列出所有可用风格
  python3 main.py --list

  # 输出 JSON 格式
  python3 main.py --topic "产品展示" --style "产品" --output json
        """
    )

    # 输入参数
    input_group = parser.add_argument_group("输入参数")
    input_group.add_argument("--topic", "-t", help="视频主题")
    input_group.add_argument("--keywords", "-k", help="关键词（逗号分隔）")
    input_group.add_argument("--style", "-s", default="landscape",
                            help=f"视频风格（默认: landscape）")
    input_group.add_argument("--variants", "-v", type=int, default=1,
                            help="生成变体数量（默认: 1）")

    # 输出参数
    output_group = parser.add_argument_group("输出参数")
    output_group.add_argument("--output", "-o", choices=["readable", "json", "markdown"],
                             default="readable", help="输出格式（默认: readable）")
    output_group.add_argument("--file", "-f", help="输出到文件")
    output_group.add_argument("--no-enhance", action="store_true",
                             help="不自动增强提示词")

    # 视频生成参数
    video_group = parser.add_argument_group("视频生成参数")
    video_group.add_argument("--generate-video", action="store_true",
                            help="调用 Grok Imagine API 生成视频")
    video_group.add_argument("--duration", "-d", type=int, default=5,
                            help="视频时长，1-15秒（默认: 5）")
    video_group.add_argument("--aspect-ratio", "-a", default="16:9",
                            choices=["16:9", "9:16", "4:3", "1:1"],
                            help="宽高比（默认: 16:9）")
    video_group.add_argument("--api-key", help="XAI API Key（默认从环境变量 XAI_API_KEY 读取）")

    # 工具参数
    tool_group = parser.add_argument_group("工具")
    tool_group.add_argument("--list", "-l", action="store_true",
                           help="列出所有可用风格")
    tool_group.add_argument("--version", action="store_true",
                           help="显示版本信息")

    args = parser.parse_args()

    # 显示版本信息
    if args.version:
        print_header()
        print("Video Prompt Generator v1.0")
        print("集成 XAI Grok Imagine API")
        return

    # 列出所有风格
    if args.list:
        print_header()
        list_styles()
        return

    # 验证输入
    if not args.topic and not args.keywords:
        parser.print_help()
        print()
        print_error("必须提供 --topic 或 --keywords")
        print_info("使用 --list 查看所有可用风格")
        sys.exit(1)

    # 解析关键词
    keywords_list = []
    if args.keywords:
        keywords_list = [k.strip() for k in args.keywords.split(",")]

    # 验证变体数量
    if args.variants < 1:
        print_error("变体数量必须大于 0")
        sys.exit(1)

    # 验证视频参数
    if args.generate_video:
        if not 1 <= args.duration <= 15:
            print_error("视频时长必须在 1-15 秒之间")
            sys.exit(1)

        # 检查 API Key
        api_key = args.api_key
        if not api_key and not os.getenv('XAI_API_KEY'):
            print_error("需要提供 XAI_API_KEY")
            print_info("通过 --api-key 参数或环境变量设置")
            sys.exit(1)

    # 显示标题
    print_header()

    # 生成提示词
    print_info("正在生成提示词...")
    prompts, style = generate_prompts(
        topic=args.topic,
        keywords=keywords_list if keywords_list else None,
        style_key=args.style,
        variants=args.variants,
        enhance=not args.no_enhance
    )

    print_success(f"生成了 {len(prompts)} 个提示词")
    print()

    # 格式化输出
    output = format_prompt_output(prompts, style, args.output)

    # 输出到控制台
    print(output)

    # 输出到文件
    if args.file:
        try:
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(output)
            print_success(f"已保存到: {args.file}")
        except Exception as e:
            print_error(f"保存文件失败: {e}")

    # 生成视频
    if args.generate_video:
        print()
        print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}开始生成视频...{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.END}")
        print()

        results = generate_videos(
            prompts=prompts,
            duration=args.duration,
            aspect_ratio=args.aspect_ratio,
            api_key=args.api_key
        )

        # 保存视频结果
        if args.file:
            # 添加 .videos.json 扩展名
            video_file = args.file.rsplit('.', 1)[0] + '.videos.json'
            try:
                with open(video_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "prompts": prompts,
                        "videos": results
                    }, f, ensure_ascii=False, indent=2)
                print_success(f"视频结果已保存到: {video_file}")
            except Exception as e:
                print_error(f"保存视频结果失败: {e}")


if __name__ == "__main__":
    main()
