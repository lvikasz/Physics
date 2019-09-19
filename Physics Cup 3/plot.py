import matplotlib.pyplot as plt
from math import sqrt, sin, cos, tan, radians, atan, fabs

vx = 0
vy = 0

dt = 0.0001

degree = 5
alpha = radians(degree)
sur = radians(180 - degree)

g = -9.81
d = 2
k = 2*d/cos(alpha)
h = h = d/cos(alpha)
n = 0

x = 0
y = d / cos(alpha)
t = 0

xArray = []
yArray = []

yCurrentSurface = -2*k*sin(sur)*n*(n+1)*sin(sur)
xSurface = []
ySufrace = []

xFoci = []
yFoci = []

xSurface.append(x)
ySufrace.append(yCurrentSurface)


def makeMove():
    global vx, vy, x, y, g, dt, alpha, sur, yCurrentSurface, xSurface, ySufrace, n, T, t0, t, xNextSurface, yNextSurface

    # when ball touches plane
    if y < yCurrentSurface:
        n+=1
        yCurrentSurface = -2*k*sin(sur)*(n+1)*(n)*sin(sur)
        
        xSurface.append(x)
        ySufrace.append(y)

        # slip vlocities
        # gamma - the angle between velocity and horizontal line
        if vx != 0:
            gamma = atan(fabs(vy) / vx)

        else:
            gamma = radians(90)
        
        # beta - the angle between reflected velocity and horizontal line
        beta = gamma - 2*alpha
        v = sqrt(vx**2 + vy ** 2)
        
        vx = v * cos(beta)
        vy = v * sin(beta)


    # vx is constant between bounces
    vy += g * dt

    x += vx * dt
    y += vy * dt
    
    xFoci.append(x)
    yFoci.append(-tan(2*alpha)*x + h)
    

def main():
    global t, xArray, yArray, dt
    while t < 10:
        xArray.append(x)
        yArray.append(y)
        makeMove()
        t += dt

    fig, ax = plt.subplots()
    
    ax.plot(xArray, yArray, '-b', label = "Motion of ball")
    ax.plot(xSurface, ySufrace, '-g', label = "Surface")
    ax.plot(xFoci, yFoci, '-k', label = "Foci shape")

    ax.grid(True, which='both')
    ax.axhline(y=h, color='k')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.legend(loc='upper right')
    
    plt.title("The motion path of ball for alpha = %.2f" % degree)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


main()
