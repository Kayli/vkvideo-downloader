from typing import Optional
import logging
from pathlib import Path

from ...app.extractor import Extractor, VideoDTO
from ...app.cli_app import CLIApp, GOODSTUFF_VIDEOS
from ...app.logger import Logger
from ...app.settings import Settings
from ...app.downloader import Downloader  # Import the Downloader class

class CLIAppTestFactory:
    """
    Factory for creating CLIApp instances with test dependencies
    """
    @staticmethod
    def create_cli_app(
        extractor: Optional[Extractor] = None,
        logger: Optional[Logger] = None
    ):
        """
        Create a CLIApp instance with test dependencies

        Args:
            extractor (Optional[Extractor], optional): Extractor for extracting video links.
                Defaults to a fake Extractor for testing.
            logger (Optional[Logger], optional): Logger for recording application events.
                Defaults to a fake Logger for testing.

        Returns:
            CLIApp: Configured CLIApp instance
        """

        class FakeExtractor(Extractor):
            """
            A fake extractor for testing
            """
            def __init__(self, settings=None, logger=None, browser=None):
                super().__init__(settings, logger, browser)
                self.predefined_videos = GOODSTUFF_VIDEOS

            def extract_videos_from_urls(self, urls=None):
                """
                Simulate video link extraction

                Args:
                    urls (Optional[List[str]], optional): URLs to extract from.
                        Defaults to predefined videos.

                Returns:
                    List[VideoDTO]: Extracted video links
                """
                urls = urls or self.predefined_videos
                return [
                    VideoDTO(url=f"{url}/video1", title=f"Video from {url}")
                    for url in urls
                ]

        class FakeDownloader(Downloader):
            """
            A fake downloader for testing
            """
            def __init__(self, logger=None):
                super().__init__(logger)

            def download_video(self, url: str, desired_filename: str, low_res: bool = False, destination_folder: Optional[str] = None) -> Path:
                """
                Simulate video download

                Args:
                    url (str): URL of the video to download
                    desired_filename (str): Base filename for the video
                    low_res (bool, optional): Whether to download low resolution. Defaults to False.
                    destination_folder (Optional[str], optional): Folder to save the video. Defaults to None.

                Returns:
                    Path: Path to the simulated downloaded video
                """
                # Create a mock path in the destination folder
                if destination_folder is None:
                    destination_folder = '.'
                return Path(destination_folder) / f"{desired_filename}.mp4"

        class FakeLogger(Logger):
            """
            A fake logger for testing
            """
            def __init__(self, name=None, level=logging.INFO):
                super().__init__(name, level)
                self.captured_logs = {"info": [], "error": []}

            def info(self, msg):
                """Capture info logs"""
                super().info(msg)
                self.captured_logs["info"].append(msg)

            def error(self, msg):
                """Capture error logs"""
                super().error(msg)
                self.captured_logs["error"].append(msg)

        # Use provided dependencies or create fake ones
        extractor = extractor or FakeExtractor()
        logger = logger or FakeLogger()
        downloader = FakeDownloader(logger)

        return CLIApp(extractor=extractor, logger=logger, downloader=downloader)
