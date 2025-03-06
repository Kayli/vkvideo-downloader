from playwright.sync_api import sync_playwright, Playwright
import os, time
from typing import Optional

class Downloader2:
    def __init__(self):
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

    def capture_headers(self, page):
        # Store the headers in a dictionary
        request_headers = []
        response_headers = []

        # Function to handle request headers
        def handle_request(request):
            request_headers.append({
                "url": request.url,
                "headers": request.headers
            })

        # Function to handle response headers
        def handle_response(response):
            response_headers.append({
                "url": response.url,
                "headers": response.headers
            })

        # Set up listeners for request and response events
        page.on('request', handle_request)
        page.on('response', handle_response)

        # Wait to capture requests and responses (adjust the timeout as needed)
        page.wait_for_timeout(5000)

        # Return both request and response headers as collections
        return {
            "requests": request_headers,
            "responses": response_headers
        }

    def download_video(self, url: str, desired_filename: str, low_res: bool = False, destination_folder: Optional[str] = None):
        download_path = destination_folder or os.getcwd()
        path_to_extension = '/home/illiam/Downloads/VK-Video-Downloader-main/chromium'
        user_data_dir = os.path.expanduser("~/.config/chromium/")
        download_link_selector = self.low_res_selector if low_res else self.download_link_selector
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


            # capturing headers
            headers = self.capture_headers(page)
            print(f"Captured headers: {headers}")

            with page.expect_download() as download_info:
                # Perform the action that initiates download
                download_link.click()
            download = download_info.value
            if not download:
                raise Exception('Download failed.')
            print("Download started ...")
            print(f"Downloaded file: {download.suggested_filename}")
            # time.sleep(500)
            
            # Wait for the download process to complete
            download_path = download.path()
            print(f'Download completed: {download_path}')
            return Path(download_path)
