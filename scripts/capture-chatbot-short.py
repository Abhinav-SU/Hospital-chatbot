#!/usr/bin/env python3
"""
Improved screenshot capture with proper wait times for chatbot responses
"""

import asyncio
import time
from playwright.async_api import async_playwright
from pathlib import Path

CHATBOT_URL = "http://localhost:8502"
OUTPUT_DIR = "screenshots"
VOICEOVER_DURATION = 130  # 2:10 minutes

# Shorter demo with fewer queries
DEMO_QUERIES = [
    ("Show me all hospitals in California", 15),
    ("What are the hospital statistics?", 15),
    ("Which patients were treated by Dr. Sarah Johnson?", 15),
    ("What is the visit history for patient John Smith?", 15),
    ("Show me the most common diagnoses", 15),
    ("Show me patient reviews", 15),
]

async def capture_chatbot_screenshots():
    print("🎬 Starting chatbot screenshot capture (SHORTER VERSION)...")
    print(f"⏱️  Target duration: ~{VOICEOVER_DURATION}s")
    
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1
        )
        page = await context.new_page()
        
        try:
            print(f"📍 Loading chatbot at {CHATBOT_URL}...")
            await page.goto(CHATBOT_URL, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(5)  # Wait for full load
            
            screenshot_count = 0
            
            # Intro - show clean interface (20 seconds)
            print("\n📍 Scene 1: Introduction (20s)")
            for i in range(40):  # 40 screenshots at 2fps = 20s
                await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                screenshot_count += 1
                await asyncio.sleep(0.5)
            
            # Execute queries (90 seconds total = 6 queries × 15s each)
            print("\n📍 Executing queries...")
            
            for idx, (query, duration) in enumerate(DEMO_QUERIES, 1):
                print(f"   Query {idx}: {query}")
                
                # Find chat input
                try:
                    chat_input = await page.wait_for_selector('textarea[aria-label="Chat input"]', timeout=5000)
                except:
                    chat_input = await page.query_selector('textarea')
                
                if chat_input:
                    # Clear and type query
                    await chat_input.fill("")
                    await chat_input.type(query, delay=50)
                    
                    # Take screenshots during typing (3 seconds)
                    for i in range(6):
                        await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                        screenshot_count += 1
                        await asyncio.sleep(0.5)
                    
                    # Submit
                    await page.keyboard.press('Enter')
                    
                    # Wait for response to appear
                    await asyncio.sleep(3)
                    
                    # Capture response (remaining duration - 6s)
                    remaining_frames = int((duration - 6) * 2)  # 2 fps
                    for i in range(remaining_frames):
                        await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                        screenshot_count += 1
                        await asyncio.sleep(0.5)
                
                else:
                    print(f"   ⚠️  Could not find input, taking static screenshots")
                    for i in range(int(duration * 2)):
                        await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                        screenshot_count += 1
                        await asyncio.sleep(0.5)
            
            # Conclusion (20 seconds)
            print("\n📍 Scene 2: Conclusion (20s)")
            await page.mouse.wheel(0, -1000)  # Scroll up
            await asyncio.sleep(1)
            for i in range(40):
                await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                screenshot_count += 1
                await asyncio.sleep(0.5)
            
            print(f"\n✅ Captured {screenshot_count} screenshots")
            print(f"📁 Location: {OUTPUT_DIR}/")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await context.close()
            await browser.close()
    
    return screenshot_count

async def main():
    print("=" * 70)
    print("🎬 HOSPITAL CHATBOT - IMPROVED SCREENSHOT CAPTURE")
    print("=" * 70)
    print(f"\n⚙️  Target duration: ~{VOICEOVER_DURATION}s (~2 minutes)")
    print(f"   Queries: {len(DEMO_QUERIES)}")
    print("")
    
    screenshot_count = await capture_chatbot_screenshots()
    
    print("")
    print("=" * 70)
    print("✅ CAPTURE COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Total screenshots: {screenshot_count}")
    print(f"📁 Location: {OUTPUT_DIR}/")
    print("\n🎬 Next: Create video with ./scripts/create-video-from-screenshots.sh")
    print("")

if __name__ == "__main__":
    asyncio.run(main())
