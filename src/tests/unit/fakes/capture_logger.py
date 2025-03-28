import logging
import sys
from ....app.logger import Logger

class CaptureLogger(Logger):
    """
    A logger that captures log messages for testing purposes.
    """
    
    def __init__(self, name=None, level=logging.INFO):
        """
        Initialize a capture logger.
        
        Args:
            name (str, optional): Name of the logger. Defaults to None.
            level (int, optional): Logging level. Defaults to logging.INFO.
        """
        super().__init__(name, level)
        self.captured_logs = {
            'info': [],
            'error': []
        }
    
    def info(self, msg):
        """Capture info log messages."""
        self.captured_logs['info'].append(msg)
        super().info(msg)
        print(f'INFO: {msg}')  # Print to stdout
    
    def error(self, msg):
        """Capture error log messages."""
        self.captured_logs['error'].append(msg)
        super().error(msg)
        print(f'ERROR: {msg}', file=sys.stderr)  # Print to stderr
    
    def clear_logs(self):
        """Clear all captured logs."""
        self.captured_logs = {
            'info': [],
            'error': []
        }
