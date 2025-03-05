import pytest
import sys
import io
import os
import yaml
import tempfile
import unittest.mock
import re

from ...app.cli_app import CLIApp, GOODSTUFF_VIDEOS
from ...app.exporter import OUTPUT_YAML_FILE
from ...tests.factory import CLIAppTestFactory

def test_goodstuff_list_command(tmp_path):
    """
    Test the goodstuff --list functionality
    
    Verifies that:
    1. The command saves extracted links to a YAML file
    2. The correct number of videos are extracted
    3. The YAML file is created with the expected content
    """
    # Set the output YAML path to a temporary file
    output_yaml_path = os.path.join(tmp_path, OUTPUT_YAML_FILE)

    # Create a test CLIApp with mock dependencies and custom output path
    exporter = CLIAppTestFactory.create_cli_app().exporter.__class__(output_file=output_yaml_path)
    app = CLIAppTestFactory.create_cli_app(exporter=exporter)

    # Run the command with --list argument
    app.run(['goodstuff', '--list'])

    # Verify the YAML file was created
    assert os.path.exists(output_yaml_path), "YAML file should be created when --list is used"

    # Read the exported YAML file
    with open(output_yaml_path, 'r') as f:
        exported_links = yaml.safe_load(f)

    # Verify the number of extracted links matches the number of predefined URLs
    assert len(exported_links) > 0, "Should extract at least one video link"
    assert len(exported_links) == len(app.extractor.extract_videos_from_urls(GOODSTUFF_VIDEOS)), "Number of extracted links should match"

    # Verify the log messages
    assert any("Extracting videos from predefined URLs" in log for log in app.logger.captured_logs['info']), "Should log URL extraction"
    assert any("Saving extracted links to" in log for log in app.logger.captured_logs['info']), "Should log YAML export"
    logs_with_video_links = [log for log in app.logger.captured_logs['info'] if re.search(r"Extracted \d+ unique video links", log)]
    assert len(logs_with_video_links) > 0, "Should log number of extracted videos"

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
    """
    Test that when no arguments are specified, help information is displayed
    """
    # Create a test CLIApp with mock dependencies
    app = CLIAppTestFactory.create_cli_app()

    # Run the command without arguments
    with pytest.raises(SystemExit) as excinfo:
        app.run([])

    # Capture stderr
    captured = capsys.readouterr()

    # Check if the expected help information is displayed in stderr
    help_message = "VK Video Link Downloader"
    assert help_message in captured.err, "Help information should be displayed when no arguments are specified"

    # Verify that 'Examples:' is also present in the output
    examples_message = "Examples:"
    assert examples_message in captured.err, "Examples section should be displayed when no arguments are specified"

    # Verify that 'Examples:' is also present in the output
    assert "Examples:" in captured.err, "Examples section should be displayed when no arguments are specified"
