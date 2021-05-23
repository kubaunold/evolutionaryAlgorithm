# sample 5.py



import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from mpl_toolkits.mplot3d.axes3d import get_test_data


# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))

#===============
#  First subplot
#===============
# set up the axes for the first plot
ax = fig.add_subplot(2, 2, 1, projection='3d')

# plot a 3D surface like in the example mplot3d/surface3d_demo
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)
fig.colorbar(surf, shrink=0.5, aspect=10)

#===============
# Second subplot
#===============
# set up the axes for the second plot
ax = fig.add_subplot(2, 2, 2, projection='3d')

# plot a 3D wireframe like in the example mplot3d/wire3d_demo
X, Y, Z = get_test_data(0.05)
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)


#===============
# Third subplot
#===============
# set up the axes for the second plot
ax = fig.add_subplot(2, 2, 3, projection='3d')

# plot a 3D surface like in the example mplot3d/surface3d_demo
# X = np.arange(0, 4, 0.25)
# Y = np.arange(-10, 10, 0.25)
X = np.linspace(-3, 5, 100)
Y = np.linspace(-3, 5, 100)

XX, YY = np.meshgrid(X, Y)
# Z = (XX+2*YY-7)**2 + (2*XX + YY - 5)**2
Z = (9 - XX - YY)/2
surf = ax.plot_surface(XX, YY, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)
fig.colorbar(surf, shrink=0.5, aspect=10)

#===============
# Fourth subplot
#===============
# set up the axes for the second plot
ax = fig.add_subplot(2, 2, 4, projection='3d')

# plot a 3D surface like in the example mplot3d/surface3d_demo
# X = np.arange(0, 4, 0.25)
# Y = np.arange(-10, 10, 0.25)
X = np.linspace(-3, 5, 100)
Y = np.linspace(-3, 5, 100)

XX, YY = np.meshgrid(X, Y)
Z = (XX+2*YY-7)**2 + (2*XX + YY - 5)**2
# Z = (9 - XX - YY)/2
# surf = ax.plot_surface(XX, YY, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
#                         linewidth=0, antialiased=False)
surf = ax.plot_surface(XX, YY, Z, alpha=0.5, rstride=1, cstride=1, cmap=cm.coolwarm)
fig.colorbar(surf)


plt.show()