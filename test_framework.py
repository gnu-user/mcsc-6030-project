#!/usr/bin/env python2
###############################################################################
#
# The test framework for executing the test plan to test the various
# implementations of matrix operations.
#
# Copyright (C) 2015, Jonathan Gillett
# All rights reserved.
#
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import yaml
from math import ceil, floor
from os import path, popen
from docopt import docopt
from schema import Schema, Or, And, Use, SchemaError
from clint.textui import puts, progress, colored, indent, columns


usage = """Test Framework

Usage:
  test_framework.py [-v | --verbose] --code=<dir> TEST_PLAN
  test_framework.py -h | --help

  Executes the test plan and evaluates the code in the directory.

Arguments:
  TEST_PLAN     The test plan YAML document.

Options:
  -h, --help     Show this screen and exit.
  -v, --verbose  Increased verbosity, display more information.
  ---code=<dir>  The directory containing the code to execute.

"""

schema = Schema({
    '--code': And(path.exists, error='Code directory does not exist.'),
    'TEST_PLAN': And(path.exists, error='Test plan does not exist.'),
    '--help': Or(None, Use(bool)),
    '--verbose': Or(None, Use(bool))
})


class PrettyPrint(object):
    """Prints the text for the test framework to the screen prettily."""
    _col2 = 15  # Default width for second column

    def __init__(self, verbose=False, col1=None, col2=None):
        """Initializes object, optionally can set widths of columns."""
        self.verbose = verbose
        self.rows, self.cols = map(int, popen('stty size', 'r').read().split())
        self.col1 = self.cols - 15 if col1 is None else col1
        self.col2 = self._col2 if col2 is None else col2

    def print_summary(self, test_plan):
        """Print the summary of the test plan."""
        if self.verbose:
            puts(colored.cyan('Description:'))
            with indent(4):
                puts(columns([test_plan['description'], self.col1]))

        puts(colored.cyan('Codes:'))
        with indent(4):
            for code in test_plan['codes']:
                puts(code['name'])
        puts()

        puts(colored.cyan('Tests:'))
        with indent(4):
            for test in test_plan['tests']:
                puts(test['name'])
        puts()

    def print_title(self, title, symbol="-"):
        """Displays the title/heading for each section."""
        lpad = int(floor((self.col1 - len(title) - len(' Test Plan')) / 2)) - 1
        rpad = int(floor((self.col1 - len(title) - len(' Test Plan')) / 2)) - 1
        puts(symbol * self.col1)
        puts(symbol + ' ' * lpad + title + ' Test Plan' + ' ' * rpad + symbol)
        puts(symbol * self.col1 + '\n')

if __name__ == '__main__':
    args = docopt(usage)
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    # Load the test plan
    test_plan = None
    try:
        with open(args['TEST_PLAN'], 'r') as stream:
            test_plan = yaml.load(stream)
    except Exception as e:
        print "Error parsing test plan!"
        exit(e)

    pretty = PrettyPrint(verbose=True)
    pretty.print_title('Derpy mcDerp', symbol="=")
    pretty.print_summary(test_plan)
