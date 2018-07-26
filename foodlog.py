#! /usr/bin/env python3

################################################################
# Food Log:  a system for logging diet and lifestyle.
# Copyright (C) 2018  Hal Peterson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
################################################################

from foodlog import app
import argparse

def run (debug):
    app.run (debug=debug)

def main (argv):
    """CLI."""
    parser = argparse.ArgumentParser (
        'Foodlog: Simple Web-based log for diet and weight')
    parser.add_argument ('--debug', '-d',
                         action='store_true',
                         help='Run server in debug mode')

    args = parser.parse_args (argv)
    run (args.debug)

if __name__ == '__main__':
    from sys import argv
    main (argv[1:])
