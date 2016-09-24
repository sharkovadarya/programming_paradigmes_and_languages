
import numpy as np
from math import log, ceil


def read_matrix(n):
    m = np.zeros([n, n], dtype=int)
    for i in range(n):
        lst = input().split()
        m[i][:len(lst)] = np.asarray(lst, dtype=int)

    return m


def strassen(m1, m2, c):
    # using base 2 logarithm to round n up to nearest power of 2
    s = 2 ** (ceil(log(m1.shape[0], 2)))
    a = np.zeros([s, s], dtype=int)
    a[:m1.shape[0], :m1.shape[1]] = m1
    b = np.zeros([s, s], dtype=int)
    b[:m2.shape[0], :m2.shape[1]] = m2

    size = s // 2
    if size == 1:
        return a.dot(b)

    a11 = a[:size, :size]
    a12 = a[:size, size:]
    a21 = a[size:, :size]
    a22 = a[size:, size:]

    b11 = b[:size, :size]
    b12 = b[:size, size:]
    b21 = b[size:, :size]
    b22 = b[size:, size:]

    calc1 = strassen(a11 + a22, b11 + b22, np.empty([size, size], dtype=int))
    calc2 = strassen(a21 + a22, b11, np.empty([size, size], dtype=int))
    calc3 = strassen(a11, b12 - b22, np.empty([size, size], dtype=int))
    calc4 = strassen(a22, b21 - b11, np.empty([size, size], dtype=int))
    calc5 = strassen(a11 + a12, b22, np.empty([size, size], dtype=int))
    calc6 = strassen(a21 - a11, b11 + b12, np.empty([size, size], dtype=int))
    calc7 = strassen(a12 - a22, b21 + b22, np.empty([size, size], dtype=int))

    c[:size, :size] = calc1 + calc4 - calc5 + calc7
    c[:size, size:] = calc3 + calc5
    c[size:, :size] = calc2 + calc4
    c[size:, size:] = calc1 + calc3 - calc2 + calc6

    return c

n = int(input())
A = read_matrix(n)
B = read_matrix(n)
s = 2 ** (ceil(log(n, 2)))
print('\n'.join(' '.join(str(cell) for cell in row) for row in (strassen(A, B, np.empty([s, s], dtype=int)))[:n, :n]))




