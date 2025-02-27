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

### Basic Usage

```bash
# Extract video links from a specific VK page
poetry run vkvideo https://vk.com/video_page

# Extract video links from predefined "good stuff" URLs
poetry run vkvideo goodstuff

# List video links to stdout
poetry run vkvideo goodstuff --list

# Show browser window during extraction
poetry run vkvideo https://vk.com/video_page --noheadless

# Specify custom output file
poetry run vkvideo https://vk.com/video_page -o my_videos.txt
```

### Options

- `URL`: VK page URL to extract video links from
- `goodstuff`: Use predefined list of interesting video URLs
- `--list`: Print video links to stdout
- `--noheadless`: Disable headless mode (browser window will be visible)
- `--output, -o`: Specify output file for video links (default: `video_links.txt`)

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