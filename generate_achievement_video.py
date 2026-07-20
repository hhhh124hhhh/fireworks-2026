#!/usr/bin/env python3
"""
Generate an introduction video for Achievement System
- Duration: 8-15 seconds
- Resolution: 1080p
- Style: Tech/gaming aesthetic
- Language: Chinese
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio
import numpy as np
import os
from pathlib import Path

# Configuration
WIDTH, HEIGHT = 1920, 1080
FPS = 30
DURATION_SEC = 12
TOTAL_FRAMES = FPS * DURATION_SEC

# Colors (tech/gaming aesthetic)
BG_COLOR = (10, 14, 23)  # Dark blue
PRIMARY_COLOR = (59, 130, 246)  # Blue
SECONDARY_COLOR = (139, 92, 246)  # Purple
ACCENT_COLOR = (236, 72, 153)  # Pink
TEXT_COLOR = (249, 250, 251)  # White
GLOW_COLOR = (59, 130, 246, 50)  # Semi-transparent blue

# Text content
TEXT_CONTENT = [
    {"text": "成就系统", "start_frame": 0, "end_frame": 60},
    {"text": "Achievement System", "start_frame": 30, "end_frame": 90},
    {"text": "🎯 成就追踪", "start_frame": 90, "end_frame": 150},
    {"text": "📊 数据统计", "start_frame": 120, "end_frame": 180},
    {"text": "📈 可视化展示", "start_frame": 150, "end_frame": 210},
    {"text": "🎮 游戏化激励", "start_frame": 180, "end_frame": 240},
    {"text": "Python + CLI", "start_frame": 240, "end_frame": 300},
    {"text": "让成就更有趣", "start_frame": 270, "end_frame": TOTAL_FRAMES},
]

def create_gradient_background(frame_num):
    """Create animated gradient background"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    # Animated gradient colors
    offset = (frame_num / TOTAL_FRAMES) * 100
    for y in range(HEIGHT):
        r = int(BG_COLOR[0] + np.sin(y * 0.01 + offset * 0.1) * 20)
        g = int(BG_COLOR[1] + np.cos(y * 0.01 + offset * 0.1) * 10)
        b = int(BG_COLOR[2] + np.sin(y * 0.008 + offset * 0.1) * 30)
        draw.rectangle([(0, y), (WIDTH, y + 1)], fill=(r, g, b))

    # Add grid lines
    grid_spacing = 60
    for x in range(0, WIDTH, grid_spacing):
        alpha = 20 + int(10 * np.sin(frame_num * 0.1))
        line_color = (*PRIMARY_COLOR[:3], alpha)
        draw.rectangle([(x + (frame_num % grid_spacing), 0),
                       (x + (frame_num % grid_spacing) + 1, HEIGHT)],
                      fill=line_color)

    for y in range(0, HEIGHT, grid_spacing):
        alpha = 20 + int(10 * np.cos(frame_num * 0.1))
        line_color = (*PRIMARY_COLOR[:3], alpha)
        draw.rectangle([(0, y + (frame_num % grid_spacing)),
                       (WIDTH, y + (frame_num % grid_spacing) + 1)],
                      fill=line_color)

    return img

def add_glow_effect(img, text, position, font, color):
    """Add glow effect to text"""
    draw = ImageDraw.Draw(img)

    # Create glow layers
    for i in range(3, 0, -1):
        glow_color = (*color[:3], 30 // i)
        draw.text((position[0] - i, position[1] - i), text, font=font,
                 fill=glow_color)
        draw.text((position[0] + i, position[1] - i), text, font=font,
                 fill=glow_color)
        draw.text((position[0] - i, position[1] + i), text, font=font,
                 fill=glow_color)
        draw.text((position[0] + i, position[1] + i), text, font=font,
                 fill=glow_color)

    # Main text
    draw.text(position, text, font=font, fill=color)
    return img

def draw_badge(draw, x, y, size, frame_num):
    """Draw animated badge icon"""
    # Badge circle
    radius = size // 2
    pulse = 1 + 0.1 * np.sin(frame_num * 0.2)

    # Outer glow
    for i in range(5):
        alpha = 50 - i * 10
        glow_color = (*SECONDARY_COLOR[:3], alpha)
        draw.ellipse([x - radius * pulse - i, y - radius * pulse - i,
                     x + radius * pulse + i, y + radius * pulse + i],
                    outline=glow_color, width=2)

    # Main badge
    draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                outline=SECONDARY_COLOR, width=3)

    # Star in center
    star_points = []
    for i in range(10):
        angle = i * 36 - 90 + frame_num * 0.5
        r = radius * 0.6 if i % 2 == 0 else radius * 0.3
        star_points.append((x + r * np.cos(np.radians(angle)),
                           y + r * np.sin(np.radians(angle))))

    draw.polygon(star_points, fill=PRIMARY_COLOR, outline=TEXT_COLOR)

def draw_progress_bar(draw, x, y, width, height, frame_num):
    """Draw animated progress bar"""
    # Background
    draw.rounded_rectangle([x, y, x + width, y + height],
                          radius=10, fill=(31, 41, 55))

    # Animated fill
    progress = (frame_num % 60) / 60
    fill_width = int(width * progress)

    # Gradient fill
    for i in range(fill_width):
        ratio = i / width
        r = int(PRIMARY_COLOR[0] * (1 - ratio) + SECONDARY_COLOR[0] * ratio)
        g = int(PRIMARY_COLOR[1] * (1 - ratio) + SECONDARY_COLOR[1] * ratio)
        b = int(PRIMARY_COLOR[2] * (1 - ratio) + SECONDARY_COLOR[2] * ratio)
        draw.line([(x + i, y), (x + i, y + height)], fill=(r, g, b), width=1)

    # Glow effect
    glow_img = Image.new('RGBA', (fill_width + 20, height + 20), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.rounded_rectangle([10, 10, fill_width + 10, height + 10],
                               radius=10, fill=(*SECONDARY_COLOR[:3], 30))

def create_frame(frame_num):
    """Create a single video frame"""
    # Create background
    img = create_gradient_background(frame_num)
    draw = ImageDraw.Draw(img)

    # Add animated elements
    # Title
    for text_info in TEXT_CONTENT:
        start = text_info["start_frame"]
        end = text_info["end_frame"]

        if start <= frame_num <= end:
            # Fade in/out effect
            if frame_num < start + 15:
                alpha = int(255 * (frame_num - start) / 15)
            elif frame_num > end - 15:
                alpha = int(255 * (end - frame_num) / 15)
            else:
                alpha = 255

            text = text_info["text"]
            font_size = 80 if len(text) < 10 else 60

            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                                          font_size)
            except:
                font = ImageFont.load_default()

            # Calculate position
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (WIDTH - text_width) // 2
            y = HEIGHT // 2

            # Draw text with glow
            if alpha > 50:
                add_glow_effect(img, text, (x, y), font,
                              (*TEXT_COLOR[:3], alpha))

    # Add decorative badges
    badge_positions = [(300, 200), (1620, 200), (300, 880), (1620, 880)]
    for i, (bx, by) in enumerate(badge_positions):
        draw_badge(draw, bx, by, 80, frame_num + i * 30)

    # Add progress bar at bottom
    draw_progress_bar(draw, 400, 950, 1120, 30, frame_num)

    # Add tech decorations
    # Corner decorations
    corner_size = 100
    draw.line([(0, 0), (corner_size, 0)], fill=PRIMARY_COLOR, width=3)
    draw.line([(0, 0), (0, corner_size)], fill=PRIMARY_COLOR, width=3)
    draw.line([(WIDTH - corner_size, 0), (WIDTH, 0)], fill=PRIMARY_COLOR, width=3)
    draw.line([(WIDTH, 0), (WIDTH, corner_size)], fill=PRIMARY_COLOR, width=3)
    draw.line([(0, HEIGHT - corner_size), (0, HEIGHT)], fill=PRIMARY_COLOR, width=3)
    draw.line([(0, HEIGHT), (corner_size, HEIGHT)], fill=PRIMARY_COLOR, width=3)
    draw.line([(WIDTH - corner_size, HEIGHT), (WIDTH, HEIGHT)], fill=PRIMARY_COLOR, width=3)
    draw.line([(WIDTH, HEIGHT - corner_size), (WIDTH, HEIGHT)], fill=PRIMARY_COLOR, width=3)

    return np.array(img)

def main():
    """Generate the video"""
    output_path = "/tmp/achievement_system_intro.mp4"
    frames = []

    print(f"🎬 Generating achievement system intro video...")
    print(f"   Duration: {DURATION_SEC}s")
    print(f"   Resolution: {WIDTH}x{HEIGHT}")
    print(f"   Frames: {TOTAL_FRAMES}")

    # Generate frames
    for frame_num in range(TOTAL_FRAMES):
        if frame_num % 30 == 0:
            progress = (frame_num / TOTAL_FRAMES) * 100
            print(f"   Progress: {progress:.1f}%")

        frame = create_frame(frame_num)
        frames.append(frame)

    # Save video
    print(f"\n💾 Saving video to {output_path}...")
    imageio.mimsave(output_path, frames, fps=FPS, codec='libx264', quality=8)

    print(f"\n✅ Video created successfully!")
    print(f"   Path: {output_path}")
    print(f"   Size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")

    return output_path

if __name__ == "__main__":
    main()
