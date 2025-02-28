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
