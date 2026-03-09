#!/usr/bin/env python3
"""
双向情感交流 - 核心处理脚本
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime

# 配置路径
SENSEVOICE_MODEL_PATH = "/tmp/models/iic/SenseVoiceSmall"
DEFAULT_VIDEO_DIR = os.path.expanduser("~/.openclaw/workspace/emo_video")
DEFAULT_GIF_DIR = os.path.expanduser("~/.openclaw/workspace/emo_gif")

# 早上时间范围（6:00-10:00）
MORNING_START = 6
MORNING_END = 10

# 状态文件路径
STATE_FILE = os.path.expanduser("~/.openclaw/workspace/.emo_state.json")

# 通道类型配置 - 支持视频自动播放的通道
VIDEO_CHANNELS = ["telegram", "whatsapp", "discord"]
GIF_CHANNELS = ["feishu", "slack", "dingtalk", "signal", "imessage"]

# 情绪映射表
EMOTION_MAP = {
    "HAPPY": {
        "keywords": ["开心", "高兴", "棒", "好", "赞", "太好了", "happy", "great", "good"],
        "video": "happy.mp4",
        "gif": "happy.gif"
    },
    "SAD": {
        "keywords": ["难过", "伤心", "哭", "sad", "crying"],
        "video": "cry.mp4",
        "gif": "cry.gif"
    },
    "ANGRY": {
        "keywords": ["生气", "怒", "不爽", "angry", "mad"],
        "video": "cry.mp4",  # 用哭的
        "gif": "cry.gif"
    },
    "MISCHIEF": {
        "keywords": ["调皮", "逗", "玩", "mischief", "搞怪", "调皮"],
        "video": "mischief.mp4",
        "gif": "mischief.gif"
    },
    "HIGHFIVE": {
        "keywords": ["击掌", "干得漂亮", "厉害", "牛", "highfive", "awesome"],
        "video": "highfive.mp4",
        "gif": "highfive.gif"
    },
    "HARDWORKING": {
        "keywords": ["辛苦", "累", "工作", "hardworking"],
        "video": "hardworking.mp4",
        "gif": "hardworking.gif"
    },
    "SORRY": {
        "keywords": ["抱歉", "对不起", "sorry", "对不起"],
        "video": "sorry.mp4",
        "gif": "sorry.gif"
    },
    "EYEROLL": {
        "keywords": ["翻白眼", "无语", "eyeroll", "真服了"],
        "video": "eyeroll.mp4",
        "gif": "eyeroll.gif"
    },
    "GOODNIGHT": {
        "keywords": ["晚安", "goodnight", "睡觉", "困"],
        "video": "goodnight.mp4",
        "gif": "goodnight.gif"
    },
    "MORNING": {
        "keywords": ["早安", "morning", "早上好", "早晨"],
        "video": "morning.mp4",
        "gif": "morning.gif"
    },
    "RESIGNED": {
        "keywords": ["无奈", "没办法", "无助", "resigned", "无奈", "算了"],
        "video": "resigned.mp4",
        "gif": "resigned.gif"
    },
    "SNOW": {
        "keywords": ["雪", "下雪", "snow"],
        "video": "snow.mp4",
        "gif": "snow.gif"
    },
    "SWIM": {
        "keywords": ["游泳", "swim", "玩水", "下水"],
        "video": "swim.mp4",
        "gif": "swim.gif"
    },
    "OBEDIENT": {
        "keywords": ["好的", "收到", "obey", "听话", "OK", "嗯"],
        "video": "obedient.mp4",
        "gif": "obedient.gif"
    },
    "FOX": {
        "keywords": ["狐狸", "fox", "小狐狸", "变身"],
        "video": "fox.mp4",
        "gif": "fox.gif"
    },
    "SHY": {
        "keywords": ["害羞", "不好意思", "尴尬", "shy"],
        "video": "shy.mp4",
        "gif": "shy.gif"
    },
    "DELIVER": {
        "keywords": ["外卖", "吃饭", "_DELIVER", "deliver", "饿了"],
        "video": "deliver.mp4",
        "gif": "deliver.gif"
    },
    "SPRINGFESTIVAL": {
        "keywords": ["除夕", "春节", "过年", "新年快乐", "春節"],
        "video": "springfestival.mp4",
        "gif": "springfestival.gif"
    },
    "LANTERNDAY": {
        "keywords": ["元宵节", "元宵", "灯会", "lantern"],
        "video": "lanternday.mp4",
        "gif": "lanternday.gif"
    },
    "DUANWU": {
        "keywords": ["端午节", "端午", "粽子", "duanwu"],
        "video": "duanwu.mp4",
        "gif": "duanwu.gif"
    },
    "QIXI": {
        "keywords": ["七夕节", "七夕", "牛郎织女", "qixi"],
        "video": "qixi.mp4",
        "gif": "qixi.gif"
    },
    "MIDAUTUMN": {
        "keywords": ["中秋节", "中秋", "月饼", "赏月", "midautumn"],
        "video": "midautumn.mp4",
        "gif": "midautumn.gif"
    },
    "LOVE": {
        "keywords": ["爱你", "爱", "么么哒", "love", "爱心"],
        "video": "love.mp4",
        "gif": "love.gif"
    },
    "JOKE": {
        "keywords": ["笑话", "讲个笑话", "joke", "笑死了", "搞笑"],
        "video": "joke.mp4",
        "gif": "happy.gif"
    },
    "NEUTRAL": {
        "keywords": [],
        "video": "happy.mp4",  # 默认
        "gif": "happy.gif"
    }
}

def check_sensevoice():
    """检查SenseVoice是否已安装"""
    return os.path.exists(SENSEVOICE_MODEL_PATH)

def recognize_sensevoice(audio_path):
    """调用SenseVoice识别语音"""
    if not check_sensevoice():
        return None, "SenseVoice未安装"
    
    # 调用SenseVoice
    cmd = [
        "~/.venv/sensevoice/bin/python", "-c",
        f"""
from funasr import AutoModel
model = AutoModel(model='/tmp/models/iic/SenseVoiceSmall', device='cpu')
result = model.generate(input='{audio_path}')
print(json.dumps(result))
"""
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout), "success"
        else:
            return None, result.stderr
    except Exception as e:
        return None, str(e)

def analyze_text_emotion(text):
    """分析文字情绪"""
    text_lower = text.lower()
    
    for emotion, data in EMOTION_MAP.items():
        for keyword in data["keywords"]:
            if keyword.lower() in text_lower:
                return emotion
    
    return "NEUTRAL"

def check_morning_greeting(user_id="default"):
    """检测是否是早上（6:00-10:00）且是当天首次对话，返回早安情绪"""
    import time
    
    current_hour = datetime.now().hour
    if not (MORNING_START <= current_hour < MORNING_END):
        return None
    
    # 检查是否是当天首次对话
    today = datetime.now().strftime("%Y-%m-%d")
    
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
        except:
            state = {}
    
    last_date = state.get(f"last_date_{user_id}", "")
    is_first = last_date != today
    
    # 更新状态
    state[f"last_date_{user_id}"] = today
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except:
        pass
    
    if is_first:
        return "MORNING"
    return None

def get_emotion_reply(emotion, channel="auto"):
    """获取情绪对应的回复"""
    # 自动检测通道类型
    if channel == "auto":
        # 默认使用视频格式
        channel = "telegram"
    
    # 根据通道类型选择格式
    if channel.lower() in VIDEO_CHANNELS:
        # 视频格式
        emotion_data = EMOTION_MAP.get(emotion, EMOTION_MAP["NEUTRAL"])
        filename = emotion_data["video"]
        path = os.path.join(DEFAULT_VIDEO_DIR, filename)
    else:
        # GIF格式
        emotion_data = EMOTION_MAP.get(emotion, EMOTION_MAP["NEUTRAL"])
        filename = emotion_data["gif"]
        path = os.path.join(DEFAULT_GIF_DIR, filename)
    
    return path, emotion

def main():
    parser = argparse.ArgumentParser(description="双向情感交流 - 情绪识别与回复")
    parser.add_argument("--text", type=str, help="要分析的文字")
    parser.add_argument("--audio", type=str, help="要分析的语音文件路径")
    parser.add_argument("--channel", type=str, default="telegram", choices=["telegram", "feishu"], help="发送通道")
    parser.add_argument("--check", action="store_true", help="检查环境状态")
    
    args = parser.parse_args()
    
    if args.check:
        # 检查状态
        status = {
            "sensevoice": check_sensevoice(),
            "video_dir": DEFAULT_VIDEO_DIR,
            "gif_dir": DEFAULT_GIF_DIR,
            "model_path": SENSEVOICE_MODEL_PATH
        }
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return
    
    # 早上自动回复早安（默认启用，不再需要参数）
    morning_emotion = check_morning_greeting()
    if morning_emotion:
        print(f"🌅 检测到早上时间（首次对话），自动回复早安")
        emotion = morning_emotion
    elif args.audio:
        # 语音输入
        print("🔍 正在识别语音...")
        result, status = recognize_sensevoice(args.audio)
        if result:
            # 提取文字和情绪
            text = result[0].get("text", "") if result else ""
            emotion = result[0].get("emotion", "NEUTRAL")
            print(f"📝 识别文字: {text}")
            print(f"😊 情绪: {emotion}")
        else:
            print(f"⚠️ 识别失败: {status}")
            emotion = "NEUTRAL"
    elif args.text:
        # 文字输入
        emotion = analyze_text_emotion(args.text)
        print(f"😊 情绪: {emotion}")
    else:
        print("请提供 --text 或 --audio 参数")
        return
    
    # 获取回复
    reply_path, detected_emotion = get_emotion_reply(emotion, args.channel)
    print(f"📎 回复文件: {reply_path}")
    print(f"✅ 检测完成")

if __name__ == "__main__":
    main()
