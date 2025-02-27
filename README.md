# VK Video Downloader

A Python tool for downloading videos from VK (VKontakte) social network.

## Features

- Extract video links from VK pages
- Support for both public and private videos (when logged in)
- Headless mode for automated scraping

## Installation

### From Source

1. Clone the repository:
```bash
git clone https://github.com/Kayli/vkvideo-downloader.git
cd vkvideo-downloader
```

2. Install with Poetry (recommended):
```bash
poetry install
```

Or install with pip:
```bash
pip install .
```

### Dependencies

- Python 3.11+
- Playwright for web scraping
- yt-dlp for video downloading

## Usage

### As a Python Package

```python
from src.main import extract_video_links

# Extract video links from a VK page
videos = extract_video_links("https://vkvideo.ru/@public111751633/all")

for video in videos:
    print(f"Title: {video['title']}")
    print(f"URL: {video['url']}")
```

## Development

### Running Tests

```bash
poetry run pytest
```

Or if using pip:
```bash
pytest
```

### Project Structure

```
vkvideo-downloader/
  ├── src/              # Source code
  │   ├── __init__.py
  │   └── main.py      # Main implementation
  ├── tests/           # Test files
  │   └── test_main.py
  ├── pyproject.toml   # Project & dependency configuration
  └── README.md
```

## License

MIT License