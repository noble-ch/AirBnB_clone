#!/usr/bin/python3
"""Test User Class - Comproving expectect outputs and documentation."""

from datetime import datetime
import models
import pep8
import inspect
import unittest
from unittest import mock
import time

Amenity = models.amenity.Amenity
mod_doc = models.amenity.__doc__


class TestDocs(unittest.TestCase):
    """Test documentation and style"""
    @classmethod
    def setUpClass(self):
        """Setup for dosctring"""
        user_i = inspect.getmembers(Amenity, inspect.isfunction)

    def testing_pep8(self):
        """Testing that models_user.py passes pep8 """

    def test_pep8_conformance_user(self):
        """testing pep8 in amenity.py"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

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
    @mock.patch('models.amenity')
    def test_instances(self, mock_storage):
        """Testing that object is correctly created"""
        instance = Amenity()
        self.assertIs(type(instance), Amenity)
        instance.name = "Holbies foravaaaa"
        instance.state_id = "111-222"

        expectec_attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "state_id": str,
            "name": str
        }
        # testing types and attr names
        for attr, types in expectec_attrs_types.items():
            with self.subTest(attr=attr, typ=types):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), types)
        self.assertEqual(instance.name, "Holbies foravaaaa")
        self.assertEqual(instance.state_id, "111-222")

    def test_datetime(self):
        """testing correct datetime assignation
        correct assignation of created_at and updated_at"""
        created_at = datetime.now()
        instance1 = Amenity()
        updated_at = datetime.now()
        self.assertEqual(created_at <= instance1.created_at
                         <= updated_at, True)
        time.sleep(1)
        created_at = datetime.now()
        instance2 = Amenity()
        updated_at = datetime.now()
        self.assertTrue(created_at <= instance2.created_at <= updated_at, True)
        self.assertEqual(instance1.created_at, instance1.created_at)
        self.assertEqual(instance2.updated_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """testing uuid"""
        instance1 = Amenity()
        instance2 = Amenity()
        for instance in [instance1, instance2]:
            tuuid = instance.id
            with self.subTest(uuid=tuuid):
                self.assertIs(type(tuuid), str)

    def test_dictionary(self):
        """testing to_dict correct funtionality"""
        """Testing that object is correctly created"""
        instance3 = Amenity()
        self.assertIs(type(instance3), Amenity)
        instance3.name = "Holbies foravaaaa"
        new_inst = instance3.to_dict()
        expectec_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "__class__"]
        self.assertCountEqual(new_inst.keys(), expectec_attrs)
        self.assertEqual(new_inst['__class__'], 'Amenity')
        self.assertEqual(new_inst['name'], 'Holbies foravaaaa')

    def test_str_method(self):
        """testing str method, checking output"""
        instance4 = Amenity()
        strr = "[Amenity] ({}) {}".format(instance4.id, instance4.__dict__)
        self.assertEqual(strr, str(instance4))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """test save method and if it updates
        "updated_at" calling storage.save"""
        instance4 = Amenity()
        created_at = instance4.created_at
        updated_at = instance4.updated_at
        instance4.save()
        new_created_at = instance4.created_at
        new_updated_at = instance4.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)
