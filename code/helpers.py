import time
import numpy as np


def timing(f):
    """Helpful decorator to get runtime of functions"""
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap


# TODO: Add full support for types; support distribution types and sparse matrices
def gen_matrix(m, n, dtype, dist='uniform', sparse=1.00):
    """Generates a dynamic matrix given the parameters specified.

    :param m: The m dimension of the matrix
    :param n: The n dimension of the matrix
    :param dtype: The data type must be supported by numpy
    :param dist: The distribution must be one of zero, uniform, normal, weibull, poisson
    :param sparse: The sparsity of the matrix
    """
    if dtype == 'int32':
        return np.int32(np.random.random_integers(1, 100, (m, n)))
    elif dtype == 'bool':
        A = np.random.rand(m, n)
        A[A < 0.5] = 0
        A[A >= 0.5] = 1
        A = A.astype('bool')
        return A
    elif dtype == 'float':
        return np.random.rand(m, n)


# The docopt string for command line usage of all benchmark programs
usage = """Benchmarks

Usage:
  benchmark.py <m> <n> --dtype=<type> [--dist=<name> --sparse=<val>]
  benchmark.py -h | --help

Options:
  -h, --help      Show this screen and exit.
  --dtype=<type>  Numpy data type e.g. float, int32, bool.
  --dist=<name>   Statistical distribution [default: uniform].
  --sparse=<val>  The sparsity of the matrix [default: 1.0].

"""
