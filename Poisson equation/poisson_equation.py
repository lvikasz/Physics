import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import diags
from matplotlib import cm
import copy
from mpl_toolkits.mplot3d import Axes3D

rho = 1600
l = 1
cw = 830
k = 1 #l/(rho*cw)

z = 1

N = 100
x = y = np.linspace(0, z, N)
temp = np.array([18+273 for j in y for i in x])
T = temp.reshape(N, N)

dz = z/N

k = 2
dx = (2/N)
delta = 1
dt = delta**2/4

t = 0

def f(x, y):
    if x == N/2 and y == N/2:
        return -10e5
    return 0

def calculate(T):
    T_new = copy.deepcopy(T)
    s = 2*(1 + ( 1 - (np.cos(np.pi/k)**2 )**(0.5) ) )**(-1)

    for i in range(1, len(T) - 1):
        for j in range(1, len(T) - 1):

            # T_new[i, j] = T[i, j] + dt/(delta)**2 * (T[i, j+1] + T[i, j-1] + T[i+1, j] + T[i-1, j] - 4*T[i, j]) - dt*f(i, j)
            
            T_new[i, j] = 0.25*(T[i, j+1] + T[i, j-1] + T[i+1, j] + T[i-1, j] - delta**2*f(i, j))
    
    for i in range(1, len(T) - 1):
        for j in range(1, len(T) - 1):        
            error = T[i, j+1] + T[i, j-1] + T[i+1, j] + T[i-1, j] - 4*T[i, j] - f(i, j)*delta**2
            T_new[i, j] = T[i, j] + s * error/4
    

    return T_new

def run():
    global T
    while True:
        for i in range(200):
            T_ = calculate(T)
            T = T_
            # surf = ax.plot_surface(X, Y, T, cmap=cm.coolwarm,
            #                linewidth=1, antialiased=False)
        
        plt.clf()
        plt.contourf(x, y, T, N)
        plt.colorbar()
        plt.pause(0.1)

X, Y = np.meshgrid(x, y)

plt.ion()
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# surf = ax.plot_surface(X, Y, T, cmap=cm.coolwarm,
#                        linewidth=1, antialiased=False)
# fig.colorbar(surf, shrink=0.5, aspect=5)
run()
plt.show()
