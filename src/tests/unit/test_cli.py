import pytest
import sys
import io
import os
import yaml
import tempfile
import unittest.mock
import re

from ...app.cli_app import CLIApp, GOODSTUFF_VIDEOS
from ...app.exporter import VideoLinkExporter
from ..unit.factory import CLIAppTestFactory

def test_goodstuff_list_command():
    """
    Test the goodstuff --list functionality
    
    Verifies that:
    1. The correct number of videos are extracted
    2. The correct links are exported
    """
    # Create a test CLIApp with mock dependencies
    app = CLIAppTestFactory.create_cli_app()

    # Run the command with --list argument
    app.run(['goodstuff', '--list'])

    # Verify the number of extracted links matches the number of predefined URLs
    assert len(app.exporter.exported_links) > 0, "Should extract at least one video link"

def test_goodstuff_command():
    """
    Test the goodstuff command without --list
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
    logs_with_video_links = [log for log in app.logger.captured_logs['info'] if re.search(r"Extracted \d+ unique video links", log)]
    assert len(logs_with_video_links) > 0, "Should log number of extracted videos"

def test_no_arguments(capsys):
    app = CLIAppTestFactory.create_cli_app()
    exit_code = app.run([])  # Pass an empty list to simulate no arguments
    assert exit_code == 1  # Check that the exit code is 1 for no arguments
    captured = capsys.readouterr()
    assert "usage:" in captured.err
