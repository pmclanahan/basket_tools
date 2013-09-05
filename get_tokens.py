#!/usr/bin/env python

import codecs
import csv
import locale
import os
import sys
from uuid import uuid4

import basket


SUPERTOKEN = os.getenv('SUPERTOKEN')

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)


def get_new_token():
    return str(uuid4())


def get_user(email):
    try:
        user_data = basket.debug_user(email, SUPERTOKEN)
    except basket.BasketException:
        user_data = None
    return user_data


def get_emails_from_file(filename):
    with codecs.open(filename, encoding='utf8') as f:
        for line in f:
            yield line.strip()


def any_missmatches(filename):
    with open(filename) as csvfile:
        rows = csv.reader(csvfile)
        print [row[0] for row in rows if row[3] != row[4]]


if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Please provide a file.'

    print 'Email,Token,In ET,In Basket'
    emailfile = sys.argv[1]
    for email in get_emails_from_file(emailfile):
        in_basket = False
        in_ET = False
        token = None
        user = get_user(email)
        if user:
            token = user['token']
            in_basket = user['in_basket']
            in_ET = bool(token)
            if not in_ET:
                token = get_new_token()
        else:
            token = get_new_token()

        print u'%s,%s,%s,%s'.decode('utf8') % (email, token, in_ET, in_basket)
        sys.stderr.write('.')
        sys.stderr.flush()
