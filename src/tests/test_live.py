import sys
import pytest
from playwright.sync_api import TimeoutError

from ..app.factory import CLIAppFactory
from ..app.logger import CaptureLogger
from ..app.browser import Browser

@pytest.fixture
def test_url():
    return "https://vkvideo.ru/@public111751633/all"

@pytest.fixture
def capture_logger():
    """Create a CaptureLogger for testing."""
    return CaptureLogger()

def test_extract_video_links(test_url, capture_logger):
    """Test successful video extraction via CLIApp"""
    # Create a browser with the capture logger
    browser = Browser(logger=capture_logger)
    
    # Create a CLIApp with the custom browser and logger
    app = CLIAppFactory.create_cli_app(
        browser=browser,
        logger=capture_logger
    )
    
    # Simulate command-line arguments
    sys.argv = ['vkvideo-downloader', 'url', test_url]
    
    # Run the app
    app.run()
    
    # Check captured logs
    assert len(capture_logger.captured_logs['info']) > 0, "Should have info logs"
    assert any("Extracting videos from URL" in log for log in capture_logger.captured_logs['info']), "Should log URL extraction"
    
    # Check for video extraction logs
    assert any("Extracted" in log for log in capture_logger.captured_logs['info']), "Should log number of extracted videos"

def test_extract_video_links_invalid_url(capture_logger):
    """Test handling of invalid URLs via CLIApp"""
    # Create a browser with the capture logger
    browser = Browser(logger=capture_logger)
    
    # Create a CLIApp with the custom browser and logger
    app = CLIAppFactory.create_cli_app(
        browser=browser,
        logger=capture_logger
    )
    
    # Simulate command-line arguments with an invalid URL
    invalid_url = "https://nonexistent-domain-that-should-fail.example"
    sys.argv = ['vkvideo-downloader', 'url', invalid_url]
    
    # Expect an exception
    with pytest.raises(Exception, match="net::ERR_NAME_NOT_RESOLVED"):
        app.run()
    
    # Check captured logs
    assert len(capture_logger.captured_logs['error']) > 0, "Should have error logs"
    assert any("Error extracting video links" in log or "Failed to extract videos" in log for log in capture_logger.captured_logs['error']), "Should log extraction failure"
