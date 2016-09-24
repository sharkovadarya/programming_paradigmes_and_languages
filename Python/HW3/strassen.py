
import numpy as np


def read_matrix(n):
    m = np.empty([n, n], dtype=int)
    for i in range(n):
        m[i] = np.asarray(input().split(), dtype=int)

    return m


def strassen(m1, m2):

    def process_input(m1, m2):
        if (m1.shape[0] - 1) & m1.shape[0]:
            s = 2 ** m1.shape[0].bit_length()
            a = np.zeros([s, s], dtype=int)
            a[:m1.shape[0], :m1.shape[1]] = m1
            b = np.zeros([s, s], dtype=int)
            b[:m2.shape[0], :m2.shape[1]] = m2
            c = np.empty([s, s], dtype=int)
            return a, b, c
        c = np.empty([m1.shape[0], m1.shape[0]], dtype=int)
        return m1, m2, c

    def multiply(a, b, c):
        size = a.shape[0] // 2
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

        calc1 = strassen(a11 + a22, b11 + b22)
        calc2 = strassen(a21 + a22, b11)
        calc3 = strassen(a11, b12 - b22)
        calc4 = strassen(a22, b21 - b11)
        calc5 = strassen(a11 + a12, b22)
        calc6 = strassen(a21 - a11, b11 + b12)
        calc7 = strassen(a12 - a22, b21 + b22)

        c[:size, :size] = calc1 + calc4 - calc5 + calc7
        c[:size, size:] = calc3 + calc5
        c[size:, :size] = calc2 + calc4
        c[size:, size:] = calc1 + calc3 - calc2 + calc6

        return c

    a, b, c = process_input(m1, m2)
    return multiply(a, b ,c)


n = int(input())
A = read_matrix(n)
B = read_matrix(n)
print('\n'.join(' '.join(str(cell) for cell in row) for row in (strassen(A, B))[:n, :n]))




