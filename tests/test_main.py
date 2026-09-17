import unittest
from unittest.mock import patch, MagicMock
from main import job
import config

class TestMainLoop(unittest.TestCase):
    @patch('main.scrape_facebook')
    @patch('main.send_email')
    @patch('main.is_new_listing')
    @patch('main.add_listing')
    def test_job_processing(self, mock_add, mock_is_new, mock_send, mock_scrape_fb):
        # Setup: Mock a new listing for Facebook
        mock_scrape_fb.return_value = [{'title': 'Pinball Machine', 'url': 'http://fb.com/item/1', 'hash': 'h1'}]
        
        mock_is_new.return_value = True
        
        job()
        
        mock_send.assert_called()
        mock_add.assert_called_with('Facebook', 'h1')

if __name__ == '__main__':
    unittest.main()
