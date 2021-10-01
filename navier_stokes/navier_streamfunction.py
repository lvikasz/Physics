import numpy as np
import matplotlib.pyplot as plt

Ny = Nx = 41

xmax = 1
ymax = 1

x = np.linspace(0, xmax, Nx)
y = np.linspace(0, ymax, Ny)

X, Y = np.meshgrid(x, y)

nu = 0.1

dt = 0.0002
dx = xmax / (Nx - 1)
dy = ymax / (Ny - 1)

u = np.zeros((Ny, Nx))
v = np.zeros((Ny, Nx))
w = np.zeros((Ny, Nx)) # pomocnicza zmienna 

streamfunction = np.zeros((Ny, Nx))
vorticity = np.zeros((Ny, Nx))

u_prawa = 0 # + w gore 
u_lewa = -1 # + w gore
v_gorna = 0 # + w prawo
v_dolna = 1 # + w prawo

def calculate_velocity():
    global u, v
    u[1:-1, 0] = u_lewa # lewa sciana, + w gore
    u[1:-1, -1] = u_prawa # prawa sciana, + w gore
    u[0, 1:-1] = 0 # dolna sciana, + w gore
    u[-1, 1:-1] = 0 # gorna sciana, + w gore

    v[1:-1, 0] = v_dolna # dolna sciana, + w prawo
    v[1:-1, -1] = v_gorna # gorna sciana, + w prawo
    v[0, 1:-1] = 0 # dolna sciana, + w prawo
    v[-1, 1:-1] = 0 # gorna sciana, + w prawo

    u_new = (streamfunction[1:-1, 0:-2] - streamfunction[1:-1, 1:-1]) / dx
    v_new = -(streamfunction[0:-2, 1:-1] - streamfunction[1:-1, 1:-1]) / dy

    u[1:-1, 1:-1] = u_new
    v[1:-1, 1:-1] = v_new

def make_step():
    global u, v, streamfunction, vorticity

    beta = 1.5
    for t in range(75):
        for i in range(1, Nx - 1):
            for j in range(1, Ny - 1):
                # SOR
                streamfunction[i, j] = 1/4*beta*(streamfunction[i+1, j] + streamfunction[i-1, j] \
                    + streamfunction[i, j+1] + streamfunction[i, j-1] + dx**2*vorticity[i, j]) + (1-beta)*streamfunction[i, j]

    vorticity[1:-1, 0] = -2*streamfunction[1:-1, 1] / dx**2 - u_lewa*2/dy # po lewej
    vorticity[1:-1, -1] = -2*streamfunction[1:-1, -2] /dx**2 + u_prawa*2/dx # po prawej
    vorticity[0, 1:-1] = -2*streamfunction[1, 1:-1]/dx**2  + v_dolna*2/dx # po scianie dolnej
    vorticity[-1, 1:-1] = -2*streamfunction[-2, 1:-1]/dx**2 - v_gorna*2/dx # po scianie gornej

    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            w[i,j] = -1*v[i, j]/(2*dx)*(vorticity[i+1, j] - vorticity[i-1, j]) \
                - u[i, j]/(2*dy)*(vorticity[i, j+1]-vorticity[i, j-1]) \
                + nu*(vorticity[i+1,j]+vorticity[i-1,j]+vorticity[i,j+1]+vorticity[i,j-1]-4.0*vorticity[i,j])/(dx**2)
    
    vorticity[1:-1, 1:-1] = vorticity[1:-1, 1:-1] + dt*w[1:-1, 1:-1]

    calculate_velocity()


def run():
    for i in range(1000):
        print("t = ", dt*i)
        make_step()
        plt.clf()

        plt.xlim([0, xmax])
        plt.ylim([0, ymax])
        plt.streamplot(X, Y, v, u)
        plt.contourf(X, Y, streamfunction)
        plt.colorbar()
        plt.pause(0.0001)

plt.ion()
run()

# Bibliografia:
# https://www.iist.ac.in/sites/default/files/people/psi-omega.pdf