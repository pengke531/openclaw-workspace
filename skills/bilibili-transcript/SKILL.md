---
name: bilibili-transcript
description: "Transcribe Bilibili videos to text with full transcript and detailed summary. Use when the user provides a Bilibili video URL and wants to: (1) Extract the complete audio content as text, (2) Get a detailed summary of the video content that doesn't lose key information, (3) Both summary and full transcript together. Automatically detects CC subtitles if available, otherwise uses Whisper speech-to-text."
---

# Bilibili Transcript

Transcribe Bilibili videos to text with detailed summary and full transcript.

## Overview

This skill provides **two outputs** for every Bilibili video:
1. **Detailed Summary** - Comprehensive overview that captures key points without losing important information
2. **Full Transcript** - Complete word-for-word transcription of the entire video

The skill uses a smart two-step approach:
1. **Check for CC subtitles** - If available, download them directly (fastest, most accurate)
2. **Speech-to-text fallback** - Use OpenAI Whisper to transcribe audio when no subtitles exist

## Requirements

- `yt-dlp` - For downloading video/audio
- `ffmpeg` - For audio processing  
- `whisper` - For speech-to-text (local, no API key needed)

## Workflow

### Step 1: Run the Transcription Script

```bash
./scripts/bilibili_transcript.sh "https://www.bilibili.com/video/BVxxxxx" [output_dir]
```

The script will:
- Detect if CC subtitles exist
- Download subtitles OR transcribe audio
- Save **full transcript** to a text file
- Output the file path

### Step 2: Generate Detailed Summary

After getting the transcript file, read the full content and generate a **detailed summary** that includes:

- **Main topic/theme** of the video
- **Key arguments or points** made (don't skip important details)
- **Specific examples or data** mentioned
- **Conclusions or recommendations**
- **Structure** - How the content is organized

**Important**: The summary should be **comprehensive**, not overly concise. Include enough detail that someone reading only the summary understands the full message.

### Step 3: Present Results to User

Format the output as:

```
## 📋 视频摘要

[Detailed summary here - comprehensive but well-organized]

---

## 📝 完整原文

[Full transcript text here - complete word-for-word content]
```

## Output Format Example

```
✅ 转录完成！

## 📋 视频摘要

这是一个关于[主题]的视频。主讲人首先介绍了[背景]，然后详细讲解了：

1. **[第一点]** - 具体内容包括...
2. **[第二点]** - 提到了关键数据...
3. **[第三点]** - 给出了实际案例...

视频最后总结[结论]，并建议[行动方案]。

关键点：
- 具体数据1：xxx
- 具体数据2：yyy
- 重要结论：zzz

---

## 📝 完整原文

[完整的时间戳文本或纯文本转录]
```

## Notes

- **Model choice**: `base` model for Chinese (good speed/accuracy balance)
- **Subtitle priority**: CC subtitles > Whisper transcription > Danmaku (not used)
- **Summary depth**: Err on the side of **too much detail** rather than too little
- **Full transcript**: Always include the complete text, not just excerpts
