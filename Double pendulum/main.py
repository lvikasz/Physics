import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

import sys
sys.path.append('../')

from utils.load_constants import load_constants
import yaml

with open("initial_conditions.yaml", 'r') as stream:
    try:
        yamlFile = yaml.safe_load(stream)

        m1 = yamlFile['m1']
        m2 = yamlFile['m2']
        L1 = yamlFile['L1']
        L2 = yamlFile['L2']
        angular_speed1_0 = yamlFile['angular_speed1_0']
        angular_speed2_0 = yamlFile['angular_speed2_0']
        theta1_0 = np.radians(yamlFile['theta1_0'])
        theta2_0 = np.radians(yamlFile['theta2_0'])
    except yaml.YAMLError as exc:
        print(exc)
        exit()

g, dt = load_constants()

print(g)
print(dt)

time = np.arange(0, 10, dt)

x1_plot = []
y1_plot = []

x2_plot = []
y2_plot = []

theta1_plot = []
theta2_plot = []


# kinematic equations (converters from angles to xy plane)
def x1(theta1):
    return L1 * np.sin(theta1)


def y1(theta1):
    return -L1 * np.cos(theta1)


def x2(x1, theta2):
    return x1 + L2 * np.sin(theta2)


def y2(y1, theta2):
    return y1 - L2 * np.cos(theta2)


def angular_acceleration1(theta1, theta2, angular_velocity1, angular_velocity2):
    nominator = -g * (2*m1 + m2) * np.sin(theta1) - m2 * g * np.sin(theta1 - 2 * theta2) - 2 * np.sin(theta1 - theta2) * m2 * ((angular_velocity2 ** 2) * L2 + (angular_velocity1**2) * L1 * np.cos(theta1 - theta2))
    denominator = L1 * (2 * m1 + m2 - m2 * np.cos(2 * (theta1 - theta2)))

    return nominator / denominator


def angular_acceleration2(theta1, theta2, angular_velocity1, angular_velocity2):
    nominator = 2 * np.sin(theta1 - theta2) * ((angular_velocity1 ** 2) * L1 * (m1 + m2) + g * (m1 + m2) * np.cos(theta1) + (angular_velocity2**2) * L2 * m2 * np.cos(theta1 - theta2))
    denominator = L2 * (2 * m1 + m2 - m2 * np.cos(2 * (theta1 - theta2)))

    return nominator / denominator


def make_move():
    theta1 = theta1_0
    theta2 = theta2_0
    angular_velocity1 = angular_speed1_0
    angular_velocity2 = angular_speed2_0

    for t in time:
        x_1 = x1(theta1) + t
        y_1 = y1(theta1)

        x_2 = x2(x_1, theta2)
        y_2 = y2(y_1, theta2)

        x1_plot.append(x_1)
        y1_plot.append(y_1)

        x2_plot.append(x_2)
        y2_plot.append(y_2)

        theta1_plot.append(theta1)
        theta2_plot.append(theta2)

        theta1 += angular_velocity1 * dt
        theta2 += angular_velocity2 * dt

        angular_velocity1 += dt * angular_acceleration1(theta1, theta2, angular_velocity1, angular_velocity2)
        angular_velocity2 += dt * angular_acceleration2(theta1, theta2, angular_velocity1, angular_velocity2)


make_move()

fig, ax = plt.subplots()

ax.plot(time, theta1_plot)
ax.grid(True, which='both')
plt.title(r"The motion path of ball for ${\theta_1 = %.2f ^\circ}$ and ${\theta_2 = %.2f ^\circ}$" % (np.degrees(theta1_0), np.degrees(theta2_0)))
plt.ylabel(r"${\Theta_1}[rad]$")
plt.xlabel(r"$t[s]$")

plt.show()