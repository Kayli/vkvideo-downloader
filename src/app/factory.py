from typing import Optional, List

from .exporter import VideoLinkExporter
from .logger import Logger
from .browser import Browser

class CLIAppFactory:
    """
    Factory for creating CLIApp instances with real dependencies
    """
    @staticmethod
    def create_cli_app(
        exporter: Optional[VideoLinkExporter] = None,
        browser: Optional[Browser] = None,
        logger: Optional[Logger] = None
    ):
        """
        Create a CLIApp instance with real dependencies

        Args:
            exporter (Optional[VideoLinkExporter], optional): Video link exporter.
                Defaults to a new VideoLinkExporter with default settings.
            browser (Optional[Browser], optional): Browser for extracting video links.
                Defaults to a new Browser instance.
            logger (Optional[Logger], optional): Logger instance.
                Defaults to a new Logger with default settings.
        
        Returns:
            CLIApp: Configured CLIApp instance
        """
        from .main import CLIApp  # Import here to avoid circular dependency
        
        # Use provided logger or create a default one
        logger = logger or Logger()
        
        # Use provided exporter or create a default one
        exporter = exporter or VideoLinkExporter()
        
        # Use provided browser or create a default one with the logger
        browser = browser or Browser(logger=logger)
        
        return CLIApp(exporter=exporter, browser=browser, logger=logger)
