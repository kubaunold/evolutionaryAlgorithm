from sympy import symbols, lambdify   # for symbolic math
from sympy import Number, NumberSymbol, Symbol
import numpy as np

def variablesInit():
    # n <= 5
    x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')

    return x1, x2, x3, x4, x5

x1,x2,x3,x4,x5 = variablesInit()


class Function():
    """Represent a function class."""

    # x1, x2, x3, x4, x5 = variablesInit()  # variables
    function = None # function formula
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

    def parseFunction(self, functionString):
        """Parses a function and fills 'function' and 'strFunction'"""
        self.strFunction = functionString
        self.function = eval(self.strFunction)

    def create2DAxes(self):
        x1min = self.vXMin[0]
        x1max = self.vXMax[0]
        x1res = self.vXRes[0]

        X = np.linspace(x1min, x1max, num=x1res)
        Y = [self.function.subs(x1, x) for x in X]
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

        Z = [[self.function.subs(x1,x).subs(x2,y) for x in X] for y in Y]

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
    
    def makeF(self):
        try:
            f = lambdify([x1, x2], self.strFunction)
        except Exception as e:
            print(f"Nie mogłem stworzyć funkcji z podanego wzoru. {e}")

        return f

    # def __init__(self):
    #     """Initialize function object."""
    #     self.(x1, x2, x3, x4, x5) = 
    # def sit(self):
    #     """Simulate sitting."""
    #     print(f"{self.name} is sitting.")



