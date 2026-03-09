#!/usr/bin/env python3
"""
节日检测模块
检测今天是什么节日，返回对应的表情关键词
"""

import os
from datetime import datetime

# 节日定义 (月, 日) -> (关键词, 表情名)
HOLIDAYS = {
    # 农历节日（按公历近似）
    (1, 1): ("春节", "SPRINGFESTIVAL"),      # 春节
    (1, 15): ("元宵节", "LANTERNDAY"),       # 元宵节
    (5, 5): ("端午节", "DUANWU"),           # 端午节
    (7, 7): ("七夕节", "QIXI"),             # 七夕
    (8, 15): ("中秋节", "MIDAUTUMN"),       # 中秋节
    (12, 30): ("除夕", "SPRINGFESTIVAL"),    # 除夕（近似）
}

# 精确节日日期（每年可能不同，需要手动维护）
SPECIAL_HOLIDAYS = {
    "2026-02-17": ("春节", "SPRINGFESTIVAL"),
    "2026-03-09": ("无", None),  # 临时测试用
}

def get_today_holiday():
    """获取今天的节日信息"""
    today = datetime.now()
    month = today.month
    day = today.day
    
    # 先检查特殊日期
    today_str = today.strftime("%Y-%m-%d")
    if today_str in SPECIAL_HOLIDAYS:
        name, emotion = SPECIAL_HOLIDAYS[today_str]
        if emotion:
            return name, emotion
        return None, None
    
    # 检查常规节日
    if (month, day) in HOLIDAYS:
        return HOLIDAYS[(month, day)]
    
    return None, None

def get_holiday_video(holiday_name):
    """获取节日对应的视频文件名"""
    holiday_map = {
        "春节": "springfestival.mp4",
        "除夕": "springfestival.mp4",
        "元宵节": "lanternday.mp4",
        "端午节": "duanwu.mp4",
        "七夕节": "qixi.mp4",
        "中秋节": "midautumn.mp4",
    }
    return holiday_map.get(holiday_name)

if __name__ == "__main__":
    name, emotion = get_today_holiday()
    if name and emotion:
        print(f"今天节日: {name}, 表情: {emotion}")
    else:
        print("今天没有节日")
