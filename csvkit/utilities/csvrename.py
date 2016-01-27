#!/usr/bin/env python

"""
csvcut is originally the work of eminent hackers Joe Germuska and Aaron Bycoffe.

This code is forked from:
https://gist.github.com/561347/9846ebf8d0a69b06681da9255ffe3d3f59ec2c97

Used and modified with permission.
"""

import itertools

import agate

from csvkit.cli import CSVKitUtility, parse_column_identifiers
from csvkit.headers import make_default_headers


class CSVRename(CSVKitUtility):
    description = 'Filter and truncate CSV files. Like unix "cut" command, but for tabular data.'

    def add_arguments(self):
        self.argparser.add_argument('-n', '--names', dest='names',
                                    help='')
        self.argparser.add_argument('-c', '--columns', dest='columns',
                                    help='')

    def main(self):

        rows = agate.reader(self.input_file, **self.reader_kwargs)

        if self.args.no_header_row:
            row = next(rows)

            column_names = make_default_headers(len(row))

            # Put the row back on top
            rows = itertools.chain([row], rows)
        else:
            column_names = next(rows)

        output = agate.writer(self.output_file, **self.writer_kwargs)

        columns = None
        if self.args.names:
            new_column_names = self.args.names.split(',')
            if self.args.columns:
                old_column_names = self.args.columns.split(',')
                columns = dict(zip(old_column_names, new_column_names))
            else:
                if len(new_column_names) == len(column_names):
                    columns = dict(zip(column_names, new_column_names))


        if isinstance(columns, dict):
            column_names = [columns[name] if name in columns else name for name in column_names]

        output.writerow(column_names)

        for row in rows:
            output.writerow(row)


def launch_new_instance():
    utility = CSVRename()
    utility.main()

if __name__ == "__main__":
    launch_new_instance()
