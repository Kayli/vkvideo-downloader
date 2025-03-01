from dataclasses import dataclass

@dataclass
class Settings:
    """
    Centralized application settings with a focus on timeout configurations.
    
    Provides a single source of truth for various timeout and configuration settings.
    """
    
    # Browser and page loading timeouts in seconds
    page_load_timeout_sec: int = 60  
    scroll_timeout_sec: int = 10     
    
    # Browser configuration defaults
    headless: bool = True
