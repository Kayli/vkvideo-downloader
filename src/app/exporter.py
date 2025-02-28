import os
import yaml
import logging
import sys
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Default output file path
OUTPUT_YAML_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'vkvideo_links.yml')

def save_video_links_to_yaml(
    video_links: List[Dict[str, str]], 
    output_file: str = OUTPUT_YAML_FILE
) -> None:
    """
    Save video links to a YAML file.
    
    Args:
        video_links (List[Dict[str, str]]): List of video links to save
        output_file (str): Path to output YAML file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(video_links, f, allow_unicode=True)
    
    logger.info(f"Saved {len(video_links)} video links to {output_file}")
