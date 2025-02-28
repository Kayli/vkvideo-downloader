from typing import Optional, List, Dict

from .exporter import VideoLinkExporter
from .browser import Browser
from .browser import extract_videos_from_urls

class CLIAppFactory:
    """
    Factory for creating CLIApp instances with real dependencies
    """
    @staticmethod
    def create_cli_app(
        videos: Optional[List[str]] = None,
        exporter: Optional[VideoLinkExporter] = None
    ):
        """
        Create a CLIApp instance with real dependencies

        Args:
            videos (Optional[List[str]], optional): List of video URLs. 
                Defaults to GOODSTUFF_VIDEOS if not provided.
            exporter (Optional[VideoLinkExporter], optional): Video link exporter.
                Defaults to a new VideoLinkExporter with default settings.
        
        Returns:
            CLIApp: Configured CLIApp instance
        """
        from .main import CLIApp, GOODSTUFF_VIDEOS  # Import here to avoid circular dependency
        
        # Use provided videos or default
        videos = videos or GOODSTUFF_VIDEOS
        
        # Use provided exporter or create a default one
        exporter = exporter or VideoLinkExporter()
        
        return CLIApp(videos=videos, exporter=exporter)

    @staticmethod
    def create_dependency_graph():
        """
        Create a dependency graph using real production objects

        Returns:
            Dict: A dictionary representing the dependency graph
        """
        return {
            "exporter": VideoLinkExporter(),
            "video_extractor": Browser()
        }

    @staticmethod
    def create_video_extractor(
        headless: bool = True,
        timeout: int = 30000
    ) -> Browser:
        """
        Create a Browser with optional configuration

        Args:
            headless (bool, optional): Whether to run browser in headless mode. Defaults to True.
            timeout (int, optional): Maximum time to wait for page load. Defaults to 30000.
        
        Returns:
            Browser: Configured Browser instance
        """
        return Browser(headless=headless, timeout=timeout)

    @staticmethod
    def create_video_link_exporter(
        output_file: Optional[str] = None
    ) -> VideoLinkExporter:
        """
        Create a VideoLinkExporter with optional configuration

        Args:
            output_file (Optional[str], optional): Path to output YAML file. 
                Defaults to None (uses default from VideoLinkExporter).
        
        Returns:
            VideoLinkExporter: Configured VideoLinkExporter instance
        """
        return VideoLinkExporter(output_file) if output_file else VideoLinkExporter()

    @staticmethod
    def extract_videos(
        urls: Optional[List[str]] = None
    ) -> List[Dict[str, str]]:
        """
        Extract videos from given URLs

        Args:
            urls (Optional[List[str]], optional): URLs to extract videos from. 
                Defaults to GOODSTUFF_VIDEOS if not provided.
        
        Returns:
            List[Dict[str, str]]: Extracted video links
        """
        from .main import GOODSTUFF_VIDEOS
        urls = urls or GOODSTUFF_VIDEOS
        return extract_videos_from_urls(urls)

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
        from .main import CLIApp, GOODSTUFF_VIDEOS  # Import here to avoid circular dependency
        
        # Use provided videos or default
        videos = videos or GOODSTUFF_VIDEOS
        
        # Use provided exporter or create a fake one
        class FakeVideoLinkExporter:
            """
            A fake video link exporter for testing purposes
            """
            def __init__(self):
                self.exported_links = []

            def export(self, links):
                """
                Simulate exporting links
                
                Args:
                    links (List[str]): Video links to export
                """
                self.exported_links.extend(links)

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
            def __init__(self):
                self.extracted_videos = []

            def extract_video_links(self, url):
                """
                Simulate extracting video links
                
                Args:
                    url (str): URL to extract videos from

                Returns:
                    List[Dict[str, str]]: Simulated video links
                """
                return [f"fake_video_link_{url}"]

            def extract_videos_from_urls(self, urls):
                """
                Simulate extracting videos from multiple URLs
                
                Args:
                    urls (List[str]): URLs to extract videos from

                Returns:
                    List[Dict[str, str]]: Simulated video links
                """
                return [f"fake_video_link_{url}" for url in urls]

        return {
            "exporter": CLIAppFactoryTest.create_cli_app().exporter,
            "video_extractor": FakeBrowser()
        }

    @staticmethod
    def create_video_extractor(
        headless: bool = True,
        timeout: int = 30000
    ) -> Browser:
        """
        Create a fake Browser for testing

        Args:
            headless (bool, optional): Ignored in test implementation. Defaults to True.
            timeout (int, optional): Ignored in test implementation. Defaults to 30000.
        
        Returns:
            Browser: Fake Browser instance
        """
        class FakeBrowser(Browser):
            """
            A fake browser for testing purposes
            """
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

        return FakeBrowser(headless=headless, timeout=timeout)
