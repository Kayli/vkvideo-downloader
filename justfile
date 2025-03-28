# Justfile for vkvideo-downloader project

# Default recipe to list all available commands
default:
    @just --list

# Run all tests
test: test-unit && test-live

# Run unit tests
test-unit:
    poetry run pytest src/tests/unit

# Run live tests
test-live:
    poetry run pytest src/tests/live

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
