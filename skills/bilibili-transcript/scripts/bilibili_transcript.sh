#!/bin/bash
# B站视频字幕智能获取脚本
# 优先使用CC字幕，没有则语音转录
# 输出：完整原文保存到文件

VIDEO_URL="$1"
OUTPUT_DIR="${2:-/tmp}"

if [ -z "$VIDEO_URL" ]; then
    echo "用法: $0 <B站视频链接> [输出目录]"
    exit 1
fi

echo "🔍 正在检查视频字幕信息..."

# 尝试下载字幕（只检测，不下载视频）
SUB_CHECK=$(yt-dlp --list-subs "$VIDEO_URL" 2>&1)

# 检查是否有真正的人工字幕（不是danmaku）
HAS_REAL_SUBS=false

# 检查输出中是否有实际的语言字幕（排除danmaku）
if echo "$SUB_CHECK" | grep -E "^[[:space:]]*(zh|en|ja|ko)-" | grep -v "danmaku" | grep -q "[[:space:]]"; then
    HAS_REAL_SUBS=true
fi

# 或者检查是否有 "Available subtitles" 且不是只有 danmaku
if echo "$SUB_CHECK" | grep -q "Available subtitles"; then
    # 提取字幕列表，排除danmaku
    REAL_SUB_COUNT=$(echo "$SUB_CHECK" | grep -E "^[[:space:]]*(zh|en|ja|ko)-" | grep -v "danmaku" | wc -l)
    if [ "$REAL_SUB_COUNT" -gt 0 ]; then
        HAS_REAL_SUBS=true
    fi
fi

if [ "$HAS_REAL_SUBS" = true ]; then
    echo "✅ 发现人工字幕，优先下载..."
    
    # 下载字幕（优先srt格式）
    yt-dlp --skip-download --write-subs --sub-langs zh-CN,zh-TW,zh-Hans,zh --convert-subs srt \
        -o "${OUTPUT_DIR}/bilibili_subtitle.%(ext)s" "$VIDEO_URL" 2>&1
    
    # 找到下载的字幕文件
    SUB_FILE=$(find "$OUTPUT_DIR" -maxdepth 1 -name "bilibili_subtitle*.srt" -type f 2>/dev/null | head -1)
    
    if [ -n "$SUB_FILE" ] && [ -s "$SUB_FILE" ]; then
        echo "✅ 字幕下载成功: $SUB_FILE"
        
        # 转换为纯文本（去除时间戳和序号）
        TXT_FILE="${OUTPUT_DIR}/bilibili_transcript.txt"
        sed '/^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]/d' "$SUB_FILE" | sed '/^[0-9]*$/d' | sed '/^$/d' > "$TXT_FILE"
        
        echo "📝 完整原文已保存: $TXT_FILE"
        echo "$TXT_FILE"
        exit 0
    else
        echo "⚠️  字幕下载失败或为空，切换到语音转录..."
    fi
else
    echo "⚠️  没有人工字幕（只有弹幕），使用语音转录..."
fi

# 语音转录流程
echo "⬇️  正在下载音频..."
yt-dlp -x --audio-format mp3 -o "${OUTPUT_DIR}/bilibili_audio.%(ext)s" "$VIDEO_URL" 2>&1

AUDIO_FILE=$(find "$OUTPUT_DIR" -maxdepth 1 \( -name "bilibili_audio*.mp3" -o -name "bilibili_audio*.m4a" \) 2>/dev/null | head -1)

if [ -z "$AUDIO_FILE" ]; then
    echo "❌ 音频下载失败"
    exit 1
fi

echo "🎤 正在语音转录（使用base模型）..."
whisper "$AUDIO_FILE" --model base --output_format txt --output_dir "$OUTPUT_DIR" --language Chinese 2>&1

TXT_FILE="${OUTPUT_DIR}/bilibili_audio.txt"
if [ -f "$TXT_FILE" ] && [ -s "$TXT_FILE" ]; then
    echo "📝 完整原文已保存: $TXT_FILE"
    echo "$TXT_FILE"
else
    echo "❌ 转录失败"
    exit 1
fi
