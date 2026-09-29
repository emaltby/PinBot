import unittest
import os
from unittest.mock import patch, MagicMock
from main import job
import config

class TestMainLoop(unittest.TestCase):
    def setUp(self):
        os.environ["TESTING"] = "true"

    @patch('main.scrape_facebook')
    @patch('main.send_email')
    @patch('main.is_new_listing')
    @patch('main.add_listing')
    def test_job_processing(self, mock_add, mock_is_new, mock_send, mock_scrape_fb):
        # Setup: Mock a new listing with a typo/variation for Facebook
        mock_scrape_fb.return_value = [{
            'title': 'Medievall Madness Pinball Machine',
            'url': 'http://fb.com/item/1',
            'hash': 'h1',
            'price': 500.0
        }]
        
        mock_is_new.return_value = True
        
        job()
        
        mock_send.assert_called()
        mock_add.assert_any_call('Facebook (Query 1)', 'h1', 'Medievall Madness Pinball Machine', 'http://fb.com/item/1', emailed=True)

if __name__ == '__main__':
    unittest.main()
