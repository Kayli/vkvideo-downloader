import pytest
from ...app.downloader2 import Downloader2

def test_downloader2():
    downloader = Downloader2()
    url = 'https://vkvideo.ru/video-111751633_456239058'
    desired_filename = 'test_video'
    downloader.download_video(url, desired_filename, low_res=True)
