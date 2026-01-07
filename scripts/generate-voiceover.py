#!/usr/bin/env python3
"""
Hospital Chatbot - AI Voiceover Generator
Generates professional voiceover for demo video using edge-tts
"""

import asyncio
import edge_tts
import os
import sys

# Read the voiceover script
script_file = 'scripts/voiceover-script.txt'

try:
    with open(script_file, 'r', encoding='utf-8') as f:
        script = f.read()
except FileNotFoundError:
    print(f"❌ Error: Script file not found: {script_file}")
    print("📝 Create the script file first with your voiceover text")
    sys.exit(1)

async def generate_voiceover():
    """Generate AI voiceover from script"""
    os.makedirs("voiceover", exist_ok=True)
    
    print("🎙️ Generating AI voiceover...")
    print(f"📄 Script: {script_file}")
    print(f"📊 Script length: {len(script)} characters, ~{len(script.split())} words")
    
    # Professional female voice (AriaNeural recommended)
    # Other options: en-US-JennyNeural, en-US-GuyNeural, en-GB-SoniaNeural, en-GB-RyanNeural
    voice = "en-US-AriaNeural"
    communicate = edge_tts.Communicate(script, voice)
    
    output_file = "voiceover/demo-voiceover.mp3"
    
    try:
        await communicate.save(output_file)
        print(f"\n✅ Voiceover generated successfully!")
        print(f"📁 Output: {output_file}")
        print(f"🎤 Voice: {voice} (Professional Female)")
        print(f"\n🎬 Next steps:")
        print(f"   1. Listen to the voiceover: {output_file}")
        print(f"   2. Combine with video: ./scripts/combine-video-audio.sh")
        print(f"\n💡 To try different voices:")
        print(f"   - Edit this script and change voice variable")
        print(f"   - Run: edge-tts --list-voices")
    except Exception as e:
        print(f"❌ Error generating voiceover: {e}")
        sys.exit(1)

async def list_voices():
    """List all available voices"""
    print("\n🎤 Available voices:")
    print("\nRecommended voices:")
    print("  - en-US-AriaNeural (Professional Female) ⭐")
    print("  - en-US-JennyNeural (Friendly Female)")
    print("  - en-US-GuyNeural (Professional Male)")
    print("  - en-GB-SoniaNeural (British Female)")
    print("  - en-GB-RyanNeural (British Male)")
    print("\nFor full list, run: edge-tts --list-voices")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list-voices":
        asyncio.run(list_voices())
    else:
        asyncio.run(generate_voiceover())
