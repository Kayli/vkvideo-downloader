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
