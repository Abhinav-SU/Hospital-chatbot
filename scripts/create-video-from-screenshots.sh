#!/bin/bash

# Hospital Chatbot - Create Video from Screenshots

set -e

echo "🎬 Hospital Chatbot - Video Creator from Screenshots"
echo "=" 
echo ""

SCREENSHOT_DIR="screenshots"
VOICEOVER="voiceover/demo-voiceover.mp3"
OUTPUT_RAW="Hospital-Chatbot-Demo-Raw.mp4"
OUTPUT_FINAL="Hospital-Chatbot-Demo-Final.mp4"

# Get voiceover duration dynamically
if [ -f "$VOICEOVER" ]; then
    VOICEOVER_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VOICEOVER" 2>/dev/null || echo "174.816")
    # Calculate FPS: frames / duration
    FRAME_COUNT=$(ls -1 "$SCREENSHOT_DIR"/frame_*.png 2>/dev/null | wc -l)
    if [ "$FRAME_COUNT" -gt 0 ]; then
        FPS=$(awk "BEGIN {printf \"%.2f\", $FRAME_COUNT / $VOICEOVER_DURATION}")
    else
        FPS=1.32
    fi
else
    FPS=1.32
fi

# Check if screenshots exist
if [ ! -d "$SCREENSHOT_DIR" ]; then
    echo "❌ Error: Screenshots directory not found!"
    echo "   Run: python scripts/capture-chatbot-demo.py first"
    exit 1
fi

# Count screenshots
FRAME_COUNT=$(ls -1 "$SCREENSHOT_DIR"/frame_*.png 2>/dev/null | wc -l)
if [ "$FRAME_COUNT" -eq 0 ]; then
    echo "❌ Error: No screenshots found in $SCREENSHOT_DIR/"
    exit 1
fi

echo "✅ Found $FRAME_COUNT screenshot frames"
echo ""

# Create video from screenshots
echo "🎥 Creating video from screenshots (FPS=$FPS)..."
ffmpeg -y \
    -framerate $FPS \
    -pattern_type glob \
    -i "$SCREENSHOT_DIR/frame_*.png" \
    -c:v libx264 \
    -preset slow \
    -crf 18 \
    -pix_fmt yuv420p \
    -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
    "$OUTPUT_RAW" 2>&1 | grep -E "(frame=|time=|size=)" || true

if [ ! -f "$OUTPUT_RAW" ]; then
    echo "❌ Error: Failed to create video"
    exit 1
fi

echo "✅ Video created: $OUTPUT_RAW"
echo ""

# Check if voiceover exists
if [ ! -f "$VOICEOVER" ]; then
    echo "⚠️  Warning: Voiceover not found at $VOICEOVER"
    echo "   Video will be created without audio"
    mv "$OUTPUT_RAW" "$OUTPUT_FINAL"
else
    # Combine video with voiceover
    echo "🎙️ Adding voiceover to video..."
    
    ffmpeg -y \
        -i "$OUTPUT_RAW" \
        -i "$VOICEOVER" \
        -c:v copy \
        -c:a aac \
        -b:a 192k \
        -shortest \
        "$OUTPUT_FINAL" 2>&1 | grep -E "(frame=|time=|size=)" || true
    
    if [ ! -f "$OUTPUT_FINAL" ]; then
        echo "❌ Error: Failed to add voiceover"
        exit 1
    fi
    
    echo "✅ Voiceover added successfully!"
    rm "$OUTPUT_RAW"
fi

echo ""
echo "=" 
echo "✅ DEMO VIDEO COMPLETE!"
echo "=" 
echo ""
echo "📁 Output: $OUTPUT_FINAL"
ls -lh "$OUTPUT_FINAL"
echo ""

# Get video duration
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT_FINAL" 2>/dev/null || echo "unknown")
if [ "$DURATION" != "unknown" ]; then
    echo "⏱️  Duration: ${DURATION}s"
fi

echo ""
echo "🎬 Ready for upload!"
echo ""
