
from typing import Callable
from dataclasses import dataclass

from optimization.utils.lib import *
from optimization.utils.sm.vectorfunc import get_lambda, Xn
from optimization.base.mfo import MultiFunctionOpt


@dataclass
class GradientDescent(MultiFunctionOpt):
    ex: Expr
    delta: float
    iterations: int
    e1: float
    e2: float
    def run(self, onStep: Callable[[np.ndarray], None]) -> np.ndarray:
        print(self.ex)

        x = np.copy(self.x_i)
        itr =0        
        d1=self.e1+1
        d2=self.e2+1
        self.pdif = [ sp.diff(self.ex, Xn(i)) for i in range(self.dimension()) ]        
        v = self.f(x)
        while(itr < self.iterations and d1 > self.e1 and d2 > self.e2):
            itr+=1
            x=self.step(x)
            d1 = np.absolute(v- self.f(x))
            d2 = np.linalg.norm(self.gradient(x))
            v=self.f(x)
            onStep(x)
        return x

    def step(self, xs: np.ndarray) -> np.ndarray:
        return np.add(xs, -self.delta*self.gradient(xs))

    def gradient(self, xs: np.ndarray) -> np.ndarray:
        return arr([get_lambda( self.pdif[i], xs.size)(*xs) for i in range(xs.size) ])

    def f(self, xs:np.ndarray) -> float:
        return get_lambda(self.ex, self.dimension())(*xs)