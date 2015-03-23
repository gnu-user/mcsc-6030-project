###############################################################################
#
# Set a baseline for all benchmarks using numpy's serial matrix multiplication
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
from docopt import docopt
from helpers import gen_matrix, timing, usage, schema
from schema import SchemaError


@timing
def baseline(A, B):
    return np.dot(A, B)


if __name__ == '__main__':
    args = docopt(usage)
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    # Generate the dynamic matrices for the test
    m, n, dtype = args['<m>'], args['<n>'], args['--dtype']
    A = gen_matrix(m, n, dtype)
    B = gen_matrix(m, n, dtype)
    C = baseline(A, B)
