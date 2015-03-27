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
from collections import OrderedDict
import sys
from os import path, popen
from subprocess import Popen, PIPE
from docopt import docopt
from schema import Schema, Or, And, Use, SchemaError
from clint.textui import puts, progress, colored, indent, columns
from tabulate import tabulate


usage = """Test Framework

Usage:
  test_framework.py [-v | --verbose] --code=<dir> TESTPLAN
  test_framework.py -h | --help

  Executes the test plan and evaluates the code in the directory.

Arguments:
  TESTPLAN       The test plan YAML document.

Options:
  -h, --help     Show this screen and exit.
  -v, --verbose  Increased verbosity, display more information.
  ---code=<dir>  The directory containing the code to execute.

"""

schema = Schema({
    '--code': And(path.exists, error='Code directory does not exist.'),
    'TESTPLAN': And(path.exists, error='Test plan does not exist.'),
    '--help': Or(None, Use(bool)),
    '--verbose': Or(None, Use(bool))
})


class PrettyPrint(object):
    """Prints the text for the test framework to the screen prettily."""
    _col2 = 30  # Default width for second column
    _tab = 3  # Number of space charaters for tab

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
            with indent(self._tab):
                puts(columns([test_plan['description'], self.col1-self._tab]))

        puts(colored.cyan('Codes:'))
        if self.verbose:
            with indent(self._tab):
                for code in test_plan['codes']:
                    puts(colored.magenta(code['name']))
                    with indent(self._tab):
                        puts(columns([code['description'] + '\n', self.col1-self._tab*2]))
        else:
            with indent(self._tab):
                for code in test_plan['codes']:
                    puts(code['name'])

        puts(colored.cyan('Tests:'))
        if self.verbose:
            with indent(self._tab):
                for test in test_plan['tests']:
                    puts(colored.magenta(test['name']))
                    with indent(self._tab):
                        puts(columns([test['description'], self.col1-self._tab*2]))
        else:
            with indent(self._tab):
                for test in test_plan['tests']:
                    puts(test['name'])
            puts()

    def title(self, title, end='Test Plan'):
        """Displays the main testplan heading."""
        lpad = int(floor((self.col1 - len(title) - len(' ' + end)) / 2)) - 1
        rpad = self.col1 - len(title) - len(' ' + end) - lpad - 2
        puts('\n' + '=' * self.col1)
        puts('=' + ' ' * lpad + title + ' ' + end + ' ' * rpad + '=')
        puts('=' * self.col1)

    def heading(self, title):
        """Displays the heading for each test being executed."""
        lpad = int(floor((self.col1 - len(title) - len('Executing Test ')) / 2)) - 1
        rpad = self.col1 - len(title) - len('Executing Test ') - lpad - 2
        puts('\n' + '-' * self.col1)
        puts('-' + ' ' * lpad + 'Executing ' + title + ' Test' + ' ' * rpad + '-')
        puts('-' * self.col1)

    def test_summary(self, test, trials):
        puts(colored.cyan('Trials: ') + str(trials))
        puts(colored.cyan('Dimensions: ') + str(test['dimensions']))
        if self.verbose:
            puts(colored.cyan('Description:'))
            with indent(self._tab):
                puts(columns([test['description'], self.col1-self._tab]))

    def progress(self, name):
        """Returns a label for progress bar so it's properly aligned."""
        lpad = self._tab
        rpad = self.col1 - len(name) - lpad
        return ' ' * lpad + name + ' ' * rpad

    def table(self, data):
        """Prints a pretty table of the data, where each key is a column, and
           the value is an iterable for the rows of data.
        """
        puts(tabulate(data, headers="keys", tablefmt="grid", floatfmt=".3f"))


# TODO: Clean this up, should be part of a class
def gen_summary(results, codes):
    """Creates a dictionary summarizing the results of execution times."""
    summary = OrderedDict()
    summary['codes'] = list(codes.keys())
    for test, result in results.iteritems():
        summary[test] = []
        for i, code in enumerate(result):
            summary[test].append(0)
            for times in result[code].values():
                summary[test][i] += sum(times) / float(len(times))
    return summary


if __name__ == '__main__':
    args = docopt(usage)
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    # Load the test plan
    testplan = None
    try:
        with open(args['TESTPLAN'], 'r') as stream:
            testplan = yaml.load(stream)
    except Exception as e:
        print "Error parsing test plan!"
        exit(e)

    # Store the codes and tests as ordered dictionaries
    codes = OrderedDict()
    tests = OrderedDict()
    for code in testplan['codes']:
        if 'args' in code:
            codes[code['name']] = {'description': code['description'],
                                   'file': code['file'],
                                   'exec': code['exec'],
                                   'args': code['args']}
        else:
            codes[code['name']] = {'description': code['description'],
                                   'file': code['file'],
                                   'exec': code['exec']}
    for test in testplan['tests']:
        tests[test['name']] = {'description': test['description'],
                               'dimensions': test['dimensions'],
                               'type': test['type']}

    pretty = PrettyPrint(verbose=args['--verbose'])
    pretty.title(testplan['name'])
    pretty.summary(testplan)

    # Execute each test in the test plan and store the results
    results = OrderedDict()
    for test in testplan['testplan']:
        name, trials = test['test'], test['trials']
        results[name] = OrderedDict()
        pretty.heading(name)
        pretty.test_summary(tests[name], trials)

        for dim in tests[name]['dimensions']:
            puts(colored.cyan(str(dim) + ':'))
            for code_name, code in codes.iteritems():
                # The results for this test
                results[name][code_name] = OrderedDict()
                results[name][code_name][str(dim)] = []

                for i in progress.bar(range(trials), label=pretty.progress(code_name), width=10):
                    # Execute the test, record the execution time
                    if 'args' in code:
                        pargs = [code['exec']] + code['args'] +\
                                [path.join(args['--code'], code['file']),
                                 '--dtype=' + tests[name]['type'], str(dim)]
                    else:
                        pargs = [code['exec'], path.join(args['--code'], code['file']),
                                 '--dtype=' + tests[name]['type'], str(dim)]
                    p = Popen(pargs, stdout=PIPE)
                    output, err = p.communicate()
                    # Store the results of each trial
                    results[name][code_name][str(dim)].append(float(output))

    # Display the descriptive statistics of the results
    pretty.title(testplan['name'], end='Runtime Summary')
    pretty.table(gen_summary(results, codes))
