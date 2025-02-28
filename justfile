# Justfile for vkvideo-downloader project

# Default recipe (shows available recipes)
default:
    @just --list

# Run all tests
test:
    poetry run python -m pytest

# Run main script
run:
    poetry run python -m src.app.main goodstuff

# Alias goodstuff to run
goodstuff: run

# Install dependencies
install:
    poetry install

# Update dependencies
update:
    poetry update


# Clean up Python cache files
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
    poetry env remove --all
