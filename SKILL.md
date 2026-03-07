---
name: emotion-comm
description: 双向情感交流技能 - 根据用户情绪自动回复合适的动态表情包。支持语音情绪识别（需SenseVoice）和文字情绪分析，区分通道发送视频或GIF表情。
---

# 双向情感交流 (Emotion Communication)

智能识别用户情绪并回复对应动态表情包的技能。

## 功能特性

- **情绪识别**：支持语音（SenseVoice）和文字情绪分析
- **通道差异化回复**：Telegram发送视频，飞书发送GIF
- **引导安装**：首次使用引导安装SenseVoice以获得更好体验
- **多情绪支持**：HAPPY, SAD, ANGRY, FEARFUL, SURPRISED, NEUTRAL
- **早上自动回复**：早上时间段（6:00-10:00）用户首次对话时自动回复早安表情

## 前置要求

### 推荐安装

为获得最佳语音情绪识别体验，建议安装：

```bash
# 1. 安装SenseVoice模型
# 模型会自动下载到 /tmp/models/iic/SenseVoiceSmall

# 2. 准备表情包资源
# - 视频表情：~/.openclaw/workspace/emo_video/*.mp4
# - GIF表情：~/.openclaw/workspace/emo_gif/*.gif
```

**注意**：未安装SenseVoice时，技能将使用基础文字情绪分析功能。

## 通道差异化回复

技能会根据发送通道自动选择合适的格式：

| 通道类型 | 格式 | 说明 |
|----------|------|------|
| **支持视频自动播放** | 视频(.mp4) | Telegram, QQ, WhatsApp, Discord |
| **仅支持GIF/需点击** | GIF(.gif) | 飞书, 钉钉, Slack, Signal, iMessage |

**自动检测逻辑：**
- 脚本会根据 `--channel` 参数自动选择
- 优先使用视频格式（如通道支持）

### 手动触发

```bash
# 分析文字情绪并回复
python3 emotion_handler.py --text "你好棒"

# 分析语音文件情绪并回复
python3 emotion_handler.py --audio /path/to/voice.ogg
```

### 自动触发（需配置）

在Skill配置中启用自动触发模式，当用户发送消息时自动分析情绪并回复。

## 情绪映射

| 情绪 | 触发词 | 视频回复 | GIF回复 |
|------|--------|----------|----------|
| HAPPY | 开心、高兴、棒 | happy.mp4 | happy.gif |
| SAD | 难过、伤心、哭 | crying.mp4 | crying.gif |
| ANGRY | 生气、怒、不爽 | angry.mp4 | angry.gif |
| PLAYFUL | 调皮、逗、玩 | playful.mp4 | playful.gif |
| HIGHFIVE | 击掌、干得漂亮 | highfive.mp4 | highfive.gif |
| HARDWORKING | 辛苦了 | hardworking.mp4 | hardworking.gif |

## 配置选项

在 `config/settings.json` 中配置：

```json
{
  "sensevoice_path": "/tmp/models/iic/SenseVoiceSmall",
  "video_dir": "~/.openclaw/workspace/emo_video",
  "gif_dir": "~/.openclaw/workspace/emo_gif",
  "auto_trigger": true,
  "default_emotion": "NEUTRAL"
}
```

## 故障排除

- **未检测到SenseVoice**：请确认模型已安装，或跳过安装使用基础版
- **找不到表情包**：请确认 emo_video/ 和 emo_gif/ 目录存在
- **通道识别失败**：手动指定通道使用 `--channel telegram` 或 `--channel feishu`

---

*作者：Sanzhier*
*版本：1.0.0*
