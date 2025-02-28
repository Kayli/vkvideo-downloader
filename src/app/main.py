import os
import sys
import yaml
import argparse
import logging
from typing import List, Dict, Optional, Union

from .browser import extract_video_links, extract_videos_from_urls

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# Constants
GOODSTUFF_VIDEOS = [
    "https://vkvideo.ru/@public111751633/all",
    "https://vkvideo.ru/@club180058315/all"
]
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

def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='VK Video Link Downloader',
        epilog='''
Examples:
  # Extract video links from predefined URLs
  %(prog)s goodstuff

  # Extract video links from predefined URLs and save to YAML
  %(prog)s goodstuff --list

  # Extract video links from a specific URL
  %(prog)s url https://vkvideo.ru/@public111751633/all
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Goodstuff command
    goodstuff_parser = subparsers.add_parser('goodstuff', help='Extract links from predefined URLs')
    goodstuff_parser.add_argument('--list', action='store_true', 
                                   help='Save extracted links to YAML file')
    
    # URL command
    url_parser = subparsers.add_parser('url', help='Extract links from specific URL')
    url_parser.add_argument('url', type=str, help='URL to extract video links from')
    
    return parser

def main() -> Optional[List[Dict[str, str]]]:
    """
    Main entry point for the VK Video Link Downloader.
    
    Returns:
        Optional[List[Dict[str, str]]]: List of extracted video links or None
    """
    # Create parser
    parser = create_parser()
    
    # If no arguments, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    # Parse arguments
    args = parser.parse_args()
    
    if args.command == 'goodstuff':
        videos = extract_videos_from_urls(GOODSTUFF_VIDEOS)
        
        if args.list:
            save_video_links_to_yaml(videos)
            return None
        
        return videos
    
    elif args.command == 'url':
        return extract_video_links(args.url)
    
    return None

if __name__ == '__main__':
    result = main()
    if result is not None:
        print(yaml.safe_dump(result, allow_unicode=True))
