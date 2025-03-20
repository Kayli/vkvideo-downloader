from dataclasses import dataclass
from pathlib import Path
from typing import List
@dataclass
class Settings:
    """
    Centralized application settings with a focus on timeout configurations.
    
    Provides a single source of truth for various timeout and configuration settings.
    """
    
    # Browser and page loading timeouts in seconds
    timeout_browser_scroll_sec: int = 20
    timeout_browser_sec: int = 120
    
    # Browser configuration defaults
    headless: bool = True
    
    # Cache directory for browser record/replay
    cache_dir: str = "recordings"

    skiplist = [
        "https://vkvideo.ru/video-180058315_456239188"
    ]