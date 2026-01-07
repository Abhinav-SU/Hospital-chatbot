# 🎬 Hospital Chatbot Demo Video & Voiceover Guide

Complete step-by-step guide to create a professional demo video with AI voiceover for the Hospital System Chatbot.

---

## 📋 Prerequisites

### Required Software

1. **Python 3.12+** (Already installed)
   ```bash
   python --version  # Should be 3.12+
   ```

2. **FFmpeg** (for video/audio processing)
   ```bash
   ffmpeg -version  # Check if installed
   ```
   
   **Install FFmpeg (Linux/Codespaces):**
   ```bash
   sudo apt update && sudo apt install -y ffmpeg
   ```

3. **Screen Recording Software**
   - **OBS Studio** (Free, all platforms) - https://obsproject.com/
   - **Loom** (Free, Browser-based) - https://loom.com/
   - **QuickTime** (Mac built-in)
   - **SimpleScreenRecorder** (Linux)

4. **Python packages** (for AI voiceover)
   ```bash
   pip install edge-tts pydub
   ```

### Application Setup

1. **Verify chatbot is running:**
   ```bash
   ./demo_preflight.sh
   ```
   
   Should show:
   - ✅ Server running on port 8502
   - ✅ Neo4j connected
   - ✅ All demo queries work

2. **Open the chatbot:**
   - URL: http://localhost:8502
   - Clear any existing chat history

3. **Test queries ready:**
   - Review QUICK_DEMO_GUIDE.md for test questions
   - All 8 core queries should work

---

## 🎥 Step 1: Record the Video

### Recording Setup

1. **Prepare your browser:**
   ```bash
   # Open chatbot in browser
   # Press F11 for fullscreen mode
   # Clear chat history if needed
   ```

2. **Start your screen recorder:**
   - **OBS Studio:**
     - Add Browser Source: http://localhost:8502
     - Resolution: 1920x1080 (Full HD)
     - FPS: 30
     
   - **Loom:**
     - Select "Full Desktop" or "Browser Tab"
     - Choose http://localhost:8502 tab
     
   - **SimpleScreenRecorder (Linux):**
     ```bash
     simplescreenrecorder
     ```
     - Select window containing chatbot
     - Resolution: 1920x1080
     - Video codec: H.264
     - Audio: None (we'll add voiceover later)

### Recording Process

Follow this scene-by-scene guide (from DEMO_SCRIPT.md):

**Scene 1 (0:00-0:15): Introduction**
- Show the chatbot interface
- Highlight sidebar with About and Example Questions
- Pan to main chat area

**Scene 2 (0:15-0:35): Interface Overview**
- Scroll sidebar to show example questions
- Highlight chat input at bottom
- Show title and info message

**Scene 3 (0:35-1:15): Hospital Queries**
- Type: "Show me all hospitals in California"
- Wait for response
- Type: "What are the hospital statistics?"
- Wait for response

**Scene 4 (1:15-1:50): Patient Data**
- Type: "Which patients were treated by Dr. Sarah Johnson?"
- Wait for response
- Type: "What is the visit history for patient John Smith?"
- Wait for response

**Scene 5 (1:50-2:20): Medical Insights**
- Type: "Show me the most common diagnoses"
- Wait for response
- Type: "Which physicians have the highest salaries?"
- Wait for response

**Scene 6 (2:20-2:45): Reviews**
- Type: "Show me patient reviews"
- Wait for response

**Scene 7 (2:45-3:15): Natural Language Demo**
- Type a custom question
- Type another custom question
- Show chat history

**Scene 8 (3:15-3:35): Conclusion**
- Scroll through chat history
- Show sidebar again
- End on chatbot home screen

### Save Your Recording

- **OBS Studio:** Stop recording → File saved in Videos folder
- **Loom:** Click "Stop" → Download video
- **SimpleScreenRecorder:** Stop → Save as `hospital-chatbot-demo.mp4`

**Recommended filename:** `Hospital-Chatbot-Demo-Raw.mp4`

---

## 🎙️ Step 2: Create Voiceover Script

### Write Your Script

Create `scripts/voiceover-script.txt`:

```txt
Hello! Today I'm going to demonstrate a Hospital System Chatbot built with Python, Streamlit, and Neo4j graph database.

This chatbot can answer questions about patients, hospitals, physicians, visits, and insurance data using natural language.

The interface is clean and simple. On the left sidebar, you can see the About section explaining what the chatbot does, and below that are example questions you can ask.

The main area has a chat interface where we can type our questions.

Let's start with a simple query. I'll ask "Show me all hospitals in California."

As you can see, the chatbot successfully retrieved hospitals located in California from the Neo4j database.

Now let's get some statistics. I'll ask "What are the hospital statistics?"

The chatbot returns visit counts for each hospital, showing us which hospitals have the most patient visits.

The chatbot can also query patient information. Let me ask about patients treated by a specific physician - Dr. Sarah Johnson.

Great! It returns a list of patients who were treated by Dr. Sarah Johnson, showing the relationships in our graph database.

We can also look up individual patient histories. Let's check John Smith's visit history.

The chatbot retrieves John Smith's medical visits, including diagnoses and visit dates.

The system can analyze medical data patterns. Let me ask about the most common diagnoses.

Here we see the most frequently occurring diagnoses across all patients.

We can also query financial and administrative data, like physician salaries.

The chatbot returns physicians ranked by salary.

Finally, let's look at patient reviews - this is unstructured text data stored in the database.

The chatbot retrieves actual patient reviews, showing both positive and negative feedback.

The beauty of this chatbot is its natural language understanding. I can ask questions in plain English, and it converts them to database queries automatically.

The chatbot understood my question, generated the appropriate database query, and returned the answer.

As you can see, this chatbot successfully demonstrates querying a hospital system database using natural language.

It handles various types of questions - from simple lookups to complex aggregations and reviews.

The system uses Neo4j graph database for efficient relationship queries, and Streamlit provides this clean, user-friendly interface.

This demonstrates the power of combining modern technologies with graph databases for healthcare data.

Thank you for watching this demonstration!
```

### Save the Script

```bash
mkdir -p scripts
nano scripts/voiceover-script.txt
# Paste the script above
# Save: Ctrl+O, Enter, Ctrl+X
```

---

## 🎤 Step 3: Generate AI Voiceover

### Create Voiceover Generator

Create `scripts/generate-voiceover.py`:

```python
import asyncio
import edge_tts
import os

# Read the voiceover script
with open('scripts/voiceover-script.txt', 'r', encoding='utf-8') as f:
    script = f.read()

async def generate_voiceover():
    os.makedirs("voiceover", exist_ok=True)
    
    # Professional female voice (AriaNeural recommended)
    # Other options: en-US-JennyNeural, en-US-GuyNeural, en-GB-SoniaNeural
    communicate = edge_tts.Communicate(script, "en-US-AriaNeural")
    
    output_file = "voiceover/demo-voiceover.mp3"
    await communicate.save(output_file)
    
    print(f"✅ Voiceover generated: {output_file}")
    print(f"📊 Voice: en-US-AriaNeural (Professional Female)")

if __name__ == "__main__":
    asyncio.run(generate_voiceover())
```

### Run the Generator

```bash
python scripts/generate-voiceover.py
```

**Output:** `voiceover/demo-voiceover.mp3`

### Available Voices

Test different voices to find your favorite:

- **`en-US-AriaNeural`** - Professional female (recommended)
- **`en-US-JennyNeural`** - Friendly female
- **`en-US-GuyNeural`** - Professional male
- **`en-GB-SoniaNeural`** - British female
- **`en-GB-RyanNeural`** - British male

**List all available voices:**
```bash
edge-tts --list-voices
```

---

## 🎬 Step 4: Combine Video + Audio

### Method 1: Automatic Script (Recommended)

Create `scripts/combine-video-audio.sh`:

```bash
#!/bin/bash

# Hospital Chatbot - Combine Video and Voiceover
echo "🎬 Combining video and voiceover..."

# Find video file
VIDEO="Hospital-Chatbot-Demo-Raw.mp4"
AUDIO="voiceover/demo-voiceover.mp3"
OUTPUT="Hospital-Chatbot-Demo-Final.mp4"

# Check if files exist
if [ ! -f "$VIDEO" ]; then
    echo "❌ Error: Video file not found: $VIDEO"
    echo "📝 Make sure you've recorded the demo and saved it as: $VIDEO"
    exit 1
fi

if [ ! -f "$AUDIO" ]; then
    echo "❌ Error: Audio file not found: $AUDIO"
    echo "📝 Run: python scripts/generate-voiceover.py"
    exit 1
fi

# Combine video and audio
ffmpeg -i "$VIDEO" -i "$AUDIO" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  -shortest \
  -y "$OUTPUT"

if [ $? -eq 0 ]; then
    echo "✅ Demo video created: $OUTPUT"
    echo "📊 Video codec: H.264"
    echo "📊 Audio codec: AAC 192kbps"
    echo ""
    echo "🎥 Next steps:"
    echo "   1. Watch the video to check sync"
    echo "   2. Upscale to 4K (optional): ffmpeg -i $OUTPUT -vf scale=3840:2160:flags=lanczos -c:v libx264 -preset slow -crf 18 -c:a copy Hospital-Chatbot-Demo-4K.mp4"
    echo "   3. Upload to YouTube"
else
    echo "❌ Error: FFmpeg failed"
    exit 1
fi
```

Make it executable and run:
```bash
chmod +x scripts/combine-video-audio.sh
./scripts/combine-video-audio.sh
```

### Method 2: Manual FFmpeg Command

```bash
ffmpeg -i Hospital-Chatbot-Demo-Raw.mp4 -i voiceover/demo-voiceover.mp3 \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  -shortest \
  -y Hospital-Chatbot-Demo-Final.mp4
```

**Parameters explained:**
- `-c:v libx264` - H.264 video codec (universal compatibility)
- `-preset medium` - Encoding speed/quality balance
- `-crf 23` - Quality (18-28, lower = better, 23 = good default)
- `-c:a aac` - AAC audio codec
- `-b:a 192k` - Audio bitrate (192kbps = good quality)
- `-shortest` - Match video to audio length (or vice versa)
- `-y` - Overwrite output file without asking

### Sync Audio with Video

If audio is out of sync:

```bash
# Delay audio by 0.5 seconds (if voiceover starts too early)
ffmpeg -i Hospital-Chatbot-Demo-Raw.mp4 -i voiceover/demo-voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -itsoffset 0.5 -i voiceover/demo-voiceover.mp3 \
  -map 0:v:0 -map 2:a:0 \
  -shortest Hospital-Chatbot-Demo-Final.mp4

# Speed up audio by 5% (if voiceover is too slow)
ffmpeg -i voiceover/demo-voiceover.mp3 -filter:a "atempo=1.05" voiceover/demo-voiceover-fast.mp3
```

---

## 🎞️ Step 5: Upscale to 4K (Optional)

### Upscale to 2K (2560x1440)

```bash
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 \
  -vf "scale=2560:1440:flags=lanczos" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a copy \
  -y Hospital-Chatbot-Demo-2K.mp4
```

### Upscale to 4K (3840x2160)

```bash
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 \
  -vf "scale=3840:2160:flags=lanczos" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a copy \
  -y Hospital-Chatbot-Demo-4K.mp4
```

**Parameters:**
- `scale=3840:2160` - 4K resolution
- `flags=lanczos` - High-quality scaling (best for upscaling)
- `-preset slow` - Better quality, slower encoding
- `-crf 18` - Very high quality (18 = nearly lossless)
- `-c:a copy` - Copy audio without re-encoding

**⏱️ Note:** Upscaling takes time. A 3-minute video may take 10-15 minutes.

---

## ✂️ Step 6: Trim & Adjust (Optional)

### Trim Video

```bash
# Remove first 2 seconds (if recording starts too early)
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 -ss 00:00:02 -c copy trimmed.mp4

# Trim to exact duration (3 minutes 30 seconds)
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 -t 00:03:30 -c copy trimmed.mp4

# Trim specific segment (from 5s to 3min 30s)
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 -ss 00:00:05 -to 00:03:30 -c copy trimmed.mp4
```

### Adjust Audio Volume

```bash
# Increase volume by 50%
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 -af "volume=1.5" -c:v copy louder.mp4

# Normalize audio (recommended for consistent volume)
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:v copy normalized.mp4
```

### Add Title Screen (Optional)

```bash
# Create a 5-second title screen
ffmpeg -f lavfi -i color=c=black:s=1920x1080:d=5 \
  -vf "drawtext=text='Hospital System Chatbot':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
  title.mp4

# Concatenate title + demo
echo "file 'title.mp4'" > filelist.txt
echo "file 'Hospital-Chatbot-Demo-Final.mp4'" >> filelist.txt
ffmpeg -f concat -safe 0 -i filelist.txt -c copy Hospital-Chatbot-Demo-WithTitle.mp4
```

---

## 📤 Step 7: Upload & Share

### Upload to YouTube

1. **Go to:** https://www.youtube.com/upload

2. **Upload:** `Hospital-Chatbot-Demo-4K.mp4` (or Final version)

3. **Video Details:**
   - **Title:** "Hospital System Chatbot - Natural Language Database Queries with Python, Streamlit & Neo4j"
   - **Description:**
     ```
     A demonstration of an AI-powered hospital system chatbot that answers questions about patients, physicians, hospitals, visits, and insurance data using natural language.
     
     🔧 Tech Stack:
     - Python 3.12
     - Streamlit 1.31.0
     - Neo4j Graph Database
     - Natural Language Processing
     
     💬 Features:
     - Ask questions in plain English
     - Query patient records, physician data, hospital statistics
     - View patient reviews and medical insights
     - Real-time graph database queries
     
     📊 Database:
     - 5 Hospitals
     - 10 Patients
     - 5 Physicians
     - 10 Visits & Reviews
     
     🔗 GitHub: https://github.com/Abhinav-SU/Hospital-chatbot
     
     #Python #Chatbot #Neo4j #GraphDatabase #Streamlit #Healthcare #AI #NaturalLanguageProcessing #DataScience
     ```
   
   - **Thumbnail:** Use a screenshot of the chatbot interface
   - **Visibility:** Public or Unlisted
   - **Tags:** Python, Chatbot, Neo4j, Streamlit, Healthcare, Graph Database, AI, NLP

4. **Copy the video URL:** `https://www.youtube.com/watch?v=YOUR_VIDEO_ID`

### Update README

Add to your README.md:

```markdown
## 🎥 Demo Video

[![Hospital Chatbot Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

Watch the full demonstration to see the chatbot in action!
```

### Share on Social Media

**LinkedIn Post:**
```
🏥 Just built a Hospital System Chatbot using Python, Streamlit, and Neo4j!

Ask questions in plain English about:
✅ Patients & physicians
✅ Hospital visits & diagnoses  
✅ Medical statistics & insights
✅ Patient reviews

The chatbot converts natural language to database queries in real-time using Neo4j graph database.

🎥 Watch the demo: [YouTube URL]
💻 GitHub: https://github.com/Abhinav-SU/Hospital-chatbot

#Python #AI #GraphDatabase #Healthcare #DataScience
```

**Twitter/X:**
```
🏥 Built a hospital chatbot with Python + Neo4j! 

Ask questions in plain English → Get instant answers from graph database

Features:
✅ Natural language queries
✅ Patient/physician data
✅ Medical insights
✅ Real-time responses

🎥 Demo: [YouTube URL]
💻 Code: [GitHub URL]

#Python #AI #Neo4j
```

---

## 🔧 Troubleshooting

### Video Recording Issues

**Problem:** Screen recorder lag/stuttering
- **Solution:** Close unnecessary programs, record at 720p instead of 1080p

**Problem:** Mouse cursor not visible
- **Solution:** Enable cursor recording in OBS/recorder settings

**Problem:** Chat responses too slow during recording
- **Solution:** Wait patiently, or edit pauses out later

### Voiceover Issues

**Problem:** `edge-tts` not installed
- **Solution:** `pip install edge-tts`

**Problem:** Voice sounds robotic
- **Solution:** Try different voices: `en-US-JennyNeural`, `en-US-GuyNeural`

**Problem:** Audio too fast/slow
- **Solution:** Adjust script, add pauses (blank lines), or use `atempo` filter

### FFmpeg Issues

**Problem:** FFmpeg not found
- **Solution:** `sudo apt install ffmpeg` (Linux) or download from ffmpeg.org

**Problem:** Audio/video out of sync
- **Solution:** Use `-itsoffset` parameter to delay audio

**Problem:** Output file too large
- **Solution:** Increase CRF (e.g., `-crf 28`) for smaller file size

### Quality Issues

**Problem:** Video looks pixelated
- **Solution:** Record at higher resolution (1920x1080 minimum)

**Problem:** Audio quality poor
- **Solution:** Use higher bitrate: `-b:a 256k` or `-b:a 320k`

---

## 📊 Complete Workflow Summary

```bash
# 1. Start the chatbot
./demo_preflight.sh  # Verify everything works

# 2. Record demo video
# Use OBS Studio, Loom, or SimpleScreenRecorder
# Follow DEMO_SCRIPT.md for scene-by-scene guide
# Save as: Hospital-Chatbot-Demo-Raw.mp4

# 3. Create voiceover script
nano scripts/voiceover-script.txt
# Write your script (see Step 2 above)

# 4. Generate AI voiceover
python scripts/generate-voiceover.py

# 5. Combine video + audio
./scripts/combine-video-audio.sh

# 6. (Optional) Upscale to 4K
ffmpeg -i Hospital-Chatbot-Demo-Final.mp4 \
  -vf "scale=3840:2160:flags=lanczos" \
  -c:v libx264 -preset slow -crf 18 \
  -c:a copy \
  Hospital-Chatbot-Demo-4K.mp4

# 7. Upload to YouTube and share!
```

---

## 📝 Tips & Best Practices

### Recording Tips

1. **Clean interface:** Clear chat history before recording
2. **Smooth typing:** Type slowly and deliberately
3. **Wait for responses:** Pause 2-3 seconds after each answer
4. **Mouse movements:** Move cursor smoothly, avoid erratic movements
5. **Full screen:** Use F11 to hide browser UI

### Script Writing Tips

1. **Match timing:** Write script while watching video
2. **Natural pauses:** Add blank lines for breathing room
3. **Clear pronunciation:** Avoid complex words or jargon
4. **Enthusiasm:** Use exclamation points for energy
5. **Length:** Aim for 600-800 words for 3-minute video

### Video Quality Tips

1. **Resolution:** Record at 1920x1080 minimum
2. **Frame rate:** 30 FPS is standard, 60 FPS for smooth motion
3. **Bitrate:** Use CRF 18-23 for quality
4. **Audio:** 192kbps AAC is good, 256kbps for best quality
5. **File size:** Balance quality vs. file size (4K videos are large!)

### YouTube Optimization

1. **Thumbnail:** Create custom thumbnail with title text
2. **Title:** Include keywords: "Python", "Chatbot", "Neo4j"
3. **Description:** Detailed, with timestamps and links
4. **Tags:** Use 10-15 relevant tags
5. **End screen:** Add subscribe button and related videos

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Test chatbot | `./demo_preflight.sh` |
| Generate voiceover | `python scripts/generate-voiceover.py` |
| Combine video+audio | `./scripts/combine-video-audio.sh` |
| Upscale to 4K | `ffmpeg -i input.mp4 -vf "scale=3840:2160:flags=lanczos" -c:v libx264 -preset slow -crf 18 -c:a copy output-4k.mp4` |
| Trim video | `ffmpeg -i input.mp4 -ss 00:00:05 -t 00:03:30 -c copy trimmed.mp4` |
| Normalize audio | `ffmpeg -i input.mp4 -af "loudnorm=I=-16" -c:v copy normalized.mp4` |
| List voices | `edge-tts --list-voices` |

---

## ✅ Pre-Upload Checklist

Before uploading to YouTube:

- [ ] Video plays without errors
- [ ] Audio is in sync throughout
- [ ] Audio volume is consistent
- [ ] No black screens or glitches
- [ ] Video is at least 720p (preferably 1080p+)
- [ ] Audio quality is clear and professional
- [ ] Demo covers all key features
- [ ] Video length is appropriate (2-4 minutes ideal)
- [ ] Title and description are ready
- [ ] Custom thumbnail created
- [ ] Tags and keywords added

---

**🎬 You're ready to create an amazing demo video! Follow this guide step by step, and you'll have a professional showcase of your Hospital Chatbot.**

**Need help? Check the troubleshooting section or refer to the individual script files for detailed comments.**
