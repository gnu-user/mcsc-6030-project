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
from os import path
from docopt import docopt
from schema import Schema, Or, And, Use, SchemaError


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


if __name__ == '__main__':
    args = docopt(usage)
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    print args
