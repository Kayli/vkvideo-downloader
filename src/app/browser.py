import os
import hashlib
from typing import Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from .settings import Settings

class Browser:
    """
    A wrapper class for Playwright browser interactions with record/replay functionality.
    """
    
    def __init__(self, settings: Settings, record_replay: bool = False):
        """
        Initialize Browser with configuration from Settings.
        
        Args:
            settings (Settings): Application settings for browser configuration.
            record_replay (bool): If True, cache page HTML and use cached versions when available.
        """
        self.headless = settings.headless
        self.timeout = settings.timeout_browser_sec * 1000  # Convert seconds to milliseconds
        self.scroll_timeout = settings.timeout_browser_scroll_sec * 1000  # Convert seconds to milliseconds
        self.record_replay = record_replay
        self.cache_dir = settings.cache_dir
        
    
    def _get_cache_path(self, url: str) -> str:
        """Generate a cache file path based on the URL hash."""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.html")
    
    def get_page_html(self, url: str) -> str:
        """
        Retrieve full page HTML after scrolling, using cache if enabled.
        
        Args:
            url (str): URL of the web page to retrieve HTML from.
        
        Returns:
            str: Full page HTML content.
        
        Raises:
            TimeoutError: If page load or scrolling fails.
            Exception: For other unexpected errors during page retrieval.
        """
        cache_path = self._get_cache_path(url)
        
        # Make sure that cache directory exists when record_replay enabled
        if self.record_replay:
            os.makedirs(self.cache_dir, exist_ok=True)
        
        # Use cached HTML if available
        if self.record_replay and os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.goto(url, timeout=self.timeout, wait_until='load')
                
                # Scroll to the bottom to load all content
                page.evaluate("""
                    async () => {
                        await new Promise((resolve) => {
                            let totalHeight = 0;
                            const distance = 100;
                            const timer = setInterval(() => {
                                const scrollHeight = document.body.scrollHeight;
                                window.scrollBy(0, distance);
                                totalHeight += distance;
                                if (totalHeight >= scrollHeight) {
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, 100);
                        });
                    }
                """)
                
                page.wait_for_timeout(self.scroll_timeout)
                full_html = page.content()
                browser.close()
                
                # Cache HTML if recording is enabled
                if self.record_replay:
                    with open(cache_path, "w", encoding="utf-8") as f:
                        f.write(full_html)
                
                return full_html
        
        except PlaywrightTimeoutError as e:
            raise TimeoutError(f"Timeout while retrieving page HTML from {url}: {e}")
        
        except Exception as e:
            raise RuntimeError(f"Error retrieving page HTML: {e}")
