from playwright.sync_api import sync_playwright
import time
import re
import os

def extract_video_links(url, record_har=False, har_path=None):
    print(f"\nStarting extraction from URL: {url}")
    with sync_playwright() as p:
        # Launch browser with more options
        print("\n--- Launching browser ---")
        browser = p.chromium.launch(headless=False)
        
        # Create a new context with HAR recording if requested
        context_options = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        if record_har and har_path:
            context_options['record_har_path'] = har_path
            
        context = browser.new_context(**context_options)
        page = context.new_page()
        
        try:
            print(f"\n--- Navigating to URL ---")
            page.goto(url, timeout=60000, wait_until='networkidle')
            print("Page loaded successfully")
            
            # Wait for video elements to be present
            print("Waiting for video elements to load...")
            page.wait_for_selector('a[href^="/video-"]', timeout=10000)
            time.sleep(2)  # Give the page a moment to fully render
            
            # Extract video information using JavaScript
            videos = page.evaluate("""
                () => {
                    const videos = [];
                    const seen = new Set();
                    
                    // Find all video cards
                    document.querySelectorAll('[class*="VideoCard"]').forEach(card => {
                        // Find video link
                        const link = card.querySelector('a[href^="/video-"]');
                        if (!link) return;
                        
                        const href = link.getAttribute('href');
                        if (seen.has(href) || !href.match(/^\/video-\\d+_\\d+$/)) return;
                        seen.add(href);
                        
                        // Try multiple ways to find the title
                        let title = '';
                        
                        // Method 1: Look for title in VideoCard__title
                        const titleElem = card.querySelector('[class*="VideoCard__title"]');
                        if (titleElem) {
                            const text = titleElem.textContent.trim();
                            if (text && !text.match(/^\\d+:\\d+$/)) {
                                title = text;
                            }
                        }
                        
                        // Method 2: Look for description
                        if (!title) {
                            const descElem = card.querySelector('[class*="VideoCard__description"]');
                            if (descElem) {
                                const text = descElem.textContent.trim();
                                if (text && !text.match(/^\\d+:\\d+$/)) {
                                    title = text;
                                }
                            }
                        }
                        
                        // Method 3: Look for any text content that's not a timestamp
                        if (!title) {
                            const texts = Array.from(card.querySelectorAll('*'))
                                .map(el => el.textContent.trim())
                                .filter(text => text && !text.match(/^\\d+:\\d+$/));
                            
                            if (texts.length > 0) {
                                // Find the longest text that's not just a number
                                title = texts.reduce((a, b) => a.length > b.length ? a : b);
                            }
                        }
                        
                        videos.push({
                            url: 'https://vkvideo.ru' + href,
                            title: title || 'Untitled Video'
                        });
                    });
                    return videos;
                }
            """)
            
            print("\n=== Found Videos ===")
            for video in videos:
                print(f"\nTitle: {video['title']}")
                print(f"URL: {video['url']}")
                print("-" * 80)
                
            return videos
                
        finally:
            if record_har and har_path:
                context.close()  # This will save the HAR file
            print("\n--- Closing browser ---")
            browser.close()

if __name__ == "__main__":
    # Example usage
    url = "https://vkvideo.ru/@public111751633/all"
    videos = extract_video_links(url)
    print(f"\nTotal videos found: {len(videos)}")
