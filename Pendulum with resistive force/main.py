import numpy as np
import matplotlib.pyplot as plt

# d^2 alpha(t) / dt^2 = -psi * d alpha(t) / dt - g/L *sin(alpha(t))
g = 9.81
L = 2
u = 0.3

dt = 0.01
init_alpha = np.radians(10)  # initial position
init_angular_speed = 0

alpha_plot = []
time_plot = []
time = np.arange(0, 10, dt)

sin_comparison = init_alpha * np.cos(np.sqrt(g/L) * time)


# d^2 alpha(t) / dt^2
def get_angular_acceleration(alpha, angular_speed):
    return -u * angular_speed - (g / L) * np.sin(alpha)


def make_move():
    alpha = init_alpha
    angular_speed = init_angular_speed

    for t in time:
        alpha_plot.append(alpha)
        time_plot.append(t)

        alpha += angular_speed * dt
        angular_speed += get_angular_acceleration(alpha, angular_speed) * dt


def make_plot():
    fig, ax = plt.subplots()

    ax.plot(time_plot, alpha_plot, '-b', label = "Motion of the real pendulum")
    ax.plot(time, sin_comparison, '-k', label = "Montion of the ideal mathematical pendulum")

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=3, fancybox=True, shadow=True)
    ax.grid(True, which='both')

    plt.title(r"For u = %.2f and ${\alpha = %.2f ^\circ}$" % (u, np.degrees(init_alpha)))
    plt.xlabel("t[s]")
    plt.ylabel(r"${\alpha[rad]}$")

    plt.show()


make_move()
make_plot()
