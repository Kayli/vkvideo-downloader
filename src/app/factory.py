from typing import Optional, List

from .logger import Logger
from .extractor import Extractor
from .downloader import Downloader
from .settings import Settings
from .cli_app import CLIApp

class Factory:
    @staticmethod
    def create_cli_app(
        extractor: Optional[Extractor] = None,
        downloader: Optional[Downloader] = None,
        settings: Optional[Settings] = None,
        logger: Optional[Logger] = None,
    ) -> CLIApp:
        logger = logger or Logger()
        extractor = extractor or Extractor(logger=logger)
        downloader = downloader or Downloader(logger=logger)
        settings = settings or Settings()
        return CLIApp(
            extractor=extractor,
            downloader=downloader,
            logger=logger,
            settings=settings,
        )
