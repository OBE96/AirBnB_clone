#!/usr/bin/python3
"""
Unittest for amenity.py
"""
import unittest
from models.amenity import Amenity
import datetime


class TestAmenity(unittest.TestCase):
    """Tests for instances and methods from amenity class"""

    a = Amenity()

    def test_class_exists(self):
        """tests if the class exists"""
        res = "<class 'models.amenity.Amenity'>"
        self.assertEqual(str(type(self.a)), res)

    def test_user_inheritance(self):
        """tests for Amenity as a subclass of BaseModel"""
        self.assertIsInstance(self.a, Amenity)

    def testHasAttributes(self):
        """verify if the attributes exist"""
        self.assertTrue(hasattr(self.a, 'name'))
        self.assertTrue(hasattr(self.a, 'id'))
        self.assertTrue(hasattr(self.a, 'created_at'))
        self.assertTrue(hasattr(self.a, 'updated_at'))

    def test_types(self):
        """test whether the attribute's type is the appropriate one."""
        self.assertIsInstance(self.a.name, str)
        self.assertIsInstance(self.a.id, str)
        self.assertIsInstance(self.a.created_at, datetime.datetime)
        self.assertIsInstance(self.a.updated_at, datetime.datetime)


if __name__ == '__main__':
    unittest.main()
