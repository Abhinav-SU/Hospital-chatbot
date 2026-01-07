#!/usr/bin/env python3
"""
Hospital Chatbot - Real Demo Video Recorder
Captures actual chatbot interactions using Playwright screenshots
"""

import asyncio
import time
from playwright.async_api import async_playwright
from pathlib import Path

# Configuration
CHATBOT_URL = "http://localhost:8502"
VOICEOVER_DURATION = 175  # seconds
OUTPUT_DIR = "screenshots"
FPS = 2  # Screenshots per second (lower for smoother file size)

# Demo queries from the voiceover script
DEMO_QUERIES = [
    ("Show me all hospitals in California", 10),
    ("What are the hospital statistics?", 10),
    ("Which patients were treated by Dr. Sarah Johnson?", 10),
    ("What is the visit history for patient John Smith?", 10),
    ("Show me the most common diagnoses", 10),
    ("Which physicians have the highest salaries?", 10),
    ("Show me patient reviews", 10),
]

async def capture_chatbot_screenshots():
    """Capture screenshots of actual chatbot usage"""
    print("🎬 Starting chatbot screenshot capture...")
    print(f"📍 URL: {CHATBOT_URL}")
    print(f"⏱️  Target duration: {VOICEOVER_DURATION}s")
    print("")
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        # Launch browser in headless mode
        print("🌐 Launching browser...")
        browser = await p.chromium.launch(headless=True)
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1
        )
        
        page = await context.new_page()
        
        try:
            # Navigate to chatbot
            print(f"📍 Loading chatbot...")
            await page.goto(CHATBOT_URL, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(3)
            
            screenshot_count = 0
            start_time = time.time()
            
            # Scene 1: Introduction - Show initial interface (15 seconds)
            print("\n📍 Scene 1: Introduction (15s)")
            for i in range(int(15 * FPS)):
                await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                screenshot_count += 1
                await asyncio.sleep(1/FPS)
            
            # Scene 2: Interface overview (20 seconds)
            print("\n📍 Scene 2: Interface Overview (20s)")
            # Scroll sidebar
            try:
                sidebar = await page.query_selector('[data-testid="stSidebar"]')
                if sidebar:
                    await sidebar.scroll_into_view_if_needed()
            except:
                pass
            
            for i in range(int(20 * FPS)):
                await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                screenshot_count += 1
                await asyncio.sleep(1/FPS)
            
            # Scene 3-8: Execute queries with screenshots (120 seconds total)
            print("\n📍 Executing demo queries...")
            
            for idx, (query, duration) in enumerate(DEMO_QUERIES, 1):
                print(f"   Query {idx}: {query}")
                
                # Find and fill chat input
                chat_input = await page.query_selector('textarea[placeholder*="What"]')
                if chat_input:
                    # Clear input
                    await chat_input.fill("")
                    
                    # Type query slowly (capture typing)
                    for i in range(int(3 * FPS)):  # 3 seconds of typing
                        chars_to_type = int((i / (3 * FPS)) * len(query))
                        await chat_input.fill(query[:chars_to_type])
                        await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                        screenshot_count += 1
                        await asyncio.sleep(1/FPS)
                    
                    # Submit query
                    await chat_input.fill(query)
                    await page.keyboard.press('Enter')
                    await asyncio.sleep(2)  # Wait for submission
                    
                    # Capture response appearing (remaining duration)
                    remaining_duration = duration - 3
                    for i in range(int(remaining_duration * FPS)):
                        await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                        screenshot_count += 1
                        await asyncio.sleep(1/FPS)
                else:
                    print(f"   ⚠️  Could not find chat input, capturing static screens")
                    for i in range(int(duration * FPS)):
                        await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                        screenshot_count += 1
                        await asyncio.sleep(1/FPS)
            
            # Final conclusion scene
            print("\n📍 Scene 9: Conclusion (10s)")
            # Scroll through chat history
            try:
                await page.mouse.wheel(0, -500)
                await asyncio.sleep(1)
            except:
                pass
            
            for i in range(int(10 * FPS)):
                await page.screenshot(path=f"{OUTPUT_DIR}/frame_{screenshot_count:05d}.png")
                screenshot_count += 1
                await asyncio.sleep(1/FPS)
            
            elapsed = time.time() - start_time
            print(f"\n✅ Captured {screenshot_count} screenshots in {elapsed:.1f}s")
            print(f"📁 Screenshots saved to: {OUTPUT_DIR}/")
            
        except Exception as e:
            print(f"\n❌ Error during capture: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await context.close()
            await browser.close()
    
    return screenshot_count

async def main():
    """Main entry point"""
    print("=" * 70)
    print("🎬 HOSPITAL CHATBOT - REAL DEMO SCREENSHOT CAPTURE")
    print("=" * 70)
    print("")
    print("This will capture actual chatbot usage with real queries and responses.")
    print("")
    print("⚙️  Configuration:")
    print(f"   URL: {CHATBOT_URL}")
    print(f"   FPS: {FPS} screenshots/second")
    print(f"   Duration: ~{VOICEOVER_DURATION}s")
    print(f"   Queries: {len(DEMO_QUERIES)}")
    print("")
    
    screenshot_count = await capture_chatbot_screenshots()
    
    print("")
    print("=" * 70)
    print("✅ SCREENSHOT CAPTURE COMPLETE!")
    print("=" * 70)
    print("")
    print(f"📊 Total screenshots: {screenshot_count}")
    print(f"📁 Location: {OUTPUT_DIR}/")
    print("")
    print("🎬 Next: Create video from screenshots")
    print("")

if __name__ == "__main__":
    asyncio.run(main())
