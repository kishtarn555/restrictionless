from optimization.utils.lib import *
from typing import Callable

from dataclasses import dataclass

from optimization.base.lfo import StepAlgorithm

@dataclass
class Bisection(StepAlgorithm):
    df: Callable[[float], float]
    x_a: float
    x_b: float
    max_steps: int
    tolerance: float
    
    def run(self, onStep: Callable[[float], None]) -> float:
        a:float=self.x_a
        b:float=self.x_b
        steps:int=0
        while (b-a > self.tolerance and steps < self.max_steps):
            steps += 1
            m=(a+b)/2
            if (self.df(a)*self.df(m) < 0):
                b=m
            else:
                a=m
            onStep(m)
        return (a+b)/2


    def step(self, x: float) -> float:
        return x


