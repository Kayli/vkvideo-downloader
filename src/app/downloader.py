from playwright.sync_api import sync_playwright, Playwright
import os, time
from typing import Optional, List
from pathlib import Path
from .logger import Logger

class Downloader:
    def __init__(self, logger: Optional[Logger] = None):
        self.logger = logger or Logger()
        self.download_link_selector = '#vkVideoDownloaderPanel > a:last-of-type'
        self.low_res_selector = '#vkVideoDownloaderPanel > a:first-of-type'

    def wait_for_element(self, page, selector, timeout=20, interval=1):
        end_time = time.time() + timeout
        while time.time() < end_time:
            result = page.evaluate(f'document.querySelector("{selector}")')
            if result:
                return
        time.sleep(interval)
        raise Exception('Element not found')

    def download_video(self, url: str, desired_filename: str, low_res: bool = False, destination_folder: Optional[str] = None):
        download_path = destination_folder or os.getcwd()
        path_to_extension = '/home/illiam/Downloads/VK-Video-Downloader-main/chromium'
        user_data_dir = os.path.expanduser("~/.config/chromium/")
        download_link_selector = self.low_res_selector if low_res else self.download_link_selector
        if not desired_filename.endswith('.mp4'):
            desired_filename += '.mp4'
        filename_with_path = os.path.join(download_path, desired_filename)

        if os.path.exists(filename_with_path):
            print(f'File already exists: {filename_with_path}')
            return Path(filename_with_path)

        with sync_playwright() as playwright:
            context = playwright.chromium.launch_persistent_context(
                user_data_dir,
                channel="chromium",
                args=[
                    f"--disable-extensions-except={path_to_extension}",
                    f"--load-extension={path_to_extension}",
                    f'--download-default-directory={download_path}'
                ],
                accept_downloads=True,
                headless=False
            )
            context.set_default_timeout(settings.timeout_browser_sec * 1000)
            page = context.new_page()
            page.goto(url)
            
            # Check for logged-in status
            if page.locator('text=Зарегистрируйтесь, чтобы смотреть видео без ограничений').is_visible():
                raise Exception('User is not logged in. Please log in to continue.')
            
            self.wait_for_element(page, download_link_selector)
            download_link = page.locator(download_link_selector)
            if not download_link:
                raise Exception('Download link not found.')
            download_link_href = download_link.get_attribute('href')
            print(f'Found download link: {download_link_href}')

            # remove video player from page, so that it doesn't consume extra traffic
            page.locator('#video_player').evaluate('node => node.remove()')

            with page.expect_download() as download_info:
                # Perform the action that initiates download
                download_link.click()
            download = download_info.value
            if not download:
                raise Exception('Download failed.')
            print(f"Downloading of file {desired_filename} started ...")

            # watch progress
            page = context.new_page()
            page.goto("chrome://downloads/")

            progress = None
            while True:
                progress = page.evaluate("""[
                            ...document.querySelectorAll('*')
                            ]
                            .concat(
                                [...document.querySelectorAll('*')]
                                .flatMap(host => host.shadowRoot ? [
                                    ...host.shadowRoot.querySelectorAll('*'),
                                    ...[...host.shadowRoot.querySelectorAll('*')].flatMap(subHost => 
                                    subHost.shadowRoot ? [...subHost.shadowRoot.querySelectorAll('*')] : []
                                    )
                                ] : [])
                            )
                            .filter(el => el.id === 'details')[0].children[2].innerText""")
                print(f'Current progress: {progress.strip()}          ', end='\r')
                if progress.strip() == '':
                    break
                time.sleep(1)

            # This is a blocking call and will make sure the download is completed before proceeding further
            download.save_as(filename_with_path)
            
            print(f'Download completed: {desired_filename}')
            time.sleep(100)
            return Path(filename_with_path)


    def download_videos(self, videos: List, destination_folder: Optional[str] = None, skip: List = []) -> None:
        """
        Download multiple videos to the specified destination.

        Args:
            videos (List): List of videos to download, each with url and title attributes
            destination_folder (str, optional): Folder to save the videos. Defaults to None.
            skip (List, optional): List of videos to skip downloading. Defaults to an empty list.
        """
        self.logger.info(f"Downloading {len(videos)} videos ...")
        
        for video in videos:
            # Skip video if it's in the skip collection
            if video in skip:
                self.logger.info(f"Skipping video {video.title} as it is in the skip collection...")
                continue

            try:
                self.logger.info(f"Downloading {video.title} via {video.url}...")
                self.download_video(
                    video.url, 
                    video.title, 
                    destination_folder=destination_folder
                )
            except Exception as e:
                self.logger.error(f"Failed to download video {video.title} from {video.url}: {e}")
                raise