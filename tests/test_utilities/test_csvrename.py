#!/usr/bin/env python

import sys

import agate
import six

try:
    import unittest2 as unittest
    from mock import patch
except ImportError:
    import unittest
    from unittest.mock import patch

from csvkit.utilities.csvrename import CSVRename, launch_new_instance


class TestCSVStack(unittest.TestCase):

    def test_launch_new_instance(self):
        with patch.object(sys, 'argv', ['csvrename', 'examples/dummy.csv']):
            launch_new_instance()

    def test_rename_everything(self):
        args = ['-n','b,d,e', 'examples/dummy.csv']

        output_file = six.StringIO()
        utility = CSVRename(args, output_file)

        utility.main()

        input_file = six.StringIO(output_file.getvalue())
        reader = agate.reader(input_file)

        self.assertEqual(next(reader), ['b', 'd', 'e'])

    def test_wrong_number_of_names(self):
        args = ['-n','b,d', 'examples/dummy.csv']

        output_file = six.StringIO()
        utility = CSVRename(args, output_file)

        utility.main()

        input_file = six.StringIO(output_file.getvalue())
        reader = agate.reader(input_file)

        self.assertEqual(next(reader), ['a', 'b', 'c'])

    def test_rename_specific_columns(self):
        args = ['-n','b', '-c', 'a', 'examples/dummy.csv']

        output_file = six.StringIO()
        utility = CSVRename(args, output_file)

        utility.main()

        input_file = six.StringIO(output_file.getvalue())
        reader = agate.reader(input_file)

        self.assertEqual(next(reader), ['b', 'b', 'c'])

    def test_rename_multiple_specific_columns(self):
        args = ['-n','b,d', '-c', 'a,c', 'examples/dummy.csv']

        output_file = six.StringIO()
        utility = CSVRename(args, output_file)

        utility.main()

        input_file = six.StringIO(output_file.getvalue())
        reader = agate.reader(input_file)

        self.assertEqual(next(reader), ['b', 'b', 'd'])

