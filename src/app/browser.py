import os
import sys
import logging
from typing import List, Dict
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Import logging configuration
from .logger import configure_logging
logger = configure_logging()

def extract_video_links(
    url: str, 
    headless: bool = True, 
    timeout: int = 30000
) -> List[Dict[str, str]]:
    """
    Extract video links from a given VK video page.
    
    Args:
        url (str): URL of the VK video page
        headless (bool): Whether to run browser in headless mode
        timeout (int): Maximum time to wait for page load and video extraction
    
    Returns:
        List[Dict[str, str]]: List of video links with their titles
    
    Raises:
        TimeoutError: If page load or video extraction times out
        Exception: For other unexpected errors during extraction
    """
    logger.info("Launching browser")
    
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=headless)
            
            # Create a new page and navigate
            logger.info("Navigating to URL")
            page = browser.new_page()
            page.goto(url, timeout=timeout, wait_until='load')
            logger.info("Page loaded successfully")
            
            # Wait for video elements to load
            logger.info("Waiting for video elements to load")
            page.wait_for_selector('a[href^="/video-"]', timeout=timeout)
            
            # Extract video links
            video_links = page.evaluate("""
                () => {
                    const videos = document.querySelectorAll('a[href^="/video-"]');
                    return Array.from(videos).map(video => ({
                        href: video.getAttribute('href'),
                        title: video.textContent?.trim() || 'Untitled Video'
                    }));
                }
            """)
            
            # Convert to full URLs and add titles
            processed_videos = [
                {
                    'url': f'https://vkvideo.ru{video["href"]}',
                    'title': video['title']
                } for video in video_links
            ]
            
            browser.close()
            
            logger.info(f"Extracted {len(processed_videos)} unique video links")
            return processed_videos
    
    except PlaywrightTimeoutError as e:
        logger.error(f"Timeout error: {e}")
        raise TimeoutError(f"Timeout while extracting videos from {url}: {e}")
    
    except Exception as e:
        logger.error(f"Error extracting video links: {e}")
        raise

def extract_videos_from_urls(
    urls: List[str], 
    headless: bool = True
) -> List[Dict[str, str]]:
    """
    Extract video links from multiple URLs.
    
    Args:
        urls (List[str]): List of URLs to extract videos from
        headless (bool): Whether to run browser in headless mode
    
    Returns:
        List[Dict[str, str]]: Consolidated list of video links
    """
    all_videos = []
    for url in urls:
        try:
            logger.info(f"Processing URL: {url}")
            videos = extract_video_links(url, headless=headless)
            all_videos.extend(videos)
        except Exception as e:
            logger.error(f"Failed to extract videos from {url}: {e}")
    
    return all_videos
