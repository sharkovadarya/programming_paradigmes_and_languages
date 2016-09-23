
import numpy as np


def read_matrix(n):
    # using base 2 logarithm to round n up to nearest power of 2
    from math import log, ceil
    s = 2**(ceil(log(n, 2)))
    m = np.zeros([s, s])
    for i in range(n):
        j = 0
        lst = input().split()
        for element in lst:
            m[i][j] = element
            j += 1

    return m


def strassen(a, b):
    size = a.shape[0] // 2
    if size == 1:
        return a.dot(b)

    a11 = np.array(a[:size, :size])
    a12 = np.array(a[:size, size:])
    a21 = np.array(a[size:, :size])
    a22 = np.array(a[size:, size:])

    b11 = np.array(b[:size, :size])
    b12 = np.array(b[:size, size:])
    b21 = np.array(b[size:, :size])
    b22 = np.array(b[size:, size:])

    calc1 = strassen(a11 + a22, b11 + b22)
    calc2 = strassen(a21 + a22, b11)
    calc3 = strassen(a11, b12 - b22)
    calc4 = strassen(a22, - b11 + b21)
    calc5 = strassen(a11 + a12, b22)
    calc6 = strassen(- a11 + a21, b11 + b12)
    calc7 = strassen(a12 - a22, b21 + b22)

    c11 = calc1 + calc4 - calc5 + calc7
    c12 = calc3 + calc5
    c21 = calc2 + calc4
    c22 = calc1 + calc3 - calc2 + calc6

    c1 = np.concatenate((c11, c12), axis=1)
    c2 = np.concatenate((c21, c22), axis=1)
    return np.concatenate((c1, c2), axis=0)

n = int(input())
A = read_matrix(n)
B = read_matrix(n)
print ('\n'.join(' '.join(str(cell) for cell in row) for row in (strassen(A, B))[:n, :n]))



