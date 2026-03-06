#!/usr/bin/env python3
"""
检测SenseVoice是否已安装
"""

import os
import sys
import json

SENSEVOICE_MODEL_PATH = "/tmp/models/iic/SenseVoiceSmall"
DEFAULT_VIDEO_DIR = os.path.expanduser("~/.openclaw/workspace/emo_video")
DEFAULT_GIF_DIR = os.path.expanduser("~/.openclaw/workspace/emo_gif")

def check_sensevoice():
    """检查SenseVoice是否已安装"""
    if os.path.exists(SENSEVOICE_MODEL_PATH):
        return True
    return False

def check_emotion_resources():
    """检查表情包资源是否存在"""
    video_exists = os.path.exists(DEFAULT_VIDEO_DIR) and os.listdir(DEFAULT_VIDEO_DIR)
    gif_exists = os.path.exists(DEFAULT_GIF_DIR) and os.listdir(DEFAULT_GIF_DIR)
    return {
        "video": video_exists,
        "gif": gif_exists
    }

def get_status():
    """获取整体状态"""
    return {
        "sensevoice": check_sensevoice(),
        "resources": check_emotion_resources(),
        "model_path": SENSEVOICE_MODEL_PATH,
        "video_dir": DEFAULT_VIDEO_DIR,
        "gif_dir": DEFAULT_GIF_DIR
    }

def print_guide():
    """打印安装引导"""
    guide = """
🔔 SenseVoice 安装引导

为获得最佳语音情绪识别体验，建议安装SenseVoice：

安装步骤：
1. 确保OpenClaw已安装
2. SenseVoice模型会自动下载到: /tmp/models/iic/SenseVoiceSmall
3. 首次使用语音识别时会自动下载模型

表情包资源：
- 视频目录: ~/.openclaw/workspace/emo_video/
- GIF目录: ~/.openclaw/workspace/emo_gif/

如不安装，技能将使用基础文字情绪分析功能。
"""
    print(guide)

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check":
            status = get_status()
            print(json.dumps(status, indent=2))
        elif sys.argv[1] == "--guide":
            print_guide()
        else:
            print("Usage: check_sensevoice.py [--check|--guide]")
    else:
        status = get_status()
        if not status["sensevoice"]:
            print_guide()
        else:
            print("✓ SenseVoice已安装")
            print("✓ 表情包资源:", "已配置" if status["resources"]["video"] else "未配置")

if __name__ == "__main__":
    main()
