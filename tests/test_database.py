import unittest
import os
import sqlite3
import tempfile
from database import init_db, is_new_listing, add_listing
import config

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for the database
        self.test_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.test_dir.name, "test_listings.db")
        
        # Temporarily override DB_PATH in config
        self.old_db_path = config.DB_PATH
        config.DB_PATH = self.db_path
        init_db()

    def tearDown(self):
        # Restore old DB_PATH
        config.DB_PATH = self.old_db_path
        self.test_dir.cleanup()

    def test_deduplication(self):
        h = "test_hash"
        platform = "Test"
        self.assertTrue(is_new_listing(platform, h))
        add_listing(platform, h, "Test Title", "http://test.com")
        self.assertFalse(is_new_listing(platform, h))

if __name__ == '__main__':
    unittest.main()
