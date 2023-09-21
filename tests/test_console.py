#!/usr/bin/python3
"""
Defines tests for command interpreter
"""
import unittest
from unittest.mock import patch
from io import StringIO
import pep8
import os
import console
import sys
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
# from models import storage
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

db = os.getenv("HBNB_TYPE_STORAGE")


class TestConsole(unittest.TestCase):

    """
    Unittest module for command interpreter
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up test class before any test
        """
        cls.command = HBNBCommand()
        cls.storage = DBStorage()

    @classmethod
    def tearDownClass(cls):
        """
        Clear the test class before next tests
        """
        if db != 'db':
            if os.path.exists("file.json"):
                os.remove("file.json")

    def setUp(self):
        '''setup before each test '''
        self.backup = sys.stdout
        self.output = StringIO()
        sys.stdout = self.output
        if db == 'db':
            self.storage.reload()
        else:
            if os.path.exists("file.json"):
                os.remove("file.json")

    def tearDown(self):
        ''''''
        sys.stdout = self.backup

    def test_console_methods(self):
        """ check class methods exist """
        self.assertTrue(hasattr(self.command, "do_all"))
        self.assertTrue(hasattr(self.command, "do_EOF"))
        self.assertTrue(hasattr(self.command, "do_quit"))
        self.assertTrue(hasattr(self.command, "do_create"))
        self.assertTrue(hasattr(self.command, "do_show"))
        self.assertTrue(hasattr(self.command, "do_destroy"))
        self.assertTrue(hasattr(self.command, "do_update"))

    def test_documentation_console(self):
        """
        Test module documentation
        """
        self.assertGreater(len(console.__doc__), 3)
        self.assertGreater(len(HBNBCommand.__doc__), 3)
        self.assertGreater(len(self.__doc__), 3)

    def test_pep8_console(self):
        """
        Pep8 compliance in console.py
        """
        style = pep8.StyleGuide(quiet=False)
        errors = 0
        file = (["console.py"])
        errors += style.check_files(file).total_errors
        self.assertEqual(errors, 0, 'Need to fix Pep8')

    def test_pep8_test_console(self):
        """
        Pep8 compliance in test_console.py
        """
        style = pep8.StyleGuide(quiet=False)
        errors = 0
        file = (["tests/test_console.py"])
        errors += style.check_files(file).total_errors
        self.assertEqual(errors, 0, 'Need to fix Pep8')

    @unittest.skipIf(db == "db", "Testing file storage only")
    def test_file_show(self):
        '''
            Testing that show exists
        '''
        self.command.onecmd(
            'create User first_name="Peter" email="user@gmail.com" \
            password="user1234'
        )
        # capture the ID of user from stdout
        user_id = self.output.getvalue().strip()
        # reset the output and close the capture
        sys.stdout = self.backup
        self.output.close()
        print("test_show user.id: ", user_id)
        # create a new instance of capture
        self.output = StringIO()
        sys.stdout = self.output
        # issue a console command
        self.command.onecmd("all User")
        # capture the new output and create a dictionary
        user_dict = self.output.getvalue().strip()
        sys.stdout = self.backup
        self.output.close()
        self.assertTrue("[User]" in user_dict)

    # @unittest.skipIf(db != 'db', "Testing DBstorage only")
    # def test_db_show(self):
    #     self.storage.reload()
    #     self.command.onecmd(
    #         'create User first_name="Peter" email="user@gmail.com" \
    #         password="user1234'
    #     )
    #     result = self.storage.all("User")
    #     self.assertTrue(len(result) > 0)

    def test_emptyline(self):
        """Test emptyline command"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.command.onecmd("\n")
            self.assertEqual(fake_output.getvalue(), '')

    def test_create(self):
        """Test create command"""
        self.command.onecmd(
            'create User first_name="Peter" email="user@gmail.com" \
            password="user1234'
        )
        # capture the ID of user from stdout
        user_id = self.output.getvalue()
        # reset the output and close the capture
        sys.stdout = self.backup
        self.output.close()
        self.assertIsInstance(user_id, str)

    def test_create_invalid(self):
        """ Tests invalid cases of command create """
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.command.onecmd("create")
            self.assertEqual("** class name missing **\n",
                             fake_output.getvalue())

        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.command.onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **\n",
                             fake_output.getvalue())

    @unittest.skipIf(db == "db", "Testing file storage only")
    def test_file_all(self):
        ''' Test all exists'''
        self.command.onecmd("all")
        self.assertTrue(isinstance(self.output.getvalue(), str))

        self.command.onecmd(
            'create User first_name="Peter" email="user@gmail.com" \
            password="user1234'
        )
        # capture the ID of user from stdout
        user_id = self.output.getvalue()
        # reset the output and close the capture
        sys.stdout = self.backup
        self.output.close()
        self.assertIsInstance(user_id, str)

        # create a new instance of capture
        self.output = StringIO()
        sys.stdout = self.output
        # issue a console command
        self.command.onecmd("all User")
        # capture the new output and create a dictionary
        user_dict = (self.output.getvalue())
        sys.stdout = self.backup
        self.assertTrue("[User]" in user_dict)

    # @unittest.skipIf(db != 'db', "Testing DBstorage only")
    # def test_db_all(self):
    #     self.command.onecmd(
    #         'create User first_name="Peter" email="user@gmail.com" \
    #         password="user1234'
    #     )
    #     result = storage.all("User")
    #     self.assertTrue(len(result) > 0)

    # def test_all_invalid(self):
    #     """Test all command"""
        # with patch('sys.stdout', new=StringIO()) as fake_output:
        #     self.command.onecmd("all MyModel")
        #     self.assertEqual("** class doesn't exist **\n",
        #                      fake_output.getvalue())

        # with patch('sys.stdout', new=StringIO()) as fake_output:
        #     self.command.onecmd("all City")
        #     self.assertEqual("[]\n", fake_output.getvalue())

    @unittest.skipIf(db == "db", "Testing file storage only")
    def test_file_destroy(self):
        """ Test destroy command """
        self.command.onecmd('create State name="California"')
        # capture the ID of user from stdout
        user_id = self.output.getvalue()
        # reset the output and close the capture
        sys.stdout = self.backup
        self.output.close()

        # create a new instance of capture
        self.output = StringIO()
        sys.stdout = self.output
        # issue a console command
        self.command.onecmd("all State")
        # capture the new output and create a dictionary
        user_dict = (self.output.getvalue())
        sys.stdout = self.backup
        self.assertTrue("[State]" in user_dict)

        # destroy object and confirm
        sys.stdout = self.backup
        self.output.close()
        self.output = StringIO()
        sys.stdout = self.output
        self.command.onecmd("destroy State {}".format(user_id))
        self.command.onecmd("all State")
        user_dict = (self.output.getvalue())
        sys.stdout = self.backup
        self.assertFalse("[State]" in user_dict)
        self.assertTrue(len(user_dict), 0)

    # def test_destroy_invalid(self):
    #     """Test destroy command"""
    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         self.command.onecmd("destroy")
    #         self.assertEqual("** class name missing **\n",
    #                          fake_output.getvalue())

    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         self.command.onecmd("destroy TheWorld")
    #         self.assertEqual("** class doesn't exist **\n",
    #                          fake_output.getvalue())

    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         self.command.onecmd("destroy BaseModel")
    #         self.assertEqual("** instance id missing **\n",
    #                          fake_output.getvalue())

    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         self.command.onecmd("destroy BaseModel 12345 12345")
    #         self.assertEqual("** no instance found **\n",
    #                          fake_output.getvalue())

    # def test_update(self):
    #     """Test update command"""
    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         self.command.onecmd("update")
    #         self.assertEqual("** class name missing **\n",
    #                          fake_output.getvalue())

    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         self.command.onecmd("update MyModel")
    #         self.assertEqual("** class doesn't exist **\n",
    #                          fake_output.getvalue())

    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         self.command.onecmd("update User")
    #         self.assertEqual("** instance id missing **\n",
    #                          fake_output.getvalue())

    #     with patch('sys.stdout', new=StringIO()) as fake_output:
    #         self.command.onecmd("update BaseModel 12345")
    #         self.assertEqual("** no instance found **\n",
    #                          fake_output.getvalue())

    def test_show_invalid(self):
        """Test show command"""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.command.onecmd("show")
            self.assertEqual("** class name missing **\n",
                             fake_output.getvalue())

        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.command.onecmd("show BaseModel")
            self.assertEqual("** instance id missing **\n",
                             fake_output.getvalue())


if __name__ == "__main__":
    unittest.main()
