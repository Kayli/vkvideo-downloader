from dataclasses import dataclass

@dataclass
class Settings:
    """
    Centralized application settings with a focus on timeout configurations.
    
    Provides a single source of truth for various timeout and configuration settings.
    """
    
    # Browser and page loading timeouts
    page_load_timeout: int = 30000  # 30 seconds
    scroll_timeout: int = 10000     # 10 seconds
    
    # Browser configuration defaults
    headless: bool = True
