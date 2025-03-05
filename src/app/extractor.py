import os
import sys
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re

# Import Logger class
from .logger import Logger
from .browser import Browser
from .settings import Settings

class Extractor:
    """
    A class for extracting video links from web pages.
    
    Replaces the previous Browser class name with Extractor to better reflect its functionality.
    """
    def __init__(
        self, 
        settings: Optional[Settings] = None,
        logger: Optional[Logger] = None,
        browser: Optional[Browser] = None
    ):
        """
        Initialize Extractor with configuration options

        Args:
            settings (Optional[Settings], optional): Application settings. Defaults to a new Settings instance.
            logger (Optional[Logger], optional): Logger for recording browser events.
                Defaults to a new Logger instance.
            browser (Optional[Browser], optional): Browser instance to use for HTML retrieval.
                If not provided, a new Browser will be created with default settings.
        """
        self.settings = settings or Settings()
        self.logger = logger or Logger()
        self.browser = browser or Browser(self.settings)

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
                
                # Check if the title is a timestamp
                if is_timestamp(title):
                    self.logger.warning(f"Detected timestamp instead of title: {title}")
                    continue  # Skip this link if it's a timestamp
                
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


def is_timestamp(title):
    # Simple regex to check if the title matches a timestamp format
    import re
    timestamp_pattern = re.compile(r'^(\d{1,2}:\d{2}:\d{2}|\d{1,2}:\d{2})$')
    return bool(timestamp_pattern.match(title))
