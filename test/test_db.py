#!usr/bin/env python

import unittest
from test_common import TestCommon
from database_connection.db_connection import List, Task


class TestTables(TestCommon):

    def test_check_list_exist(self):
        assert List.table_exists()

    def test_check_task_exist(self):
        assert Task.table_exists()


if __name__ == '__main__':
    unittest.main()
