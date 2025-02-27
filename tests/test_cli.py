import os
import yaml
import unittest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import main, GOODSTUFF_VIDEOS, OUTPUT_YAML_FILE, save_video_links_to_yaml

class TestVKVideoCLI(unittest.TestCase):
    def test_goodstuff_list_command(self):
        """
        Test the goodstuff --list functionality
        This test mocks the extract_video_links and file saving
        """
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
        with patch('main.extract_video_links', side_effect=[mock_videos_1, mock_videos_2]), \
             patch('main.save_video_links_to_yaml') as mock_save_yaml, \
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
        # Prepare mock video data for two URLs
        mock_videos_1 = [
            {'href': '/video-180058315_456239247', 'title': 'Test Video 1'},
            {'href': '/video-180058315_456239245', 'title': 'Test Video 2'}
        ]
        mock_videos_2 = [
            {'href': '/video-111751633_456239144', 'title': 'Test Video 3'},
            {'href': '/video-111751633_456239099', 'title': 'Test Video 4'}
        ]
        
        # Capture stderr
        with patch('main.extract_video_links', side_effect=[mock_videos_1, mock_videos_2]), \
             patch('sys.argv', ['vkvideo', 'goodstuff']), \
             patch('sys.stderr', new_callable=MagicMock()) as mock_stderr:
            
            # Call main function
            result = main()
        
        # Verify the result contains all videos
        self.assertEqual(len(result), 4, "Incorrect number of extracted video links")
        
        # Verify stderr output
        mock_stderr.write.assert_called()
        
        # Get all stderr calls
        stderr_calls = mock_stderr.write.call_args_list
        
        # Convert calls to strings for easier inspection
        stderr_outputs = [str(call[0][0]) for call in stderr_calls]
        
        # Check for messages about processing URLs and extracted videos
        url_processing_messages = [
            msg for msg in stderr_outputs 
            if 'Processing URL:' in msg or 'Extracted' in msg
        ]
        
        # Verify we have messages about processing URLs and extracting videos
        self.assertTrue(url_processing_messages, 
                        "No URL processing or extraction messages found in stderr")
        
        # Verify total number of videos
        total_videos_message = [
            msg for msg in stderr_outputs 
            if 'Extracted 4 unique video links' in msg
        ]
        self.assertTrue(total_videos_message, 
                        "Did not find message about total number of extracted video links")

if __name__ == '__main__':
    unittest.main()
