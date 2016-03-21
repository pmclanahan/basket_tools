#!/usr/bin/env python
from __future__ import unicode_literals, print_function

import sys
from uuid import uuid4


def get_uuid():
    return str(uuid4())


def get_uuids(volume=10):
    for i in range(0, volume):
        print(get_uuid())


if __name__ == '__main__':
    if len(sys.argv) == 2:
        volume = int(sys.argv[1])
    else:
        volume = 10

    get_uuids(volume)
