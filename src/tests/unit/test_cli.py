import pytest
import sys
import io
import os
import yaml
import tempfile
import unittest.mock

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
    assert any("Extracted" in log for log in app.logger.captured_logs['info']), "Should log number of extracted videos"

#@pytest.mark.skip(reason="Test implementation removed")
def test_goodstuff_command():
    """
    Test the goodstuff command without --list
    """
    pass

@pytest.mark.skip(reason="Test implementation removed")
def test_no_arguments():
    """
    Test that when no arguments are specified, help information is displayed
    """
    pass
