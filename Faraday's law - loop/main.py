# graph of emf vs time while moving loop with constant velocity

import matplotlib.pyplot as plt
from math import sqrt

B = 1.0 # T
R = 10.0 # m
v = 1.0 # m/s

dt = 0.0001  # s
t = 0.0

dx = v * dt
dp = 0

# circle O(0,0), and R

# inital position
x = -R

earray = []
tarray = []

def darea():
    global x
    y1 = sqrt(R**2 - x**2)
    y2 = -sqrt(R**2 - x**2)

    return dx * (y1-y2)

def countEMF():
    global B
    
    dp = darea() * B
    return -(dp/dt)

def main():
    global x, R, e, t, dt, dx
    while(x < R):
        earray.append(countEMF())
        tarray.append(t)

        t += dt
        x += dx
    plt.plot(tarray,earray)
    plt.title('EMF vs time while moving loop with constant velocity (for %.2f m/s)' % v)
    plt.xlabel('t(s)')
    plt.ylabel('EMF(V)')
    plt.show()

main()    