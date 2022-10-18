from optimization.utils.lib import *
from typing import Callable

from dataclasses import dataclass

from optimization.base.lfo import StepAlgorithm

@dataclass
class Polinomial(StepAlgorithm):    
    f: Callable[[float], float]
    df: Callable[[float], float]
    x_a: float
    x_b: float
    max_steps: int
    tolerance: float
    
    def run(self, onStep: Callable[[float], None]) -> float:
        a:float=self.x_a
        b:float=self.x_b
        steps:int=0
        while (True):
            steps += 1
            m=(a+b)/2
            onStep(m)
            if (self.df(a)*self.df(m) < 0):
                b=m
                break
            else:
                a=m

        steps=0
        xt=0
        while (steps < self.max_steps):
            steps+=1
            xt = self.xt(a,b)
            onStep(xt)
            if (np.abs(self.df(xt)) < self.tolerance):
                break

            
            if (self.df(a)*self.df(xt) < 0):
                b=xt
            else:
                a=xt
        return xt
        
        return (a+b)/2

    def xt(self, x1, x2):
        m = self.mu(x1,x2)
        if (m <0):
            return x2
        if (m >1):
            return x1
        return x2-m*(x2-x1)
        
    def mu(self, x1,x2):
        w=self.w(x1,x2)
        z=self.z(x1,x2)
        return (self.df(x2)+w-z)/( self.df(x2)-self.df(x1)+2*w)

    def w(self, x1, x2):
        return (x2-x1)/np.abs(x2-x1)+np.sqrt(self.z(x1,x2)**2-self.df(x1)*self.df(x2))

    def z(self, x1, x2):
        return 3*(self.f(x1)-self.f(x2))/(x2-x1)+self.df(x1)+self.df(x2)
    def step(self, x: float) -> float:
        return x


