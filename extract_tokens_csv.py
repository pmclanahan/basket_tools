#!/usr/bin/env python

"""
A quick script to get tokens from a CSV file.
"""

import codecs
import csv
import sys


def get_tokens(filename):
    count = 0
    with codecs.open(filename, 'r', 'utf8') as csvf:
        rows = csv.reader(csvf)
        for row in rows:
            if row[1] != 'TOKEN' and row[0] == 'test@example.com':
                sys.stdout.write('%s\n' % row[1])
                sys.stdout.flush()
                sys.stderr.write('.')
                sys.stderr.flush()
                count += 1
    sys.stderr.write('Total: %s' % count)


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Please provide a csv file.'
    get_tokens(sys.argv[1])
    exit(0)
