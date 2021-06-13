from sympy import *
from sympy import symbols, lambdify   # for symbolic math
from sympy import Number, NumberSymbol, Symbol
import numpy as np
import matplotlib.pyplot as plt


def variablesInit():
    # n <= 5
    x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')

    return x1, x2, x3, x4, x5


x1, x2, x3, x4, x5 = variablesInit()


class Function():
    """Represent a function class."""

    # x1, x2, x3, x4, x5 = variablesInit()  # variables
    function = None  # function formula
    strFunction = None
    temp = 5
    vXMin = [0.0, 0.0, 0.0, 0.0, 0.0]      # vector of 'x' minimums (cube)
    vXMax = [0.0, 0.0, 0.0, 0.0, 0.0]      # vector of 'x' maximums (cube)
    vXRes = [0, 0, 0, 0, 0]      # vecor of 'x' resolution
    lRests = []     # function restrictions (restrictions)

    lOccVars = []   # list of occuring variables
    n = None        # number of occuring variables

    # def __init__(self):
    #     """Create global variables x1...x5"""
    #     global x1, x2, x3, x4, x5
    #     x1, x2, x3, x4, x5 = variablesInit()

    def getSimulationObjectiveAndBounds(self):
        objective = None
        bounds = None

        objective = self.getValueAt # przekaż uchwyt do tej funkcji - bez '()'
        
        if self.n == 1:  # 2D function
            x1min = self.vXMin[0]
            x1max = self.vXMax[0]
            bounds = np.asarray([[x1min, x1max]])
        elif self.n == 2:  # 3D function
            x1min = self.vXMin[0]
            x1max = self.vXMax[0]
            x2min = self.vXMin[0]
            x2max = self.vXMax[0]
            bounds = np.asarray([[x1min, x1max], [x2min, x2max]])


        return objective, bounds

    def funToString(self) -> str:
        return str(self.function)

    def parseFunction(self, functionString):
        """Parses a function and fills 'function' and 'strFunction'"""
        self.strFunction = functionString
        self.function = eval(self.strFunction)

    def getValueAt(self, point) -> float:
        N = self.n
        value = None

        if N == 1:  # this is a 2D function
            x = point
            value = self.function.subs(x1,x)
        if N == 2:  # it's a 3D function!
            x, y = point
            value = self.function.subs(x1, x).subs(x2, y)
        
        return value

    def create2DAxes(self):
        x1min = self.vXMin[0]
        x1max = self.vXMax[0]
        x1res = self.vXRes[0]

        X = np.linspace(x1min, x1max, num=x1res)
        # Y = [self.function.subs(x1, x) for x in X]
        f = self.makeF2D()
        Y = f(X)

        return X, Y

    def create3DAxes(self):
        x1min = self.vXMin[0]
        x1max = self.vXMax[0]
        x1res = self.vXRes[0]
        X = np.linspace(x1min, x1max, num=x1res)

        x2min = self.vXMin[1]
        x2max = self.vXMax[1]
        x2res = self.vXRes[1]
        Y = np.linspace(x2min, x2max, num=x2res)

        temp = np.meshgrid(X, Y)
        X, Y = np.meshgrid(X, Y)

        Z = [[self.function.subs(x1, x).subs(x2, y) for x in X] for y in Y]

        # for x in X:
        #     for y in Y:
        #         Z = self.function.
        #     abc = x
        #     print("okay")
        return X, Y, Z

    def makeZ(self):
        x = np.linspace(-6, 6, 30)
        y = np.linspace(-6, 6, 30)

        X, Y = np.meshgrid(x, y)
        Z = self.function.subs([(x, X), (y, Y)])
        return Z
    def makeF2D(self):
        try:
            f = lambdify(x1, self.funToString())
        except Exception as e:
            print(f"Nie mogłem stworzyć funkcji 2D z podanego wzoru. {e}")
        else:
            return f
    def makeF(self):
        try:
            f = lambdify([x1, x2], self.funToString())
        except Exception as e:
            print(f"Nie mogłem stworzyć funkcji 3D z podanego wzoru. {e}")
        else:
            return f

    def make3dgraph(self):
        # plt.clf()
        # plt.cla()
        x1min = self.vXMin[0]
        x1max = self.vXMax[0]
        x1res = self.vXRes[0]
        X = np.linspace(x1min, x1max, num=x1res)

        x2min = self.vXMin[1]
        x2max = self.vXMax[1]
        x2res = self.vXRes[1]
        Y = np.linspace(x2min, x2max, num=x2res)

        X, Y = np.meshgrid(X, Y)
        f = self.makeF()
        Z = f(X, Y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.contour3D(X, Y, Z, 50, cmap='binary')
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.set_zlabel('f(x1,x2)')
        # ax.view_init(60, 35)
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap='viridis', edgecolor='none')
        # ax.set_title('Wykres 3D')

        return fig

    def make_2d_countour_lines(self):
        x1min = self.vXMin[0]
        x1max = self.vXMax[0]
        x1res = self.vXRes[0]
        X = np.linspace(x1min, x1max, num=x1res)

        x2min = self.vXMin[1]
        x2max = self.vXMax[1]
        x2res = self.vXRes[1]
        Y = np.linspace(x2min, x2max, num=x2res)




        X, Y = np.meshgrid(X, Y)
        # Z1 = np.exp(-X**2 - Y**2)
        # Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
        # Z = (Z1 - Z2) * 2

        f = self.makeF()
        Z = f(X, Y)


        fig, ax = plt.subplots()
        CS = ax.contour(X, Y, Z)
        ax.clabel(CS, inline=True, fontsize=10)
        # ax.set_title(f'Warstwice funkcji {self.funToString()}')

        return fig, ax  


    # def __init__(self):
    #     """Initialize function object."""
    #     self.(x1, x2, x3, x4, x5) = 
    # def sit(self):
    #     """Simulate sitting."""
    #     print(f"{self.name} is sitting.")



