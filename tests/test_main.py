import pytest
from playwright.sync_api import TimeoutError
import os
from main import extract_video_links

# Create directory for HAR files if it doesn't exist
HAR_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
os.makedirs(HAR_DIR, exist_ok=True)

@pytest.fixture
def test_url():
    return "https://vkvideo.ru/@public111751633/all"

def test_extract_video_links(test_url):
    har_path = os.path.join(HAR_DIR, 'successful_extraction.har')
    
    # Run the extraction with HAR recording
    videos = extract_video_links(test_url, record_har=True, har_path=har_path)
    
    # Basic assertions
    assert isinstance(videos, list), "Should return a list"
    assert len(videos) > 0, "Should find at least one video"
    
    # Check structure of each video entry
    for video in videos:
        assert isinstance(video, dict), "Each video should be a dictionary"
        assert 'url' in video, "Each video should have a URL"
        assert 'title' in video, "Each video should have a title"
        assert video['url'].startswith('https://vkvideo.ru/video-'), "URL should be properly formatted"
        assert len(video['title']) > 0, "Title should not be empty"

def test_extract_video_links_invalid_url():
    har_path = os.path.join(HAR_DIR, 'failed_extraction.har')
    
    # Using a completely invalid domain that should fail
    invalid_url = "https://nonexistent-domain-that-should-fail.example"
    with pytest.raises((TimeoutError, Exception)):
        extract_video_links(invalid_url, record_har=True, har_path=har_path)
