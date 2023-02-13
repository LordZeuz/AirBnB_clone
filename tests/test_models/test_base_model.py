#!/usr/bin/python3
'''unittest for ``BaseModel`` '''

import uuid
from datetime import datetime
from unittest import TestCase
from models.base_model import BaseModel


class BaseModelTestCase(TestCase):
    '''TestCase for BaseModel'''

    def setUp(self):
        self.base = BaseModel()

    def test_init_works(self):
        self.assertIsNotNone(self.base)

    def test_init_works_with_kwargs(self):
        '''checks that instance can be loaded from kwargs'''
        b = self.base
        d = b.to_dict()
        loaded = BaseModel(**d)
        self.assertDictEqual(b._dict, loaded.dict_)

    def test_id_is_string(self):
        '''checks that id is correctly casted to string'''
        self.assertIsInstance(self.base.id, str)

    def test_id_is_unique(self):
        '''checks that each instance have a unique id'''
        a = BaseModel()
        b = BaseModel()
        self.assertNotEqual(a.id, b.id)
        self.assertNotEqual(a.id, self.base.id)
        self.assertNotEqual(b.id, self.base.id)

    def test_id_is_valid_uuid_in_string(self):
        '''checks that ``id`` is casted from uuid4'''
        try:
            valid = uuid.UUID(self.base.id, version=4)
        except ValueError:
            self.fail("invalid uuid string")

        self.assertIsInstance(valid, uuid.UUID)

    def test_create_at_is_valid_datetime(self):
        '''checks that created_at is a valid datetime'''
        self.assertIsInstance(self.base.created_at, datetime)

    def test_updated_at_is_valid_datetime(self):
        '''checks that updated_at is a valid datetime'''
        self.assertIsInstance(self.base.updated_at, datetime)

    def test_dates_are_correctly_initialized(self):
        '''checks that updated_at is correctly set to creeated_at'''
        b = self.base
        self.assertEqual(b.created_at, b.updated_at)
        self.assertGreater(datetime.now(), b.created_at)

    def test_str_returns_expected(self):
        '''checks that str method formats as expected'''
        b = self.base
        self.assertEqual(
            str(b),
            "[{}] ({}) {}".format(
                b._class.name_,
                b.id,
                b._dict_
             )
        )

    def test_save_works(self):
        '''checks that `save` updates correctly'''
        b = self.base
        then = b.updated_at
        b.save()
        self.assertNotEqual(then, b.updated_at)

    def test_to_dict_works(self):
        '''checks that `to_dict` returns appropriate dict'''
        d = self.base.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(len(self.base._dict_) + 1, len(d))
        self.assertIn('_class_', d)

        # check that datetime variables are correctly casted
        self.assertEqual(
                d['created_at'],
                self.base.created_at.isoformat()
            )
