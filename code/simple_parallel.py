#!/usr/bin/env python2
###############################################################################
#
# Simple parallel implementation using MPI to divide the rows and columns
# amongst several workers.
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
from mpi4py import MPI
from math import floor
from time import time
from docopt import docopt
from helpers import gen_matrix, usage, schema
from schema import SchemaError

# Define process 0 as MASTER
MASTER = 0


def master(dim, dtype, n_proc, comm):
    """The master process, generates matrices and divides up the work."""
    A = gen_matrix(dim, dtype)
    B = gen_matrix(dim, dtype)
    C = np.zeros([dim, dim], dtype=dtype)
    ans = np.zeros([dim, dim], dtype=dtype)

    # Broadcast the second matrix to all processes
    comm.Bcast(B, MASTER)

    # Divide the rows of the matrix amongst the processes
    row = 0
    num_rows = floor(dim / (n_proc - 1))
    for k in range(1, min(dim+1, n_proc)):
        # Send the remainder to the last process
        if k == n_proc - 1:
            comm.Send(A[row::, :], k, tag=row)
        else:
            comm.Send(A[row:num_rows, :], k, tag=row)
        row += num_rows

    # Loop and receive the dot product from the processes
    while row > 0:
        status = MPI.Status()
        comm.Recv(ans, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, 
                  status=status)
        row = status.tag
        # Handle when the last row is returned
        if dim - row >= num_rows:
            C[row:, :] = ans
        else:
            C[row:num_rows] = ans
        row -= num_rows

    print C
    D = np.dot(A, B)   
    print "Is C == D?", np.array_equal(C, D)


def slave(dim, dtype, proc_id, comm):
    """The slave process, computes the matrix product and returns results."""
    subset = np.zeros([dim, dim], dtype=dtype)
    B = np.zeros([dim, dim], dtype=dtype)

    # Receive the second matrix
    comm.Bcast(B, MASTER)

    # Receive the subset of the first matrix
    status = MPI.Status()
    comm.Recv(subset, source=MASTER, tag=MPI.ANY_TAG, status=status)

    # Return the results, including the index of the row computed
    comm.Send(np.dot(subset, B), MASTER, tag=status.tag)


if __name__ == '__main__':
    args = docopt(usage)
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    # Initialize MPI environment
    comm = MPI.COMM_WORLD
    n_proc = comm.Get_size()
    proc_id = comm.Get_rank()

    if n_proc < 2:
        print "Error: requires two or more processes to operate!"

    if proc_id == MASTER:
        master(args['DIM'], args['--dtype'], n_proc, comm)
    else:
        slave(args['DIM'], args['--dtype'], n_proc, comm)
    # Generate the dynamic matrices for the test

    # Calculate the execution time for the baseline
    #start = time()
    #C = np.dot(A, B)
    #end = time()
    #print "%0.3f" % (end-start,)
