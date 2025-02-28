import os
import sys
import logging
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Import Logger class
from .logger import Logger, configure_logging

class Browser:
    """
    A class for extracting video links from VK video pages
    """
    def __init__(
        self, 
        headless: bool = True, 
        timeout: int = 30000, 
        logger: Optional[Logger] = None
    ):
        """
        Initialize Browser with configuration options

        Args:
            headless (bool, optional): Whether to run browser in headless mode. Defaults to True.
            timeout (int, optional): Maximum time to wait for page load and video extraction. Defaults to 30000.
            logger (Optional[Logger], optional): Logger for recording browser events.
                Defaults to a new Logger instance.
        """
        self.headless = headless
        self.timeout = timeout
        self.logger = logger or Logger()

    def extract_video_links(self, url: str) -> List[Dict[str, str]]:
        """
        Extract video links from a given VK video page.
        
        Args:
            url (str): URL of the VK video page
        
        Returns:
            List[Dict[str, str]]: List of video links with their titles
        
        Raises:
            TimeoutError: If page load or video extraction times out
            Exception: For other unexpected errors during extraction
        """
        self.logger.info("Launching browser")
        
        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=self.headless)
                
                # Create a new page and navigate
                self.logger.info("Navigating to URL")
                page = browser.new_page()
                page.goto(url, timeout=self.timeout, wait_until='load')
                self.logger.info("Page loaded successfully")
                
                # Wait for video elements to load
                self.logger.info("Waiting for video elements to load")
                page.wait_for_selector('a[href^="/video-"]', timeout=self.timeout)
                
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
                
                self.logger.info(f"Extracted {len(processed_videos)} unique video links")
                return processed_videos
        
        except PlaywrightTimeoutError as e:
            self.logger.error(f"Timeout error: {e}")
            raise TimeoutError(f"Timeout while extracting videos from {url}: {e}")
        
        except Exception as e:
            self.logger.error(f"Error extracting video links: {e}")
            raise

    def extract_videos_from_urls(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Extract video links from multiple URLs.
        
        Args:
            urls (List[str]): List of URLs to extract videos from
        
        Returns:
            List[Dict[str, str]]: Consolidated list of video links
        """
        all_videos = []
        for url in urls:
            try:
                self.logger.info(f"Processing URL: {url}")
                videos = self.extract_video_links(url)
                all_videos.extend(videos)
            except Exception as e:
                self.logger.error(f"Failed to extract videos from {url}: {e}")
        
        return all_videos
