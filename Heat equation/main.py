import numpy as np
import matplotlib.pyplot as plt

plate_length = 50
iter_time = 1000

alpha = 2.0
dx = 1
dt = (dx**2) / (2*4*alpha)
gamma = (alpha * dt) / (dx**2)

# initial grid
T = np.empty((iter_time, plate_length, plate_length))

# initial condition
T_init = 0.0

# boundary conditions
T_top = 100
T_left = 100
T_bottom = 100
T_right = 100

# setting initial conditions
T.fill(T_init)

# boundary conditions
T[:, (plate_length - 1):, :] = T_top
T[:, :, :1] = T_left
T[:, :1, 1:] = T_bottom
T[:, :, (plate_length - 1):] = T_right


def make_step(T):
    for k in range(0, iter_time - 1, 1):
        for i in range(1, plate_length - 1, dx):
            for j in range(1, plate_length - 1, dx):
                T[k + 1, i, j] = gamma*(T[k, i + 1, j] + T[k, i - 1, j] + T[k, i, j + 1] + T[k, i, j - 1] - 4*T[k, i, j]) + T[k, i, j]

    return T


def plot_map(T_k, k):
    plt.clf()
    plt.title(f"Temperature at t = {k*dt:.3f} s")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.pcolormesh(T_k, cmap=plt.cm.jet)
    plt.colorbar()


T = make_step(T)

plt.figure()
plt.ion()

for i in range(0, iter_time):
    plot_map(T[i], i)
    plt.pause(0.001)
