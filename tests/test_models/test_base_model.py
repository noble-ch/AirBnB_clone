#!/usr/bin/python3
"""Test BaseModel- Comproving expectect outputs and documentation."""
from datetime import datetime
import time
import unittest
# from pep8 import pycodestyle
import models
import inspect
from unittest import mock

BaseModel = models.base_model.BaseModel
mod_doc = models.base_model.__doc__


class TestDocs(unittest.TestCase):
    """Test documentation and style"""
    @classmethod
    def setUpClass(self):
        """Setup for dosctring"""
        self.base_f = inspect.getmembers(BaseModel, inspect.isfunction)

    # def testing_pep8(self):
    # """testing that BaseModel.py passes pep8"""
    # for path in ['models/base_model.py',
    # "tests/test_models/test_base_model.py"]:
    # with self.suptest(path=path):
    # err = pycodestyle.Checker(path).check_all()
    # self.assertEqual(err, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(mod_doc, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(mod_doc) > 1,
                        "base_model.py needs a docstring")

    def test_dosctring(self):
        """Testing documentation"""
        self.assertIsNot(mod_doc, None,
                         "base_model.py needs a doctring")
        self.assertTrue(len(mod_doc) > 1,
                        "base_model.py needs a docstring")


class TestBaseModel(unittest.TestCase):
    """testing BaseModel Class"""
    @mock.patch('models.storage')
    def test_instances(self, mock_storage):
        """Testing that object is correctly created"""
        instance = BaseModel()
        self.assertIs(type(instance), BaseModel)
        instance.name = "Holberton"
        instance.number = 89
        expectec_attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        # testing types and attr names
        for attr, types in expectec_attrs_types.items():
            with self.subTest(attr=attr, typ=types):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), types)
        self.assertTrue(mock_storage.new.called)
        self.assertEqual(instance.name, "Holberton")
        self.assertEqual(instance.number, 89)

    def test_datetime(self):
        """testing correct datetime assignation
        correct assignation of created_at and updated_at"""
        created_at = datetime.now()
        instance1 = BaseModel()
        updated_at = datetime.now()
        self.assertEqual(created_at <= instance1.created_at
                         <= updated_at, True)
        time.sleep(1)
        created_at = datetime.now()
        instance2 = BaseModel()
        updated_at = datetime.now()
        self.assertTrue(created_at <= instance2.created_at <= updated_at, True)
        self.assertEqual(instance1.created_at, instance1.created_at)
        self.assertEqual(instance2.updated_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """testing uuid"""
        instance1 = BaseModel()
        instance2 = BaseModel()
        for instance in [instance1, instance2]:
            tuuid = instance.id
            with self.subTest(uuid=tuuid):
                self.assertIs(type(tuuid), str)

        self.assertNotEqual(instance1.id, instance2.id)

    def test_dictionary(self):
        """testing to_dict correct funtionality"""
        instance3 = BaseModel()
        instance3.name = "Holbies"
        instance3.my_number = 89
        new_inst = instance3.to_dict()
        expectec_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(new_inst.keys(), expectec_attrs)
        self.assertEqual(new_inst['__class__'], 'BaseModel')
        self.assertEqual(new_inst['name'], 'Holbies')
        self.assertEqual(new_inst['my_number'], 89)

    def test_str_method(self):
        """testing str method, checking output"""
        instance4 = BaseModel()
        strr = "[BaseModel] ({}) {}".format(instance4.id, instance4.__dict__)
        self.assertEqual(strr, str(instance4))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """test save method and if it updates
        "updated_at" calling storage.save"""
        instance4 = BaseModel()
        created_at = instance4.created_at
        updated_at = instance4.updated_at
        instance4.save()
        new_created_at = instance4.created_at
        new_updated_at = instance4.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)
