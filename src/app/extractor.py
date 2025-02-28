import os
import sys
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

# Import Logger class
from .logger import Logger
from .browser import Browser

class Extractor:
    """
    A class for extracting video links from web pages.
    
    Replaces the previous Browser class name with Extractor to better reflect its functionality.
    """
    def __init__(
        self, 
        headless: bool = True, 
        timeout: int = 30000, 
        logger: Optional[Logger] = None
    ):
        """
        Initialize Extractor with configuration options

        Args:
            headless (bool, optional): Whether to run browser in headless mode. Defaults to True.
            timeout (int, optional): Maximum time to wait for page load and video extraction. Defaults to 30000.
            logger (Optional[Logger], optional): Logger for recording browser events.
                Defaults to a new Logger instance.
        """
        self.headless = headless
        self.timeout = timeout
        self.logger = logger or Logger()
        self.browser = Browser(headless=headless, timeout=timeout)

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
            # Get full page HTML
            full_html = self.browser.get_page_html(url)
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(full_html, 'html.parser')
            
            # Find all video links
            video_links = []
            for link in soup.find_all('a', href=re.compile(r'^/video-')):
                href = link.get('href')
                title = link.get_text(strip=True) or 'Untitled Video'
                
                # Convert to full URL
                full_url = f'https://vkvideo.ru{href}'
                
                video_links.append({
                    'url': full_url,
                    'title': title
                })
            
            self.logger.info(f"Extracted {len(video_links)} unique video links")
            return video_links
        
        except TimeoutError as e:
            self.logger.error(f"Timeout error: {e}")
            raise
        
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
        
        Raises:
            Exception: If any URL fails to extract videos
        """
        all_videos = []
        for url in urls:
            self.logger.info(f"Processing URL: {url}")
            videos = self.extract_video_links(url)
            all_videos.extend(videos)
        
        return all_videos
