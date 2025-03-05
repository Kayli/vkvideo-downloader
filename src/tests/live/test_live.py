import pytest
from playwright.sync_api import TimeoutError

from ..app.factory import CLIAppFactory
from src.tests.fakes.capture_logger import CaptureLogger

@pytest.fixture
def test_url():
    return "https://vkvideo.ru/@public111751633/all"

@pytest.fixture
def capture_logger():
    """Create a CaptureLogger for testing."""
    return CaptureLogger()

def test_extract_video_links(test_url, capture_logger):
    """Test successful video extraction via CLIApp"""
    # Create CLIApp using factory with capture logger
    app = CLIAppFactory.create_cli_app(logger=capture_logger)
    
    # Run the app with URL command
    app.run(['url', test_url])
    
    # Verify logging and other aspects
    assert len(capture_logger.captured_logs['info']) > 0, "Should have info logs"
    assert any("Extracting videos from URL" in log for log in capture_logger.captured_logs['info']), "Should log URL extraction"
    # Check for video extraction logs
    assert any("Extracted" in log for log in capture_logger.captured_logs['info']), "Should log number of extracted videos"

def test_extract_video_links_invalid_url(capture_logger):
    """Test handling of invalid URLs via CLIApp"""
    # Create a CLIApp with the custom logger
    app = CLIAppFactory.create_cli_app(logger=capture_logger)
    
    # Simulate command-line arguments with an invalid URL
    invalid_url = "https://nonexistent-domain-that-should-fail.example"
    
    # Expect an exception
    with pytest.raises(Exception, match="net::ERR_NAME_NOT_RESOLVED"):
        app.run(['url', invalid_url])
    
    # Check captured logs
    assert len(capture_logger.captured_logs['error']) > 0, "Should have error logs"
    assert any("Error extracting video links" in log or "Failed to extract videos" in log for log in capture_logger.captured_logs['error']), "Should log extraction failure"

def test_browser_record_replay(test_url, tmp_path):
    """Test the record and replay functionality of Browser."""
    from ..app.settings import Settings
    from ..app.browser import Browser
    import os

    # Create settings with custom cache directory
    settings = Settings(cache_dir=str(tmp_path))

    # First run: fetch and cache the page
    browser1 = Browser(settings, record_replay=True)
    first_html = browser1.get_page_html(test_url)

    # Verify cache file was created
    cache_filename = browser1._get_cache_path(test_url)
    assert os.path.exists(cache_filename), "Cache file should be created when record_replay is True"

    # Second run: should use cached HTML
    browser2 = Browser(settings, record_replay=True)
    second_html = browser2.get_page_html(test_url)

    # Verify the HTML content is exactly the same
    assert first_html == second_html, "Cached HTML should be identical to first fetch"
    assert len(first_html) > 0, "Fetched HTML should not be empty"
