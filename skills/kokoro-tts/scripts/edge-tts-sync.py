#!/usr/bin/env python3
import edge_tts
import os
import sys
import time

def generate_speech(text, voice="zh-CN-XiaoxiaoNeural", output_file=None):
    """Generate speech using Edge TTS"""

    if output_file is None:
        media_dir = "/root/clawd/skills/kokoro-tts/media"
        os.makedirs(media_dir, exist_ok=True)
        timestamp = int(time.time())
        output_file = os.path.join(media_dir, f"tts_edge_{timestamp}.mp3")

    try:
        # Generate speech
        communicate = edge_tts.Communicate(text, voice)
        
        # Save to file (synchronous)
        communicate.save_sync(output_file)

        # Check if file exists
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"File saved: {output_file} ({file_size} bytes)")
            print(f"MEDIA: {output_file}")
            return output_file
        else:
            print(f"Error: File not created: {output_file}", file=sys.stderr)
            return None

    except Exception as e:
        print(f"Error generating speech: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 edge-tts-sync.py <text> [voice]", file=sys.stderr)
        print("\nAvailable voices:", file=sys.stderr)
        print("  - zh-CN-XiaoxiaoNeural (晓晓 - 女声)", file=sys.stderr)
        print("  - zh-CN-YunxiNeural (云希 - 男声)", file=sys.stderr)
        print("  - zh-CN-YunyangNeural (云扬 - 男声)", file=sys.stderr)
        print("  - zh-CN-XiaoyiNeural (晓伊 - 女声)", file=sys.stderr)
        print("  - en-US-AriaNeural (Aria - US Female)", file=sys.stderr)
        print("  - en-GB-SoniaNeural (Sonia - UK Female)", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else "zh-CN-XiaoxiaoNeural"

    generate_speech(text, voice)
