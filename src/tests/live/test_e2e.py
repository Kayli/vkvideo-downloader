import pytest
from ..unit.fakes.capture_logger import CaptureLogger
from ...app.factory import Factory

@pytest.fixture
def test_url():
    return "https://vkvideo.ru/@public111751633/all"

@pytest.fixture
def capture_logger():
    """Create a CaptureLogger for testing."""
    return CaptureLogger()

@pytest.mark.skip(reason="Skipping this test for now, as it tries to download a bunch of huge size videos")
def test_extract_video_links(test_url, capture_logger):
    """Test successful video extraction via CLIApp"""
    app = Factory.create_cli_app(logger=capture_logger)
    app.run(['url', test_url])
    assert len(capture_logger.captured_logs['info']) > 0, "Should have info logs"
    assert any("Extracting videos from URL" in log for log in capture_logger.captured_logs['info']), "Should log URL extraction"
    assert any("Extracted" in log for log in capture_logger.captured_logs['info']), "Should log number of extracted videos"


def test_extract_video_links_invalid_url(capture_logger):
    """Test handling of invalid URLs via CLIApp"""
    app = Factory.create_cli_app(logger=capture_logger)
    invalid_url = "https://nonexistent-domain-that-should-fail.example"
    with pytest.raises(Exception, match="net::ERR_NAME_NOT_RESOLVED"):
        app.run(['url', invalid_url])
    assert len(capture_logger.captured_logs['error']) > 0, "Should have error logs"
    assert any("Error extracting video links" in log or "Failed to extract videos" in log for log in capture_logger.captured_logs['error']), "Should log extraction failure"
