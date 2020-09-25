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


if __name__ == '__main__':
    unittest.main()
