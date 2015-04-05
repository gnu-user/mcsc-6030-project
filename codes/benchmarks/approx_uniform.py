#!/usr/bin/env python2
###############################################################################
#
# Performs approximate matrix multiplication using a uniform distribution.
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
import numpy as np
from math import ceil
from time import time
from docopt import docopt
from helpers import gen_matrix, usage, schema
from schema import SchemaError


def uniform_approx(A, B, S, R):
    """Creates uniformly approximate matrices of A and B, C and R."""
    # Pick rows from A and corresponding column from B uniformly random
    n = A.shape[1]
    c = S.shape[1]
    print "C, N:", c, n
    p_each = 1.0 / n  # Since uniform all row/col have equal probability
    for t in range(0, c):
        # Pick a random row and column independently with replacement
        i_t = np.random.randint(0, n)
        S[:, t] = A[i_t, :]
        R[t, :] = B[:, i_t]
        # Apply scaling
        print S[:, t]
        print np.sqrt(c * p_each)
        S[:, t] /= np.sqrt(c * p_each)
        R[t, :] /= np.sqrt(c * p_each)


if __name__ == '__main__':
    args = docopt(usage)
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    # Generate the dynamic matrices for the test
    dim, dtype = args['DIM'], args['--dtype']
    A = gen_matrix(dim, dim, dtype)
    B = gen_matrix(dim, dim, dtype)

    D = gen_matrix(dim, dim, dtype)
    E = gen_matrix(dim, dim, dtype)

    # Make the approximate matrices C and R 75% of the size of A and B
    # TODO make this a test parameter
    approx_dim = int(ceil(dim * 0.75))
    S = gen_matrix(dim, approx_dim, 'float', empty=True)
    R = gen_matrix(approx_dim, dim, 'float', empty=True)

    # Calculate the uniform approximate matrix and compute the product
    # S*R as the sum of outer products
    uniform_approx(A, B, S, R)
    start = time()
    T = np.dot(S, R)
    end = time()
    print "%0.3f" % (end-start,)

    C = np.dot(A, B)
    F = np.dot(D, E)
    print T.shape, C.shape

    RES = T - C
    print "T - C:", RES
    print "F - C:", F - C
    print "C - C:", C - C

    print "NORM T-C:", np.linalg.norm(RES)
    print "NORM F-C:", np.linalg.norm(F-C)
    print "NORM C-C:", np.linalg.norm(C-C)

    # Calculate the bound
    error = (1.0 / approx_dim) * (np.linalg.norm(A) * np.linalg.norm(B))
    print "ERROR BOUND:", error

    # Calculate the error %
    print "ERROR %:", (np.linalg.norm(RES) / error) * 100
