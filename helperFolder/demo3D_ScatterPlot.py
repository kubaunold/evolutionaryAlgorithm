
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import array


# data = np.random.randint(0, 255, size=[50, 50, 50])
# x, y, z = data[0], data[1], data[2]
# ax = plt.subplot(111, projection='3d')
ax = plt.subplot(111)

# ax.scatter(x[:10], y[:10], z[:10], c='y')
# ax.scatter(x[10:20], y[10:20], z[10:20], c='r')
# ax.scatter(x[30:40], y[30:40], z[40:50], c='g')



off = [array([-0.82977995,  2.20324493]), array([-4.99885625, -1.97667427]), array([-3.53244109, -4.07661405]), array([-3.13739789, -1.54439273]), array([-1.03232526,  0.38816734])]

# make x, y
x = list()
y = list()
for o in off:
    x.append(o[0])
    y.append(o[1])


ax.scatter(x,y)

# ax.set_zlabel('Z')
ax.set_ylabel('Y')
ax.set_xlabel('X')

plt.show()