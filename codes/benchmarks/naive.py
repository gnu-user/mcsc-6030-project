#!/usr/bin/env python2
###############################################################################
#
# Naive implementation of matrix multiplication to compare to the baseline
# results when using numpy.
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
from time import time
from docopt import docopt
from helpers import gen_matrix, usage, schema
from schema import SchemaError


def naive(A, B, C):
    """Computes the matrix multiplication using the naive approach"""
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]


if __name__ == '__main__':
    args = docopt(usage)
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    # Generate the dynamic matrices for the test
    dim, dtype, mtype = args['DIM'], args['--dtype'], args['--mtype']
    A = gen_matrix(dim, dim, dtype, mtype)
    B = gen_matrix(dim, dim, dtype, mtype)
    C = gen_matrix(dim, dim, dtype, empty=True)

    # Calculate the execution time for the naive approach
    start = time()
    naive(A, B, C)
    end = time()
    print "%0.3f" % (end-start,)
