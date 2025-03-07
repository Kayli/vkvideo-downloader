from typing import Optional, List

from .logger import Logger
from .extractor import Extractor
from .downloader import Downloader
from .settings import Settings

def create_cli_app(
    extractor: Optional[Extractor] = None,
    downloader: Optional[Downloader] = None,
    logger: Optional[Logger] = None,
    settings: Optional[Settings] = None
):
    """
    Create a CLIApp instance with real dependencies

    Args:
        extractor (Optional[Extractor], optional): Extractor for extracting video links.
            Defaults to a new Extractor instance.
        downloader (Optional[Downloader], optional): Downloader for downloading videos.
            Defaults to a new Downloader instance.
        logger (Optional[Logger], optional): Logger instance.
            Defaults to a new Logger with default settings.
        settings (Optional[Settings], optional): Application settings.
            Defaults to a new Settings instance.
    
    Returns:
        CLIApp: Configured CLIApp instance
    """
    from .cli_app import CLIApp  # Import here to avoid circular dependency
    
    # Use provided logger or create a default one
    logger = logger or Logger()
    
    # Use provided extractor or create a default one with the logger
    extractor = extractor or Extractor(logger=logger)
    
    # Use provided downloader or create a default one with the logger
    downloader = downloader or Downloader(logger=logger)
    
    # Use provided settings or create a default one
    settings = settings or Settings()
    
    return CLIApp(
        extractor=extractor, 
        downloader=downloader, 
        logger=logger, 
        settings=settings
    )

# Export the function at module level
__all__ = ['create_cli_app']

class CLIAppFactory:
    """
    Factory for creating CLIApp instances with real dependencies
    """
    @staticmethod
    def create_cli_app(*args, **kwargs):
        """
        Wrapper method for create_cli_app function
        """
        return create_cli_app(*args, **kwargs)
