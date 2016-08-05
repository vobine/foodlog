"""Import data from a Google CSV."""

import argparse
import csv
import datetime as dt
import foodlog.models as flm

categories = {
    'Exercise': 'Ex',
    'Fat': 'Fat',
    'Green': 'Grn',
    'Lean': 'Lean',
    'Lean and/or Green': 'L/G',
    'Medifast': 'MF',
    'Off plan': 'Off',
    'Supplement': 'Sup',
    'Water': 'H2O',
    'Weight': None,             # Weight is a different table.
}

def cvt (cFile, header=True):
    """Load rows from a CSV file, insert into table."""
    with open (cFile, 'rt') as cc:
        reader = enumerate (csv.reader (cc))
        if header:
            # Ignore the first line, it's a header
            next (reader)

        for i, row in reader:
            try:
                cat = categories[row[1]]
            except KeyError:
                print ('Unknown row type {0:d}: "{1:s}"'.format (i, row[1]))
                return
            else:
                yield (cat,
                       dt.datetime.strptime (row[0], '%m/%d/%Y %H:%M:%S'),
                       row[2])

def main (argv):
    """CLI."""
    import collections as coll
    coo = coll.Counter (_[0] for _ in cvt (argv[0]))
    for k, v in coo.items ():
        try:
            print ('{0:5s} {1:d}'.format (k, v))
        except TypeError:
            print ('Weight {0:d}'.format (v))

if __name__ == '__main__':
    from sys import argv
    main (argv[1:])
