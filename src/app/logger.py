import logging
import sys

class Logger:
    """
    A simple wrapper for Python's logging module with info and error methods.
    Configures logging on initialization.
    """
    
    def __init__(self, name=None, level=logging.INFO):
        """
        Initialize a logger with an optional name and logging configuration.
        
        Args:
            name (str, optional): Name of the logger. Defaults to None.
            level (int, optional): Logging level. Defaults to logging.INFO.
        """
        # Configure logging if not already configured
        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=level, 
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.StreamHandler(sys.stderr)
                ]
            )
        
        # Get or create logger
        self._logger = logging.getLogger(name or __name__)
    
    def info(self, msg):
        """Log an info message."""
        self._logger.info(msg)
    
    def error(self, msg):
        """Log an error message."""
        self._logger.error(msg)
