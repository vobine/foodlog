"""Import data from a Google CSV."""

import argparse
import csv
from itertools import chain, islice
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

def chunks (iterable, size):
    """Split an iterable into bites of a fixed maximum size.
From http://stackoverflow.com/a/24527424/1150562 retrieved 8/6/2016."""
    iterator = iter (iterable)
    for first in iterator:
        yield chain ([first], islice (iterator, size-1))

def load (cFile, header=True, size=100):
    """Load chunks of rows from a CSV file.
Yields a series of [chunk number, chunk generator] pairs.
Each chunk generator yields at most SIZE rows."""
    with open (cFile, 'rt') as cc:
        reader = enumerate (csv.reader (cc))
        if header:
            # Ignore the first line, it's a header
            next (reader)

        for i, chunk in enumerate (chunks (reader, size)):
            yield i, chunk

def cvt (row):
    """Convert a CSV row to internal format."""
    timeStamp = dt.datetime.strptime (row[0], '%m/%d/%Y %H:%M:%S')
    quantity = unit = None             # By default; exceptions below

    # Convert the row-type from Google Forms to FoodLog
    try:
        cat = categories[row[1]]
    except KeyError:
        print ('Unknown row type {0:d}: "{1:s}"'.format (i, row[1]))
        return None

    # Special cases for column 2, the "what was it?"
    if cat == "H2O":
        # For water, it's usually a quantity in ounces
        try:
            quantity = int (row[2])
            unit = 'floz'
            row[2] = ''
        except ValueError:
            pass

    elif cat == None:
        # Weight quantities should be floating point
        try:
            quantity = float (row[2])
            unit = 'lb'
            row[2] = ''
        except ValueError:
            pass

    # The result: [timeStamp, type, quantity, unit, *notes]
    return [timeStamp, cat, quantity, unit,
            row[2].strip (), row[3].strip ()]

def store (row):
    """Store one converted row to DBMS."""
    if row[1]:
        # It's a regular event
        dbrow = flm.FoodLog (timestamp=row[0],
                             kind=flm.session.query (flm.Kind) \
                                  .filter_by (id=row[1]) \
                                  .one (),
                             quantity=row[2],
                             unit=row[3])
        # TBD: notes go here.
    else:
        # It's a weigh-in
        dbrow = flm.Weight (timestamp=row[0],
                            weight=row[2],
                            unit=row[3])
        # TBD: notes here.

    flm.session.add (dbrow)

def loadcsv (cfile, url, headers=True):
    """Do the deed: load, convert, and store events."""
    # Connect to database
    flm.init_db (url)

    # Open the import file
    for cn, cc in load (cfile, headers):
        # Load each chunk-o-rows
        for rn, rr in cc:
            # Convert and store each row
            store (cvt (rr))

        # That's a chunk, commit it.
        flm.session.commit ()

def main (argv):
    """CLI."""
    import collections as coll

if __name__ == '__main__':
    from sys import argv
    main (argv[1:])
