from typing import Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

class Browser:
    """
    A wrapper class for Playwright browser interactions.
    
    Provides a clean abstraction over Playwright's browser operations,
    focusing on retrieving page HTML with full content loading.
    """
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        """
        Initialize Browser with configuration options.
        
        Args:
            headless (bool, optional): Whether to run browser in headless mode. Defaults to True.
            timeout (int, optional): Maximum time to wait for page load and interactions. Defaults to 30000.
        """
        self.headless = headless
        self.timeout = timeout
    
    def get_page_html(self, url: str) -> str:
        """
        Retrieve full page HTML after scrolling to load all content.
        
        Args:
            url (str): URL of the web page to retrieve HTML from
        
        Returns:
            str: Full page HTML content after scrolling
        
        Raises:
            TimeoutError: If page load or scrolling fails
            Exception: For other unexpected errors during page retrieval
        """
        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=self.headless)
                
                # Create a new page and navigate
                page = browser.new_page()
                page.goto(url, timeout=self.timeout, wait_until='load')
                
                # Scroll to the bottom of the page to load all content
                page.evaluate("""
                    async () => {
                        await new Promise((resolve) => {
                            let totalHeight = 0;
                            const distance = 100;
                            const timer = setInterval(() => {
                                const scrollHeight = document.body.scrollHeight;
                                window.scrollBy(0, distance);
                                totalHeight += distance;

                                if(totalHeight >= scrollHeight){
                                    clearInterval(timer);
                                    resolve();
                                }
                            }, 100);
                        });
                    }
                """)
                
                # Wait a short time after scrolling to ensure all content is loaded
                page.wait_for_timeout(1000)
                
                # Get the full page HTML
                full_html = page.content()
                
                browser.close()
                
                return full_html
        
        except PlaywrightTimeoutError as e:
            raise TimeoutError(f"Timeout while retrieving page HTML from {url}: {e}")
        
        except Exception as e:
            raise RuntimeError(f"Error retrieving page HTML: {e}")
