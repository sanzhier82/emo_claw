# 🦐 小虾拟人化表情交流技能 (emo_claw)

为OpenClaw量身打造的拟人化动态表情包回复技能，能自动根据用户情绪并回复合适的动态表情包。

## 🎬 介绍视频

https://youtu.be/-tLqPCCq8s0

## ✨ 功能特性

- **多情绪识别**：支持文字和语音情绪分析
- **SenseVoice支持**：语音情绪识别更准确（推荐安装）
- **通道差异化回复**：根据通道自动选择视频或GIF格式
- **情景化回复**：如6:00-10:00首次对话自动回复早安
- **天气触发**：查询天气时根据温度/天气自动回复对应表情
- **可扩展可替换**：用户可扩展更多的表情加入表情包，也可整体替换为自己的表情库，保持表情文件同名即可

## 🎭 支持的情绪

| 情绪 | 关键词示例 | 触发场景 |
|------|-----------|----------|
| morning | 早安、早上好 | 每天早上首次对话 |
| happy | 开心、高兴、棒 | 被表扬/开心时 |
| highfive | 击掌、干得漂亮 | 完成任务/庆祝 |
| fox | 变身、狐狸 | 调皮时 |
| snow | 下雪、雪 | 查询天气显示下雪 |
| swim | 游泳、高温 | 查询天气30度以上 |
| resigned | 无奈、没办法 | 无奈时 |
| mischief | 搞怪、调皮 | 开玩笑时 |
| fighting | 加油 | 鼓励时 |
| sorry | 抱歉、对不起 | 道歉时 |
| goodnight | 晚安、睡觉 | 晚上对话结束 |
| angry | 生气、不爽 | 不满时 |
| cry | 哭、难过 | 伤心时 |
| eyeroll | 翻白眼、无语 | 无语时 |
| hardworking | 辛苦、累 | 工作相关 |

## 📱 通道差异化

| 通道 | 发送格式 |
|------|----------|
| Telegram | 视频 (.mp4) |
| WhatsApp | 视频 (.mp4) |
| Discord | 视频 (.mp4) |
| 飞书 | GIF (.gif) |
| 钉钉 | GIF (.gif) |
| QQ | GIF (.gif) |

## 🚀 安装

### 方式一：GitHub安装（推荐）

1. 克隆仓库到本地：
```bash
git clone https://github.com/sanzhier82/emo_claw.git
```

2. 将表情资源复制到指定目录：
```bash
# 视频表情
cp -r assets/emo_video/* ~/.openclaw/workspace/emo_video/

# GIF表情  
cp -r assets/emo_gif/* ~/.openclaw/workspace/emo_gif/
```

3. 复制技能文件：
```bash
cp SKILL.md ~/.openclaw/workspace/skills/emotion-comm/
cp -r scripts/* ~/.openclaw/workspace/skills/emotion-comm/scripts/
cp -r config/* ~/.openclaw/workspace/skills/emotion-comm/config/
```

4. 重启OpenClaw使技能生效

### 可选：安装SenseVoice（支持语音情绪识别）

推荐安装，可大幅提升语音情绪识别的准确率。

1. 创建模型目录：
```bash
mkdir -p /tmp/models/iic
```

2. 模型会自动在首次运行时从 HuggingFace 下载：
   - 模型地址：https://huggingface.co/iic/SenseVoiceSmall
   - 或从 Modelscope：https://modelscope.cn/models/iic/SenseVoiceSmall

3. 首次使用语音功能时会自动下载模型（约100MB）

### 方式二：手动下载安装

访问 GitHub releases 页面下载最新版本：
https://github.com/sanzhier82/emo_claw/releases

## ⚙️ 配置

在 `config/settings.json` 中配置：

```json
{
  "video_dir": "~/.openclaw/workspace/emo_video",
  "gif_dir": "~/.openclaw/workspace/emo_gif",
  "auto_trigger": true,
  "default_emotion": "NEUTRAL",
  "sensevoice_path": "/tmp/models/iic/SenseVoiceSmall"
}
```

| 配置项 | 说明 |
|--------|------|
| video_dir | 视频表情存放目录 |
| gif_dir | GIF表情存放目录 |
| auto_trigger | 是否自动触发 |
| default_emotion | 默认情绪 |
| sensevoice_path | SenseVoice模型路径（推荐安装） |

## 📖 使用

### 命令行

```bash
# 文字情绪分析
python3 emotion_handler.py --text "你真棒！"

# 语音情绪分析
python3 emotion_handler.py --audio voice.ogg

# 早上自动回复
python3 emotion_handler.py --auto-morning --channel telegram
```

### 自动触发

配置技能自动触发后，用户发送消息时会自动分析情绪并回复对应表情。

## 🎨 自定义表情

1. 添加视频文件到 `emo_video/` 目录
2. 添加同名GIF到 `emo_gif/` 目录
3. 在 `emotion_handler.py` 的 `EMOTION_MAP` 中添加映射

## 📦 项目结构

```
emo_claw/
├── SKILL.md              # 技能定义
├── _meta.json            # 元数据
├── config/
│   └── settings.json     # 配置文件
├── scripts/
│   ├── emotion_handler.py    # 核心处理脚本
│   ├── check_sensevoice.py   # SenseVoice检测
│   └── check_morning.py      # 早上检测
└── assets/
    ├── emo_video/       # 视频表情
    └── emo_gif/         # GIF表情
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

@sanzhier82- 2026
