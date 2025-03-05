import subprocess
import json
from pathlib import Path
from typing import Optional
from .logger import Logger

class Downloader:
    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger or Logger()

    def _build_base_command(self, url: str, desired_filename: str, low_res: bool = False, destination_folder: Optional[str] = None) -> list:
        """
        Build the base command for yt-dlp with common parameters.

        Args:
            url (str): The URL of the video to download
            desired_filename (str): The base filename for the downloaded video
            low_res (bool, optional): If True, download a low-resolution version of the video. Defaults to False.
            destination_folder (str, optional): Folder to save the video. Defaults to None.

        Returns:
            list: The base command as a list of strings
        """
        # Prepare base command
        command = ["yt-dlp", "-o", f"{desired_filename}.%(ext)s", url]
        
        # Always import cookies from Chrome
        command.extend(["--cookies-from-browser", "chrome"])
        
        # Add low-resolution format selection if enabled
        if low_res:
            command.extend(["-f", "dash_sep-1"])
        
        # Add destination folder if specified
        if destination_folder:
            command.extend(["-P", destination_folder])
        
        return command

    def _get_filename(self, url: str, desired_filename: str) -> str:
        """
        Retrieve the filename for a video without downloading it.

        Args:
            url (str): The URL of the video
            desired_filename (str): The base filename for the downloaded video

        Returns:
            str: The actual filename that would be used for the download
        """
        # Prepare base command to get filename
        command = ["yt-dlp", "-o", f"{desired_filename}.%(ext)s", url]
        
        # Always import cookies from Chrome
        command.extend(["--cookies-from-browser", "chrome"])
        
        # Add --get-filename to retrieve the actual filename
        command.append("--get-filename")
        
        self.logger.debug(f"Retrieving filename with command: {' '.join(command)}")
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            
            # Log stdout and stderr
            if result.stdout:
                self.logger.debug(f"Filename retrieval stdout: {result.stdout.strip()}")
            if result.stderr:
                self.logger.debug(f"Filename retrieval stderr: {result.stderr.strip()}")
        except subprocess.CalledProcessError as e:
            # Log error details
            self.logger.error(f"Failed to get filename. Return code {e.returncode}")
            if e.stdout:
                self.logger.error(f"Stdout: {e.stdout.strip()}")
            if e.stderr:
                self.logger.error(f"Stderr: {e.stderr.strip()}")
            raise
        
        filename = result.stdout.strip()
        self.logger.debug(f"Retrieved filename: {filename}")
        
        return filename

    def download_video(self, url: str, desired_filename: str, low_res: bool = False, destination_folder: Optional[str] = None) -> Path:
        """
        Download a video from the given URL.

        Args:
            url (str): The URL of the video to download
            desired_filename (str): The base filename for the downloaded video
            low_res (bool, optional): If True, download a low-resolution version of the video. Defaults to False.
            destination_folder (str, optional): Folder to save the video. Defaults to None.

        Returns:
            Path: Path to the downloaded video file

        Raises:
            subprocess.CalledProcessError: If the download fails
        """
        # First, get the filename
        filename = self._get_filename(url, desired_filename)
        
        # Build download command (with low-res option if specified)
        command = self._build_base_command(url, desired_filename, low_res, destination_folder)
        
        self.logger.debug(f"Downloading video with command: {' '.join(command)}")
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            
            # Log stdout and stderr
            if result.stdout:
                self.logger.debug(f"Download stdout: {result.stdout.strip()}")
            if result.stderr:
                self.logger.debug(f"Download stderr: {result.stderr.strip()}")
        except subprocess.CalledProcessError as e:
            # Log error details
            self.logger.error(f"Download failed. Return code {e.returncode}")
            if e.stdout:
                self.logger.error(f"Stdout: {e.stdout.strip()}")
            if e.stderr:
                self.logger.error(f"Stderr: {e.stderr.strip()}")
            raise
        
        # Return Path to the downloaded file
        downloaded_file = Path(filename)
        self.logger.debug(f"Download complete. File: {downloaded_file}")
        
        return downloaded_file
