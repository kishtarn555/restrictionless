from sympy import Symbol
from sympy.core.expr import Expr
from sympy.core.function import FunctionClass
from sympy import lambdify

def get_lambda(e: Expr, dimensions: int) -> FunctionClass:
    x = [Xn(i) for i in range(dimensions)]
    return lambdify(x, e)

def Xn(i:int) -> Symbol:
    return Symbol(f"x{i+1}")





