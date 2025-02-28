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

class CLIApp:
    """
    Command-line interface application for VK Video Link Downloader
    """
    def __init__(self, videos: Optional[List[str]] = None):
        """
        Initialize the CLIApp with optional video URLs

        Args:
            videos (Optional[List[str]], optional): List of video URLs. 
                Defaults to GOODSTUFF_VIDEOS if not provided.
        """
        self.videos = videos or GOODSTUFF_VIDEOS

    def create_parser(self) -> argparse.ArgumentParser:
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

    def run(self) -> Optional[List[Dict[str, str]]]:
        """
        Main entry point for the VK Video Link Downloader.
        
        Returns:
            Optional[List[Dict[str, str]]]: List of extracted video links or None
        """
        # Create parser
        parser = self.create_parser()
        
        # If no arguments, print help and exit
        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)
        
        # Parse arguments
        args = parser.parse_args()
        
        if args.command == 'goodstuff':
            videos = extract_videos_from_urls(self.videos)
            
            if args.list:
                save_video_links_to_yaml(videos)
                return None
            
            return videos
        
        elif args.command == 'url':
            return extract_video_links(args.url)
        
        return None


def main() -> Optional[List[Dict[str, str]]]:
    """
    Convenience function to create and run CLIApp
    
    Returns:
        Optional[List[Dict[str, str]]]: Result from CLIApp run method
    """
    app = CLIApp()
    result = app.run()
    if result is not None:
        print(yaml.safe_dump(result, allow_unicode=True))
    return result

if __name__ == '__main__':
    main()
