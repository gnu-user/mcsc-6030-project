#!/usr/bin/env python2
###############################################################################
#
# Collection of helper functions and other utilities used by each of the
# benchmarking implementations.
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
import time
import numpy as np
from schema import Schema, Or, Use


def timing(f):
    """Helpful decorator to get runtime of functions"""
    def wrap(*args):
        start = time.time()
        ret = f(*args)
        end = time.time()
        print '%s function took %0.3f seconds' % (f.func_name, (end-start))
        return ret
    return wrap


# TODO: Add full support for types; support distribution types and sparse matrices
def gen_matrix(dim, dtype, dist='uniform', sparse=1.00):
    """Generates a dynamic matrix given the parameters specified.

    :param dim: The dimension of the square matrix
    :param dtype: The data type must be supported by numpy
    :param dist: The distribution must be one of zero, uniform, normal, weibull, poisson
    :param sparse: The sparsity of the matrix
    """
    if dtype == 'int32':
        return np.int32(np.random.random_integers(1, 100, (dim, dim)))
    elif dtype == 'bool':
        A = np.random.rand(dim, dim)
        A[A < 0.5] = 0
        A[A >= 0.5] = 1
        A = A.astype('bool')
        return A
    elif dtype == 'float':
        return np.random.rand(dim, dim)


# The docopt string for command line usage of all benchmark programs
usage = """Benchmarks

Usage:
  benchmark.py --dtype=<type> [--dist=<name> --sparse=<val>] DIM
  benchmark.py -h | --help

Arguments:
  DIM             The dimension of the square matrix

Options:
  -h, --help      Show this screen and exit.
  --dtype=<type>  Numpy data type e.g. float, int32, bool.
  --dist=<name>   Statistical distribution [default: uniform].
  --sparse=<val>  The sparsity of the matrix [default: 1.0].

"""

# The schema for validating the command line arguments
# TODO: Add better validation for numpy type provided, stat. distribution, sparsity
schema = Schema({
    'DIM': Use(int, error='Matrix dimension must be an integer.'),
    '--dtype': Use(str, error='--dtype=<type> must be a valid numpy data type.'),
    '--dist': Or(None, Use(str, error='--dist=<name> must be a valid distribution.')),
    '--sparse': Or(None, Use(float, error='--sparse=<val> must be a floating point value.')),
    '--help': Or(None, Use(bool))
})
