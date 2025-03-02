import pytest
import os

from ..fakes.capture_logger import CaptureLogger
from ...app.settings import Settings
from ...app.browser import Browser
from ...app.extractor import Extractor

@pytest.fixture
def test_url():
    return "https://vkvideo.ru/@public111751633/all"

def test_extractor_with_record_replay(test_url):
    """
    Test Extractor with a Browser configured for record-replay.
    
    This test verifies that:
    1. Extractor can successfully extract video links using a cached page
    2. The Browser's record-replay functionality works correctly
    3. The cache is used in subsequent calls
    """
    # Create settings with recordings folder as cache directory
    recordings_dir = os.path.join(os.path.dirname(__file__), 'recordings')
    settings = Settings(cache_dir=recordings_dir)
    
    # Create a capture logger for tracking
    logger = CaptureLogger()

    # First run: create Browser with record_replay enabled
    browser = Browser(settings, record_replay=True)
    
    # Create Extractor with the Browser and logger
    extractor = Extractor(
        settings=settings, 
        browser=browser, 
        logger=logger
    )

    # Extract video links (first run will fetch and cache)
    first_video_links = extractor.extract_video_links(test_url)

    # Verify cache file was created
    cache_filename = browser._get_cache_path(test_url)
    assert os.path.exists(cache_filename), "Cache file should be created when record_replay is True"
    
    # Verify video links were extracted
    assert len(first_video_links) > 0, "Should extract at least one video link"
    
    # Check logging
    assert any("Extracted" in log for log in logger.captured_logs['info']), "Should log number of extracted videos"

    # Create a new Extractor with the same settings (simulating a second run)
    browser2 = Browser(settings, record_replay=True)
    extractor2 = Extractor(
        settings=settings, 
        browser=browser2, 
        logger=logger
    )

    # Extract video links again (should use cached HTML)
    second_video_links = extractor2.extract_video_links(test_url)

    # Verify the video links are the same
    assert first_video_links == second_video_links, "Video links should be identical in both runs"
    
    # Verify log messages
    assert len(logger.captured_logs['info']) > 0, "Should have info logs"
    assert any("Extracted" in log for log in logger.captured_logs['info']), "Should log URL processing"
