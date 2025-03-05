import pytest
from ..app.settings import Settings
from ..app.browser import Browser
import os

@pytest.fixture
def test_url():
    return "https://vkvideo.ru/@public111751633/all"

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
