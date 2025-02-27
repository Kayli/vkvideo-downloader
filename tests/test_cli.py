import os
import yaml
import unittest
from unittest.mock import patch, MagicMock, call
import tempfile
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import main, GOODSTUFF_VIDEOS, OUTPUT_YAML_FILE

class TestVKVideoCLI(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for output files
        self.test_dir = tempfile.mkdtemp()
        
        # Patch the output YAML file to use a temp file
        self.test_output_file = os.path.join(self.test_dir, 'test_video_links.yml')
        
    def test_goodstuff_list_command(self):
        """
        Test the goodstuff --list functionality
        This test mocks the extract_video_links to return predefined data
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
        
        # Patch the extract_video_links function to return mock data
        with patch('main.extract_video_links', side_effect=[mock_videos_1, mock_videos_2]), \
             patch('main.OUTPUT_YAML_FILE', self.test_output_file), \
             patch('sys.argv', ['vkvideo', 'goodstuff', '--list']):
            
            # Call main function and verify return value is None
            result = main()
            self.assertIsNone(result, "Main function should return None when using --list")
        
        # Verify the YAML file was created
        self.assertTrue(os.path.exists(self.test_output_file), 
                        "YAML output file was not created")
        
        # Read and verify the YAML content
        with open(self.test_output_file, 'r', encoding='utf-8') as f:
            video_links = yaml.safe_load(f)
        
        # Verify the content of the YAML file
        self.assertEqual(len(video_links), 4, "Incorrect number of video links")
        
        # Check each video link
        expected_hrefs = [
            '/video-180058315_456239247', 
            '/video-180058315_456239245',
            '/video-111751633_456239144', 
            '/video-111751633_456239099'
        ]
        expected_titles = ['Test Video 1', 'Test Video 2', 'Test Video 3', 'Test Video 4']
        
        for i, video in enumerate(video_links):
            self.assertIn('title', video, f"Missing title in video link {i}")
            self.assertIn('url', video, f"Missing URL in video link {i}")
            
            # Verify URL format
            self.assertTrue(video['url'].startswith('https://vkvideo.ru'), 
                            f"Invalid URL format: {video['url']}")
            
            # Verify title and URL match mock data
            self.assertEqual(video['title'], expected_titles[i])
            self.assertEqual(video['url'], f'https://vkvideo.ru{expected_hrefs[i]}')
    
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
            main()
        
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
