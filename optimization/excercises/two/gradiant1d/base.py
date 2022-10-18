from typing import List, TypeVar
from abc import ABC, abstractmethod
from dataclasses import dataclass

from optimization.utils.lib import *

from optimization.utils.sm.vectorfunc import get_lambda
from optimization.restrictionless.gradient import GradientDescent
import matplotlib.pyplot as plt

T = TypeVar("T", float, Expr, np.ndarray)

@dataclass
class Excercise1D(ABC):
    x_i: float
    delta: float
    iterations: int
    e1: float
    e2: float
    lx: float
    rx: float

    def plot(self, points: List[float]) -> None:
        steps=500
        maxi=1e-9
        mini=1e9
        di = (self.rx-self.lx)/steps
        for i in range(0, steps+1):
            cx = self.f(self.lx+di*i)
            if (cx < mini):
                mini=cx
            if (cx > maxi):
                maxi=cx

        mini-=(maxi-mini)*0.1
        X = np.linspace(self.lx, self.rx, steps)
        Y = self.f(X)
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_xlim(self.lx, self.rx)
        ax.set_ylim(mini, maxi)

        ax.plot(X, Y)
        
        ax.scatter(
            [p for p in points],
            [self.f(p) for p in points],
            c=[i+1 for i in range(len(points))],            
            norm="log",
        )        
        fig.show()       
        
    def on_step(self, points:List[float], x:float):
        if (len(points)< 5):
            print(f"{len(points)}: {x}")
        elif (len(points)%4==0):
            print(f"{len(points)}: {x}")
        points.append(x)

    def run(self)->None:
        g = GradientDescent(
            np.array([self.x_i]),
            self.sf(sp.Symbol('x1')),
            self.delta,
            self.iterations,
            self.e1,
            self.e2,            
        )
        print(f"Iniciando en x_0 = {self.x_i}")
        print(f"Delta = {self.delta}")
        points: List[float]=[self.x_i]
        x=g.run(lambda x: self.on_step(points, x[0]))
        print(f"Termino en {len(points)-1} pasos")
        print(f"x*    = {x[0]}")
        print(f"f(x*) = {self.f(x[0])}")
        self.plot(points)

    @abstractmethod
    def f(self,x:T) -> T:
        pass
    
    @abstractmethod
    def sf(self,x:Expr) -> Expr:
        pass