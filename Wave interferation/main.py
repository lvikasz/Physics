import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# amplitude of the wave
A = 1

# period of the wave
T = 1.0 # 2200.0

# length of the wave
l = 0.155

# current time
t = 0

# coordinates of first source
x1 = 0
y1 = 0

# coordinates of second source
x2 = 0.5
y2 = 0

def get_amp(X, Y):
    return (A * (np.sin(2*np.pi*((np.sqrt((X - x1)**2 + (Y - y1)**2) / l) - (t / T))) + np.sin(2*np.pi*((np.sqrt((X - x2)**2 + (Y - x1)**2) / l) - (t / T)))))

# plane
X = np.arange(-0.1, 1.7, 0.005)
Y = np.arange(-0.1, 5, 0.005)
X, Y = np.meshgrid(X, Y)

# init
Z = get_amp(X, Y)

# plotting stuff
fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()
p = ax.pcolor(X, Y, Z, cmap=cm.RdBu, vmin=Z.min(), vmax=Z.max())
cb = fig.colorbar(p)
plt.title("Interference of two waves from two sources (with coordinates A(%.2f, %.2f) and B(%.2f, %.2f))" % (x1, y1, x2, y2))
plt.show()

# through time
# while True:
#     print(Z)
#     p = ax.pcolor(X, Y, Z, cmap=cm.RdBu, vmin=Z.min(), vmax=Z.max())
#     # cb = fig.colorbar(p)
#     fig.canvas.draw()
#
#     time.sleep(0.1)
#     t += 0.1
#
#     Z = get_amp(X, Y)