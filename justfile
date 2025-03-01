# Justfile for vkvideo-downloader project

# Default recipe to list all available commands
default:
    @just --list

# Run all tests
test:
    poetry run pytest

# Run live tests
test-live:
    poetry run pytest src/tests/test_live.py

# Run unit tests
test-unit:
    poetry run pytest src/tests/unit

# Run the main application script
run:
    poetry run python -m src.app.main goodstuff

# Alias for running the main script
goodstuff: run

# Install project dependencies
install:
    poetry install

# Update project dependencies
update:
    poetry update

# Remove Python cache files and clean up virtual environment
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
    poetry env remove --all

# Run integration tests
test-integration:
    poetry run python -m pytest src/tests/integration

# Run system tests
test-system:
    poetry run python -m pytest src/tests/system
