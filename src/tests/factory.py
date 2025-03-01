from typing import Optional, List, Dict

from ..app.exporter import VideoLinkExporter
from ..app.extractor import Extractor
from ..app.main import CLIApp, GOODSTUFF_VIDEOS
from ..app.settings import Settings

class CLIAppFactoryTest:
    """
    Factory for creating CLIApp instances with test dependencies
    """
    @staticmethod
    def create_cli_app(
        videos: Optional[List[str]] = None,
        exporter: Optional[VideoLinkExporter] = None
    ):
        """
        Create a CLIApp instance with test dependencies

        Args:
            videos (Optional[List[str]], optional): List of video URLs. 
                Defaults to GOODSTUFF_VIDEOS if not provided.
            exporter (Optional[VideoLinkExporter], optional): Video link exporter.
                Defaults to a fake VideoLinkExporter for testing.
        
        Returns:
            CLIApp: Configured CLIApp instance
        """
        class FakeVideoLinkExporter(VideoLinkExporter):
            """
            A fake video link exporter for testing
            """
            def __init__(self):
                super().__init__()
                self.exported_links = []

            def export(self, links):
                """
                Simulate exporting links
                
                Args:
                    links (List[str]): Video links to export
                """
                self.exported_links.extend(links)

        # Use provided videos or default
        videos = videos or GOODSTUFF_VIDEOS
        
        # Use provided exporter or create a fake one
        exporter = exporter or FakeVideoLinkExporter()
        
        return CLIApp(videos=videos, exporter=exporter)

    @staticmethod
    def create_dependency_graph():
        """
        Create a dependency graph using fake objects for testing

        Returns:
            Dict: A dictionary representing the test dependency graph
        """
        class FakeBrowser:
            """
            A fake browser for testing purposes
            """
            def __init__(self, settings: Settings):
                pass

        def create_fake_browser(
            *,
            settings: Settings = None,
        ) -> Extractor:
            """
            Create a fake Extractor for testing

            Args:
                settings (Settings, optional): Application settings. Defaults to None.

            Returns:
                Extractor: Fake Extractor instance
            """
            settings = settings or Settings()
            
            class FakeBrowser(Extractor):
                def __init__(self, settings: Settings):
                    super().__init__(settings)

            return FakeBrowser(settings)

        return {
            "exporter": CLIAppFactoryTest.create_cli_app().exporter,
            "video_extractor": create_fake_browser()
        }

    @staticmethod
    def create_video_extractor(
        settings: Optional[Settings] = None
    ) -> Extractor:
        """
        Create a fake Extractor for testing

        Args:
            settings (Optional[Settings], optional): Application settings. Defaults to None.
        
        Returns:
            Extractor: Fake Extractor instance
        """
        settings = settings or Settings()
        
        class FakeBrowser(Extractor):
            """
            A fake browser for testing purposes
            """
            def __init__(self, settings: Settings):
                super().__init__(settings)

            def extract_video_links(self, url: str) -> List[Dict[str, str]]:
                """
                Simulate extracting video links
                
                Args:
                    url (str): URL to extract videos from

                Returns:
                    List[Dict[str, str]]: Simulated video links
                """
                return [
                    {
                        'url': f'https://fake-vkvideo.ru/video-{url}',
                        'title': f'Fake Video from {url}'
                    }
                ]

            def extract_videos_from_urls(self, urls: List[str]) -> List[Dict[str, str]]:
                """
                Simulate extracting videos from multiple URLs
                
                Args:
                    urls (List[str]): URLs to extract videos from

                Returns:
                    List[Dict[str, str]]: Simulated video links
                """
                return [
                    {
                        'url': f'https://fake-vkvideo.ru/video-{url}',
                        'title': f'Fake Video from {url}'
                    } for url in urls
                ]

        return FakeBrowser(settings)
