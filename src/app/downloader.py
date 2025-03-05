import subprocess

class Downloader:
    def download_video(self, url: str, desired_filename: str):
        command = ["yt-dlp", "-o", f"{desired_filename}.%(ext)s", url]
        try:
            subprocess.run(command, check=True)
            print(f"Downloaded: {desired_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {url}: {e}")
