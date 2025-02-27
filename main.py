from playwright.sync_api import sync_playwright
import time
import re

def extract_video_links(url):
    print(f"\nStarting extraction from URL: {url}")
    with sync_playwright() as p:
        # Launch browser with more options
        print("\n--- Launching browser ---")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print(f"\n--- Navigating to URL ---")
            page.goto(url, timeout=60000, wait_until='networkidle')
            print("Page loaded successfully")
            
            # Wait for video elements to be present and add a small delay
            print("Waiting for video elements to load...")
            page.wait_for_selector('a[href^="/video-"]', timeout=10000)
            time.sleep(2)  # Give the page a moment to fully render
            
            # Extract video information using JavaScript
            videos = page.evaluate("""
                () => {
                    const videos = [];
                    // Find all links that start with /video-
                    const links = document.querySelectorAll('a[href^="/video-"]');
                    const seen = new Set();
                    
                    links.forEach(link => {
                        const href = link.getAttribute('href');
                        // Only process each video once
                        if (!seen.has(href) && href.match(/^\/video-\\d+_\\d+$/)) {
                            seen.add(href);
                            
                            // Try multiple ways to find the title
                            let title = '';
                            
                            // Method 1: Check parent div with video-card-title class
                            const parentCard = link.closest('[class*="video-card"]');
                            if (parentCard) {
                                const titleDiv = parentCard.querySelector('[class*="title"]');
                                if (titleDiv) {
                                    title = titleDiv.textContent.trim();
                                }
                            }
                            
                            // Method 2: Check for aria-label on the link itself
                            if (!title && link.getAttribute('aria-label')) {
                                title = link.getAttribute('aria-label');
                            }
                            
                            // Method 3: Look for a sibling or nearby div with title
                            if (!title) {
                                const siblings = link.parentElement.querySelectorAll('[class*="title"]');
                                for (const sibling of siblings) {
                                    const text = sibling.textContent.trim();
                                    if (text && !text.match(/^\\d+:\\d+$/)) {
                                        title = text;
                                        break;
                                    }
                                }
                            }
                            
                            // Method 4: Get parent text if it's not just a timestamp
                            if (!title) {
                                const parentText = link.parentElement.textContent.trim();
                                if (parentText && !parentText.match(/^\\d+:\\d+$/)) {
                                    title = parentText;
                                }
                            }
                            
                            // Debug: Log the HTML around this link
                            console.log('Link HTML:', link.parentElement.innerHTML);
                            
                            videos.push({
                                url: 'https://vkvideo.ru' + href,
                                title: title || 'Untitled Video'
                            });
                        }
                    });
                    return videos;
                }
            """)
            
            print("\n=== Found Videos ===")
            for video in videos:
                print(f"Title: {video['title']}")
                print(f"URL: {video['url']}\n")
                
            return videos
                
        finally:
            print("\n--- Closing browser ---")
            browser.close()

if __name__ == "__main__":
    # Example URL
    url = "https://vkvideo.ru/@public111751633/all"
    
    try:
        print(f"\n=== Starting VK video URL extraction ===")
        videos = extract_video_links(url)
        
        if not videos:
            print("No videos found!")
        
    except Exception as e:
        print(f"Error during extraction: {e}")
