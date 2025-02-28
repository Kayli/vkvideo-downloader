import os
import sys
import yaml
import argparse
from typing import List, Dict, Optional, Union

# Import classes from other modules
from .browser import Browser
from .exporter import VideoLinkExporter, OUTPUT_YAML_FILE
from .factory import CLIAppFactory

# Constants
GOODSTUFF_VIDEOS = [
    "https://vkvideo.ru/@public111751633/all",
    "https://vkvideo.ru/@club180058315/all"
]

class CLIApp:
    """
    Command-line interface application for VK Video Link Downloader
    """
    def __init__(
        self, 
        videos: Optional[List[str]] = None, 
        exporter: Optional[VideoLinkExporter] = None,
        browser: Optional[Browser] = None
    ):
        """
        Initialize the CLIApp with optional video URLs, exporter, and browser

        Args:
            videos (Optional[List[str]], optional): List of video URLs. 
                Defaults to GOODSTUFF_VIDEOS if not provided.
            exporter (Optional[VideoLinkExporter], optional): Video link exporter.
                Defaults to a new VideoLinkExporter with default settings.
            browser (Optional[Browser], optional): Browser for extracting video links.
                Defaults to a new Browser instance.
        """
        self.videos = videos or GOODSTUFF_VIDEOS
        self.exporter = exporter or VideoLinkExporter()
        self.browser = browser or Browser()

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

    def run(self) -> None:
        """
        Main entry point for the VK Video Link Downloader.
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
            videos = self.browser.extract_videos_from_urls(self.videos)
            
            if args.list:
                self.exporter.save_to_yaml(videos)
            
            if videos is not None:
                print(yaml.safe_dump(videos, allow_unicode=True))
        
        elif args.command == 'url':
            videos = self.browser.extract_videos_from_urls([args.url])
            
            if videos is not None:
                print(yaml.safe_dump(videos, allow_unicode=True))


if __name__ == '__main__':
    CLIAppFactory.create_cli_app().run()
