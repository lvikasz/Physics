#!/usr/bin/env python3
import numpy as np

# Given constants
g = 9.8  # m/s^2
k = 0.203  # Kg/m
m = 80 # Kg
fall_ht_aprox = 5000 # m

# We use fourth order Runge-Kutta method to solve this ODE
def RK4_integrate(f, y0, m, g, k):
    # initial values
    w = [y0]
    t = [0]
    i = 0
    # subsequent values
    while w[i][0] < 5000:
            h = 0.1
            h2 = h/2
            s1 = f(w[i],t[i],m, g, k)
            s2 = f(w[i] + h2*s1, t[i]+h2,m, g, k)
            s3 = f(w[i] + h2*s2, t[i]+h2,m, g, k)
            s4 = f(w[i] + h*s3, t[i]+h,m, g, k)
            w_n = w[i] + h/6 * (s1 + 2*s2 + 2*s3 + s4)
            t.append(t[i]+h)
            w.append(w_n)
            i += 1
    fall_ht = w[i][0]
    time = t[i]
    return fall_ht, time 

# RHS of the equation
def func(y, t, m, g, k):
    f1 = y[1]
    f2 = g - (k/m)*pow(y[1],2)
    return np.array([f1,f2])

# Initial conditions
y0=np.array([0.0, 0.0])

# Solve the eqution
Sol = RK4_integrate(func, y0, m, g, k)
print("The actual fall distance is ", Sol[0]," in meters.")
print("The time taken for fall is ", Sol[1]," in seconds.")
