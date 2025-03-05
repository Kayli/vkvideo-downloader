import pytest
import os

from ..fakes.capture_logger import CaptureLogger
from ...app.settings import Settings
from ...app.browser import Browser
from ...app.extractor import Extractor, is_timestamp

@pytest.fixture
def test_url():
    return "https://vkvideo.ru/@public111751633/all"

def setup_test_environment():
    recordings_dir = os.path.join(os.path.dirname(__file__), 'recordings')
    settings = Settings(cache_dir=recordings_dir)
    logger = CaptureLogger()
    browser = Browser(settings, record_replay=True)
    return settings, logger, browser


def test_cache_creation(test_url):
    settings, logger, browser = setup_test_environment()
    extractor = Extractor(settings=settings, browser=browser, logger=logger)
    extractor.extract_video_links(test_url)
    cache_filename = browser._get_cache_path(test_url)
    assert os.path.exists(cache_filename), "Cache file should be created when record_replay is True"


def test_video_link_extraction(test_url):
    settings, logger, browser = setup_test_environment()
    extractor = Extractor(settings=settings, browser=browser, logger=logger)
    first_video_links = extractor.extract_video_links(test_url)
    assert len(first_video_links) > 0, "Should extract at least one video link"


def test_logging_for_extraction(test_url):
    settings, logger, browser = setup_test_environment()
    extractor = Extractor(settings=settings, browser=browser, logger=logger)
    extractor.extract_video_links(test_url)
    assert any("Extracted" in log for log in logger.captured_logs['info']), "Should log number of extracted videos"


def test_cache_usage(test_url):
    settings, logger, browser = setup_test_environment()
    extractor = Extractor(settings=settings, browser=browser, logger=logger)
    first_video_links = extractor.extract_video_links(test_url)
    extractor2 = Extractor(settings=settings, browser=browser, logger=logger)
    second_video_links = extractor2.extract_video_links(test_url)
    assert first_video_links == second_video_links, "Video links should be identical in both runs"


def test_logging_for_second_run(test_url):
    settings, logger, browser = setup_test_environment()
    extractor = Extractor(settings=settings, browser=browser, logger=logger)
    extractor.extract_video_links(test_url)
    extractor2 = Extractor(settings=settings, browser=browser, logger=logger)
    extractor2.extract_video_links(test_url)
    assert len(logger.captured_logs['info']) > 0, "Should have info logs"
    assert any("Extracted" in log for log in logger.captured_logs['info']), "Should log URL processing"


def test_title_extraction(test_url):
    settings, logger, browser = setup_test_environment()
    extractor = Extractor(settings=settings, browser=browser, logger=logger)
    video_links = extractor.extract_video_links(test_url)

    for video in video_links:
        title = video.title  # Access the title using the attribute
        assert title, f"Title is empty or None for video: {video}"
        assert not is_timestamp(title), f"Detected timestamp instead of title: {title}"  
