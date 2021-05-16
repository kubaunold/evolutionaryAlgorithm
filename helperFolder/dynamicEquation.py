from sympy import symbols


# Symbolic Math
# Working with mathematical symbols in a programmatic way,
# instead of working with numerical values in a programmatic way.

# n <= 5
x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')


expr = 2*x1 + x2

#Booth Funtion with global minimum in f(1,3)=0
exprBF = (x1+2*x2-7)**2 + (2*x1 + x2 - 5)**2

print(exprBF.subs(x1,1).subs(x2,3))
# print(expr.subs(x1, 2))