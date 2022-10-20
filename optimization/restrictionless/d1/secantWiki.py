from optimization.utils.lib import *
from typing import Callable

from dataclasses import dataclass

from optimization.base.lfo import StepAlgorithm

@dataclass
class Secant(StepAlgorithm):
    df: Callable[[float], float]
    x_a: float
    x_b: float
    max_steps: int
    tolerance: float
    
    def run(self, onStep: Callable[[float], None]) -> float:
        a:float=self.x_a
        b:float=self.x_b
        steps:int=0
        m= 0
        while (steps< self.max_steps):
            steps+=1            
            m = a-self.df(a)*(b-a)/((self.df(b)-self.df(a)))
            a=b
            b=m
            onStep(b)
            if (np.abs(a-b)<self.tolerance):
                return m
        return  m


    def step(self, x: float) -> float:
        return x


