#!/usr/bin/env python3
"""
Hospital Chatbot - Automated Demo Video Recorder
Uses Playwright to automate browser interactions and record demo video
"""

import asyncio
import time
from playwright.async_api import async_playwright

# Demo configuration
CHATBOT_URL = "http://localhost:8502"
VOICEOVER_DURATION = 175  # seconds (from ffprobe)
OUTPUT_VIDEO = "Hospital-Chatbot-Demo-Raw.webm"

# Scene timings (total = 175 seconds)
SCENES = [
    {
        "name": "Introduction",
        "duration": 15,
        "actions": ["wait_for_page_load", "show_sidebar", "show_main_area"]
    },
    {
        "name": "Interface Overview",
        "duration": 20,
        "actions": ["scroll_sidebar", "highlight_examples", "show_input"]
    },
    {
        "name": "Hospital Queries",
        "duration": 40,
        "queries": [
            "Show me all hospitals in California",
            "What are the hospital statistics?"
        ]
    },
    {
        "name": "Patient Data",
        "duration": 35,
        "queries": [
            "Which patients were treated by Dr. Sarah Johnson?",
            "What is the visit history for patient John Smith?"
        ]
    },
    {
        "name": "Medical Insights",
        "duration": 30,
        "queries": [
            "Show me the most common diagnoses",
            "Which physicians have the highest salaries?"
        ]
    },
    {
        "name": "Reviews",
        "duration": 25,
        "queries": [
            "Show me patient reviews"
        ]
    },
    {
        "name": "Conclusion",
        "duration": 10,
        "actions": ["scroll_chat_history", "show_sidebar_final"]
    }
]

async def type_slowly(page, selector, text, delay=0.1):
    """Type text slowly for natural appearance"""
    await page.fill(selector, "")
    for char in text:
        await page.type(selector, char, delay=delay * 1000)
    await asyncio.sleep(0.5)

async def wait_for_response(page, timeout=10):
    """Wait for chatbot response to appear"""
    try:
        # Wait for the response to finish loading
        await asyncio.sleep(3)  # Give chatbot time to process
        return True
    except Exception as e:
        print(f"Warning: Response timeout - {e}")
        return False

async def record_demo():
    """Record automated demo video with Playwright"""
    print("🎬 Starting automated demo recording...")
    print(f"🎯 Target duration: {VOICEOVER_DURATION} seconds")
    print(f"📹 Output: {OUTPUT_VIDEO}")
    print("")
    
    async with async_playwright() as p:
        # Launch browser with video recording
        print("🌐 Launching browser...")
        browser = await p.chromium.launch(
            headless=False,  # Show browser
            args=[
                '--start-maximized',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            record_video_dir=".",
            record_video_size={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        try:
            print(f"📍 Navigating to {CHATBOT_URL}...")
            await page.goto(CHATBOT_URL, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(3)
            
            start_time = time.time()
            
            # Scene 1: Introduction (15s)
            print("\n📍 Scene 1: Introduction (15s)")
            await asyncio.sleep(5)
            await page.mouse.move(200, 300, steps=30)  # Show sidebar
            await asyncio.sleep(5)
            await page.mouse.move(600, 400, steps=30)  # Show main area
            await asyncio.sleep(5)
            
            # Scene 2: Interface Overview (20s)
            print("\n📍 Scene 2: Interface Overview (20s)")
            # Scroll sidebar to show examples
            sidebar = await page.query_selector('[data-testid="stSidebar"]')
            if sidebar:
                await sidebar.scroll_into_view_if_needed()
                await asyncio.sleep(3)
            
            # Highlight chat input
            chat_input = await page.query_selector('textarea[placeholder*="What"]')
            if chat_input:
                await chat_input.scroll_into_view_if_needed()
                await asyncio.sleep(2)
                # Click to focus
                await chat_input.click()
                await asyncio.sleep(3)
            
            await asyncio.sleep(12)
            
            # Scene 3: Hospital Queries (40s)
            print("\n📍 Scene 3: Hospital Queries (40s)")
            
            # Query 1: California hospitals
            query1 = "Show me all hospitals in California"
            print(f"   Typing: {query1}")
            if chat_input:
                await type_slowly(page, 'textarea[placeholder*="What"]', query1, delay=0.08)
                await page.keyboard.press('Enter')
                await wait_for_response(page, timeout=8)
                await asyncio.sleep(5)
            
            # Query 2: Hospital statistics
            query2 = "What are the hospital statistics?"
            print(f"   Typing: {query2}")
            chat_input = await page.query_selector('textarea[placeholder*="What"]')
            if chat_input:
                await type_slowly(page, 'textarea[placeholder*="What"]', query2, delay=0.08)
                await page.keyboard.press('Enter')
                await wait_for_response(page, timeout=8)
                await asyncio.sleep(8)
            
            # Scene 4: Patient Data (35s)
            print("\n📍 Scene 4: Patient Data (35s)")
            
            # Query 3: Patients by physician
            query3 = "Which patients were treated by Dr. Sarah Johnson?"
            print(f"   Typing: {query3}")
            chat_input = await page.query_selector('textarea[placeholder*="What"]')
            if chat_input:
                await type_slowly(page, 'textarea[placeholder*="What"]', query3, delay=0.08)
                await page.keyboard.press('Enter')
                await wait_for_response(page, timeout=8)
                await asyncio.sleep(5)
            
            # Query 4: Patient visit history
            query4 = "What is the visit history for patient John Smith?"
            print(f"   Typing: {query4}")
            chat_input = await page.query_selector('textarea[placeholder*="What"]')
            if chat_input:
                await type_slowly(page, 'textarea[placeholder*="What"]', query4, delay=0.08)
                await page.keyboard.press('Enter')
                await wait_for_response(page, timeout=8)
                await asyncio.sleep(7)
            
            # Scene 5: Medical Insights (30s)
            print("\n📍 Scene 5: Medical Insights (30s)")
            
            # Query 5: Common diagnoses
            query5 = "Show me the most common diagnoses"
            print(f"   Typing: {query5}")
            chat_input = await page.query_selector('textarea[placeholder*="What"]')
            if chat_input:
                await type_slowly(page, 'textarea[placeholder*="What"]', query5, delay=0.08)
                await page.keyboard.press('Enter')
                await wait_for_response(page, timeout=8)
                await asyncio.sleep(5)
            
            # Query 6: Physician salaries
            query6 = "Which physicians have the highest salaries?"
            print(f"   Typing: {query6}")
            chat_input = await page.query_selector('textarea[placeholder*="What"]')
            if chat_input:
                await type_slowly(page, 'textarea[placeholder*="What"]', query6, delay=0.08)
                await page.keyboard.press('Enter')
                await wait_for_response(page, timeout=8)
                await asyncio.sleep(7)
            
            # Scene 6: Reviews (25s)
            print("\n📍 Scene 6: Reviews (25s)")
            
            # Query 7: Patient reviews
            query7 = "Show me patient reviews"
            print(f"   Typing: {query7}")
            chat_input = await page.query_selector('textarea[placeholder*="What"]')
            if chat_input:
                await type_slowly(page, 'textarea[placeholder*="What"]', query7, delay=0.08)
                await page.keyboard.press('Enter')
                await wait_for_response(page, timeout=8)
                await asyncio.sleep(12)
            
            # Scene 7: Conclusion (10s)
            print("\n📍 Scene 7: Conclusion (10s)")
            # Scroll through chat history
            await page.mouse.wheel(0, -500)
            await asyncio.sleep(3)
            
            # Show sidebar again
            sidebar = await page.query_selector('[data-testid="stSidebar"]')
            if sidebar:
                await sidebar.scroll_into_view_if_needed()
            await asyncio.sleep(4)
            
            # Scroll back to bottom
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(3)
            
            elapsed = time.time() - start_time
            print(f"\n⏱️  Total recording time: {elapsed:.1f} seconds")
            print(f"🎯 Target time: {VOICEOVER_DURATION} seconds")
            
            if elapsed < VOICEOVER_DURATION:
                # Add freeze frame at end to match voiceover
                freeze_time = VOICEOVER_DURATION - elapsed
                print(f"➕ Adding {freeze_time:.1f}s freeze frame to match voiceover...")
                await asyncio.sleep(freeze_time)
            
            print("\n✅ Demo recording completed!")
            
        except Exception as e:
            print(f"\n❌ Error during recording: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Close browser and save video
            print("\n💾 Saving video...")
            await context.close()
            await browser.close()
            
            # Get the recorded video path
            print("\n📹 Video saved!")
            print(f"📁 Check the current directory for the video file")
            print(f"   (Playwright saves it automatically)")

async def main():
    """Main entry point"""
    print("=" * 60)
    print("🎬 HOSPITAL CHATBOT - AUTOMATED DEMO RECORDER")
    print("=" * 60)
    print("")
    print("⚙️  Configuration:")
    print(f"   Chatbot URL: {CHATBOT_URL}")
    print(f"   Voiceover duration: {VOICEOVER_DURATION}s")
    print(f"   Video resolution: 1920x1080")
    print(f"   Output format: WebM")
    print("")
    print("📝 Make sure:")
    print("   1. Chatbot is running on port 8502")
    print("   2. Neo4j database is connected")
    print("   3. All demo queries are working")
    print("")
    input("Press Enter to start recording... ")
    print("")
    
    await record_demo()
    
    print("")
    print("=" * 60)
    print("✅ RECORDING COMPLETE!")
    print("=" * 60)
    print("")
    print("🎬 Next steps:")
    print("   1. Find the recorded video file in current directory")
    print("   2. Rename it to: Hospital-Chatbot-Demo-Raw.mp4")
    print("   3. Run: ./scripts/combine-video-audio.sh")
    print("")

if __name__ == "__main__":
    asyncio.run(main())
