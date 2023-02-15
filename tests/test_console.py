#!/usr/bin/python3
'''Unittest for Console'''

from models import storage
from models.base_model import BaseModel
from unittest import TestCase
from unittest.mock import patch
from console import HBNBCommand
from io import StringIO


class TestConsole(TestCase):
    '''Tests basic funtioning of the Console'''
    def setUp(self):
        self.con = HBNBCommand()

    def test_quit(self):
        '''Tests if quit works as expected'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            self.assertEqual(f.getvalue().strip(), "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
            self.assertEqual(f.getvalue().strip(), "")

    def test_help(self):
        ''''Test help works'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertIn("help", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("?")
            self.assertIn("help", f.getvalue())

    def test_prompt(self):
        '''Test prompt is as specified'''
        self.assertEqual("(hbnb)", self.con.prompt.strip())

    def test_emptyline(self):
        '''Test emptyline works'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("  ")
            self.assertEqual(f.getvalue().strip(), "")


class TestCmdError_name(TestCase):
    '''Test Correct Error functioning for all cmds'''
    def setUp(self):
        self.name = "** class doesn't exist **"
        self.no_nm = "** class name missing **"
        self.id = "** no instance found **"
        self.no_id = "** instance id missing **"

    def test_no_name(self):
        '''Correct err msg for no name'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            HBNBCommand().onecmd("destroy")
            HBNBCommand().onecmd("show")
            for i in f.getvalue().split("\n"):
                if len(i) > 1:
                    self.assertEqual(self.id, i)

    def test_invalid_name_create(self):
        '''Test invalid name as inpot'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Mod")
            self.assertEqual(self.name, f.getvalue().strip())

    def test_invalid_name_show(self):
        '''Test invalid name as inpot'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show Mod")
            self.assertEqual(self.name, f.getvalue().strip())

    def test_invalid_name_update(self):
        '''Test invalid name as inpot'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update Mod")
            self.assertEqual(self.name, f.getvalue().strip())

    def test_invalid_name_destroy(self):
        '''Test invalid name as inpot'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Mod")
            self.assertEqual(self.name, f.getvalue().strip())

    def test_invalid_name_create(self):
        '''Test invalid name as inpot'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Mod")
            self.assertEqual(self.name, f.getvalue().strip())

    def test_no_name(self):
        '''Correct err msg for no name'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            self.assertEqual(self.no_nm, f.getvalue().strip())

    def test_invalid_id(self):
        '''Tests invalid id'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 121212")
            HBNBCommand().onecmd("destroy BaseModel 121212")
            HBNBCommand().onecmd("update BaseModel 121212")
#        for default cmds
            HBNBCommand().onecmd('User.show("246c227a2")')
            HBNBCommand().onecmd('User.destroy("246c227a2")')
            HBNBCommand().onecmd('User.update("246c227a2", "first\
                                 _nm", "John")')
            for i in f.getvalue().split("\n"):
                if len(i) > 1:
                    self.assertEqual(self.id, i)


class TestHelpCmds(TestCase):
    '''Tests correct functioning of Create Command'''
    def test_create_help(self):
        '''Test help works on create cmd'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")


class TestConsoleCmdSpace(TestCase):
    '''Test working of show command in all cases for space notation'''
    def setUp(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            self.b_id = f.getvalue().strip()

    def test_create(self):
        '''Test create from setup works'''
        self.assertEqual(36, len(self.b_id))

    def test_show_destroy(self):
        '''Test proper functioning of show using user'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show BaseModel {self.b_id}")
            self.assertIn("BaseModel", f.getvalue())
            HBNBCommand().onecmd(f"destroy BaseModel {self.b_id}")
            HBNBCommand().onecmd(f"show BaseModel {self.b_id}")
            output = f.getvalue().split("\n")
            self.assertEqual(output[1], "** no instance found **")

    def test_update(self):
        '''Test update for space notation'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {self.b_id}  attr_name\
                                 "attr_value"')
            test_dict = storage.all()["BaseModel.{}".format(self.b_id)].\
                __dict__
            self.assertEqual("attr_value", test_dict["attr_name"])

    def test_all(self):
        '''Test all cmd'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            self.assertIsInstance(list(f.getvalue()), list)

    def test_all_base(self):
        '''Test all cmd'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all BaseModel")
            self.assertIn("[BaseModel", f.getvalue())


class TestConsoleDefault(TestCase):
    '''Test default method works'''
    def setUp(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            self.b_id = f.getvalue().strip()

    def test_all(self):
        '''TEst all cmd via default option'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.all()")
            self.assertIsInstance(list(f.getvalue()), list)

    def test_count(self):
        '''Test count cmd'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("User.count()")
            self.assertIsInstance(int(f.getvalue()), int)

    def test_show(self):
        '''Test show works via default cmd option'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'User.show({self.b_id})')
            self.assertIn("[User]", f.getvalue())

    def test_update(self):
        '''Test update cmd via default option'''
        with patch('sys.stdout', new=StringIO()) as f:
            testCmd = "User.update({}, attr_name, attr_value)".\
                      format(self.b_id)
            HBNBCommand().onecmd(testCmd)
            test_dict = storage.all()["User.{}".format(self.b_id)].__dict__
            self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_from_dic(self):
        '''Tests update from dictionary'''
        with patch('sys.stdout', new=StringIO()) as f:
            testCmd = "User.update({}, ".format(self.b_id) +\
                      "{'attr_name': 'attr_value'})"
            HBNBCommand().onecmd(testCmd)
            test_dict = storage.all()["User.{}".format(self.b_id)].__dict__
            self.assertEqual("attr_value", test_dict["attr_name"])
