import os
import sys
import yaml
import argparse
import subprocess
from enum import IntEnum
from typing import List, Optional
from pathlib import Path

from .extractor import Extractor
from .downloader import Downloader
from .logger import Logger
from .settings import Settings
from .extractor import VideoDTO

# Constants
GOODSTUFF_VIDEOS = [
    "https://vkvideo.ru/@public111751633/all",
    "https://vkvideo.ru/@club180058315/all"
]

class CLIAppError(Exception):
    """Base exception for CLIApp errors"""
    pass

class CLIApp:
    """
    Command-line interface application for VK Video Link Downloader
    """
    def __init__(
        self, 
        extractor: Extractor, 
        downloader: Downloader, 
        logger: Logger, 
        settings: Settings
    ):
        """
        Initialize the CLI application

        Args:
            extractor (Extractor): Video link extractor
            downloader (Downloader): Video downloader
            logger (Logger): Logging utility
            settings (Settings): Application settings
        """
        self.videos = GOODSTUFF_VIDEOS
        self.extractor = extractor
        self.downloader = downloader
        self.logger = logger
        self.settings = settings

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
    
      # Extract video links from a specific URL
      %(prog)s url https://vkvideo.ru/@public111751633/all
    ''',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Goodstuff command
        goodstuff_parser = subparsers.add_parser('goodstuff', help='Extract links from predefined URLs')
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

    def _validate_destination_path(self, destination: Optional[str]) -> Path:
        """
        Validate and prepare destination path for video downloads

        Args:
            destination (Optional[str]): Destination path for downloads

        Returns:
            Path: Validated and absolute path to destination
        
        Raises:
            CLIAppError: If destination path is invalid or cannot be created
        """
        # Use current directory if no destination specified
        if destination is None:
            destination = '.'
        
        # Convert to absolute path and expand user
        dest_path = Path(destination).expanduser().resolve()

        # Create directory if it doesn't exist
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            raise CLIAppError(f"Cannot create destination directory: {dest_path}. {str(e)}")

        # Check if path is writable
        if not os.access(dest_path, os.W_OK):
            raise CLIAppError(f"Destination path is not writable: {dest_path}")

        return dest_path

    def _get_vk_video_page_urls(self, args) -> List[str]:
        """
        Get VK video page URLs from command arguments

        Args:
            args (argparse.Namespace): Parsed command arguments

        Returns:
            List[str]: List of VK video page URLs
        
        Raises:
            CLIAppError: If no URLs are provided and not in goodstuff mode
        """
        # Goodstuff mode with predefined URLs
        if args.command == 'goodstuff':
            self.logger.info("Extracting videos from predefined URLs")
            return self.videos

        # Use provided URLs
        if not args.url:
            raise CLIAppError("No VK video URLs provided. Use --urls or 'goodstuff' command.")

        return [args.url]

    def _download_videos(self, videos: List, dest_path: Path) -> None:
        """
        Download videos to the specified destination.

        Args:
            videos (List): List of videos to download
            dest_path (Path): Destination path for downloads
        
        Raises:
            CLIAppError: If download fails
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
                raise CLIAppError(f"Failed to download video {video.title} from {video.url}: {e}")


    def filter(self, videos: List[VideoDTO]) -> List[VideoDTO]:
        """
        Filter out videos that are in the skiplist.
        
        Args:
            videos (List[VideoDTO]): List of videos to filter
        
        Returns:
            List[VideoDTO]: Filtered list of videos
        """
        filtered_videos = []
        for video in videos:
            if video.url not in self.settings.skiplist:
                filtered_videos.append(video)
            else:
                self.logger.info(f'Skipped video: {video.title}')
        return filtered_videos


    def run(self, cli_args: Optional[List[str]] = None) -> None:
        """
        Main entry point for the VK Video Link Downloader.
        
        Args:
            cli_args (Optional[List[str]], optional): Command-line arguments. Defaults to None.
        
        Raises:
            CLIAppError: For various application-level errors
        """
        # Use provided arguments or default to system arguments
        if cli_args is None:
            cli_args = sys.argv[1:]
        
        # Create parser
        parser = self.create_parser()
        
        # If no arguments, print help and exit
        if len(cli_args) == 0:
            parser.print_help(sys.stderr)
            raise CLIAppError("No arguments provided")
        
        # Parse arguments
        args = parser.parse_args(cli_args)
        
        self.logger.info(f"Application started with command: {args.command}")
        
        # Validate destination directory
        dest_path = self._validate_destination_path(args.destination)

        # Gets video URLs from command line or from goodstuff hardcoded list
        videopage_urls = self._get_vk_video_page_urls(args)

        # Extracts video URLs from the vk videos pages or from cache
        videos_cached = self.extractor.extract_videos_from_urls_cached(videopage_urls)
        videos_cached = self.filter(videos_cached)

        # Download videos
        self.downloader.download_videos(videos_cached, str(dest_path))

        # Check for videos that are not in the cache and download them if there are any
        videos_not_in_cache = self.extractor.extract_videos_from_urls(videopage_urls)
        videos_not_in_cache = self.filter(videos_not_in_cache)
        self.downloader.download_videos(videos_not_in_cache, str(dest_path), skip=videos_cached)
        
        self.logger.info("Application execution completed")
