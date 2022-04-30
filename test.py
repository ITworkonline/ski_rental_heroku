from app.models import User, Ski
from app import app, bcrypt, db
import unittest
from pymock import PyMock

class FlaskTest(unittest.TestCase):
    def test_index(self):
        """
        GIVEN a route page /about
        WHEN checked
        THEN return 200 status
        """
        tester = app.test_client(self)
        response = tester.get("/about")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_user_models(self):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the username, email fields are defined correctly
        """
        user = User(username="test-user", email="test-user@gmail.com", password="test-password")
        self.assertEqual(user.username, "test-user")
        self.assertEqual(user.email, "test-user@gmail.com")

    def test_ski_models(self):
        """
        GIVEN a Ski model
        WHEN a new Ski is created
        THEN check the ski_brand, ski_type, price, and availability fields are defined correctly
        """
        ski = Ski(ski_brand="test-brand-1", ski_type="test-type-1", price=20, availability='Yes')
        self.assertEqual(ski.ski_brand, "test-brand-1")
        self.assertEqual(ski.ski_type, "test-type-1")
        self.assertEqual(ski.price, 20)
        self.assertEqual(ski.availability, "Yes")


class MockTest(unittest.TestCase):
    def mock_user(self):
        user = PyMock.create(User)
        PyMock.setup(user.email).returns(User.email)
        self.assertEqual(user.email, User.email)

    def mock_ski(self):
        ski = PyMock.create(Ski)
        PyMock.setup(ski.ski_brand).returns(Ski.ski_brand)
        self.assertEqual(ski.ski_brand, Ski.ski_brand)

if __name__ == "__main__":
    unittest.main()
