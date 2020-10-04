# Real time plotting, there may be some bugs. If it stop, you should resize the window.

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# physical constants and initial conditions
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

time = np.arange(0, 10, dt)

x1_plot = []
y1_plot = []

x2_plot = []
y2_plot = []

theta1_plot = []
theta2_plot = []

time_plot = []
current_time = 0

# init
theta1 = theta1_0
theta2 = theta2_0
angular_velocity1 = angular_speed1_0
angular_velocity2 = angular_speed2_0


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
    global theta1, theta2, angular_velocity1, angular_velocity2, current_time
    x_1 = x1(theta1)
    y_1 = y1(theta1)

    x_2 = x2(x_1, theta2)
    y_2 = y2(y_1, theta2)

    x1_plot.append(x_1)
    y1_plot.append(y_1)

    x2_plot.append(x_2)
    y2_plot.append(y_2)

    theta1_plot.append(theta1)
    theta2_plot.append(theta2)

    time_plot.append(current_time)

    theta1 += angular_velocity1 * dt
    theta2 += angular_velocity2 * dt

    angular_velocity1 += dt * angular_acceleration1(theta1, theta2, angular_velocity1, angular_velocity2)
    angular_velocity2 += dt * angular_acceleration2(theta1, theta2, angular_velocity1, angular_velocity2)

    current_time += dt


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# ax = plt.axes(ax1)
# line, = ax.plot([], [], lw=2)
#
#
#
# def init():
#     line.set_data([], [])
#     return line,


def animate(i, time_plot, theta1_plot):
    make_move()

    # Limit x and y lists to 20 items
    time_plot = time_plot[-500:]
    theta1_plot = theta1_plot[-500:]
    #print(time_plot)

    # Draw x and y lists
    ax.clear()
    ax.plot(time_plot, theta1_plot)
    ax.grid(True, which='both')

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)


# animation function.  This is called sequentially
# def animate(i):
#     global time_plot, theta1_plot
#     make_move()
#
#     # Limit x and y lists to 20 items
#     time_plot = time_plot[-500:]
#     theta1_plot = theta1_plot[-500:]
#     line.set_data(time_plot, theta1_plot)
#     return line,

plt.autoscale(False, 'x')
ani = animation.FuncAnimation(fig, animate, fargs=(time_plot, theta1_plot), interval=dt)
# anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=100, interval=dt, blit=True)


plt.show()
