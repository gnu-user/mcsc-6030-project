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
from math import ceil
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
    ANS = np.zeros(dim, dtype=dtype)
    n_rows = dim  # TODO maybe support separate columns and rows

    # Broadcast the second matrix to all processes
    comm.Bcast(B, MASTER)

    # Send the first rows to other processes
    n_sent = 0
    for k in range(1, min(n_rows+1, n_proc)):
        comm.Send(A[n_sent, :], k, tag=n_sent)
        n_sent += 1

    # Loop and receive the dot product from the processes
    for k in range(n_rows):
        status = MPI.Status()
        # Receive a computed vector product of that row
        comm.Recv(ANS, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        sender = status.source
        row = status.tag
        # Record the results
        C[row, :] = ANS

        # Either send another row to sender or a tag to signal completion
        if n_sent < n_rows:
            comm.Send(A[n_sent, :], sender, tag=n_sent)
            n_sent += 1
        else:
            comm.Send(np.zeros(dim, dtype=dtype), sender, tag=n_rows+1)
    print "Finished!"

    print C
    D = np.dot(A, B)
    print "Is C == D?", np.array_equal(C, D)


def slave(dim, dtype, proc_id, comm):
    """The slave process, computes the matrix product and returns results."""
    my_row = np.zeros(dim, dtype=dtype)
    B = np.zeros([dim, dim], dtype=dtype)
    stop = np.empty(1, dtype=np.bool)
    n_rows = dim  # TODO maybe support separate columns and rows
    # Receive the second matrix
    comm.Bcast(B, MASTER)

    # Receive the subset of the first matrix
    status = MPI.Status()
    comm.Recv(my_row, source=MASTER, tag=MPI.ANY_TAG, status=status)
    row = status.tag

    while row < n_rows:
        # Return the results, including the index of the row computed
        comm.Send(np.dot(my_row, B), MASTER, tag=status.tag)
        status = MPI.Status()
        comm.Recv(my_row, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        row = status.tag


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