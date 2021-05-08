import matplotlib.pyplot as plt
# plt.style.use('seaborn-white')
import numpy as np
# import time

def f(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

x_axis = np.linspace(0, 5, 50)
y_axis = np.linspace(0, 5, 40)

[X, Y] = np.meshgrid(x_axis, y_axis)

fig, ax = plt.subplots(1,1)
Z = f(X, Y)
ax.contourf(X, Y, Z) 
ax.set_title('Contour Plot') 
ax.set_xlabel('x_axis') 
ax.set_ylabel('y_axis')
plt.show()

# plt.contour(X, Y, Z, colors='black');

# plt.contour(X, Y, Z, 20, cmap='RdGy')
# plt.cm.<TAB>

# plt.contourf(X, Y, Z, 20, cmap='RdGy')
# plt.colorbar();


# plt.imshow(Z, extent=[0, 5, 0, 5], origin='lower',
#            cmap='RdGy')
# plt.colorbar()
# plt.axis(aspect='image');
