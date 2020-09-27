#!usr/bin/env python

import unittest
from click.testing import CliRunner
from main import main
from test_common import TestCommon


class TestTables(TestCommon):

    def test_create_list(self):
        runner = CliRunner()
        result = runner.invoke(main, ['create-list', 'lista'], input='y')
        assert result.exit_code == 0
        assert 'Success' in result.output

    def test_create_list_same_name(self):
        runner = CliRunner()
        list_one = runner.invoke(main, ['create-list', 'lista'], input='y')
        assert list_one.exit_code == 0
        assert 'Success' in list_one.output
        list_two = runner.invoke(main, ['create-list', 'lista'], input='y')
        assert 'already has a list with this name' in list_two.output

    def test_delete_list(self):
        runner = CliRunner()
        result = runner.invoke(main, ['create-list', 'lista'], input='y')
        assert result.exit_code == 0
        assert 'Success' in result.output
        delete = runner.invoke(main, ['delete-list', 'lista'])
        assert delete.exit_code == 0
        assert 'deleted' in delete.output

    def test_delete_not_exist_list(self):
        runner = CliRunner()
        result = runner.invoke(main, ['create-list', 'lista'], input='y')
        assert result.exit_code == 0
        assert 'Success' in result.output
        delete = runner.invoke(main, ['delete-list', 'lista2'])
        assert delete.exit_code == 0
        assert 'This list does not exist' in delete.output


if __name__ == '__main__':
    unittest.main()
