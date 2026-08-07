import numpy as np

# N = 2

m = np.array([1000.0, 1.0, 0], dtype=float)

N=3
y0 = np.array([1, 1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype = float)
r = y0[0 : 3*N].reshape(N, 3)
v = y0[3*N : 6*N].reshape(N, 3)

print(m[None, :, None])