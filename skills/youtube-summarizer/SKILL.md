---
name: youtube-summarizer
description: 总结 YouTube 视频内容并生成中文摘要。支持有字幕和无字幕视频：有字幕时提取字幕文本，无字幕时自动下载音频并使用 AI 语音识别转录。适用于"总结 YouTube 视频"、"分析视频内容"、"视频摘要"等请求。
allowed-tools: [Bash, Read, Glob]
---

# YouTube 视频总结 Skill

快速理解 YouTube 视频内容，无需观看完整视频。

## 功能特性

- ✅ 自动从 YouTube 视频下载字幕
- ✅ 支持中文、英文等多语言字幕
- ✅ 智能解析和清理字幕文本
- ✅ 生成结构化的中文摘要
- ✅ 使用 yt-dlp 确保稳定可靠
- ✅ 无字幕时自动使用 AI 语音识别转录（mlx-whisper）

## 使用方法

直接向 Claude 提供 YouTube URL 并请求总结：

```
"总结这个 YouTube 视频：https://www.youtube.com/watch?v=VIDEO_ID"
"请帮我提取并总结这个视频的字幕：[URL]"
"分析这个视频内容并给我中文摘要：[URL]"
```

## 工作流程

1. **验证 URL**：检查提供的 YouTube 链接有效性
2. **下载字幕**：使用 `yt-dlp --write-sub --write-auto-sub` 下载可用字幕
3. **检测字幕**：判断是否成功获取字幕
   - ✓ 有字幕 → 读取 VTT 文件，提取文本
   - ✗ 无字幕 → 进入音频转录流程（见下方）
4. **提取文本**：清理时间戳和格式标记，提取纯文本
5. **生成摘要**：分析内容并生成结构化的中文总结
6. **清理文件**：删除所有临时文件

### 无字幕时的音频转录流程

当视频没有可用字幕时，自动执行以下步骤：

1. **下载音频**：
   ```bash
   yt-dlp -x --audio-format mp3 -o "/tmp/yt_audio_%(id)s.%(ext)s" "VIDEO_URL"
   ```

2. **转录音频**（使用 mlx-whisper turbo 模型）：
   ```bash
   mlx_whisper --model mlx-community/whisper-turbo \
     --language zh \
     --output-format txt \
     --output-dir /tmp \
     "/tmp/yt_audio_VIDEO_ID.mp3"
   ```
   - 若视频非中文，可使用 `--language auto` 自动检测语言

3. **读取转录文本**：读取生成的 `.txt` 文件

4. **清理临时文件**：
   ```bash
   rm -f /tmp/yt_audio_VIDEO_ID.mp3 /tmp/yt_audio_VIDEO_ID.txt
   ```

## 摘要格式

生成的摘要包含：

- 📊 **视频主题**：视频的核心主题
- 📝 **主要内容**：按章节或主题组织的要点
- 🔑 **关键观点**：视频中的重要观点和结论
- 💡 **核心思想**：提炼出的核心信息

## 技术要求

- yt-dlp 已安装（通过 Homebrew 或 pip）
- mlx-whisper 已安装（`pip install mlx-whisper`）— 用于无字幕视频转录
- macOS with Apple Silicon（M1/M2/M3/M4）— mlx-whisper 依赖
- 网络连接以下载字幕/音频
- Bash 和 Read 工具权限

## 支持的字幕类型

- 手动上传的字幕（多语言）
- YouTube 自动生成的字幕
- 社区贡献的字幕

## 示例

**输入：**
```
请总结这个视频：https://www.youtube.com/watch?v=qbU7LHPZ4Xo
```

**输出：**
```
## 📊 视频主题
股票投资分析框架：如何结合基本面分析和技术分析

## 📝 主要内容
### 一、基本面分析框架
- 商业模式分析
- 财务表现评估
- 市场定价研究

### 二、技术面分析框架
- 趋势判断
- 位置分析
- 风险管理

## 🔑 关键观点
1. 基本面用于定性，技术面用于交易
2. 优秀公司需要具备四个条件...
3. 投资要有预期、有底线、有计划
```

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| mlx-whisper 未安装 | 提示用户运行 `pip install mlx-whisper` |
| 音频下载失败 | 提示"无法下载音频，视频可能受保护或不可用" |
| 转录失败 | 提示错误信息，建议检查 mlx-whisper 安装 |
| 视频过长（>3小时） | 提示"视频较长，转录可能需要较长时间"，继续执行 |
| 磁盘空间不足 | 捕获错误，提示清理 `/tmp` 目录 |

## 进度提示

执行音频转录时，显示以下进度信息：

```
正在下载字幕... → 未找到字幕
正在下载音频... → 完成
正在使用 AI 语音识别转录（约需 X 分钟）... → 完成
正在生成摘要...
```
