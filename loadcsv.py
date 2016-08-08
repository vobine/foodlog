"""Import data from a Google CSV."""

import argparse
import csv
from itertools import chain, islice
import datetime as dt
import foodlog.models as flm
from sqlalchemy import func

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
    quantity = dimension = None # By default; exceptions below

    # Convert the row-type from Google Forms to FoodLog
    try:
        cat = categories[row[1]]
    except KeyError:
        print ('Unknown row type {0:d}: "{1:s}"'.format (i, row[1]))
        return None

    # Special cases for column 2, the "what was it?"
    if cat == 'H2O':
        # For water, it's usually a quantity in ounces. Convert to liters.
        try:
            quantity = float (row[2]) / 33.814022701843
            dimension = 'volume'
            row[2] = ''
        except ValueError:
            pass

    elif cat == None:
        # Weight quantities in pounds. Convert to grams
        try:
            quantity = float (row[2]) / 0.002204622621848776
            dimension = 'weight'
            row[2] = ''
        except ValueError:
            pass

    # The result: [timeStamp, type, quantity, dimension, *notes]
    return [timeStamp, cat, quantity, dimension,
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
                             dimension=row[3])
        # TBD: notes go here.
    else:
        # It's a weigh-in
        dbrow = flm.Weight (timestamp=row[0],
                            weight=row[2])
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

    # Summarize results
    print ('Loaded {0:d} rows in {1:d} chunks:'.format (rn, cn))

    for n, l in flm.session.query (func.count ('*'),
                                   flm.FoodLog) \
        .group_by (flm.FoodLog.kind_id) \
        .order_by (flm.FoodLog.kind_id) \
        .all ():
        print ('    {0:4s} {1:5d}'.format (l.kind_id, n))

def main (argv):
    """CLI."""

    # Declare command line
    parser = argparse.ArgumentParser (
        'loadcsv: Load FoodLog database from Google Forms CSV.')
    parser.add_argument ('--debug', '-d',
                         action='store_true',
                         help='More console output than you want to read')
    parser.add_argument ('--quiet', '-q',
                         action='store_true',
                         help='Suppress console output unless fail')
    parser.add_argument ('--headless',
                         help='CSV file has no header row')
    parser.add_argument ('infile',
                         action='store',
                         help='CSV file to import')
    parser.add_argument ('dbms',
                         action='store',
                         help='URL for database')

    # Parse command line
    args = parser.parse_args (argv)

    # Run
    loadcsv (args.infile, args.dbms, headers=not args.headless)

if __name__ == '__main__':
    from sys import argv
    main (argv[1:])
