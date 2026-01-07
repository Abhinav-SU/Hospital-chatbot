# 🎬 Demo Video Creation - Complete Resource Map

## 📚 All Resources at a Glance

### 🚀 Quick Start (Start Here!)
- **[QUICK_START_VIDEO.md](QUICK_START_VIDEO.md)** ⭐
  - 7-step fast track guide
  - Complete workflow in 30 minutes
  - Troubleshooting included

### 📖 Detailed Guides
1. **[VIDEO_DEMO_GUIDE.md](VIDEO_DEMO_GUIDE.md)** - Complete comprehensive guide
   - Prerequisites & software installation
   - Recording tips and best practices
   - AI voiceover generation
   - Video editing with FFmpeg
   - Upscaling to 4K
   - YouTube upload guide
   - Social media sharing templates

2. **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - Voiceover script
   - 3-minute script with exact timing
   - Scene-by-scene breakdown
   - Alternative 2-minute version
   - Recording tool recommendations

3. **[QUICK_DEMO_GUIDE.md](QUICK_DEMO_GUIDE.md)** - Quick reference
   - 8 test questions with expected results
   - Key talking points
   - Timing guide
   - Social media snippets

4. **[README_DEMO.md](README_DEMO.md)** - System documentation
   - Features overview
   - Database contents
   - Technology stack
   - Recording metrics

### 🛠️ Scripts & Tools

#### Verification
- **`demo_preflight.sh`** - Pre-recording system check
  ```bash
  ./demo_preflight.sh
  ```
  - Checks server running
  - Verifies Neo4j connection
  - Tests demo queries
  - Reports readiness status

#### Voiceover Generation
- **`scripts/voiceover-script.txt`** - Voiceover text
  - Professional script (~600 words)
  - Matches demo video timing
  - Edit to customize

- **`scripts/generate-voiceover.py`** - AI voice generator
  ```bash
  python scripts/generate-voiceover.py
  ```
  - Generates MP3 voiceover
  - Uses Microsoft Edge TTS
  - Professional voice options
  - Output: `voiceover/demo-voiceover.mp3`

#### Video Processing
- **`scripts/combine-video-audio.sh`** - Video+Audio combiner
  ```bash
  ./scripts/combine-video-audio.sh
  ```
  - Combines video with voiceover
  - Uses FFmpeg
  - Output: `Hospital-Chatbot-Demo-Final.mp4`

---

## 🎯 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEMO VIDEO CREATION WORKFLOW                  │
└─────────────────────────────────────────────────────────────────┘

STEP 1: Preparation
    │
    ├─► Run: ./demo_preflight.sh
    │   └─► Verify: Server, Neo4j, Demo queries
    │
    ├─► Install: pip install edge-tts pydub
    │   └─► Install: sudo apt install ffmpeg
    │
    └─► Review: DEMO_SCRIPT.md

STEP 2: Record Video
    │
    ├─► Tools: OBS Studio, Loom, SimpleScreenRecorder
    ├─► URL: http://localhost:8502
    ├─► Duration: 3-4 minutes
    ├─► Resolution: 1920x1080
    │
    └─► Save as: Hospital-Chatbot-Demo-Raw.mp4

STEP 3: Generate Voiceover
    │
    ├─► Optional: Edit scripts/voiceover-script.txt
    │
    ├─► Run: python scripts/generate-voiceover.py
    │
    └─► Output: voiceover/demo-voiceover.mp3

STEP 4: Combine Video + Audio
    │
    ├─► Run: ./scripts/combine-video-audio.sh
    │
    └─► Output: Hospital-Chatbot-Demo-Final.mp4

STEP 5: Optional - Upscale to 4K
    │
    └─► Run: ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 \
             -vf scale=3840:2160:flags=lanczos \
             -c:v libx264 -preset slow -crf 18 \
             -c:a copy Hospital-Chatbot-Demo-4K.mp4

STEP 6: Upload to YouTube
    │
    ├─► Upload: Hospital-Chatbot-Demo-Final.mp4
    ├─► Use templates from VIDEO_DEMO_GUIDE.md
    │   └─► Title, Description, Tags
    │
    └─► Copy URL and update README.md

STEP 7: Share
    │
    └─► Use social media templates from QUICK_DEMO_GUIDE.md
        ├─► LinkedIn
        ├─► Twitter/X
        └─► YouTube description
```

---

## 📦 File Structure

```
Hospital-Chatbot/
├── 📘 Guides
│   ├── QUICK_START_VIDEO.md          ⭐ Start here!
│   ├── VIDEO_DEMO_GUIDE.md           📖 Complete guide
│   ├── DEMO_SCRIPT.md                🎙️ Voiceover script
│   ├── QUICK_DEMO_GUIDE.md           📋 Quick reference
│   └── README_DEMO.md                📊 System docs
│
├── 🛠️ Scripts
│   ├── demo_preflight.sh             ✅ System check
│   ├── generate-voiceover.py         🎤 AI voiceover
│   ├── combine-video-audio.sh        🎬 Video+Audio
│   └── voiceover-script.txt          📝 Script text
│
├── 💬 Chatbot
│   ├── chatbot_ai.py                 🤖 Main app
│   ├── load_data.py                  📊 Data loader
│   └── requirements.txt              📦 Dependencies
│
├── 📁 Data
│   └── data/*.csv                    📊 Hospital data
│
└── 🎥 Output (created by you)
    ├── Hospital-Chatbot-Demo-Raw.mp4     🎥 Your recording
    ├── voiceover/demo-voiceover.mp3       🎙️ AI voice
    ├── Hospital-Chatbot-Demo-Final.mp4    ✅ Final video
    └── Hospital-Chatbot-Demo-4K.mp4      🌟 4K version
```

---

## ⚡ Quick Commands

```bash
# System check
./demo_preflight.sh

# Install dependencies
pip install edge-tts pydub
sudo apt install ffmpeg

# Generate voiceover
python scripts/generate-voiceover.py

# Combine video + audio
./scripts/combine-video-audio.sh

# Upscale to 4K
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 \
  -vf scale=3840:2160:flags=lanczos \
  -c:v libx264 -preset slow -crf 18 \
  -c:a copy Hospital-Chatbot-Demo-4K.mp4
```

---

## 🎯 Key Features

### Recording Software Options
- **OBS Studio** - Free, powerful, all platforms
- **Loom** - Easy, browser-based, free tier
- **SimpleScreenRecorder** - Linux-native, lightweight
- **QuickTime** - Mac built-in

### AI Voiceover Voices
- `en-US-AriaNeural` - Professional female ⭐ (default)
- `en-US-JennyNeural` - Friendly female
- `en-US-GuyNeural` - Professional male
- `en-GB-SoniaNeural` - British female
- `en-GB-RyanNeural` - British male

### Video Quality Options
- **720p** - 1280x720 (Fast, smaller file)
- **1080p** - 1920x1080 (Standard HD) ⭐
- **2K** - 2560x1440 (High quality)
- **4K** - 3840x2160 (Ultra quality)

---

## 📊 Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Video Length | 3-4 minutes | ⏱️ Plan |
| Resolution | 1920x1080+ | 📐 Set |
| Audio Quality | 192kbps AAC | 🔊 Ready |
| File Size | <100MB (1080p) | 📦 Good |
| Upload Speed | <5 minutes | ⚡ Fast |
| Sync Quality | Perfect | ✅ Test |

---

## 🔍 Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| Chatbot not running | `./demo_preflight.sh` |
| FFmpeg not found | `sudo apt install ffmpeg` |
| edge-tts not installed | `pip install edge-tts pydub` |
| Audio out of sync | See VIDEO_DEMO_GUIDE.md Step 4 |
| Video too large | Use `-crf 28` for smaller size |
| Voice sounds robotic | Try different voice in script |
| Recording lags | Close apps, record at 720p |

---

## 🎊 Next Steps

1. **Start**: Open [QUICK_START_VIDEO.md](QUICK_START_VIDEO.md)
2. **Verify**: Run `./demo_preflight.sh`
3. **Record**: Follow DEMO_SCRIPT.md
4. **Process**: Use scripts to combine
5. **Upload**: Share on YouTube!

---

**📚 Documentation Status:**
- ✅ Quick Start Guide
- ✅ Complete Video Guide
- ✅ Demo Script with Timing
- ✅ Quick Reference Card
- ✅ System Documentation
- ✅ Automated Scripts
- ✅ AI Voiceover System
- ✅ FFmpeg Workflow
- ✅ Troubleshooting Guide
- ✅ Social Media Templates

**🎬 Everything you need to create a professional demo video is ready!**
