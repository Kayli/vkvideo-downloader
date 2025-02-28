import logging
import sys

def configure_logging(level=logging.INFO):
    """
    Configure logging with a standard format and output to stderr.
    
    Args:
        level (int, optional): Logging level. Defaults to logging.INFO.
    
    Returns:
        logging.Logger: Configured root logger
    """
    logging.basicConfig(
        level=level, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )
    return logging.getLogger(__name__)

class Logger:
    """
    A simple wrapper for Python's logging module with info and error methods.
    """
    
    def __init__(self, name=None):
        """
        Initialize a logger with an optional name.
        
        Args:
            name (str, optional): Name of the logger. Defaults to None.
        """
        self._logger = logging.getLogger(name or __name__)
    
    def info(self, msg):
        """Log an info message."""
        self._logger.info(msg)
    
    def error(self, msg):
        """Log an error message."""
        self._logger.error(msg)
