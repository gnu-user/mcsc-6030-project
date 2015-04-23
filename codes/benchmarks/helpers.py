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
from schema import Schema, And, Or, Use


def timing(f):
    """Helpful decorator to get runtime of functions"""
    def wrap(*args):
        start = time.time()
        ret = f(*args)
        end = time.time()
        print '%s function took %0.3f seconds' % (f.func_name, (end-start))
        return ret
    return wrap


def gen_matrix(m, n, dtype, mtype=None, dist='uniform', sparse=1.00, empty=False):
    """Generates a dynamic matrix given the parameters specified.

    :param m: The rows of the matrix
    :param n: The columns of the matrix
    :param dtype: The data type must be supported by numpy
    :param mtype: The type of matrix: adjacency, stochastic, sparse
    :param dist: The distribution must be one of zero, uniform, normal, weibull, poisson
    :param sparse: The sparsity of the matrix
    """
    if empty:
        if dtype == 'int32':
            return np.zeros([m, n], dtype=np.int32)
        elif dtype == 'bool':
            return np.zeros([m, n], dtype=np.int8)
        elif dtype == 'float':
            return np.zeros([m, n], dtype=np.float)

    if mtype == 'adjacency':
        # Create an adjacency matrix representing a graph
        A = np.int32(np.random.random_integers(1, 100, (m, n)))
        A[A < 70] = 0  # 70% of vertexes are not completely connected
        A[A >= 95] = 3  # 5% have 3
        A[A >= 85] = 2  # 10% have 2 connections
        A[A >= 70] = 1  # 15% of vertexes have 1 connection
        return A
    elif mtype == 'stochastic':
        # Create a stochastic matrix representing a markov chain,
        # where the sum of each col and row is 1
        A = np.random.rand(m, n)
        B = np.copy(A)
        for i in range(0, m):
            tot = np.sum(A[i, :])
            A[i, :] /= tot
        for j in range(0, n):
            tot = np.sum(B[:, j])
            B[:, j] /= tot
        return np.dot(A, B)

    if dtype == 'int32':
        return np.int32(np.random.random_integers(1, 100, (m, n)))
    elif dtype == 'bool':
        A = np.random.rand(m, n)
        A[A < 0.5] = 0
        A[A >= 0.5] = 1
        A = A.astype('B')
        return A
    elif dtype == 'float':
        return np.random.rand(m, n)


def gen_vector(m, dtype, dist='uniform', sparse=1.00, empty=False):
    """Generates a dynamic vector given the parameters specified.

    :param m: The rows of the matrix
    :param n: The columns of the matrix
    :param dtype: The data type must be supported by numpy
    :param dist: The distribution must be one of zero, uniform, normal, weibull, poisson
    :param sparse: The sparsity of the matrix
    """
    if empty:
        if dtype == 'int32':
            return np.zeros(m, dtype=np.int32)
        elif dtype == 'bool':
            return np.zeros(m, dtype=np.int8)
        elif dtype == 'float':
            return np.zeros(m, dtype=np.float)
    if dtype == 'int32':
        return np.int32(np.random.random_integers(1, 100, m))
    elif dtype == 'bool':
        A = np.random.rand(m)
        A[A < 0.5] = 0
        A[A >= 0.5] = 1
        A = A.astype('B')
        return A
    elif dtype == 'float':
        return np.random.rand(m)

# The docopt string for command line usage of all benchmark programs
usage = """Benchmarks

Usage:
  benchmark.py --dtype=<type> [--mtype=<type> --dist=<name> --sparse=<val> --approx=<type>] DIM
  benchmark.py -h | --help

Arguments:
  DIM             The dimension of the square matrix

Options:
  -h, --help       Show this screen and exit.
  --dtype=<type>   Numpy data type e.g. float, int32, bool.
  --mtype=<type>   Specific type of matrix, either adjacency or stochastic.
  --dist=<name>    Statistical distribution [default: uniform].
  --sparse=<val>   The sparsity of the matrix [default: 1.0].
  --approx=<type>  Type of approximate multiplication, uniform or non-uniform [default: uniform].

"""

# The schema for validating the command line arguments
schema = Schema({
    'DIM': Use(int, error='Matrix dimension must be an integer.'),
    '--dtype': Use(str, error='--dtype=<type> must be a valid numpy data type.'),
    '--mtype': Or(None, Use(str, error='--mtype=<type> must be a type of adjacency or stochastic.')),
    '--dist': Or(None, Use(str, error='--dist=<name> must be a valid distribution.')),
    '--sparse': Or(None, Use(float, error='--sparse=<val> must be a floating point value.')),
    '--approx': Or(None, And(Use(str), lambda x: x in ['uniform', 'non-uniform'],
                   error='--approx=<type> must be uniform or non-uniform.')),
    '--help': Or(None, Use(bool))
})
