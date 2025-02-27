import os
import sys
import yaml
import argparse
import logging
from typing import List, Dict, Optional, Union

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Constants
GOODSTUFF_VIDEOS = [
    "https://vkvideo.ru/@public111751633/all",
    "https://vkvideo.ru/@club180058315/all"
]
OUTPUT_YAML_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vkvideo_links.yml')

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

def save_video_links_to_yaml(
    video_links: List[Dict[str, str]], 
    output_file: str = OUTPUT_YAML_FILE
) -> None:
    """
    Save video links to a YAML file.
    
    Args:
        video_links (List[Dict[str, str]]): List of video links to save
        output_file (str): Path to output YAML file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(video_links, f, allow_unicode=True)
    
    logger.info(f"Saved {len(video_links)} video links to {output_file}")

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='VK Video Link Downloader')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Goodstuff command
    goodstuff_parser = subparsers.add_parser('goodstuff', help='Extract links from predefined URLs')
    goodstuff_parser.add_argument('--list', action='store_true', 
                                  help='Save extracted links to YAML file')
    
    # URL command
    url_parser = subparsers.add_parser('url', help='Extract links from specific URL')
    url_parser.add_argument('url', type=str, help='URL to extract video links from')
    
    return parser.parse_args()

def main() -> Optional[List[Dict[str, str]]]:
    """
    Main entry point for the VK Video Link Downloader.
    
    Returns:
        Optional[List[Dict[str, str]]]: List of extracted video links or None
    """
    args = parse_arguments()
    
    # Headless mode by default
    headless = True
    
    if args.command == 'goodstuff':
        if args.list:
            # Save to YAML file
            video_links = extract_videos_from_urls(GOODSTUFF_VIDEOS, headless=headless)
            save_video_links_to_yaml(video_links)
            return None
        else:
            # Return video links to stdout
            return extract_videos_from_urls(GOODSTUFF_VIDEOS, headless=headless)
    
    elif args.command == 'url':
        return extract_video_links(args.url, headless=headless)
    
    return None
