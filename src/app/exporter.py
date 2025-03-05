import os
import yaml
import logging
from typing import List, Dict

# Import logging configuration
from .logger import Logger
logger = Logger()

# Default output file path
DEFAULT_OUTPUT_YAML_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vkvideo_links.yml')

class VideoLinkExporter:
    """
    A class to handle exporting video links to YAML files
    """
    def __init__(self, 
                 output_file: str = DEFAULT_OUTPUT_YAML_FILE, 
                 logger: logging.Logger = logger):
        """
        Initialize the VideoLinkExporter

        Args:
            output_file (str, optional): Path to output YAML file. 
                Defaults to DEFAULT_OUTPUT_YAML_FILE.
            logger (logging.Logger, optional): Logger instance. 
                Defaults to the module-level logger.
        """
        self.output_file = output_file
        self.logger = logger

    def save_to_yaml(self, video_links: List[Dict[str, str]]) -> None:
        """
        Save video links to a YAML file.
        
        Args:
            video_links (List[Dict[str, str]]): List of video links to save
        """
        with open(self.output_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(video_links, f, allow_unicode=True)
        
        self.logger.info(f"Saved {len(video_links)} video links to {self.output_file}")
