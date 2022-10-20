from dataclasses import dataclass
from optimization.utils.lib import *
from typing import List, TypeVar, Any

from optimization.restrictionless.d1.secant import Secant

import matplotlib.pyplot as plt
import matplotlib.colors as plcl

from abc import ABC, abstractmethod
T = TypeVar("T", float, Expr, np.ndarray)

@dataclass
class Excercise(ABC):
    x_a:float
    x_b: float
    max_steps:int
    tolerance:float
    arrow:int
    def run(self):
        points: List[float] = [self.x_a, self.x_b]
        b = Secant(
            self.df,  
            self.x_a, 
            self.x_b, 
            self.max_steps, 
            self.tolerance)

        print(f"a: {self.x_a}")
        print(f"b: {self.x_b}")
        res=b.run(lambda x: self.on_step(points,x))
        print(f"Termino en {len(points)-2} pasos")
        print(f"   x={res}")
        print(f"f(x)={self.f(res)}")
        self.plot(points)
        return res

    def on_step(self, points:List[float], x:float):
        
        print(f"alpha_{len(points)-1}: {x}")
        
        points.append(x)

    def plot(self, points:List[float])->None:
        steps=500
        maxi=1e-9
        mini=1e9
        sa = self.x_a
        sb = self.x_b
        for pt in points:
            if (sa > pt):
                sa=pt
            if (sb < pt):
                sb=pt
        di = (sb-sa)/steps
        for i in range(0, steps+1):
            cx = self.f(sa+di*i)
            if (cx < mini):
                mini=cx
            if (cx > maxi):
                maxi=cx

        mini-=(maxi-mini)*0.1
        X = np.linspace(sa, sb, steps)
        Y = self.f(X)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_xlim(sa, sb)
        ax.set_ylim(mini, maxi)

        ax.plot(X, Y)
        for i, pt in enumerate(points):
            color = "green"
            if (i <2):
                color = "blue"
            elif (i == len(points)-1):
                color = "red"
            ax.scatter(pt,self.f(pt), c=color)
        
        fig.show()

    def df(self, x:float) -> float:
        X=sp.Symbol('x')
        expr = self.sf(X)
        return sp.lambdify(X, sp.diff(expr,X))(x)

    @abstractmethod
    def f(self, x:T) -> T:
        pass


    @abstractmethod
    def sf(self, x:Expr) -> Expr:
        pass
