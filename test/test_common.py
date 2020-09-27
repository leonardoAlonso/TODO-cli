#!usr/bin/env python

import unittest
import peewee

from database_connection.db_connection import List, Task

MODELS = [List, Task]

test_db = peewee.SqliteDatabase(':memory:')


class TestCommon(unittest.TestCase):

    def setUp(self):
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()
        test_db.create_tables(MODELS)
