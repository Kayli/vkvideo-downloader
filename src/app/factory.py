from typing import Optional, List

from .exporter import VideoLinkExporter
from .logger import Logger

class CLIAppFactory:
    """
    Factory for creating CLIApp instances with real dependencies
    """
    @staticmethod
    def create_cli_app(
        exporter: Optional[VideoLinkExporter] = None,
        logger: Optional[Logger] = None
    ):
        """
        Create a CLIApp instance with real dependencies

        Args:
            exporter (Optional[VideoLinkExporter], optional): Video link exporter.
                Defaults to a new VideoLinkExporter with default settings.
            logger (Optional[Logger], optional): Logger instance.
                Defaults to a new Logger with default settings.
        
        Returns:
            CLIApp: Configured CLIApp instance
        """
        from .main import CLIApp  # Import here to avoid circular dependency
        
        # Use provided exporter or create a default one
        exporter = exporter or VideoLinkExporter()
        
        # Use provided logger or create a default one
        logger = logger or Logger()
        
        return CLIApp(exporter=exporter, logger=logger)
