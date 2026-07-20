#!/usr/bin/env python3
import requests
import time
import os
import sys
import uuid

# Edge TTS configuration
EDGE_TTS_API = "https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1"

# Available voices
VOICES = {
    "zh-CN-XiaoxiaoNeural": {"gender": "Female", "name": "晓晓（女声）"},
    "zh-CN-YunxiNeural": {"gender": "Male", "name": "云希（男声）"},
    "zh-CN-YunyangNeural": {"gender": "Male", "name": "云扬（男声）"},
    "zh-CN-XiaoyiNeural": {"gender": "Female", "name": "晓伊（女声）"},
    "en-US-AriaNeural": {"gender": "Female", "name": "Aria (美式女声)"},
    "en-GB-SoniaNeural": {"gender": "Female", "name": "Sonia (英式女声)"},
}

def get_headers(text, voice):
    """Generate headers for Edge TTS API"""
    timestamp = str(int(time.time() * 1000))

    headers = {
        "Content-Type": "application/ssml+xml",
        "X-Ms-Client-Id": "EdgeGPT.TTS",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    return headers

def generate_speech(text, voice="zh-CN-XiaoxiaoNeural", output_file=None):
    """Generate speech using Edge TTS"""
    if output_file is None:
        media_dir = "/root/clawd/skills/kokoro-tts/media"
        os.makedirs(media_dir, exist_ok=True)
        timestamp = int(time.time())
        output_file = os.path.join(media_dir, f"tts_edge_{timestamp}.mp3")

    # SSML format
    ssml = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
        <voice name='{voice}'>
            <prosody rate='1.0'>
                {text}
            </prosody>
        </voice>
    </speak>"""

    # Edge TTS API endpoint
    params = {
        "TrustedClientToken": "6A5AA1D4EAFF4E9FB37E23D68491D6F1",
        "ConnectionId": uuid.uuid4().hex,
    }

    url = f"{EDGE_TTS_API}?{requests.compat.urlencode(params)}"

    headers = get_headers(text, voice)

    try:
        response = requests.post(url, data=ssml.encode('utf-8'), headers=headers, stream=True, timeout=30)

        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"MEDIA: {output_file}")
            return output_file
        else:
            print(f"Error: {response.status_code} {response.text[:200]}", file=sys.stderr)
            return None

    except Exception as e:
        print(f"Error generating speech: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 edge-tts.py <text> [voice]", file=sys.stderr)
        print(f"\nAvailable voices:", file=sys.stderr)
        for voice_id, info in VOICES.items():
            print(f"  - {voice_id}: {info['name']} ({info['gender']})", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else "zh-CN-XiaoxiaoNeural"

    generate_speech(text, voice)
