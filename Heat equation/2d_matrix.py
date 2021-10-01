import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags

rho = 1600
l = 1
cw = 830
k = 1 #l/(rho*cw)

z = 1

N = 50
x = y = np.linspace(0, z, N)
temp = np.array([18+273 for j in y for i in x])
# temp = np.array([np.sin(np.pi*i)*np.sin(np.pi*j) for j in y for i in x])
T = temp.reshape(N, N)

dz = z/N

k = 100000
dx = (2/N)
dt = 0.5*dx**2/(4*k)#0.01#3600

t = 0

def f(i):
    if i == N/2 or i == N/2-1 or i == N/2-2 or i == N/2+1 or i == N/2+2 or i == N/2-3 or i == N/2+3:
        return 35500
    if i == -1:
        return 0
    return 0

def construct_matrix(T, i):
    global t
    a = -k*dt/(dz)**2
    c = a
    b = 1 + 2*k*dt/(dz)**2

    tridiagonal = np.array([np.ones(N-1)*c, np.ones(N)*b, np.ones(N-1)*a])
    offset = [-1,0,1]
    A = diags(tridiagonal, offset).toarray()

    A[0, 1] += c
    A[-1, -2] += a

    B = T[::-1]

    B[0] -= c*2*dz/l*f(i)

    return A, B

def calculate(T):
    for i in range(0, N - 1):
        t_ = T[i, :]
        A, B = construct_matrix(t_, i)

        T_next = np.linalg.solve(A, B)
        t_ = T_next[::-1]

        T[i, :] = t_

    for j in range(0, N - 1):
        t_ = T[:, j]
        A, B = construct_matrix(t_, -1)

        T_next = np.linalg.solve(A, B)
        t_ = T_next[::-1]

        T[:, j] = t_

    return T

def run(T):
    global t
    k = 0

    while True:
        t = k*dt

        T = calculate(T)
        print(T)
        plt.clf()
        plt.contourf(x, y, T, N+150)
        plt.colorbar()
        plt.pause(0.1)
        k += 1
        print("Update")

        # A, B = construct_matrix(T)

        # T_next = np.linalg.solve(A, B)
        # T = T_next[::-1]

        # plt.clf()
        # plt.plot(zs, T, 'b')

        # plt.grid()
        # plt.pause(0.1)

# plt.clf()
# plt.contourf(x, y, T, 100)
# plt.colorbar()
# plt.show()  

plt.ion()
run(T)