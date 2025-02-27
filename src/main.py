import argparse
import re
import os
import sys
from typing import List, Union
from playwright.sync_api import sync_playwright, expect

# Predefined list of "good stuff" video URLs
GOODSTUFF_VIDEOS = [
    "https://vkvideo.ru/@club180058315/all",
    "https://vkvideo.ru/@public111751633/all",
    # Add more interesting video URLs here
]

def extract_video_links(url, headless=True):
    """
    Extract video links from a VK page.

    Args:
        url (str): The VK page URL to extract video links from.
        headless (bool, optional): Run browser in headless mode. Defaults to True.

    Returns:
        list: A list of video link hrefs from the page.

    Raises:
        Exception: If there are issues navigating or extracting video links.
    """
    print(f"\nStarting extraction from URL: {url}")
    with sync_playwright() as p:
        # Launch browser with more options
        print("\n--- Launching browser ---")
        browser = p.chromium.launch(headless=headless)
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        try:
            print(f"\n--- Navigating to URL ---")
            page.goto(url, timeout=60000, wait_until='networkidle')
            print("Page loaded successfully")
            
            # Wait for video elements to be present and visible
            print("Waiting for video elements to load...")
            # Wait for at least one video link to be present
            page.wait_for_selector('a[href^="/video-"]', state='visible', timeout=10000)
            # Wait for video cards to be fully loaded
            page.wait_for_selector('[class*="VideoCard"]', state='visible', timeout=10000)
            
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
                            title = text;
                        }
                        
                        videos.push({
                            'href': href,
                            'title': title
                        });
                    });
                    
                    return videos;
                }
            """)
            
            # Close browser
            browser.close()
            
            # Extract just the href links
            video_links = [video['href'] for video in videos]
            
            print(f"\nExtracted {len(video_links)} unique video links")
            return video_links
        
        except Exception as e:
            browser.close()
            print(f"Error extracting video links: {e}")
            raise

def validate_vk_url(url: str) -> str:
    """
    Validate and normalize VK video URL.
    
    Args:
        url (str): Input URL to validate
    
    Returns:
        str: Validated and normalized URL
    
    Raises:
        argparse.ArgumentTypeError: If URL is invalid
    """
    # Basic VK URL validation
    vk_url_pattern = re.compile(r'^https?://(www\.)?vk\.com/(video|.*@.*)')
    
    if not vk_url_pattern.match(url):
        raise argparse.ArgumentTypeError(f"Invalid VK URL: {url}")
    
    return url

def main():
    parser = argparse.ArgumentParser(description='VK Video Downloader: Extract video links from VK pages')
    
    # Create a mutually exclusive group for URL input
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument('url', nargs='?', type=validate_vk_url, 
                            help='VK page URL to extract video links from')
    url_group.add_argument('goodstuff', nargs='?', choices=['goodstuff'], 
                            help='Use predefined list of interesting video URLs')
    
    parser.add_argument('--noheadless', action='store_true', 
                        help='Disable headless mode (default: headless)')
    parser.add_argument('--list', action='store_true', 
                        help='Print video links to stdout')
    
    args = parser.parse_args()
    
    try:
        # Determine which URLs to use
        if args.goodstuff:
            urls = GOODSTUFF_VIDEOS
        else:
            urls = [args.url]
        
        # Collect videos from all URLs
        all_videos = []
        for url in urls:
            print(f"\nProcessing URL: {url}", file=sys.stderr)
            videos = extract_video_links(url, headless=not args.noheadless)
            all_videos.extend(videos)
        
        # Print video links based on --list option
        if args.list:
            for video in all_videos:
                print(video)
        else:
            print(f"\nExtracted {len(all_videos)} video links", file=sys.stderr)
        
        return all_videos
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
