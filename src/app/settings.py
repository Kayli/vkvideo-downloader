from dataclasses import dataclass
from pathlib import Path

@dataclass
class Settings:
    """
    Centralized application settings with a focus on timeout configurations.
    
    Provides a single source of truth for various timeout and configuration settings.
    """
    
    # Browser and page loading timeouts in seconds
    page_load_timeout_sec: int = 120  
    scroll_timeout_sec: int = 20     
    
    # Browser configuration defaults
    headless: bool = True
    
    # Cache directory for browser record/replay
    cache_dir: str = "recordings"