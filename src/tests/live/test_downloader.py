import pytest
import subprocess
import os
from ...app.downloader import Downloader 
from ...tests.unit.fakes.capture_logger import CaptureLogger
from pathlib import Path

def test_downloader():
    url = 'https://vkvideo.ru/video66755390_456239173'  # URL to test
    logger = CaptureLogger()  # Use CaptureLogger for testing
    downloader = Downloader(logger)  # Create an instance of your Downloader class with CaptureLogger
    
    # Test low-resolution download
    try:
        result_low = downloader.download_video(url, 'test_video', low_res=True)
        assert result_low is not None, "Download result should not be None"
        assert result_low.exists(), f"Downloaded file {result_low} does not exist. Current working directory: {os.getcwd()}"
    except subprocess.CalledProcessError as e:
        print(f"Low-res download failed: {e}")
        print(f"Error details: {e.stderr}")
        raise
