import numpy as np


def naive_mult(A, B, C):
    """Computes the matrix multiplication using the naiive approach"""
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            for k in range(A.shape[1]):
                C[i, j] += A[i, k] * B[k, j]


A = np.round(100*np.random.rand(100, 100)).astype('i')
B = np.round(100*np.random.rand(100, 100)).astype('i')
C = np.zeros([100, 100], dtype=np.int32)
naive_mult(A, B, C)
D = np.dot(A, B)

print "Is C == D?", np.array_equal(C, D)
