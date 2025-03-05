import yt_dlp
from pathlib import Path
from typing import Optional
from .logger import Logger

class Downloader:
    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger or Logger()

    def _get_ydl_opts(self, url: str, desired_filename: str, low_res: bool = False, destination_folder: Optional[str] = None) -> dict:
        """
        Build yt-dlp options for downloading or getting filename.

        Args:
            url (str): The URL of the video to download
            desired_filename (str): The base filename for the downloaded video
            low_res (bool, optional): If True, download a low-resolution version of the video. Defaults to False.
            destination_folder (str, optional): Folder to save the video. Defaults to None.

        Returns:
            dict: Configuration options for yt-dlp
        """
        # Prepare base options
        ydl_opts = {
            'outtmpl': f"{desired_filename}.%(ext)s",
            'cookiesfrombrowser': ('chrome', None, None),
        }
        
        # Add low-resolution format selection if enabled
        if low_res:
            ydl_opts['format'] = 'dash_sep-1'
        
        # Add destination folder if specified
        if destination_folder:
            ydl_opts['paths'] = {'home': destination_folder}
        
        return ydl_opts

    def _get_filename(self, url: str, desired_filename: str) -> str:
        """
        Retrieve the filename for a video without downloading it.

        Args:
            url (str): The URL of the video
            desired_filename (str): The base filename for the downloaded video

        Returns:
            str: The actual filename that would be used for the download
        """
        # Prepare yt-dlp options
        ydl_opts = self._get_ydl_opts(url, desired_filename)
        ydl_opts['simulate'] = True
        ydl_opts['quiet'] = True
        
        self.logger.debug(f"Retrieving filename for URL: {url}")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info_dict)
                
                self.logger.debug(f"Retrieved filename: {filename}")
                return filename
        except Exception as e:
            self.logger.error(f"Failed to get filename: {e}")
            raise

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
            Exception: If the download fails
        """
        # If no destination folder is specified, use current working directory
        if destination_folder is None:
            destination_folder = str(Path.cwd())
        
        # Prepare yt-dlp options
        ydl_opts = self._get_ydl_opts(url, desired_filename, low_res, destination_folder)
        
        self.logger.debug(f"Downloading video from URL: {url}")
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
                
                # Return Path to the downloaded file
                downloaded_file = Path(filename)
                self.logger.debug(f"Download complete. File: {downloaded_file}")
                
                return downloaded_file
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
            raise
