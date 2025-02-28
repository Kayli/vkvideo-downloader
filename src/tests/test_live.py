import pytest
from playwright.sync_api import TimeoutError
from ..app.main import extract_video_links

@pytest.fixture
def test_url():
    return "https://vkvideo.ru/@public111751633/all"

def test_extract_video_links(test_url):
    """Test successful video extraction"""
    videos = extract_video_links(test_url, headless=True)
    
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
    """Test handling of invalid URLs"""
    invalid_url = "https://nonexistent-domain-that-should-fail.example"
    with pytest.raises((TimeoutError, Exception)):
        extract_video_links(invalid_url, headless=True)
