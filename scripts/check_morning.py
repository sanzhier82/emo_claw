#!/usr/bin/env python3
"""
早上首次对话检测
检测用户当天是否第一次说话，以及是否在早上时间段
"""

import os
import json
from datetime import datetime, time

# 配置文件路径
STATE_FILE = os.path.expanduser("~/.openclaw/workspace/.morning_state.json")

# 早上时间范围
MORNING_START = time(6, 0)
MORNING_END = time(10, 0)

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

def should_send_greeting(user_id="default"):
    """判断是否应该发送早安"""
    return is_morning() and check_first_message_today(user_id)

if __name__ == "__main__":
    import sys
    user_id = sys.argv[1] if len(sys.argv) > 1 else "default"
    
    if should_send_greeting(user_id):
        print("SEND_MORNING")
    else:
        print("NO_GREETING")
