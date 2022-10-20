from dataclasses import dataclass
from optimization.utils.lib import *
from optimization.utils.plot import get_colors
from typing import List, TypeVar, Any

from optimization.restrictionless.d1.newton import Netwon1D

import matplotlib.pyplot as plt
import matplotlib.colors as plcl

from abc import ABC, abstractmethod
T = TypeVar("T", float, Expr, np.ndarray)

@dataclass
class Excercise(ABC):
    x_a:float
    x_b:float
    x_i: float
    max_steps:int
    tolerance:float
    def run(self):
        points: List[float] = [self.x_i]
        b = Netwon1D(
            self.df,
            self.df2,  
            self.x_i, 
            self.max_steps, 
            self.tolerance)
        print(f"x_{0} = {b.x_i}")
        res=b.run(lambda x: self.on_step(points,x))
        print(f"Termino en {len(points)-1} pasos")
        print(f"   x={res}")
        print(f"f(x)={self.f(res)}")
        self.plot(points)
        return res

    def on_step(self, points:List[float], x:float):
        if (len(points)< 10):
            print(f"x_{len(points)} = {x}")
        elif (len(points)%10==0):
            print(f"x_{len(points)} = {x}")
        points.append(x)

    def plot(self, points:List[float])->None:
        steps=500
        maxi=1e-9
        mini=1e9
        di = (self.x_b-self.x_a)/steps
        for i in range(0, steps+1):
            cx = self.f(self.x_a+di*i)
            if (cx < mini):
                mini=cx
            if (cx > maxi):
                maxi=cx

        mini-=(maxi-mini)*0.1
        X = np.linspace(self.x_a, self.x_b, steps)
        Y = self.f(X)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_title(self.__class__.__name__)
        ax.set_xlim(self.x_a, self.x_b)
        ax.set_ylim(mini, maxi)

        ax.plot(X, Y)
        
        ax.scatter(
            [p for p in points],
            [self.f(p) for p in points],
            c=get_colors(len(points))            
        )        
        fig.show()

    def df(self, x:float) -> float:
        X=sp.Symbol('x')
        expr = self.sf(X)
        return sp.lambdify(X, sp.diff(expr,X))(x)

    @abstractmethod
    def f(self, x:T) -> T:
        pass

    def df2(self, x:T) -> T:
        X=sp.Symbol('x')
        expr = self.sf(X)
        return sp.lambdify(X, sp.diff(sp.diff(expr,X),X))(x)


    @abstractmethod
    def sf(self, x:Expr) -> Expr:
        pass
