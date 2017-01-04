import unittest
from flask import current_app
from app import create_app, db
from seed import LoadSeedData


class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # load seed data
        LoadSeedData()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])


if __name__ == "__main__":
    import unittest

    unittest.main()
