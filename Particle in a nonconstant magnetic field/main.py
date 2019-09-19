# Curve which a point charge (with mass m and charge q) moves in a nonconstant magnetic field (B = B0(1+ay))

import matplotlib.pyplot as plt
import numpy as np
from math import tanh, sin, cos, sqrt

# position
x = 0
y = 0
t = 0

# velocity
vx = 0
vy = 100

# constants
q = 1.6 * 10**-19
m = 5.1 * 10**-26
B0 = 3.0 * 10**-5
step = 0.000001

# B = B0(1+ay)
a = 1

# draw array
xArray = []
yArray = []

def B():
    global y, B0, a

    return B0 * (1 + a*y)

def v():
    global vx, vy

    return sqrt(vx**2 + vy**2)

def makeMove():
    global vx, vy, x, y, m, q, step

    px = B() * vy * q * step
    py = -B() * vx * q * step

    vx += px/m
    vy += py/m

    x += vx * step
    y += vy *step

def main():
    global t
    while(t <= 0.12):
        xArray.append(x)
        yArray.append(y)

        makeMove()
        #print("(%f, %f)" % (x, y))

        t += step

def drawPlot():
    # a = np.linspace(0.2, 10, 100)
    fig, ax = plt.subplots()
    
    ax.plot(xArray,yArray)
    ax.set_aspect('equal')
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title('B = %f(1 + %f*y)' % (B0, a))

    plt.show()

main()
drawPlot()
