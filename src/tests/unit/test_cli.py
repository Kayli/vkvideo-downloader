import io
import sys
import re
import pytest

from ...app.cli_app import CLIApp, CLIAppError, GOODSTUFF_VIDEOS
from ...app.main import ExitCode
from ..unit.factory import CLIAppTestFactory


def test_goodstuff_command():
    """
    Test the goodstuff command
    """
    # Create a test CLIApp with mock dependencies
    app = CLIAppTestFactory.create_cli_app()

    # Capture the stdout
    captured_stdout = io.StringIO()
    sys.stdout = captured_stdout

    # Run the command without arguments
    app.run(['goodstuff'])

    # Reset the stdout
    sys.stdout = sys.__stdout__

    # Check if the expected output or log messages are generated
    assert "Application started with command: goodstuff" in app.logger.captured_logs['info'][0], "Should log application start"
    assert "Extracting videos from predefined URLs" in app.logger.captured_logs['info'][1], "Should log URL extraction"
    
    # Check the number of downloaded videos using the download_calls counter
    downloader = app.downloader
    assert downloader.download_calls > 0, "Should download at least one video"

    # Optional: Check the number of videos matches the predefined GOODSTUFF_VIDEOS
    assert downloader.download_calls == len(GOODSTUFF_VIDEOS), "Number of downloaded videos should match predefined videos"

def test_no_arguments(capsys):
    app = CLIAppTestFactory.create_cli_app()
    
    # Expect CLIAppError to be raised when no arguments are provided
    with pytest.raises(CLIAppError, match="No arguments provided"):
        app.run([])

    # Capture the stderr output
    captured = capsys.readouterr()
    
    # Check that help message was printed to stderr
    assert "VK Video Link Downloader" in captured.err
    assert "goodstuff" in captured.err
    assert "url" in captured.err
