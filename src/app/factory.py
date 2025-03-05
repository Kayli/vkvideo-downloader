from typing import Optional, List

from .logger import Logger
from .extractor import Extractor

class CLIAppFactory:
    """
    Factory for creating CLIApp instances with real dependencies
    """
    @staticmethod
    def create_cli_app(
        extractor: Optional[Extractor] = None,
        logger: Optional[Logger] = None
    ):
        """
        Create a CLIApp instance with real dependencies

        Args:
            extractor (Optional[Extractor], optional): Extractor for extracting video links.
                Defaults to a new Extractor instance.
            logger (Optional[Logger], optional): Logger instance.
                Defaults to a new Logger with default settings.
        
        Returns:
            CLIApp: Configured CLIApp instance
        """
        from .main import CLIApp  # Import here to avoid circular dependency
        
        # Use provided logger or create a default one
        if logger is None:
            logger = Logger()
        elif not isinstance(logger, Logger):
            raise ValueError("Invalid logger instance")
        
        # Use provided extractor or create a default one with the logger
        extractor = extractor or Extractor(logger=logger)
        
        return CLIApp(extractor=extractor, logger=logger)
