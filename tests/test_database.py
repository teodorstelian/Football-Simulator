import unittest
import sqlite3
import os

import sys

sys.path.insert(0, os.path.abspath("../src"))

from src import settings


class TestFootballSimulator(unittest.TestCase):
    def setUp(self):
        # Create a temporary database for testing
        self.test_db = "test_db.sqlite"
        settings.COMPETITIONS_DB = self.test_db
        # Set up a database connection
        self.conn = sqlite3.connect(settings.COMPETITIONS_DB)

    def tearDown(self):
        # Remove the temporary database
        if os.path.exists(self.test_db):
            # Close the database connection
            self.conn.close()
            os.remove(self.test_db)

    # Add tests for methods - TBA


if __name__ == '__main__':
    unittest.main()