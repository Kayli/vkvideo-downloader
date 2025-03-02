from typing import Optional
import logging
import yaml

from ..app.exporter import VideoLinkExporter, OUTPUT_YAML_FILE
from ..app.extractor import Extractor
from ..app.cli_app import CLIApp, GOODSTUFF_VIDEOS
from ..app.logger import Logger
from ..app.settings import Settings

class CLIAppTestFactory:
    """
    Factory for creating CLIApp instances with test dependencies
    """
    @staticmethod
    def create_cli_app(
        exporter: Optional[VideoLinkExporter] = None,
        extractor: Optional[Extractor] = None,
        logger: Optional[Logger] = None
    ):
        """
        Create a CLIApp instance with test dependencies

        Args:
            exporter (Optional[VideoLinkExporter], optional): Video link exporter.
                Defaults to a fake VideoLinkExporter for testing.
            extractor (Optional[Extractor], optional): Extractor for extracting video links.
                Defaults to a fake Extractor for testing.
            logger (Optional[Logger], optional): Logger for recording application events.
                Defaults to a fake Logger for testing.

        Returns:
            CLIApp: Configured CLIApp instance
        """
        class FakeVideoLinkExporter(VideoLinkExporter):
            """
            A fake video link exporter for testing
            """
            def __init__(self, output_file=OUTPUT_YAML_FILE):
                super().__init__()
                self.exported_links = []
                self.output_file = output_file

            def export(self, links):
                """
                Simulate exporting links

                Args:
                    links (List[str]): Video links to export
                """
                self.exported_links.extend(links)
                
                # Write to the specified output file
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(links, f, allow_unicode=True)

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
                    List[Dict[str, str]]: Extracted video links
                """
                urls = urls or self.predefined_videos
                return [
                    {"url": f"{url}/video1", "title": f"Video from {url}"}
                    for url in urls
                ]

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
        exporter = exporter or FakeVideoLinkExporter()
        extractor = extractor or FakeExtractor()
        logger = logger or FakeLogger()

        return CLIApp(exporter=exporter, extractor=extractor, logger=logger)
