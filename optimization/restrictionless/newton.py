
from typing import Callable
from dataclasses import dataclass

from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import get_lambda

from optimization.utils.sm.vectorfunc import get_lambda, Xn
from optimization.utils.sm.hessian import hessian as shessian
from optimization.base.mfo import MultiFunctionOpt

@dataclass
class Newton (MultiFunctionOpt):
    ep1: float
    ep2: float
    delta: float
    ex: Expr
    
    def run(self, onStep:Callable[[arr], None]) -> arr:
        d1= self.ep1+10
        d2= self.ep2+10
        x = np.copy(self.x_i)
        v = self.f(x)
        while (d1 > self.ep1 and d2 > self.ep2):
            d2= np.linalg.norm(self.gradient(x))
            x=self.step(x)
            d1=np.absolute(v-self.f(x))
            v=self.f(x)
            onStep(x)
        return x


    def step(self, x: arr) -> arr:
        s = -np.matmul(
            np.linalg.inv(
                self.hessian(x)
                ), 
            self.gradient(x))
        return np.add(x,self.delta*s)            

    def _func(self) -> SFunction:
        return get_lambda(self.ex, self.x_i.size)

    def f(self, xs: arr) -> float:   
        return self._func()(*xs)

    def gradient(self, xs: arr) -> arr:
        return arr(
            [
                get_lambda(sp.diff( self.ex, Xn(i)),xs.size)(*xs) 
                for i in range(xs.size)
            ]
        )

    def hessian(self, xs: arr) -> np.array:        
        return shessian(self.ex, xs)    

    
