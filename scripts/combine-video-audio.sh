#!/bin/bash

# Hospital Chatbot - Combine Video and Voiceover
# This script combines your screen recording with AI-generated voiceover

set -e  # Exit on error

echo "🎬 Hospital Chatbot - Video + Audio Combiner"
echo "============================================"
echo ""

# File paths
VIDEO="Hospital-Chatbot-Demo-Raw.mp4"
AUDIO="voiceover/demo-voiceover.mp3"
OUTPUT="Hospital-Chatbot-Demo-Final.mp4"

# Check if video file exists
if [ ! -f "$VIDEO" ]; then
    echo "❌ Error: Video file not found: $VIDEO"
    echo ""
    echo "📝 Please record your demo video first and save it as:"
    echo "   $VIDEO"
    echo ""
    echo "💡 Recording tips:"
    echo "   - Open http://localhost:8502 in browser"
    echo "   - Press F11 for fullscreen"
    echo "   - Use OBS Studio, Loom, or SimpleScreenRecorder"
    echo "   - Follow DEMO_SCRIPT.md for scene-by-scene guide"
    exit 1
fi

# Check if audio file exists
if [ ! -f "$AUDIO" ]; then
    echo "❌ Error: Audio file not found: $AUDIO"
    echo ""
    echo "📝 Generate voiceover first:"
    echo "   python scripts/generate-voiceover.py"
    echo ""
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: FFmpeg not installed"
    echo ""
    echo "📝 Install FFmpeg:"
    echo "   sudo apt update && sudo apt install -y ffmpeg"
    echo ""
    exit 1
fi

echo "✅ Video file found: $VIDEO"
echo "✅ Audio file found: $AUDIO"
echo "✅ FFmpeg installed"
echo ""
echo "🎥 Combining video and voiceover..."
echo ""

# Combine video and audio
ffmpeg -i "$VIDEO" -i "$AUDIO" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  -shortest \
  -y "$OUTPUT" \
  -loglevel error -stats

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Demo video created successfully!"
    echo "📁 Output: $OUTPUT"
    echo "📊 Video codec: H.264"
    echo "📊 Audio codec: AAC 192kbps"
    echo ""
    
    # Get file size
    SIZE=$(du -h "$OUTPUT" | cut -f1)
    echo "📦 File size: $SIZE"
    echo ""
    
    echo "🎬 Next steps:"
    echo "   1. Watch the video to verify sync and quality"
    echo "   2. (Optional) Upscale to 4K:"
    echo "      ffmpeg -i $OUTPUT -vf scale=3840:2160:flags=lanczos -c:v libx264 -preset slow -crf 18 -c:a copy Hospital-Chatbot-Demo-4K.mp4"
    echo "   3. Upload to YouTube"
    echo "   4. Update README.md with video link"
    echo ""
    echo "💡 Tips:"
    echo "   - If audio is out of sync, use -itsoffset parameter"
    echo "   - For better quality, use -crf 18 (larger file)"
    echo "   - For smaller file, use -crf 28 (lower quality)"
else
    echo ""
    echo "❌ Error: FFmpeg failed to combine video and audio"
    exit 1
fi
