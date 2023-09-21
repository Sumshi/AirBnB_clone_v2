#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel, unittest
from models.user import User
import os


class test_User(test_basemodel):
    """testing user class"""

    def __init__(self, *args, **kwargs):
        """innit method for the user class"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') ==
                     'db', "database storage not supported")
    def test_first_name(self):
        """testing user first name attribute"""
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """testing user last name attribute"""
        new = self.value()
        self.assertEqual(type(new.last_name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_email(self):
        """testing user email attribue"""
        new = self.value()
        self.assertEqual(type(new.email), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_password(self):
        """ testing user password attr"""
        new = self.value()
        self.assertEqual(type(new.password), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
