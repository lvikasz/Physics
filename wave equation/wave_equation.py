import matplotlib.pyplot as plt
import numpy as np

Nz = 400
v = 20
L = 1
# L = np.sqrt(2)/2
# L = 0.5
dz = 2*L/Nz
dt = dz/v
xs = np.linspace(0, 2*L, Nz)

# zmienna pomocnicza, zeby nie obliczac wiele razy
C = v * dt/dz

# wychylenie
def f(x):
    return np.exp( -20*(x-1)**2 )

def g(x):
    return f(x) - f(0)
    # return -1*x*(x-1)*np.exp(-1*x**2 * (x - 2)**2)

def g_prim(x):
    return -40*np.exp(-20*(x-1)**2)*(x-1)
    # return (4*x**5-16*x**4+20*x**3-8*x**2-2*x+1)*np.exp(-1 * (x-2)**2 * x**2)

p = [ g(xs) ]

# podstawienie
s = [ v*g_prim(xs) ]
r = [ [0]*len(p[0]) ]

# pierwsza iteracja 
r_next = [0]
s_next = [v*(p[-1][1] - p[-1][0])/(dz)]

for i in range(1, len(r[-1]) - 1):
    r_next.append( 0.5*C*(s[-1][i+1] - s[-1][i-1]) + r[-1][i] )
    s_next.append( 0.5*C*(r[-1][i+1] - r[-1][i-1]) + s[-1][i] )

r_next.append(0)
s_next.append(v*(p[-1][-1] - p[-1][-2])/dz)

r.append(r_next)
s.append(s_next)

plt.clf()
# input()
plt.ylim([0, 1])
plt.plot(xs, p[-1], 'b')
plt.grid()
plt.pause(1)


def iterate():
    global r, s, p
    r_next = [0]
    s_next = [v*(p[-1][1] - p[-1][0])/dz]
    # s_next = [v*(p[-1][1] - 0)/(2*dz)]

    for i in range(1, len(r[-1]) - 1):
        r_next.append( C*(s[-1][i+1] - s[-1][i-1]) + r[-2][i] )
        s_next.append( C*(r[-1][i+1] - r[-1][i-1]) + s[-2][i] )

    r_next.append(0)
    s_next.append(v*(p[-1][-1] - p[-1][-2])/dz)
    # s_next.append(v*(0 - p[-1][-2])/(2*dz))

    return (r_next, s_next)

def gen_p(ps, rs):
    return [pi+ri*dt for (pi, ri) in zip(ps, rs)]

def solve():
    for i in range(100000):
        (r_next, s_next) = iterate()

        r.append(r_next)
        s.append(s_next)
        
        p.append(gen_p(p[-1], r[-1]))
        
        plt.clf()
        plt.ylim([-1, 1])
        plt.plot(xs, p[-1], 'b')
        plt.grid()
        plt.pause(0.0001)

plt.ion()
solve()
plt.show()