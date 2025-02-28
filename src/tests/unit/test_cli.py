import os
import yaml
import unittest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import sys
import logging
import importlib

from ...app.main import main, GOODSTUFF_VIDEOS, OUTPUT_YAML_FILE, save_video_links_to_yaml


class TestVKVideoCLI(unittest.TestCase):
    def test_goodstuff_list_command(self):
        """
        Test the goodstuff --list functionality
        This test mocks the extract_video_links and file saving
        """
        # Get the full module name dynamically
        main_module_name = main.__module__
        
        # Prepare mock video data for two URLs
        mock_videos_1 = [
            {'href': '/video-180058315_456239247', 'title': 'Test Video 1'},
            {'href': '/video-180058315_456239245', 'title': 'Test Video 2'}
        ]
        mock_videos_2 = [
            {'href': '/video-111751633_456239144', 'title': 'Test Video 3'},
            {'href': '/video-111751633_456239099', 'title': 'Test Video 4'}
        ]
        
        # Mocks for file saving and video extraction
        with patch(f'{main_module_name}.extract_video_links', side_effect=[mock_videos_1, mock_videos_2]), \
             patch(f'{main_module_name}.save_video_links_to_yaml') as mock_save_yaml, \
             patch('sys.argv', ['vkvideo', 'goodstuff', '--list']):
            
            # Call main function and verify return value is None
            result = main()
            self.assertIsNone(result, "Main function should return None when using --list")
        
        # Verify save_video_links_to_yaml was called with correct arguments
        mock_save_yaml.assert_called_once()
        
        # Get the argument passed to save_video_links_to_yaml
        saved_videos = mock_save_yaml.call_args[0][0]
        
        # Verify the content of saved videos
        self.assertEqual(len(saved_videos), 4, "Incorrect number of video links")
        
        # Check each video link
        expected_hrefs = [
            '/video-180058315_456239247', 
            '/video-180058315_456239245',
            '/video-111751633_456239144', 
            '/video-111751633_456239099'
        ]
        expected_titles = ['Test Video 1', 'Test Video 2', 'Test Video 3', 'Test Video 4']
        
        for i, video in enumerate(saved_videos):
            self.assertIn('title', video, f"Missing title in video link {i}")
            self.assertIn('href', video, f"Missing href in video link {i}")
            
            # Verify title matches mock data
            self.assertEqual(video['title'], expected_titles[i])
            self.assertEqual(video['href'], expected_hrefs[i])
    
    def test_goodstuff_command_without_list(self):
        """
        Test the goodstuff command without --list
        """
        # Get the full module name dynamically
        main_module_name = main.__module__
        
        # Prepare mock video data for two URLs
        mock_videos_1 = [
            {'href': '/video-180058315_456239247', 'title': 'Test Video 1'},
            {'href': '/video-180058315_456239245', 'title': 'Test Video 2'}
        ]
        mock_videos_2 = [
            {'href': '/video-111751633_456239144', 'title': 'Test Video 3'},
            {'href': '/video-111751633_456239099', 'title': 'Test Video 4'}
        ]

        # Combine mock videos
        mock_videos = mock_videos_1 + mock_videos_2

        # Capture logging with more detailed mocking
        with patch(f'{main_module_name}.extract_videos_from_urls', side_effect=lambda urls, headless: mock_videos), \
             patch('sys.argv', ['vkvideo', 'goodstuff']):
        
            # Call main function
            result = main()
    
        # Verify the result contains all videos
        self.assertEqual(len(result), 4, "Incorrect number of extracted video links")

    def test_no_arguments(self):
        """
        Test that when no arguments are specified, help information is displayed
        """
        import sys
        import io
        import importlib
        
        # Dynamically import the module to patch
        main_module = importlib.import_module('...app.main', package=__package__)
        
        # Temporarily capture stderr
        original_stderr = sys.stderr
        sys.stderr = captured_stderr = io.StringIO()
        
        # Temporarily replace sys.argv
        original_argv = sys.argv
        sys.argv = ['vkvideo']
        
        try:
            # Call main with no arguments
            result = main_module.main()
            
            # Check that result is None
            self.assertIsNone(result)
            
            # Check that help information was printed to stderr
            stderr_output = captured_stderr.getvalue()
            
            # Verify key help text is present
            help_texts = [
                'VK Video Link Downloader',
                'usage:',
                'goodstuff',
                'url',
                'Examples:'
            ]
            
            for text in help_texts:
                self.assertIn(text, stderr_output, f"Help text '{text}' not found in stderr output")
        
        finally:
            # Restore original stderr and argv
            sys.stderr = original_stderr
            sys.argv = original_argv

if __name__ == '__main__':
    unittest.main()
