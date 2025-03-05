import os
import sys
import yaml
import argparse
import subprocess
from typing import List, Optional
from pathlib import Path

from .extractor import Extractor
from .exporter import VideoLinkExporter, DEFAULT_OUTPUT_YAML_FILE
from .downloader import Downloader
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
        downloader: Optional[Downloader] = None,
        logger: Optional[Logger] = None
    ):
        """
        Initialize the CLIApp.

        Args:
            exporter (Optional[VideoLinkExporter], optional): Video link exporter.
                Defaults to a new VideoLinkExporter with default settings.
            extractor (Optional[Extractor], optional): Extractor for extracting video links.
                Defaults to a new Extractor instance.
            downloader (Optional[Downloader], optional): Downloader for downloading videos.
                Defaults to a new Downloader instance.
            logger (Optional[Logger], optional): Logger for recording application events.
                Defaults to a new Logger instance.
        """
        self.videos = GOODSTUFF_VIDEOS
        self.exporter = exporter or VideoLinkExporter()
        self.extractor = extractor or Extractor()
        self.downloader = downloader or Downloader()
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
        goodstuff_parser.add_argument(
            '-d', 
            '--destination', 
            type=str, 
            default=os.getcwd(), 
            help='Destination folder for downloaded videos (default: current working directory)'
        )
        
        # URL command
        url_parser = subparsers.add_parser('url', help='Extract links from specific URL')
        url_parser.add_argument('url', type=str, help='URL to extract video links from')
        url_parser.add_argument(
            '-d', 
            '--destination', 
            type=str, 
            default=os.getcwd(), 
            help='Destination folder for downloaded videos (default: current working directory)'
        )
        
        return parser

    def run(self, cli_args: Optional[List[str]] = None) -> int:
        """
        Main entry point for the VK Video Link Downloader.
        
        Args:
            cli_args (Optional[List[str]], optional): Command-line arguments. 
                Defaults to sys.argv[1:] if not provided.
        
        Returns:
            int: Exit code
        """
        # Use provided arguments or default to system arguments
        if cli_args is None:
            cli_args = sys.argv[1:]
        
        # Create parser
        parser = self.create_parser()
        
        # If no arguments, print help and exit
        if len(cli_args) == 0:
            parser.print_help(sys.stderr)
            return 1
        
        # Parse arguments
        args = parser.parse_args(cli_args)
        
        self.logger.info(f"Application started with command: {args.command}")
        
        # Validate destination directory
        dest_path = Path(args.destination).resolve()
        if not dest_path.exists():
            self.logger.error(f"Destination directory does not exist: {dest_path}")
            return 1
        if not dest_path.is_dir():
            self.logger.error(f"Destination is not a directory: {dest_path}")
            return 1

        if args.command == 'goodstuff':
            self.logger.info(f"Extracting videos from predefined URLs: {self.videos}")
            videos = self.extractor.extract_videos_from_urls(self.videos)
            
            if hasattr(args, 'list') and args.list:
                self.logger.info(f"Saving extracted links to YAML file")
                self.exporter.export(videos)
            
            if videos is not None:
                self.logger.info(f"Extracted {len(videos)} unique video links")

         
        elif args.command == 'url':
            self.logger.info(f"Extracting videos from URL: {args.url}")
            videos = self.extractor.extract_videos_from_urls([args.url])
            
            self.logger.info(f"Extracted {len(videos)} video links")

        self.logger.info(f"Downloading videos ...")
        for video in videos:
            try:
                self.logger.info(f"Downloading {video.title} via {video.url}...")
                self.downloader.download_video(
                    video.url, 
                    video.title, 
                    destination_folder=str(dest_path)
                )
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to download video {video.title} from {video.url}: {e}")
        
        self.logger.info("Application execution completed")
        return 0
