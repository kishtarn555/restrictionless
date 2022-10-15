
#**************************************************#
#                                                  #
#      FIXME: THIS FILE IS WRONG, AND OUTDATED     #
#                                                  #
#**************************************************#

# from dataclasses import dataclass
# import numpy as np
# import sympy as sp
# from sympy.utilities import lambdify
# from sympy.parsing import parse_expr
# from sympy.core.expr import Expr
# from abc import ABC, abstractmethod
# arr = np.array
# @dataclass
# class Levenberg(ABC):
#     x_i: np.ndarray
#     ep1: float
#     ep2: float
    
#     def run(self) -> np.ndarray:
#         d1= self.ep1+10
#         d2= self.ep2+10
#         x = np.copy(self.x_i)
#         while (d1 > self.ep1 and d2 > self.ep2):
#             s = np.matmul(self.hessiana(x), self.gradiente(x))
#             x = np.add(x,s)            
#             print(x)
#             d1-=1
#             d2-=1
#         return x

#     @abstractmethod
#     def f(self, xs: np.ndarray) -> float:
#         pass    

#     @abstractmethod
#     def gradiente(self,xs: np.ndarray) -> np.ndarray:
#         pass

    
#     @abstractmethod
#     def hessiana (self, xs:np.ndarray)-> np.ndarray:
#         pass

# There's too much repeating yourself
# @dataclass
# class SysLevenberg (Levenberg):
#     ex: Expr
#     def f(self, xs: np.ndarray) -> float:   
#         x = [sp.Symbol(f'x{i+1}') for i in range(xs.size)]
#         func = lambdify(x, self.ex)
#         print(func(1,2))
#         return func(*xs)

#     def gradiente(self, xs: np.ndarray) -> np.ndarray:
#         x = [sp.Symbol(f'x{i+1}') for i in range(xs.size)]
#         func = lambdify(x, self.ex)
        
#         return np.arr([sp.diff(func, x[i])(x) for i in range(xs.size)])

#     def hessiana(self, xs: arr) -> np.array:        
#         x = [sp.Symbol(f'x{i+1}') for i in range(xs.size)]
#         func = lambdify(x, self.ex)
#         return np.array([
#             [sp.diff(sp.diff(func, xs[i]),xs[j] ) for j in range(xs.size) ] 
#             for i in range(xs.size)
#         ])     

        

# if (__name__ == "__main__"):
#     e=parse_expr("x1*x1")
#     print(e)
#     input: SysLevenberg =  SysLevenberg(np.array([1,3], np.longdouble), 1e-5, 1e-5, e)
#     print(input.run(np.array([3,6])))

