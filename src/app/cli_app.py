import os
import sys
import yaml
import argparse
from typing import List, Optional

from .extractor import Extractor
from .exporter import VideoLinkExporter, OUTPUT_YAML_FILE
from .logger import Logger

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
        exporter: Optional[VideoLinkExporter] = None,
        extractor: Optional[Extractor] = None,
        logger: Optional[Logger] = None
    ):
        """
        Initialize the CLIApp.

        Args:
            exporter (Optional[VideoLinkExporter], optional): Video link exporter.
                Defaults to a new VideoLinkExporter with default settings.
            extractor (Optional[Extractor], optional): Extractor for extracting video links.
                Defaults to a new Extractor instance.
            logger (Optional[Logger], optional): Logger for recording application events.
                Defaults to a new Logger instance.
        """
        self.videos = GOODSTUFF_VIDEOS
        self.exporter = exporter or VideoLinkExporter()
        self.extractor = extractor or Extractor()
        self.logger = logger or Logger()

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

    def run(self, cli_args: Optional[List[str]] = None) -> None:
        """
        Main entry point for the VK Video Link Downloader.
        
        Args:
            cli_args (Optional[List[str]], optional): Command-line arguments. 
                Defaults to sys.argv[1:] if not provided.
        """
        # Use provided arguments or default to system arguments
        if cli_args is None:
            cli_args = sys.argv[1:]
        
        # Create parser
        parser = self.create_parser()
        
        # If no arguments, print help and exit
        if len(cli_args) == 0:
            parser.print_help(sys.stderr)
            sys.exit(1)
        
        # Parse arguments
        args = parser.parse_args(cli_args)
        
        self.logger.info(f"Application started with command: {args.command}")
        
        if args.command == 'goodstuff':
            self.logger.info(f"Extracting videos from predefined URLs: {self.videos}")
            videos = self.extractor.extract_videos_from_urls(self.videos)
            
            if hasattr(args, 'list') and args.list:
                self.logger.info(f"Saving extracted links to {OUTPUT_YAML_FILE}")
                self.exporter.export(videos)
            
            if videos is not None:
                self.logger.info(f"Extracted {len(videos)} unique video links")
                print(yaml.safe_dump(videos, allow_unicode=True))
        
        elif args.command == 'url':
            self.logger.info(f"Extracting videos from URL: {args.url}")
            videos = self.extractor.extract_videos_from_urls([args.url])
            
            self.logger.info(f"Extracted {len(videos)} video links")
        
        self.logger.info("Application execution completed")
