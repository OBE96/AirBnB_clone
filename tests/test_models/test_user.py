#!/usr/bin/env python3
#!/usr/bin/python3
"""Unit testing module for the user class
comprising Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""

import unittest
import os
from models import storage
from models.user import User
from models.base_model import BaseModel
from datetime import datetime
from time import sleep
import uuid

class TestUser_instantiation(unittest.TestCase):
    """Test scenario for the user model class"""

    @classmethod
    def setUpClass(cls):
        """Configure the unittestt"""
        cls.user = User()
        cls.user.email = "me@example.com"
        cls.user.password = "123i123"
        cls.user.first_name = "John"
        cls.user.last_name = "Swag"

    def test_for_instantiation(self):
        """Examines the instantiation of the User class."""
        user = User()
        self.assertEqual(str(type(user)), "<class 'models.user.User'>")
        self.assertIsInstance(user, User)
        self.assertTrue(issubclass(type(user), BaseModel))

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_has_attributes(self):
        self.assertTrue('id' in self.user.__dict__)
        self.assertTrue('created_at' in self.user.__dict__)
        self.assertTrue('updated_at' in self.user.__dict__)
        self.assertTrue('email' in self.user.__dict__)
        self.assertTrue('password' in self.user.__dict__)
        self.assertTrue('first_name' in self.user.__dict__)
        self.assertTrue('last_name' in self.user.__dict__)

    def test_attributes_are_string(self):
        self.assertIs(type(self.user.email), str)
        self.assertIs(type(self.user.password), str)
        self.assertIs(type(self.user.first_name), str)
        self.assertIs(type(self.user.last_name), str)

    def test_is_subclass(self):
        """Verify that User is a derived class of BaseModel."""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))

    def test_email_attr(self):
        """Check whether the User class has the attribute "email," 
        and if so, ensure it is initialized as an empty string"""
        user = User()
        self.assertTrue(hasattr(user, "email"))
        self.assertEqual(user.email, "")

    def test_password_attr(self):
        """Examine whether the User class possesses the attribute "password" 
        and confirm that it is initialized as an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "password"))
        self.assertEqual(user.password, "")

    def test_first_name_attr(self):
        """Verify that the User class includes the attribute "first_name," 
        and validate that it is initialized as an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "first_name"))
        self.assertEqual(user.first_name, "")

    def test_last_name_attr(self):
        """Verify that the User class includes the attribute "last_name,"
          and validate that it is initialized as an empty string."""
        user = User()
        self.assertTrue(hasattr(user, "last_name"))
        self.assertEqual(user.last_name, "")

    def test_str(self):
        """Verify that the str method produces the accurate output."""
        user = User()
        string = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(string, str(user))

    def test_is_subclass(self):
        self.assertTrue(issubclass(self.user.__class__, BaseModel))

    def checking_for_doc(self):
        self.assertIsNotNone(User.__doc__)

    def test_save(self):
        self.user.save()
        self.assertNotEqual(self.user.created_at, self.user.updated_at)

    def test_to_dict(self):
        self.assertTrue('to_dict' in dir(self.user))

    def test_to_dict_creates_dict(self):
        """Check that the to_dict method generates a dictionary with appropriate attributes."""
        u = User()
        new_d = u.to_dict()
        self.assertEqual(type(new_d), dict)
        for attr in u.__dict__:
            self.assertTrue(attr in new_d)
            self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Verify that the values in the dictionary returned by the to_dict method are accurate."""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        u = User()
        new_d = u.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], u.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], u.updated_at.strftime(t_format))


if __name__ == "__main__":
    unittest.main()
    