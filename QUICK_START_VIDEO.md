# 🎬 Quick Start: Create Demo Video in 7 Steps

**Complete professional demo video in under 30 minutes!**

---

## ⚡ Fast Track

```bash
# 1. Verify system ready
./demo_preflight.sh

# 2. Install dependencies
pip install edge-tts pydub
sudo apt update && sudo apt install -y ffmpeg

# 3. Record video (use OBS/Loom/SimpleScreenRecorder)
#    - Open: http://localhost:8502
#    - Press F11 for fullscreen
#    - Follow: DEMO_SCRIPT.md
#    - Save as: Hospital-Chatbot-Demo-Raw.mp4

# 4. Generate AI voiceover
python scripts/generate-voiceover.py

# 5. Combine video + audio
./scripts/combine-video-audio.sh

# 6. Watch and verify
# Play: Hospital-Chatbot-Demo-Final.mp4

# 7. Upload to YouTube
# Done! 🎉
```

---

## 📋 Step-by-Step Guide

### Step 1: System Check ✅

```bash
cd /workspaces/Hospital-chatbot
./demo_preflight.sh
```

**Expected output:**
- ✅ Server running on port 8502
- ✅ Neo4j connected
- ✅ Demo queries work

### Step 2: Install Tools 🛠️

```bash
# Install AI voiceover tool
pip install edge-tts pydub

# Install video processor
sudo apt update && sudo apt install -y ffmpeg

# Verify installation
edge-tts --list-voices | head -10
ffmpeg -version
```

### Step 3: Record Video 🎥

**Option A: OBS Studio (Recommended)**
1. Download: https://obsproject.com/
2. Add Browser Source: http://localhost:8502
3. Set resolution: 1920x1080, 30 FPS
4. Follow scenes in [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
5. Save as: `Hospital-Chatbot-Demo-Raw.mp4`

**Option B: Loom (Easiest)**
1. Go to: https://loom.com/
2. Select "Browser Tab"
3. Choose chatbot tab (http://localhost:8502)
4. Record and download as: `Hospital-Chatbot-Demo-Raw.mp4`

**Option C: SimpleScreenRecorder (Linux)**
```bash
# Install
sudo apt install simplescreenrecorder

# Run
simplescreenrecorder

# Settings:
# - Select window with chatbot
# - Resolution: 1920x1080
# - Codec: H.264
# - Save as: Hospital-Chatbot-Demo-Raw.mp4
```

**Recording Tips:**
- ⏱️ Aim for 3-4 minutes total
- 🖱️ Move cursor slowly and deliberately
- ⏸️ Pause 2-3 seconds after each response
- 🧹 Clear chat history before starting
- 🖥️ Use F11 for fullscreen mode

### Step 4: Generate Voiceover 🎙️

```bash
# Generate AI voiceover from script
python scripts/generate-voiceover.py
```

**Output:** `voiceover/demo-voiceover.mp3`

**Want a different voice?**
```bash
# List available voices
edge-tts --list-voices

# Edit the script and change voice:
nano scripts/generate-voiceover.py
# Change: voice = "en-US-AriaNeural"
# To: voice = "en-US-GuyNeural" (male)
```

**Edit voiceover script:**
```bash
nano scripts/voiceover-script.txt
# Make changes, then regenerate:
python scripts/generate-voiceover.py
```

### Step 5: Combine Video + Audio 🎬

```bash
./scripts/combine-video-audio.sh
```

**Output:** `Hospital-Chatbot-Demo-Final.mp4`

**If audio is out of sync:**
```bash
# Delay audio by 0.5 seconds
ffmpeg -i Hospital-Chatbot-Demo-Raw.mp4 -i voiceover/demo-voiceover.mp3 \
  -itsoffset 0.5 -i voiceover/demo-voiceover.mp3 \
  -c:v libx264 -c:a aac -b:a 192k \
  -map 0:v:0 -map 2:a:0 \
  -shortest -y Hospital-Chatbot-Demo-Final.mp4
```

### Step 6: Watch & Verify ✅

```bash
# Play the video (in VS Code or external player)
# Check:
# - Audio syncs with video
# - Volume is good
# - No glitches or black screens
# - Demo flows smoothly
```

### Step 7: Upload to YouTube 📤

1. **Go to:** https://www.youtube.com/upload
2. **Upload:** `Hospital-Chatbot-Demo-Final.mp4`
3. **Title:** "Hospital System Chatbot - Natural Language Queries with Python, Streamlit & Neo4j"
4. **Description:** (See [VIDEO_DEMO_GUIDE.md](VIDEO_DEMO_GUIDE.md) for full template)
5. **Tags:** Python, Chatbot, Neo4j, Streamlit, Healthcare, AI, Graph Database
6. **Thumbnail:** Screenshot of chatbot interface
7. **Publish** and copy URL!

---

## 🎯 Optional: Upscale to 4K

```bash
# Upscale to 4K (takes 10-15 minutes)
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 \
  -vf "scale=3840:2160:flags=lanczos" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a copy \
  -y Hospital-Chatbot-Demo-4K.mp4

# Upload the 4K version to YouTube
```

---

## 🔧 Troubleshooting

### Video file not found
```bash
# Make sure file is named exactly:
ls -lh Hospital-Chatbot-Demo-Raw.mp4

# If different name, rename it:
mv "your-video.mp4" Hospital-Chatbot-Demo-Raw.mp4
```

### FFmpeg not installed
```bash
sudo apt update && sudo apt install -y ffmpeg
```

### edge-tts not installed
```bash
pip install edge-tts pydub
```

### Audio/video out of sync
```bash
# Try delaying audio by 0.5 seconds (see Step 5)
# Or regenerate voiceover with adjusted script timing
```

### Chatbot not running
```bash
# Check if server is running
lsof -i :8502

# If not running, start it:
streamlit run chatbot_ai.py --server.port 8502
```

---

## 📚 Additional Resources

- **Full Guide:** [VIDEO_DEMO_GUIDE.md](VIDEO_DEMO_GUIDE.md) - Complete detailed guide
- **Demo Script:** [DEMO_SCRIPT.md](DEMO_SCRIPT.md) - 3-minute voiceover script
- **Quick Reference:** [QUICK_DEMO_GUIDE.md](QUICK_DEMO_GUIDE.md) - Test questions
- **Pre-flight Check:** `./demo_preflight.sh` - Verify system ready

---

## 🎊 Success Checklist

- [ ] System verified ready (demo_preflight.sh passed)
- [ ] FFmpeg and edge-tts installed
- [ ] Screen recording software installed
- [ ] Video recorded (3-4 minutes)
- [ ] Voiceover generated
- [ ] Video + audio combined
- [ ] Final video plays correctly
- [ ] Audio syncs with video
- [ ] Uploaded to YouTube
- [ ] README.md updated with video link

---

**🚀 You've got this! The complete process takes 20-30 minutes from start to finish.**

**Questions? Check [VIDEO_DEMO_GUIDE.md](VIDEO_DEMO_GUIDE.md) for detailed troubleshooting.**
