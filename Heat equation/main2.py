import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt

e = np.e
N = 5
dx = 1.0/N
x = np.linspace(0, 1, N+1)

b = np.zeros((1, N+1)).ravel()
b[0] = 1

main_diagonal = (-2 - 8*dx**2)*np.ones((1, N+1)).ravel()
upper_diagonal = (1+dx)*np.ones((1, N)).ravel()
lower_diagonal = (1-dx)*np.ones((1, N)).ravel()

diagonals = [lower_diagonal, main_diagonal, upper_diagonal]


A = sparse.diags(diagonals, [-1, 0, 1]).toarray()
A[0, 0] = 1
A[0, 1] = 0
A[N, N-1] = 0
A[N, N] = 1

print(A)

y = np.linalg.solve(A, b)

xf = np.linspace(0, 1, 1001)
yexact = (1/(1-np.exp(6)))*np.exp(2*xf)+(1/(1-np.exp(-6)))*np.exp(-4*xf)
print(y)
plt.plot(x, y)
plt.plot(xf, yexact)
plt.legend(['Finite difference', 'Exact solution'])
plt.tight_layout()
plt.show()
