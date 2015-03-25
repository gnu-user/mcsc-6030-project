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
from math import floor
from time import sleep
from random import random
from collections import OrderedDict
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
    _col2 = 16  # Default width for second column

    def __init__(self, verbose=False, col1=None, col2=None):
        """Initializes object, optionally can set widths of columns."""
        self.verbose = verbose
        self.rows, self.cols = map(int, popen('stty size', 'r').read().split())
        self.col1 = self.cols - self._col2 if col1 is None else col1
        self.col2 = self._col2 if col2 is None else col2

    def summary(self, test_plan):
        """Print the summary of the test plan."""
        if self.verbose:
            puts(colored.cyan('Description:'))
            with indent(4):
                puts(columns([test_plan['description'], self.col1]))

        puts(colored.cyan('Codes:'))
        if self.verbose:
            with indent(4):
                for code in test_plan['codes']:
                    puts(colored.magenta(code['name']))
                    with indent(4):
                        puts(columns([code['description'], self.col1]))
        else:
            with indent(4):
                for code in test_plan['codes']:
                    puts(code['name'])

        puts(colored.cyan('\nTests:'))
        if self.verbose:
            with indent(4):
                for test in test_plan['tests']:
                    puts(colored.magenta(test['name']))
                    with indent(4):
                        puts(columns([test['description'], self.col1]))
        else:
            with indent(4):
                for test in test_plan['tests']:
                    puts(test['name'])
        puts()

    def title(self, title):
        """Displays the main testplan heading."""
        lpad = int(floor((self.col1 - len(title) - len(' Test Plan')) / 2)) - 1
        rpad = self.col1 - len(title) - len(' Test Plan') - lpad - 2
        puts('=' * self.col1)
        puts('=' + ' ' * lpad + title + ' Test Plan' + ' ' * rpad + '=')
        puts('=' * self.col1)

    def heading(self, title):
        """Displays the heading for each test being executed."""
        lpad = int(floor((self.col1 - len(title) - len('Executing Test ')) / 2)) - 1
        rpad = self.col1 - len(title) - len('Executing Test ') - lpad - 2
        puts('-' * self.col1)
        puts('-' + ' ' * lpad + 'Executing ' + title + ' Test' + ' ' * rpad + '-')
        puts('-' * self.col1)

    def test_summary(self, test, trials):
        puts(colored.cyan('Trials: ') + str(trials))
        puts(colored.cyan('Dimensions: ') + str(test['dimensions']))
        if self.verbose:
            puts(colored.cyan('Description:'))
            with indent(4):
                puts(columns([test['description'], self.col1]))


if __name__ == '__main__':
    args = docopt(usage)
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    # Load the test plan
    testplan = None
    try:
        with open(args['TEST_PLAN'], 'r') as stream:
            testplan = yaml.load(stream)
    except Exception as e:
        print "Error parsing test plan!"
        exit(e)

    # Store the codes and tests as ordered dictionaries
    codes = OrderedDict()
    tests = OrderedDict()
    for code in testplan['codes']:
        codes[code['name']] = {'description': code['description'],
                               'file': code['file'],
                               'exec': code['exec']}
    for test in testplan['tests']:
        tests[test['name']] = {'description': test['description'],
                               'dimensions': test['dimensions']}

    pretty = PrettyPrint(verbose=args['--verbose'])
    pretty.title(testplan['name'])
    pretty.summary(testplan)

    for test in testplan['testplan']:
        name, code, trials = test['test'], test['code'], test['trials']
        pretty.heading(name)
        pretty.test_summary(tests[name], trials)

        for dimension in tests[name]['dimensions']:
            puts(colored.cyan(str(dimension) + ':'))
            for name, code in codes.iteritems():
                with progress.Bar(label=' '*4 + name + ' '*32, width=16, expected_size=10) as bar:
                    for i in range(10):
                        sleep(random() * 0.2)
                        bar.show(i)


