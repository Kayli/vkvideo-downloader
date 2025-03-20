import os
import sys
import logging
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import re
import yaml

# Import Logger class
from .logger import Logger
from .browser import Browser
from .settings import Settings

class VideoDTO:
    def __init__(self, url: str, title: str):
        self.url = url
        self.title = title

    def __repr__(self):
        return f"VideoDTO(url={self.url}, title={self.title})"

    def __eq__(self, other):
        if not isinstance(other, VideoDTO):
            return NotImplemented
        return self.url == other.url and self.title == other.title


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
        self.cache_dir = os.path.expanduser('~/.cache/vkvideo')
        os.makedirs(self.cache_dir, exist_ok=True)


    def extract_video_links_cached(self, url: str) -> List[VideoDTO]:
        """
        Extract video links from a given VK video page, using cached links if available.
        
        Args:
            url (str): URL of the VK video page
        
        Returns:
            List[VideoDTO]: List of VideoDTOs containing video URLs and titles
        
        Raises:
            TimeoutError: If page load or video extraction times out
            Exception: For other unexpected errors during extraction
        """
        # Create cache filename based on URL hash
        import hashlib
        cache_filename = os.path.join(self.cache_dir, hashlib.md5(url.encode()).hexdigest() + '.yaml')
        
        # Check if cache file exists
        if os.path.exists(cache_filename):
            self.logger.info(f"Using cached links for {url}")
            with open(cache_filename, 'r') as f:
                cached_videos = yaml.safe_load(f)
            
            # Convert cached data to VideoDTO
            video_links = [VideoDTO(video['url'], video['title']) for video in cached_videos]
            self.logger.info(f"Found {len(video_links)} videos in cache")
            return video_links
        
        self.logger.info(f"No cache found for {url}. Extracting video links using browser.")
        video_links = self.extract_video_links(url)
        
        # Cache the extracted links
        if video_links:
            cached_data = [{'url': video.url, 'title': video.title} for video in video_links]
            with open(cache_filename, 'w') as f:
                yaml.safe_dump(cached_data, f)
            self.logger.info(f"Cached {len(video_links)} video links for {url}")
        else:
            self.logger.warning(f"No videos found to cache for {url}")
        
        return video_links


    def extract_video_links(self, url: str) -> List[VideoDTO]:
        """
        Extract video links from a given VK video page.
        
        Args:
            url (str): URL of the VK video page
        
        Returns:
            List[VideoDTO]: List of VideoDTOs containing video URLs and titles
        
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
            extracted_videos = []
            for link in soup.find_all('a', href=re.compile(r'^/video-')):
                href = link.get('href')
                title = link.get_text(strip=True) or 'Untitled Video'
                
                # Check if the title is a timestamp
                if is_timestamp(title):
                    self.logger.warning(f"Detected timestamp instead of title: {title}")
                    continue  # Skip this link if it's a timestamp
                
                # Convert to full URL
                full_url = f'https://vkvideo.ru{href}'
                
                extracted_videos.append({'url': full_url, 'title': title})
            
            for video in extracted_videos:
                url = video['url']
                title = video['title']
                video_links.append(VideoDTO(url, title))
            
            self.logger.info(f"Extracted {len(video_links)} unique video links")

            # Cache the extracted links
            # Create cache filename based on URL hash
            import hashlib
            cache_filename = os.path.join(self.cache_dir, hashlib.md5(url.encode()).hexdigest() + '.yaml')

            if os.path.exists(cache_filename):
                # remove cache file if old cache exists
                os.remove(cache_filename)

            if video_links:
                cached_data = [{'url': video.url, 'title': video.title} for video in video_links]
                with open(cache_filename, 'w') as f:
                    yaml.safe_dump(cached_data, f)
                self.logger.info(f"Cached {len(video_links)} video links for {url}")
            else:
                self.logger.warning(f"No videos found to cache for {url}")
            
            return video_links
        
        except TimeoutError as e:
            self.logger.error(f"Timeout error: {e}")
            raise
        
        except Exception as e:
            self.logger.error(f"Error extracting video links: {e}")
            raise


    def extract_videos_from_urls_cached(self, urls: List[str]) -> List[VideoDTO]:
        """
        Extract video links from multiple URLs using cached extraction method.
        
        Args:
            urls (List[str]): List of URLs to extract videos from
        
        Returns:
            List[VideoDTO]: Consolidated list of video links
        
        Raises:
            Exception: If any URL fails to extract videos
        """
        all_videos = []
        for url in urls:
            self.logger.info(f"Processing URL: {url}")
            videos = self.extract_video_links_cached(url)
            all_videos.extend(videos)
        
        # Log number of extracted videos
        self.logger.info(f"Extracted {len(all_videos)} unique video links")
        
        return all_videos


    def extract_videos_from_urls(self, urls: List[str]) -> List[VideoDTO]:
        """
        Extract video links from multiple URLs using cached extraction method.
        
        Args:
            urls (List[str]): List of URLs to extract videos from
        
        Returns:
            List[VideoDTO]: Consolidated list of video links
        
        Raises:
            Exception: If any URL fails to extract videos
        """
        all_videos = []
        for url in urls:
            self.logger.info(f"Processing URL: {url}")
            videos = self.extract_video_links(url)
            all_videos.extend(videos)
        
        # Log number of extracted videos
        self.logger.info(f"Extracted {len(all_videos)} unique video links")
        
        return all_videos



def is_timestamp(title):
    # Simple regex to check if the title matches a timestamp format
    import re
    timestamp_pattern = re.compile(r'^(\d{1,2}:\d{2}:\d{2}|\d{1,2}:\d{2})$')
    return bool(timestamp_pattern.match(title))
