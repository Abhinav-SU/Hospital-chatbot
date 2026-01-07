#!/bin/bash

# Hospital Chatbot - Create Demo Video with Screenshots
# Since we're in headless environment, we'll create video from screenshots + voiceover

set -e

echo "🎬 Hospital Chatbot - Demo Video Creator (Headless Mode)"
echo "============================================================"
echo ""

# Configuration
VOICEOVER_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 voiceover/demo-voiceover.mp3 2>/dev/null || echo "175")
echo "🎙️  Voiceover duration: ${VOICEOVER_DURATION} seconds"
echo ""

# Create a simple title screen video
echo "📸 Creating title screen..."
ffmpeg -f lavfi -i color=c=#667eea:s=1920x1080:d=5 \
  -vf "drawtext=text='Hospital System Chatbot':fontsize=80:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-100,\
       drawtext=text='Natural Language Database Queries':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+50,\
       drawtext=text='Python • Streamlit • Neo4j':fontsize=30:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+150" \
  -y title_screen.mp4 -loglevel error

# Create demo interface screen (static with text overlays showing queries)
echo "📸 Creating demo screen with queries..."
ffmpeg -f lavfi -i color=c=#f8f9fa:s=1920x1080:d=$VOICEOVER_DURATION \
  -vf "drawtext=text='🏥 Hospital Chatbot Demo':fontsize=60:fontcolor=0x667eea:x=(w-text_w)/2:y=100,\
       drawtext=text='✓ California Hospitals':fontsize=35:fontcolor=0x333333:x=200:y=300,\
       drawtext=text='✓ Hospital Statistics':fontsize=35:fontcolor=0x333333:x=200:y=370,\
       drawtext=text='✓ Patient Records':fontsize=35:fontcolor=0x333333:x=200:y=440,\
       drawtext=text='✓ Visit Histories':fontsize=35:fontcolor=0x333333:x=200:y=510,\
       drawtext=text='✓ Medical Insights':fontsize=35:fontcolor=0x333333:x=200:y=580,\
       drawtext=text='✓ Physician Salaries':fontsize=35:fontcolor=0x333333:x=200:y=650,\
       drawtext=text='✓ Patient Reviews':fontsize=35:fontcolor=0x333333:x=200:y=720,\
       drawtext=text='Powered by Neo4j Graph Database':fontsize=30:fontcolor=0x666666:x=(w-text_w)/2:y=950" \
  -y demo_screen.mp4 -loglevel error

# Create ending screen
echo "📸 Creating ending screen..."
ffmpeg -f lavfi -i color=c=#667eea:s=1920x1080:d=5 \
  -vf "drawtext=text='Thank You!':fontsize=90:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2-100,\
       drawtext=text='github.com/Abhinav-SU/Hospital-chatbot':fontsize=35:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2+100" \
  -y ending_screen.mp4 -loglevel error

# Concatenate screens
echo "🔗 Combining all screens..."
echo "file 'title_screen.mp4'" > filelist.txt
echo "file 'demo_screen.mp4'" >> filelist.txt
echo "file 'ending_screen.mp4'" >> filelist.txt

ffmpeg -f concat -safe 0 -i filelist.txt -c copy Hospital-Chatbot-Demo-Raw.mp4 -y -loglevel error

# Cleanup temporary files
rm -f title_screen.mp4 demo_screen.mp4 ending_screen.mp4 filelist.txt

echo ""
echo "✅ Demo video created: Hospital-Chatbot-Demo-Raw.mp4"
echo "⏱️  Duration: ~$VOICEOVER_DURATION seconds (matches voiceover)"
echo ""
echo "🎬 Next step: Combine with voiceover"
echo "   ./scripts/combine-video-audio.sh"
echo ""
