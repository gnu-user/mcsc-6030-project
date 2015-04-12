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
from scipy.stats import rv_discrete
from math import ceil
from time import time
from docopt import docopt
from helpers import gen_matrix, usage, schema
from schema import SchemaError


def uniform_approx(A, B, S, R):
    """Creates uniformly approximate matrices of A and B, C and R."""
    # Pick rows from A and corresponding column from B uniformly random
    n = A.shape[1]
    s = S.shape[1]
    p_each = 1.0 / n  # Since uniform all row/col have equal probability
    for t in range(0, s):
        # Pick a random row and column independently with replacement
        i_t = np.random.randint(0, n)
        S[:, t] = A[i_t, :]
        R[t, :] = B[:, i_t]
        # Apply scaling
        S[:, t] /= np.sqrt(s * p_each)
        R[t, :] /= np.sqrt(s * p_each)


def non_uniform_approx(A, B, S, R):
    """Creates non-uniformly approximate matrices of A and B, C and R."""
    # Pick rows from A and corresponding column from B uniformly random
    n = A.shape[1]
    s = S.shape[1]
    rows = np.arange(0, n)  # The list of rows
    probs = np.zeros(n)  # The probability of each column

    # Calculate the probability of selecting each column based on the amount of
    # information using the method proposed by Drineas and Kannan. The probability
    # is based on the product of the row and column euclidean norms divided by
    # the cumulative sum of the product of euclidean norms for all rows and columns
    D = 0.0
    for i in range(0, n):
        prod = np.sqrt((A[i, :]*A[i, :]).sum()) * np.sqrt((B[:, i]*B[:, i]).sum())
        D += prod
        probs[i] = prod / D

    # Use the probabilities to pick the rows and columns non-uniformly
    distrib = rv_discrete(values=(rows, probs))
    for t, i_t in enumerate(distrib.rvs(size=s)):
        S[:, t] = A[i_t, :]
        R[t, :] = B[:, i_t]
        # Apply scaling
        S[:, t] /= np.sqrt(s * probs[i_t])
        R[t, :] /= np.sqrt(s * probs[i_t])


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

    # Make the approximate matrices S and R 75% of the size of A and B
    # TODO make this a test parameter
    approx_dim = int(ceil(dim * 0.75))
    S = gen_matrix(dim, approx_dim, 'float', empty=True)
    R = gen_matrix(approx_dim, dim, 'float', empty=True)

    # Calculate the uniform approximate matrix and compute the product
    # S*R as the sum of outer products
    start = time()
    uniform_approx(A, B, S, R)
    T = np.dot(S, R)
    end = time()
    print "%0.3f" % (end-start,)
