# import json
from unittest import TestCase
from model import (connect_to_db, db, example_data)
from server import app
from seed import load_seeddata


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Needed for using sessions with Flask
        app.config['SECRET_KEY'] = 'key'

    def test_index(self):
        """Test homepage, not logged in."""

        result = self.client.get("/")
        self.assertIn("takes the work out of choosing", result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()

        # load seed data
        load_seeddata()

        # Create tables and add sample data
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

        with self.client as c:
            with c.session_transaction() as sess:
                del sess['user_id']

    def test_departments_list(self):
        """Test departments page."""

        result = self.client.get("/departments")
        self.assertIn("Legal", result.data)

    def test_departments_details(self):
        """Test departments page."""

        result = self.client.get("/department/fin")
        self.assertIn("Phone: 555-1000", result.data)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"user_id": "rachel", "password": "123"},
                                  follow_redirects=True)
        self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_important_page(self):
#         """Test important page."""

#         result = self.client.get("/important")
#         self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/important", follow_redirects=True)
#         self.assertNotIn("You are a valued user", result.data)
#         self.assertIn("You must be logged in", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
