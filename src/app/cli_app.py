import os
import sys
import yaml
import argparse
import subprocess
from enum import IntEnum
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

class ExitCode(IntEnum):
    """
    Enum representing exit codes for the CLI application.
    
    Follows standard Unix/Linux exit code conventions with some application-specific additions.
    """
    SUCCESS = 0
    GENERAL_ERROR = 1
    MISUSE_OF_SHELL_BUILTIN = 2
    INVALID_USAGE = 64
    DESTINATION_ERROR = 73  # Data error
    DOWNLOAD_ERROR = 74     # Input/output error
    CONFIG_ERROR = 78       # Configuration error

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

    def _validate_destination(self, dest_path: Path) -> bool:
        """
        Validate the destination directory.

        Args:
            dest_path (Path): Path to the destination directory

        Returns:
            bool: True if destination is valid, False otherwise
        """
        if not dest_path.exists():
            self.logger.error(f"Destination directory does not exist: {dest_path}")
            return False
        if not dest_path.is_dir():
            self.logger.error(f"Destination is not a directory: {dest_path}")
            return False
        return True

    def _extract_videos(self, command: str, args) -> Optional[List]:
        """
        Extract videos based on the command.

        Args:
            command (str): The command ('goodstuff' or 'url')
            args: Parsed command-line arguments

        Returns:
            Optional[List]: List of extracted videos or None
        """
        if command == 'goodstuff':
            self.logger.info(f"Extracting videos from predefined URLs: {self.videos}")
            videos = self.extractor.extract_videos_from_urls(self.videos)
            
            if hasattr(args, 'list') and args.list:
                self.logger.info(f"Saving extracted links to YAML file")
                self.exporter.export(videos)
            
            if videos is not None:
                self.logger.info(f"Extracted {len(videos)} unique video links")
            
            return videos

        elif command == 'url':
            self.logger.info(f"Extracting videos from URL: {args.url}")
            videos = self.extractor.extract_videos_from_urls([args.url])
            
            self.logger.info(f"Extracted {len(videos)} video links")
            
            return videos

        return None

    def _download_videos(self, videos: List, dest_path: Path) -> ExitCode:
        """
        Download videos to the specified destination.

        Args:
            videos (List): List of videos to download
            dest_path (Path): Destination path for downloads

        Returns:
            ExitCode: Status of the download operation
        """
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
                return ExitCode.DOWNLOAD_ERROR
        
        return ExitCode.SUCCESS

    def run(self, cli_args: Optional[List[str]] = None) -> ExitCode:
        """
        Main entry point for the VK Video Link Downloader.
        
        Args:
            cli_args (Optional[List[str]], optional): Command-line arguments. 
                Defaults to sys.argv[1:] if not provided.
        
        Returns:
            ExitCode: Exit code representing the result of the application execution
        """
        # Use provided arguments or default to system arguments
        if cli_args is None:
            cli_args = sys.argv[1:]
        
        # Create parser
        parser = self.create_parser()
        
        # If no arguments, print help and exit
        if len(cli_args) == 0:
            parser.print_help(sys.stderr)
            return ExitCode.INVALID_USAGE
        
        # Parse arguments
        args = parser.parse_args(cli_args)
        
        self.logger.info(f"Application started with command: {args.command}")
        
        # Validate destination directory
        dest_path = Path(args.destination).resolve()
        if not self._validate_destination(dest_path):
            return ExitCode.DESTINATION_ERROR

        # Extract videos
        videos = self._extract_videos(args.command, args)
        
        # Download videos
        if videos:
            download_status = self._download_videos(videos, dest_path)
            if download_status != ExitCode.SUCCESS:
                return download_status
        
        self.logger.info("Application execution completed")
        return ExitCode.SUCCESS
