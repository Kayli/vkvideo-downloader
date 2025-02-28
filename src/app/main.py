import os
import sys
import yaml
import argparse
from typing import List, Dict, Optional, Union

# Import functions from other modules
from .browser import extract_video_links, extract_videos_from_urls
from .exporter import save_video_links_to_yaml, OUTPUT_YAML_FILE

# Import logging configuration
from .logger import configure_logging
logger = configure_logging()

# Constants
GOODSTUFF_VIDEOS = [
    "https://vkvideo.ru/@public111751633/all",
    "https://vkvideo.ru/@club180058315/all"
]

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
