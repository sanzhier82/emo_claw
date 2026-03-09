#!/usr/bin/env python3
"""
早上首次对话检测
检测用户当天是否第一次说话，以及是否在早上时间段
新增：节日检测 - 节日当天首次对话自动发送节日表情
"""

import os
import sys
import json
from datetime import datetime, time

# 配置文件路径
STATE_FILE = os.path.expanduser("~/.openclaw/workspace/.morning_state.json")

# 早上时间范围
MORNING_START = time(6, 0)
MORNING_END = time(10, 0)

# 节日定义
SPECIAL_HOLIDAYS = {
    "2026-02-17": ("春节", "springfestival.mp4"),
    "2027-01-26": ("春节", "springfestival.mp4"),
    "2026-02-24": ("元宵节", "lanternday.mp4"),
    "2026-05-31": ("端午节", "duanwu.mp4"),
    "2026-08-14": ("七夕节", "qixi.mp4"),
    "2026-09-25": ("中秋节", "midautumn.mp4"),
    "2026-02-17": ("春节", "springfestival.mp4"),
}

def is_morning():
    """检测当前是否在早上时间段"""
    now = time()
    return MORNING_START <= now < MORNING_END

def get_today():
    """获取今天的日期字符串"""
    return datetime.now().strftime("%Y-%m-%d")

def check_first_message_today(user_id="default"):
    """检测是否是当天第一次消息"""
    today = get_today()
    
    # 读取状态
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
        except:
            state = {}
    
    # 检查是否是今天第一次
    last_date = state.get(f"last_date_{user_id}", "")
    is_first = last_date != today
    
    # 更新状态
    state[f"last_date_{user_id}"] = today
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except:
        pass
    
    return is_first

def get_today_holiday():
    """获取今天的节日信息"""
    today_str = get_today()
    if today_str in SPECIAL_HOLIDAYS:
        return SPECIAL_HOLIDAYS[today_str]
    return None, None

def check_holiday_today(user_id="default"):
    """检测今天是否是节日，并检查是否已发送过节日祝福"""
    today = get_today()
    holiday_name, video_file = get_today_holiday()
    
    if not holiday_name:
        return None, None
    
    # 检查是否已发送过
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
        except:
            state = {}
    
    last_holiday = state.get(f"last_holiday_{user_id}", "")
    
    if last_holiday != today:
        # 未发送过，今天是节日，返回节日信息
        # 更新状态
        state[f"last_holiday_{user_id}"] = today
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f)
        except:
            pass
        return holiday_name, video_file
    
    return None, None

def should_send_greeting(user_id="default"):
    """判断是否应该发送早安或节日祝福"""
    # 优先检查节日
    holiday_name, video_file = check_holiday_today(user_id)
    if holiday_name:
        return f"SEND_HOLIDAY:{holiday_name}:{video_file}"
    
    # 然后检查早安
    if is_morning() and check_first_message_today(user_id):
        return "SEND_MORNING"
    
    return "NO_GREETING"

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else "default"
    result = should_send_greeting(user_id)
    print(result)
